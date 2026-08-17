#!/usr/bin/env python3
"""
Li-ion packs vs Energizer Ultimate Lithium AA (L91, Li/FeS2) for the night sweeper.

A natural question from a balloon operator - L91s are the standard HAB payload
battery (cold to -40 C, superb shelf life, ~300 Wh/kg at LOW drain). The physics
question is whether they survive contact with a propulsion load.

SI units; prices indicative street (EUR, Aug 2026).
"""
import math
def hr(c="="): print(c * 104)

G0 = 9.80665
# night-sweeper loads (from night_sweeper.py / sensor_upgrade.py)
P_CRUISE, P_CLIMB, P_AVION = 48.0, 220.0, 8.0
AUW_BASE, LD, V_CR, ETA = 2.09, 12.0, 13.0, 0.55
LIION_PACK_WH, LIION_PACK_G, LIION_PACK_EUR = 150.0, 600.0, 110.0

# ---------------------------------------------------------------- L91 model
# Energizer L91 datasheet-shaped behaviour: 15 g, ~1.5 V nominal falling to
# ~1.2 V under heavy load; capacity vs continuous drain (approximate curve):
L91_G, L91_EUR = 15.0, 2.5
L91_CAP = [(0.25, 3.0), (0.5, 2.9), (1.0, 2.6), (1.5, 2.3), (2.0, 2.0)]
L91_IMAX = 2.0        # A continuous per cell, datasheet ceiling
def l91_capacity(i_cell):
    for (i1, c1), (i2, c2) in zip(L91_CAP, L91_CAP[1:]):
        if i_cell <= i2:
            return c1 + (c2 - c1) * (i_cell - i1) / (i2 - i1)
    return 2.0
V_LOADED = 1.25       # V per cell under propulsion-class load

print(); hr()
print("  BATTERY CHEMISTRY - your Li-ion packs vs AA Ultimate Lithium (L91) primaries")
hr()

# ---------------------------------------------------------------- inventory
print("""
[1] THE INVENTORY QUESTION - answered honestly

    Searched the Gmail account: no battery purchase records - Saft newsletters
    and HobbyKing marketing (addressed to Robert Falco and Jose Luis Bravo, who
    are therefore the people to ask). Google Drive search was attempted twice
    but requires an interactive tool approval this remote session cannot
    collect - run it from claude.ai and the query takes seconds.

    Design compatibility while the shelf is inventoried: the airframe absorbs
    ANY 3S-6S Li-ion or LiPo pack of 450-700 g without redesign - the ESC takes
    the voltage range, the motor/prop pairing tolerates it, and only the trim
    ballast moves. Whatever is found flies; nothing found blocks the build.
""")

# ---------------------------------------------------------------- propulsion pack
print("[2] CAN L91 PRIMARIES FLY THE AIRCRAFT? - solve the pack, then judge\n")
# series count for ~12 V bus under load; parallel count set by the CLIMB burst
S = math.ceil(12.0 / V_LOADED)
i_climb_bus = P_CLIMB / (S * V_LOADED)
P_par = math.ceil(i_climb_bus / L91_IMAX)
n_cells = S * P_par
i_cell_cruise = (P_CRUISE / (S * V_LOADED)) / P_par
cap = l91_capacity(max(i_cell_cruise, 0.25))
e_l91 = S * V_LOADED * cap * P_par
m_l91 = n_cells * L91_G
c_l91 = n_cells * L91_EUR
assert i_climb_bus / P_par <= L91_IMAX + 1e-9

print(f"    Bus: {S}S x {V_LOADED} V = {S*V_LOADED:.1f} V under load")
print(f"    Climb burst {P_CLIMB:.0f} W -> {i_climb_bus:.1f} A bus -> {P_par}P to respect {L91_IMAX:.0f} A/cell")
print(f"    Pack: {S}S{P_par}P = {n_cells} cells, {m_l91:.0f} g, {e_l91:.0f} Wh usable, {c_l91:.0f} EUR")
print(f"    Cruise per-cell drain {i_cell_cruise:.2f} A -> capacity {cap:.1f} Ah/cell (the low-drain magic is intact)")

# endurance with the heavier pack (same formulas as night_sweeper.py)
auw_l91 = AUW_BASE - LIION_PACK_G / 1000 + m_l91 / 1000
p_l91 = auw_l91 * G0 * V_CR / (LD * ETA) + P_AVION
t_l91 = e_l91 * 0.95 / p_l91          # primaries: no reserve-for-cycle-life, 5% margin
t_liion = LIION_PACK_WH * 0.85 / P_CRUISE
print(f"""
    {'':<24}{'Li-ion 4S2P (yours)':>21}{'L91 {0}S{1}P'.format(S,P_par):>14}
    {'pack mass':<24}{LIION_PACK_G:>19.0f} g{m_l91:>12.0f} g
    {'usable energy':<24}{LIION_PACK_WH*0.85:>18.0f} Wh{e_l91*0.95:>11.0f} Wh
    {'AUW':<24}{AUW_BASE:>18.2f} kg{auw_l91:>11.2f} kg
    {'endurance':<24}{t_liion*60:>17.0f} min{t_l91*60:>10.0f} min
    {'cost of THIS flight':<24}{'~0.5 EUR amortised':>21}{f'{c_l91:.0f} EUR consumed':>17}
""")

print("[3] CAMPAIGN COST - the number that ends the argument\n")
print(f"    {'sorties':>9}{'Li-ion (3 packs+charger)':>26}{'L91 primaries':>16}")
for n in (5, 10, 20, 40):
    li = 420.0
    l9 = n * c_l91
    print(f"    {n:>9}{li:>24,.0f}E{l9:>15,.0f}E")
print(f"""
    Primaries cost {c_l91:.0f} EUR per sortie, forever. The rechargeable kit is bought
    once. By sortie two the primaries have burned the entire Li-ion budget.

    Full honesty: the 90-cell primary pack WOULD fly longer per sortie (299 min
    vs 159 - it carries 2.4x the usable energy). But it burns 225 EUR doing it,
    every time, and 90 spring-contact cells in a vibrating airframe is a
    reliability lottery no serious operator plays.

    And the physics is no kinder than the economics: the {P_par}P needed to survive
    the climb burst drags {m_l91-LIION_PACK_G:.0f} g of extra pack up every flight for
    {e_l91*0.95 - LIION_PACK_WH*0.85:+.0f} Wh of usable energy. High-drain loads are exactly where
    Li/FeS2 stops being magic. VERDICT: not for propulsion. Ever.
""")

print("[4] WHERE THE L91 GENUINELY BELONGS\n")
# an Iridium beacon duty-cycles: one SBD burst every 10 min -> ~30 mW average
P_BEACON_AVG = 0.030
for cells, label in [(2, "2xAA on the drone's Iridium backup bus"),
                     (4, "4xAA on the next balloon payload tracker")]:
    e = cells * 1.5 * 3.0          # low-drain: full 3.0 Ah
    days = e / P_BEACON_AVG / 24
    print(f"    {label:<44}{e:>5.0f} Wh -> {days:>4.0f} days of duty-cycled beacon")
print(f"""
    Cold to -40 C, a decade of shelf life, no charging logistics, no fire risk,
    ~{2*1.5*3.0/0.030:.0f} Wh/kg at beacon drain - this is why L91s are the standard HAB
    battery, and both beacons here should fly them:
    - the drone's Iridium beacon gets an INDEPENDENT 2xAA bus, so the crash
      that kills the main pack cannot kill the thing that reports the crash;
    - the next balloon flight's tracker flies 4xAA, as every HAB tracker should.

    The chemistry rule in one line: rechargeables spin the propeller,
    primaries keep the promise.
""")
hr()
