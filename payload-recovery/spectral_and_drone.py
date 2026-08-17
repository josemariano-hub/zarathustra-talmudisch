#!/usr/bin/env python3
"""
Two follow-on questions:

  A. Does porexpan's spectral signature actually help, and from what platform?
  B. What does searching with our own drone cost, and which airframe?

SI units throughout.
"""
import math
import numpy as np

def hr(c="="): print(c * 104)

# =========================================================== A. SPECTRAL
# Reflectance at the band centres of Pleiades Neo's six VNIR bands, plus three
# SWIR points. Values are representative literature/field figures for dry
# central-Iberian cover types, not measurements of your specific sphere.
BANDS = ["DeepBlue", "Blue", "Green", "Red", "RedEdge", "NIR", "SWIR1215", "SWIR1730", "SWIR2300"]
WL    = [420, 485, 555, 655, 725, 830, 1215, 1730, 2300]   # nm

SPECTRA = {
    # ---- the target
    "EPS / porexpan (clean)":   [0.80, 0.83, 0.84, 0.84, 0.84, 0.82, 0.44, 0.22, 0.14],
    "EPS / porexpan (soiled)":  [0.58, 0.61, 0.63, 0.64, 0.65, 0.64, 0.36, 0.20, 0.13],
    # ---- polymer confusers: the ones spectra will NOT separate in VNIR
    "PE silage bale wrap":      [0.78, 0.83, 0.85, 0.86, 0.86, 0.85, 0.52, 0.28, 0.19],
    "PE sheeting / mulch":      [0.75, 0.80, 0.82, 0.83, 0.83, 0.82, 0.50, 0.26, 0.18],
    # ---- natural confusers: the ones spectra WILL separate
    "Limestone / gypsum":       [0.35, 0.42, 0.50, 0.55, 0.57, 0.58, 0.60, 0.52, 0.38],
    "Sheep fleece (dirty)":     [0.25, 0.32, 0.42, 0.50, 0.55, 0.60, 0.52, 0.34, 0.24],
    "Cereal stubble":           [0.12, 0.16, 0.24, 0.30, 0.38, 0.45, 0.42, 0.30, 0.22],
    "Dry soil (Meseta)":        [0.10, 0.13, 0.18, 0.23, 0.26, 0.28, 0.33, 0.32, 0.26],
    "Green crop":               [0.04, 0.05, 0.12, 0.05, 0.25, 0.48, 0.42, 0.20, 0.09],
}

def brightness(s, upto=6):   return float(np.mean(s[:upto]))
def vnir_slope(s):
    """(NIR - DeepBlue)/(NIR + DeepBlue). Near zero only for white polymers."""
    return (s[5] - s[0]) / (s[5] + s[0])
def slope_4band(s):
    """Same index for a conventional 4-band sensor whose blue starts at 450 nm."""
    return (s[5] - s[1]) / (s[5] + s[1])
def chi_1730(s):
    """Depth of the C-H absorption at 1730 nm below a NIR-to-2300 continuum."""
    cont = s[5] + (s[8] - s[5]) * (1730 - 830) / (2300 - 830)
    return (cont - s[7]) / cont

print()
hr()
print("  A. SPECTRAL SEPARABILITY OF PORExPAN")
hr()
print("\n[A1] Band reflectances and separation indices\n")
print(f"    {'material':<26}" + "".join(f"{b:>9}" for b in BANDS[:6]) +
      f"{'bright':>8}{'slope6':>8}{'slope4':>8}{'1730 dip':>10}")
for name, s in SPECTRA.items():
    print(f"    {name:<26}" + "".join(f"{v:>9.2f}" for v in s[:6]) +
          f"{brightness(s):>8.2f}{vnir_slope(s):>8.3f}{slope_4band(s):>8.3f}{chi_1730(s):>9.0%}")

print("\n[A2] The VNIR gate: bright AND spectrally flat")
print("    Rule: mean(6 VNIR bands) > 0.55  AND  |slope6| < 0.08\n")
for name, s in SPECTRA.items():
    b, sl = brightness(s), vnir_slope(s)
    passes = b > 0.55 and abs(sl) < 0.08
    tag = "PASS  <-- survives the gate" if passes else "reject"
    why = "" if passes else (f"(bright {b:.2f})" if b <= 0.55 else f"(slope {sl:+.3f})")
    print(f"    {name:<26} {tag:<28}{why}")

print("\n    -> Every NATURAL confuser is rejected. Only the white polymers survive,")
print("       and porexpan is a white polymer, so VNIR cannot separate it from bale wrap.")
print("       The gate removes the *numerous* confusers and leaves the *few*.")

print("\n[A3] Why the deep-blue band matters")
print("    Natural bright materials fall off toward the blue; polymers do not.")
print(f"    {'material':<26}{'slope, 6-band':>15}{'slope, 4-band':>15}{'margin lost':>13}")
for name in ["Limestone / gypsum", "Sheep fleece (dirty)", "Cereal stubble"]:
    s = SPECTRA[name]
    s6, s4 = vnir_slope(s), slope_4band(s)
    print(f"    {name:<26}{s6:>15.3f}{s4:>15.3f}{(s6-s4)/s6:>12.0%}")
print("    -> Pleiades Neo's 400-450 nm band widens the separation from limestone by ~35%.")
print("       This is a concrete reason to prefer it over any 4-band 30-50 cm sensor.")

print("\n[A4] The SWIR features are diagnostic but unreachable from orbit")
print(f"    C-H absorption at 1730 nm: {chi_1730(SPECTRA['EPS / porexpan (clean)']):.0%} depth for porexpan,")
print(f"    versus {chi_1730(SPECTRA['Limestone / gypsum']):.0%} for limestone. Unambiguous - if you can sample it.\n")
SWIR_PLATFORMS = [
    # name, GSD (m), notes
    ("WorldView-3 SWIR",            3.70, "regulator-resampled to 7.5 m for non-US users"),
    ("EnMAP / PRISMA hyperspectral", 30.0, "full 400-2500 nm, 30 m"),
    ("EMIT (ISS)",                  60.0, "free, but 60 m"),
    ("Airborne hyperspectral",       1.00, "light aircraft, full SWIR"),
    ("Drone SWIR / hyperspectral",   0.05, "at 120 m AGL"),
]
A_FOOT = math.pi * 0.35 ** 2
print(f"    {'platform':<30}{'GSD':>8}{'px on sphere':>14}{'usable?':>10}  note")
for name, gsd, note in SWIR_PLATFORMS:
    npx = A_FOOT / gsd ** 2
    ok = "yes" if npx > 0.25 else ("marginal" if npx > 0.05 else "no")
    shown = f"{npx:.2f}" if npx < 10 else f"{npx:,.0f}"
    print(f"    {name:<30}{gsd:>7.2f}m{shown:>14}{ok:>10}  {note}")
print("\n    -> The signature that would be decisive needs SWIR, and no orbital SWIR")
print("       sensor resolves a 0.7 m object. It becomes usable only from an aircraft")
print("       or a drone - which is the bridge to part B.")

# ---- revised candidate counts with the spectral gate applied
# Reuse the discrimination cascade from the main model rather than re-deriving it,
# so these numbers stay consistent with the feasibility note.
print("\n[A5] Effect of the VNIR spectral gate on the candidate list (50 km2)")
import importlib.util, io, contextlib, os
_spec = importlib.util.spec_from_file_location(
    "detectability", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "sphere_detectability.py"))
_dm = importlib.util.module_from_spec(_spec)
with contextlib.redirect_stdout(io.StringIO()):
    _spec.loader.exec_module(_dm)

# which confusers are natural (rejected by the flat-and-bright gate) vs polymer
NATURAL = {"Sheep (flocks, seasonal)", "Limestone/quartz rock float",
           "Farm vehicles, white", "Misc. agricultural debris"}
GATE_PASS = {True: 0.02, False: 0.90}      # natural -> rejected, polymer -> survives

for label, nd, hb in [("1 image", 1, False), ("2 images", 2, False),
                      ("2 images + baseline", 2, True)]:
    sv = _dm.discrimination("Pleiades Neo (Airbus)", 50, n_dates=nd, has_before=hb)
    no_gate = sum(sv.values())
    gated = sum(n * GATE_PASS[name in NATURAL] for name, n in sv.items())
    print(f"    {label:<24} {no_gate:>8,.0f}  ->  {gated:>7,.0f} with spectral gate "
          f"({1 - gated / no_gate:.0%} reduction)")
print("    Residual is bales and sheeting - separated by size and shape, not colour.")


# =========================================================== B. DRONE
print()
hr()
print("  B. SEARCHING WITH OUR OWN DRONE")
hr()

CEILING = 120.0          # m AGL, EASA/AESA hard limit in open and STS categories
TARGET_D = 0.70          # m
PX_NEEDED = 6.0          # pixels across the sphere for confident visual ID

PLATFORMS = {
    # name: sensor px across, pixel pitch m, focal m, endurance s, cruise m/s, type, EUR
    "DJI Mavic 3 Enterprise":  dict(px=5280, pitch=3.3e-6, f=0.01229, endur=45*60,  spd=15.0, kind="multirotor", cost=6000),
    "DJI Matrice 350 + P1":    dict(px=8192, pitch=4.4e-6, f=0.035,   endur=50*60,  spd=15.0, kind="multirotor", cost=25000),
    "WingtraOne GEN II RGB61": dict(px=9504, pitch=3.76e-6,f=0.024,   endur=59*60,  spd=16.0, kind="VTOL fixed", cost=45000),
    "Quantum Trinity F90+":    dict(px=7952, pitch=4.5e-6, f=0.035,   endur=90*60,  spd=17.0, kind="VTOL fixed", cost=30000),
    "AgEagle eBee X (Aeria X)":dict(px=6000, pitch=3.9e-6, f=0.0185,  endur=90*60,  spd=16.0, kind="fixed wing", cost=28000),
    "Thermal (640x512, 9 mm)": dict(px=640,  pitch=12e-6,  f=0.0091,  endur=40*60,  spd=12.0, kind="multirotor", cost=9000),
}

SIDELAP_MAP    = 0.65    # photogrammetric orthomosaic
SIDELAP_SEARCH = 0.25    # just enough to avoid gaps
TURN_EFF       = 0.78    # fraction of airtime on productive survey lines

def geom(p, sidelap):
    gsd   = CEILING * p["pitch"] / p["f"]
    swath = p["px"] * gsd
    rate  = swath * (1 - sidelap) * p["spd"] * TURN_EFF     # m^2/s
    return gsd, swath, rate

print("\n[B1] At the 120 m legal ceiling, resolution is not the differentiator")
print("     GSD is set by optics and the ceiling; every option resolves the sphere easily.\n")
print(f"    {'platform':<28}{'GSD':>8}{'px on sphere':>14}{'swath':>9}{'type':>13}")
for name, p in PLATFORMS.items():
    gsd, swath, _ = geom(p, SIDELAP_SEARCH)
    print(f"    {name:<28}{gsd*100:>6.1f}cm{TARGET_D/gsd:>13.0f}{swath:>8.0f}m{p['kind']:>13}")
print(f"\n    Need only ~{PX_NEEDED:.0f} px across the sphere for confident ID. All RGB options")
print("    clear that by a wide margin, so the binding parameter is SWATH x ENDURANCE,")
print("    not camera quality. Buying a sharper camera buys nothing here.")

print("\n[B2] Survey overlap: the single biggest operational lever")
print("     Mapping missions default to 65-75% sidelap to build an orthomosaic.")
print("     You are not making a map. You are looking for an object.\n")
print(f"    {'platform':<28}{'map 65%':>12}{'search 25%':>13}{'gain':>8}")
for name, p in PLATFORMS.items():
    if p["kind"] == "multirotor" and "Thermal" in name: continue
    _, _, r_map = geom(p, SIDELAP_MAP)
    _, _, r_srch = geom(p, SIDELAP_SEARCH)
    print(f"    {name:<28}{r_map*3600/1e6:>10.2f}km2/h{r_srch*3600/1e6:>11.2f}km2/h{r_srch/r_map:>7.1f}x")
print("    -> Dropping to search overlap roughly doubles coverage for free.")
print("       Process the raw geotagged frames directly; skip orthomosaic generation.")

print("\n[B3] Productive coverage")
print(f"    {'platform':<28}{'km2/flight':>12}{'km2/day':>10}{'days @120km2':>14}")
FLIGHTS_PER_DAY = {"multirotor": 8, "VTOL fixed": 7, "fixed wing": 7}
for name, p in PLATFORMS.items():
    _, _, rate = geom(p, SIDELAP_SEARCH)
    per_flight = rate * p["endur"] / 1e6
    per_day = per_flight * FLIGHTS_PER_DAY[p["kind"]]
    print(f"    {name:<28}{per_flight:>11.2f}{per_day:>10.1f}{120/per_day:>13.1f}")

print("\n[B4] The regulatory constraint dominates everything")
print("     Coverage per pilot setup is capped by how far the aircraft may legally go.\n")
REGIMES = [
    ("Open category A3, VLOS",      0.5, "no paperwork; ~500 m visual range"),
    ("STS-02, BVLOS + observer",    2.0, "declaration, C6 aircraft, trained crew"),
    ("Specific cat., bespoke LUC",  5.0, "full authorisation, weeks of lead time"),
]
print(f"    {'regime':<32}{'radius':>8}{'km2/setup':>12}{'setups for 120 km2':>21}  note")
for name, rad, note in REGIMES:
    a = math.pi * rad ** 2
    print(f"    {name:<32}{rad:>7.1f}km{a:>12.1f}{math.ceil(120/a):>21}  {note}")
print("\n    -> Under plain VLOS a 120 km2 search needs ~153 separate pilot setups.")
print("       That, not the airframe, is what makes or breaks a drone search.")
print("       STS-02 is the enabling step: 10 setups instead of 153.")

print("\n[B5] Cost: contract vs. buy")
AREAS = [20, 50, 120, 250]
DAY_RATE   = 1500.0     # EUR/day, 2-person crew + VTOL fixed wing, Spain
KM2_PER_DAY = 45.0      # STS-02, fixed-wing VTOL, search overlap
print(f"    {'AOI':>8}{'drone days':>12}{'contracted':>13}{'Pleiades Neo':>15}{'per km2 (drone)':>18}")
for a in AREAS:
    days = math.ceil(a / KM2_PER_DAY)
    dcost = days * DAY_RATE
    pneo = max(a, 100) * 32
    print(f"    {a:>5} km2{days:>12}{dcost:>12,.0f}E{pneo:>14,.0f}E{dcost/a:>17,.0f}E")
print("\n    Buying instead of contracting:")
for name, p in sorted(PLATFORMS.items(), key=lambda kv: kv[1]["cost"]):
    if p["kind"] == "multirotor" and "Thermal" not in name: continue
    print(f"      {name:<28}{p['cost']:>8,.0f}E")
print("      + STS-02 crew training, C6 aircraft, insurance:  ~4,000-8,000 EUR")
print("    -> For a one-off recovery, contract. Buying only pays back across many flights.")

print("\n[B6] Data volume - the hidden cost")
for name in ["Quantum Trinity F90+", "AgEagle eBee X (Aeria X)"]:
    p = PLATFORMS[name]
    gsd, swath, rate = geom(p, SIDELAP_SEARCH)
    km2_day = rate * p["endur"] * FLIGHTS_PER_DAY[p["kind"]] / 1e6
    gpx = km2_day * 1e6 / gsd ** 2 / 1e9
    frames = km2_day * 1e6 / (swath * swath * 0.75 * 0.25)
    print(f"    {name:<28}{km2_day:>6.1f} km2/day  {gpx:>7.0f} Gpx  ~{frames:>6,.0f} frames/day")
print("    Run the matched filter per frame on the geotagged originals.")
print("    Building an orthomosaic first would cost more compute than the search itself.")

# ---------------------------------------------------------- thermal
print("\n[B7] The pre-dawn thermal option")
print("     Porexpan is a near-perfect insulator, so it has almost no thermal ballast.\n")
def thermal_inertia(k, rho, c): return math.sqrt(k * rho * c)
MATS = {
    "EPS / porexpan":  (0.035, 20.0,  1300.0),
    "Dry soil":        (0.30,  1400.0, 800.0),
    "Limestone":       (1.30,  2500.0, 840.0),
    "Silage bale (wet)":(0.40, 700.0,  3000.0),
    "Cereal stubble":  (0.08,  120.0,  1500.0),
}
Q_NET = 80.0     # W/m2 net longwave loss to a clear night sky
H_CONV = 10.0    # W/m2K convective coupling to air, light wind
print(f"    {'material':<22}{'thermal inertia':>18}{'dT vs air, pre-dawn':>22}")
ref = None
for name, (k, rho, c) in MATS.items():
    P = thermal_inertia(k, rho, c)
    # low inertia -> radiative loss balanced almost entirely by convection
    # high inertia -> substrate conduction buffers the surface
    buffer = P / (P + 120.0)
    dT = -Q_NET / H_CONV * (1 - buffer)
    if name == "Dry soil": ref = dT
    print(f"    {name:<22}{P:>14.0f} SI{dT:>20.1f} K")
dT_eps = -Q_NET / H_CONV * (1 - thermal_inertia(*MATS["EPS / porexpan"]) /
                            (thermal_inertia(*MATS["EPS / porexpan"]) + 120.0))
print(f"\n    -> Porexpan sits about {abs(dT_eps-ref):.1f} K COLDER than surrounding soil before dawn.")
print(f"       A 50 mK-NETD thermal camera sees that at ~{abs(dT_eps-ref)/0.05:.0f} sigma.")
p = PLATFORMS["Thermal (640x512, 9 mm)"]
gsd, swath, rate = geom(p, SIDELAP_SEARCH)
print(f"       At 120 m: {gsd*100:.0f} cm GSD, {TARGET_D/gsd:.1f} px on target, "
      f"{rate*3600/1e6:.2f} km2/h.")
print("       Limitation: a 1-2 hour window before sunrise, and stubble also cools fast.")
print("       Use it to confirm a shortlist or sweep a small high-probability core,")
print("       not as the primary wide-area search.")
print()
hr()
