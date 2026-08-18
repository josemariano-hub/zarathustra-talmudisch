# Shopping lists — AliExpress vs Amazon.es, cheaper-wins rule

Rule applied per item: **AliExpress only where it actually beats Amazon.es**; ties and
near-ties go to Amazon.es for the 24–48 h delivery and returns. Prices marked
**[live]** were scraped 18 Aug 2026 (AliExpress search JSON / Amazon.es result
pages); the rest are indicative. Compare checkout prices with VAT only — both sites
show them VAT-inclusive in Spain.

## 1. The comparison table

| Item | AliExpress | Amazon.es | Verdict | Note |
| --- | --- | --- | --- | --- |
| Believer 1960 airframe KIT | **$269–289 [live]** | not stocked | **ALI** | no race — Amazon has no survey airframes |
| Pixhawk 6C + M10 GPS (Holybro official) | ~€210 | marketplace scalpers only | **ALI** | official store; clones are the trap |
| SunnySky X2216 880KV ×2 | ~€40 | rare/overpriced | **ALI** | |
| Hobbywing Skywalker 40A ESC ×2 | ~€30 | ~€50 | **ALI** | |
| Props 11×5.5 / 12×6 (6+) | ~€2.5/prop | **€14–30 for 2–3 [live]** | **ALI** | 3–5× gap; buy many |
| EMAX metal-gear servos ×6 | **$4.39/u [live]** | **€25/pair [live]** (ES08MD) | **ALI** | 3× gap |
| RadioMaster Pocket ELRS + RP1 rx | ~€90 | barely stocked | **ALI** | 868 MHz LBT region for Spain |
| Waveshare SIM7600**E-H** 4G HAT | ~€55 (official) | ~€75–90 (3rd party; **[live]** search shows only generic €47 boards + €117 OSTENT modems) | **ALI** | E-H = EU bands B3/B20 |
| ToolkitRC M6D dual charger | ~€65 | **ISDT D2 MK2 €93 [live]** | **ALI** | M6D is DC-in — the Amarok DC-DC feeds it |
| XT60, balance leads, nickel strip, silicone wire | ~€25 lot | ~€45 equivalent | **ALI** | |
| Sony shutter cable + PWM trigger | ~€15 | **€22.54 [live]** (A6000-compatible cable) | **ALI** | if compatibility doubts: Amazon version, returnable |
| Raspberry Pi Zero 2 W | ~€28 (often scalped) | ~€25 | **AMAZON** | kubii/berrybase ~€18 beats both if not urgent |
| LiPo safe bag | ~€12 | **€17–23 [live]** | **AMAZON** | near-tie after shipping; fire safety item, want it before first charge |
| Foam-safe CA + activator, epoxy | slow, liquid-shipping issues | ~€15, next-day | **AMAZON** | |
| Velcro straps, cable ties, heatshrink | ~€8 | ~€12 | **AMAZON** | tie → speed wins |

## 2. Final AliExpress cart (~€800)

Search lines, in order of lead time (airframe first):

1. `Believer 1960mm UAV kit` — KIT, twin-motor, EPO — ~€270
2. `Pixhawk 6C flight controller` — Holybro official store, M10 GPS combo — ~€210
   (budget path: `Matek F405 WING V2` + `Matek M10Q GPS` ~€110)
3. `SunnySky X2216 880KV motor` ×2 — ~€40
4. `Hobbywing Skywalker 40A ESC` ×2 — ~€30
5. `APC style propeller 11x5.5` + `12x6` — 3 pairs each — ~€15
6. `EMAX ES08MA II metal gear servo` ×6 — ~€26
7. `RadioMaster Pocket ELRS` + `RadioMaster RP1 receiver` — ~€90
8. `Waveshare SIM7600E-H 4G HAT` — Waveshare official store, E-H variant — ~€55
9. `ToolkitRC M6D dual charger` — ~€65
10. `Sony multi terminal shutter release cable` + `camera trigger PWM` — ~€15
11. `XT60 connector` + `4S balance lead JST-XH` + `nickel strip 0.15mm` + `16AWG silicone wire` — ~€25

## 3. Final Amazon.es cart (~€75)

The this-week-with-returns basket:

1. Raspberry Pi Zero 2 W — ~€25 (or kubii.fr €18 if a few days don't matter)
2. Bolsa LiPo ignífuga — ~€19 [live €17–23] — before the first pack charge, not after
3. Cianocrilato apto para foam + activador, epoxi 30 min — ~€15
4. Velcro, bridas, termorretráctil — ~€12

## 4. Neither list (never was a two-way race, ~€620)

- **24× 18650 (Samsung 35E / Molicel P28A)** — nkon.nl ~€130. Both marketplaces are
  fake-capacity minefields for cells; this is non-negotiable for flight packs.
- **Used Sony a6000 + 16 mm f/2.8** — Wallapop/eBay ES ~€470.
- **IoT SIM: 1NCE Lifetime Flat** (1nce.com, ships to Spain) — **€12 + €1 SIM,
  one-time, 10 years, 500 MB included**, roams onto **Movistar + Vodafone + Orange**
  in Spain (attaches to whichever serves the field — exactly the multi-carrier
  requirement), throttled to 1 Mbit/s, top-up €10 per extra 500 MB + 250 SMS.
  APN `iot.1nce.net`. Data budget: MAVLink ~30 MB/sortie + geotagged thumbnails
  ~20 MB + a few full-res confirmations ~30 MB ≈ **80 MB/sortie → ~6 sorties on the
  included 500 MB** — one Zone A campaign costs €13, maybe one top-up. The 1 Mbit/s
  cap fits the 330 kbps design load; full-res frames take ~1 min each, so send them
  only for flagged candidates and dump the rest from the SD card after landing.
  Fat-pipe plan B if live full-res ever matters: a €5–7/mo Simyo/Lobster consumer
  prepaid (Orange network, 10–25 GB) — single-network, so check the Zone A coverage
  map before trusting it.
- **RECCO tab** ~€5; foil + Depron + spray adhesive (reflector/test corner) ~€15 — local.

## Totals

AliExpress ~€800 + Amazon.es ~€75 + neither ~€620 ≈ **€1,495–1,570 landed** against
the €1,980 plan → **~€400 crash reserve**, which a foam aircraft on a real search
will spend (second motor pair, props, servos, wing foam).

## Warnings that save money

1. **Name collision:** "Sky Surfer X8" (€50–150 trainer) is neither a Skywalker X8
   nor our airframe.
2. **Official stores only** on AliExpress for FC, motors, ELRS, Waveshare — clone
   Pixhawks are the second classic trap after fake 18650s. On Amazon, "Adapter
   Universe" style resellers are legitimate but charge the 3× shown above.
3. **Band gates:** SIM7600**E-H** (EU LTE bands), ELRS **868 MHz LBT** for Spain.
4. **% OFF theatre on both sites** — compare checkout totals only.
5. Order sequence: AliExpress cart today (1–2 week lead), nkon with it, Amazon cart
   the week the airframe ships, camera hunt on Wallapop in parallel.
