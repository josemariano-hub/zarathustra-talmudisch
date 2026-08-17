# Octahedral corner-reflector cluster — build sheet

**Purpose:** passive radar target for balloon payloads (and one embedded corner for the
sweeper itself). Makes any styrofoam payload a ~14 m² radar echo at 24 GHz with no power,
no electronics, and no expiry date. Print the frame on the X1C; build in an evening.

## Performance

| Radar | Band | RCS (15 cm legs) | Note |
| --- | --- | --- | --- |
| Our 24 GHz FMCW bay | K | **13.7 m²** | design case — 227 m detection range |
| ICEYE / Capella / PAZ spotlight | X (9.6 GHz) | 2.2 m² | ~13 dB over 1 m² cell clutter — usable |
| Sentinel-1 | C | 0.6 m² | not useful; ignore |

One cluster serves both the DIY radar and, marginally, commercial X-band tasking.

## Bill of materials (~€20, ~70 g)

| Item | Qty | Mass |
| --- | --- | --- |
| Depron 3 mm sheet, cut to 3 × (300 × 300 mm) | 3 plates | 30 g |
| Kitchen aluminium foil, 12 µm, **both faces of every plate** | ~0.6 m² | 17 g |
| Spray adhesive (3M 77 class) | thin coat | ~3 g |
| X1C-printed slot-joint frame set + lanyard lug (PETG, **not CF**) | 1 set | 25 g |

Foil goes on *both* faces because the octahedral geometry uses both sides of every
plate — the 8 corner cavities between them are the reflectors.

## Geometry

Three identical 300 × 300 mm plates (2a × 2a with a = 150 mm), interlocked mutually
orthogonal through half-depth slots:

- Plate A: one slot, 150 mm long × 3 mm wide, from mid-edge to centre.
- Plate B: same slot; A and B interlock into a cross (+).
- Plate C: two slots from opposite edges to centre; slides over the A–B cross.
- Printed corner clips seat on the 12 outer edges and pull the assembly square.

Result: 8 trihedral corners, one always facing up-and-out at any resting attitude.

## Tolerances — the two that matter

1. **Flatness ≤ 0.8 mm** (λ/16 at 24 GHz) over each plate. The Depron guarantees this
   if stored flat; check with a straightedge after foiling.
2. **Orthogonality ≤ ±1°** between plates. Beyond that, RCS collapses fast — this is
   the printed frame's whole job. Check with a machinist square at the centre joint.

Smooth the foil with a felt edge; wrinkles under ~1 mm depth are harmless.

## Do not

- Substitute metallized mylar / space blanket: its ~100 nm aluminium layer is under one
  skin depth (0.53 µm at 24 GHz) — visually shiny, electrically poor. **Real foil only.**
- Use CF filament in the frame near the plate faces (conductive, detunes edges).
- Paint the foil. Bare foil; UV does not care and neither does the radar.

## Variants

| Variant | Legs | RCS @24 GHz | Range | Mass |
| --- | --- | --- | --- | --- |
| Standard (this sheet) | 15 cm | 13.7 m² | 227 m | ~70 g |
| Compact | 10 cm | 2.7 m² | 152 m | ~42 g |
| Sweeper self-tag (single corner, embedded in fuselage) | 8 cm | 1.1 m² | ~120 m | ~10 g |

## Acceptance test

Stand the cluster in a field; fly the radar bay past at 150–200 m offset and 120 m AGL.
A clean, stable point return ≥10 dB over the surrounding clutter in the range-FFT is a
pass. Rotate the cluster arbitrarily and repeat — the return must persist within ~3 dB.
