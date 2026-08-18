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
