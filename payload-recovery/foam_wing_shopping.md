# The foam wing alone — order this today

The airframe is the critical path (1–2 week lead), and it is the one part of the
build that **cannot be started, tested or printed around until the box arrives**.
Everything here makes the aircraft *fly*. Nothing here is about finding the canopy —
camera, LTE node, packs and charger are in `aliexpress_shopping_list.md` and can be
ordered later without costing a day.

**Total ~€665.** ~10 build-hours to a maiden flight (a further ~30 for the search fit-out).

## The cart

| # | Search line / part | Spec that matters | Qty | ~€ |
| --- | --- | --- | --- | --- |
| 1 | **`Believer 1960mm UAV kit`** | **KIT** (airframe only, no electronics), twin motor, EPO, ~1960 mm span | 1 | 270 |
| 2 | **`SunnySky X2216 880KV motor`** | 880 KV, 3–4S, prop-saver or collet adapter included | 2 | 40 |
| 3 | **`Hobbywing Skywalker 40A ESC`** | 40 A, 3–4S, **BEC on one only** — disable/disconnect the second | 2 | 30 |
| 4 | **`EMAX ES08MA II metal gear servo`** | **metal gear**, 12 g class. 4 fly (2 aileron, elevator, rudder) + 2 spares | 6 | 26 |
| 5 | **`APC style propeller 11x5.5`** and **`12x6`** | matched pairs; buy both sizes to test | 3+3 pr | 15 |
| 6 | **`Matek F405 WING V2`** + **`Matek M10Q GPS`** | ArduPlane-capable, integrated BEC + servo rail | 1+1 | 110 |
| 7 | **`RadioMaster Pocket ELRS 2.4GHz`** + **`RadioMaster RP1 receiver`** | handset + nano rx — launch, land and failsafe | 1+1 | 90 |
| 8 | **`XT60 connector`**, `16AWG silicone wire`, `heatshrink`, `servo extension 30cm` | harness stock | lot | 20 |
| 9 | **`4S 5000mAh LiPo`** *(bench + maiden only)* | any decent 4S — the 18650 flight packs come later | 1 | 45 |
| 10 | Foam-safe CA + activator, 30-min epoxy, fibreglass tape | **foam-safe CA only** — normal CA melts EPO | lot | 20 |

Items 1–8 from AliExpress **filtered "Enviado desde: España/Europa"**, or
rc-innovations.es for 6–7 if you want them this week. Items 9–10 from Amazon.es
tomorrow.

## Two deliberate choices

**Matek F405 WING instead of the Pixhawk 6C** (−€100). For a foam wing this is the
better part, not just the cheaper one: it is a *wing-specific* board with the BEC and
servo rail already integrated, so there is no separate power module or breakout to
wire. Run ArduPlane. If you later want the Pixhawk's redundancy for a bigger
airframe, the F405 becomes the spare. Buy the Pixhawk instead only if you already
know you want it.

**A cheap LiPo for the maiden.** You will bin the first pack's cycles on trim flights,
CG hunting and one inevitable hard landing. Do not do that to hand-built 18650 packs.
€45 buys the right to be careless during the phase where being careless is normal.

## Do not buy yet

Camera, 16 mm lens, LTE node, 18650 cells, ToolkitRC charger, RECCO tab. None of
them is on the critical path, all of them are cheaper or better-chosen once the
aircraft exists, and the used-camera hunt runs in parallel anyway.

## While the box is in transit

Print on the X1C — none of this needs the airframe present:
motor-mount plate, battery tray, the two-camera bay shell, belly skids (TPU),
antenna mounts (**PETG, never CF-filled — carbon fill is conductive**), and the
launch grip. Manifest in `day_vs_night.py`.

## Airframe fallback

If the Believer has no EU-warehouse stock: the **Skywalker X8 empty frame** (~$253,
2120 mm flying wing) is the substitute. It changes three things — single pusher
motor instead of twin, CG more sensitive with swappable bays, and keep your throwing
hand clear of the prop. The rest of this list carries over unchanged, minus one
motor and one ESC.
