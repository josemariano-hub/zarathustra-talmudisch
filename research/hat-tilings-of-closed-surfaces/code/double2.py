exec(open('/home/user/hat-surfaces/double.py').read().split("tiles=[poly_of")[0])
import math
tiles=[poly_of(pc) for pc in sol]

def bcycles(kset):
    cnt=Counter()
    for k in kset:
        c=cycle(k)
        for i in range(4): cnt[frozenset((c[i],c[(i+1)%4]))]+=1
    be=[e for e,n in cnt.items() if n==1]
    adj=defaultdict(list)
    for e in be:
        p,q=tuple(e); adj[p].append(q); adj[q].append(p)
    if any(len(v)!=2 for v in adj.values()): return None
    cycles=[]; unseen=set(adj)
    while unseen:
        st=next(iter(unseen)); path=[st]; prev=None; cur=st
        while True:
            a,b=adj[cur]; nx=a if a!=prev else b; prev,cur=cur,nx
            if cur==st: break
            path.append(cur)
        for v in path: unseen.discard(v)
        cycles.append(path)
    return cycles

def ang_at(v, tilepolys):
    tot=0
    for P in tilepolys:
        for i in range(len(P)):
            if P[i]==v:
                p=xy(P[i-1]); q=xy(P[i]); r=xy(P[(i+1)%len(P)])
                tot+=round(degrees((math.atan2(p[1]-q[1],p[0]-q[0])-math.atan2(r[1]-q[1],r[0]-q[0]))%(2*pi)))
    return tot

def report(idxs, label):
    ks=set().union(*[sol[i] for i in idxs]); tp=[tiles[i] for i in idxs]
    cyc=bcycles(ks)
    if cyc is None: return False
    b=len(cyc); n=len(idxs)
    bv=[v for c in cyc for v in c]
    cone=[2*ang_at(v,tp) for v in bv]; dfs=[360-a for a in cone]
    chi=2*(2-b)
    nm={2:"SPHERE",0:"TORUS"}.get(chi,"genus %d"%((2-chi)//2))
    print("%-46s %2d hats, %d boundary circle(s) -> DOUBLE: %3d hats, chi=%+d  %s"%(label,n,b,2*n,chi,nm))
    print("     seam cone angles theta   :", dict(sorted(Counter(cone).items())))
    print("     sum of defects           : %+d deg   (Gauss-Bonnet: %+d)  match=%s"%(sum(dfs),360*chi,sum(dfs)==360*chi))
    print("     disclination charges q   :", dict(sorted(Counter(d//60 for d in dfs).items())), " sum q =", sum(d//60 for d in dfs))
    print("     every defect a multiple of 60 deg:", all(d%60==0 for d in dfs))
    return True

# 1) single hat
print("=== 1. one hat, doubled ===")
report([0], "single hat (a disc)")

# 2) grow the largest patch whose boundary stays a clean simple cycle
print("\n=== 2. larger simply-connected patches, doubled ===")
cur=[0]; grown=True
best=[0]
while grown:
    grown=False
    for i in range(len(sol)):
        if i in cur: continue
        if not any(any(any(p in cycle(k2) for p in cycle(k)) for k2 in sol[i]) for k in set().union(*[sol[j] for j in cur])):
            pass
        trial=cur+[i]
        ks=set().union(*[sol[j] for j in trial])
        c=bcycles(ks)
        if c is not None and len(c)==1:
            cur=trial; grown=True; break
print("   grew a clean simply-connected patch of", len(cur), "hats")
report(cur, "grown disc patch")

# 3) annulus: clean patch minus an interior tile
print("\n=== 3. annulus (patch with a hat-shaped hole), doubled ===")
done=False
for i in cur:
    rest=[j for j in cur if j!=i]
    if not rest: continue
    ks=set().union(*[sol[j] for j in rest])
    c=bcycles(ks)
    if c is not None and len(c)==2:
        done=report(rest, "annulus = disc patch minus one interior hat")
        if done: break
if not done: print("   (no single-tile removal left a clean annulus in this patch)")
