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

# ================================================================ descend-to-inspect
print()
hr()
print("  DESCEND-TO-INSPECT - altitude as the zoom lens you already own")
hr()
INSPECT_ALT=50.0
gsd640_lo=INSPECT_ALT*12e-6/0.0091
px_lo=TARGET/gsd640_lo
print(f"""
  The 640 core at {INSPECT_ALT:.0f} m AGL: GSD {gsd640_lo*100:.1f} cm -> {px_lo:.1f} px on the sphere.
  That is PAST the 6 px identification threshold - the same certainty the
  1,280-class core delivers from 120 m, using the 900 EUR sensor already bought.
""")
# maneuver cost: spiral down, low pass, climb back
sink_spiral=3.0; climb=3.0; dh=CEILING-INSPECT_ALT
t_down=dh/sink_spiral; t_pass=20.0; t_up=dh/climb
t_insp=(t_down+t_pass+t_up)/60.0
e_climb=2.09*G0*dh/0.55/3600     # Wh, climb at drivetrain efficiency
print(f"  Cost per inspection: {t_down:.0f} s spiral down + {t_pass:.0f} s pass + {t_up:.0f} s climb "
      f"= {t_insp:.1f} min, {e_climb:.1f} Wh (negligible)")
# acoustics at 50 m
spl_lo=18.0+20*math.log10(CEILING/INSPECT_ALT)
print(f"  Noise during the pass: ~{spl_lo:.0f} dBA at ground - still under the 32 dBA night ambient.")

# break-even vs the 1280 core
rate640=res["NIGHT InfiRay 640 (baseline)"][2]
surv=128.0
print(f"\n  {'false alarms/km2':>18}{'inspections/sortie':>20}{'survey lost':>13}{'km2/sortie':>12}")
for d in [0.5,1,2,3,5,8]:
    # solve A = rate*(surv - t_insp*d*A)/60  ->  A = rate*surv/60 / (1 + rate*t_insp*d/60)
    A=rate640*surv/60/(1+rate640*t_insp*d/60)
    n=d*A
    print(f"  {d:>18.1f}{n:>20.0f}{n*t_insp:>10.0f}min{A:>12.1f}")
print(f"""
  Break-even: even at 3 false alarms per km2 the inspections cost only 17 of the
  128 survey minutes (13% of coverage); it takes ~8/km2 before nearly a third of
  the sortie is spent spiralling. Below that, identification is essentially free.

  VERDICT - revised: DO NOT buy the 1280 core yet. Fly the 900 EUR 640 with
  descend-to-inspect: detect at 120 m, geotag, finish the survey lines, then fly
  one inspection tour of the queue at 50 m before landing (the LTE preview makes
  the queue live - the van marks candidates as they appear). The first sortie
  MEASURES the real false-alarm density; buy the 1280 sharp core only if it
  comes in well above ~5/km2. The 3,300 EUR stays in the pocket until the data,
  not a datasheet, says otherwise.

  One safety note: 50 m at night demands a hard terrain floor - flat llanura
  only, ArduPilot terrain data loaded, inspection waypoints auto-capped, and
  no descents in the barrancos. The sphere is not worth the aircraft.
""")
hr()
