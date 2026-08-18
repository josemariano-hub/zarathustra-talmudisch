#!/usr/bin/env python3
"""
Field ops from the Amarok pickup: what the truck changes, computed.

The 'van is the node' architecture lands on a VW Amarok: open bed, 12 V
alternator, and 4Motion that treats Meseta caminos as roads. Three effects
worth numbers, one worth a warning.
"""
import math
def hr(c="="): print(c*104)

print(); hr()
print("  LAUNCHING FROM THE AMAROK - the truck is part of the aircraft system")
hr()

# ---------------------------------------------------------------- 1. bed launch
print("""
[1] LAUNCH FROM THE BED - height and sight, modest but free

    Launcher standing in the bed releases at ~3.4 m instead of ~1.9 m.
    The extra 1.5 m of height buys ~1 s of grace before any stall-mush
    meets the ground - the difference between a fumbled throw costing a
    re-launch and costing a wingtip. Observer eye height ~3.2 m also
    lifts the VLOS horizon over standing cereal and gentle rises: the
    0.5 km bubble becomes reliably usable instead of hedge-limited.
""")

# ---------------------------------------------------------------- 2. rolling launch
V_STALL=8.3; V_TRUCK_KMH=15.0
v_truck=V_TRUCK_KMH/3.6
print(f"""[2] ROLLING LAUNCH - the option that moves the Pareto ceiling

    Drive into wind along a camino at {V_TRUCK_KMH:.0f} km/h and release from the bed:
    the aircraft starts with {v_truck:.1f} m/s of free airspeed against a stall of
    {V_STALL:.1f} m/s (at 3.0 kg MTOM). The thrower now only adds ~{V_STALL-v_truck:.1f} m/s -
    a push, not a javelin throw. Consequences:
      - Hand-launch at MTOM becomes routine instead of athletic.
      - The size_pareto hand-launch ceiling (3.5 kg) stretches toward
        ~4.5-5 kg IF a bigger aircraft is ever wanted - the bungee-cadence
        penalty that closed the >3.5 kg branch softens when the truck IS
        the bungee. (The 3 kg verdict stands; this is future margin.)
    Private farm tracks only, walking-pace release, thrower harnessed or
    seated on the bed rail - a dropped aircraft at 15 km/h still bounces.
""")

# ---------------------------------------------------------------- 3. alternator
P_DCDC=300.0          # W into the power station from a 25 A 12V DC-DC charger
relocs=35; drive_min=6.0
e_free=relocs*drive_min/60*P_DCDC
p_fleet_avg=60.0; airborne_h=9.0
e_need=p_fleet_avg*airborne_h
print(f"""[3] THE ALTERNATOR IS THE GENERATOR - the field power problem dissolves

    A 25 A DC-DC charger feeds the 2 kWh station ~{P_DCDC:.0f} W whenever the
    engine runs. The VLOS day IS driving: ~{relocs} relocations x ~{drive_min:.0f} min =
    {relocs*drive_min/60:.1f} h of engine time -> ~{e_free:.0f} Wh harvested per day, against a
    fleet consumption of ~{e_need:.0f} Wh ({p_fleet_avg:.0f} W x {airborne_h:.0f} h airborne).

    -> After the ~85% charge-chain efficiency that is ~{e_free*0.85:.0f} Wh delivered -
       still {e_free*0.85/e_need*100:.0f}% of daily flight energy, free, during drives you make anyway.
       and the 2 kWh station becomes a buffer, not a reservoir. No petrol
       generator, ever - which also protects the night acoustic budget.

[4] THE WARNING: DUST

    Meseta caminos in August are talc. The charging crate's fan now needs
    a filter (print a G3-foam holder for the duct), packs travel in the
    closed crate, and the camera bay gets a lens check per relocation.
    Dust is the Amarok's only tax on this architecture.

[5] BED RACK - three more X1C prints

    - Charging crate tie-down base + filtered fan duct       (PETG)
    - Aircraft chocks: wing cradles for transit on stubble   (TPU pads)
    - GCS/antenna mast foot for the bed rail (ELRS + LTE)    (PETG, no CF)

  SUMMARY: the truck was already in the plan as 'the van'; the Amarok makes
  it better than planned - higher launch, free rolling airspeed, and an
  alternator that cancels the generator. The ops doctrine gains one line:
  ENGINE ON while relocating is not idling, it is refuelling the fleet.
""")
hr()
