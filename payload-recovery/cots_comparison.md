# The COTS mirror — closest full commercial product to the sweeper

**Question:** what is the closest commercial off-the-shelf *complete* product to our
sweeper spec (3.4 kg hand-launch foam fixed wing, two-camera RGB day bay + swappable
InfiRay 640 thermal, **LTE-primary telemetry**, independent Iridium beacon, 24 GHz
radar bay, climb-glide quiet doctrine, ~€3.5k DIY)?

**Answer: the Delair UX11 is the architectural twin, the AgEagle eBee X is the
doctrinal twin, and a Believer-class RTF mapping package is the genetic and price
twin.** No COTS product matches all of it — and one gap runs the other way: COTS can
sell you a C6 class label, which a homebuilt can never have.

## The lineup

| Product | MTOM | Launch | Sensors | Comms | C-class | Street price | What it lacks vs our spec |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Delair UX11** | 1.5 kg | hand | 21.4 MP global-shutter, PPK | **2.4 GHz + 3G/4G LTE C2** | C6 variant sold | ~€15–20k (indicative) | thermal, radar, Iridium, price |
| **AgEagle eBee X** + S.O.D.A. / Duet T | 1.6 kg | hand | swappable RGB / RGB+thermal bays | 2.4 GHz (LTE via add-on) | **C6 since Oct 2023** | ~€15–38k w/ payloads | radar, Iridium bus, quiet doctrine, price |
| **Believer RTF mapping package** (MakeFlyEasy / Foxtech) | 3.5–5.5 kg | hand/bungee | Sony A-series or dual oblique | ELRS/RFD900; LTE if you add it | none | ~€3–6k | thermal, radar, Iridium — you integrate them, which is our DIY |
| **Quantum Trinity Pro** | 5 kg | VTOL | swappable, incl. oblique 3-view | LTE option, iBase PPK | none (SORA route) | ~€48k (indicative) | radar, price ×13; it IS our 5 kg 3-camera BVLOS variant, commercialized |
| (Event 38 E400) | 6 kg VTOL | VTOL | Sony, ArduPilot-native | RFD900/LTE options | none | ~$20k | the open-source cousin, US-centric |
| (Parrot Disco) | 0.75 kg | hand | fixed FPV cam | Wi-Fi | — | dead (2019) | the consumer ancestor; donor airframes still circulate |

Prices are indicative street/quote levels, August 2026; survey-drone pricing is
quote-driven and moves.

## Why each twin is the twin

- **UX11 — architecture.** A 1.5 kg hand-launched foam survey wing whose signature
  feature is flying C2 and telemetry **over the cellular network**. Our LTE-primary
  decision (Pi + EC25 + WireGuard) independently reinvented Delair's headline
  capability. It even ships as a C6-labelled variant now. What it can't do: carry our
  thermal, our radar bay, or our beacon bus — the payload is sealed, one camera,
  theirs.
- **eBee X — doctrine.** Hand-launch foam, field-swappable payload bays (S.O.D.A. RGB,
  Duet T RGB+thermal — exactly our two-bay concept), rated to ~90 min, and the first
  aircraft family to earn the **EASA C6 label** — BVLOS over a controlled ground area
  with airspace observers, legal in the EU since 1 Jan 2024. This is the one thing on
  the table money can buy and a homebuilt cannot: STS-02 eligibility.
- **Believer RTF — genetics and price.** The same airframe family our DIY design
  started from, sold pre-integrated with ArduPilot and a Sony sensor by Chinese
  integrators at €3–6k. Buying one and adding our thermal + radar + beacon is not an
  alternative to the DIY plan — it *is* the DIY plan with the airframe labour bought
  out. This is the honest answer to "closest full product at our price."
- **Trinity Pro — the scaled variant.** Our co-optimized frontier said the per-euro
  BVLOS peak is a ~5 kg aircraft flying a 3-camera bay; Quantum sells exactly that
  aircraft for ~€48k. The frontier and the market agree on the shape — the market just
  charges 13× for it.

## What no COTS product has (the gap analysis)

1. **The 24 GHz radar bay.** No commercial survey wing carries radar. The boom-glint /
   corner-reflector channel — the thing that makes the *next* recovery a non-event —
   exists only in our build.
2. **The independent L91 Iridium beacon bus.** COTS trackers exist, but no survey
   drone ships with a self-finding channel on its own primary-cell bus.
3. **The acoustic doctrine.** Climb-glide at 18 dBA is an operating procedure plus a
   prop choice, not a product feature anyone sells.
4. **The price.** €3.5k versus €15–48k. The 4–13× premium buys integration, warranty,
   support, and (eBee/UX11) the C-class label — not capability our mission needs.

## Verdict

- **Closest single product:** the **Delair UX11** — it is our comms architecture and
  airframe class in a sealed commercial shell.
- **Closest to what we'd actually buy:** a **Believer-class RTF package**, because it
  is our build minus the parts that make it a recovery aircraft.
- **The pivot condition:** if legal BVLOS ever matters more than the radar channel —
  say the AOI grows past what VLOS setups can sweep — stop building and buy an
  **eBee X with Duet T**: the C6 label is the one spec line that cannot be
  homebuilt at any price.
