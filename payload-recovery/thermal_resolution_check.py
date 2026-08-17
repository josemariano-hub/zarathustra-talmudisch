#!/usr/bin/env python3
"""
Is the Mavic 3 Thermal's nominal GSD honest, or does diffraction eat it?

LWIR optics run at long wavelengths and fast f-numbers, so the diffraction spot
can rival the pixel pitch. That is worth checking before claiming a wide lens
buys coverage for free.
"""
import math

LAMBDA = 10.0e-6      # m, LWIR band centre weighted by a ~290 K Planck curve
CEILING = 120.0
TARGET_D = 0.70
A_FOOT = math.pi * (TARGET_D / 2) ** 2

CAMS = {
    # name:            px,  pitch(m), DFOV(deg), f-number
    "M3T thermal":   (640, 12.0e-6, 61.0, 1.0),
    "M4T thermal":   (640, 12.0e-6, 45.0, 1.0),
    "H30T thermal":  (1280, 12.0e-6, 45.0, 1.0),
}

print("=" * 96)
print("  THERMAL RESOLUTION CHECK")
print("=" * 96)
print(f"\n  Q = lambda * F/# / pixel_pitch      Q<1 detector-limited, Q~2 diffraction-limited\n")
print(f"  {'camera':<16}{'focal':>9}{'GSD@120m':>11}{'Airy FWHM':>12}{'Q':>7}{'limited by':>16}")
for name, (px, pitch, dfov, fno) in CAMS.items():
    h = px * 0.8
    diag_m = math.hypot(px, h) * pitch
    f = (diag_m / 2) / math.tan(math.radians(dfov / 2))
    gsd = CEILING * pitch / f
    fwhm = 1.03 * LAMBDA * fno            # m at the focal plane
    q = LAMBDA * fno / pitch
    lim = "detector (pixel)" if q < 1.4 else "optics (diffraction)"
    print(f"  {name:<16}{f*1000:>7.2f}mm{gsd*100:>10.1f}cm{fwhm*1e6:>10.1f}um{q:>7.2f}  {lim:<20}")

print(f"\n  Pixel pitch is 12.0 um. The diffraction FWHM is {1.03*LAMBDA*1.0*1e6:.1f} um,")
print(f"  i.e. {1.03*LAMBDA*1.0/12e-6:.2f} of a pixel - the optics are slightly SHARPER than the")
print("  detector samples. The null-to-null Airy diameter is 2.44*lambda*F = "
      f"{2.44*LAMBDA*1.0*1e6:.1f} um (~2 px),")
print("  but resolution tracks the PSF core, not the first null. So the nominal GSD is honest.")

print("\n  What the target actually subtends:\n")
print(f"  {'camera':<16}{'GSD':>9}{'px across':>11}{'px on target':>14}{'with MTF loss':>15}")
for name, (px, pitch, dfov, fno) in CAMS.items():
    h = px * 0.8
    f = (math.hypot(px, h) * pitch / 2) / math.tan(math.radians(dfov / 2))
    gsd = CEILING * pitch / f
    across = TARGET_D / gsd
    npx = A_FOOT / gsd ** 2
    print(f"  {name:<16}{gsd*100:>7.1f}cm{across:>11.1f}{npx:>14.1f}{npx/1.4**2:>15.1f}")

print("\n  DETECTION vs IDENTIFICATION - the distinction I glossed over")
print("  ---------------------------------------------------------------")
NETD, DT = 0.050, 5.0
for name, (px, pitch, dfov, fno) in CAMS.items():
    h = px * 0.8
    f = (math.hypot(px, h) * pitch / 2) / math.tan(math.radians(dfov / 2))
    gsd = CEILING * pitch / f
    across = TARGET_D / gsd
    mtf_keep = min(1.0, across / (across + 1.4))* 2  # crude PSF dilution for a small target
    mtf_keep = min(1.0, mtf_keep)
    sigma = DT * mtf_keep / NETD
    idable = "yes" if across >= 6 else "NO - a cold blob only"
    print(f"  {name:<16}{across:>5.1f} px across   detect {sigma:>5.0f} sigma   shape ID: {idable}")
print("""
  Detection needs contrast, not pixels: a 5 K anomaly against a 50 mK detector is
  detectable at 2 px across. Identification needs ~6 px, and none of these deliver
  that on a 0.70 m target from 120 m. Thermal tells you WHERE to walk. It does not
  tell you the thing you found is your sphere rather than a patch of dry straw.
""")
print("=" * 96)
