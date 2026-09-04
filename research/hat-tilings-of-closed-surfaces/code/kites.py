"""
Exact construction of the kite lattice (deltoidal trihexagonal tiling) and
enumeration of octakites, in order to pin down the 'hat' monotile from
first principles (no trusted external coordinate list).

Integer coordinate system
-------------------------
Point (a,b) means the Euclidean point  u*(a + b/2, b*sqrt(3)/2)  with u = 1/sqrt(3).
Triangle vertices sit at multiples of 6 in this integer lattice, so the
equilateral triangle side is 6*u = 2*sqrt(3).

  V (triangle vertex)   : both coords == 0 (mod 6)
  M (edge midpoint)     : both coords == 0 (mod 3), not both 0 (mod 6)
  G (triangle centroid) : coords == (2,2) or (4,4) (mod 6)

Kite edges then have exactly two lengths:
  V-M  = sqrt(3)   ("long")
  M-G  = 1         ("short")
"""
from math import sqrt, atan2, degrees, isclose
from itertools import combinations

U = 1.0/sqrt(3.0)
def xy(p):
    a,b = p
    return (U*(a + b/2.0), U*(b*sqrt(3)/2.0))

def dist(p,q):
    (x1,y1),(x2,y2) = xy(p), xy(q)
    return sqrt((x1-x2)**2 + (y1-y2)**2)

def ptype(p):
    a,b = p
    if a % 6 == 0 and b % 6 == 0: return 'V'
    if a % 3 == 0 and b % 3 == 0: return 'M'
    return 'G'

def mid(p,q): return ((p[0]+q[0])//2, (p[1]+q[1])//2)

def triangles(R):
    for a in range(-R, R+1):
        for b in range(-R, R+1):
            yield ('u', a, b)
            yield ('d', a, b)

def tri_pts(t):
    kind, a, b = t
    if kind == 'u':
        A = (6*a, 6*b); B = (6*a+6, 6*b); C = (6*a, 6*b+6)
        G = (6*a+2, 6*b+2)
    else:
        A = (6*a+6, 6*b); B = (6*a, 6*b+6); C = (6*a+6, 6*b+6)
        G = (6*a+4, 6*b+4)
    return A,B,C,G

def kites_of(t):
    A,B,C,G = tri_pts(t)
    out = []
    for (X,Y,Z) in ((A,B,C),(B,C,A),(C,A,B)):
        # kite at corner X: X, mid(X,Y), G, mid(X,Z)
        out.append((X, mid(X,Y), G, mid(X,Z)))
    return out

def kite_key(k):
    return tuple(sorted(k))

def kite_edges(k):
    X, M1, G, M2 = k
    return [frozenset((X,M1)), frozenset((M1,G)), frozenset((G,M2)), frozenset((M2,X))]

# ---- build a finite patch -------------------------------------------------
R = 5
KITES = {}                 # key -> ordered 4-tuple
EDGE2K = {}                # edge -> set of kite keys
for t in triangles(R):
    for k in kites_of(t):
        kk = kite_key(k)
        KITES[kk] = k
        for e in kite_edges(k):
            EDGE2K.setdefault(e, set()).add(kk)

NBR = {kk: set() for kk in KITES}
for e, ks in EDGE2K.items():
    ks = list(ks)
    for i in range(len(ks)):
        for j in range(i+1, len(ks)):
            NBR[ks[i]].add(ks[j]); NBR[ks[j]].add(ks[i])

# sanity: interior kites are 4-regular; edge lengths are only 1 and sqrt(3)
degs = {}
for kk, ns in NBR.items():
    degs[len(ns)] = degs.get(len(ns),0)+1
lens = set()
for e in EDGE2K:
    p,q = tuple(e)
    lens.add(round(dist(p,q), 9))
print("kite adjacency degree histogram:", degs)
print("distinct edge lengths:", sorted(lens), " (expect 1.0 and sqrt(3)=%.9f)" % sqrt(3))
print("num kites in patch:", len(KITES))
