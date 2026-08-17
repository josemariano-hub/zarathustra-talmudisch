#!/usr/bin/env python3
"""
Our own radar, for the next flight: the payload carries the X1C-printed
octahedral corner-reflector cluster, and the sweeper carries a small FMCW
radar bay. What does it cost, and what does it actually deliver?

Design philosophy: DIY radar sanity means buying a COTS 24 GHz FMCW
front-end module and owning the signal processing - not building microwave
hardware from scratch. 24.000-24.250 GHz is the ISM band (ETSI-compliant
modules ship at the 100 mW EIRP limit), so this flies without a licence.

SI units. Prices indicative street (EUR, Aug 2026).
"""
import math
def hr(c="="): print(c*104)

C = 299792458.0
K_B = 1.380649e-23

# ---------------------------------------------------------------- band & module
F0     = 24.125e9            # Hz, ISM band centre
LAM    = C / F0
B      = 200e6               # Hz, sweep inside the ISM allocation
EIRP_W = 0.100               # W, ISM limit (20 dBm) - modules ship at this
G_ANT  = 10**(13/10)         # 13 dBi patch array (K-MD2 / IWR1443 class)
NF     = 10**(10/10)
T_CHIRP= 1e-3                # s -> ~1 kHz noise bandwidth per range bin
SNR_DET= 10**(13/10)         # 13 dB detection threshold
DR     = C / (2*B)

# ---------------------------------------------------------------- the target
# X1C-printed trihedral cluster, aluminium-faced, leg a per corner
print(); hr()
print("  DIY RADAR FOR THE NEXT FLIGHT - the corner reflector closes the loop")
hr()
print(f"\n[1] THE TARGET, AT OUR OWN FREQUENCY\n")
print(f"    At 24 GHz (lambda {LAM*1000:.1f} mm) the printed trihedral is enormous:")
print(f"    {'leg a':>8}{'RCS at 24 GHz':>15}{'vs the sphere alone':>22}")
for a in (0.08, 0.10, 0.15, 0.20):
    rcs = 4*math.pi*a**4/(3*LAM**2)
    print(f"    {a*100:>6.0f}cm{rcs:>13.1f} m2{'(porexpan itself: ~0.001 m2 - invisible)' if a==0.08 else '':>40}")
A_LEG = 0.15
RCS = 4*math.pi*A_LEG**4/(3*LAM**2)
print(f"""
    Design point: 15 cm legs -> {RCS:.1f} m2 - a truck-sized radar target.

    MASS, corrected (the first estimate reused SAR-panel areal density and
    double-counted geometry): the octahedral cluster is THREE interlocking
    2a x 2a plates sharing every face among 8 corners - 0.27 m2 total, not
    0.54. At 24 GHz the skin depth in aluminium is 0.53 um, so 12 um kitchen
    foil is 23 skin depths - a perfect reflector at 32 g/m2 - and the
    lambda/16 flatness spec (0.78 mm) is trivial for foil on 3 mm Depron.

      12 um foil + 3 mm Depron + printed slot-joint frame:   ~63 g
      foil drum-skinned on printed edge frame only:          ~43 g
      (metallized mylar/ripstop REJECTED: ~100 nm Al is under
       one skin depth - looks shiny, reflects poorly at 24 GHz)

    Build the foil-on-Depron version: 63 g, robust, flatness guaranteed by
    the substrate. 2% of the payload. The cluster keeps one corner facing
    any direction, so resting attitude does not matter. And if 150 m radar
    range suffices, a 10 cm cluster weighs 42 g.
""")

# ---------------------------------------------------------------- range
print("[2] DETECTION RANGE FROM THE SWEEPER\n")
N_THERM = K_B*290*(1/T_CHIRP)*NF
num = EIRP_W*G_ANT*LAM**2*RCS
R_max = (num/((4*math.pi)**3 * N_THERM*SNR_DET))**0.25
print(f"    Radar equation, noise-limited: R_max = {R_max:.0f} m  (13 dB SNR, single chirp)")
# clutter-limited check: side-looking from 120 m, ~45 deg grazing over stubble
theta_az = math.radians(20.0)
R_op = 200.0
cell = R_op*theta_az*DR
sigma0 = 10**(-12/10)
clut = sigma0*cell
scr = RCS/clut
print(f"    Clutter check at {R_op:.0f} m: cell {cell:.0f} m2 x sigma0(-12 dB) = {clut:.1f} m2 clutter")
print(f"    -> signal-to-clutter {10*math.log10(scr):.0f} dB; a stable point over speckle, and")
print(f"       coherent integration over ~100 chirps adds ~10 dB more margin.")
assert R_max > 200 and scr > 3

swath = 2*R_op*0.85          # sweep both sides, some overlap loss
rate = swath*13.0*0.78*3600/1e6
print(f"""
    Operating swath ~{swath:.0f} m (side-looking both sides at {R_op:.0f} m):
    {rate:.0f} km2/h from the same 13 m/s glider - vs 4.8 for day RGB and 2.8
    for thermal. And it is indifferent to cloud, fog, rain, darkness and the
    sphere being under a hedge. Range resolution {DR:.2f} m localises the hit
    to a strip a tractor can drive down.
""")

# ---------------------------------------------------------------- cost
print("[3] WHAT IT COSTS\n")
BOM = [
    ("24 GHz FMCW eval module (IWR1443BOOST / K-MD2 class)", 320),
    ("Raw-ADC capture board (DCA1000 class, used)",          220),
    ("Printed radome + side-look mount (X1C, PETG - no CF)",   5),
    ("Cabling, power from existing 5 A UBEC stock",            5),
]
tot = sum(v for _,v in BOM)
for k,v in BOM: print(f"      {k:<56}{v:>7,}E")
print(f"      {'TOTAL RADAR BAY':<56}{tot:>7,}E")
print(f"""
      Plus the true cost: ~40-60 h of FMCW signal-processing work (chirp
      config, range-FFT, CFAR detection, geotagging on the Pi). That is DSP
      on a laptop, not microwave engineering - the module IS the radar.
      A from-scratch or harmonic-radar build (SDR + PA + LNA + two bands)
      runs ~800-1,000 EUR and 3-5x the hours; not worth it when a 5 EUR
      RECCO tab and a rented detector already give the clutter-free channel.

[4] THE NEXT-FLIGHT RECOVERY KIT, COMPLETE

      X1C-printed octahedral reflector cluster (foil/Depron)   ~20 EUR, 63 g
      Iridium tracker on 4xAA L91 (the real fix)              ~300 EUR, 120 g
      RECCO reflector                                            ~5 EUR, 4 g
      Radar bay on the sweeper (above)                          {tot} EUR
      ------------------------------------------------------------------
      Three independent recovery channels for ~{tot+325} EUR total. The tracker
      tells you where it landed; the radar and RECCO find it if the tracker
      dies; the reflector needs no power at all and outlives everything.
      That is what "the next recovery becomes a non-event" costs.
""")
hr()
