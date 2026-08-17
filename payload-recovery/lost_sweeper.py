#!/usr/bin/env python3
"""
The sweeper is down and its Iridium beacon is dead. Can radar find it?

Three physical questions:
  1. Can the DEAD MODEM's electronics be detected from the air?
     (nonlinear junction detection - the real technology, with brutal range physics)
  2. Is the sweeper AIRFRAME a usable radar target on its own?
  3. What ~19 g of preparation makes the question moot?

SI units.
"""
import math
def hr(c="="): print(c*104)

C=299792458.0; K_B=1.380649e-23
LAM=0.0124

print(); hr()
print("  FINDING THE FINDER - a downed sweeper with a dead Iridium beacon")
hr()

# ---------------------------------------------------------------- 1. NLJD
print("""
[1] DETECTING THE DEAD ELECTRONICS THEMSELVES - honest physics

    The technology exists: nonlinear junction detection (NLJD). Illuminate a
    semiconductor junction and it re-radiates harmonics (2f, 3f) - how bug
    sweepers and RECCO both work. But an UNTUNED junction (a dead modem's
    PCB) has a monstrous conversion loss, and the harmonic radar equation
    scales as R^8, not R^4 - both legs of the trip are one-way.

    Anchor on reality: a commercial 3 W NLJD detects a phone at ~3 m.
    Scaling to airborne standoff:
""")
R0, P0 = 3.0, 3.0
for R in (10.0, 30.0, 100.0):
    factor = (R/R0)**8
    print(f"      {R:>5.0f} m standoff -> needs {10*math.log10(factor):.0f} dB more link budget "
          f"({factor:.1e}x the power-aperture)")
print("""    -> At 30 m you need +80 dB; at 100 m, +122 dB. No airborne platform
       closes that on an untuned target. VERDICT: NO - a dead modem cannot
       be radar-detected from the aircraft. NLJD is a 1-3 m technology; it
       could help ON FOOT, sweeping the last 100 m2 - a rented TSCM wand
       or RECCO detector on the ground, not from a plane.

    The exception that proves the rule: RECCO. Its diode sits between TWO
    TUNED antennas (917 MHz in, 1.83 GHz out), recovering ~40-60 dB of the
    conversion loss - which is exactly why a helicopter detector reaches
    ~100-200 m. Tuning is everything; dead modems are not tuned.
""")

# ---------------------------------------------------------------- 2. airframe RCS
print("[2] IS THE BARE AIRFRAME A RADAR TARGET? - marginal at best\n")
# foam is transparent; returns come from motor, battery, wiring, servos
RCS_AIRFRAME=0.05
EIRP_W, G_ANT, NF, T_CHIRP, SNR = 0.100, 10**1.3, 10**1.0, 1e-3, 10**1.3
N=K_B*290*(1/T_CHIRP)*NF
Rmax=(EIRP_W*G_ANT*LAM**2*RCS_AIRFRAME/((4*math.pi)**3*N*SNR))**0.25
DR=C/(2*200e6)
cell=150.0*math.radians(20)*DR
clut=10**(-1.2)*cell
print(f"    Foam is radar-transparent; the echo is motor+battery+harness ~{RCS_AIRFRAME} m2.")
print(f"    Noise-limited range: {Rmax:.0f} m - but clutter in a 150 m cell is {clut:.1f} m2,")
print(f"    i.e. the airframe sits {10*math.log10(RCS_AIRFRAME/clut):.0f} dB UNDER the stubble. Undetectable")
print(f"    in clutter, marginal even on plowed bare soil. Not a search plan.")

# ---------------------------------------------------------------- 3. the fix
print("""
[3] THE 14-GRAM FIX - make the sweeper carry its own answer

    a) EMBEDDED CORNER, 10 cm, foil-on-Depron, built into the fuselage bay
       wall (~15 g, ~0 EUR from build-sheet offcuts): 2.7 m2 at 24 GHz.
       Checked against clutter honestly: at 100 m the single-look SCR is
       only ~2 dB - the corner needs the ~10 dB of coherent chirp
       integration to stand out, giving reliable detection at ~100 m and
       degrading fast beyond. Fly the SPARE airframe (radar bay swaps over)
       in tight 150 m lines over the LTE last-fix strip. The attrition
       doctrine pays again: the fleet searches for its own casualty.
       (An 8 cm corner sits BELOW clutter at range - too small; 10 cm is
       the floor for an embedded tag.)

    b) RECCO TAB glued in the fuselage (~4 g, 5 EUR): a tuned harmonic
       target detectable by any RECCO detector - mountain rescue flies
       them on helicopters across Europe, and handheld units cover the
       last-100-m ground search.

    c) Plus the forensics that cost nothing: the LTE modem's last WireGuard
       keepalive gives a last-known position to ~one survey line; ELRS
       link-loss telemetry brackets it further. Radar then only has to
       clear a strip, not a map.

    VERDICT: you cannot radar-detect the dead modem - but ~19 g of passive
    preparation makes the dead modem irrelevant. Add the embedded corner
    and the RECCO tab to the build NOW, while the fuselage is still open.
    Every asset that flies should carry the same three-layer humility:
    a link, a tag, and a shape that answers radar.
""")
hr()
