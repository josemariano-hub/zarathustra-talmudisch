#!/usr/bin/env python3
"""
Sensor investment within the 3.0 kg MTOM, and the full-sortie arithmetic:
how long is a flight, and how much ground does it scan for a 0.70 m target?

SI units. Prices indicative street (EUR, Aug 2026); 1280-class LWIR cores are
quote-only items - the figure used is a mid-estimate and is flagged as such.
"""
import math
def hr(c="="): print(c*104)

G0=9.80665; CEILING=120.0; TARGET=0.70
SIDELAP=0.25; TURN=0.78; V=13.0
RESERVE=0.85          # land with 15% battery
OVERHEAD_MIN=6.0      # launch+climb (40 s to 120 m at 3 m/s), transit out/back, landing
AUG_NIGHT_H=7.4; TURNAROUND_MIN=10.0

def sortie(rate_km2h, endur_min):
    productive=endur_min*RESERVE-OVERHEAD_MIN
    return productive, rate_km2h*productive/60.0

def optics(px_w, pitch, f):
    gsd=CEILING*pitch/f; return gsd, px_w*gsd, px_w*gsd*(1-SIDELAP)*V*TURN*3600/1e6

print(); hr()
print("  SENSOR INVESTMENT + FULL-SORTIE ARITHMETIC  (3.0 kg MTOM, ~0.5-0.9 kg margin free)")
hr()

CONFIGS=[
 # name                                px_w  pitch    f      endur  mass_d  price_d  px_on_t note
 ("DAY  a6000 24MP (baseline)",        6000, 3.9e-6, 0.016,  138,   0,      0),
 ("DAY  a7R-class 61MP (upgrade)",     9504, 3.76e-6,0.016,  132,  250,   1100),
 ("NIGHT InfiRay 640 (baseline)",       640, 12e-6,  0.0091, 158,   0,      0),
 ("NIGHT 1280 LWIR, sharp lens",       1280, 12e-6,  0.0182, 156,   60,   3300),
 ("NIGHT 1280 LWIR, wide lens",        1280, 12e-6,  0.0091, 156,   60,   3300),
]
print(f"\n  {'configuration':<34}{'GSD':>7}{'swath':>8}{'px on 0.7m':>11}{'ID?':>5}"
      f"{'flight':>8}{'km2/sortie':>12}{'+EUR':>7}")
res={}
for name,pw,pitch,f,endur,md,pd in CONFIGS:
    gsd,sw,rate=optics(pw,pitch,f)
    pmin,km2=sortie(rate,endur)
    pxt=TARGET/gsd
    idc="YES" if pxt>=6 else "no"
    res[name]=(gsd,sw,rate,pmin,km2,endur)
    print(f"  {name:<34}{gsd*100:>5.1f}cm{sw:>7.0f}m{pxt:>11.1f}{idc:>5}"
          f"{endur:>5.0f}min{km2:>12.1f}{pd:>7,}")

print(f"""
  FULL SORTIE, wall clock (night, baseline 640):
    preflight checks           10 min
    hand launch + climb         1 min      (40 s to 120 m at 3 m/s)
    transit to survey area      2 min      (~1.5 km at 13 m/s)
    survey lines              {res['NIGHT InfiRay 640 (baseline)'][3]:.0f} min
    return + land               5 min
    ------------------------------------
    airborne ~{res['NIGHT InfiRay 640 (baseline)'][5]:.0f} min, block time ~{res['NIGHT InfiRay 640 (baseline)'][5]+15:.0f} min, {res['NIGHT InfiRay 640 (baseline)'][4]:.1f} km2 scanned
""")

n_sorties=(AUG_NIGHT_H*60)//(158+TURNAROUND_MIN)
print(f"  Per 7.4 h August night: {n_sorties:.0f} full sorties + a partial ->")
for k in ["NIGHT InfiRay 640 (baseline)","NIGHT 1280 LWIR, sharp lens","NIGHT 1280 LWIR, wide lens"]:
    g=res[k]
    per_night=g[2]*(AUG_NIGHT_H*0.80)  # 80% of night productive incl. turnarounds
    print(f"    {k:<36}~{per_night:>5.1f} km2/night")

print(f"""
  THE INVESTMENT CALL
  Same core, two lenses, two different missions:
    - SHARP (18.2 mm): 7.9 cm GSD, 8.8 px on target -> crosses the 6 px
      IDENTIFICATION threshold. Every night detection is self-confirming;
      the day-confirmation loop disappears. Coverage unchanged (~17 km2/night).
    - WIDE (9.1 mm): same 16 cm GSD as the 640 but double swath ->
      ~34 km2/night of positions-only.
  Buy the SHARP lens. Nights are plentiful; what is scarce is certainty at
  3 a.m. An identification-capable night sensor removes an entire day-loop
  per candidate cluster. NETD upgrades (Boson+ 20 mK) buy nothing - the
  margin is already ~100 sigma; resolution is the only axis that matters.
  Mass +60 g fits the MTOM margin trivially. ~3,300 EUR is a quote-item
  mid-estimate; night sweeper goes ~3,540 -> ~6,000 EUR.
  The 61 MP day upgrade (+1,100 EUR, +52% swath, 13.0 km2/sortie) is a
  separate, defensible coverage buy - take it only if the ellipse is large.
""")
hr()
