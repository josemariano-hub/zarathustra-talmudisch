#!/usr/bin/env python3
"""
Datalink trade for the night sweeper: Starlink? Iridium? What did the
anti-poachers fly, and what does Ukraine teach a civilian search program?

Scope note: the Ukraine section draws only widely published, civilian-applicable
engineering lessons - link-independence, GNSS fallbacks, attrition tolerance,
logistics. Nothing operational or weapons-related is needed to answer this.

SI units; prices indicative street (EUR, Aug 2026).
"""
import math

def hr(c="="): print(c * 104)

G0 = 9.80665

# ---- night-sweeper baseline (identical formulas to night_sweeper.py)
AUW0, LD, V_CR, ETA, P_AVION = 2.0, 12.0, 13.0, 0.55, 8.0
E_WH, USABLE = 150.0, 0.85
VT0_ANCHOR, P0_ANCHOR, SPL0, R0 = 133.0, 200.0, 65.0, 15.0
AMBIENT_NIGHT, CEILING = 32.0, 120.0

def cruise_power(auw_kg, extra_w=0.0):
    return auw_kg * G0 * V_CR / (LD * ETA) + P_AVION + extra_w

def endurance_h(p_w):
    return E_WH * USABLE / p_w

def spl_ground(v_tip, p_elec):
    spl = SPL0 + 55 * math.log10(v_tip / VT0_ANCHOR) + 10 * math.log10(p_elec / P0_ANCHOR)
    return spl - 20 * math.log10(CEILING / R0)

def tip(d, rpm): return math.pi * d * rpm / 60.0

print()
hr()
print("  DATALINK TRADE - what flies on the aircraft, what stays on the ground")
hr()

# ================================================================ 1. options
print("""
[1] THE CANDIDATE LINKS

    An A3 homebuilt flies VLOS - at most ~2 km from the pilot, usually much
    less. That legal fact does most of the deciding before any link budget:
    a link only earns its mass if it serves a mission the aircraft may fly.
""")
LINKS = [
    # name                        mass_g  power_W  cost_E  service      rate         latency    role it serves
    ("ELRS 868 + MAVLink telem",     25,    1.0,    110,  "free",      "~100 kbps", "ms",      "C2 + telemetry over the whole VLOS envelope"),
    ("4G LTE modem + SIM",           50,    2.5,     70,  "10 E/mo",   "10+ Mbps",  "~100 ms", "live thumbnails / candidate coords to the van"),
    ("Iridium SBD (RockBLOCK)",      30,    0.5,    260,  "~15 E/mo",  "340 B/msg", "minutes", "lost-aircraft beacon; works with zero infrastructure"),
    ("Starlink Mini",              1100,   30.0,    300,  "40+ E/mo",  "100+ Mbps", "~30 ms",  "broadband - but see what it does to the aircraft"),
]
print(f"    {'link':<28}{'mass':>7}{'power':>8}{'kit':>7}{'service':>9}{'rate':>11}{'latency':>9}  serves")
for n, m, p, c, s, r, lat, role in LINKS:
    print(f"    {n:<28}{m:>6}g{p:>7.1f}W{c:>6}E{s:>9}{r:>11}{lat:>9}  {role}")

# ================================================================ 2. starlink penalty
print("\n[2] STARLINK MINI ON THE GLIDER - computed, not assumed\n")
p_base = cruise_power(AUW0)
t_base = endurance_h(p_base)
auw_sl = AUW0 + 1.1
p_sl   = cruise_power(auw_sl, extra_w=30.0)
t_sl   = endurance_h(p_sl)
# heavier -> faster stall -> higher cruise; keep V for simplicity (favourable to Starlink)
spl_base = spl_ground(tip(0.356, 2800), p_base)
# more power at same prop -> higher rpm; assume rpm scales with sqrt(P/P0) as a first cut
rpm_sl = 2800 * math.sqrt(p_sl / p_base)
spl_sl = spl_ground(tip(0.356, rpm_sl), p_sl)
print(f"    {'':<26}{'baseline':>12}{'with Starlink Mini':>20}")
print(f"    {'AUW':<26}{AUW0:>10.1f} kg{auw_sl:>18.1f} kg   (+55%)")
print(f"    {'cruise power':<26}{p_base:>10.0f} W{p_sl:>18.0f} W   (+{(p_sl/p_base-1)*100:.0f}%)")
print(f"    {'endurance':<26}{t_base*60:>10.0f} min{t_sl*60:>16.0f} min   ({t_sl/t_base-1:+.0%})")
print(f"    {'noise at ground':<26}{spl_base:>10.0f} dBA{spl_sl:>16.0f} dBA   (ambient {AMBIENT_NIGHT:.0f})")
assert t_sl < 0.55 * t_base
print(f"""
    -> The terminal weighs more than half the aircraft. Endurance collapses from
       {t_base*60:.0f} to {t_sl*60:.0f} minutes, the wing loading and stall speed jump, and the
       acoustic margin thins. And the bandwidth buys nothing the mission needs:
       the matched filter runs POST-FLIGHT on logged frames - there is no
       real-time consumer of 100 Mbps on this aircraft. Disqualified on physics,
       not fashion. Starlink's home is the GROUND VEHICLE: Z2I already owns the
       kit, and the van needs the fat pipe (candidate review, PNOA tiles,
       weather, coordinating two teams) far more than the wing does.
""")

# ================================================================ 3. iridium
print("[3] IRIDIUM - wrong as telemetry, right as insurance\n")
print("""    As a telemetry link Iridium SBD is a non-starter: 340-byte messages with
    minutes of latency cannot carry imagery and cannot do C2. But reframe it:

    - On the DRONE, as a lost-aircraft beacon: 30 g and ~260 EUR one-off. A night
      aircraft that goes down 1.5 km away in dark scrub is itself a recovery
      problem - position-on-descent over Iridium turns that from a morning of
      searching into a walk. The aircraft hunting a lost payload should not
      become a lost payload. VERDICT: carry it. It is 1.5% of AUW.

    - On the NEXT BALLOON FLIGHT: this same 30 g module transmitting one fix per
      minute through descent would have made this entire project unnecessary.
      That is the cheapest sentence in this repository.

    (A 4G module is the same insurance for a fifth of the service cost wherever
    there is coverage - rural Meseta coverage is good but not guaranteed in
    barrancos; Iridium works everywhere, which is the point of insurance.)
""")

# ================================================================ 4. precedent
print("[4] WHAT THE ANTI-POACHERS ACTUALLY FLEW\n")
print("""    Air Shepherd's architecture (6,000+ night hours): a thin RF C2/video link
    from the aircraft to a CONTROL VEHICLE - a van that is the ops centre, with
    the pilots, the screens, the batteries and the uplink in it. The aircraft
    carried the minimum radio that closed the loop; everything heavy stayed on
    wheels. Delta/Kruger operations ran the same shape with radio masts.

    That is the pattern to copy, and it maps directly onto our kit:

        AIRCRAFT : ELRS 868 C2 + telemetry (in the BOM already)
                   Iridium beacon (new, 30 g)
                   everything else logged onboard to the Pi
        VAN      : Starlink Mini (Z2I existing kit) - candidate review,
                   satellite tasking follow-ups, PNOA tiles, team coordination
                   2 kWh power station (in the kit list already)

    The van is the node. The wing is a sensor that comes home.
""")

# ================================================================ 5. ukraine
print("[5] LESSONS FROM UKRAINE - the civilian-applicable ones\n")
print("""    The published engineering lessons of the drone war, filtered to what a
    civilian search program can legitimately use:

    1. LINKS FAIL; AUTONOMY COMPLETES THE MISSION. The defining airframe lesson:
       any architecture that needs a continuous link is fragile. Ours passes
       already - the survey flies a pre-planned ArduPilot mission and the
       matched filter runs post-flight on logged frames. Telemetry is a
       convenience, not a dependency. Keep it that way: no design decision
       should ever make the downlink load-bearing.

    2. GNSS IS NOT GUARANTEED. Jamming taught everyone that position is a
       service, not a fact. Irrelevant over the Meseta on a good day - and
       free to hedge: ArduPilot's airspeed+compass+baro dead reckoning gets
       the aircraft home from 2 km with GPS dark. Enable it, test it once.

    3. CHEAP-AND-MANY BEATS EXQUISITE-AND-ONE. The war normalised treating
       airframes as consumables. Our 2,865 EUR wing embodies that philosophy,
       and a spare foam airframe + motor is ~275 EUR - carry one built. The
       fleet that keeps flying after a crash out-searches the fleet that
       grounds itself to grieve.

    4. LOGISTICS SET THE SORTIE RATE. Ukraine's drone units live and die by
       batteries and chargers, not airframes. We quantified the same law in
       battery_logistics.py: packs, channels and field watts govern coverage.
       The van's power budget is mission-critical infrastructure.

    5. OUR SUPPLY CHAIN IS THE WAR'S SUPPLY CHAIN. ELRS links, Pixhawk clones,
       Li-ion packs, FPV motors at these prices exist because that ecosystem
       scaled to wartime volumes. The BOM's cheapness is not an accident of
       hobbyism - order spares while the ecosystem is glutted.
""")

# ================================================================ 6. bom delta
print("[6] WHAT CHANGES IN THE BUILD\n")
DELTA = [
    ("Iridium SBD module (RockBLOCK 9603) + antenna",  260),
    ("4G LTE USB modem + prepaid SIM (thumbnail path)",  70),
    ("Spare foam airframe + motor, built and trimmed",  275),
]
tot_delta = sum(v for _, v in DELTA)
for k, v in DELTA:
    print(f"      {k:<52}{v:>7,}E")
print(f"      {'TOTAL DELTA':<52}{tot_delta:>7,}E")
print(f"      Night sweeper: 2,865 -> {2865+tot_delta:,} EUR. Starlink stays in the van (0 EUR: existing kit).")
print()
hr()
print("  VERDICT: neither Starlink nor Iridium AS TELEMETRY. ELRS closes the legal")
print("  envelope; the fat pipe goes in the van where Z2I already owns it; Iridium")
print("  flies as a 30 g beacon so the search asset can always be found; and the")
print("  architecture stays autonomous so no link is ever load-bearing.")
hr()
