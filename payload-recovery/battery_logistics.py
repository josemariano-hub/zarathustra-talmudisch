#!/usr/bin/env python3
"""
How many batteries to keep one multirotor flying continuously?

The short formula the question asks for is charge time divided by flight time.
That is the right starting point but it under-counts, because a pack is also
unavailable while it cools, and because charging throughput is capped by the
number of parallel charging channels and by the power you can generate in a field.

This also checks whether continuous flight is the binding constraint at all:
under visual-line-of-sight rules the legal bubble around the pilot may be
exhausted long before a battery is.

SI units, except battery energy in Wh and times in minutes where that reads better.
"""
import math

def hr(c="="): print(c * 104)

CEILING  = 120.0
TARGET_D = 0.70
SIDELAP  = 0.25
TURN_EFF = 0.78

# ---------------------------------------------------------------- candidates
# Second-hand thermal-capable multirotors. Prices are indicative used-market
# figures, not quotes, and exclude batteries (see the warning at the end).
AIRCRAFT = {
    "DJI Mavic 2 Enterprise Adv.": dict(
        flight=29, packs=1, wh=59.3, charge=90, cool=15, channels=1,
        rgb_px=5472, rgb_pitch=2.4e-6, rgb_f=0.0088, th_px=640, th_dfov=57.0,
        spd=11.0, used=2800, batt_new=180),
    "Autel EVO II Dual 640T v3": dict(
        flight=34, packs=1, wh=82.0, charge=90, cool=15, channels=1,
        rgb_px=5472, rgb_pitch=2.4e-6, rgb_f=0.0088, th_px=640, th_dfov=56.0,
        spd=11.0, used=4000, batt_new=230),
    "DJI Mavic 3 Thermal (M3T)": dict(
        flight=42, packs=1, wh=77.0, charge=60, cool=15, channels=1,
        rgb_px=8064, rgb_pitch=2.4e-6, rgb_f=0.0124, th_px=640, th_dfov=61.0,
        spd=12.0, used=4500, batt_new=270),
    "DJI Matrice 30T": dict(
        flight=38, packs=2, wh=131.6, charge=60, cool=20, channels=2,
        rgb_px=8000, rgb_pitch=2.4e-6, rgb_f=0.0124, th_px=640, th_dfov=45.0,
        spd=13.0, used=9000, batt_new=750),
    "DJI Matrice 300 + H20T": dict(
        flight=50, packs=2, wh=274.0, charge=60, cool=20, channels=2,
        rgb_px=5184, rgb_pitch=2.4e-6, rgb_f=0.0247, th_px=640, th_dfov=40.6,
        spd=14.0, used=13000, batt_new=1100),
}

SWAP = 4.0          # min, land, swap packs, restart the mission
CHARGE_EFF = 0.85

print()
hr()
print("  BATTERY LOGISTICS FOR CONTINUOUS SORTIES")
hr()

# ---------------------------------------------------------------- 1. the formula
print("\n[1] The formula, corrected")
print("""
    Naive:   N = charge / flight

    Actual:  a pack is unavailable for (flight + cooldown + charge) after each
             launch, while the aircraft launches again every (flight + swap).

                 N_sets  = ceil( (flight + cool + charge) / (flight + swap) )
                 N_packs = N_sets x packs_per_flight

             and separately, charging throughput must keep up:

                 channels_needed = ceil( packs x charge / (flight + swap) )

    Cooldown is the term people forget. A DJI hub refuses to charge a pack above
    about 40 C, and in an August field in Castilla that is 15-20 minutes of doing
    nothing. It can add a whole battery to the requirement on its own.
""")

print(f"    {'aircraft':<30}{'naive':>8}{'+cool':>8}{'sets':>7}{'PACKS':>8}{'ch. needed':>12}{'have':>6}")
for name, a in AIRCRAFT.items():
    naive = a["charge"] / a["flight"]
    cyc = a["flight"] + SWAP
    sets = math.ceil((a["flight"] + a["cool"] + a["charge"]) / cyc)
    packs = sets * a["packs"]
    ch = math.ceil(a["packs"] * a["charge"] / cyc)
    flag = "" if ch <= a["channels"] else "  <-- need a 2nd charger"
    print(f"    {name:<30}{naive:>8.1f}{(a['charge']+a['cool'])/a['flight']:>8.1f}"
          f"{sets:>7}{packs:>8}{ch:>12}{a['channels']:>6}{flag}")

print("\n    -> Three to four packs sustains a single-battery aircraft; six to eight a")
print("       twin-pack one. Beyond that you are buying idle inventory, not airtime.")

# ---------------------------------------------------------------- 2. cooldown sensitivity
print("\n[2] What cooldown actually costs you")
print("    Whether it tips you into another pack depends on how much headroom the")
print("    aircraft's flight-to-charge ratio already has. Raw ratio shown alongside,")
print("    so you can see how close each one sits to rounding up.\n")
print(f"    {'condition':<38}", end="")
for nm in ["M3T", "M2EA"]:
    print(f"{nm + ' ratio':>12}{nm + ' packs':>12}", end="")
print()
for cool, cond in [(0, "shaded, cool morning, forced-air fan"),
                   (10, "spring / autumn, ambient 15 C"),
                   (20, "August afternoon, ambient 35 C"),
                   (30, "midday in the sun, no shade")]:
    print(f"    {cond:<38}", end="")
    for key in ["DJI Mavic 3 Thermal (M3T)", "DJI Mavic 2 Enterprise Adv."]:
        a = AIRCRAFT[key]
        ratio = (a["flight"] + cool + a["charge"]) / (a["flight"] + SWAP)
        print(f"{ratio:>12.2f}{math.ceil(ratio) * a['packs']:>12}", end="")
    print()
print("\n    -> The M3T charges fast relative to its endurance, so it sits at 2.2-2.9")
print("       and stays on 3 packs whatever the weather. The older M2EA charges slowly")
print("       relative to a shorter flight, sits right on the boundary, and a hot")
print("       August afternoon genuinely costs it a fifth pack.")
print("       So: a 20 EUR fan and a shaded crate is worth having either way, but it")
print("       only saves you money on the slow-charging aircraft.")

# ---------------------------------------------------------------- 3. field power
print("\n[3] Field power - the constraint that actually bites")
print("    To sustain continuous flight you must generate, on average, the energy")
print("    the aircraft burns, divided by charger efficiency.\n")
print(f"    {'aircraft':<30}{'Wh/sortie':>11}{'avg draw':>10}{'peak draw':>11}  field supply")
for name, a in AIRCRAFT.items():
    wh = a["wh"] * a["packs"]
    cyc_h = (a["flight"] + SWAP) / 60.0
    avg = wh / cyc_h / CHARGE_EFF
    ch = math.ceil(a["packs"] * a["charge"] / (a["flight"] + SWAP))
    peak = a["wh"] / (a["charge"] / 60.0) / CHARGE_EFF * max(ch, 1)
    if peak < 300:   supply = "car inverter or 500 Wh power station"
    elif peak < 800: supply = "1 kWh power station"
    else:            supply = "2 kW generator or 2+ kWh station"
    print(f"    {name:<30}{wh:>9.0f}Wh{avg:>9.0f}W{peak:>10.0f}W  {supply}")
print("\n    -> A single-battery Mavic-class aircraft sips ~130 W average. You can run it")
print("       all day off a car inverter. A twin-TB60 Matrice 300 needs ~700 W average,")
print("       which is a real generator, fuel, and noise at 04:00 in a village field.")
print("       For night thermal work that difference matters more than the spec sheet.")

# ---------------------------------------------------------------- 4. reality check
print("\n[4] Reality check: is the battery even the bottleneck?")
print("    Under VLOS the pilot may only work a ~500 m bubble. Time to exhaust it:\n")
print(f"    {'aircraft':<30}{'RGB rate':>12}{'VLOS area':>12}{'time to clear':>15}{'vs flight':>11}")
for name, a in AIRCRAFT.items():
    gsd = CEILING * a["rgb_pitch"] / a["rgb_f"]
    swath = a["rgb_px"] * gsd
    rate = swath * (1 - SIDELAP) * a["spd"] * TURN_EFF        # m2/s
    area = math.pi * 500.0 ** 2
    t_min = area / rate / 60.0
    print(f"    {name:<30}{rate*3600/1e6:>10.2f}km2/h{area/1e6:>11.2f}km2"
          f"{t_min:>13.0f} min{t_min/a['flight']:>10.0%}")
print("\n    -> Every one of these clears its entire legal VLOS bubble in roughly a third")
print("       to a half of one battery. You then have to pack up and drive to the next")
print("       field. Under strict VLOS you are RELOCATION-limited, not energy-limited,")
print("       and a fourth battery buys you nothing.")
print("\n       Buying more batteries only pays off if you first buy more range:")
print("         - an observer and an EVLOS arrangement, or")
print("         - a second pilot leapfrogging setups in a second vehicle, or")
print("         - a bespoke specific-category authorisation.")
print("       Of those, the second pilot is the cheapest and doubles throughput outright.")

# ---------------------------------------------------------------- 5. night thermal
print("\n[5] The night thermal sortie, which is the case that DOES need batteries")
print("    Thermal sweeps a small core continuously from one setup - no relocation,")
print("    because you are re-flying ground you already know rather than covering new.\n")
AUG_NIGHT = 7.4
for name in ["DJI Mavic 3 Thermal (M3T)", "DJI Matrice 30T"]:
    a = AIRCRAFT[name]
    sorties = AUG_NIGHT * 60 / (a["flight"] + SWAP)
    packs_used = sorties * a["packs"]
    sets = math.ceil((a["flight"] + a["cool"] + a["charge"]) / (a["flight"] + SWAP))
    w, h = a["th_px"], a["th_px"] * 0.8
    f_px = (math.hypot(w, h) / 2) / math.tan(math.radians(a["th_dfov"] / 2))
    tg = CEILING / f_px
    tsw = w * tg
    trate = tsw * (1 - SIDELAP) * 8.0 * TURN_EFF
    print(f"    {name}")
    print(f"      {sorties:.0f} sorties across a {AUG_NIGHT:.1f} h August night, "
          f"{packs_used:.0f} pack-charges")
    print(f"      {sets*a['packs']} packs cycling keeps it airborne all night "
          f"({tg*100:.0f} cm thermal GSD, {TARGET_D/tg:.1f} px on target)")
    print(f"      clears ~{trate*AUG_NIGHT*3600*0.55/1e6:.1f} km2 of thermal core per night\n")

# ---------------------------------------------------------------- 6. shopping list
print("[6] Shopping list, and the one thing not to buy used")
a = AIRCRAFT["DJI Mavic 3 Thermal (M3T)"]
sets = math.ceil((a["flight"] + a["cool"] + a["charge"]) / (a["flight"] + SWAP))
npacks = sets * a["packs"]
items = [
    ("Mavic 3 Thermal airframe + controller, used", a["used"]),
    (f"{npacks} x BS65 battery, NEW (see warning)", npacks * a["batt_new"]),
    ("2nd charging hub, so throughput is not the limit", 220),
    ("2 kWh portable power station", 1300),
    ("12 V fan + insulated crate for pack cooldown", 60),
    ("Flashing green beacon for night operations", 90),
    ("Spare props, filters, SD cards, hard case", 400),
]
tot = sum(v for _, v in items)
for label, v in items:
    print(f"    {label:<52}{v:>9,.0f}E")
print(f"    {'':<52}{'-'*9}")
print(f"    {'total':<52}{tot:>9,.0f}E")
print(f"\n    Pays back against contracting at 1,500 EUR/day in {tot/1500:.0f} search days.")

print("\n    WARNING - buy the airframe used, buy the batteries NEW.")
print("    Second-hand lithium packs are the one component where the saving is not worth")
print("    it. You cannot see cycle count or storage abuse from a photograph, a tired pack")
print("    sags under load and triggers a low-voltage landing over the wrong field, and a")
print("    swollen cell is a fire in the back of the car. DJI packs are good for roughly")
print("    200-400 cycles; a 10-day search at 10 sorties a day is ~25 cycles per pack, so")
print("    new packs will outlast several campaigns. The airframe has no such wear item.")
print()
hr()
