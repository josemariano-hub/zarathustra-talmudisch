#!/usr/bin/env python3
"""
Detectability of a 0.70 m white EPS (porexpan) sphere from orbital optical sensors.
SI units throughout. Nadir viewing assumed (worst case for shadow, best for footprint).
"""
import numpy as np

# ---------------------------------------------------------------- target
D_SPHERE   = 0.70          # m, diameter
R          = D_SPHERE / 2   # m
A_FOOT     = np.pi * R**2   # m^2, occluded/projected ground footprint (nadir)
H_SPHERE   = D_SPHERE       # m, height above ground for shadow (sphere resting on soil)

RHO_EPS_FRESH = 0.80        # broadband VIS reflectance, clean expanded polystyrene
RHO_EPS_DIRTY = 0.60        # after dust / soil contact / partial burial of lower hemisphere

# ---------------------------------------------------------------- backgrounds (central Spain, VIS red band)
BACKGROUNDS = {
    "Bare tilled soil (dark, moist)":      0.13,
    "Bare soil, dry Meseta (typical)":     0.20,
    "Cereal stubble, post-harvest":        0.30,
    "Green irrigated crop (maize/alfalfa)":0.08,
    "Dry pasture / fallow":                0.25,
    "Chalk/gypsum outcrop (worst case)":   0.40,
}

# ---------------------------------------------------------------- sensors
# eff_res: the true optical resolution cell size (m) -> drives how much the signal is diluted.
# pix:     the delivered product pixel spacing (m).
# psf:     peak-retention factor of the point-spread function for a ~2-px target.
# snr:     sensor SNR at typical scene radiance -> noise-equivalent delta reflectance.
SENSORS = {
    "Pleiades Neo (Airbus)":      dict(pix=0.30, eff_res=0.30, psf=0.75, snr=150, bands=6),
    "Pleiades 1A/1B (Airbus)":    dict(pix=0.50, eff_res=0.70, psf=0.60, snr=147, bands=4),
    "SkySat (Planet)":            dict(pix=0.50, eff_res=0.72, psf=0.60, snr=100, bands=5),
    "WorldView-3 / Legion (ref)": dict(pix=0.31, eff_res=0.31, psf=0.75, snr=150, bands=8),
    "PlanetScope SuperDove":      dict(pix=3.00, eff_res=3.70, psf=0.85, snr=120, bands=8),
    "Sentinel-2 (free)":          dict(pix=10.0, eff_res=10.0, psf=0.90, snr=150, bands=13),
}

# contrast attenuation through a clear atmosphere (direct upward transmittance, red band, nadir)
T_ATM = 0.82
# residual scene clutter in a co-registered difference image, in reflectance units,
# at the native scale of each sensor (soil texture, tracks, stones, BRDF, mis-registration)
def clutter(eff_res):
    # clutter decreases with averaging but is floored by radiometric/geometric stability
    return max(0.010, 0.045 * (0.30 / eff_res) ** 0.5)

# ---------------------------------------------------------------- sphere photometry
def sphere_effective_reflectance(rho_s, theta_s_deg):
    """
    Apparent reflectance of the sphere's projected footprint, viewed at nadir.
    Lambertian sphere; phase angle alpha == solar zenith angle for a nadir viewer.

    Nadir intensity  I = (rho_s * E0 / pi) * J,
      J = integral over lit&visible cap of (n.s)(n.v) dA
        = (2/3) r^2 [ sin(a) + (pi - a) cos(a) ]      (verified: a=0 -> 2*pi*r^2/3)

    An equivalent flat Lambertian patch of area A_foot=pi r^2 and reflectance rho_eff,
    lit at zenith angle theta_s, gives I = rho_eff * E0 * cos(theta_s) * A_foot / pi.
    Equate  ->  rho_eff = rho_s * J / (cos(theta_s) * pi * r^2)
    """
    a = np.radians(theta_s_deg)
    J = (2.0 / 3.0) * R**2 * (np.sin(a) + (np.pi - a) * np.cos(a))
    return rho_s * J / (np.cos(a) * np.pi * R**2)

def shadow_length(sun_elev_deg):
    """Ground-projected shadow length of a sphere of height H (m)."""
    return H_SPHERE / np.tan(np.radians(sun_elev_deg))

def shadow_area(sun_elev_deg):
    """Approx. area of the cast shadow ellipse: semi-minor R, semi-major (L+D)/2 minus the footprint."""
    L = shadow_length(sun_elev_deg)
    return max(0.0, np.pi * R * (L + D_SPHERE) / 2.0 - A_FOOT)

# ---------------------------------------------------------------- detection metric
def detect(sensor, rho_s, rho_b, theta_s_deg, use_shadow=True):
    s = SENSORS[sensor]
    cell = s["eff_res"] ** 2                       # m^2, true resolution cell
    rho_eff = sphere_effective_reflectance(rho_s, theta_s_deg)

    # --- bright-target channel
    fill  = min(1.0, A_FOOT / cell)                # fraction of the resolution cell filled
    d_rho = (rho_eff - rho_b) * fill * s["psf"] * T_ATM
    n_px_bright = A_FOOT / (s["pix"] ** 2)

    # --- shadow channel (dark, opposite sign, sun-azimuth aligned)
    sun_elev = 90.0 - theta_s_deg
    A_sh  = shadow_area(sun_elev)
    # shadow is not black: it still receives diffuse skylight, ~15-25% of total irradiance
    diffuse_frac = 0.18
    fill_sh = min(1.0, A_sh / cell)
    d_rho_sh = -rho_b * (1 - diffuse_frac) * fill_sh * s["psf"] * T_ATM
    n_px_sh = A_sh / (s["pix"] ** 2)

    # --- noise budget
    ne_drho = rho_b / s["snr"]                     # sensor noise-equivalent delta reflectance
    clut    = clutter(s["eff_res"])                # scene clutter in a difference image
    sigma   = np.hypot(ne_drho, clut)

    # matched filter over N independent resolution cells gains sqrt(N) on the combined signature
    n_cells = max(1.0, A_FOOT / cell + (A_sh / cell if use_shadow else 0.0))
    signal  = abs(d_rho) + (abs(d_rho_sh) if use_shadow else 0.0)
    ccr     = signal / sigma * np.sqrt(min(n_cells, 12.0)) ** 0.5   # conservative: 4th-root gain

    return dict(rho_eff=rho_eff, d_rho=d_rho, n_px_bright=n_px_bright,
                shadow_len=shadow_length(sun_elev), d_rho_sh=d_rho_sh, n_px_sh=n_px_sh,
                ne_drho=ne_drho, clutter=clut, ccr=ccr)

def verdict(ccr):
    if ccr >= 8:  return "STRONG   - unambiguous point/dipole detection"
    if ccr >= 5:  return "GOOD     - detectable, few false alarms"
    if ccr >= 3:  return "MARGINAL - detectable, heavy false-alarm load"
    if ccr >= 1.5:return "POOR     - only with multi-date stacking"
    return "NO       - below clutter floor"

# ---------------------------------------------------------------- discrimination
# Radiometric detection is the EASY half. The hard half is telling a 0.7 m white sphere
# apart from every other bright compact object in Spanish farmland.
# Densities are order-of-magnitude field estimates per km2 of Meseta agricultural land.
CONFUSERS = {
    #  name                        per km2   size_m  moves?  3D/shadow?  frac. NEW in a ~2-week window
    "White-wrapped silage bales":  (25.0,    1.2,    False,  True,       0.40),  # baling season: bursts
    "Sheep (flocks, seasonal)":    (120.0,   0.8,    True,   True,       1.00),  # always 'new' somewhere
    "Limestone/quartz rock float": (60.0,    0.6,    False,  True,       0.00),  # static: killed by baseline
    "Plastic sheeting / mulch":    (15.0,    2.0,    False,  False,      0.10),
    "Farm vehicles, white":        (2.0,     4.0,    True,   True,       1.00),
    "Misc. agricultural debris":   (40.0,    0.5,    False,  True,       0.05),
}

def discrimination(sensor, area_km2, n_dates=2, has_before=True):
    """
    Cascade of filters applied to raw bright-blob candidates:
      1) brightness threshold            -> only genuinely bright objects survive
      2) size gate (0.5-1.0 m)           -> resolution-dependent; poor at >=0.5 m pixels
      3) temporal persistence (n dates)  -> kills anything that moves
      4) change detection vs. a 'before' -> kills anything that pre-dates the flight
    """
    s = SENSORS[sensor]
    res = s["eff_res"]
    survivors = {}
    for name, (dens, size, moves, threed, frac_new) in CONFUSERS.items():
        n = dens * area_km2
        # size gate: can we resolve the difference between `size` and 0.70 m?
        # need ~2 resolution cells across the object to measure its size at all
        size_ratio = abs(size - D_SPHERE) / D_SPHERE
        resolvable = size_ratio > (res / D_SPHERE) * 0.5
        if resolvable:
            n *= 0.05                      # 95% rejected on size/shape
        else:
            n *= 0.60                      # size gate nearly useless
        if not threed:
            n *= 0.15                      # no shadow dipole -> mostly rejected
        if moves and n_dates >= 2:
            n *= 0.02                      # persistence across dates kills movers
        if has_before:
            # only objects that appeared AFTER the baseline image survive change detection
            n *= (frac_new + 0.02)         # +2% residual for mis-registration / illumination artefacts
        survivors[name] = n
    return survivors

# ================================================================= reports
def hr(c="="): print(c * 104)

print()
hr()
print("  0.70 m WHITE EPS SPHERE - ORBITAL DETECTABILITY")
print(f"  projected footprint = {A_FOOT:.3f} m^2   |   height above ground = {H_SPHERE:.2f} m")
hr()

# --- 1. the curvature penalty
print("\n[1] SPHERE vs FLAT PANEL - the curvature penalty")
print("    A sphere is NOT a white panel: curvature spreads flux, so apparent brightness drops.\n")
print(f"    {'solar zenith':>13} {'sun elev':>9} {'rho_eff (clean)':>16} {'rho_eff (dirty)':>16} {'vs flat panel':>15}")
for tz in [10, 20, 30, 40, 50, 60, 70]:
    re_c = sphere_effective_reflectance(RHO_EPS_FRESH, tz)
    re_d = sphere_effective_reflectance(RHO_EPS_DIRTY, tz)
    print(f"    {tz:>11}deg {90-tz:>7}deg {re_c:>16.3f} {re_d:>16.3f} {re_c/RHO_EPS_FRESH:>14.0%}")

# --- 2. shadow leverage
print("\n[2] SHADOW LEVERAGE - central Spain (lat 40.4N), ~10:30 local solar time overpass")
print("    The shadow is the bigger target for most of the year.\n")
print(f"    {'month':>10} {'sun elev':>9} {'shadow len':>11} {'shadow area':>12} {'px @30cm':>9} {'px @50cm':>9}")
# solar elevation at 10:30 solar time, lat 40.4N, by month (declination-based)
for month, dec in [("Jan",-20.9),("Feb",-12.3),("Mar",-1.8),("Apr",9.8),("May",18.8),("Jun",23.1),
                   ("Jul",21.2),("Aug",13.5),("Sep",2.2),("Oct",-9.6),("Nov",-19.1),("Dec",-23.3)]:
    lat, H = np.radians(40.4), np.radians(-22.5)     # 10:30 solar -> hour angle -22.5 deg
    d = np.radians(dec)
    elev = np.degrees(np.arcsin(np.sin(lat)*np.sin(d) + np.cos(lat)*np.cos(d)*np.cos(H)))
    L, A = shadow_length(elev), shadow_area(elev)
    print(f"    {month:>10} {elev:>7.1f}deg {L:>9.2f} m {A:>10.2f} m2 {A/0.09:>9.1f} {A/0.25:>9.1f}")

# --- 3. sensor comparison
print("\n[3] SENSOR COMPARISON  (clean sphere, dry Meseta soil rho=0.20, sun elev 40deg / zenith 50deg)")
print("    CCR = contrast-to-clutter ratio in a co-registered before/after difference image.\n")
print(f"    {'sensor':<28}{'px':>6}{'bright px':>11}{'d_rho':>9}{'shadow px':>11}{'CCR':>7}  verdict")
for name in SENSORS:
    r = detect(name, RHO_EPS_FRESH, 0.20, 50.0)
    print(f"    {name:<28}{SENSORS[name]['pix']:>5.2f}m{r['n_px_bright']:>11.1f}"
          f"{r['d_rho']:>9.3f}{r['n_px_sh']:>11.1f}{r['ccr']:>7.1f}  {verdict(r['ccr'])}")

# --- 4. background sensitivity (the real risk)
print("\n[4] BACKGROUND SENSITIVITY - Pleiades Neo 30 cm, clean sphere, sun elev 40deg")
print("    What the sphere is lying ON matters more than which satellite you buy.\n")
print(f"    {'background':<40}{'rho_b':>7}{'d_rho':>9}{'CCR':>7}  verdict")
for bg, rb in sorted(BACKGROUNDS.items(), key=lambda kv: kv[1]):
    r = detect("Pleiades Neo (Airbus)", RHO_EPS_FRESH, rb, 50.0)
    print(f"    {bg:<40}{rb:>7.2f}{r['d_rho']:>9.3f}{r['ccr']:>7.1f}  {verdict(r['ccr'])}")

# --- 5. dirty / degraded sphere
print("\n[5] DEGRADED TARGET - Pleiades Neo 30 cm, dry soil rho=0.20, sun elev 40deg")
for label, rs in [("clean white EPS", RHO_EPS_FRESH), ("dusty / soiled", RHO_EPS_DIRTY),
                  ("half-buried or in stubble (50% obscured)", RHO_EPS_FRESH)]:
    obsc = 0.5 if "buried" in label else 1.0
    r = detect("Pleiades Neo (Airbus)", rs, 0.20, 50.0)
    ccr = r["ccr"] * obsc
    print(f"    {label:<45}CCR={ccr:>5.1f}  {verdict(ccr)}")

# --- 6. search economics
print("\n[6] SEARCH ECONOMICS - indicative, confirm current rates with the providers")
print(f"    {'area':>9} {'PNeo 30cm':>13} {'SkySat flex':>13} {'SkySat assured':>16} {'drone @3cm':>13} {'drone days':>11}")
for area in [10, 25, 50, 100, 200, 400]:
    pneo   = max(area, 100) * 32          # EUR/km2 tasking, 100 km2 practical min
    sky_f  = max(area, 25) * 12 * 0.92    # USD->EUR approx
    sky_a  = max(area, 25) * 40 * 0.92
    drone  = area * 90                    # EUR/km2 all-in contracted VTOL mapping
    ddays  = area / 12.0                  # km2 per productive day, VTOL at 120 m AGL
    print(f"    {area:>6} km2 {pneo:>12,.0f}EUR {sky_f:>12,.0f}EUR {sky_a:>15,.0f}EUR {drone:>12,.0f}EUR {ddays:>10.1f}")
print("    NOTE: SkySat carries a ~$15k tasking / ~$5k archive order minimum; PNeo tasking min ~100 km2")
print("          (50 km2 under a OnePlan subscription). Small AOIs pay the minimum, not the area price.")

# --- 7. how many pixels must be searched
print("\n[7] DISCRIMINATION - the real bottleneck (50 km2 AOI)")
print("    Radiometric detection is easy. Telling the sphere from every other white blob is not.\n")
for name in ["Pleiades Neo (Airbus)", "SkySat (Planet)"]:
    print(f"    --- {name} ({SENSORS[name]['eff_res']:.2f} m effective resolution)")
    for scenario, nd, hb in [("1 image, no 'before' baseline", 1, False),
                             ("2 images, no 'before' baseline", 2, False),
                             ("2 images + archive 'before'   ", 2, True)]:
        sv = discrimination(name, 50, n_dates=nd, has_before=hb)
        tot = sum(sv.values())
        top = max(sv.items(), key=lambda kv: kv[1])
        print(f"        {scenario}  -> {tot:>8,.0f} candidates to eyeball "
              f"(worst: {top[0]}, {top[1]:,.0f})")
    print()

print("[8] EFFECT OF SEARCH-AREA REDUCTION (Pleiades Neo, 2 dates + before-baseline)")
print("    Shrinking the ellipse with a proper descent reconstruction is the cheapest win available.\n")
print(f"    {'AOI':>9} {'candidates':>12} {'analyst-hours @400/hr':>23} {'imagery cost':>14}")
for area in [5, 10, 25, 50, 100, 200]:
    tot = sum(discrimination("Pleiades Neo (Airbus)", area, 2, True).values())
    print(f"    {area:>6} km2 {tot:>12,.0f} {tot/400:>21.1f} h {max(area,100)*32:>12,.0f}EUR")
print()
hr()

# ================================================================= SAR reflector sizing (next flight)
print("\n[9] NEXT FLIGHT - trihedral corner reflector sizing for SAR recovery")
print("    Trihedral RCS: sigma = 4*pi*a^4 / (3*lambda^2), a = inner leg length.")
print("    Requirement: reflector RCS must exceed farmland clutter in one resolution cell by ~15 dB.\n")
SAR = {
    "Sentinel-1 IW (free, C-band)":  dict(lam=0.0555, res_az=20.0, res_rg=5.0,  s0_db=-10.0, rev=6),
    "ICEYE spotlight (X-band)":      dict(lam=0.0311, res_az=1.0,  res_rg=1.0,  s0_db=-10.0, rev=1),
    "Capella spotlight (X-band)":    dict(lam=0.0311, res_az=0.5,  res_rg=0.5,  s0_db=-10.0, rev=1),
    "TerraSAR-X ST (Airbus, X)":     dict(lam=0.0311, res_az=1.0,  res_rg=1.0,  s0_db=-10.0, rev=2),
    "PAZ (Hisdesat, Spain, X)":      dict(lam=0.0311, res_az=1.0,  res_rg=1.0,  s0_db=-10.0, rev=2),
}
print(f"    {'sensor':<32}{'cell m2':>9}{'clutter':>10}{'need RCS':>11}{'leg a':>9}{'mass~':>8}{'revisit':>9}")
for name, p in SAR.items():
    cell = p["res_az"] * p["res_rg"]
    clut_rcs = cell * 10 ** (p["s0_db"] / 10.0)
    need = clut_rcs * 10 ** (15.0 / 10.0)                 # +15 dB signal-to-clutter
    a = (need * 3 * p["lam"] ** 2 / (4 * np.pi)) ** 0.25
    # 3 plates of a^2 each, aluminised 3 mm foam-core ~ 0.35 kg/m2, +30% for edging
    mass = 3 * a ** 2 * 0.35 * 1.3 * 1000.0      # grams
    print(f"    {name:<32}{cell:>9.1f}{clut_rcs:>10.2f}{need:>11.1f}{a:>8.2f}m{mass:>7.0f}g{p['rev']:>8}d")
print("\n    -> An X-band trihedral of ~30 cm leg, well under 100 g, makes the payload a")
print("       point target that SAR finds through cloud, at night, in ANY weather.")
print("       Mount it so at least one trihedral faces up-and-sideways in any resting attitude")
print("       (an octahedral / 8-corner cluster guarantees this) and it always answers.")
