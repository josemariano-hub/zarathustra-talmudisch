# Payload recovery — 0.70 m white porexpan sphere, central Spain

> **Note on placement.** This directory is unrelated to the Zarathustra edition that
> occupies the rest of this repository. It was committed here because the working
> branch for this task pointed at this repo. Move it to a proper home when convenient.

Feasibility analysis for locating a 3 kg high-altitude balloon payload — a 0.70 m
white expanded-polystyrene sphere carrying a **1.5 m carbon-fibre boom + Insta360** —
over the Spanish Meseta. The conductive boom is a linear radar scatterer (11.4 m²
broadside at 24 GHz, glint-lobe 0.24°: a once-per-pass 65-chirp flash for the radar
bay — a stochastic third channel for THIS search) and, at drone GSD, a 52-px dark
line attached to the white disc — the compound sphere+boom+camera template empties
the residual confuser list. SAR tasking unchanged (glint ~1–2%/scene: never task
for it). The Insta360's card holds the descent video — the recovery prize.

## Contents

| File | What it is |
| --- | --- |
| `sphere_detectability.py` | Detection model. Lambertian sphere photometry, shadow geometry, sensor comparison, confuser discrimination cascade, search economics, SAR reflector sizing. |
| `analysis_output.txt` | Full numeric output of the above. |
| `feasibility_note.html` | Written brief, suitable for forwarding to imagery providers. |
| `descent_reconstruction.py` | Telemetry → landing ellipse → tasking AOI as GeoJSON. |
| `sphere_detector.py` | Matched-filter detector over delivered imagery → ranked candidate list. |
| `outreach_drafts.md` | Emails to Planet and Airbus. |
| `spectral_and_drone.py` | Porexpan spectral separability, and a costed drone-search trade study. |
| `spectral_and_drone_output.txt` | Full numeric output of the above. |
| `drone_procurement.py` | Buy-vs-contract case: thermal smear, night window, C2/C6 class limits, payback. |
| `drone_procurement_output.txt` | Full numeric output of the above. |
| `battery_logistics.py` | Pack count, charging channels, field power, and the used-airframe kit list. |
| `battery_logistics_output.txt` | Full numeric output of the above. |
| `thermal_resolution_check.py` | Diffraction/Q check on the thermal optics; detection vs identification. |
| `thermal_resolution_output.txt` | Full numeric output of the above. |
| `diy_drone_costing.py` | Purpose-built DIY drone: two variants, BOMs, physics, verdict. |
| `diy_drone_costing_output.txt` | Full numeric output of the above. |
| `night_sweeper.py` | Iterating the sweeper into a quiet night aircraft: acoustics, sensor ladder, BOM. |
| `night_sweeper_output.txt` | Full numeric output of the above. |
| `datalink_tradeoff.py` | Comms trade: Starlink/Iridium/4G/ELRS, anti-poacher precedent, Ukraine lessons. |
| `datalink_tradeoff_output.txt` | Full numeric output of the above. |
| `sensor_upgrade.py` | 1280-LWIR / 61 MP upgrade trade and full-sortie coverage arithmetic. |
| `sensor_upgrade_output.txt` | Full numeric output of the above. |
| `battery_chemistry.py` | Li-ion vs AA Ultimate Lithium (L91) primaries; beacon buses. |
| `battery_chemistry_output.txt` | Full numeric output of the above. |
| `day_vs_night.py` | Honest day/night recheck (day wins; night = hours + tie-breaker) and the X1C printed-parts manifest. |
| `day_vs_night_output.txt` | Full numeric output of the above. |
| `diy_radar.py` | 24 GHz FMCW radar bay for the reflector-equipped next flight; costs and physics. |
| `diy_radar_output.txt` | Full numeric output of the above. |
| `prop_and_speed.py` | Cruise-speed optimization (wind, sensors, regimes) and the folding-prop buy list. |
| `prop_and_speed_output.txt` | Full numeric output of the above. |
| `reflector_build_sheet.md` | One-page build sheet for the 70 g octahedral reflector cluster. |
| `lost_sweeper.py` | Can radar find a downed sweeper with a dead beacon? NLJD physics + the 19 g fix. |
| `lost_sweeper_output.txt` | Full numeric output of the above. |
| `boom_detectability.py` | The payload's 1.5 m CF boom as a radar/optical target, per channel. |
| `boom_detectability_output.txt` | Full numeric output of the above. |

## Workflow

```sh
pip install numpy scipy          # rasterio too, if you have GeoTIFFs

# 1. turn telemetry into a search box
python3 descent_reconstruction.py flight.csv --mass 3.0 --ground-alt 700 --out landing
#    -> landing.geojson  (nominal point, 50%/95% ellipses, square tasking AOI)

# 2. send the AOI with the emails in outreach_drafts.md

# 3. when imagery arrives, rank the candidates
python3 sphere_detector.py --post post_a.tif post_b.tif --pre baseline.tif \
        --gsd 0.30 --sun-az 148 --sun-elev 57 --out candidates
#    -> candidates.geojson  (open in QGIS over the imagery, work down the ranking)
```

`descent_reconstruction.py` pulls ERA5 winds from Open-Meteo automatically. If the flight
is too recent for ERA5, or you are offline, it falls back to using the balloon's **own
ascent as a wind sonde** — differentiating the ascent track recovers the wind profile it
flew through, which is often better than reanalysis anyway since it is the actual air the
payload moved through. You can also supply `--winds` manually.

The default `--cda` assumes the sphere descending as its own drag body (Cd 0.5). **If you
flew a parachute, pass the real drag area** — the ellipse depends on it strongly.

`sphere_detector.py` was validated on a synthetic 420 m scene at 30 cm seeded with 73
confusers (silage bales, limestone float, sheep, and bales appearing after the baseline).
The target ranked **first at 22.8 σ against a next-best of 3.6**.

## Headline results

**Detection is not the problem.** A 0.70 m sphere presents 0.385 m² of projected
area — 4.3 pixels at 30 cm. Against dry soil the post-atmosphere contrast is
Δρ ≈ 0.24, roughly 180× the sensor noise floor of Pléiades Neo.

**Curvature costs ~27%.** A sphere is not a flat panel. Integrating the lit-and-visible
cap gives an apparent reflectance of 0.53–0.59 over the projected footprint, against
a material albedo of 0.80.

**The shadow is the bigger target for most of the year.** At a 10:30 overpass in
December the shadow runs 1.65 m — about 10 pixels at 30 cm, versus 4.3 for the sphere.
It is also the feature that separates a sphere from flat white plastic. Prefer *low*
sun elevation, contrary to the usual instinct.

**Sensor choice:**

| Sensor | True cell | Δρ | Verdict |
| --- | --- | --- | --- |
| Pléiades Neo (Airbus) | 0.30 m | 0.238 | First choice |
| Pléiades 1A/1B (Airbus) | 0.70 m | 0.150 | Workable |
| SkySat (Planet) | 0.72 m | 0.142 | Workable |
| PlanetScope SuperDove | 3.70 m | 0.008 | Cannot detect |
| Sentinel-2 | 10.0 m | 0.001 | Cannot detect |

**The real bottleneck is discrimination, not detection.** Spanish farmland is full of
bright metre-scale objects — silage bales, limestone float, plastic sheeting, sheep.
Over 50 km²:

- 1 image, no baseline → ~5,600 candidates
- 2 images, no baseline → ~2,000 candidates
- 2 images + archive "before" → ~143 candidates

The archive baseline is what makes this tractable. Round silage bales are the residual
confuser, and separating a 1.2 m bale from a 0.70 m sphere requires 30 cm — which is
the strongest argument for Pléiades Neo over SkySat.

**Cost is set by order minimums, not area.** SkySat ~$15k tasking / ~$5k archive with a
25 km² polygon minimum; Pléiades Neo tasking practical minimum ~100 km². A 10 km² box
and a 100 km² box cost the same.

## Next flight

An X-band trihedral corner reflector of 16 cm inner leg (~37 g) is theoretically
sufficient for a +15 dB signal-to-clutter margin against a 1 m spotlight cell
(ICEYE, Capella, PAZ, TerraSAR-X). Build at 25–30 cm for margin; arrange eight as an
octahedral cluster so one corner always faces up regardless of resting attitude.
Sentinel-1 is free but needs 0.69 m / 660 g to beat its 100 m² cell.

Add a surviving satellite tracker and a 4 g RECCO reflector. The corner reflector is
elegant; the tracker is what actually recovers payloads.

### Our own radar — €550

Once the payload carries the printed reflector cluster, the sweeper grows a radar bay:
a COTS 24 GHz FMCW module (ISM, licence-free at 100 mW EIRP) + raw-ADC capture + printed
mount = **€550**, plus 40–60 h of FMCW DSP (the module IS the radar). Choosing our own
wavelength makes 15 cm printed legs return **13.7 m²** — noise-limited range 227 m,
6 dB over stubble clutter (+~10 dB integration), **~340 m swath, 12 km²/h** — double the
day camera, in any weather, at night, under hedges, with 0.75 m range resolution.
From-scratch/harmonic SDR builds (~€900, 3–5× hours) are not worth it next to a €5 RECCO.

**Complete next-flight recovery kit ~€875**: printed reflector ~€20/63 g (three interlocking foil-on-Depron plates — one metallized-mylar
caveat: ~100 nm Al is under one skin depth at 24 GHz, use real foil) + Iridium tracker on
4×AA ~€300 + RECCO €5 + radar bay €550 — three independent recovery channels.

## Buying a drone

**Buy the DJI Matrice 4T (~€9,500, ~€11,000 all-in).** One aircraft, RGB and thermal,
37.7 km²/day daylight and 5.3 km²/night thermal. Pays back against €1,500/day contracting
in 7 search days.

Two findings behind that:

- **Fixed wings do not smear the thermal target.** A ~10 ms microbolometer time constant
  gives 1.4 px of smear at 17 m/s on a 5.8 px target — 80% of peak contrast retained,
  against a starting margin of ~100σ. Smear is real and irrelevant.
- **The night window is ~7.4 h in August, not 1–2 h.** Porexpan settles to its cold offset
  within ~30 min of sunset; soil keeps drawing heat from depth all night. Allow 3 h after
  sunset for high-inertia objects to shed daytime heat and the anomaly is clean.

**The constraint that decides the aircraft is regulatory, not optical.** STS-02 BVLOS needs
a **C6**-class aircraft; multirotors carry **C2** and are VLOS-only (0.8 km² per pilot setup
against 12.6). A €48,000 fixed wing does not pay back on recovery alone — it needs other
survey work to carry it. For a large ellipse, contract the daylight sweep and fly your own
aircraft on the thermal follow-up.

Night flying requires a flashing green beacon and a current remote-pilot certificate — both
cheap, both with lead time.

### Batteries for continuous sorties

`charge / flight` is the right start but under-counts. A pack is unavailable for
*flight + cooldown + charge* while the aircraft relaunches every *flight + swap*:

```
packs    = ceil((flight + cool + charge) / (flight + swap)) x packs_per_flight
channels = ceil(packs x charge / (flight + swap))
```

**Three packs for a single-battery aircraft, six for a twin-pack one.** Charging
throughput is a separate constraint — every candidate needs a **second charging hub**.
Cooldown is the forgotten term: DJI hubs refuse packs above ~40 °C, which is 15–20 min
in an August field.

**Check you can use the third pack before buying a fourth.** Under VLOS the pilot works
a ~500 m bubble (0.79 km²), which an M3T clears in **10 minutes** — a quarter of one
battery. Under strict VLOS you are relocation-limited, not energy-limited. More batteries
only pay once you have more range; a second pilot leapfrogging setups is the cheapest way
to get it. The exception is the **night thermal sortie**, which re-flies a small known
core with no relocation — 10 sorties, 3 packs cycling, ~7.6 km² of core per August night.

**Field power** favours the small aircraft decisively: M3T draws ~118 W average (car
inverter), a twin-TB60 Matrice 300 needs ~716 W (a petrol generator running at 04:00).

### Thermal resolution — checked

LWIR at 10 µm against a 12 µm pixel and f/1.0 optics is where diffraction can make a
nominal GSD meaningless, so it was verified. **Q = λF/p = 0.83** for all three cameras:
the diffraction FWHM is 10.3 µm against a 12 µm pixel, so they are detector-limited and
the nominal GSD is honest. (The Airy null-to-null diameter is 24.4 µm ≈ 2 px, which looks
alarming, but resolution tracks the PSF core, not the first null.)

**Correction to an earlier claim.** The RGB analysis set six pixels across as the threshold
for confident identification; the thermal case was then waved through at 4.1 px without
noting the criterion had changed. The relaxation is defensible but the reason should have
been stated: **detection is contrast-limited, identification is resolution-limited.**

| Camera | GSD | px across | Detect | Identify |
| --- | --- | --- | --- | --- |
| M3T thermal (61°) | 17.2 cm | 4.1 | yes, ~100σ | no — cold blob only |
| M4T thermal (45°) | 12.1 cm | 5.8 | yes, ~100σ | marginal |
| H30T (1280², 45°) | 6.1 cm | 11.5 | yes, ~100σ | yes |

A 5 K anomaly against a 50 mK detector is unmistakable at 2 px across, so all of them
detect. None of the Mavic-class cameras identifies. **Thermal tells you where to walk;
RGB at 2–3 cm or a car journey tells you what you found.**

### DIY build — costed

A homebuilt has **no C-class marking, so STS-02 is unavailable at any price** — it flies
Open A3 (VLOS) or needs a full SORA. DIY cannot buy range, only sensors and redundancy.

- **Variant A "Sweeper" — €1,940 + ~40 h**: foam twin-boom (Believer class), ArduPilot,
  used 24 MP APS-C + 16 mm at 1 fps. 82 W cruise → 93 min sorties; 2.9 cm GSD = **24 px
  on the sphere** (ID threshold is 6); 9.2 km²/flight; 3 Li-ion packs to fly continuously.
  A day-one crash costs ~€1,470 and repairs with hot glue.
- **Variant B "Night core" — €4,390 + ~50 h**: 10-inch quad + Boson 640 (8.7 mm f/1.0,
  Q = 0.83, 4.2 px on target). The ≤9 Hz export-friendly Boson suffices (1 fps = ~90%
  forward overlap at 8 m/s). **67% of the cost is the sensor** — it is a €2,950 core with
  €1,440 of aircraft around it, and the used M3T (€7,380) delivers the same detector
  integrated and warrantied.

### Night sweeper iteration — €2,865, day and night, below ambient noise

Prior art: this class is proven (Air Shepherd — foam fixed wings + LWIR, night-only
anti-poaching, 6,000+ flight hours). Scope: "quiet" means acoustic courtesy; the legally
required green night beacon stays on.

- **Sensor ladder**: detection is contrast-limited, so even a €250 Lepton "sees" the
  5 K anomaly (36σ) but discriminates nothing at 1 m GSD. The reset: an **InfiRay
  Mini2-640 (~€900) matches Boson 640 geometry at 1/3 the price** — 16 cm GSD,
  4.4 px on target, 125σ.
- **The airframe swap is where quiet comes from**: prop noise ~ tip-speed^5.5. A 2.5 m
  foam motor-glider with a 14″ folding prop at 2,800 rpm = 52 m/s tip speed, 47 W cruise
  → **18 dBA at ground vs 32 dBA rural night ambient** (below ambient), and **164 min**
  endurance on the same 150 Wh pack. Climb-glide makes 73% of the sortie motor-off silent.
- **~17 km² of thermal per August night** — 4× any quad option — and the same airframe
  flies the APS-C day bay. Total €2,865 (€2,335 night-only), ~50–60 build hours.

Night thermal produces positions (125σ); identification at 4.4 px remains impossible —
the day bay or a car closes the loop. A3 rules bind at night as by day.

### Comms architecture — the van is the node

**Starlink Mini on the glider is disqualified by physics**: +1.1 kg on a 2.0 kg aircraft,
cruise power 47 → 98 W, endurance 164 → 78 min — to deliver bandwidth with no consumer,
since the matched filter runs post-flight. Starlink stays on the **ground vehicle** (Z2I
existing kit) where the fat pipe is actually needed.

**Iridium is wrong as telemetry, right as insurance**: 30 g / ~€260 lost-aircraft beacon —
the aircraft hunting a lost payload should not become a lost payload. The same module on
the next balloon flight would have made this whole project unnecessary.

**Precedent (Air Shepherd, 6,000 night hours)**: thin RF in the air, ops centre on wheels.
Aircraft: ELRS + Iridium beacon + onboard logging. Van: Starlink, power, decisions.

**Ukraine lessons (civilian-applicable)**: links fail — keep the sortie autonomous and the
downlink never load-bearing; GNSS is a service — enable ArduPilot dead reckoning; cheap-
and-many beats exquisite-and-one — carry a €275 built spare airframe; logistics set sortie
rate; the cheap FPV supply chain is wartime-scaled — buy spares while it is glutted.

**Decision: LTE (SIM card) is the primary telemetry.** Stack: Pixhawk → Pi Zero 2 W
(mavlink-router) → EC25/SIM7600 modem → WireGuard → GCS in the van. Data budget: 330 kbps
sustained (4 Hz MAVLink + 1 fps thermal preview) vs 5–20 Mbps rural uplink; 1.1 GB per
full August night. Use a **multi-carrier IoT roaming SIM** (attaches to the strongest of
Movistar/Orange/Vodafone), band-lock after the first flight (many-towers handover churn at
120 m). ELRS retained for launch/landing + failsafe; Iridium retained as beacon; SD card
means no link is ever load-bearing; MAVLink never raw on the internet (WireGuard only).
Gate before night ops: one daylight sortie on LTE alone with ELRS off.

Delta: +€605 (beacon, modem, spare airframe) +€70 (LTE-primary upgrade) →
night sweeper **€3,540** all-in.

### Cruise speed, optimized — and the props

13 m/s was an assumption; the sensors don't limit speed (all clear 20+ m/s: blur 0.35 px,
gapless overlap to 65–90 m/s, thermal smear 1.3 px). The optimum depends on the scarce
resource: **energy-limited → ~14 m/s calm** (avionics floor pushes it above best-L/D),
rising with wind (**add half the wind**: the broad energy optimum makes speeding up ~free
in km²/Wh but worth ~15% in km²/h); **time-limited → fast cruise 16–18 m/s** (+30–38%
km²/h). With 3 packs cycling, day sweeps are time-limited → fly fast; night thermal flies
the energy optimum. Noise never vetoes: even 20 m/s stays under the 32 dBA night ambient.
Survey lines fly **crosswind** for uniform crab and sidelap.

**Props (folding, Aeronaut CAM system, ~€135)**: 14×8 blades for the quiet night/energy
regime (~54 m/s tip), 14×11 for the fast day regime (~61 m/s tip), 42 mm spinner + yoke,
magnetic balancer — balance every pair; an unbalanced folder eats the thermal camera's
vibration budget. Two props, two missions, one aircraft.

### Correction: day is the primary search, not night

A fair challenge exposed drift in emphasis. Sensor for sensor, **day RGB wins**: 2.9 vs
15.8 cm GSD, 24 vs 4.4 px, identifies in-pass, 8.9 vs 5.9 km²/sortie, no terrain-floor
risk — and at 3 cm the discrimination problem doesn't exist. Night buys **hours** (~16 km²
thermal on top of ~54 km² daylight per August 24 h, airtime-limited) plus the one unique
thing: the 5 K cold-anomaly signature nothing agricultural imitates — the **tie-breaker**
for candidates day RGB can't call. Doctrine: day sweeps, night is second shift +
discriminator. Procurement re-orders: airframe + camera + comms first (~€2,640), thermal
core only if the ellipse exceeds ~two day-searches.

### Bambu X1C printed parts

CF-PETG bays/trays/mounts/grip, TPU isolation mount + skids, PETG hatches and all antenna
mounts (CF is conductive — keep it away from RF). Never props or the spar. ~€120 of bought
hardware → ~€25 of filament, field breakages become overnight reprints, and the printer
makes the next flight's octahedral corner-reflector frame.

### Sensor upgrade + sortie arithmetic

Full night sortie: ~158 min airborne (10 preflight + 1 launch/climb + 2 transit +
128 survey + 5 return/land), **5.9 km²/sortie**, ~16 km²/night over 2–3 sorties.
Day: 138 min, 8.9 km²/sortie.

**Upgrade call — revised: don't buy optics, descend.** The €900 640 core at **50 m AGL
gives 6.6 cm GSD = 10.6 px on the sphere** — past the identification threshold, same
certainty the €3,300 1280-core delivers from 120 m. An inspection (spiral down, low pass,
climb back) costs 1.1 min and 0.7 Wh, stays under the 32 dBA night ambient (~26 dBA), and
even at 3 false alarms/km² eats only 13% of the sortie. Fly: detect at 120 m → geotag →
finish lines → one 50 m inspection tour of the queue (the LTE preview makes the queue
live from the van). The first sortie *measures* the false-alarm density; buy the 1280
sharp core only if it comes in well above ~5/km². Safety: hard terrain floor, flat
llanura only, no night descents in barrancos. The 61 MP day camera (+€1,100,
13.0 km²/sortie) remains a separate coverage buy for a large ellipse.

**Verdict: ~€6,130 + ~90 h for both.** Build A (nothing touches its cost-per-km² if hours
are free, and it out-resolves everything in this repo); skip B and buy the used M3T —
unless the Boson has a second life on the balloon payloads, which is the one defensible
reason to build it.

**Li-ion vs AA Ultimate Lithium (L91):** the 220 W climb burst against L91's 2 A/cell
ceiling forces a 10S9P, 90-cell, 1,350 g pack (vs 600 g Li-ion). It would fly longer
(299 vs 159 min) but consumes €225 per sortie and burns the rechargeable budget by
sortie two — not for propulsion, ever. L91s belong on the beacons: an independent 2×AA
bus for the drone's Iridium (12 days duty-cycled — the crash that kills the main pack
can't kill the thing that reports it) and 4×AA on the next balloon tracker.
*Rechargeables spin the propeller, primaries keep the promise.* Pack inventory: no
purchase records in Gmail (ask Bravo/Falco; Drive needs an interactive approval); the
airframe absorbs any 3S–6S, 450–700 g pack without redesign.

**Buy the airframe used, buy the batteries new.** Cycle count and storage abuse are
invisible in a photograph; a tired pack sags under load and a swollen cell is a fire in
the car. A used M3T field kit totals ~€7,380 and pays back in 5 search days.

## Running it

```sh
pip install numpy scipy
python3 sphere_detectability.py
```

## Model assumptions

Lambertian sphere, nadir viewing, clear-atmosphere contrast attenuation 0.82, matched
filter across bright and shadow lobes against a difference-image clutter floor.
Confuser densities are order-of-magnitude field estimates, not measurements — the
ranking of strategies is robust, the absolute counts are not. Prices are indicative,
from public reseller listings as of August 2026, not quotes.
