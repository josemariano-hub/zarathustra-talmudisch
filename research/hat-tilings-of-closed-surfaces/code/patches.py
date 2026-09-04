"""Plane-tiling vertex statistics; convex-region test; explicit doubling constructions."""
exec(open('/home/user/hat-surfaces/kites.py').read().split("# ---- build")[0])
import pickle, sys
from math import sqrt, atan2, degrees, pi
from collections import Counter, defaultdict
H=pickle.load(open('/home/user/hat-surfaces/hat.pkl','rb'))
base=[tuple(c) for c in H['cells']]
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
kid=lambda k: tuple(sorted(k))
def cen(k):
    P=[xy(p) for p in k]; return (sum(x for x,y in P)/4,sum(y for x,y in P)/4)
def rad(k):
    x,y=cen(k); return sqrt(x*x+y*y)

def gen(base, keep):
    seen=set(); out=[]
    for f in SYMS:
        img=[tuple(f(p) for p in k) for k in base]
        for i in range(-14,15):
            for j in range(-14,15):
                t=(6*i,6*j)
                ks=frozenset(kid(tuple((p[0]+t[0],p[1]+t[1]) for p in k)) for k in img)
                if ks in seen: continue
                seen.add(ks)
                if keep(ks): out.append(ks)
    return out

def cover(universe, pcs, limit=3_000_000):
    c2p=defaultdict(list)
    for i,p in enumerate(pcs):
        for c in p&universe: c2p[c].append(i)
    used=set(); unc=set(universe); sol=[]; nodes=[0]
    def go():
        nodes[0]+=1
        if nodes[0]>limit: raise TimeoutError
        if not unc: return True
        c=min(unc,key=lambda c: sum(1 for i in c2p[c] if not (pcs[i]&used)))
        for i in c2p[c]:
            if pcs[i]&used: continue
            used.update(pcs[i]); unc.difference_update(pcs[i]); sol.append(i)
            if go(): return True
            used.difference_update(pcs[i]); unc.update(pcs[i]&universe); sol.pop()
        return False
    try: return (go(), [pcs[i] for i in sol])
    except TimeoutError: return (None, [])

# ---------- 1. vertex statistics of a real hat tiling patch ----------
RI,RO=9,16
pcs=gen(base, lambda ks: all(rad(k)<=RO for k in ks))
inner={k for p in pcs for k in p if rad(k)<=RI}
ok,sol=cover(inner,pcs)
print("plane patch: covered disc of %d kites with %d hats -> %s" % (len(inner),len(sol),ok))
# reconstruct each placed hat's boundary polygon and its corner angles
def cycle(k):
    """sorted 4-tuple of kite corners -> cyclic order V, M, G, M"""
    V=[p for p in k if ptype(p)=='V']; M=[p for p in k if ptype(p)=='M']; G=[p for p in k if ptype(p)=='G']
    assert len(V)==1 and len(M)==2 and len(G)==1, (k,[ptype(p) for p in k])
    return (V[0],M[0],G[0],M[1])
def poly_of(pc):
    cnt=Counter()
    for k in pc:
        c=cycle(k)
        for e in [frozenset((c[0],c[1])),frozenset((c[1],c[2])),frozenset((c[2],c[3])),frozenset((c[3],c[0]))]:
            cnt[e]+=1
    be=[e for e,n in cnt.items() if n==1]
    adj=defaultdict(list)
    for e in be:
        p,q=tuple(e); adj[p].append(q); adj[q].append(p)
    st=next(iter(adj)); path=[st]; prev=None; cur=st
    while True:
        a,b=adj[cur]; nx=a if a!=prev else b; prev,cur=cur,nx
        if cur==st: break
        path.append(cur)
    s=0
    for i in range(len(path)):
        (x1,y1)=xy(path[i]); (x2,y2)=xy(path[(i+1)%len(path)]); s+=x1*y2-x2*y1
    if s<0: path=path[::-1]
    return path
vang=Counter(); vdeg=Counter()
for pc in sol:
    P=poly_of(pc)
    for i in range(len(P)):
        p=xy(P[i-1]); q=xy(P[i]); r=xy(P[(i+1)%len(P)])
        a=round(degrees((atan2(p[1]-q[1],p[0]-q[0])-atan2(r[1]-q[1],r[0]-q[0]))%(2*pi)))
        vang[P[i]]+=a; vdeg[P[i]]+=1
inner_v=[v for v in vang if all(rad(k)<=RI-3 for k in [] ) or True]
deep=[v for v in vang if sqrt(xy(v)[0]**2+xy(v)[1]**2) < RI-3]
print("  vertices well inside the patch: %d" % len(deep))
print("  angle sums at those vertices  :", Counter(vang[v] for v in deep))
print("  #hat-corners meeting there    :", Counter(vdeg[v] for v in deep))

# ---------- 2. can hats tile a CONVEX region? ----------
def tri_region(side, updown='u'):
    ks=set()
    for a in range(side):
        for b in range(side-a):
            for k in kites_of(('u',a,b)): ks.add(kid(k))
            if a+b < side-1:
                for k in kites_of(('d',a,b)): ks.add(kid(k))
    return ks
def hex_region(n):
    ks=set()
    for a in range(-n,n):
        for b in range(-n,n):
            for kind in ('u','d'):
                A,B,C,G=tri_pts((kind,a,b))
                cx=sum(xy(p)[0] for p in (A,B,C))/3; cy=sum(xy(p)[1] for p in (A,B,C))/3
                # hexagon of circumradius n*side centred at origin
                import math
                r=math.hypot(cx,cy)
                th=math.atan2(cy,cx)
                R=n*2*sqrt(3)*sqrt(3)/2
                if r*max(abs(math.cos(th-k*pi/3)) for k in range(3)) <= R+1e-9:
                    for k in kites_of((kind,a,b)): ks.add(kid(k))
    return ks
for name,reg in (("triangle side 4 (48 kites = 6 hats)", tri_region(4)),
                 ("triangle side 8 (192 kites = 24 hats)", tri_region(8))):
    if len(reg)%8: print("  %s : %d kites, not a multiple of 8 -> skip"%(name,len(reg))); continue
    p2=gen(base, lambda ks: ks<=reg)
    ok,sol2=cover(reg,p2)
    print("convex region %-40s %3d kites, %2d hats needed -> tileable: %s" % (name,len(reg),len(reg)//8,ok))
    sys.stdout.flush()
