#!/usr/bin/env python3
"""
Can we buy a drone that does this job?

Sizes the thermal night search properly, checks whether a fixed wing can carry a
microbolometer without smearing the target, and works the buy-vs-contract case.

SI units throughout. Prices are indicative street prices, not quotes.
"""
import math

def hr(c="="): print(c * 104)

CEILING  = 120.0     # m AGL, EASA/AESA
TARGET_D = 0.70      # m
LAT      = 40.4      # deg N, central Spain

# ---------------------------------------------------------------- platforms
# thermal_px / thermal_dfov describe the microbolometer; rgb_* the survey camera.
FLEET = {
    "DJI Mavic 3 Thermal (M3T)": dict(
        rgb_px=8064, rgb_pitch=2.4e-6, rgb_f=0.0124,
        th_px=640, th_dfov=61.0, endur=42*60, spd_rgb=12.0, spd_th=8.0,
        kind="multirotor", cls="C2", price=6000, both=True),
    "DJI Matrice 4T": dict(
        rgb_px=8192, rgb_pitch=2.4e-6, rgb_f=0.0124,
        th_px=640, th_dfov=45.0, endur=47*60, spd_rgb=15.0, spd_th=8.0,
        kind="multirotor", cls="C2", price=9500, both=True),
    "DJI Matrice 350 + H30T": dict(
        rgb_px=8192, rgb_pitch=3.2e-6, rgb_f=0.024,
        th_px=1280, th_dfov=45.0, endur=50*60, spd_rgb=15.0, spd_th=8.0,
        kind="multirotor", cls="C2", price=28000, both=True),
    "AgEagle eBee X + Duet T": dict(
        rgb_px=6000, rgb_pitch=3.9e-6, rgb_f=0.0185,
        th_px=640, th_dfov=45.0, endur=90*60, spd_rgb=16.0, spd_th=16.0,
        kind="fixed wing", cls="C6", price=38000, both=True),
    "Quantum Trinity Pro (RGB+thermal)": dict(
        rgb_px=7952, rgb_pitch=4.5e-6, rgb_f=0.035,
        th_px=640, th_dfov=45.0, endur=90*60, spd_rgb=17.0, spd_th=17.0,
        kind="VTOL fixed", cls="C6", price=48000, both=True),
    "WingtraOne GEN II (RGB only)": dict(
        rgb_px=9504, rgb_pitch=3.76e-6, rgb_f=0.024,
        th_px=None, th_dfov=None, endur=59*60, spd_rgb=16.0, spd_th=None,
        kind="VTOL fixed", cls="C6", price=45000, both=False),
}

SIDELAP = 0.25       # search overlap, not photogrammetric
TURN_EFF = 0.78

def rgb_geom(p):
    gsd = CEILING * p["rgb_pitch"] / p["rgb_f"]
    swath = p["rgb_px"] * gsd
    return gsd, swath, swath * (1 - SIDELAP) * p["spd_rgb"] * TURN_EFF

def th_geom(p):
    """Thermal GSD from diagonal FOV and detector format (assume 5:4 array)."""
    if not p["th_px"]:
        return None
    w, h = p["th_px"], p["th_px"] * 0.8
    diag = math.hypot(w, h)
    f_px = (diag / 2) / math.tan(math.radians(p["th_dfov"] / 2))
    gsd = CEILING / f_px
    swath = w * gsd
    return gsd, swath, swath * (1 - SIDELAP) * p["spd_th"] * TURN_EFF

print()
hr()
print("  BUYING A DRONE FOR THIS JOB")
hr()

# ---------------------------------------------------------------- 1. smear
print("\n[1] Does a fixed wing smear the thermal target?")
print("    Uncooled microbolometers have a thermal time constant of ~8-12 ms.")
print("    A moving platform drags the scene across the detector during that time.\n")
TAU     = 0.010      # s, microbolometer thermal time constant
DT_CONTRAST = 5.0    # K, porexpan against soil before dawn
NETD    = 0.050      # K, detector noise-equivalent temperature difference

w, h = 640, 512
f_px = (math.hypot(w, h) / 2) / math.tan(math.radians(45.0 / 2))
gsd_th = CEILING / f_px
d_px = TARGET_D / gsd_th        # target diameter in thermal pixels

print(f"    Target spans {d_px:.1f} thermal px at {gsd_th*100:.0f} cm GSD; raw margin is "
      f"{DT_CONTRAST/NETD:.0f} sigma.\n")
print(f"    {'speed':>10}{'smear':>9}{'smear px':>10}{'peak kept':>12}{'margin left':>13}  verdict")
for spd, label in [(6.0, "multirotor slow"), (8.0, "multirotor"), (12.0, "slow fixed wing"),
                   (17.0, "fixed wing cruise"), (22.0, "fast fixed wing")]:
    smear_px = spd * TAU / gsd_th
    kept = d_px / (d_px + smear_px)          # peak contrast retained after linear smear
    sigma = DT_CONTRAST * kept / NETD
    v = "fine" if sigma > 20 else ("marginal" if sigma > 6 else "too little margin")
    print(f"    {spd:>7.0f} m/s{spd*TAU:>8.2f}m{smear_px:>10.2f}{kept:>11.0%}{sigma:>11.0f}s  "
          f"{v}  ({label})")
print("\n    -> Even at fast fixed-wing cruise the target keeps ~80% of its peak contrast")
print("       and retains tens of sigma of margin. Smear is real but irrelevant here,")
print("       because a 5 K anomaly against a 50 mK detector is an enormous signal.")
print("       Fixed-wing thermal is viable; smear is not a reason to prefer a multirotor.")

# ---------------------------------------------------------------- 2. night window
print("\n[2] How long is the usable night window?")
print("    Correction to the earlier note: this is NOT a 1-2 hour pre-dawn slot.")
print("    Porexpan reaches its steady cold offset within ~30 min of sunset, while soil")
print("    keeps drawing heat from depth all night, so the contrast is open for hours.")
print("    Waiting 3 h after sunset lets high-inertia objects shed their daytime heat,")
print("    which is what makes the cold anomaly clean rather than merely present.\n")

def daylength(lat_deg, decl_deg):
    lat, d = math.radians(lat_deg), math.radians(decl_deg)
    x = -math.tan(lat) * math.tan(d)
    x = max(-1.0, min(1.0, x))
    return 2 * math.degrees(math.acos(x)) / 15.0     # hours

print(f"    {'month':>8}{'night length':>15}{'usable window':>16}  (sunset +3 h to sunrise)")
for m, dec in [("Aug", 13.5), ("Sep", 2.2), ("Oct", -9.6), ("Nov", -19.1), ("Dec", -23.3)]:
    night = 24.0 - daylength(LAT, dec)
    usable = max(0.0, night - 3.0)
    print(f"    {m:>8}{night:>13.1f} h{usable:>14.1f} h")
AUG_WINDOW = 24.0 - daylength(LAT, 13.5) - 3.0
print(f"\n    -> August gives ~{AUG_WINDOW:.1f} usable hours per night, not one or two.")
print("       That is 3-4 fixed-wing sorties, or 6-8 multirotor batteries.")

# ---------------------------------------------------------------- 3. coverage
print("\n[3] Coverage, both sensors, at the 120 m ceiling")
print(f"    {'platform':<36}{'RGB GSD':>9}{'RGB km2/d':>11}{'TH GSD':>9}{'TH px':>7}{'TH km2/night':>14}")
for name, p in FLEET.items():
    rg, rs, rr = rgb_geom(p)
    flights_day = 8 if p["kind"] == "multirotor" else 7
    rgb_day = rr * p["endur"] * flights_day / 1e6
    t = th_geom(p)
    if t:
        tg, ts, tr = t
        th_night = tr * AUG_WINDOW * 3600 * 0.55 / 1e6   # 55% duty: swaps, transits, turns
        print(f"    {name:<36}{rg*100:>7.1f}cm{rgb_day:>11.1f}{tg*100:>7.1f}cm"
              f"{TARGET_D/tg:>7.1f}{th_night:>14.1f}")
    else:
        print(f"    {name:<36}{rg*100:>7.1f}cm{rgb_day:>11.1f}{'-':>9}{'-':>7}{'-':>14}")
print("\n    -> Thermal covers far less ground than RGB: the detector has 640 px where")
print("       the RGB camera has 8,000. Even across a full night, thermal sweeps a few")
print("       km2, not tens. It is a shortlist and small-core tool, as suspected -")
print("       but a whole night of it clears a genuinely useful area.")

# ---------------------------------------------------------------- 4. regulation
print("\n[4] The catch that decides which aircraft to buy")
print("    STS-02 (BVLOS, 2 km from pilot) requires a C6-class aircraft.")
print("    Multirotors carry C2. They are therefore VLOS-only unless you write your")
print("    own SORA and obtain a bespoke authorisation.\n")
print(f"    {'platform':<36}{'class':>7}{'max regime':>26}{'km2 per setup':>15}")
for name, p in FLEET.items():
    if p["cls"] == "C6":
        regime, area = "STS-02 BVLOS, 2 km", math.pi * 2.0 ** 2
    else:
        regime, area = "VLOS only, ~500 m", math.pi * 0.5 ** 2
    print(f"    {name:<36}{p['cls']:>7}{regime:>26}{area:>15.1f}")
print("\n    -> This, not coverage rate, is the real split. A 9,500 EUR Matrice 4T is")
print("       an excellent instrument tethered to a 0.8 km2 bubble around the pilot.")

print("\n[5] What each option can realistically search")
print(f"    {'platform':<36}{'10 km2':>10}{'30 km2':>10}{'60 km2':>10}{'120 km2':>10}")
for name, p in FLEET.items():
    rg, rs, rr = rgb_geom(p)
    flights_day = 8 if p["kind"] == "multirotor" else 7
    rgb_day = rr * p["endur"] * flights_day / 1e6
    setup_area = math.pi * (2.0 if p["cls"] == "C6" else 0.5) ** 2
    row = ""
    for area in (10, 30, 60, 120):
        # a VLOS platform loses ~40 min per relocation between setups
        setups = math.ceil(area / setup_area)
        fly_days = area / rgb_day
        move_days = setups * (40 / 60) / 8.0 if p["cls"] != "C6" else setups * (20/60) / 8.0
        row += f"{fly_days + move_days:>10.1f}"
    print(f"    {name:<36}{row}   days")

# ---------------------------------------------------------------- 5. money
print("\n[6] Buy vs contract")
DAY_RATE = 1500.0
print(f"    Contracted VTOL fixed wing + crew: {DAY_RATE:,.0f} EUR/day at ~45 km2/day\n")
print(f"    {'platform':<36}{'price':>9}{'+ compliance':>14}{'total':>10}{'payback':>12}")
for name, p in FLEET.items():
    compliance = 6000 if p["cls"] == "C6" else 1500   # STS-02 crew training vs A2 certificate
    total = p["price"] + compliance
    print(f"    {name:<36}{p['price']:>8,.0f}E{compliance:>13,.0f}E{total:>9,.0f}E"
          f"{total/DAY_RATE:>9.0f} days")
print("\n    Compliance covers: remote pilot certification, STS-02 declaration and crew")
print("    training where applicable, operator registration, third-party insurance,")
print("    and a night-operations flashing green beacon (required for any night flight).")

print("\n[7] Payback across your own flight cadence")
print("    Assume one balloon campaign needs a 2-day search when a payload is lost.\n")
print(f"    {'losses per year':>17}{'M4T (9.5k+1.5k)':>20}{'Trinity Pro (48k+6k)':>23}")
for n in (1, 2, 4, 8):
    saved = n * 2 * DAY_RATE
    print(f"    {n:>17}{11000/saved:>17.1f} yr{54000/saved:>20.1f} yr")
print("\n    -> A ~10k EUR dual-sensor multirotor pays for itself in under four years")
print("       at one loss per year, and in under one year at four. A 48k EUR fixed wing")
print("       does not pay back on recovery alone - it needs other survey work to carry it.")
print()
hr()
print("\nRECOMMENDATION")
print("  Buy the DJI Matrice 4T (or Mavic 3 Thermal if budget is tight). One aircraft,")
print("  both sensors, ~10k EUR all-in, and it covers the thermal idea properly.")
print("  Accept that it is VLOS-only: it is a precision instrument for a small area,")
print("  a shortlist, or a whole-night thermal sweep of a high-probability core.")
print()
print("  Do NOT buy a 48k EUR fixed wing for payload recovery alone. If this ellipse")
print("  turns out large, contract a Spanish STS-02 operator for the wide RGB sweep")
print("  and use your own aircraft for the thermal follow-up. That splits the job")
print("  along the line where each tool is actually better.")
print()
hr()
