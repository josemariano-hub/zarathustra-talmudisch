# Flight 2 ground truth — what the investigation report changes

Source: *Loss of HAB Flight 2 — Investigation Report* (Villadiego, Burgos; launched
12 Aug 2026; Loonatec HAB Pilot, Iridium 9603A). This file is the digest of that report
into the search plan — every downstream document now uses these numbers.

## The facts that feed the search

| Item | Value |
| --- | --- |
| Launch | Villadiego, Burgos — 42.52471 N, 3.97540 W — 12 Aug 2026, 18:23 UTC |
| Last packet | 19:22:11 UTC, **42.5732 N, 3.8484 W, 22,205 m**, still climbing +6.5 m/s |
| Termination | Venter watchdog burn-wire ~19:32 UTC at ~25.8 km (near-certain; three armed paths) |
| Landing | ~21:12 UTC (23:12 local), **after dark**, ~2.4 m/s under canopy |
| Descending mass | 2.52 kg under a Fruity Chutes Iris Ultra SUL-84 (CdA 7.87 m²) |
| **Search Zone A** | centre **42.66265 N, 3.85740 W** — 50%: r=3.5 km (38 km²); 90%: r=6.7 km (139 km²) |
| Zone B (outer bound only) | 42.67460 N, 4.10652 W — needs BOTH termination paths to fail; do not search first |
| Radio route | **Permanently closed** — battery flat within hours of landing; 5 days of silence confirm |
| On the ground since | 12 Aug — imagery from any pass after 21:00 UTC that day is valid |

Cross-check run on their numbers: 2.52 kg at CdA 7.87 m² gives 2.3–2.4 m/s terminal at
site altitude — matches the report's touchdown figure. The reconstruction is
self-consistent; no need to re-run ours unless the raw CSV surfaces.

## The two things that change our analysis

### 1. The parachute stayed attached — the canopy is the target now

Everything before this was designed around a 0.70 m sphere at 2.3 px. The **2.13 m
canopy** is the object to search for:

| Sensor | GSD | Sphere px | **Canopy px** | Verdict change |
| --- | --- | --- | --- | --- |
| Pléiades Neo | 0.30 m | 2.3 | **7.1** | detection → easy; **discrimination now works too** |
| Pléiades | 0.50 m | 1.4 | **4.3** | was marginal → now usable |
| SkySat (true cell) | 0.72 m | ~1 | **3.0** | was "sees a blob" → now a real candidate sensor |
| PlanetScope | 3 m | — | 0.7 | still no |

The discrimination problem inverts: a silage bale is 1.2–1.5 m, the canopy is 2.13 m —
the size gate now rejects bales *from above*, and the canopy is fabric draped over
stubble, not a compact 3-D object with a hard shadow. If the canopy has any colour
(**unconfirmed — the one datum to nail down before tasking; the report flags it too**),
an RGB colour gate ends the bale problem outright. The sphere + boom + Insta360 sit
within metres of the canopy on the train — find the canopy, walk the line.

For the sweeper the change is bigger still: at 120 m AGL the day camera puts **~90 px**
across the canopy. False-alarm density collapses; descend-to-inspect passes become
confirmations, not identifications.

### 2. The AOI is real, small, and Zone A is a one-day sweep

- **Zone A 50% (38 km²)**: under one sweeper day (51 km²/day VLOS, two-camera bay) or
  one M4T day. Satellite tasking box: 42.63156–42.69375 N, 3.89968–3.81511 W.
- **Zone A 90% (139 km²)**: ~3 sweeper days. Box: 42.60287–42.72243 N, 3.93869–3.77610 W.
- Zone B only if A is exhausted — it requires both termination systems to have failed.
- Terrain: páramo farmland ~18 km NE of the Villadiego launch site — Amarok country.

## Small print

- The payload has been down since 12 Aug — six days of harvest traffic already; the
  ploughing clock in the outreach emails is real, not rhetorical.
- The Venter strobe was armed but its batteries are long flat: no night-light shortcut.
- This flight carried **no corner reflector** — the 24 GHz radar's only channel on this
  search is the CF boom glint. The reflector cluster remains a next-flight fix.
- Report line worth honouring as-is: "The parachute is the target, not the payload."
