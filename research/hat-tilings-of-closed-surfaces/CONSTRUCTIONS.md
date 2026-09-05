# Explicit hat tilings of a sphere and a torus

> **A correctness note that changes several results below.** The first version of
> the placement test required a placed hat to have *no* kite adjacency beyond the
> hat's own nine internal edges. That is wrong on a small closed surface, where a
> tile's boundary can legitimately be glued to itself. It was caught by a positive
> control: the solver was handed the surface of the 6-hat sphere, on which six
> hats demonstrably tile, and returned "no tiling" — the six known tiles were not
> even among the placements it generated.
>
> The correct condition is that a placement is an embedding: its eight kites are
> distinct, every internal adjacency of the hat is realised, and **at each surface
> vertex the angle the placement subtends is at most that vertex's cone angle**.
> The last clause is what stops a tile wrapping around a cone point, without
> forbidding a tile that touches itself. With it the positive control passes
> (84 placements, tiling found in 7 nodes) and `code/kcx.py` replaces the old
> pipeline.
>
> Re-running everything: the cone-angle parity table, the flat tori, the
> icosahedra, the 480° quadrilateral and every cone torus come back **unchanged**.
> One result flips — the subdivided octahedron at n=2 **does** tile, with 12 hats.

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
are perfectly flat. Kite-compatibility is verified directly, not inferred from
the angles: every point identified by the gluing keeps its V/M/G type, so the
kite lattice runs continuously across every seam.

The underlying equilateral complex is

```
V = 9   E = 24   F = 17   chi = 2
faces      14 triangles + 3 bigons
vertices   3 of degree 4, 6 of degree 6
cone points  3 bigon centres at 240 deg  +  3 degree-4 vertices at 240 deg
```

All six disclinations carry **positive** charge, which is the whole of the 720°
a sphere needs. Nothing negative appears anywhere on it.

Net: `net_sphere6.png`. Six hats laid out edge-to-edge in the kite lattice —
that patch is an ordinary piece of hat tiling — with the 37 remaining
identifications marked in colour. Fold and glue.

3D: `sphere6_a.png` is a genuine isometric realization of the cone metric,
max edge error 0.003%. It is not the convex one. Alexandrov's theorem
guarantees a convex realization exists and is unique (all cone angles ≤ 2π);
volume-maximising relaxation did not reach it, so the picture is a valid but
non-convex embedding of the right surface. The convex realization has exactly
6 corners and, being 6-vertex and triangulated, octahedral combinatorics.

## The sphere — 12 hats on a regular octahedron

```
regular octahedron, each face cut into 4 equilateral triangles
32 faces, 96 kites, 12 hats
cone points   six vertices of the octahedron, 240 deg each, charge +1
total defect  +720
```

This one needs no numerical embedding at all: the surface *is* the regular
octahedron, so the 3D model is exact. `octa12_a.png`, `octa12_b.png`. Hats run
across the octahedron's edges and fold over its corners.

Only n=2 works. n=3 (27 hats), n=4 (48) and n=5 (75) are exhaustively untileable
under the corrected test, so this is not a family that continues.

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
| octahedron subdivided, n=2 (six 240° points) | 96 | 12 | **YES** |
| octahedron subdivided, n=3 | 216 | 27 | no |
| octahedron subdivided, n=4 | 384 | 48 | no |
| octahedron subdivided, n=5 | 600 | 75 | no |

The icosahedral cases die on the parity law above. Among the octahedral ones
only the coarsest subdivision tiles; n = 3, 4, 5 do not, so the six 240° cone
points being in the right places is necessary and nowhere near sufficient.
n = 6 (108 hats, 329251 nodes) and n = 7 (147 hats, 1535903 nodes) were re-run
under the corrected test and come back "no" again. n = 8 was only ever checked
with the faulty filter and has not been redone.

## Where curvature is allowed to sit

Split each face of a closed surface into kites (centroid to edge midpoints).
Then all three kinds of kite-lattice point can in principle carry curvature:

```
vertex V         cone angle  60 * (number of faces meeting there)
face centre G    cone angle 120 * (number of sides of the face)
edge midpoint M  cone angle 180 * (number of faces on the edge)
```

M is always 360° on a manifold — an edge has exactly two faces — so edge
midpoints are never cone points. That leaves V and G, and both are now closed
off except in one direction.

**G carries curvature of one sign only.** A face that is not a triangle is a
cone point at its centre: a quadrilateral gives 480° (charge -1), a bigon 240°
(charge +1). A flat triangulated disc with a single quad in the middle:

```
plain flat disc (control)         cover 72 kites -> YES   [89 nodes]
one quad face, 480 deg cone point cover 46 kites -> NO    [39 nodes]
```

So a 480° face centre is uncoverable. A 240° bigon centre is not — the 6-hat
sphere below contains three of them.

**V carries both signs but needs even degree**, from the cone table earlier:
240° (degree 4) and 480° (degree 8) are both coverable, 300° and 420° are not.

So the surfaces available are polygonal complexes of equilateral faces in which
every vertex has even degree, non-triangular faces are bigons or (at vertices)
degree 8, and no face is a quadrilateral.

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

Even cone tori do exist, and long random flip walks are the wrong way to find
them — they are *close* to the flat torus, not far. Exhaustive flip BFS from the
9-vertex flat torus hits the first one at depth 4 (1 of 395 triangulations) and
has 11 by depth 6. A beam search guided by the number of odd-degree vertices,
with visited states excluded so it cannot fall back into the undo, produces them
directly. Tiling those exhaustively:

| base | degrees | cone angles | hats | tiling | nodes |
|---|---|---|---|---|---|
| m=4 | 4²,6¹²,8² | 240×2, 360×12, 480×2 | 12 | no | 241 |
| m=4 | 4³,6¹⁰,8³ | 240×3, 360×10, 480×3 | 12 | no | 233 |
| m=6 | 4³,6³⁰,8³ | 240×3, 360×30, 480×3 | 27 | no | 1961 |
| m=6 | 4²,6³²,8² | 240×2, 360×32, 480×2 | 27 | no | 2971 |

All exhaustive. Together with the two dead ends above, and with every flat torus,
nothing kite-compatible has yet been tiled at genus 1. The 3-hat torus stands as
the only torus here, and it is not kite-compatible.

| m=8 | 4³,6⁵⁸,8³ | 240×3, 360×58, 480×3 | 48 | no | 11196 |
| m=8 | 4²,6⁶⁰,8² | 240×2, 360×60, 480×2 | 48 | no | 32851 |

Re-run under the corrected test the four m=4 and m=6 entries come back "no" with
larger search trees (1008, 976, 15465, 9805 nodes), as do both bigon tori
(13 hats, 327 nodes; 50 hats, 4405 nodes). Going *below* 12 hats needs flat tori
from non-square sublattices; at V=12 (9 hats) four even profiles exist,
including the minimal one — a single degree-4 vertex and a single degree-8, one
+120° and one -120° disclination — and all four are exhaustively untileable.

**Conjecture.** The hat tiles no kite-compatible torus — no closed genus-1
surface on which the tiling looks locally like a plane hat tiling. Evidence:
flat tori impossible (proved); 480° face centres impossible (exhaustive);
odd-degree vertex cone points impossible (exhaustive); six even cone tori
untileable (exhaustive; roughly 30 of them, 9 to 50 hats, every disclination
profile reachable including the minimal single +120/-120 pair). Not a proof.

**The sign hypothesis is refuted.** I had suggested the obstruction might be
negative curvature: the sphere that worked was all-positive, a torus must carry
negative charge, and 480° face centres are impossible. Sweeping even-degree
sphere triangulations kills it — this one tiles:

```
sphere, 12 hats, degrees 4^7 6^10 8^1
cone angles 240 x 7, 360 x 90, 480 x 1        one NEGATIVE disclination
```

So a hat tiling can carry a -120° disclination at a degree-8 vertex on a closed
surface. Negative curvature is not the barrier.

What the positives have in common is size, not sign:

| surface | hats | tiles |
|---|---|---|
| sphere, irregular, 3 bigons + 3 degree-4 | 6 | yes |
| sphere, regular octahedron, 4⁶6¹² | 12 | yes |
| sphere, 4⁷6¹⁰8¹ | 12 | yes |
| sphere, 4⁸6⁸8², 4⁹6⁶8³ | 12 | no |
| sphere, every even profile tried at n=3 | 27 | no |
| sphere, octahedra n=4,5,6,7 | 48–147 | no |
| torus, roughly 30 kite-compatible cone tori | 9–50 | no |

Every surface that tiles has 12 hats or fewer, and nothing at 27 hats or more
has tiled, sphere or torus. That fits aperiodicity better than any curvature
argument does: a small surface can close up because tiles wrap round and glue to
themselves, while a large one has to contain a genuine patch of plane hat tiling
and then close it, which the hierarchy resists.

## A counting condition

In a kite-compatible tiling the hat covers 5 faces with kite counts 3,2,1,1,1 —
one triangle entirely, one two-thirds, three one-third. So with H hats on T
triangles: 3T = 8H; each hat owns exactly one full triangle; the number of
triangles split 2+1 equals H; and the number split 1+1+1 is 2H/3. Hence

    T = 8H/3,   H = 0 (mod 3),   T = 0 (mod 8).

Every surface tried above satisfies this, so it rules nothing out here, but it
is a cheap first filter for any candidate.

Positive control for the machinery: the same solver covers a disc of the plane
(cone angle 360°) without difficulty, and reproduces the known impossibility of
every flat torus.

## Files
`complex.py` surfaces as equilateral triangulations, kite complexes, hat
placements, exact cover · `cone.py` cone-point neighbourhood test ·
`glue_search.py` gluing search with union-find angle, manifold and Euler pruning ·
`build3d.py` metric mesh + R^3 relaxation · `render3d.py`, `net.py` figures.
