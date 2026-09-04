"""Exhaustive search for tilings of FLAT TORI R^2/Lambda by a given octakite.

A tiling of a flat torus R^2/Lambda lifts to a Lambda-periodic tiling of the
plane, and conversely.  So: <tile> tiles some flat torus  <=>  <tile> admits a
periodic tiling of the plane.  This program therefore doubles as (a) a test
that separates the aperiodic hat from periodic look-alikes and (b) the direct
answer to "which flat tori can be tiled".
"""
exec(open('/home/user/hat-surfaces/kites.py').read().split("# ---- build")[0])
import pickle, sys
from itertools import product

def rot(p): a,b=p; return (-b, a+b)
def ref(p): a,b=p; return (a+b, -b)
def sym(i):
    r,m = i//2, i%2
    def f(p):
        q=ref(p) if m else p
        for _ in range(r): q=rot(q)
        return q
    return f
SYMS=[sym(i) for i in range(12)]

def sublattices(D):
    """Hermite normal forms [[a,0],[b,c]], a*c=D, 0<=b<a -> index-D sublattices of Z^2."""
    out=[]
    for a in range(1,D+1):
        if D%a: continue
        c=D//a
        for b in range(a):
            out.append(((a,0),(b,c)))
    return out

def reducer(L):
    (a,_),(b,c) = L
    # lattice of TRANSLATIONS in integer point coords is 6*L
    A=(6*a,0); B=(6*b,6*c)
    def red(p):
        x,y=p
        k = y // B[1]
        x -= k*B[0]; y -= k*B[1]
        x %= A[0]
        return (x,y)
    return red

def build_cells(L):
    red=reducer(L)
    (a,_),(b,c)=L
    cells={}
    for i in range(-4*max(a,b,c)-4, 4*max(a,b,c)+4):
        for j in range(-4*max(a,b,c)-4, 4*max(a,b,c)+4):
            for kind in ('u','d'):
                for k in kites_of((kind,i,j)):
                    key=frozenset(red(p) for p in k)
                    cells.setdefault(key, 0)
    return cells, red

def placements(base_cells_pts, L):
    """base_cells_pts: list of 4-tuples of points for the 8 kites of the tile."""
    red=reducer(L); (a,_),(b,c)=L
    seen=set(); out=[]
    for f in SYMS:
        img=[tuple(f(p) for p in k) for k in base_cells_pts]
        for i in range(-2*max(a,b,c)-2, 2*max(a,b,c)+2):
            for j in range(-2*max(a,b,c)-2, 2*max(a,b,c)+2):
                t=(6*i+3*j, 3*j)  # translations by triangle-lattice vectors (e1,e2 scaled by 6)
                t=(6*i, 6*j)
                ks=frozenset(frozenset(red((p[0]+t[0], p[1]+t[1])) for p in k) for k in img)
                if len(ks)!=8: continue
                if ks in seen: continue
                seen.add(ks); out.append(ks)
    return out

def exact_cover(universe, pieces):
    cell2p={c:[] for c in universe}
    for idx,pc in enumerate(pieces):
        for c in pc: cell2p[c].append(idx)
    uncovered=set(universe); used=[]
    def solve():
        if not uncovered: return True
        c=min(uncovered, key=lambda c: sum(1 for i in cell2p[c] if pieces[i]<=uncovered))
        opts=[i for i in cell2p[c] if pieces[i]<=uncovered]
        if not opts: return False
        for i in opts:
            uncovered.difference_update(pieces[i]); used.append(i)
            if solve(): return True
            uncovered.update(pieces[i]); used.pop()
        return False
    return solve(), used

winners = dict((i,(c,p)) for i,c,p in pickle.load(open('/home/user/hat-surfaces/tileab.pkl','rb')))
for idx in (8,22):
    cells,path = winners[idx]
    base=[KITES4[c] for c in cells] if False else [tuple(c) for c in cells]  # cells are sorted 4-tuples
    print("\n########## candidate %d ##########" % idx)
    for D in (4,8,12,16):
        found=[]
        for L in sublattices(D):
            uni,red = build_cells(L)
            uni=set(uni.keys())
            if len(uni)!=6*D:
                print("  !! cell-count mismatch", L, len(uni)); continue
            pcs=[p for p in placements(base,L) if p<=uni]
            ok,_=exact_cover(uni,pcs)
            if ok: found.append(L)
        print("  index D=%2d (%2d tiles): tileable sublattices: %s" % (D, 6*D//8, found if found else "NONE"))
        sys.stdout.flush()
