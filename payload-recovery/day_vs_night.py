#!/usr/bin/env python3
"""
An honest recheck: do we really see the sphere better at night than by day?

Short answer: NO - and the challenge that prompted this recheck is correct.
The brief drifted into treating night thermal as the flagship. Recomputed
side by side, day RGB is the stronger search mode and night is the second
shift plus the tie-breaker. This file makes the correction explicit.

Also: the Bambu X1C printed-parts manifest for the sweeper.

SI units; same optics/coverage formulas as sensor_upgrade.py.
"""
import math
def hr(c="="): print(c*104)

CEILING, TARGET = 120.0, 0.70
SIDELAP, TURN, V = 0.25, 0.78, 13.0
RESERVE, OVERHEAD = 0.85, 6.0

def optics(px_w, pitch, f):
    gsd = CEILING*pitch/f
    return gsd, px_w*gsd, px_w*gsd*(1-SIDELAP)*V*TURN*3600/1e6

def sortie_km2(rate, endur):
    return rate*(endur*RESERVE-OVERHEAD)/60.0

print(); hr()
print("  DAY vs NIGHT - the recheck the question deserved")
hr()

g_day, sw_day, r_day = optics(6000, 3.9e-6, 0.016)      # a6000 + 16 mm
g_ngt, sw_ngt, r_ngt = optics(640, 12e-6, 0.0091)       # InfiRay 640
day_sortie  = sortie_km2(r_day, 138)
ngt_sortie  = sortie_km2(r_ngt, 158)

print(f"""
[1] SENSOR-FOR-SENSOR, DAY WINS ALMOST EVERYTHING

    {'':<30}{'day RGB':>12}{'night thermal':>15}
    {'GSD':<30}{g_day*100:>10.1f}cm{g_ngt*100:>13.1f}cm
    {'px on the sphere':<30}{TARGET/g_day:>12.1f}{TARGET/g_ngt:>15.1f}
    {'identify without descending?':<30}{'YES':>12}{'no':>15}
    {'coverage per sortie':<30}{day_sortie:>9.1f} km2{ngt_sortie:>12.1f} km2
    {'terrain-floor risk':<30}{'none':>12}{'real at 50 m':>15}
    {'confuser handling':<30}{'shape, at 3 cm':>12}{'  unique signature':>17}

    At 2.9 cm a silage bale, a stone and a plastic sheet are OBVIOUSLY not a
    0.7 m sphere - the satellite's discrimination problem simply does not
    exist at drone GSD. Day RGB detects, identifies and covers more, in one
    pass, with no low-altitude night maneuvering.
""")

# per-24h tempo, August: ~14 h flyable daylight, 7.4 h usable night
DAY_H, NGT_H = 14.0, 7.4
day_24 = r_day*DAY_H*0.80
ngt_24 = r_ngt*NGT_H*0.80
print(f"""[2] WHAT NIGHT ACTUALLY BUYS: HOURS, NOT VISION

    August day (~{DAY_H:.0f} h flyable):   {day_24:>5.1f} km2 of RGB search
    August night ({NGT_H:.1f} h usable):   {ngt_24:>5.1f} km2 of thermal search
    Day+night total:              {day_24+ngt_24:>5.1f} km2/24h  (+{ngt_24/(day_24):.0%} tempo)

    (Airtime-limited figures. Under strict VLOS both are relocation-limited
    - ~0.8 km2 per pilot setup, as established earlier - so the real daily
    numbers are lower for BOTH modes equally; the day:night ratio holds.)

    So the honest sentence is: at night we do not see the sphere BETTER -
    we see it DIFFERENTLY, and we get to keep searching after sunset.
    "Better at night" was true for one narrow thing only: the thermal
    CONTRAST signature (a 5 K cold anomaly no bale, rock or plastic sheet
    can imitate) exists only at night. That makes thermal the TIE-BREAKER
    for a candidate that day RGB cannot call - white blob deep in a hedge,
    half-buried, in shadow - not the primary search instrument.

[3] CORRECTED DOCTRINE AND SHOPPING ORDER

    - PRIMARY:   day RGB sweep. Detects and identifies in one pass.
    - SECOND SHIFT: night thermal, when the ellipse is big enough that
      {day_24:.0f} km2/day of daylight coverage is not finishing the job fast
      enough, or ploughing pressure demands 24 h tempo.
    - TIE-BREAKER: thermal signature on specific ambiguous candidates.

    Procurement re-order: buy airframe + camera + comms FIRST (~2,640 EUR
    without the thermal core) and start flying days immediately. Add the
    900 EUR InfiRay when - and only when - the ellipse turns out larger
    than about two day-searches of area, or day sorties produce
    ambiguous candidates that need the cold-anomaly check. The telemetry
    still decides everything: a small ellipse never needs the night shift.
""")

hr()
print("  BAMBU X1C - printed-parts manifest for the sweeper")
hr()
PARTS = [
 # part, material, why
 ("Camera/thermal payload bays (swappable)","CF-PETG","stiff, dimensionally stable in a hot car"),
 ("Battery tray + strap anchors",           "CF-PETG","the 600 g pack must not move in a hand launch"),
 ("Motor mount reinforcement plate",        "CF-PETG","print flat, load in-plane; NOT the firewall itself"),
 ("Thermal-core isolation mount",           "TPU",    "replaces the silicone-damper hack, tuned durometer"),
 ("Prop-saver belly skids",                 "TPU",    "field landings on stubble, every sortie"),
 ("LTE/ELRS/Iridium antenna mounts",        "PETG",   "RF-transparent, no CF near antennas"),
 ("Hatches, covers, wire combs, GPS mast",  "PETG",   "quick reprints when field repairs eat them"),
 ("Hand-launch grip insert",                "CF-PETG","repeatable release at 3.0 kg MTOM"),
 ("Charge-crate fan duct (pack cooling)",   "PETG",   "the 20 EUR fan that saves a battery, ducted"),
 ("Octahedral corner-reflector frame",      "CF-PETG","NEXT FLIGHT: print frame, bond aluminium sheet"),
]
print(f"\n    {'part':<44}{'material':>9}  note")
for p,m,n in PARTS: print(f"    {p:<44}{m:>9}  {n}")
print("""
    DO NOT PRINT: propellers, the wing spar (buy carbon tube), any part
    bathed in motor heat unless switched to ASA. CF-PETG is stiff but its
    layer adhesion is the weak axis - orient loads in-plane, and keep CF
    filament away from antenna line-of-sight (carbon is conductive).

    BOM effect: replaces ~120 EUR of bought mounts, bays and brackets with
    ~25 EUR of filament, and turns every field breakage into an overnight
    reprint instead of a shipping delay. The printer also manufactures the
    corner-reflector cluster for the next balloon flight - the part of this
    whole saga that makes the NEXT recovery a non-event.
""")
hr()
