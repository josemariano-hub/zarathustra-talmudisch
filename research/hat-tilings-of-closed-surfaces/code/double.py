"""Explicit closed surfaces: double a hat patch (-> sphere) and a hat annulus (-> torus).
Everything is verified by direct Gauss-Bonnet / Euler bookkeeping, not asserted."""
exec(open('/home/user/hat-surfaces/patches.py').read().split("# ---------- 2.")[0])
import math
def region_boundary_cycles(kset):
    cnt=Counter()
    for k in kset:
        c=cycle(k)
        for i in range(4): cnt[frozenset((c[i],c[(i+1)%4]))]+=1
    be=[e for e,n in cnt.items() if n==1]
    adj=defaultdict(list)
    for e in be:
        p,q=tuple(e); adj[p].append(q); adj[q].append(p)
    if any(len(v)!=2 for v in adj.values()): return None,be
    cycles=[]; unseen=set(adj)
    while unseen:
        st=next(iter(unseen)); path=[st]; prev=None; cur=st
        while True:
            a,b=adj[cur]; nx=a if a!=prev else b; prev,cur=cur,nx
            if cur==st: break
            path.append(cur)
        for v in path: unseen.discard(v)
        cycles.append(path)
    return cycles,be

def interior_angle_sum_at(v, tiles):
    """total angle the patch subtends at boundary vertex v"""
    tot=0
    for P in tiles:
        for i in range(len(P)):
            if P[i]==v:
                p=xy(P[i-1]); q=xy(P[i]); r=xy(P[(i+1)%len(P)])
                tot+=round(degrees((math.atan2(p[1]-q[1],p[0]-q[0])-math.atan2(r[1]-q[1],r[0]-q[0]))%(2*pi)))
    return tot

tiles=[poly_of(pc) for pc in sol]
allk=set().union(*sol)
cyc,be = region_boundary_cycles(allk)
print("patch of %d hats: %d boundary cycle(s)" % (len(sol), len(cyc) if cyc else -1))

def report(kset, tilepolys, label):
    cyc,_=region_boundary_cycles(kset)
    if cyc is None: print(label,": boundary is pinched, skip"); return
    b=len(cyc)
    n=len(tilepolys)
    # doubled surface
    bverts=[v for c in cyc for v in c]
    cone=[2*interior_angle_sum_at(v,tilepolys) for v in bverts]
    defects=[360-a for a in cone]
    chi_double = 2*(2-b)          # double of a genus-0 surface with b boundary circles
    print("%-42s  %2d hats, %d boundary circle(s)  ->  double = %d hats, chi = %d (%s)"
          % (label, n, b, 2*n, chi_double,
             {2:"SPHERE",0:"TORUS",-2:"genus 2"}.get(chi_double,"genus %d"%((2-chi_double)//2))))
    print("      seam cone angles      :", dict(Counter(sorted(cone))))
    print("      sum of angle defects  : %+d deg   (Gauss-Bonnet requires %+d)" % (sum(defects), 360*chi_double))
    print("      all defects multiples of 60 :", all(d%60==0 for d in defects))
    print("      disclination charge q=(360-theta)/60 :", dict(Counter(sorted(d//60 for d in defects))))

report(allk, tiles, "disc patch  (simply connected)")

# annulus: drop one tile that is well inside
inner_tile=None
for pc,P in zip(sol,tiles):
    if all(rad(k)<5 for k in pc): inner_tile=(pc,P); break
if inner_tile:
    pc0,P0=inner_tile
    k2=allk-pc0
    t2=[P for pc,P in zip(sol,tiles) if pc is not pc0]
    report(k2, t2, "annulus (same patch, one hat removed)")
