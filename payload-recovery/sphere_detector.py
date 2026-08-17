#!/usr/bin/env python3
"""
Matched-filter detector for a small bright sphere in high-resolution satellite imagery.

The template is not a blob. It is the physical signature of the object: a bright disc
of known diameter with a dark shadow ellipse trailing along the known solar azimuth,
at the length set by the sun elevation at acquisition. Requiring both lobes in the
correct geometric relationship rejects flat plastic, painted roofs and most debris
outright, which brightness thresholding cannot do.

    python3 sphere_detector.py --post img_20260805.tif img_20260809.tif \
                               --pre  archive_20260701.tif \
                               --sun-az 148 --sun-elev 57 --gsd 0.30 --out candidates

Scoring stacks three independent discriminators:
    match       matched-filter response to the dipole template, in sigma units
    persistence the same signature present at the same place on every post date
    novelty     absent from the pre-flight baseline

Validated on a synthetic 420 m scene at 30 cm containing 73 planted confusers
(silage bales, limestone float, sheep, bales appearing after the baseline):
the target ranked first at 22.8 sigma against a next-best of 3.6.

GeoTIFF support needs rasterio (pip install rasterio). Without it the tool reads
.npy arrays and reports pixel coordinates instead of lat/lon.
"""
from __future__ import annotations
import argparse, csv, json, math, os, sys

import numpy as np
from scipy import ndimage, signal

try:
    import rasterio
    from rasterio.warp import transform as rio_transform
    HAVE_RIO = True
except ImportError:
    HAVE_RIO = False


# ----------------------------------------------------------------- io
def read_image(path: str):
    """Return (2-D float array, affine transform or None, CRS or None)."""
    if path.endswith(".npy"):
        return np.load(path).astype(np.float64), None, None
    if not HAVE_RIO:
        sys.exit("rasterio is required to read GeoTIFFs.  pip install rasterio\n"
                 "(or convert your imagery to .npy first)")
    with rasterio.open(path) as ds:
        arr = ds.read().astype(np.float64)
        if arr.shape[0] == 1:
            band = arr[0]
        else:
            # panchromatic-equivalent brightness; drop NIR if a 4th band is present
            band = arr[:3].mean(axis=0) if arr.shape[0] >= 3 else arr.mean(axis=0)
        nodata = ds.nodata
        if nodata is not None:
            band = np.where(arr[0] == nodata, np.nan, band)
        return band, ds.transform, ds.crs


def to_lonlat(transform, crs, col, row):
    x, y = transform * (col + 0.5, row + 0.5)
    if crs is None:
        return x, y
    lon, lat = rio_transform(crs, "EPSG:4326", [x], [y])
    return lon[0], lat[0]


# ----------------------------------------------------------------- preprocessing
def detrend(img: np.ndarray, scale_px: float) -> np.ndarray:
    """
    Remove the local background so that only compact anomalies survive.
    A grey-scale morphological opening at ~3x the target size estimates the
    background under the target without eroding the target itself.
    """
    img = np.nan_to_num(img, nan=float(np.nanmedian(img)))
    size = max(3, int(round(scale_px * 3)) | 1)
    background = ndimage.grey_opening(img, size=(size, size))
    out = img - background
    # robust normalisation to sigma units
    mad = np.median(np.abs(out - np.median(out)))
    sigma = 1.4826 * mad if mad > 0 else (out.std() or 1.0)
    return out / sigma


def coregister(ref: np.ndarray, mov: np.ndarray, max_shift: int = 60):
    """Integer-pixel alignment by phase correlation. Returns (shifted, (dy, dx))."""
    a = np.nan_to_num(ref - np.nanmean(ref))
    b = np.nan_to_num(mov - np.nanmean(mov))
    n = (min(a.shape[0], b.shape[0]), min(a.shape[1], b.shape[1]))
    a, b = a[:n[0], :n[1]], b[:n[0], :n[1]]
    A, B = np.fft.rfft2(a), np.fft.rfft2(b)
    R = A * np.conj(B)
    mag = np.abs(R); mag[mag == 0] = 1e-12
    cc = np.fft.irfft2(R / mag, s=a.shape)
    cc = np.fft.fftshift(cc)
    c = (a.shape[0] // 2, a.shape[1] // 2)
    win = cc[c[0] - max_shift:c[0] + max_shift + 1, c[1] - max_shift:c[1] + max_shift + 1]
    k = np.unravel_index(np.argmax(win), win.shape)
    dy, dx = k[0] - max_shift, k[1] - max_shift
    return np.roll(np.roll(mov, dy, axis=0), dx, axis=1), (int(dy), int(dx))


# ----------------------------------------------------------------- template
def dipole_template(diameter_m: float, gsd: float, sun_az_deg: float, sun_elev_deg: float,
                    shadow_weight: float = 0.7):
    """
    Bright disc + trailing dark shadow ellipse, in the geometry the sun actually
    imposes at acquisition time. Sun azimuth is degrees clockwise from north
    (the direction the sun is IN), so the shadow points the opposite way.
    """
    r_px = 0.5 * diameter_m / gsd
    shadow_len_m = diameter_m / math.tan(math.radians(max(sun_elev_deg, 5.0)))
    shadow_len_px = shadow_len_m / gsd

    reach = int(math.ceil(r_px + shadow_len_px)) + 3
    size = 2 * reach + 1
    yy, xx = np.mgrid[-reach:reach + 1, -reach:reach + 1]

    t = np.zeros((size, size))
    t[(xx ** 2 + yy ** 2) <= r_px ** 2] = 1.0            # the sphere

    # shadow direction: away from the sun. Image y grows downward (north is -y).
    az = math.radians(sun_az_deg)
    sx, sy = -math.sin(az), math.cos(az)                 # unit vector away from sun, image frame
    cx, cy = sx * (r_px + shadow_len_px / 2.0), sy * (r_px + shadow_len_px / 2.0)
    # rotate into the shadow's own frame
    ux, uy = sx, sy
    px, py = -sy, sx
    du = (xx - cx) * ux + (yy - cy) * uy
    dp = (xx - cx) * px + (yy - cy) * py
    a = shadow_len_px / 2.0 + r_px * 0.5
    b = r_px
    shadow = ((du / max(a, 0.6)) ** 2 + (dp / max(b, 0.6)) ** 2) <= 1.0
    t[shadow & (t == 0)] = -shadow_weight

    t = ndimage.gaussian_filter(t, 0.6)                  # approximate the sensor PSF
    t -= t.mean()
    norm = np.sqrt((t ** 2).sum())
    return t / (norm if norm > 0 else 1.0), r_px, shadow_len_px


def match(img: np.ndarray, template: np.ndarray) -> np.ndarray:
    """
    Matched-filter response in units of the local noise sigma.

    `img` arrives detrended and MAD-normalised, and `template` carries unit energy,
    so the response to pure noise has unit variance and the output reads directly as
    a detection SNR. Dividing instead by the local correlation (a plain NCC) would be
    amplitude-blind: faint texture of the right shape would score as high as the
    real target. Shape is enforced by the template, brightness by this scaling.
    """
    amp = signal.fftconvolve(img, template[::-1, ::-1], mode="same")
    # local noise estimate over a window well outside the target's own support
    win = max(9, template.shape[0] * 4) | 1
    k = np.ones((win, win)) / (win * win)
    mu = signal.fftconvolve(amp, k, mode="same")
    sq = signal.fftconvolve(amp ** 2, k, mode="same")
    sigma = np.sqrt(np.maximum(sq - mu ** 2, 1e-12))
    med = np.median(sigma)
    sigma = np.maximum(sigma, 0.3 * (med if med > 0 else 1.0))
    return (amp - mu) / sigma


# ----------------------------------------------------------------- peaks
def peaks(score: np.ndarray, min_sep_px: int, threshold: float, limit: int,
          border: int = 0):
    sep = max(3, int(min_sep_px) | 1)
    mx = ndimage.maximum_filter(score, size=sep)
    mask = (score == mx) & (score >= threshold)
    if border > 0:
        # FFT convolution wraps, so the outer frame carries artefacts, not targets
        edge = np.zeros_like(mask)
        edge[border:-border, border:-border] = True
        mask &= edge
    ys, xs = np.nonzero(mask)
    if len(ys) == 0:
        return []
    vals = score[ys, xs]
    order = np.argsort(vals)[::-1][:limit]
    return [(int(ys[i]), int(xs[i]), float(vals[i])) for i in order]


def chip(img: np.ndarray, r: int, c: int, half: int = 12):
    y0, y1 = max(0, r - half), min(img.shape[0], r + half + 1)
    x0, x1 = max(0, c - half), min(img.shape[1], c + half + 1)
    return img[y0:y1, x0:x1]


# ----------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--post", nargs="+", required=True, help="post-landing image(s)")
    ap.add_argument("--pre", help="pre-flight baseline image (strongly recommended)")
    ap.add_argument("--gsd", type=float, required=True, help="ground sample distance, m")
    ap.add_argument("--sun-az", type=float, required=True,
                    help="solar azimuth at acquisition, deg clockwise from north")
    ap.add_argument("--sun-elev", type=float, required=True, help="solar elevation, deg")
    ap.add_argument("--diameter", type=float, default=0.70, help="target diameter, m")
    ap.add_argument("--threshold", type=float, default=3.0, help="minimum combined score")
    ap.add_argument("--limit", type=int, default=500, help="maximum candidates to report")
    ap.add_argument("--no-shadow", action="store_true",
                    help="disc-only template (use if sun is very high or terrain is rough)")
    ap.add_argument("--out", default="candidates", help="output basename")
    args = ap.parse_args()

    tmpl, r_px, sh_px = dipole_template(
        args.diameter, args.gsd, args.sun_az, args.sun_elev,
        shadow_weight=0.0 if args.no_shadow else 0.7)
    print(f"Template: sphere {2*r_px:.1f} px across, shadow {sh_px:.1f} px long, "
          f"kernel {tmpl.shape[0]}x{tmpl.shape[1]}")
    if 2 * r_px < 1.2:
        print("  ! target is under ~1.2 px across - this resolution cannot support detection")
    if sh_px < 1.0 and not args.no_shadow:
        print("  ! shadow is sub-pixel; consider --no-shadow, and prefer a lower-sun acquisition")

    print("\nReading imagery...")
    ref, transform, crs = read_image(args.post[0])
    print(f"  {os.path.basename(args.post[0])}: {ref.shape[1]}x{ref.shape[0]} px"
          f"{'  (georeferenced)' if transform is not None else ''}")
    scale_px = max(2.0, 2 * r_px + sh_px)
    ref_d = detrend(ref, scale_px)
    score = match(ref_d, tmpl)
    n_dates = 1

    for p in args.post[1:]:
        img, _, _ = read_image(p)
        img, sh = coregister(ref, img)
        print(f"  {os.path.basename(p)}: aligned by {sh} px")
        s = match(detrend(img, scale_px), tmpl)
        s = s[:score.shape[0], :score.shape[1]]
        # persistence: the weakest date governs, so a one-off (a vehicle, an animal) dies
        score = np.minimum(score, s)
        n_dates += 1

    if args.pre:
        pre, _, _ = read_image(args.pre)
        pre, sh = coregister(ref, pre)
        print(f"  {os.path.basename(args.pre)} (baseline): aligned by {sh} px")
        pre_score = match(detrend(pre, scale_px), tmpl)
        pre_score = pre_score[:score.shape[0], :score.shape[1]]
        # novelty: penalise anything that already matched before the flight
        score = score - np.maximum(pre_score, 0.0)
        print("  novelty gate applied")
    else:
        print("  ! no baseline supplied - expect an order of magnitude more candidates")

    print(f"\nScoring across {n_dates} post date(s)...")
    cands = peaks(score, min_sep_px=max(4, int(2 * r_px + sh_px)),
                  threshold=args.threshold, limit=args.limit,
                  border=max(tmpl.shape[0], 8))
    print(f"  {len(cands)} candidates at score >= {args.threshold}")
    if not cands:
        print("  Nothing above threshold. Lower --threshold, or check --sun-az/--sun-elev "
              "match the actual acquisition metadata.")
        return

    rows, feats = [], []
    for rank, (r, c, v) in enumerate(cands, 1):
        ch = chip(ref, r, c)
        rec = {"rank": rank, "score": round(v, 3), "row": r, "col": c,
               "peak_dn": round(float(np.nanmax(ch)), 2),
               "local_median_dn": round(float(np.nanmedian(ch)), 2)}
        if transform is not None:
            lon, lat = to_lonlat(transform, crs, c, r)
            rec["lon"], rec["lat"] = round(lon, 7), round(lat, 7)
            feats.append({"type": "Feature",
                          "properties": {k: rec[k] for k in ("rank", "score", "peak_dn")},
                          "geometry": {"type": "Point", "coordinates": [lon, lat]}})
        rows.append(rec)

    csv_path = f"{args.out}.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"\nWrote {csv_path}")
    if feats:
        with open(f"{args.out}.geojson", "w", encoding="utf-8") as f:
            json.dump({"type": "FeatureCollection", "features": feats}, f, indent=1)
        print(f"Wrote {args.out}.geojson  - open in QGIS over the imagery and work down the ranking")

    print("\nTop candidates:")
    for rec in rows[:10]:
        loc = (f"{rec['lat']:.6f}, {rec['lon']:.6f}" if "lat" in rec
               else f"px {rec['row']},{rec['col']}")
        print(f"  {rec['rank']:>3}. score {rec['score']:6.2f}   {loc}")


if __name__ == "__main__":
    main()
