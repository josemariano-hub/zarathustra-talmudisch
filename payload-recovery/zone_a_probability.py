#!/usr/bin/env python3
"""
Zone A landing-probability surface, and the search-order argument it implies.

The investigation report publishes two points on the radial CDF - 50% inside
3.5 km, 90% inside 6.7 km - but every map so far has drawn them as UNIFORM
circles. They are not uniform: probability peaks hard at the centre, and that
is exactly what decides where a one-day search starts.

We do not have the raw Monte Carlo (no telemetry CSV ever arrived, so
descent_reconstruction.monte_carlo() was never run). Instead we fit a
two-parameter radial CDF to the two published radii:

    P(<r) = 1 - exp(-(r/a)^k)

which reproduces BOTH radii exactly. Re-run this against real Monte Carlo
samples when they exist; the rendering below takes any radial CDF.
"""
import math, os, sys

R50, R90 = 3500.0, 6700.0          # m, from the investigation report
LAT, LON = 42.66265, -3.85740

# ---------------------------------------------------------------- the fit
K = math.log(math.log(10) / math.log(2)) / math.log(R90 / R50)
A = R50 / (math.log(2) ** (1.0 / K))

def cdf(r):                        # P(landing within radius r)
    return 1.0 - math.exp(-((r / A) ** K))

assert abs(cdf(R50) - 0.50) < 5e-3, cdf(R50)
assert abs(cdf(R90) - 0.90) < 5e-3, cdf(R90)

def r_at(p):                       # radius containing probability p
    return A * (-math.log(1.0 - p)) ** (1.0 / K)

def hr(c="="): print(c * 78)

if __name__ == "__main__":
    print(); hr()
    print("  ZONE A - LANDING PROBABILITY SURFACE")
    hr()
    print(f"""
  Fitted to the report's own numbers, not assumed:

      P(<r) = 1 - exp(-(r/a)^k)      k = {K:.3f}    a = {A/1000:.2f} km

      check:  P(<3.5 km) = {cdf(R50):.3f}   (report: 0.50)
              P(<6.7 km) = {cdf(R90):.3f}   (report: 0.90)

  Note k = {K:.2f}, not 2. A pure 2-D Gaussian (k=2, sigma {R50/math.sqrt(2*math.log(2))/1000:.2f} km)
  matches the 50% radius but puts 90% at {R50/math.sqrt(2*math.log(2))*math.sqrt(2*math.log(10))/1000:.1f} km, tighter than the
  report's 6.7 km. The real distribution has a slightly heavier tail -
  wind-shear spread in the reconstruction - so use the fitted k.
""")
    hr("-")
    print("  WHERE TO SEARCH FIRST - probability per km2 by ring\n")
    print(f"    {'ring':>12}{'area':>10}{'P in ring':>12}{'P per km2':>12}{'vs outer':>10}")
    rings = [(0, 1000), (1000, 2000), (2000, 3500), (3500, 5000), (5000, 6700)]
    rows = []
    for r0, r1 in rings:
        p = cdf(r1) - cdf(r0)
        area = math.pi * (r1**2 - r0**2) / 1e6
        rows.append((r0, r1, area, p, p / area))
    base = rows[-1][4]
    for r0, r1, area, p, dens in rows:
        print(f"    {r0/1000:>4.1f}-{r1/1000:<3.1f} km{area:>9.1f}{p*100:>11.1f}%{dens*100:>11.2f}%{dens/base:>9.1f}x")
    inner, inner_a = rows[0][3] + rows[1][3], rows[0][2] + rows[1][2]
    tot_a = math.pi * R90**2 / 1e6
    print(f"""
    THE ARGUMENT IN ONE LINE: the inner 2 km holds {inner*100:.0f}% of the probability
    in {inner_a:.0f} km2 - {inner_a/tot_a*100:.0f}% of the 90% area. Per hectare it is {rows[0][4]/base:.0f}x richer
    than the outer ring. Fly concentric boxes outward from the centre;
    do not fly lawnmower lines across the whole circle.
""")
    hr()

    # ------------------------------------------------------------ render
    if "--render" in sys.argv:
        from PIL import Image, ImageDraw, ImageFont
        SCRATCH = os.environ.get("SCRATCH", ".")
        base_png = os.path.join(SCRATCH, "zoneA_base.png")
        Z, RAD = 13, 3
        def deg2tile(lat, lon, z):
            n = 2**z
            return ((lon+180)/360*n,
                    (1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*n)
        cx, cy = deg2tile(LAT, LON, Z); x0, y0 = int(cx)-RAD, int(cy)-RAD
        def px(lat, lon):
            tx, ty = deg2tile(lat, lon, Z); return ((tx-x0)*256, (ty-y0)*256)

        img = Image.open(base_png).convert("RGBA"); W, H = img.size
        # metres per pixel at this latitude/zoom
        mpp = 156543.03392 * math.cos(math.radians(LAT)) / (2**Z)
        px_c, py_c = px(LAT, LON)

        # per-pixel probability mass -> normalised intensity
        heat = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        hp = heat.load()
        def pdf_area(r):                    # probability per m^2 at radius r
            if r < 1.0: r = 1.0
            return (K/(2*math.pi*A*A)) * (r/A)**(K-2) * math.exp(-((r/A)**K))
        peak = pdf_area(mpp/2)
        RAMP = [(0,(0,0,0,0)),(0.08,(40,0,90,90)),(0.22,(120,20,140,130)),
                (0.42,(214,60,90,165)),(0.62,(250,130,30,190)),
                (0.82,(255,200,40,205)),(1.0,(255,255,210,215))]
        def ramp(t):
            for i in range(len(RAMP)-1):
                a, ca = RAMP[i]; b, cb = RAMP[i+1]
                if a <= t <= b:
                    u = 0 if b == a else (t-a)/(b-a)
                    return tuple(int(ca[j]+(cb[j]-ca[j])*u) for j in range(4))
            return RAMP[-1][1]
        total = 0.0
        for yy in range(H):
            dy = (yy-py_c)*mpp
            for xx in range(W):
                dx = (xx-px_c)*mpp
                r = math.hypot(dx, dy)
                if r > 11000: continue
                d = pdf_area(r); total += d*mpp*mpp
                t = (d/peak) ** 0.42
                if t > 0.012: hp[xx, yy] = ramp(min(1.0, t))
        print(f"    [render] integrated probability on grid: {total:.3f}")
        assert 0.90 < total < 1.02

        out = Image.alpha_composite(img, heat)
        d = ImageDraw.Draw(out, "RGBA")
        FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        f = lambda s: ImageFont.truetype(FB, s) if os.path.exists(FB) else ImageFont.load_default()

        def ring(r_m, col, w, dash=False, label=None):
            Re = 6371008.8; pts = []
            for i in range(181):
                th = 2*math.pi*i/180
                pts.append(px(LAT+math.degrees(r_m*math.cos(th)/Re),
                              LON+math.degrees(r_m*math.sin(th)/(Re*math.cos(math.radians(LAT))))))
            if dash:
                for i in range(0, len(pts)-1, 2): d.line([pts[i], pts[i+1]], fill=col, width=w)
            else: d.line(pts+[pts[0]], fill=col, width=w)
            if label:
                lx, ly = pts[135]
                fo = f(27); tw = d.textbbox((0,0), label, font=fo)[2]
                d.rectangle([lx-8, ly-16, lx+tw+16, ly+26], fill=(0,0,0,195))
                d.text((lx+4, ly-10), label, font=fo, fill=col)
        for p, col, dash in [(0.25,(255,255,255,235),False),(0.50,(255,255,255,255),False),
                             (0.75,(255,255,255,215),True),(0.90,(255,220,120,235),True)]:
            rr = r_at(p)
            ring(rr, col, 5 if p in (0.25,0.5) else 4, dash, f"{int(p*100)}%  ·  {rr/1000:.1f} km")

        x, y = px(LAT, LON)
        d.ellipse([x-9,y-9,x+9,y+9], fill=(255,255,255,255), outline=(0,0,0,255), width=3)

        # marker: last contact
        mx, my = px(42.57317, -3.84840)
        d.ellipse([mx-11,my-11,mx+11,my+11], fill=(0,160,255,255), outline=(255,255,255,255), width=3)
        fo = f(29); t = "Último contacto (globo a 22 km)"; tw = d.textbbox((0,0),t,font=fo)[2]
        d.rectangle([mx-tw//2-12, my+30, mx+tw//2+12, my+76], fill=(0,0,0,195))
        d.text((mx-tw//2, my+38), t, font=fo, fill=(255,255,255,255))

        # title
        fo = f(38); t = "ZONA A — densidad de probabilidad de aterrizaje"
        d.rectangle([30, 28, 30+d.textbbox((0,0),t,font=fo)[2]+36, 96], fill=(0,0,0,200))
        d.text((48, 40), t, font=fo, fill=(255,255,255,255))
        fo2 = f(26); t2 = f"ajuste P(<r)=1−exp(−(r/{A/1000:.2f} km)^{K:.2f}) a los radios 50% / 90% del informe"
        d.rectangle([30, 100, 30+d.textbbox((0,0),t2,font=fo2)[2]+36, 148], fill=(0,0,0,185))
        d.text((48, 110), t2, font=fo2, fill=(220,220,220,255))

        # colour bar
        bx, by, bw, bh = 48, H-210, 460, 34
        for i in range(bw):
            d.line([(bx+i, by), (bx+i, by+bh)], fill=ramp(i/bw)[:3]+(255,))
        d.rectangle([bx, by, bx+bw, by+bh], outline=(255,255,255,220), width=2)
        fo = f(26)
        d.rectangle([bx-14, by-46, bx+bw+150, by+bh+46], outline=None, fill=None)
        d.text((bx, by-38), "menos probable", font=fo, fill=(255,255,255,235))
        tw = d.textbbox((0,0),"más probable",font=fo)[2]
        d.text((bx+bw-tw, by-38), "más probable", font=fo, fill=(255,255,255,235))
        d.text((bx, by+bh+10), f"pico central ≈ {rows[0][4]/base:.0f}× la densidad del anillo exterior",
               font=fo, fill=(255,255,255,235))

        # scale bar
        Re = 6371008.8
        x1,_ = px(LAT, LON); x2,_ = px(LAT, LON+math.degrees(5000/(Re*math.cos(math.radians(LAT)))))
        sl = abs(x2-x1); sx, sy = 48, H-96
        d.rectangle([sx-14, sy-44, sx+sl+14, sy+24], fill=(0,0,0,175))
        d.line([(sx,sy),(sx+sl,sy)], fill=(255,255,255,255), width=6)
        for xx in (sx, sx+sl): d.line([(xx,sy-12),(xx,sy+12)], fill=(255,255,255,255), width=6)
        d.text((sx, sy-40), "5 km", font=f(29), fill=(255,255,255,255))

        p_out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zone_a_heatmap.jpg")
        out.convert("RGB").save(p_out, "JPEG", quality=87, optimize=True)
        print(f"    [render] saved {p_out} ({os.path.getsize(p_out)} bytes)")
