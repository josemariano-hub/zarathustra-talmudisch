"""Local-tileability (corona) test: can the shape cover a disc of kites exactly,
using copies that never overlap?  Plus a positive control (the 6-kite hexagon)."""
exec(open('/home/user/hat-surfaces/kites.py').read().split("# ---- build")[0])
import pickle, sys
from math import sqrt

def rot(p): a,b=p; return (-b,a+b)
def ref(p): a,b=p; return (a+b,-b)
def sym(i):
    r,m=i//2,i%2
    def f(p):
        q=ref(p) if m else p
        for _ in range(r): q=rot(q)
        return q
    return f
SYMS=[sym(i) for i in range(12)]

def kid(k): return tuple(sorted(k))
def cen(k):
    pts=[xy(p) for p in k]; return (sum(x for x,y in pts)/4, sum(y for x,y in pts)/4)
def rad(k):
    x,y=cen(k); return sqrt(x*x+y*y)

def gen_placements(base, RO):
    seen=set(); out=[]
    N=int(RO*1.2)+4
    for f in SYMS:
        img=[tuple(f(p) for p in k) for k in base]
        for i in range(-N,N+1):
            for j in range(-N,N+1):
                t=(6*i,6*j)
                ks=frozenset(kid(tuple((p[0]+t[0],p[1]+t[1]) for p in k)) for k in img)
                if ks in seen: continue
                seen.add(ks)
                if all(rad(k)<=RO for k in ks): out.append(ks)
    return out

def cover_disc(base, RI, RO, limit=4_000_000):
    pcs=gen_placements(base,RO)
    inner=set()
    for pc in pcs:
        for k in pc:
            if rad(k)<=RI: inner.add(k)
    cell2p={c:[] for c in inner}
    for i,pc in enumerate(pcs):
        for c in pc:
            if c in inner: cell2p[c].append(i)
    used_cells=set(); uncov=set(inner); nodes=[0]
    def solve():
        nodes[0]+=1
        if nodes[0]>limit: raise TimeoutError
        if not uncov: return True
        c=min(uncov,key=lambda c: sum(1 for i in cell2p[c] if not (pcs[i]&used_cells)))
        opts=[i for i in cell2p[c] if not (pcs[i]&used_cells)]
        for i in opts:
            used_cells.update(pcs[i]); uncov.difference_update(pcs[i])
            if solve(): return True
            used_cells.difference_update(pcs[i]); uncov.update(pcs[i]&inner)
        return False
    try:
        r=solve()
    except TimeoutError:
        return None, len(inner), nodes[0]
    return r, len(inner), nodes[0]

# positive control: hexagon of 6 kites around the origin vertex V=(0,0)
hexk=[]
for kind in ('u','d'):
    for a in (-1,0):
        for b in (-1,0):
            for k in kites_of((kind,a,b)):
                if (0,0) in k: hexk.append(tuple(k))
hexk=list({kid(k) for k in hexk})
print("control hexagon kite count:", len(hexk))
for RI,RO in ((6,11),):
    r,n,nd = cover_disc(hexk,RI,RO)
    print("  hexagon covers disc R=%d (%d kites): %s  [%d nodes]" % (RI,n,r,nd))

winners=dict((i,(c,p)) for i,c,p in pickle.load(open('/home/user/hat-surfaces/tileab.pkl','rb')))
for idx in (8,22,2):
    base=[tuple(c) for c in winners[idx][0]]
    for RI,RO in ((6,12),(9,16)):
        r,n,nd = cover_disc(base,RI,RO)
        print("cand %2d : disc R=%2d (%3d kites) -> %s  [%d nodes]" % (idx,RI,n,r,nd))
        sys.stdout.flush()
        if r is False: break
