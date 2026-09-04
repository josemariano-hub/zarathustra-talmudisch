"""Enumerate free octakites; filter to those whose boundary is a simple closed
14-gon with 6 long (sqrt3) and 8 short (1) edges -- the Tile(1,sqrt3) signature."""
exec(open('/home/user/hat-surfaces/kites.py').read().split("# ---- build")[0])

from math import sqrt, atan2, degrees, pi
R = 6
KITES = {}; EDGE2K = {}
for t in triangles(R):
    for k in kites_of(t):
        kk = kite_key(k); KITES[kk] = k
        for e in kite_edges(k): EDGE2K.setdefault(e, set()).add(kk)
NBR = {kk:set() for kk in KITES}
for e,ks in EDGE2K.items():
    ks=list(ks)
    for i in range(len(ks)):
        for j in range(i+1,len(ks)):
            NBR[ks[i]].add(ks[j]); NBR[ks[j]].add(ks[i])

# lattice symmetries: rotation R60 (a,b)->(-b,a+b) about origin, reflection (a,b)->(a+b,-b)
def rot(p): a,b=p; return (-b, a+b)
def ref(p): a,b=p; return (a+b, -b)
SYMS=[]
for r in range(6):
    for m in range(2):
        def f(p, r=r, m=m):
            q=p
            if m: q=ref(q)
            for _ in range(r): q=rot(q)
            return q
        SYMS.append(f)
# origin of symmetry must be a lattice point of the *kite tiling* symmetry group.
# Rotations of order 6 sit at V points, order 3 at G, order 2 at M. Using V=origin
# with 12 symmetries + all translations by triangle-lattice vectors covers p6m.

def canon(cells):
    best=None
    for f in SYMS:
        pts=[tuple(sorted(f(p) for p in KITES[c])) for c in cells]
        # normalise translation: shift so min corner is at origin (translations by 6*Z^2)
        allp=[p for c in pts for p in c]
        ma=min(p[0] for p in allp); mb=min(p[1] for p in allp)
        # snap shift to multiples of 6 (triangle lattice translations)
        sa=(ma//6)*6; sb=(mb//6)*6
        for da in (0,6,-6):
            for db in (0,6,-6):
                sh=(sa+da, sb+db)
                key=tuple(sorted(tuple(sorted((p[0]-sh[0], p[1]-sh[1]) for p in c)) for c in pts))
                if best is None or key<best: best=key
    return best

# grow polyforms
seed = kite_key(kites_of(('u',0,0))[0])
level = {canon(frozenset([seed])): frozenset([seed])}
for size in range(2, 9):
    nxt = {}
    for cells in level.values():
        frontier=set()
        for c in cells: frontier |= NBR[c]
        frontier -= cells
        for c in frontier:
            ns = cells | {c}
            # keep inside patch generously
            key = canon(ns)
            if key not in nxt: nxt[key]=ns
    level = nxt
    print("free polykites of size %d: %d" % (size, len(level)))

def boundary_info(cells):
    cnt={}
    for c in cells:
        for e in kite_edges(KITES[c]): cnt[e]=cnt.get(e,0)+1
    bedges=[e for e,n in cnt.items() if n==1]
    # build cycle
    adj={}
    for e in bedges:
        p,q=tuple(e)
        adj.setdefault(p,[]).append(q); adj.setdefault(q,[]).append(p)
    if any(len(v)!=2 for v in adj.values()): return None
    start=next(iter(adj)); path=[start]; prev=None; cur=start
    while True:
        a,b=adj[cur]
        nxt = a if a!=prev else b
        prev,cur = cur,nxt
        if cur==start: break
        path.append(cur)
        if len(path)>len(bedges): return None
    if len(path)!=len(bedges): return None   # not a simple closed curve
    return path

results=[]
for key,cells in level.items():
    path = boundary_info(cells)
    if path is None: continue
    if len(path)!=14: continue
    L=[round(dist(path[i], path[(i+1)%14]),6) for i in range(14)]
    nlong=sum(1 for x in L if abs(x-sqrt(3))<1e-6); nshort=sum(1 for x in L if abs(x-1)<1e-6)
    if (nlong,nshort)!=(6,8): continue
    results.append((key,cells,path,L))
print("octakites with simple 14-gon boundary, 6 long + 8 short edges:", len(results))
import pickle
pickle.dump([(c,p) for _,c,p,_ in results], open('/home/user/hat-surfaces/cands.pkl','wb'))
