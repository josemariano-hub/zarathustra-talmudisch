# AliExpress shopping list — the €2,000 sweeper, cart by cart

Maps every line of `eur2000_build.md` to a search line, what to pick, and a realistic
price. Prices marked **[live]** were scraped from AliExpress on 18 Aug 2026; the rest
are indicative street prices — AliExpress "% OFF" theatre means you compare final
checkout prices only, with EU VAT included (shown at checkout in Spain).

## A. The AliExpress cart

| # | Search line | Pick / spec gate | Qty | ~Price |
| --- | --- | --- | --- | --- |
| 1 | `Believer 1960mm UAV kit` | KIT (no electronics), twin-motor, EPO. **[live] $269–289** | 1 | ~€270 |
| 2 | `Pixhawk 6C flight controller` | **Holybro official store only.** Pixhawk 6C + M10 GPS/compass combo. Budget alternative: `Matek F405 WING V2` + `Matek M10Q GPS` (~€110 total, same ArduPilot) | 1 | ~€210 |
| 3 | `SunnySky X2216 880KV motor` | ×2 (twin). Official SunnySky/Emax store | 2 | ~€40 |
| 4 | `Hobbywing Skywalker 40A ESC` | ×2, with BEC disabled on one (one 5 V source rule) | 2 | ~€30 |
| 5 | `APC style propeller 11x5.5` + `12x6` | 3 pairs of each — crash spares are cheap here | 6+ | ~€15 |
| 6 | `EMAX ES08MA II metal gear servo` | **[live] $4.39 each.** Metal gear only. 4 needed + 2 spares | 6 | ~€26 |
| 7 | `RadioMaster Pocket ELRS 2.4GHz` or `RadioMaster Ranger Micro 868` | **Spain = 868 MHz LBT firmware region for long range**; 2.4 GHz ELRS is fine for launch/land-only under LTE-primary. Handset + one `RadioMaster RP1 receiver` | 1+1 | ~€90 |
| 8 | `Waveshare SIM7600E-H 4G HAT` | **Waveshare official store; the E-H variant** — EU bands B3/B20. (The G-A variant is the Americas one.) | 1 | ~€55 |
| 9 | `ToolkitRC M6D dual charger` | Dual-channel, DC-input — feeds straight off the Amarok DC-DC | 1 | ~€65 |
| 10 | `Sony multi terminal shutter release cable` + `camera trigger PWM` | Multiport shutter cable for the a6000 + PWM-to-shutter trigger board (Seagull MAP-style) | 1 | ~€30 |
| 11 | `XT60 connector` , `4S balance lead JST-XH` , `nickel strip 0.15mm` , `16AWG silicone wire` | Pack-building hardware and harness stock | lot | ~€25 |
| 12 | `lipo safe bag large` + velcro straps + foam-safe CA glue | Field kit | lot | ~€20 |

**Cart A total ≈ €875** (airframe + all electronics except camera and cells).

## B. Deliberately NOT from AliExpress

| Item | Where | Why not Ali | ~Price |
| --- | --- | --- | --- |
| **18650 cells** (24× Samsung 35E / Molicel P28A for 3× 4S3P packs) | nkon.nl or EU battery vendor | AliExpress 18650s are the fake-capacity epicentre; a flight pack is not the place to find out | ~€130 |
| **Used Sony a6000 + 16 mm f/2.8** | Wallapop / eBay ES | Used market is cheaper and inspectable; no used-gear market on Ali | ~€470 |
| **Raspberry Pi Zero 2 W** | EU retail (kubii.fr, berrybase) | Ali scalps it above EU retail (~€18) | ~€20 |
| **Multi-carrier IoT SIM** | Spanish/EU IoT provider (1NCE, Things Mobile class) | The whole point is roaming across Movistar/Orange/Vodafone in Zone A | ~€10–20/yr |
| **RECCO tab** | Recco dealer / ski shop | Not sold on Ali | ~€5 |
| Kitchen foil, 3 mm Depron, spray adhesive (reflector + test corner) | Local | Trivial | ~€15 |
| Filament (PETG, CF-PETG, TPU) | Bambu store / eSUN EU | Print quality consistency; Ali okay as fallback | ~€45 |

**Cart B total ≈ €700.**

## Running total vs budget

≈ **€1,575–1,650 landed** against the €1,980 plan — the margin (~€350) is the crash
reserve, which a foam aircraft on a real search *will* spend: a second motor pair,
more props, a servo handful, spare wing foam.

## Warnings that save money

1. **Name collision:** "Sky Surfer X8" (€50–150 beginner trainer) is not a Skywalker
   X8 and neither is our airframe. Search terms above avoid it.
2. **Official stores only** for FC, motors, ELRS, Waveshare — the clone Pixhawks are
   the second classic AliExpress trap after fake 18650s.
3. **Band checks:** SIM7600**E-H** (EU LTE bands), ELRS on **868 MHz LBT** region for
   Spain if you go the long-range module route.
4. **The €3,067 "UAV catapult launcher"** that shows up in these searches is what the
   Amarok rolling launch does for €0.
5. Shipping: AliExpress Choice consolidates and lands in ~1–2 weeks to Spain; order
   the airframe first (longest lead), electronics second, and start the pack build
   the day the nkon box arrives.
