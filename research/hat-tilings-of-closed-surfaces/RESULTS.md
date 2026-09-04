# Spheres and tori tileable by the hat monotile

All statements below are derived from the geometry, then checked numerically by the
scripts in `code/`. Nothing here is quoted from memory: the hat itself is re-derived
from the kite lattice (`enumerate_hat.py`, `tileab.py`, `patch.py`) and only then
compared against Kaplan's reference implementation.

## 0. Identifying the hat from first principles

The kite lattice (deltoidal trihexagonal tiling) is built with exact integer
coordinates; kite edges have exactly two lengths, `1` (centroid–midpoint) and
`√3` (vertex–midpoint).

There are **873 free octakites**. Of these, **23** have a simple 14-gon boundary
with 6 long and 8 short edges — the Tile(1,√3) signature. Three of those survive
the defining test of the Tile(a,b) continuum,

> the polygon still closes when `a` and `b` are rescaled independently
> ⟺ Σ(unit vectors of a-edges) = 0 **and** Σ(unit vectors of b-edges) = 0,

and exactly one of the three can cover even a small disc of kites. That one is the hat.

```
interior angles v0..v13 : 90 120 270 120 180 120 90 240 90 240 90 120 270 120   (Σ = 2160°)
edge lengths    e0..e13 : b  b  a  a  a  a  b  b  a  a  b  b  a  a      a = 1, b = √3
area                    : 8√3 = 13.856 a²
perimeter               : 8a + 6b = 18.392 a
```

As a 13-gon: 6 edges of √3, 6 of length 1, one of length 2 (the two `a` edges
flanking the 180° vertex).

Two independent checks.

*Against the reference implementation.* `hat_outline` in `geometry.js` of
[isohedral/hatviz](https://github.com/isohedral/hatviz) (Kaplan's P5 sketch for the
paper) reads

```js
const hat_outline = [
    hexPt(0, 0), hexPt(-1,-1), hexPt(0,-2), hexPt(2,-2),
    hexPt(2,-1), hexPt(4,-2), hexPt(5,-1), hexPt(4, 0),
    hexPt(3, 0), hexPt(2, 2), hexPt(0, 3), hexPt(0, 2),
    hexPt(-1, 2) ];                       // hexPt(x,y) = (x + y/2, (√3/2)y)
```

Its boundary word, normalised to short edge = 1, is a cyclic rotation of the mirror
image of the one above — the same tile, opposite chirality, because free-polyform
enumeration canonicalises up to reflection. Area 13.856406 = 8√3 on both sides.
A copy sits in `code/reference_geometry.js`.

*Against a real tiling.* A 28-hat patch tiles a disc of 150 kites with **every
interior vertex at exactly 360°** (2, 3 or 4 hat corners meeting; mostly 2).
See `patch.png`.

## 1. Flat tori: none. Not one.

A tiling of the flat torus `R²/Λ` lifts to a `Λ`-periodic tiling of the plane,
and conversely. So

> a tile tiles some flat torus ⟺ it admits a periodic tiling of the plane.

The hat is aperiodic, so **the family of flat tori tileable by the hat is empty**.
This is not a property of the hat specifically — it is what "aperiodic monotile"
means. It holds for every Tile(a,b) with a/b ∉ {0, 1, ∞} and for the Spectre.

Checked directly for all index-D sublattices, D = 4, 8, 12, 16 (3, 6, 9 and 12
tiles per fundamental domain), all 7+15+28+45 Hermite normal forms: no tiling
(`torus.py`). The positive control — the 6-kite hexagon — tiles immediately.

So every hat-tiled torus carries **cone points**.

## 2. The curvature quantum is 60°, not 30°

Every hat angle is a multiple of 30°, which invites the conclusion that cone
angles come in 30° steps. That is wrong. The edge lengths forbid half of them.

The hat presents nine corner types (angle; the two arms in CCW order):

```
 90 (a,b)   120 (a,a)   180 (a,a)   240 (a,a)   270 (a,b)
 90 (b,a)   120 (b,b)               240 (b,b)   270 (b,a)
```

A corner of 90° or 270° always joins one short arm to one long arm: it **switches**
edge class. Corners of 120°, 180°, 240° preserve it. Going once around a vertex the
class must return to its start, so the number `s` of switching corners is **even**.
Modulo 60°, `90 ≡ 270 ≡ 30` and `120 ≡ 180 ≡ 240 ≡ 0`, hence

> **θ ≡ 30s ≡ 0 (mod 60°)** for every vertex of every hat tiling of every surface.

Exhaustive search over edge-matched cyclic corner sequences confirms it — the
realizable cone angles are exactly

```
120  180  240  300  360  420  480  540  600  660  720 ...   (gcd = 60°)
```

The argument uses only the angle sequence and the a/b labelling, both constant along
the Tile(a,b) continuum, so **the 60° quantum holds for the whole hat family** —
hat, turtle, everything with a ≠ b.

Define the **disclination charge** `q = (360° − θ)/60 ∈ Z`.

## 3. What this forces

For F hats glued edge-to-edge on a closed surface: `E = 7F`, and
`χ = V − 7F + F`, so `V = 6F + χ`. Gauss–Bonnet gives `Σ(360° − θ_v) = 360°·χ`, i.e.

> **Σ q_v = 6χ**

| surface | χ | total charge Σq | minimum cone points |
|---|---|---|---|
| sphere | 2 | **+12** | 3 (max charge per point is 4, at θ = 120°) |
| torus | 0 | **0** | 2 (flat is impossible, so ≥1 positive and ≥1 negative) |
| genus 2 | −2 | −12 | — |
| Klein bottle | 0 | 0 | 2 |

**Total charge +12 on a sphere is exactly the fullerene/geodesic-dome number.** If
you insist that every vertex be flat except for the mildest possible defects
(θ = 300°, q = +1), a hat-tiled sphere needs **exactly twelve 60° disclinations** —
the same count and the same magnitude as the twelve pentagons in a truncated
icosahedron. The hat buys aperiodicity. It does not buy finer curvature resolution.

## 4. Existence: what actually closes up

### One tile is enough
Gluing the hat's own 14 edges in 7 length-matched pairs (6 long → 3 pairs,
8 short → 4 pairs; 1575 pairings × 2⁷ orientations) yields:

```
orientable   χ=+2 SPHERE       30 gluings,  18 cone-angle spectra (8 cone points each)
orientable   χ= 0 TORUS       295 gluings, 119 spectra            (6 cone points each)
orientable   χ=-2 genus 2     780 gluings, 165 spectra
orientable   χ=-4 genus 3     470 gluings,  17 spectra
non-orientable χ=+1 RP²       324 gluings   /  χ=0 KLEIN BOTTLE  1859 gluings
                              ... up to non-orientable genus 7
```

Every cone angle in every one of these spectra is a multiple of 60° — an
independent confirmation of §2. Example tori (edge pairing given):

```
θ = 240 240 360 360 480 480   q = +2 +2 0 0 −2 −2   (2,9)(3,8)(4,12)(5,13)(0,11)(1,10)(6,7)
θ = 240 360 360 360 360 480   q = +2  0 0 0  0 −2   (2,9)(3,8)(4,13)(5,12)(0,7)(1,10)(6,11)
```

No single-hat sphere has all cone angles below 360°, so none of the 18 is a convex
polyhedron in the sense of Alexandrov.

### Infinite families, at every even tile count
For any hat patch P:

* P simply connected → the **double** of P is a hat-tiled **sphere** with 2|P| tiles.
* P an annulus → the double is a hat-tiled **torus** with 2|P| tiles.

Verified end to end: a clean 25-hat disc doubles to a 50-hat sphere with
Σ defects = +720° and Σq = +12; the same patch minus one interior hat doubles to a
48-hat torus with Σ defects = 0 and Σq = 0. Curvature sits on the seam; the two
interiors are ordinary plane hat tiling.

These are honest but blunt: the seam carries charges up to ±3 per vertex. **Whether a
hat-tiled sphere exists whose only defects are twelve q = +1 points is not settled by
this computation.** The charge bookkeeping is exact and permits it; construction is open.

### Convex regions
Hats do not tile the equilateral triangle of side 4 (48 kites, 6 hats) or side 8
(192 kites, 24 hats) — exhaustive. Convex hat patches, and hence convex doubled
polyhedra, look unavailable.

## 5. The Spectre is the better tile for curved surfaces

Tile(1,1) has all 14 edges congruent, so the a/b parity argument evaporates and any
edge matches any edge. Re-running the vertex enumeration with a single edge class:

```
realizable θ : 90 120 180 210 240 270 300 330 360 390 420 ...   gcd = 30°
```

**Quantum 30°, charge to close a sphere = 24.** The Spectre's edges are a single
curve carried by all 14 sides and matching itself, so its combinatorics is
Tile(1,1)'s and it inherits the 30° quantum — twice the angular resolution of the
hat, and it is chiral, so no mirrored panels are needed. For panelling a dome, the
Spectre dominates the hat on both counts. (The edge-decoration claim is inferred
from the Spectre's self-matching edge design, not verified here.)

## 6. The third option: keep the vertices flat and curve the tiles

Cone points are not the only way. Euler allows a sphere tiled by F hat-combinatorics
panels with **every** vertex at exactly 360°:

```
V = 6F + 2,  E = 7F,  Σ angles = 2160F   →   360V − 2160F = 720° = 4π  ✓ for every F
```

The 720° then lives in the panels as spherical excess, `A/R²` per tile, and the panels
must vary slightly across the surface. The Tile(a,b) continuum is the natural vehicle:
`a` and `b` can be graded smoothly across a surface like a conformal factor, so a
curved shell can be built from hat-family panels of gradually varying proportion with
no disclination anywhere. For a sphere of radius R and short edge a,

```
N = 4πR² / (8√3 a²) = πR² / (2√3 a²)          per-tile spherical excess = 8√3 a²/R²
```

e.g. R = 5 m, a = 0.25 m → N ≈ 1814 panels, excess ≈ 0.035 rad ≈ 2.0° per tile.
This is a design direction, not a verified construction.

## Files
`kites.py` lattice · `enumerate_hat.py` octakite enumeration · `tileab.py` Tile(a,b) test ·
`patch.py` corona test · `torus.py` flat-torus search · `glue1.py` single-tile gluings ·
`vertices.py`/`quantum.py` cone-angle spectrum · `patches.py`/`double.py`/`double2.py`
doubling constructions · `render*.py`, `png.py` figures.
