# ACTION PLAN — do these, in this order

Zone A centre **42.66265 N, 3.85740 W**. Target: **2.13 m orange canopy** + 0.70 m
white sphere + boom + Insta360. On the ground since **12 Aug 2026, ~21:12 UTC**.
Today is day 0.

## The strategy in four lines

Four lanes run at different speeds. Start all of them today; let none of them wait
for another.

| Lane | Can find it in | Cost | Odds |
| --- | --- | --- | --- |
| **1. The village** — farmers, harvest crews, hunters | **days** | ~€350 | **best** |
| **2. Satellites** — Airbus / Planet goodwill tasking | 1–3 weeks | €0 if goodwill | good |
| **3. Local drones** — UBU lab, Aerobur | 1–2 weeks | €0–1,500 | good |
| **4. Our own sweeper** | 2–3 weeks minimum | ~€1,600 | it is the hedge |

**Say it plainly: the sweeper will probably not be what finds this payload.** It is
the insurance policy and the permanent capability for every future flight. Build it —
but do not let its lead time set the pace of the search. In August, combine harvesters
cover every hectare of Zone A at walking pace. Lane 1 is where the money is.

---

# DAY 0 — TODAY (about 2 hours total)

## Step 1 · Fill in three blanks (5 min)

Open `cartel_villadiego.html` and replace `[TELÉFONO]` and `[NOMBRE]` with a phone
that accepts WhatsApp and the name to answer it. Decide the reward figure — €300 is
the printed default; €200 is fine, €500 if you want it found this week.

**Then print 30 copies in colour.** The orange is the whole point of the poster.

## Step 2 · Call the Ayuntamiento de Villadiego (10 min) — HIGHEST PRIORITY

Phone them, ask for the alcalde or the secretario. Script:

> «Buenos días, le llamo de Zero 2 Infinity, una empresa española de vuelos
> estratosféricos. El 12 de agosto perdimos un globo científico que cayó en el campo
> al norte de Villadiego, bajo un paracaídas naranja de dos metros. No es peligroso —
> no lleva nada tóxico ni explosivo. ¿Podrían ayudarnos a hacerlo saber en el pueblo?
> Les mando un cartel en PDF para el tablón y para las redes del ayuntamiento, y hay
> una recompensa de 300 € para quien lo encuentre.»

Then email them the poster PDF. Ask specifically for: **the tablón de anuncios, the
municipality's Facebook page, and the WhatsApp groups of the pedanías.**

**Why this is step 2 and not step 8:** the people driving over Zone A right now are
the most likely finders in this entire plan, and this costs a phone call.

## Step 3 · Email the UBU drone laboratory (10 min) — the best partner

- **To:** Prof. **José Manuel González**, coordinator, Unidad de Investigación
  Conjunta en Tecnología de Drones — via the UBU Escuela Politécnica Superior
  directory (`ubu.es`). Copy the JRU/UBUDrone general contact if listed.
- **Send:** email A in `local_partners_burgos.md` (Spanish, ready).
- **Attach:** `zone_a.geojson`, `zone_a.kml`, `flight_facts.md` (as PDF), **and the
  investigation report** `HAB_Flight1_Investigation_Report.docx`.
- **Also paste in the link** to the feasibility note artifact.
- **Ask:** a joint exercise / student campaign, not a paid job.
- Expect a reply in 3–10 days (academic August). Follow up day 5.

## Step 4 · Email Aerobur (5 min) — the paid option and the farmer network

- **To:** the contact form / address at **aerobur.es**.
- **Send:** email B in `local_partners_burgos.md`.
- **Attach:** `zone_a.kml` (opens in anything) + a photo of an identical orange canopy.
- **Ask both questions**: day rate for 38 km², *and* whether they already have imagery
  of the area and can ask their farmer clients. **The second question may be worth
  more than the flight.**
- Expect a reply in 1–3 working days.

## Step 5 · Fire the satellite lane (15 min)

Two emails, two different senders — decide per contact:

- **If your Airbus/Planet contacts read Catalan/Spanish and a UPC association member
  will send it:** use `outreach_drafts_ca.md` (UPC Space Program version), sent from
  **the student's own address**, with the balloon photo attached. Do not send this
  version from your Z2I address — the identity has to match the sender.
- **Otherwise (international contact, or you are sending it yourself):** use
  `outreach_drafts.md` — the English Z2I version. Both are complete; only `[NAME]` is
  blank.
- **Attach to both:** `zone_a.geojson` + the balloon photo.
- **Airbus** → ask for Pléiades Neo, 30 cm: 1 archive scene before 12 Aug + 1–2 tasked
  after, ≤15° off-nadir, PAN separate.
- **Planet** → ask about Pelican, and SkySat + the archive baseline.

## Step 6 · Place the hardware orders (30 min)

Follow **"The 2-week plan"** section in `aliexpress_shopping_list.md`. In order:

1. **Amazon.es basket** — Pi Zero 2 W, LiPo bag, adhesives, velcro (+ the EU-substitute
   servos and charger if RC Innovations lacks stock). Arrives in 1–2 days.
2. **rc-innovations.es** — Pixhawk 6C + M10 GPS, RadioMaster Pocket + RP1, motors,
   ESCs, props. 24–72 h.
3. **SIM7600E-H hat** — Amazon.es (pay the €25 premium over AliExpress for the clock).
4. **nkon.nl** — 24× 18650 (Samsung 35E or Molicel P28A). 3–6 working days.
5. **1NCE Lifetime Flat SIM** — €12 + €1, at `1nce.com`. 3–7 days.
6. **Airframe** — work branches A→D in that section. **Hard rule: if nothing is
   secured with ≤10-day delivery by end of day 2, buy the Foxtech/MakeFlyEasy DHL
   Express option immediately.**

## Step 7 · Open the camera hunt (5 min)

Wallapop and eBay ES: saved searches for **"Sony a6000"** and **"Sony 16mm f2.8"**.
Target ~€470 for both. Local pickup in Barcelona preferred. **Deadline: day 4** —
after that, buy whatever is available with shipping.

## Step 8 · Start printing (5 min)

Put the X1C to work on the camera bay, mounts and skids (`day_vs_night.py` manifest),
and the corner-reflector frame from `reflector_build_sheet.md` for the next flight.
Filament is cheap and the printer is idle.

---

# DAY 1–2

**9.** Deliver posters in person: Villadiego bars and the panadería, the
**cooperativa agrícola**, the agricultural supply shop, the gasolinera, and the
notice boards of the surrounding pedanías. Twenty minutes each, and this is the lane
with the best odds.

**10.** Find the **cotos de caza** for the Zone A municipalities (the ayuntamiento
will know who the president is) and call them. Hunters walk the ditches, margins and
copses — exactly where a wind-dragged canopy ends up and where no harvester goes.

**11.** Post in the Villadiego-area **Facebook and WhatsApp groups**. Photo of an
identical orange canopy, the date, the map, the phone, the reward.

**12.** Email **ENG Drone** (engdroneinfo@gmail.com — verify first) and **VISUAIR**
with a shortened version of email B, to have competing quotes in hand.

**13. Airframe gate**: if no branch has confirmed ≤10-day delivery — buy the express
option now. Do not let this slide to day 3.

---

# DAY 3

**14.** No reply from Aerobur → **phone them**. Small operators answer phones, not
inboxes.

**15.** Confirm the Ayuntamiento actually posted it. Politely.

---

# DAY 5–7

**16.** No reply from UBU → phone the Escuela Politécnica Superior and ask for the
JRU coordinator directly. August is holiday season; persistence is not rudeness.

**17.** No reply from Airbus/Planet → one short follow-up, then let it rest. Goodwill
tasking either moves or it doesn't.

**18.** **Decision gate:** if UBU has not engaged and no free option is moving,
**pay Aerobur for one day** over the Zone A 50% circle. €1,000–1,500 to sweep the
38 km² where the payload most likely is, three weeks before the sweeper flies, is
good value. Do not wait for the DIY aircraft out of sunk-cost pride.

---

# DAY 10–14

**19.** Kit complete → build, bench-test the LTE node and trigger, maiden the
aircraft somewhere legal and boring, **then** fly Zone A.

**20.** Run **Z2I-TP-001** (`radar_rod_test_plan.md`) with the 70 cm rod on a
Saturday, before spending the rest of the radar money.

**21.** **Search order, always:** Zone A 50% circle → Zone A 90% ring → only then
Zone B. Zone B requires *both* independent termination systems to have failed.

---

# THE STOP RULE — when something is found

1. **Photograph it in situ before touching it** — including a wide shot showing the
   field, and note the GPS position. This is data for the next flight.
2. **Secure the Insta360 and its memory card first.** The card holds the descent
   video from 22 km. That is the real prize; the foam is replaceable.
3. **Pay the reward immediately and publicly thank whoever found it.** You will fly
   from Villadiego again, and the next payload may land in the same fields.
4. **Stand down the other lanes the same day** — email UBU, Aerobur, Airbus and
   Planet to tell them it was found, and thank them anyway. People remember being
   told the ending. It is why they help a second time.

---

# TRACKER

| # | Contact | Lane | Sent | Reply | Next action |
| --- | --- | --- | --- | --- | --- |
| 2 | Ayuntamiento de Villadiego | village | | | |
| 3 | UBU — Prof. J.M. González | drones | | | |
| 4 | Aerobur | drones | | | |
| 5 | Airbus (Pléiades Neo) | satellite | | | |
| 5 | Planet (Pelican/SkySat) | satellite | | | |
| 10 | Coto de caza — Villadiego | village | | | |
| 12 | ENG Drone / VISUAIR | drones | | | |
| 6 | Airframe order | build | | | |

---

## Attachment cheat-sheet

| File | Send it to |
| --- | --- |
| `zone_a.geojson` | Airbus, Planet, UBU — the AOI every email promises |
| `zone_a.kml` | Aerobur, ENG Drone, VISUAIR, anyone local (opens in Google Earth) |
| `cartel_villadiego.html` | print in colour → PDF for the ayuntamiento and social media |
| `flight_facts.md` | UBU, and any technical partner who asks for the details |
| investigation report `.docx` | UBU — it is the credibility document |
| feasibility note (artifact link) | Airbus, Planet, UBU — the method behind the ask |
| photo of an identical orange canopy | **everyone** — it is the single most useful attachment |
