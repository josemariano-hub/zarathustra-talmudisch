#!/usr/bin/env python3
"""
Landing-ellipse reconstruction for a high-altitude balloon payload.

Takes flight telemetry (time, lat, lon, altitude), finds burst, models the descent
through a real wind profile, and Monte-Carlos the uncertainties into a landing
ellipse exported as GeoJSON ready to hand to an imagery provider as an AOI.

    python3 descent_reconstruction.py telemetry.csv --mass 3.0 --out landing

Telemetry columns are auto-detected. Anything resembling time/lat/lon/alt works
(e.g. UBX, APRS exports, Spot/Iridium logs, SondeHub CSV).

Winds come from the Open-Meteo archive (ERA5, free, no key). If the flight is too
recent for ERA5 or you are offline, pass --winds winds.csv with columns
    altitude_m,u_ms,v_ms
where u is eastward and v is northward.

SI units throughout.
"""
from __future__ import annotations
import argparse, csv, json, math, sys, urllib.parse, urllib.request
from datetime import datetime, timezone

import numpy as np

# ----------------------------------------------------------------- constants
G0      = 9.80665       # m/s^2
R_AIR   = 287.053       # J/(kg K)
R_EARTH = 6371008.8     # m

# ISA layers: (base geopotential alt m, base temp K, lapse rate K/m, base pressure Pa)
ISA = [
    (0,     288.15, -0.0065, 101325.0),
    (11000, 216.65,  0.0,     22632.1),
    (20000, 216.65,  0.001,    5474.89),
    (32000, 228.65,  0.0028,    868.019),
    (47000, 270.65,  0.0,       110.906),
]

def isa_density(h: float) -> float:
    """ISA air density (kg/m^3) at geometric altitude h (m). Valid to ~47 km."""
    h = max(0.0, min(h, 47000.0))
    for i, (hb, tb, lr, pb) in enumerate(ISA):
        ht = ISA[i + 1][0] if i + 1 < len(ISA) else 47000.0
        if h <= ht or i == len(ISA) - 1:
            if abs(lr) < 1e-12:
                t = tb
                p = pb * math.exp(-G0 * (h - hb) / (R_AIR * tb))
            else:
                t = tb + lr * (h - hb)
                p = pb * (t / tb) ** (-G0 / (R_AIR * lr))
            return p / (R_AIR * t)
    raise RuntimeError("unreachable")


# ----------------------------------------------------------------- telemetry
ALIASES = {
    "time": ["time", "timestamp", "datetime", "utc", "date_time", "gps_time", "epoch", "t"],
    "lat":  ["lat", "latitude", "gps_lat", "lat_deg"],
    "lon":  ["lon", "long", "longitude", "lng", "gps_lon", "lon_deg"],
    "alt":  ["alt", "altitude", "alt_m", "height", "gps_alt", "altitude_m", "hgt", "elevation"],
}

def _match(header: list[str], key: str) -> str | None:
    low = {h.lower().strip(): h for h in header}
    for a in ALIASES[key]:
        if a in low:
            return low[a]
    for a in ALIASES[key]:                       # substring fallback
        for h_low, h in low.items():
            if a in h_low:
                return h
    return None

def _parse_time(v: str) -> float:
    v = v.strip()
    try:
        return float(v) if float(v) > 1e8 else float("nan")   # epoch seconds
    except ValueError:
        pass
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S", "%H:%M:%S"):
        try:
            dt = datetime.strptime(v.replace("Z", "+0000"), fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.timestamp()
        except ValueError:
            continue
    return float("nan")

def load_telemetry(path: str):
    with open(path, newline="", encoding="utf-8-sig") as f:
        sample = f.read(8192); f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t ")
        except csv.Error:
            dialect = csv.excel
        rows = list(csv.DictReader(f, dialect=dialect))
    if not rows:
        sys.exit(f"no rows in {path}")
    header = list(rows[0].keys())
    cols = {k: _match(header, k) for k in ALIASES}
    missing = [k for k in ("lat", "lon", "alt") if cols[k] is None]
    if missing:
        sys.exit(f"could not find column(s) {missing} in header: {header}")
    print(f"  columns: " + ", ".join(f"{k}<-{v}" for k, v in cols.items() if v))

    t, lat, lon, alt = [], [], [], []
    for r in rows:
        try:
            la, lo, al = float(r[cols["lat"]]), float(r[cols["lon"]]), float(r[cols["alt"]])
        except (TypeError, ValueError):
            continue
        if not (-90 <= la <= 90 and -180 <= lo <= 180):
            continue
        t.append(_parse_time(r[cols["time"]]) if cols["time"] else float("nan"))
        lat.append(la); lon.append(lo); alt.append(al)

    t, lat, lon, alt = map(np.asarray, (t, lat, lon, alt))
    if np.all(np.isnan(t)):                       # synthesise a 1 Hz clock
        t = np.arange(len(lat), dtype=float)
    else:                                         # fill gaps by interpolation
        idx = np.arange(len(t))
        good = ~np.isnan(t)
        t = np.interp(idx, idx[good], t[good])
    order = np.argsort(t)
    return t[order], lat[order], lon[order], alt[order]


# ----------------------------------------------------------------- winds
PRESSURE_LEVELS = [1000, 975, 950, 925, 900, 850, 800, 700, 600, 500,
                   400, 300, 250, 200, 150, 100, 70, 50, 30]

def fetch_winds(lat: float, lon: float, when: datetime):
    """Pull an ERA5 wind profile from Open-Meteo. Returns (alt_m, u, v) ascending."""
    hourly = []
    for p in PRESSURE_LEVELS:
        hourly += [f"wind_speed_{p}hPa", f"wind_direction_{p}hPa", f"geopotential_height_{p}hPa"]
    q = urllib.parse.urlencode({
        "latitude": f"{lat:.4f}", "longitude": f"{lon:.4f}",
        "start_date": when.strftime("%Y-%m-%d"), "end_date": when.strftime("%Y-%m-%d"),
        "hourly": ",".join(hourly), "timezone": "UTC", "wind_speed_unit": "ms",
    })
    url = f"https://archive-api.open-meteo.com/v1/archive?{q}"
    with urllib.request.urlopen(url, timeout=60) as r:
        data = json.loads(r.read())
    if data.get("error"):
        raise RuntimeError(data.get("reason", "open-meteo error"))
    h = data["hourly"]
    k = min(range(len(h["time"])),
            key=lambda i: abs(datetime.fromisoformat(h["time"][i]).replace(
                tzinfo=timezone.utc).timestamp() - when.timestamp()))
    alts, us, vs = [], [], []
    for p in PRESSURE_LEVELS:
        spd, dr, gh = (h.get(f"wind_speed_{p}hPa"), h.get(f"wind_direction_{p}hPa"),
                       h.get(f"geopotential_height_{p}hPa"))
        if not spd or spd[k] is None or gh[k] is None:
            continue
        # meteorological direction = where wind comes FROM
        th = math.radians(dr[k])
        alts.append(float(gh[k]))
        us.append(-spd[k] * math.sin(th))
        vs.append(-spd[k] * math.cos(th))
    if len(alts) < 4:
        raise RuntimeError("too few wind levels returned")
    o = np.argsort(alts)
    return np.asarray(alts)[o], np.asarray(us)[o], np.asarray(vs)[o]

def load_winds_csv(path: str):
    a, u, v = [], [], []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            r = {k.lower().strip(): val for k, val in r.items()}
            a.append(float(r["altitude_m"])); u.append(float(r["u_ms"])); v.append(float(r["v_ms"]))
    o = np.argsort(a)
    return np.asarray(a)[o], np.asarray(u)[o], np.asarray(v)[o]

def winds_from_ascent(t, lat, lon, alt, i_burst):
    """
    Fallback with no external data: the ascent itself is a wind sonde.
    Differentiating the balloon's own horizontal track gives the profile it flew through.
    """
    sl = slice(0, max(3, i_burst))
    a, la, lo, tt = alt[sl], lat[sl], lon[sl], t[sl]
    if len(a) < 4:
        raise RuntimeError("not enough ascent data to derive winds")
    mlat = math.radians(float(np.mean(la)))
    x = np.radians(lo) * R_EARTH * math.cos(mlat)
    y = np.radians(la) * R_EARTH
    dt = np.gradient(tt)
    dt[dt == 0] = 1e-6
    u, v = np.gradient(x) / dt, np.gradient(y) / dt
    # bin into 250 m shells and take the median to suppress GPS jitter
    bins = np.arange(a.min(), a.max() + 250, 250)
    idx = np.digitize(a, bins) - 1
    A, U, V = [], [], []
    for b in range(len(bins) - 1):
        m = idx == b
        if m.sum() >= 2:
            A.append(0.5 * (bins[b] + bins[b + 1]))
            U.append(float(np.median(u[m]))); V.append(float(np.median(v[m])))
    if len(A) < 4:
        raise RuntimeError("ascent too sparse to derive winds")
    return np.asarray(A), np.asarray(U), np.asarray(V)


# ----------------------------------------------------------------- descent
def descend(lat0, lon0, alt0, wind, mass, cda, ground_alt, wind_scale=1.0,
            wind_bias=(0.0, 0.0), dt=1.0):
    """
    Integrate the fall from (lat0, lon0, alt0) to ground_alt.
    Terminal velocity each step: v = sqrt(2 m g / (rho * CdA)).
    Horizontal motion is assumed to track the local wind (valid for a light,
    high-drag body: relaxation time is seconds, descent takes many minutes).
    """
    wa, wu, wv = wind
    lat, lon, h = lat0, lon0, alt0
    mlat = math.radians(lat0)
    t = 0.0
    while h > ground_alt and t < 4 * 3600:
        rho = isa_density(h)
        v = math.sqrt(2.0 * mass * G0 / (rho * cda))
        u = float(np.interp(h, wa, wu)) * wind_scale + wind_bias[0]
        vv = float(np.interp(h, wa, wv)) * wind_scale + wind_bias[1]
        step = min(dt, (h - ground_alt) / max(v, 1e-3))
        lon += math.degrees(u * step / (R_EARTH * math.cos(mlat)))
        lat += math.degrees(vv * step / R_EARTH)
        h -= v * step
        t += step
    return lat, lon, t


def monte_carlo(lat0, lon0, alt0, wind, mass, cda, ground_alt, n=3000, seed=1):
    """Perturb drag, wind magnitude, and wind direction; return landing scatter."""
    rng = np.random.default_rng(seed)
    lats, lons, times = [], [], []
    for _ in range(n):
        cda_i   = cda * float(rng.normal(1.0, 0.20))            # 20% drag uncertainty
        cda_i   = max(cda_i, 0.05 * cda)
        scale_i = float(rng.normal(1.0, 0.15))                  # 15% wind speed error
        bias    = (float(rng.normal(0, 1.5)), float(rng.normal(0, 1.5)))  # m/s residual
        la, lo, tt = descend(lat0, lon0, alt0, wind, mass, cda_i, ground_alt, scale_i, bias)
        lats.append(la); lons.append(lo); times.append(tt)
    return np.asarray(lats), np.asarray(lons), np.asarray(times)


def ellipse_from_scatter(lats, lons, conf=0.95):
    """Covariance ellipse of the landing scatter, returned in metres and degrees."""
    mlat = math.radians(float(np.mean(lats)))
    x = (lons - np.mean(lons)) * 111320.0 * math.cos(mlat)
    y = (lats - np.mean(lats)) * 110540.0
    cov = np.cov(np.vstack([x, y]))
    evals, evecs = np.linalg.eigh(cov)
    order = np.argsort(evals)[::-1]
    evals, evecs = evals[order], evecs[:, order]
    k = -2.0 * math.log(1.0 - conf)                    # chi-square, 2 dof
    a, b = math.sqrt(max(evals[0], 0) * k), math.sqrt(max(evals[1], 0) * k)
    ang = math.atan2(evecs[1, 0], evecs[0, 0])
    return float(np.mean(lats)), float(np.mean(lons)), a, b, ang

def ellipse_polygon(clat, clon, a, b, ang, n=128):
    mlat = math.radians(clat)
    pts = []
    for i in range(n + 1):
        th = 2 * math.pi * i / n
        x = a * math.cos(th) * math.cos(ang) - b * math.sin(th) * math.sin(ang)
        y = a * math.cos(th) * math.sin(ang) + b * math.sin(th) * math.cos(ang)
        pts.append([clon + x / (111320.0 * math.cos(mlat)), clat + y / 110540.0])
    return pts


# ----------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("telemetry", help="CSV of flight telemetry")
    ap.add_argument("--mass", type=float, default=3.0, help="descending mass, kg")
    ap.add_argument("--cda", type=float, default=None,
                    help="drag area Cd*A, m^2. Default: a 0.70 m sphere, Cd=0.5")
    ap.add_argument("--ground-alt", type=float, default=700.0,
                    help="terrain elevation at the landing area, m (Meseta ~700)")
    ap.add_argument("--winds", help="wind profile CSV: altitude_m,u_ms,v_ms")
    ap.add_argument("--n", type=int, default=3000, help="Monte Carlo samples")
    ap.add_argument("--out", default="landing", help="output basename")
    args = ap.parse_args()

    cda = args.cda if args.cda is not None else 0.5 * math.pi * 0.35 ** 2

    print("Loading telemetry...")
    t, lat, lon, alt = load_telemetry(args.telemetry)
    i_burst = int(np.argmax(alt))
    i_last  = len(alt) - 1
    print(f"  {len(alt)} fixes")
    print(f"  burst      : {alt[i_burst]:8.0f} m at {lat[i_burst]:.5f}, {lon[i_burst]:.5f}")
    print(f"  last fix   : {alt[i_last]:8.0f} m at {lat[i_last]:.5f}, {lon[i_last]:.5f}")
    if i_last <= i_burst:
        print("  ! telemetry ends at or before burst - propagating the whole descent")
        i_start = i_burst
    else:
        i_start = i_last
    if alt[i_start] <= args.ground_alt + 50:
        print("\n  Telemetry already reaches the ground. Landing site is the last fix:")
        print(f"    {lat[i_start]:.6f}, {lon[i_start]:.6f}")

    print("\nWind profile...")
    wind = None
    if args.winds:
        wind = load_winds_csv(args.winds); print(f"  from {args.winds}")
    else:
        when = datetime.fromtimestamp(float(t[i_start]), tz=timezone.utc)
        try:
            wind = fetch_winds(float(lat[i_start]), float(lon[i_start]), when)
            print(f"  ERA5 via Open-Meteo, {when:%Y-%m-%d %H:%M}Z, {len(wind[0])} levels")
        except Exception as e:
            print(f"  ! Open-Meteo unavailable ({e})")
            try:
                wind = winds_from_ascent(t, lat, lon, alt, i_burst)
                print(f"  using the balloon's own ascent as a wind sonde, {len(wind[0])} levels")
            except Exception as e2:
                sys.exit(f"  ! no wind profile available ({e2}). Supply one with --winds.")

    print(f"\nDescent model: mass {args.mass} kg, CdA {cda:.4f} m^2, ground {args.ground_alt} m")
    v_top = math.sqrt(2 * args.mass * G0 / (isa_density(alt[i_start]) * cda))
    v_gnd = math.sqrt(2 * args.mass * G0 / (isa_density(args.ground_alt) * cda))
    print(f"  terminal velocity: {v_top:6.1f} m/s at release, {v_gnd:5.1f} m/s at impact")
    if v_gnd > 12:
        print("  ! impact speed is high - consider whether the sphere survived intact")

    la, lo, tt = descend(float(lat[i_start]), float(lon[i_start]), float(alt[i_start]),
                         wind, args.mass, cda, args.ground_alt)
    print(f"  nominal landing: {la:.6f}, {lo:.6f}  after {tt/60:.1f} min")

    print(f"\nMonte Carlo, {args.n} samples...")
    mlats, mlons, mtimes = monte_carlo(float(lat[i_start]), float(lon[i_start]),
                                       float(alt[i_start]), wind, args.mass, cda,
                                       args.ground_alt, n=args.n)
    feats = []
    for conf, name in ((0.50, "50%"), (0.95, "95%")):
        clat, clon, a, b, ang = ellipse_from_scatter(mlats, mlons, conf)
        area = math.pi * a * b / 1e6
        print(f"  {name} ellipse: {2*a:7.0f} x {2*b:6.0f} m,  {area:7.2f} km^2, "
              f"bearing {(90 - math.degrees(ang)) % 180:5.1f} deg")
        feats.append({
            "type": "Feature",
            "properties": {"name": f"landing ellipse {name}", "confidence": conf,
                           "area_km2": round(area, 3),
                           "semi_major_m": round(a, 1), "semi_minor_m": round(b, 1)},
            "geometry": {"type": "Polygon",
                         "coordinates": [ellipse_polygon(clat, clon, a, b, ang)]},
        })

    clat, clon, a, b, ang = ellipse_from_scatter(mlats, mlons, 0.95)
    feats.insert(0, {
        "type": "Feature",
        "properties": {"name": "nominal landing point",
                       "descent_minutes": round(tt / 60, 1),
                       "impact_speed_ms": round(v_gnd, 1)},
        "geometry": {"type": "Point", "coordinates": [lo, la]},
    })
    # square AOI for tasking - providers prefer simple polygons
    pad = 1.15 * a
    mlat_r = math.radians(clat)
    dlon, dlat = pad / (111320.0 * math.cos(mlat_r)), pad / 110540.0
    aoi = [[clon - dlon, clat - dlat], [clon + dlon, clat - dlat],
           [clon + dlon, clat + dlat], [clon - dlon, clat + dlat], [clon - dlon, clat - dlat]]
    aoi_km2 = (2 * pad / 1000.0) ** 2
    feats.append({
        "type": "Feature",
        "properties": {"name": "tasking AOI", "area_km2": round(aoi_km2, 2)},
        "geometry": {"type": "Polygon", "coordinates": [aoi]},
    })
    print(f"  tasking AOI  : {2*pad/1000:.2f} x {2*pad/1000:.2f} km = {aoi_km2:.1f} km^2")

    gj = f"{args.out}.geojson"
    with open(gj, "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": feats}, f, indent=1)
    scat = f"{args.out}_scatter.csv"
    with open(scat, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["lat", "lon", "descent_s"])
        for p in zip(mlats, mlons, mtimes):
            w.writerow([f"{p[0]:.6f}", f"{p[1]:.6f}", f"{p[2]:.0f}"])
    print(f"\nWrote {gj} and {scat}")
    print("Drop the .geojson into geojson.io or QGIS, and send the tasking AOI to the provider.")


if __name__ == "__main__":
    main()
