"""Closed surfaces tiled by N hats.

A gluing is a length-respecting, orientation-reversing perfect matching of the
14N half-edges of N abstract 14-gons.

Bookkeeping that makes the search tractable:

* union-find over the 14N corner slots, carrying a running angle sum, so a
  vertex that overshoots max_theta prunes immediately;
* each corner slot starts with two unmatched half-edge ends.  Every gluing
  consumes four of them.  A union that is a no-op means "this vertex link just
  closed": legal only if the class has no open ends left, otherwise the surface
  is pinched there and the branch dies;
* closures are counted.  Exactly one closure happens per vertex, so V = closures
  and chi = V - 6N.  That bounds the count from both sides mid-search:
      closures <= 6N + chi        closures + 2*(7N - matched) >= 6N + chi
"""
import random, sys, collections
ANG = [90,120,270,120,180,120,90,240,90,240,90,120,270,120]
CLS = ['b','b','a','a','a','a','b','b','a','a','b','b','a','a']

class Search:
    def __init__(s, N, target_chi, max_theta, seed=0, node_limit=400000, mod120=True):
        s.mod120=mod120
        s.N=N; s.M=14*N; s.mt=max_theta; s.need=6*N+target_chi
        s.rng=random.Random(seed); s.limit=node_limit
        s.partner=[-1]*s.M
        s.parent=list(range(s.M))
        s.ang=[ANG[i%14] for i in range(s.M)]
        s.open=[2]*s.M
        s.trail=[]; s.nodes=0; s.closed=0; s.matched=0
    def find(s,x):
        while s.parent[x]!=x: x=s.parent[x]
        return x
    def dec(s,c):
        r=s.find(c); s.open[r]-=1; s.trail.append(('o',r))
    def union(s,a,b):
        ra,rb=s.find(a),s.find(b)
        if ra==rb:
            s.closed+=1; s.trail.append(('c',ra))
            return (s.open[ra]==0 and s.closed<=s.need
                    and (s.ang[ra]%120==0 or not s.mod120))
        s.parent[ra]=rb; s.ang[rb]+=s.ang[ra]; s.open[rb]+=s.open[ra]
        s.trail.append(('m',ra,rb,s.ang[ra],s.open[ra]))
        return s.ang[rb]<=s.mt
    def undo(s,k):
        while len(s.trail)>k:
            e=s.trail.pop()
            if e[0]=='o': s.open[e[1]]+=1
            elif e[0]=='c': s.closed-=1
            else:
                _,ra,rb,a,o=e
                s.parent[ra]=ra; s.ang[rb]-=a; s.open[rb]-=o
    def solve(s):
        s.nodes+=1
        if s.nodes>s.limit: raise TimeoutError
        if s.closed + 2*(7*s.N - s.matched) < s.need: return False
        h=-1
        for k in range(s.M):
            if s.partner[k]<0: h=k; break
        if h<0: return s.closed==s.need
        t,i = divmod(h,14)
        cands=[k for k in range(h+1,s.M) if s.partner[k]<0 and CLS[k%14]==CLS[i]]
        s.rng.shuffle(cands)
        for k in cands:
            u,j = divmod(k,14)
            mark=len(s.trail); s.matched+=1
            s.partner[h]=k; s.partner[k]=h
            s.dec(14*t+i); s.dec(14*t+(i+1)%14); s.dec(14*u+j); s.dec(14*u+(j+1)%14)
            ok = s.union(14*t+i, 14*u+(j+1)%14)
            if ok: ok = s.union(14*t+(i+1)%14, 14*u+j)
            if ok and s.solve(): return True
            s.undo(mark); s.matched-=1; s.partner[h]=-1; s.partner[k]=-1
        return False

def find(N, chi, max_theta, tries=200, node_limit=400000, mod120=True):
    for seed in range(tries):
        s=Search(N,chi,max_theta,seed,node_limit,mod120)
        try:
            if s.solve():
                cls={}
                for i in range(s.M): cls.setdefault(s.find(i),[]).append(i)
                thetas=sorted(s.ang[r] for r in cls)
                assert len(thetas)==6*N+chi
                assert sum(360-t for t in thetas)==360*chi
                pairs=[(divmod(h,14), divmod(s.partner[h],14)) for h in range(s.M) if s.partner[h]>h]
                return pairs, thetas, s.nodes, seed
        except TimeoutError:
            continue
    return None,None,None,None

if __name__=="__main__":
    import time
    for chi,mt,name in ((2,360,"SPHERE, all theta<=360 (convex, Alexandrov)"),(0,720,"TORUS")):
        print(name)
        for N in (6,10,14,18,24):
            t=time.time(); p,th,nd,sd=find(N,chi,mt,tries=25,node_limit=200000)
            print("  N=%2d  %6.1fs  %s" % (N,time.time()-t,
                  dict(sorted(collections.Counter(th).items())) if p else "none"))
            sys.stdout.flush()
