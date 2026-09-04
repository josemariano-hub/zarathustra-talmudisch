# Session notes — hat monotile on closed surfaces

**Question asked:** which families of spheres and tori can be tiled with the hat
aperiodic monotile, or a similar non-periodic tile. (Prompted by a Casey Handmer
post asking whether a variant of the hat can make curved surfaces.)

## Constraints of the working environment
The egress proxy is GitHub-shaped, not closed:

```
raw.githubusercontent.com   200  — arbitrary public repos, this is the useful hole
api.github.com              400  "Request path could not be canonicalized" (scoped to session repos)
arxiv.org, en.wikipedia.org, cs.uwaterloo.ca,
polytope.miraheze.org, chiark.greenend.org.uk, example.com   EGRESS_BLOCKED
WebSearch                   works, snippets only
```

`curl "$HTTPS_PROXY/__agentproxy/status"` is refused by the permission classifier,
not the network, so the allowlist has to be probed by hand. No numpy/scipy either,
so the lattice uses pure-Python exact integer arithmetic and figures go through a
hand-written PNG writer (`png.py`).

**Reference sources live on GitHub. Probe raw.githubusercontent.com before concluding
anything is unreachable.** Kaplan's hatviz carries the authoritative `hat_outline` in
`geometry.js`, and it confirms the lattice derivation exactly.

## Method trail
1. Built the kite lattice in integer coordinates at 1/6 granularity; triangle
   vertices at multiples of 6, midpoints at multiples of 3, centroids at (2,2)/(4,4)
   mod 6. Verified: 4-regular kite adjacency, exactly two edge lengths 1 and √3.
2. Enumerated free polykites to size 8 (873 octakites) with canonical forms under
   p6m. 23 have the Tile(1,√3) boundary signature.
3. Tried three discriminators. The *Tile(a,b) continuum test* (independent rescaling
   of a and b keeps the polygon closed) cut 23 → 3. The *disc-covering (corona) test*
   cut 3 → 1. Visual comparison with the posted image agreed.
4. Flat-torus search over Hermite normal forms — negative for the hat as expected,
   positive control (hexagon) fine.
5. Corner-type analysis produced the 60° quantum; exhaustive cyclic-sequence search
   confirmed the gcd.
6. Single-tile self-gluings enumerated exhaustively; doubling constructions verified
   by direct Gauss–Bonnet bookkeeping.

## Wrong turns worth remembering
* Generalising "blocked" from five sampled domains to the whole network, and so not
  probing GitHub, where the reference implementation was sitting the whole time. Five
  refusals is a sample, not a policy.
* Assuming "all angles are multiples of 30° ⟹ 30° curvature quantum". False. The
  a/b edge-class parity kills the odd multiples. The correct quantum is 60°, which
  is why a hat sphere needs 12 disclinations, exactly like a fullerene.
* First pick from the rendered candidates was wrong (index 12 by eye); the algebraic
  Tile(a,b) test overruled it in favour of index 8. Eyeballing 14-gons that differ by
  one kite is unreliable — the arithmetic test is not.
* `kid()` sorts a kite's four corners, destroying cyclic order; boundary extraction
  then produced pinched walks. Fixed with `cycle()`, which reorders as V, M, G, M
  using the point-type classifier.
* Piping a script through `head` closed stdout and killed it before its final
  `pickle.dump`, so a later script failed on a missing file. Do the dump first.

## Key numbers
```
hat = Tile(1,√3), 8 kites, area 8√3 a², perimeter 8a + 6b
angles  90 120 270 120 180 120 90 240 90 240 90 120 270 120
edges   b  b  a  a  a  a  b  b  a  a  b  b  a  a
curvature quantum        60°   (30° for Tile(1,1) / Spectre)
Σ charge, sphere         +12   (24 for the Spectre)
Σ charge, torus            0   but never all-zero: no flat torus exists
E = 7F,  V = 6F + χ
```

## Open
Does a hat-tiled sphere exist whose only defects are twelve q = +1 (θ = 300°) points —
the direct analogue of a fullerene? The charge arithmetic permits it; no construction
was found or ruled out here. A search would have to develop the tiling on the cone
sphere rather than enumerate edge pairings.
