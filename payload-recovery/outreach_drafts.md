# Outreach drafts — Planet and Airbus

**Status: fully sendable — the only placeholder left is [NAME].** The investigation
report (12 Aug 2026 flight) filled the dates and AOI boxes, and the canopy colour is
now confirmed: **orange**. That completes the pitch — the primary target is a 2.13 m
orange canopy, and orange fabric's high-red/low-blue signature gives a band-ratio gate
that removes white bales and bare soil categorically, on top of the size gate.

**Send both.** They are not competing for the same favour — Airbus has the resolution,
Planet has the revisit and the archive depth. If both say yes, you get a stronger
result than either alone.

---

## A. Airbus — Pléiades Neo

> **Subject:** 30 cm tasking request — recovering a stratospheric balloon payload near Burgos

Hi [NAME],

We lost a payload and I think Pléiades Neo can find it.

On 12 August 2026 we flew a stratospheric balloon from Villadiego, Burgos. Telemetry
ended at 22,205 m; the flight computer's battery failed and the balloon was cut down by
its watchdog. Our calibrated descent reconstruction (GFS winds, checked out of sample
against the recorded ascent) puts the landing in a 38 km² box on the páramo farmland
north of Villadiego, with a 139 km² 90% box around it. Exact WGS84 boxes below; GeoJSON
and GPX on request.

The good news for imaging: the 84-inch parachute stayed attached, so the target is not
just our 0.70 m polystyrene sphere — it is a **2.13 m orange canopy** spread over
stubble. At 30 cm that is 7 pixels across, riding next to the sphere's
bright-plus-shadow dipole. I ran the radiometry before writing: detection has large
margin, and the discrimination that used to worry me (white 1.2–1.5 m silage bales)
now works doubly in our favour. The canopy out-sizes every bale — and it is orange:
high red reflectance over very low blue, so a simple red/blue band ratio on the
multispectral product separates it categorically from white plastic (ratio ≈ 1) and
dry soil (≈ 1.5–2). Six-band VNIR at 30 cm is close to ideal for exactly this gate,
which is one more reason the ask is to Pléiades Neo specifically.

What would make this work:

- 1 × archive scene over the AOI, most recent available before 12 Aug 2026
- 1–2 × tasked acquisitions after that date (anything after 12 Aug 21:00 UTC is valid —
  the payload has not moved since)
- ≤15° off-nadir, ≤5% cloud, PAN delivered separately from the pansharpened product

AOI (WGS84): **50% box 42.63156–42.69375 N, 3.89968–3.81511 W (38 km²)**;
90% box 42.60287–42.72243 N, 3.93869–3.77610 W (139 km²).

I know this sits under your tasking minimums, so I am asking whether it can go out as
evaluation or goodwill collection — a single pass on an existing Iberian corridor. In
return you are welcome to the whole story: we will write up the detection method and
the recovery publicly, with the imagery credited to Airbus, whether or not we find it.
A "30 cm imagery recovers a lost stratospheric payload" case study writes itself.

One thing worth flagging: the payload has been on the ground since 12 August and the
area is in harvest — its exposure degrades week by week. If this is possible at all,
sooner is worth a great deal.

Happy to send the full feasibility note — radiometry, shadow geometry, confuser
analysis — plus the AOI as GeoJSON and the investigation report.

Best,
José Mariano

---

## B. Planet — SkySat, Pelican, PlanetScope

> **Subject:** Finding a parachute canopy near Burgos — tasking request, and a question about Pelican

Hi [NAME],

An unusual ask, and one I think is genuinely interesting rather than just a favour.

On 12 August 2026 we flew a stratospheric balloon from Villadiego, Burgos; a power
failure ended telemetry at 22 km and the balloon was cut down by its watchdog. Our
calibrated descent reconstruction gives a 38 km² primary box (90%: 139 km²) on
farmland north of the launch site — exact boxes below.

The target is better than I first thought when I modelled this. The 84-inch parachute
stayed attached, so the object to find is a **2.13 m canopy** on stubble — about
3 pixels across at SkySat's true 0.72 m cell, which moves SkySat from "sees an
unidentifiable blob" to a genuine candidate, with the 0.70 m sphere and its shadow as
a co-located confirming cue. My residual concern was separating the canopy from
1.2–1.5 m silage bales; it dissolved twice over. The canopy out-sizes them, and the
gores are **orange** — a red/blue band ratio flags orange fabric at ≈ 4–6 against ≈ 1
for white bale wrap and ≈ 1.5–2 for dry soil, so the colour gate settles the bale
problem even at SkySat's cell size.

So two questions:

1. **Is Pelican available for this?** At 40 cm the canopy is 5+ pixels and the size
   gate is decisive; a known-size, known-position, known-date target on the ground is
   a rare validation object for a new sensor.
2. **If SkySat is the realistic option**, could we get one or two acquisitions after
   12 Aug 2026 (any pass after 21:00 UTC that day is valid — nothing has moved), plus
   the most recent archive scene from before that date? The archive baseline removes
   everything that was already in the fields; anything new, bright and ~2 m is a
   candidate. Over 38 km² my estimate is a shortlist short enough for one day of
   driving.

Separately — is our PlanetScope access able to cover the AOI for the surrounding
weeks? Not to detect: at 3 m the canopy is under a pixel. But it is ideal for masking
which fields got ploughed when, and for picking cloud-free tasking dates.

AOI (WGS84): **50% box 42.63156–42.69375 N, 3.89968–3.81511 W (38 km²)**;
90% box 42.60287–42.72243 N, 3.93869–3.77610 W (139 km²).

I know this is under your order minimums and I am asking about evaluation or goodwill
terms. In exchange: full public write-up of the method and outcome, imagery credited
to Planet, and a clean real-world validation of small-object detection that is not a
parking lot or a shipping container.

Timing matters — the payload has been down since 12 August and harvest work is
ongoing.

Best,
José Mariano

---

## Notes on working these

**Lead with the ask, not the story.** Both drafts do this deliberately. The person who
can approve free tasking is usually two forwards away from your contact and will read
three lines.

**The credibility move is the numbers.** Showing you already did the radiometry — and
that a real investigation report with a calibrated wind reconstruction sits behind the
AOI — signals this is not a fishing expedition and their pixels will not be wasted.

**The canopy upgrade is the strongest new card.** A 7-pixel orange target at 30 cm
and a 3-pixel one at SkySat's cell is a materially easier ask than the original
2-pixel white sphere — and the orange colour turns discrimination from a size
argument into a band-ratio one-liner. Both emails now lead with it.

**Do not oversell the odds.** Six days of harvest traffic have already passed. The
canopy may be dragged, balled up, or in a farmer's shed. Say so if asked — a partner
who was told the honest probability will be willing to help you again.
