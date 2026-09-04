# Explicit hat tilings of a sphere and a torus

Two closed surfaces, each tiled by copies of the hat monotile, given as exact
edge gluings in `GLUINGS.txt` and drawn as planar nets. Everything here is
produced and checked by the code in `code/`; the hat itself is the one derived
in `RESULTS.md` and confirmed against Kaplan's `hat_outline`.

## The sphere — 6 hats

```
chi = +2,  38 vertices,  42 glued edge pairs
cone angles      240 deg x 6,  360 deg x 32
total defect     +720 deg   (Gauss-Bonnet requires +720)
```

Six cone points of 240°, each a 120° disclination, and thirty-two vertices that
are perfectly flat. Every cone angle is a multiple of 120°, so the tiling is
kite-compatible: the tiles meet as they do in a plane hat tiling.

Net: `net_sphere6.png`. Six hats laid out edge-to-edge in the kite lattice —
that patch is an ordinary piece of hat tiling — with the 37 remaining
identifications marked in colour. Fold and glue.

3D: `sphere6_a.png` is a genuine isometric realization of the cone metric,
max edge error 0.003%. It is not the convex one. Alexandrov's theorem
guarantees a convex realization exists and is unique (all cone angles ≤ 2π);
volume-maximising relaxation did not reach it, so the picture is a valid but
non-convex embedding of the right surface. The convex realization has exactly
6 corners and, being 6-vertex and triangulated, octahedral combinatorics.

## The torus — 3 hats

```
chi = 0,  18 vertices,  21 glued edge pairs
cone angles      120,120, 180, 240,240, 300,300, 360 x4, 420,420, 480,480, 540, 600,600
total defect     0 deg   (Gauss-Bonnet requires 0)
```

Net: `net_torus3.png`. 3D: `torus3_a.png` is an exact isometric immersion
(edge error 0.0000%) but it self-intersects; cone angles up to 600° cannot be
embedded tidily in R³ without a self-avoidance term the relaxation does not have.

This gluing is **not** kite-compatible: it has cone angles of 180, 300, 420 and
540, which are multiples of 60 but not of 120. The tiles are genuine hats and
the surface is a genuine flat cone torus, but along some edges a hat's V corner
is identified with another hat's M corner, so the kite lattice does not continue
across the seam and the tiling does not look locally like a plane hat tiling.
A kite-compatible torus was not found for N = 3, 4 within the search budget.

## Why there is no flat torus, and why the sphere needs exactly six 240° points

Three separate constraints stack up.

**1. Edge-class parity — quantum 60°.** Corners of 90° and 270° always join a
short edge to a long one; 120°, 180° and 240° preserve the class. Going once
around a vertex the class must return to its start, so an even number of
switching corners meet, and every cone angle is a multiple of 60°.

**2. Point type — quantum 120°.** Locate each hat corner in the kite lattice:

```
   corners at triangle vertices V : 120, 240      (2 or 4 kites of 60 deg)
   corners at centroids        G : 120, 240      (1 or 2 kites of 120 deg)
   corners at edge midpoints   M : 90, 180, 270  (1, 2 or 3 kites of 90 deg)
```

At V and G every hat corner is a multiple of 120°. At M every corner is a
multiple of 90°, and with constraint 1 that forces a multiple of 180°. So a
tiling that carries the kite lattice has **curvature quantum 120°**.

**3. Gauss-Bonnet.** Total defect is 360·chi.

Sphere: 720/120 = **six** 120° disclinations, i.e. six cone points of 240°.
That is the octahedral count, not the icosahedral one. The fullerene pattern —
twelve 60° disclinations, twelve pentagons — is unavailable to the hat, because
a 300° cone point would need V corners summing to 300 out of {120, 240}.

Torus: total defect 0, but not all zero, since all-flat means a flat torus and
a flat torus lifts to a periodic plane tiling, which an aperiodic monotile has
none of. So a hat torus needs at least one positive and one negative cone point.

Checked directly (`cone.py`), covering the neighbourhood of a cone point of
angle 60d at a lattice vertex:

```
 d      3     4     5     6     7     8     9    10
 angle 180   240   300   360   420   480   540   600
       no   YES    no   YES    no   YES    no   YES
```

Exactly the even degrees, exactly as the point-type argument predicts.

## Surfaces that are ruled out

Exhaustive searches, not timeouts — the solver returned with the tree closed.

| surface | kites | hats | tileable |
|---|---|---|---|
| flat torus, triangular lattice mod 4 | 96 | 12 | no |
| flat torus, triangular lattice mod 6 | 216 | 27 | no |
| icosahedron subdivided, n=2 (twelve 300° points) | 240 | 30 | no |
| icosahedron subdivided, n=4 | 960 | 120 | no |
| octahedron subdivided, n=2 (six 240° points) | 96 | 12 | no |
| octahedron subdivided, n=3 | 216 | 27 | no |
| octahedron subdivided, n=4 | 384 | 48 | no |
| octahedron subdivided, n=5 | 600 | 75 | no |
| octahedron subdivided, n=6 | 864 | 108 | no |

The icosahedral cases die on the parity law above. The octahedral ones have the
right disclination pattern — six 240° cone points, total charge 6 — and still
fail out to 108 hats. Putting the six cone points at the corners of a *regular*
octahedron is too rigid a constraint; the 6-hat sphere above carries the same
charge with the cone points placed irregularly, and that one exists.

## The open question: a kite-compatible torus

The sphere above is kite-compatible; the 3-hat torus is not. A kite-compatible
hat torus needs cone angles that are multiples of 120° summing to zero defect,
so at minimum one 240° point (charge +1) and one 480° point (charge -1). At
lattice vertices those are degrees 4 and 8, and each is individually fine — the
cone table above says both are coverable. Whether they can coexist on a torus
carrying a hat tiling is not settled here:

* gluing search (`glue_search.py`, mod-120 closure constraint) found none for
  N = 3..7. These are randomized restarts under a node cap, so they are search
  failures, not proofs.
* diagonal flips starting from the flat torus never reach an all-even degree
  profile other than the flat one: a single flip gives 5,5,7,7, and the only
  second flip restoring even degrees is the undo. 4000 random flip walks and a
  greedy parity-descent search on m = 4 and 6 found nothing else.
* a variable-width cylinder closed into a torus does produce cone tori, but the
  curvature spreads into 5s and 7s rather than concentrating into a 4 and an 8.

So the construction of an even-degree cone torus is the missing piece, not the
tiling search on top of it.

Positive control for the machinery: the same solver covers a disc of the plane
(cone angle 360°) without difficulty, and reproduces the known impossibility of
every flat torus.

## Files
`complex.py` surfaces as equilateral triangulations, kite complexes, hat
placements, exact cover · `cone.py` cone-point neighbourhood test ·
`glue_search.py` gluing search with union-find angle, manifold and Euler pruning ·
`build3d.py` metric mesh + R^3 relaxation · `render3d.py`, `net.py` figures.
