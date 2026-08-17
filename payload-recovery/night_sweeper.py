#!/usr/bin/env python3
"""
Iterating the DIY sweeper into a quiet night-capable aircraft.

Design goals, in order: works at night, acoustically discreet, cheap.
Scope note: 'discreet' means LOW NOISE - not waking villages, livestock or
dogs during pre-dawn sorties. The flashing green night beacon required by
EU/AESA night rules STAYS ON THE AIRCRAFT; conspicuity to other airspace
users and observers is a legal and safety requirement, not a design variable.

Prior art in exactly this class (foam fixed wing + LWIR, night survey):
  - Air Shepherd / UAV & Drone Solutions: night-only anti-poaching wings,
    6,000+ flight hours over African reserves - proof the concept is mature.
  - AeroVironment Raven/Puma: the hand-launched foam + IR form factor, proven
    for two decades.
  - Conservation surveys (koala/ungulate counts) fly thermal at dawn for the
    same reason we do: cold, calm air and sleeping confusers.

Physics: SI units. Acoustics via tip-speed scaling anchored on measured hobby
data; prop noise scales ~ V_tip^5.5, so tip speed is THE design variable.
Prices indicative street (EUR, Aug 2026).
"""
import math

def hr(c="="): print(c * 104)

G0, CEILING, TARGET_D = 9.80665, 120.0, 0.70
A_FOOT = math.pi * (TARGET_D / 2) ** 2
DT_K, T_ATM_TH = 5.0, 1.0      # pre-dawn contrast vs soil; LWIR path loss negligible at 120 m
SIDELAP, TURN_EFF = 0.25, 0.78

# ---------------------------------------------------------------- acoustics
# Anchor: a 10-inch hobby prop absorbing ~200 W at tip speed ~133 m/s measures
# ~65 dBA at 15 m (typical published hobby measurements). Scale:
#   dSPL = 55*log10(Vt/Vt0) + 10*log10(P/P0)   (tip-speed^5.5 law)
# Distance: spherical spreading, -20*log10(R/R0). A-weighted, no ground effect.
VT0, P0, SPL0, R0 = 133.0, 200.0, 65.0, 15.0
def spl_at_ground(v_tip, p_elec, alt=CEILING):
    if p_elec <= 0:
        return 0.0                      # motor off: airframe hiss, below ambient
    spl = SPL0 + 55 * math.log10(v_tip / VT0) + 10 * math.log10(p_elec / P0)
    return spl - 20 * math.log10(alt / R0)

def tip_speed(d_prop, rpm):
    return math.pi * d_prop * rpm / 60.0

AMBIENT_NIGHT = 32.0    # dBA, rural Meseta night (wind calm, distant road)

# ---------------------------------------------------------------- sensors
# 12 um pitch throughout; f/1.0-class optics; Q ~ 0.83 (checked previously).
SENSORS = {
    #  name                          px_w  focal_m  NETD_K  price_EUR
    "FLIR Lepton 3.5 (160x120)":    (160, 0.0014, 0.050,  250),
    "InfiRay P2-class (256x192)":   (256, 0.0032, 0.040,  340),
    "InfiRay Mini2-640, 9.1 mm":    (640, 0.0091, 0.040,  900),
    "FLIR Boson 640, 8.7 mm":       (640, 0.0087, 0.050, 2950),
}
def sensor_perf(px_w, f, netd, v=13.0):
    gsd = CEILING * 12e-6 / f
    swath = px_w * gsd
    px_on = TARGET_D / gsd
    cell = gsd ** 2
    fill = min(1.0, A_FOOT / cell)
    sigma = DT_K * fill * T_ATM_TH / netd
    rate = swath * (1 - SIDELAP) * v * TURN_EFF * 3600 / 1e6   # km2/h
    return gsd, swath, px_on, sigma, rate

print()
hr()
print("  NIGHT SWEEPER - iterating the 1,940 EUR day sweeper into a quiet night aircraft")
hr()
print("""
  Prior art check: this class EXISTS and works. Air Shepherd flew foam fixed
  wings with LWIR cameras, exclusively at night, over African reserves - 6,000+
  flight hours. We are re-implementing a proven concept at Meseta scale, not
  inventing one. The beacon stays on: quiet is a courtesy, conspicuity is law.
""")

# ---------------------------------------------------------------- iteration 0
print("[ITERATION 0] Baseline: day sweeper as designed (Believer twin-boom, APS-C RGB)")
vt_bel = tip_speed(0.229, 6000)         # 2x 9-inch at cruise
spl_bel = spl_at_ground(vt_bel, 80) + 3  # +3 dB: two props
print(f"    Night capability: NONE (RGB is blind at night)")
print(f"    Noise at ground from 120 m: {spl_bel:.0f} dBA vs {AMBIENT_NIGHT:.0f} dBA ambient"
      f"  -> {'audible hum' if spl_bel > AMBIENT_NIGHT else 'masked'}")
print(f"    Cost: 1,940 EUR\n")

# ---------------------------------------------------------------- iteration 1
print("[ITERATION 1] Bolt a cheap thermal core onto the Believer")
print(f"    {'sensor':<30}{'GSD':>8}{'swath':>8}{'px on target':>13}{'detect':>9}{'km2/h':>8}{'EUR':>7}")
for name, (pw, f, netd, price) in SENSORS.items():
    gsd, sw, pxon, sig, rate = sensor_perf(pw, f, netd, v=16.0)
    print(f"    {name:<30}{gsd*100:>6.0f}cm{sw:>7.0f}m{pxon:>13.1f}{sig:>8.0f}s{rate:>8.2f}{price:>7,}")
print("""    -> Detection is contrast-limited, so even the 250 EUR Lepton 'sees' the
       sphere - but at 1.0 m GSD every cooling straw patch is a candidate and
       nothing can be told apart. The P2-class core detects hard (125 sigma)
       at 1.6 px. The InfiRay 640 matches the Boson's geometry at 1/3 price.
       Noise and endurance unchanged - the airframe is still the limit.\n""")

# ---------------------------------------------------------------- iteration 2
print("[ITERATION 2] Swap airframe: twin-boom -> foam motor-glider (2.5 m class)")
AUW, LD, V_CR, ETA = 2.0, 12.0, 13.0, 0.55
W = AUW * G0
P_cruise = W * V_CR / (LD * ETA) + 8      # +8 W avionics/sensor
print(f"    AUW {AUW} kg, L/D {LD}, cruise {V_CR} m/s -> {P_cruise:.0f} W electric (vs 82 W twin-boom)")
E_WH = 150.0
t_endur = E_WH * 0.85 / P_cruise
print(f"    endurance on the same 150 Wh pack: {t_endur*60:.0f} min"
      f"  (sanity: foam motor-gliders publish 2.5-3.5 h - consistent)")
assert 2.0 < t_endur < 4.0

# night air bonus
rho_day, rho_night = 1.10, 1.16          # 35 C afternoon vs 12 C pre-dawn at 800 m
print(f"    night air: rho {rho_night} vs {rho_day} kg/m3 (+5%), zero thermal turbulence,")
print(f"    nocturnal boundary layer typically calm -> the quoted numbers are conservative at night")

# acoustics: big slow folding prop
vt_mg = tip_speed(0.356, 2800)           # 14-inch folding at cruise
spl_mg = spl_at_ground(vt_mg, P_cruise)
print(f"    14-inch folding prop at 2,800 rpm: tip speed {vt_mg:.0f} m/s (vs {vt_bel:.0f})")
print(f"    noise at ground: {spl_mg:.0f} dBA vs {AMBIENT_NIGHT:.0f} dBA ambient -> "
      f"{'BELOW ambient: unnoticeable' if spl_mg < AMBIENT_NIGHT else 'audible'}")
assert spl_mg < AMBIENT_NIGHT

# climb-glide profile
sink = V_CR / LD
glide_band = 60.0                        # m, glide 120 -> 60 m AGL, then climb back
t_glide = glide_band / sink
climb_rate, P_climb = 3.0, 220.0
t_climb = glide_band / climb_rate
duty_silent = t_glide / (t_glide + t_climb)
spl_climb = spl_at_ground(tip_speed(0.356, 5200), P_climb, alt=90.0)
print(f"    climb-glide option: glide {t_glide:.0f} s (motor OFF - silent), climb {t_climb:.0f} s")
print(f"    -> {duty_silent:.0%} of the sortie is a gliding airframe with the prop folded;")
print(f"       even the climb burst is {spl_climb:.0f} dBA at ground, a faint 20-second hum\n")

# ---------------------------------------------------------------- iteration 3
print("[ITERATION 3] Final configuration: motor-glider + InfiRay 640 + dual payload bay")
gsd, sw, pxon, sig, rate = sensor_perf(*SENSORS["InfiRay Mini2-640, 9.1 mm"][:3], v=V_CR)
km2_flight = rate * t_endur
AUG_NIGHT = 7.4
sorties = AUG_NIGHT / (t_endur + 0.15)
km2_night = km2_flight * sorties * 0.85
print(f"    thermal: {gsd*100:.0f} cm GSD, {sw:.0f} m swath, {pxon:.1f} px on target, {sig:.0f} sigma detection")
print(f"    smear at {V_CR} m/s: {V_CR*0.010/gsd:.1f} px on a {pxon:.1f} px target - irrelevant (checked pattern)")
print(f"    coverage: {rate:.2f} km2/h x {t_endur*60:.0f} min = {km2_flight:.1f} km2/sortie")
print(f"    an August night ({AUG_NIGHT} h usable): ~{sorties:.0f} sorties, ~{km2_night:.0f} km2 of thermal sweep")
print(f"    vs 7.3 km2/night for the DIY quad and 5.3 for the M3T - the wing wins on wing physics")

BOM = [
    ("Foam motor-glider kit, 2.5 m class",                        180),
    ("Low-Kv motor + 14-inch folding prop + spinner",              95),
    ("Pixhawk-class autopilot + M10 GPS + airspeed",              300),
    ("ELRS control link + 868 MHz telemetry",                     110),
    ("InfiRay Mini2-640, 9.1 mm, USB board",                      900),
    ("Raspberry Pi Zero 2 W logger + storage",                     80),
    ("Swappable day bay: used 24 MP APS-C + 16 mm + trigger",     530),
    ("Li-ion packs x3 (4S 10.4 Ah) + dual charger",               420),
    ("Flashing green night beacon + position strobes",             90),
    ("Harness, printed payload bays, spares",                     160),
]
tot = sum(v for _, v in BOM)
print(f"\n    Bill of materials (day AND night capable):")
for k, v in BOM:
    print(f"      {k:<56}{v:>7,}E")
print(f"      {'TOTAL':<56}{tot:>7,}E")
night_only = tot - 530
print(f"      (night-only, without the RGB day bay: {night_only:,} EUR)")

# ---------------------------------------------------------------- summary
print()
hr()
print("  ITERATION SUMMARY")
hr()
print(f"""
  {'iter':<6}{'configuration':<44}{'night':>7}{'dBA@gnd':>9}{'endur':>8}{'EUR':>8}
  {'0':<6}{'Believer + APS-C (day sweeper)':<44}{'no':>7}{spl_bel:>8.0f} {'93 min':>8}{'1,940':>8}
  {'1':<6}{'Believer + P2-class thermal':<44}{'weak':>7}{spl_bel:>8.0f} {'93 min':>8}{'2,290':>8}
  {'2':<6}{'Motor-glider airframe swap':<44}{'-':>7}{spl_mg:>8.0f} {f'{t_endur*60:.0f} min':>8}{'~same':>8}
  {'3':<6}{'Motor-glider + InfiRay 640 + day bay':<44}{'YES':>7}{spl_mg:>8.0f} {f'{t_endur*60:.0f} min':>8}{f'{tot:,}':>8}

  What the iteration bought, for +{tot-1940:,} EUR over the day sweeper:
  - Night capability at Boson-class geometry ({pxon:.1f} px, {sig:.0f} sigma) for 1/3 the Boson price
  - {spl_mg:.0f} dBA at ground against a {AMBIENT_NIGHT:.0f} dBA rural night - below ambient, the aircraft
    is inaudible in cruise and SILENT {duty_silent:.0%} of the time in climb-glide
  - {t_endur*60:.0f}-minute sorties: ~{km2_night:.0f} km2 of thermal per August night, 4x any quad option
  - The same airframe flies the APS-C by day: one aircraft, both jobs

  Chain to the mission: night thermal produces POSITIONS (detection at {sig:.0f} sigma,
  identification at {pxon:.1f} px still impossible - established); the day bay or a car
  confirms them. Air Shepherd proved this exact loop for a decade; ours is smaller,
  slower, quieter and pointed at one styrofoam ball instead of poachers.

  Honest costs not in the BOM: ~50-60 build hours (the thermal USB capture
  pipeline is the real work), ArduPilot tuning flights, and the pilot's night
  rating admin. And the A3 rules bind at night exactly as by day: VLOS to the
  beacon, 150 m from uninvolved people, relocation between setups.
""")
hr()
