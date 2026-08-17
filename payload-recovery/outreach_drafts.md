# Outreach drafts — Planet and Airbus

Placeholders in `«guillemets»` need filling once `descent_reconstruction.py` has produced
the ellipse. Keep both emails short: your contacts will forward them internally, and the
person who actually approves a goodwill tasking wants the ask in the first three lines.

**Send both.** They are not competing for the same favour — Airbus has the resolution you
need, Planet has the revisit and the archive depth. If both say yes, you get a stronger
result than either alone.

---

## A. Airbus — Pléiades Neo

> **Subject:** 30 cm tasking request — recovering a stratospheric balloon payload in central Spain

Hi «name»,

We lost a payload and I think Pléiades Neo can find it.

On «date» we flew a 3 kg stratospheric balloon from «launch site». The payload is a
0.70 m white expanded-polystyrene sphere — about as close to an ideal high-albedo
calibration target as anything that falls out of the sky by accident. Telemetry ends at
«altitude» and our descent reconstruction puts it inside a «N» km² box near «place»,
centred on «lat, lon».

I ran the detection numbers before writing to you. At 30 cm the sphere is 4.3 pixels of
projected area, with an apparent reflectance of 0.59 once you account for the fact that a
sphere is not a flat panel, giving a contrast of about 0.24 against dry Meseta soil after
atmospheric attenuation — roughly 180× Pléiades Neo's noise-equivalent contrast. It also
casts a resolvable shadow, which gives us a bright–dark dipole to matched-filter on rather
than a bare bright pixel. Detection is not the difficulty; discriminating the sphere from
silage bales is, and separating a 1.2 m bale from a 0.70 m sphere is exactly what 30 cm
buys and 50 cm does not. That is why I am asking you specifically.

What would make this work:

- 1 × archive scene over the AOI, most recent available before «date»
- 2 × tasked acquisitions after «date», separated by ≥3 days
- ≤15° off-nadir, ≤5% cloud, PAN delivered separately from the pansharpened product

I know this sits under your tasking minimums, so I am asking whether it can go out as
evaluation or goodwill collection — a single pass on an existing Iberian corridor. In
return you are welcome to the whole story: we will write up the detection method and the
recovery publicly, with the imagery credited to Airbus, whether or not we find it. A
"30 cm imagery recovers a lost stratospheric payload" case study writes itself, and the
negative result is nearly as interesting as the positive one.

One thing worth flagging: central Spain is ploughing stubble right now, so the sphere's
odds of remaining exposed drop week by week. If this is possible at all, sooner is worth
a great deal.

Happy to send the full feasibility note — radiometry, shadow geometry, confuser analysis
and the AOI as GeoJSON.

Best,
José Mariano

---

## B. Planet — SkySat, Pelican, PlanetScope

> **Subject:** Finding a 0.7 m sphere in Spain — tasking request, and a question about Pelican

Hi «name»,

An unusual ask, and one I think is genuinely interesting rather than just a favour.

On «date» we flew a 3 kg stratospheric balloon from «launch site». The payload is a 0.70 m
white expanded-polystyrene sphere. Telemetry ends at «altitude»; our reconstructed landing
ellipse is «N» km² near «place», centred on «lat, lon».

I modelled the detection before asking. Against dry soil the sphere gives about 0.14
contrast at SkySat's true 0.72 m ground sampling — comfortably above the noise floor, so
SkySat can certainly *see* it. My honest concern is discrimination rather than detection:
at 0.72 m the sphere and a 1.2 m silage bale are both "a bright blob a couple of pixels
across", and Spanish farmland has a great many bales. That is a size-gate problem, and it
is the one place where the extra resolution matters.

So two questions:

1. **Is Pelican available for this?** At 40 cm the size gate starts working, and if any
   Gen-2 hardware is collecting at 30 cm it would be decisive. This strikes me as a nice
   demonstration target for a new sensor — a known-size, known-albedo, known-position
   object is a rare thing to have on the ground.
2. **If SkySat is the realistic option**, could we get two acquisitions separated by ≥3
   days, plus the most recent archive scene from before «date»? The temporal pair is what
   kills the movers, and the archive baseline is what removes everything that was already
   there. With both, my estimate is a shortlist of a couple of hundred candidates over
   50 km², which is a day of driving.

Separately — is our PlanetScope access able to cover the AOI for the surrounding weeks? I
am not proposing to detect with it. At 3 m the sphere lifts a pixel by 0.008 in
reflectance, which is below the archive's day-to-day stability, so it is useless as a
detector. But it is ideal for masking the search area, confirming which fields got
ploughed when, and picking cloud-free tasking dates.

I know this is under your order minimums and I am asking about evaluation or goodwill
terms. In exchange: full public write-up of the method and outcome, imagery credited to
Planet, and a clean real-world validation of small-object detection that is not a parking
lot or a shipping container.

Timing matters — stubble ploughing is underway in the area and the sphere's exposure is
degrading.

Best,
José Mariano

---

## Notes on working these

**Lead with the ask, not the story.** Both drafts do this deliberately. The person who can
approve free tasking is usually two forwards away from your contact and will read three
lines.

**The credibility move is the numbers.** Showing you already did the radiometry signals
this is not a fishing expedition and that their pixels will not be wasted. It also lets a
technical reader check your reasoning immediately, which builds far more trust than
enthusiasm does.

**Being honest about SkySat's limits helps you.** Telling Planet the weakness of their own
50 cm option is what makes the Pelican question land as a serious suggestion rather than
an upsell request. People trust a request that concedes something.

**Offer something real.** A public write-up with imagery credit is worth more to their
marketing than the collection costs them, and it is genuinely in your interest too.

**Do not oversell the odds.** The sphere may be fragmented, under a hedge, or already in a
farmer's shed. Say so if asked — a partner who was told the honest probability will be
willing to help you again.
