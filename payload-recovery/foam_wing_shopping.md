# The foam wing — COMPLETE shopping list

Everything needed to go from nothing to an aircraft that can fly the search area and
bring back imagery. Nothing deferred; nothing assumed to be in a drawer except hand
tools, which are priced separately so the number is honest either way.

| | € |
| --- | --- |
| **Must buy** | **2,082** |
| Tools, only if not already owned | 145 |
| **Total starting from zero** | **2,227** |

**This comes in €102 over the €1,980 figure in `eur2000_build.md`, and that estimate
was the optimistic one.** Making the list genuinely complete surfaced items no earlier
version carried: the **spot welder** (€95 — without it the 18650 cells cannot be
assembled), **mandatory Spanish third-party insurance** (€120), the airspeed sensor
(€25), SD and microSD cards (€56), prop adapters and control linkages the airframe kit
does not include (€23), and a full filament allowance (€85 rather than €25). Choosing
the Matek over the Pixhawk claws back €160 of it.

Two honest levers if €2,082 is the wrong number:

- **Buy the flight packs pre-assembled** from an EU builder → drops the €95 welder and
  the €20 of strip, at a modest per-pack premium. Net roughly break-even, and it saves
  an evening.
- **The €120 insurance is annual, not a build cost** — but it is legally required to
  fly at all in Spain, so it belongs in the number you actually have to spend before
  the first sortie.

**Order the airframe in the same hour you read this.** It is the only 1–2 week lead
item; filter AliExpress to *Enviado desde: España/Europa*, or take the DHL Express
branch in `aliexpress_shopping_list.md`.


## 1 · Airframe & propulsion

| Item | Spec gate that matters | Qty | Vendor | € |
| --- | --- | --- | --- | --- |
| `Believer 1960mm UAV kit` | **KIT** — airframe only, twin motor, EPO, ~1960 mm span | 1 | Ali (ES/EU warehouse) | 270 |
| `SunnySky X2216 880KV motor` | 880 KV, 3–4S | 2 | Ali / rc-innovations | 40 |
| `Hobbywing Skywalker 40A ESC` | 40 A, 3–4S. **BEC on ONE only** — disable the second | 2 | Ali | 30 |
| `APC style propeller 11x5.5` + `12x6` | matched pairs, both sizes to test | 3+3 pr | Ali | 15 |
| Prop adapters / collets | match the X2216 shaft — kit does **not** include | 2 | Ali | 8 |
| `EMAX ES08MA II metal gear servo` | **metal gear**, 12 g. 4 fly + 2 spare | 6 | Ali | 26 |
| Control horns, pushrods, clevises, servo extensions | the kit ships incomplete here | set | Ali | 15 |
| | | | **subtotal** | **404** |

## 2 · Avionics & control

| Item | Spec gate that matters | Qty | Vendor | € |
| --- | --- | --- | --- | --- |
| `Matek F405 WING V2` | ArduPlane, integrated BEC + servo rail (see note) | 1 | rc-innovations / Ali | 75 |
| `Matek M10Q GPS` | M10, with compass | 1 | rc-innovations / Ali | 35 |
| Pitot / airspeed sensor (MS4525 or analog) | **worth it on a wing** — stall margin + wind estimate | 1 | Ali | 25 |
| `RadioMaster Pocket ELRS 2.4GHz` | handset — launch, land, failsafe | 1 | rc-innovations | 60 |
| `RadioMaster RP1 receiver` | nano ELRS rx + one spare | 2 | rc-innovations | 30 |
| | | | **subtotal** | **225** |

## 3 · Comms — LTE primary

| Item | Spec gate that matters | Qty | Vendor | € |
| --- | --- | --- | --- | --- |
| Raspberry Pi Zero 2 W |  | 1 | Amazon.es / kubii | 25 |
| `Waveshare SIM7600E-H 4G HAT` | **E-H variant** — EU bands B3/B20 | 1 | Amazon.es | 80 |
| 1NCE Lifetime Flat IoT SIM | €12+€1, 10 yr, 500 MB, Movistar/Vodafone/Orange | 1 | 1nce.com | 13 |
| microSD 32 GB A1 for the Pi | one spare — they fail | 2 | Amazon.es | 16 |
| LTE + GPS antennas, pigtails | keep clear of CF-filled prints | set | Ali | 15 |
| | | | **subtotal** | **149** |

## 4 · Camera payload

| Item | Spec gate that matters | Qty | Vendor | € |
| --- | --- | --- | --- | --- |
| Used Sony a6000 body | 24 MP APS-C, shutter count < 20k | 1 | Wallapop / eBay ES | 350 |
| Sony E 16 mm f/2.8 pancake, used |  | 1 | Wallapop / eBay ES | 120 |
| `Sony multi terminal shutter release cable` | A6000-compatible multiport | 1 | Amazon.es | 23 |
| PWM camera trigger board (Seagull MAP class) | FC-triggered intervalometer | 1 | Ali | 25 |
| SD cards 64 GB U3 ×2 + USB-C reader | U3 for sustained write | 3 | Amazon.es | 40 |
| | | | **subtotal** | **558** |

## 5 · Power

| Item | Spec gate that matters | Qty | Vendor | € |
| --- | --- | --- | --- | --- |
| Samsung 35E / Molicel P28A 18650 | 24 cells → 3 packs of 4S3P | 24 | nkon.nl | 130 |
| **Spot welder** (kWeld or 709A class) | **you cannot build 18650 packs without one** | 1 | Ali / Amazon.es | 95 |
| Nickel strip 0.15 mm, holders, fish paper, kapton | pack-building stock | lot | Ali | 20 |
| `ToolkitRC M6D` dual charger | **DC input** — runs off the Amarok DC-DC | 1 | Ali | 65 |
| `4S 5000mAh LiPo` — bench & maiden only | spend the careless cycles here | 1 | Amazon.es | 45 |
| 12 V DC-DC 25 A feed + XT90/Anderson leads | Amarok alternator → charging crate | set | Amazon.es | 70 |
| LiPo safe bag | **before** the first charge | 1 | Amazon.es | 19 |
| XT60 pairs, 16AWG silicone, JST-XH leads, heatshrink |  | lot | Ali | 25 |
| | | | **subtotal** | **469** |

## 6 · Build consumables

| Item | Spec gate that matters | Qty | Vendor | € |
| --- | --- | --- | --- | --- |
| Foam-safe CA + activator | **foam-safe only** — normal CA melts EPO | 2 | Amazon.es | 14 |
| 30-min epoxy + fibreglass tape | spar joins and boom roots | 1 | Amazon.es | 16 |
| Velcro straps, zip ties, double-sided foam tape |  | lot | Amazon.es | 12 |
| Threadlocker (blue) + spare M3 hardware | props and mounts vibrate loose | lot | Amazon.es | 10 |
| | | | **subtotal** | **52** |

## 7 · Filament for the X1C parts

| Item | Spec gate that matters | Qty | Vendor | € |
| --- | --- | --- | --- | --- |
| CF-PETG 1 kg | bays, trays, motor plate, grip — **never near antennas** | 1 | Bambu / eSUN | 35 |
| PETG 1 kg | antenna mounts, hatches — non-conductive | 1 | Bambu / eSUN | 25 |
| TPU 500 g | belly skids, vibration isolation | 1 | Bambu / eSUN | 25 |
| | | | **subtotal** | **85** |

## 8 · Sweeper self-recovery

| Item | Spec gate that matters | Qty | Vendor | € |
| --- | --- | --- | --- | --- |
| RECCO reflector tab | 4 g — rescue detectors can find a downed aircraft | 1 | ski shop / dealer | 5 |
| Foil + 3 mm Depron + spray adhesive | sweeper corner **and** the next balloon's cluster | lot | local | 15 |
| | | | **subtotal** | **20** |

## 9 · Legal & admin — required in Spain

| Item | Spec gate that matters | Qty | Vendor | € |
| --- | --- | --- | --- | --- |
| AESA operator registration | free, online, **mandatory before first flight** | 1 | sede.seguridadaerea.gob.es | 0 |
| A1/A3 online pilot certificate | free course + test, mandatory | 1 | AESA | 0 |
| **Third-party drone insurance** | **legally required in Spain**; quotes vary | 1 yr | broker | 120 |
| Operator-number label on the airframe |  | 1 | — | 0 |
| | | | **subtotal** | **120** |

## 10 · Tools — skip any you already own

| Item | Spec gate that matters | Qty | Vendor | € |
| --- | --- | --- | --- | --- |
| Temp-controlled soldering iron + solder | XT60s and 16AWG need ~80 W | 1 | Amazon.es | 45 |
| Digital multimeter |  | 1 | Amazon.es | 25 |
| Wattmeter / power analyser (150 A) | verify propulsion draw before trusting the endurance figure | 1 | Ali | 20 |
| LiPo cell checker / low-voltage alarm |  | 2 | Ali | 10 |
| Hex drivers, 0.1 g scale, digital calipers | CG and mass-budget work | set | Amazon.es | 45 |
| | | | **subtotal** | **145** |

## Four choices worth knowing about

**Matek F405 WING instead of the Pixhawk 6C** (−€100). The better part here, not just
the cheaper one: a wing-specific board with BEC and servo rail integrated, so nothing
extra to wire into foam. Run ArduPlane. If a bigger airframe later wants the Pixhawk's
redundancy, the F405 becomes the spare.

**The spot welder is not optional.** Every earlier list had 18650 cells and nickel
strip but no way to join them — soldering directly to cell cans damages them and is
the classic route to a pack that fails in flight. €95 buys the welder; alternatively
buy 4S3P packs pre-assembled from a reputable EU builder for roughly the same premium
and skip both the tool and the evening.

**A €45 disposable LiPo for the maiden.** The first pack's cycles go on trim flights,
CG hunting and one hard landing. Spend them on a shop LiPo, not on hand-built cells.

**Airspeed sensor added.** €25 for a pitot is the cheapest stall insurance a foam wing
can carry, and ArduPlane's wind estimate makes the search-line planning honest instead
of optimistic.

## Airframe fallback

No Believer EU stock → **Skywalker X8 empty frame** (~$253, 2120 mm flying wing).
Everything above carries over minus one motor, one ESC and one prop adapter. Three
differences: single pusher (no motor-out redundancy), CG more sensitive with swappable
bays, and keep your throwing hand clear of the prop.

## Before the box arrives

Print on the X1C — none of it needs the airframe present: motor-mount plate, battery
tray, two-camera bay shell, TPU belly skids, PETG antenna mounts, launch grip, and the
10 cm corner reflector. Manifest in `day_vs_night.py`.

Do the **AESA registration and the A1/A3 certificate the same week**. Both are free,
both take an afternoon, and neither can be done retroactively after a first flight.
