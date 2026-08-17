#!/usr/bin/env python3
"""
What would a purpose-built DIY drone for the sphere recovery cost?

Two variants, driven by the frozen mission requirements:
  A. "Sweeper"    - RGB fixed wing for the wide daylight search
  B. "Night core" - multirotor carrying a thermal core for the night sweep

Then an honest comparison against the used-market option (M3T kit, 7,380 EUR)
and contracting (1,500 EUR/day).

Physics: SI units. Cruise power from weight, speed, L/D and drivetrain
efficiency; hover power from momentum theory with a figure of merit.
Prices are indicative street prices (EUR, Aug 2026), not quotes.

One regulatory fact shapes the whole design space and is stated up front:
a privately built UAS carries NO C-class marking, so STS-02 (the BVLOS
declaration route) is unavailable to it, full stop. A homebuilt flies Open
category A3 - VLOS, under 25 kg, 150 m from uninvolved people and buildings -
or it needs a full SORA authorisation. DIY therefore cannot buy range; it can
only buy sensors and redundancy cheaply. Optimize accordingly.
"""
import math

def hr(c="="): print(c * 104)

G0       = 9.80665
RHO_AIR  = 1.10        # kg/m^3, Meseta at ~800 m elevation, warm
CEILING  = 120.0       # m AGL
TARGET_D = 0.70        # m
SIDELAP  = 0.25
TURN_EFF = 0.78
SWAP_MIN = 5.0

# ================================================================ variant A
print()
hr()
print("  VARIANT A - 'SWEEPER': RGB fixed wing, hand-launched foam twin-boom")
hr()

# ---- airframe & flight physics
AUW_A    = 2.3         # kg, all-up weight incl. camera and battery
V_CRUISE = 16.0        # m/s
LD       = 8.0         # lift-to-drag, honest for a foam twin-boom at this Re
ETA      = 0.55        # prop (0.65-0.70) x motor+ESC (0.80-0.85)

W = AUW_A * G0
P_cruise = W * V_CRUISE / (LD * ETA)          # electric watts
print(f"\n  [A1] Flight physics")
print(f"       AUW {AUW_A} kg -> weight {W:.1f} N")
print(f"       P_cruise = W*v/(L/D * eta) = {W:.1f}*{V_CRUISE}/({LD}*{ETA}) = {P_cruise:.0f} W electric")

# battery: 4S Li-ion (18650), 2 packs in parallel
V_NOM, AH  = 14.4, 10.4                       # V, Ah  (2x 4S2P LG M50-class)
E_WH       = V_NOM * AH
USABLE     = 0.85
t_endur_h  = E_WH * USABLE / P_cruise
print(f"       battery {V_NOM:.1f} V x {AH:.1f} Ah = {E_WH:.0f} Wh, {USABLE:.0%} usable")
print(f"       endurance = {t_endur_h*60:.0f} min   (sanity: Believer-class published ~90-120 min - consistent)")
assert 1.0 < t_endur_h < 2.5, "endurance out of sane range"

# ---- camera: used APS-C mirrorless + pancake prime
CAM_PX, CAM_PITCH, CAM_F = 6000, 3.9e-6, 0.016     # Sony a6000-class, 16 mm
gsd_A   = CEILING * CAM_PITCH / CAM_F
swath_A = CAM_PX * gsd_A
rate_A  = swath_A * (1 - SIDELAP) * V_CRUISE * TURN_EFF     # m^2/s
km2_flight = rate_A * t_endur_h * 3600 / 1e6
print(f"\n  [A2] Sensor: used 24 MP APS-C + 16 mm prime, 1 s intervalometer")
print(f"       GSD {gsd_A*100:.1f} cm  ({TARGET_D/gsd_A:.0f} px across the sphere - ID threshold is 6)")
print(f"       swath {swath_A:.0f} m,  {rate_A*3600/1e6:.1f} km2/h,  {km2_flight:.1f} km2 per flight")

# ---- battery logistics (formulas from battery_logistics.py)
CHG, COOL = 150.0, 10.0        # min; Li-ion charged gently at 0.5C for cycle life
cyc = t_endur_h * 60 + SWAP_MIN
packs_A = math.ceil((t_endur_h * 60 + COOL + CHG) / cyc)
print(f"\n  [A3] Packs to fly continuously: ceil(({t_endur_h*60:.0f}+{COOL:.0f}+{CHG:.0f})/({t_endur_h*60:.0f}+{SWAP_MIN:.0f})) = {packs_A}")

BOM_A = [
    ("Foam twin-boom airframe kit (Believer 1960 class)",           340),
    ("Pixhawk-class autopilot + M10 GPS + compass",                 270),
    ("Motors x2, ESCs, props, hand-launch spares",                  130),
    ("ELRS control link + 868 MHz telemetry",                       110),
    ("Used 24 MP APS-C body (a6000-class)",                         350),
    ("16 mm f/2.8 pancake prime, used",                             120),
    ("Hot-shoe/PWM intervalometer trigger + hard mount",             60),
    (f"Li-ion packs x{packs_A} (4S 10.4 Ah, built from 18650s)",    packs_A * 110),
    ("Dual-channel Li-ion charger",                                  90),
    ("Harness, connectors, 3D-printed camera bay, spares",          140),
]
tot_A = sum(v for _, v in BOM_A)
print(f"\n  [A4] Bill of materials")
for k, v in BOM_A:
    print(f"       {k:<56}{v:>7,.0f}E")
print(f"       {'TOTAL VARIANT A':<56}{tot_A:>7,.0f}E")

# ================================================================ variant B
print()
hr()
print("  VARIANT B - 'NIGHT CORE': 10-inch quad + Boson 640 thermal core")
hr()

# ---- thermal sensor choice
# Boson 640, 8.7 mm lens (50 deg HFOV), 12 um pitch. The <=9 Hz export-friendly
# version is CHEAPER and entirely sufficient: at 8 m/s survey speed a 1 Hz frame
# rate advances 8 m between frames against a 77 m forward footprint - 90% overlap.
TH_PX, TH_PITCH, TH_F, TH_FNO = 640, 12e-6, 0.0087, 1.0
gsd_B   = CEILING * TH_PITCH / TH_F
swath_B = TH_PX * gsd_B
Q = 10e-6 * TH_FNO / TH_PITCH
print(f"\n  [B1] Sensor: Boson 640, 8.7 mm f/1.0 (<=9 Hz export-friendly version)")
print(f"       GSD {gsd_B*100:.1f} cm, swath {swath_B:.0f} m, {TARGET_D/gsd_B:.1f} px on target")
print(f"       diffraction Q = {Q:.2f} (detector-limited - same check as the M3T, passes)")
print(f"       9 Hz is NOT a handicap: at 8 m/s, 1 fps gives ~90% forward overlap.")
assert 0.5 < Q < 1.4

# ---- hover/forward-flight power, momentum theory
AUW_B  = 1.7           # kg: 0.9 frame+motors+FC, 0.45 battery, 0.25 sensor+Pi, 0.1 misc
PROP_D = 0.254         # m, 10-inch props x4
A_disk = 4 * math.pi * (PROP_D / 2) ** 2
W_B    = AUW_B * G0
P_ideal = W_B ** 1.5 / math.sqrt(2 * RHO_AIR * A_disk)
FM, ETA_E = 0.65, 0.85
P_hover = P_ideal / FM / ETA_E
P_survey = P_hover * 0.95          # slow forward flight is marginally cheaper than hover
print(f"\n  [B2] Flight physics (momentum theory)")
print(f"       disk area {A_disk:.3f} m2, ideal {P_ideal:.0f} W, FM {FM}, electrical {P_hover:.0f} W hover")
E_B = 22.2 * 8.0       # 6S 8Ah Li-ion
t_B = E_B * 0.80 / P_survey
print(f"       battery {E_B:.0f} Wh -> {t_B*60:.0f} min survey endurance  (sanity: 10-inch Li-ion rigs ~40-55 min - consistent)")
assert 0.5 < t_B < 1.2
# thrust check: 4x ~2806.5-class motors on 6S/10" deliver ~1.4 kg each
TW = 4 * 1.4 / AUW_B
print(f"       thrust/weight = {TW:.1f}  (>=2 required - OK)")
assert TW >= 2

rate_B = swath_B * (1 - SIDELAP) * 8.0 * TURN_EFF
AUG_NIGHT = 7.4
km2_night = rate_B * AUG_NIGHT * 3600 * 0.55 / 1e6
packs_B = math.ceil((t_B * 60 + 15 + 75) / (t_B * 60 + SWAP_MIN))
print(f"       {rate_B*3600/1e6:.2f} km2/h -> ~{km2_night:.1f} km2 per August night; {packs_B} packs to cycle")

BOM_B = [
    ("Boson 640, 8.7 mm, <=9 Hz (via GroupGets/OEMcameras)",       2950),
    ("10-inch quad: frame, 4x motors, ESC, FC (ArduPilot)",         420),
    ("Raspberry Pi CM4 + USB capture + NVMe logger",                180),
    ("Vibration-isolated hard mount (printed + silicone)",           40),
    ("ELRS link + telemetry (shared spares with A)",                 80),
    (f"Li-ion packs x{packs_B} (6S 8 Ah)",                          packs_B * 130),
    ("Dual charger + field power wiring",                           130),
    ("Flashing green night beacon + strobes",                        90),
    ("Harness, spares, props",                                      110),
]
tot_B = sum(v for _, v in BOM_B)
print(f"\n  [B3] Bill of materials")
for k, v in BOM_B:
    print(f"       {k:<56}{v:>7,.0f}E")
print(f"       {'TOTAL VARIANT B':<56}{tot_B:>7,.0f}E")
print(f"\n       -> {BOM_B[0][1]/tot_B:.0%} of variant B is the thermal core. The drone is almost free;")
print("          you are buying a Boson and giving it wings.")

# ================================================================ comparison
print()
hr()
print("  COMPARISON - DIY vs used market vs contracting")
hr()
M3T_KIT = 7380
DAY_RATE = 1500
rgb_day_A = rate_A * t_endur_h * 3600 * 7 / 1e6     # 7 flights/day
BUILD_A, BUILD_B = 40, 50                           # honest integration hours

print(f"""
  {'option':<34}{'cash':>9}{'build':>8}{'RGB km2/d':>11}{'TH km2/night':>13}  legal envelope
  {'A: DIY RGB fixed wing':<34}{tot_A:>8,.0f}E{BUILD_A:>6} h{rgb_day_A:>11.1f}{'-':>13}  Open A3, VLOS only
  {'B: DIY thermal quad':<34}{tot_B:>8,.0f}E{BUILD_B:>6} h{'-':>11}{km2_night:>13.1f}  Open A3, VLOS only
  {'A + B (shared ground kit)':<34}{tot_A+tot_B-200:>8,.0f}E{BUILD_A+BUILD_B:>6} h{rgb_day_A:>11.1f}{km2_night:>13.1f}  Open A3, VLOS only
  {'Used M3T kit (prior analysis)':<34}{M3T_KIT:>8,.0f}E{0:>6} h{'37.7':>11}{'5.3':>13}  Open A2/A3, VLOS
  {'Contracted C6 fixed wing':<34}{'1,500E/d':>9}{0:>6} h{'45':>11}{'-':>13}  STS-02 BVLOS, 2 km
""")

print("  Notes the table cannot carry:")
print("  - A DIY build has no C-class mark: STS-02 is unavailable AT ANY PRICE. The")
print("    contracted operator's 12.6 km2/setup bubble cannot be replicated by building.")
print("  - The M3T's RGB day rate (37.7) and DIY-A's ({:.1f}) are both VLOS-limited in".format(rgb_day_A))
print("    practice: ~0.8 km2 per setup, then relocate. Per-setup, all VLOS options tie.")
print("  - Variant A's camera (24 MP APS-C at 2.9 cm) outresolves the M3T's RGB and")
print("    every satellite option by an order of magnitude. Identification is trivial.")
print("  - Build hours at engineer rates dwarf the cash gap: 90 h of integration is")
print("    real money at any loaded rate. DIY wins on cash only if the hours are free.")
print("  - One crash on day one: DIY-A loses ~{:,.0f}E and is repairable with foam and".format(tot_A - 350 - 120))
print("    glue; the camera usually survives. An M3T crash is a total loss of 4,500E.")

print()
hr()
print("  VERDICT")
hr()
print(f"""
  Total DIY cost, both aircraft, shared ground kit:  ~{tot_A+tot_B-200:,.0f} EUR + ~90 build-hours.

  The interesting split:

  - Variant A is the genuine bargain: {tot_A:,.0f} EUR for a machine that resolves the
    sphere at {TARGET_D/gsd_A:.0f} px, flies {t_endur_h*60:.0f}-minute sorties, and repairs with hot glue.
    Nothing you can buy touches its cost-per-km2 - IF your hours are free.

  - Variant B is not really a drone project. It is a {BOM_B[0][1]:,.0f} EUR sensor purchase
    with {tot_B - BOM_B[0][1]:,.0f} EUR of aircraft around it - and for {M3T_KIT:,.0f} EUR the used M3T
    delivers the same 640-class detector already integrated, gimballed, weather-
    sealed and warrantied. DIY thermal only wins if you want the Boson anyway
    (radiometric raw access, future payload integration) - which, for a company
    that flies stratospheric payloads, is a genuinely defensible reason.

  Recommendation: build A, buy the M3T used, skip B unless the Boson has a
  second life planned on your balloon payloads - where a 100 g radiometric
  640 core is exactly the instrument a recovery beacon wants next to it.
""")
hr()
