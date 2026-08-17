# Payload recovery — 0.70 m white porexpan sphere, central Spain

> **Note on placement.** This directory is unrelated to the Zarathustra edition that
> occupies the rest of this repository. It was committed here because the working
> branch for this task pointed at this repo. Move it to a proper home when convenient.

Feasibility analysis for locating a 3 kg high-altitude balloon payload — a 0.70 m
diameter white expanded-polystyrene sphere — using commercial high-resolution
satellite imagery over the Spanish Meseta.

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
