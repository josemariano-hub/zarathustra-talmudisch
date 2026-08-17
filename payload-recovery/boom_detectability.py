#!/usr/bin/env python3
"""
New fact about the lost payload: a ~1.5 m carbon-fibre boom connects an
Insta360 camera to the sphere. CF is CONDUCTIVE - the payload has been
carrying a linear radar scatterer all along. Detectability, per channel.

SI units.
"""
import math
def hr(c="="): print(c*104)

L, R_TUBE = 1.5, 0.004        # m: boom length, tube radius (8 mm OD - confirmed thin)
V, R_OP   = 13.0, 200.0       # sweeper survey speed, radar offset
GSD_DAY, GSD_SAT, GSD_TH = 0.029, 0.30, 0.158

def cyl_rcs(lam):  return 2*math.pi*L*L*R_TUBE/lam     # broadside, conducting cylinder
def lobe_deg(lam): return math.degrees(lam/(2*L))      # first-null glint half-width scale

print(); hr()
print("  THE CARBON BOOM - a 1.5 m linear scatterer attached to the sphere")
hr()

print(f"""
[1] RADAR: BRIGHT BUT ASPECT-FUSSY

    Broadside RCS of a conducting cylinder, sigma = 2*pi*L^2*r/lambda:

    {'band':<26}{'lambda':>9}{'RCS broadside':>15}{'glint width':>13}""")
BANDS=[("Our 24 GHz FMCW bay",0.0124),("X-band SAR (ICEYE/PAZ)",0.031),("C-band (Sentinel-1)",0.055)]
for name,lam in BANDS:
    print(f"    {name:<26}{lam*1000:>7.1f}mm{cyl_rcs(lam):>13.1f} m2{lobe_deg(lam):>11.2f} deg")
r24=cyl_rcs(0.0124)
assert abs(cyl_rcs(0.031)/cyl_rcs(0.0124) - 0.0124/0.031) < 1e-9   # scales as 1/lambda
print(f"""
    {r24:.1f} m2 at 24 GHz - still a strong target, though the thin 8 mm tube
    trims it (RCS scales linearly with radius). Two regime checks the thin
    tube forces: (a) circumference/lambda = 2.0 at 24 GHz - the optical
    formula is at its validity edge, good to a couple of dB; at X-band
    (ratio 0.8) it enters the resonant thin-wire regime where returns are
    weaker and strongly polarization-dependent. (b) CF conductivity
    (~5e4 S/m) is far below copper but sigma/(omega*eps0) ~ 4e4 >> 1:
    still an excellent microwave reflector, loss under ~1 dB.
    The glint lobe stays 0.24 deg wide - crossing it is still the game.

[2] DOES THE SWEEPER CROSS THE GLINT? - yes, once per pass, by geometry

    Flying a straight line past a horizontal boom, the azimuth aspect sweeps
    continuously and crosses perpendicularity to the boom axis exactly once
    per side, whatever the boom's heading. At closest approach:

      azimuth rate  = V/R = {V}/{R_OP} = {math.degrees(V/R_OP):.1f} deg/s
      glint dwell   = {lobe_deg(0.0124):.2f} deg / {math.degrees(V/R_OP):.1f} deg/s = {lobe_deg(0.0124)/math.degrees(V/R_OP)*1000:.0f} ms
      chirps in the flash at 1 kHz = ~{lobe_deg(0.0124)/math.degrees(V/R_OP)*1000:.0f}

    A ~{r24:.1f} m2 target for ~65 chirps at constant range: a brief, localised
    flash. Against clutter at 150 m offset (cell ~2.5 m2) that is ~+3 dB
    single-look and ~+11 dB across the dwell - detectable, with the
    operating offset pulled in from 200 to ~150 m for the thin tube. Three honest caveats:
      - The boom must lie near-horizontal. Propped on the sphere or a furrow,
        the specular cone tilts and can miss the aircraft's altitude plane.
        A tilt of a few degrees is fine (the drone's depression angle varies
        across the swath); tens of degrees kills it.
      - Ground contact and partial burial dampen the return.
      - The flash appears ONCE per pass in ONE range bin. The CFAR stage
        must run a TRANSIENT detector (single-sweep exceedance, logged with
        position), not a persistence filter - persistence would erase it.

    DOCTRINE UPDATE: the 550 EUR radar bay is no longer next-flight-only.
    THIS payload already carries a radar signature worth flying for -
    orientation-dependent, so treat radar as an additional stochastic
    channel over the same survey lines, not a guaranteed sweep.

[3] SATELLITE SAR: A LOTTERY TICKET, NOT A TASKING CASE

    X-band nominal {cyl_rcs(0.031):.1f} m2 (and the thin-wire regime cuts it further,
    polarization-dependent) with a {lobe_deg(0.031):.2f} deg lobe - and a satellite
    has ONE fixed look geometry per pass: the boom heading must align within
    ~a degree -> P ~ 1-2% per scene. Do not task SAR for the boom. If an
    X-band scene exists anyway, a free look costs nothing - a bright point
    in a field is worth a candidate pin.

[4] DRONE RGB: THE BEST NEW DISCRIMINATOR

    At {GSD_DAY*100:.1f} cm GSD the 8 mm boom is {L/GSD_DAY:.0f} px long but only {2*R_TUBE/GSD_DAY:.2f} px WIDE -
    sub-pixel width dilutes the dark-line contrast to ~0.07 reflectance
    per pixel. Faint to the eye, but a 52-px correlated streak is exactly
    what an oriented line filter (Hough / steerable) recovers: sqrt(52)
    ~ 7x SNR gain along the line. Plus the Insta360 blob ({0.07/GSD_DAY:.1f} px) at its
    far end. Keep the compound sphere+line+blob template - the line is now
    a supporting cue, not a headline feature - and note the 50 m inspection
    pass sees it at 0.66 px wide x 125 px long: unmistakable there.
    (At satellite 30 cm: {L/GSD_SAT:.0f} px long but {2*R_TUBE/GSD_SAT:.2f} px wide - an occasional
     1-px-wide smudge; do not rely on it. Thermal at {GSD_TH*100:.0f} cm: invisible.)

[5] THE INSTA360 ITSELF

    ~7 cm of camera: sub-pixel to satellites, {0.07/GSD_DAY:.1f} px to the drone, radios
    weeks dead - no detection channel. But it is the recovery PRIZE: its
    card holds the descent video and, with it, the ground-truth landing
    footage this entire repository has been reconstructing from physics.

  SUMMARY: the boom adds two real channels - a compound shape signature to
  the day camera (strong, deterministic) and a specular flash to our own
  radar (strong, stochastic). It changes nothing for satellite tasking.
""")
hr()
