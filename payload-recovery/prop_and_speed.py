#!/usr/bin/env python3
"""
Cruise speed, done properly - and the propellers that follow from it.

The challenge is fair: V = 13 m/s was an airframe-class assumption, never an
optimum. The real objective is coverage - per Wh when energy-limited, per
hour when time-limited - flown crosswind in real wind, subject to sensor
constraints. This file derives the optimum, checks the sensors and the
noise at speed, and only then picks the propellers.

SI units. Drag polar calibrated to the established design point.
"""
import math
def hr(c="="): print(c*104)

G0=9.80665
AUW=2.09; W=AUW*G0
ETA=0.55; P_AVION=8.0
E_WH=150.0; USABLE=0.85
SWATH_RGB=176.0; SWATH_TH=101.0
SIDELAP, TURN = 0.25, 0.78

# ---- drag polar: D = k1 V^2 + k2 / V^2, calibrated so (L/D)max = 12 at 13 m/s
V_STAR, LD_MAX = 13.0, 12.0
D_STAR = W/LD_MAX
k1 = (D_STAR/2)/V_STAR**2
k2 = (D_STAR/2)*V_STAR**2
def drag(v):   return k1*v*v + k2/(v*v)
def p_elec(v): return drag(v)*v/ETA + P_AVION

# ---- acoustics (same anchoring as night_sweeper.py)
def spl_ground(v):
    p = p_elec(v)
    rpm = 2800.0*math.sqrt(p/48.0)          # crude but consistent with prior sections
    vt  = math.pi*0.356*rpm/60.0
    return 65 + 55*math.log10(vt/133.0) + 10*math.log10(p/200.0) - 20*math.log10(120.0/15.0), rpm, vt

print(); hr()
print("  CRUISE SPEED, OPTIMIZED - not assumed")
hr()

# ---------------------------------------------------------------- sensors first
print(f"""
[1] DO THE SENSORS LIMIT SPEED? - checked, and no

    RGB, 1/2000 s shutter:  blur = V/2000 -> at 20 m/s, 1.0 cm = 0.35 px. Fine.
    RGB, 1 fps frame rate:  along-track footprint 116 m -> gapless to ~90 m/s.
    Thermal, 10 ms tau:     smear at 20 m/s = 1.3 px on 4.4 px. Acceptable.
    Thermal, 1 fps:         81 m footprint -> gapless to ~65 m/s.
    Radar, chirps at kHz:   irrelevant at aircraft speeds.

    Every sensor clears 20+ m/s. The speed decision belongs to the airframe
    and the mission constraint, not the payload. So which constraint binds?
""")

# ---------------------------------------------------------------- two regimes
print("[2] THE OPTIMUM DEPENDS ON WHICH RESOURCE IS SCARCE\n")
print("    Survey lines are flown CROSSWIND (constant crab both directions, so")
print("    sidelap stays uniform): ground speed Vg = sqrt(Va^2 - Vw^2).\n")
print(f"    {'wind':>6} | {'ENERGY-limited: max km2/Wh':^34} | {'TIME-limited: max km2/h':^30}")
print(f"    {'':>6} | {'best Va':>8}{'Vg':>6}{'P':>6}{'km2/Wh*':>12} | {'Va':>6}{'Vg':>7}{'km2/h*':>10}")
best={}
for vw in (0.0, 4.0, 8.0):
    # energy-limited: maximize Vg/P
    vs=[v/10 for v in range(int((vw+1.5)*10), 221)]
    v_e=max(vs, key=lambda v: math.sqrt(max(v*v-vw*vw,1e-9))/p_elec(v))
    vg_e=math.sqrt(v_e*v_e-vw*vw)
    eff=SWATH_RGB*(1-SIDELAP)*TURN*vg_e/p_elec(v_e)*3600/1e6   # km2 per Wh... per W*h
    # time-limited: max Vg -> structural/prop ceiling, take 18 m/s foam-glider limit
    v_t=18.0
    vg_t=math.sqrt(v_t*v_t-vw*vw)
    rate=SWATH_RGB*(1-SIDELAP)*TURN*vg_t*3600/1e6
    best[vw]=(v_e,vg_e)
    print(f"    {vw:>4.0f}m/s | {v_e:>6.1f}m/s{vg_e:>6.1f}{p_elec(v_e):>5.0f}W{eff:>12.3f} | {v_t:>4.0f}m/s{vg_t:>7.1f}{rate:>10.1f}")
print("      (*RGB payload; thermal scales by swath 101/176)")

v0,_=best[0.0]; v8,vg8=best[8.0]
print(f"""
    Two honest findings:
    - In calm air the energy optimum is ~{v0:.0f} m/s - the 13 m/s assumption was
      close but slightly slow; the avionics power floor pushes the optimum
      a little above best-L/D (classic MacCready-with-sink result).
    - In wind, SPEED UP: at 8 m/s wind the optimum airspeed rises to ~{v8:.0f} m/s.
      The energy optimum is BROAD - flying the calm-air speed in that wind
      costs only ~1% in km2/Wh - but it costs ~15% in km2/HOUR, because
      ground speed sags. Speeding up in wind is nearly free energy-wise
      and recovers the lost ground speed: textbook speed-to-fly, applied
      to surveying. Practical rule: add half the wind to the airspeed.

    WHICH REGIME ARE WE IN? With 3 packs cycling and the van charging, energy
    is NOT scarce - flight hours are (daylight, VLOS relocations, crew). So
    the day sweep should fly the TIME-limited answer: fast cruise ~16-18 m/s,
    +30-38% coverage per hour over 13 m/s, paid for in watts we can afford.
    The night thermal sortie flips regimes: packs cycle slower at night, the
    thermal swath is narrow, and quiet matters - fly the energy optimum.
""")

# ---------------------------------------------------------------- noise at speed
print("[3] DOES FAST CRUISE STAY QUIET? - the check that could veto it\n")
print(f"    {'Va':>6}{'P elec':>9}{'rpm':>7}{'tip':>8}{'dBA at ground':>15}   vs 32 dBA night ambient")
for v in (13.0, 16.0, 18.0, 20.0):
    s,rpm,vt=spl_ground(v)
    print(f"    {v:>4.0f}m/s{p_elec(v):>8.0f}W{rpm:>7.0f}{vt:>7.0f}m{s:>13.0f}  {'under' if s<32 else 'OVER'}")
print("""
    Even 20 m/s stays under the rural night ambient - the acoustic design
    margin survives the fast optimum. Day flying has ~45 dBA ambient and
    does not care at all. Noise does not veto speed; fly the optimum.
""")

# ---------------------------------------------------------------- propellers
print("[4] THE PROPELLERS TO BUY - now derivable\n")
print("    Requirements: folding (climb-glide), pitch speed matching TWO cruise")
print("    regimes, tip speed <= ~65 m/s at cruise for the night acoustic case,")
print("    and climb thrust at the 220 W burst. Pitch speed = rpm/60 * pitch.\n")
PROPS=[
 ("Aeronaut CAM 14x8 folding",  0.356, 8,  "night/energy cruise 12-13 m/s at ~2,900 rpm, tip 54 m/s"),
 ("Aeronaut CAM 14x11 folding", 0.356, 11, "day/fast cruise 16-18 m/s at ~3,300 rpm, tip 61 m/s"),
 ("Aeronaut CAM 13x11 folding", 0.330, 11, "spare/fast alternative, slightly higher rpm"),
]
print(f"    {'prop':<30}{'pitch speed @3000rpm':>21}  role")
for name,d,pitch,role in PROPS:
    ps=3000/60*pitch*0.0254
    print(f"    {name:<30}{ps:>18.1f} m/s  {role}")
print(f"""
    BUY LIST (folding-prop system, motor-glider standard):
      Aeronaut CAM blades 14x8, 2 pairs                    ~44 EUR
      Aeronaut CAM blades 14x11, 2 pairs                   ~48 EUR
      42 mm turbo spinner + folding yoke, 8 mm shaft       ~28 EUR
      Magnetic prop balancer                               ~15 EUR
      ------------------------------------------------------------
      TOTAL                                               ~135 EUR
      (replaces the 95 EUR 'motor + folding prop' line's prop share;
       net BOM delta ~ +90 EUR - the price of flying two optima)

    Rules: swap blades, not aircraft trim - the yoke stays. Balance every
    pair (an unbalanced folder is the loudest thing on the airframe and
    eats the thermal camera's vibration budget). NEVER print propellers.
    The 14x8 flies the quiet night survey at the energy optimum; the 14x11
    flies the fast day sweep at the time optimum. Two props, two missions,
    one aircraft - the same doctrine as the payload bays.
""")
hr()
