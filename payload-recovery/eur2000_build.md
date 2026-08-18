# The €2,000 build — what that budget actually buys

**Verdict up front: €2,000 buys the machine that finishes this search.** The mission
changed under the budget: the target is now a 2.13 m **orange** canopy in a 38 km²
Zone A, which is a daylight-RGB problem with a colour gate — exactly what the
cheapest end of the design does best. Everything the full €3,540 spec adds beyond
€2,000 was for harder targets (white sphere alone, night ops, reflector radar) that
this recovery no longer needs.

## The build (canopy hunter — day RGB sweeper, LTE-primary)

| Item | € |
| --- | --- |
| Foam twin-boom airframe kit (Believer 1960 class) | 340 |
| Pixhawk-class autopilot + M10 GPS + compass | 270 |
| Motors ×2, ESCs, props, hand-launch spares | 130 |
| ELRS control link (launch/land + failsafe) | 70 |
| **LTE node: Pi Zero 2 W + SIM7600 hat + multi-carrier IoT SIM** (primary telemetry + live image preview — replaces the 868 MHz telemetry radio) | 80 |
| Used 24 MP APS-C body (a6000 class) | 350 |
| 16 mm f/2.8 pancake prime, used | 120 |
| Intervalometer trigger + hard mount | 60 |
| Li-ion packs ×3 (4S 10.4 Ah, 18650 build — nothing in the Z2I stock flies) | 330 |
| Dual-channel Li-ion charger (Amarok DC-DC feeds it in the field) | 90 |
| Sweeper self-recovery: RECCO tab + printed 10 cm corner + X1C-printed bays, harness, spares | 140 |
| **TOTAL** | **1,980** |

~40 build-hours. X1C prints the camera bay, mounts and skids (~€25 of filament,
already counted). Legal envelope: Open A3, VLOS, 120 m — the whole plan assumes it.

## What it delivers against Zone A

- 2.9 cm GSD at 120 m → the canopy is **~70–90 px across**, the sphere 24 px, the
  boom a clear line. Identification is trivial; a hue threshold (orange, ≥1 m) is
  the whole detector — false alarms near zero in an August harvest landscape.
- 93-minute sorties, ~38 km²/day VLOS with Amarok relocations:
  **Zone A 50% (38 km²) ≈ one field day. Zone A 90% (139 km²) ≈ 4 days.**
- Live LTE preview means the truck sees candidates in flight and can walk to the
  find the same day.

## What the missing €1,540 was buying — and why each cut is safe now

| Cut | € | Why it's safe for THIS search |
| --- | --- | --- |
| Second camera (two-bay, 330 m swath) | ~530 | +34% coverage — turns 4 days into 3. Nice, not necessary. **First re-add if budget appears.** |
| InfiRay Mini2-640 thermal | ~900 | Day-primary was already the honest verdict; an orange canopy needs daylight, not ΔT. |
| 24 GHz radar bay | ~550 | The CF boom IS a real target for it (4.6 m² broadside, one ~65-chirp flash per pass — established doctrine says worth flying). It's cut here on redundancy, not weakness: the orange canopy hands the day camera a *deterministic* detection, so the radar's *stochastic* boom flash only earns its €550 if the canopy is hidden (hedge, ditch, dragged). It is the first re-add if Zone A's open fields come up empty. |
| Iridium sweeper beacon | ~300 | Under VLOS + LTE last-fix + RECCO/corner tab, a lost sweeper is findable without it. |
| Aeronaut CAM prop pair set | ~75 | Stock props cost ~2–3% efficiency. Accept it. |

## Priority order if the budget moves

1. **€2,000 (this brief):** single-camera day sweeper — completes Zone A 90% in ~4 days.
2. **+€530:** second camera bay → 51 km²/day, Zone A 90% in ~3 days.
3. **+€75:** proper folding props (worth it once the airframe is proven).
4. **+€550 radar bay:** the escalation move if the open-field sweep finds nothing —
   the boom's 4.6 m² glint sees through hedges, canopy folds and partial cover that
   defeat the camera, and the same bay serves every future reflector-equipped flight.
5. **+€900 thermal:** last — an orange canopy is a daylight target; thermal is for
   searches this one no longer is.

The other €2,000 option — putting it toward a used Mavic 3 Thermal (~€6,000) — buys
a third of a drone. Toward a SkySat tasking it might buy imagery once, with no
aircraft left over. The DIY sweeper is the only version of €2,000 that covers all of
Zone A **and** survives as Z2I's permanent recovery asset.
