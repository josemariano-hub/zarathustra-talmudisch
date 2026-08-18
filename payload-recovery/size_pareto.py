#!/usr/bin/env python3
"""
Pareto-optimal sweeper size: is 3 kg MTOM the right aircraft?

The 3.0 kg MTOM came from hand-launch thrust-to-weight, not a frontier.
Derive it: payload mass is FIXED, swath is sensor-fixed, and under VLOS the
relocation cadence is the daily bottleneck - so size buys endurance and wind
penetration while it taxes setups, cost and crash energy.

Scaling laws anchored at the established 2.6 kg day+radar point.
SI units.
"""
import math
def hr(c="="): print(c*104)

G0=9.80665; ETA=0.55
PAYLOAD=0.72          # kg, day config: camera bay+radar module+Pi/LTE/Iridium+beacon
AVIONICS_KG=0.10; P_AV=10.5
STRUCT_FRAC=0.454     # airframe+motor+prop+wiring fraction, ANCHORED to the real 2.6 kg
                      # mass budget (0.90+0.195+0.08 kg on 2.6) - foam shells are heavy
E_SPEC=250.0          # Wh/kg pack-level Li-ion
USABLE=0.85
SWATH=176.0; SIDELAP=0.25; TURN=0.78
DAY_H=14.0
VLOS_KM2=0.79         # bubble per setup

def aircraft(auw):
    batt = auw - PAYLOAD - AVIONICS_KG - STRUCT_FRAC*auw
    if batt <= 0: return None
    bf = batt/auw
    ld  = min(12.0*(auw/2.6)**0.12, 14.0)
    v   = 13.0*(auw/2.6)**0.15
    p   = auw*G0*v/(ld*ETA) + P_AV
    e   = batt*E_SPEC*USABLE
    t_h = e/p
    rate= SWATH*(1-SIDELAP)*v*TURN*3600/1e6            # km2/h airborne
    # VLOS daily model: per setup = clear bubble + overhead; sortie may span setups
    if   auw<=3.5: setup=8.0
    elif auw<=6.0: setup=15.0
    else:          setup=25.0
    t_clear = VLOS_KM2/rate*60.0                       # min to clear one bubble
    per_setup = t_clear + setup
    setups_day = DAY_H*60.0/per_setup
    km2_day = min(setups_day*VLOS_KM2, rate*DAY_H*0.8) # can't exceed airtime limit
    # other axes
    cost = 120*(auw/2.6)**1.3 + (batt*E_SPEC/150.0)*110*3 + 1900   # airframe+3 packs+fixed kit
    crash = 0.5*auw*v*v
    vg8 = math.sqrt(max(v*v-64.0,0.0))
    return dict(auw=auw,bf=bf,ld=ld,v=v,p=p,t=t_h*60,rate=rate,setup=setup,
                km2=km2_day,cost=cost,crash=crash,vg8=vg8,batt=batt)

print(); hr()
print("  SWEEPER SIZE - the Pareto sweep the 3 kg number never had")
hr()
print(f"""
    Fixed by the mission, independent of size: payload {PAYLOAD} kg (sensors,
    comms, beacons), swath {SWATH:.0f} m (the camera, not the wing), VLOS bubble
    {VLOS_KM2} km2 per setup. Size buys endurance, speed and wind margin;
    it taxes launch cadence, cost, crash energy and van space.
""")
print(f"    {'AUW':>6}{'batt%':>7}{'L/D':>6}{'v':>6}{'endur':>7}{'launch':>8}{'km2/day':>9}"
      f"{'kit EUR':>9}{'crash J':>9}{'Vg@8m/s':>9}")
rows=[]
for auw10 in range(12, 82, 4):
    a=aircraft(auw10/10)
    if a is None or a['bf']<0.10:
        print(f"    {auw10/10:>5.1f}kg   INFEASIBLE - fixed payload starves the battery")
        continue
    rows.append(a)
    lch = "hand" if a['auw']<=3.5 else ("bungee" if a['auw']<=6 else "2-crew")
    print(f"    {a['auw']:>5.1f}kg{a['bf']*100:>6.0f}%{a['ld']:>6.1f}{a['v']:>5.1f}m"
          f"{a['t']:>6.0f}m{lch:>8}{a['km2']:>9.1f}{a['cost']:>9,.0f}{a['crash']:>9.0f}{a['vg8']:>8.1f}m")

# anchor check: 2.6 kg case vs established 127 min day+radar
anchor=aircraft(2.6)
assert abs(anchor['t']-127)/127 < 0.20, f"anchor drift: {anchor['t']:.0f} min"
best=max(rows,key=lambda r:r['km2'])
print(f"""
    Anchor check: 2.6 kg case gives {anchor['t']:.0f} min vs the established 127 min - consistent.

  READING THE FRONTIER

    - BELOW ~1.9 kg: infeasible or battery-starved. The 0.72 kg payload is a
      fixed tax; small airframes pay it in battery fraction and die early.
    - THE KNEE, 2.4-3.4 kg: battery fraction 20-29%, hand launch keeps the
      per-setup overhead at 8 min, and daily coverage peaks (~{best['km2']:.0f} km2/day
      at {best['auw']:.1f} kg). Wind penetration at 8 m/s is workable ({aircraft(3.0)['vg8']:.0f} m/s).
    - ABOVE 3.5 kg: the bungee arrives. Endurance keeps climbing ({aircraft(5.0)['t']:.0f} min
      at 5 kg) but daily coverage FALLS ({aircraft(5.0)['km2']:.1f} km2/day) because under
      VLOS you relocate ~{DAY_H*60/ (VLOS_KM2/aircraft(5.0)['rate']*60+15):.0f} times a day and each launch now costs 15 min
      instead of 8. Crash energy doubles, the kit price climbs, and the wing
      stops fitting across the van. Size buys the wrong currency: endurance
      was never the VLOS bottleneck - setups are.
    - The 5+ kg class only wins if BVLOS ever arrives (setups vanish, lines
      lengthen) - and a homebuilt cannot fly BVLOS, so that branch is closed
      by regulation, not physics.

  VERDICT: 3.0 kg MTOM is confirmed - now by the frontier, not by habit.
  It sits at the knee: hand-launch cadence, ~28% battery fraction, peak
  km2/day, tolerable crash energy, one-person field ops. The right answer
  to "should it be bigger?" is: only if the rules ever let it fly farther
  than the pilot can see. Until then, the small quiet wing wins the day.
""")
hr()

# ================================================================ BVLOS counterfactual
print()
hr()
print("  COUNTERFACTUAL: ASSUME NO LINE-OF-SIGHT CONSTRAINT - does the knee move?")
hr()
TURN_BVLOS=0.93       # 5+ km lines, turns become rare
DUTY=0.85             # pack swaps only - no relocations at all
STANDOFF_KM=10.0      # launch point to survey area, one site serves the ellipse
print(f"""
    Remove VLOS entirely: one launch site, {STANDOFF_KM:.0f} km standoff, long lines
    (turn efficiency {TURN_BVLOS} vs 0.78), no relocations, packs cycling.

    {'AUW':>6}{'v':>7}{'endur':>8}{'transit loss':>13}{'km2/h':>8}{'km2/day':>9}{'kit EUR':>9}{'km2/day/EUR':>12}""")
bv={}
for auw in (2.0,2.4,2.8,3.2,4.0,5.0,6.0,8.0):
    a=aircraft(auw)
    rate=SWATH*(1-SIDELAP)*a['v']*TURN_BVLOS*3600/1e6
    transit=2*STANDOFF_KM*1000/a['v']/60
    prod=max(a['t']-transit,0)/a['t']
    day=rate*DAY_H*DUTY*prod
    bv[auw]=(day,a['cost'])
    print(f"    {auw:>5.1f}kg{a['v']:>6.1f}m{a['t']:>7.0f}m{transit:>10.0f}min{rate:>8.1f}{day:>9.0f}{a['cost']:>9,.0f}{day/a['cost']*1000:>12.1f}")
d32,c32=bv[3.2]; d8,c8=bv[8.0]
print(f"""
    Reading it: without LOS the aircraft flies all day from one site and
    coverage jumps for EVERY size (the real BVLOS dividend is GEOMETRY -
    long lines and zero relocations - worth ~2x at any mass). But size
    still buys almost nothing: 8 kg out-covers 3.2 kg by only {d8/d32-1:+.0%},
    because swath is fixed by the camera and speed scales as AUW^0.15.
    Meanwhile the 8 kg costs {c8/c32-1:+.0%} more, quadruples crash energy, and
    needs the bungee crew.

    THE FLEET COMPARISON that settles it:
      1 x 8.0 kg : {d8:>5.0f} km2/day for {c8:>6,.0f} EUR
      2 x 3.2 kg : {2*d32:>5.0f} km2/day for {2*c32:>6,.0f} EUR   <- +62% coverage for +18% money,
                                                 attrition-tolerant, spares shared

    VERDICT, UNCHANGED AND STRONGER: the knee stays at ~3 kg even without
    LOS, because coverage is bought MULTIPLICATIVELY (more aircraft, wider
    sensors) not by scaling one airframe. What BVLOS would actually change:
    fly longer lines (turn eff 0.78 -> 0.93), budget transit reserves, and
    nothing about the aircraft - whose LTE-primary comms architecture is,
    conveniently, already BVLOS-shaped. The 61 MP camera (+52% swath) and a
    second airframe are each worth more than any kilogram of extra wing.
""")
hr()
