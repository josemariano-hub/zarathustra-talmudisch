#!/usr/bin/env python3
"""
Fact about the lost payload, twice corrected: a 0.70 m carbon-fibre boom
(first reported "1.5 m or so") connects an Insta360 camera to the sphere.
CF is CONDUCTIVE - the payload has been carrying a linear radar scatterer
all along, just a smaller one than first thought: RCS goes as L^2, so the
length correction costs -6.6 dB. Detectability, per channel, re-derived.

SI units.
"""
import math
def hr(c="="): print(c*104)

L, R_TUBE = 0.70, 0.004       # m: boom length (CORRECTED from 1.5), tube radius (8 mm OD)
V         = 13.0              # sweeper survey speed
GSD_DAY, GSD_SAT, GSD_TH = 0.029, 0.30, 0.158
SIGMA0    = 10**(-12/10)      # stubble clutter, same model as diy_radar.py
TH_AZ, DR = math.radians(20.0), 0.75
G_INT_DB  = 8.0               # credited integration gain over partially-decorrelating clutter

def cyl_rcs(lam):  return 2*math.pi*L*L*R_TUBE/lam     # broadside, conducting cylinder
def lobe_deg(lam): return math.degrees(lam/(2*L))      # glint half-width scale
def clut_rcs(R):   return R*TH_AZ*DR*SIGMA0            # clutter equivalent RCS in one cell
def margin_db(R):
    scr = cyl_rcs(0.0124)/clut_rcs(R)
    return 10*math.log10(scr), 10*math.log10(scr)+G_INT_DB
def dwell_ms(R):   return lobe_deg(0.0124)/math.degrees(V/R)*1000

print(); hr()
print("  THE CARBON BOOM, CORRECTED - a 0.70 m linear scatterer attached to the sphere")
hr()

print(f"""
[1] RADAR: STILL BRIGHT, NO LONGER COMFORTABLE

    Broadside RCS of a conducting cylinder, sigma = 2*pi*L^2*r/lambda,
    and the L^2 law is why a factor-2.1 length correction costs 6.6 dB:

    {'band':<26}{'lambda':>9}{'RCS broadside':>15}{'glint width':>13}""")
BANDS=[("Our 24 GHz FMCW bay",0.0124),("X-band SAR (ICEYE/PAZ)",0.031),("C-band (Sentinel-1)",0.055)]
for name,lam in BANDS:
    print(f"    {name:<26}{lam*1000:>7.1f}mm{cyl_rcs(lam):>13.2f} m2{lobe_deg(lam):>11.2f} deg")
r24=cyl_rcs(0.0124)
assert abs(cyl_rcs(0.031)/cyl_rcs(0.0124) - 0.0124/0.031) < 1e-9   # scales as 1/lambda
assert abs(r24 - 2*math.pi*0.49*0.004/0.0124) < 1e-6
print(f"""
    {r24:.1f} m2 at 24 GHz (was 4.6 at the reported 1.5 m). The regime checks
    survive the correction unchanged, since they depend on radius and wall,
    not length: (a) circumference/lambda = 2.0 - optical formula at its
    validity edge, good to a couple of dB; at X-band (0.8) it enters the
    resonant thin-wire regime, weaker and polarization-dependent. (b) CF
    conductivity (~5e4 S/m) still gives loss under ~1 dB along the fibres.
    (c) The 1 mm hollow wall is ~69 skin depths - electrically a solid rod.
    What DID change: the glint lobe doubles to {lobe_deg(0.0124):.2f} deg (a shorter
    aperture beams less tightly), which buys back some dwell.

[2] DOES THE SWEEPER CROSS THE GLINT? - yes, but the margin is now thin

    Flying a straight line past a horizontal boom, the azimuth aspect still
    crosses perpendicularity once per side, whatever the boom's heading.
    Same clutter model as diy_radar.py (sigma0 = -12 dB, 20 deg x 0.75 m cell):

    {'offset':>10}{'clutter RCS':>13}{'SCR 1-look':>12}{'dwell':>9}{'chirps':>8}{'SCR + integ.':>13}""")
for R in (150.0, 120.0, 100.0, 80.0):
    s1,si = margin_db(R)
    print(f"    {R:>8.0f} m{clut_rcs(R):>11.2f} m2{s1:>10.1f} dB{dwell_ms(R):>7.0f} ms{dwell_ms(R):>7.0f}{si:>11.1f} dB")
s1_100, si_100 = margin_db(100.0)
print(f"""
    VERDICT CHANGE. At the old 150 m offset the integrated margin is now
    ~{margin_db(150)[1]:.0f} dB - below any comfortable CFAR threshold. Pulling the
    operating offset in to ~100 m recovers ~{si_100:.0f} dB: DETECTABLE BUT
    MARGINAL, where the 1.5 m boom was comfortable at 150 m. Consequences:
      - The boom channel is downgraded from "reliable once-per-pass flash"
        to "marginal, ground-test-gated". Z2I-TP-001 (the rod drive-by
        test) is now the decisive gate, not a formality: the worst-case
        polarization measurement decides whether this channel exists.
      - Radar survey lines for the boom run at ~100 m offset (both sides:
        ~170 m usable swath), not 300-400 m. Coverage rate roughly halves.
      - The three caveats stand: near-horizontal attitude required, ground
        contact damps the return, and the CFAR stage must be a TRANSIENT
        single-sweep detector - persistence filtering would erase the flash.

    DOCTRINE, RE-UPDATED: the radar bay remains the hidden-canopy
    escalation option, but its case now rests on the ground test passing
    at 100 m in the worse polarization. Do not integrate the bay before
    TP-001 produces that number.

[3] SATELLITE SAR: EVEN MORE OF A LOTTERY TICKET

    X-band nominal {cyl_rcs(0.031):.2f} m2 (thin-wire regime cuts it further,
    polarization-dependent) with a {lobe_deg(0.031):.2f} deg lobe. The wider lobe
    roughly doubles the alignment odds, but the RCS drop more than eats the
    gain: P(glint) ~ 2-4% per scene AND the flash now sits barely above a
    1 m2-cell clutter floor. Do not task SAR for the boom - unchanged, with
    more force. A free look at an existing X-band scene still costs nothing.

[4] DRONE RGB: A SHORTER STREAK, SAME ROLE

    At {GSD_DAY*100:.1f} cm GSD the 8 mm boom is {L/GSD_DAY:.0f} px long but only {2*R_TUBE/GSD_DAY:.2f} px WIDE -
    sub-pixel width dilutes the dark-line contrast to ~0.07 reflectance
    per pixel. A {L/GSD_DAY:.0f}-px correlated streak still rewards an oriented line
    filter (Hough / steerable): sqrt({L/GSD_DAY:.0f}) ~ {math.sqrt(L/GSD_DAY):.0f}x SNR gain along the line
    (was 7x at 1.5 m). Plus the Insta360 blob ({0.07/GSD_DAY:.1f} px) at its far end.
    Keep the compound sphere+line+blob template - the line was already a
    supporting cue, and it supports a little less now. The 50 m inspection
    pass sees it at 0.66 px wide x {L/(GSD_DAY*50/120):.0f} px long: still unmistakable.
    (At satellite 30 cm: {L/GSD_SAT:.1f} px long x {2*R_TUBE/GSD_SAT:.2f} px wide - forget it.
     Thermal at {GSD_TH*100:.0f} cm: invisible.)

[5] THE INSTA360 ITSELF - unchanged

    ~7 cm of camera: sub-pixel to satellites, {0.07/GSD_DAY:.1f} px to the drone, radios
    weeks dead - no detection channel, but the recovery PRIZE: its card
    holds the descent video.

  SUMMARY, CORRECTED: the boom still adds two channels, both demoted one
  grade - a shorter compound-shape cue to the day camera (still useful),
  and a marginal specular flash to our own radar at ~100 m offset that
  only counts if the ground test confirms it. The orange canopy remains
  the primary target by a wide margin; satellite tasking is unaffected.
""")
hr()
