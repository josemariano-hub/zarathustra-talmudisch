"""Kite-compatible cone tori: equilateral triangulations of the torus whose
vertex degrees are all even (so every cone angle is a multiple of 120 deg).

A diagonal flip moves degrees by (-1,-1,+1,+1), so one flip gives 5,5,7,7 --
odd, and the point-type law forbids odd degrees at lattice vertices.  Two flips
can give 4,6,...,8 or 4,4,...,8,8, which are allowed.  Then tile exhaustively.
"""
from complex import KiteComplex, hat_word, placements, exact_cover, flat_torus
from collections import Counter, defaultdict
import sys, time, pickle

def edgemap(tris):
    e={}
    for t,(a,b,c) in enumerate(tris):
        for (p,q) in ((a,b),(b,c),(c,a)): e[(p,q)]=t
    return e

def flip(tris, p, q, e=None):
    e = e or edgemap(tris)
    t1=e.get((p,q)); t2=e.get((q,p))
    if t1 is None or t2 is None or t1==t2: return None
    A=[v for v in tris[t1] if v not in (p,q)]; B=[v for v in tris[t2] if v not in (p,q)]
    if len(A)!=1 or len(B)!=1: return None
    c,d=A[0],B[0]
    if c==d: return None
    if (c,d) in e or (d,c) in e: return None      # would duplicate an edge
    new=list(tris); new[t1]=(c,d,q); new[t2]=(d,c,p)
    return new

def degrees(tris):
    dg=Counter()
    for (a,b,c) in tris:
        for v in (a,b,c): dg[v]+=1
    return dg

def even_cone_tori(m, limit=None):
    base=[tuple(t) for t in flat_torus(m)]
    seen=set(); out=[]
    e0=edgemap(base)
    for (p,q) in sorted(e0):
        f1=flip(base,p,q,e0)
        if f1 is None: continue
        e1=edgemap(f1)
        for (r,s) in sorted(e1):
            f2=flip(f1,r,s,e1)
            if f2 is None: continue
            dg=degrees(f2)
            if any(d%2 for d in dg.values()): continue
            sig=tuple(sorted(Counter(dg.values()).items()))
            if sig in seen: continue
            try: KiteComplex(f2)
            except Exception: continue
            seen.add(sig); out.append((sig,f2))
            if limit and len(out)>=limit: return out
    return out

if __name__=="__main__":
    info,key,nb = hat_word()
    for m in (4,6):
        cands=even_cone_tori(m)
        print("torus base m=%d: %d distinct even-degree profiles from two flips"%(m,len(cands)))
        for sig,tris in cands:
            kc=KiteComplex(tris); K=len(kc.kites)
            ca=dict(sorted(Counter(kc.cone_angles().values()).items()))
            if K%8:
                print("   degrees %s -> %d kites, not a multiple of 8"%(dict(sig),K)); continue
            pcs=placements(kc,info,key,nb)
            t=time.time(); ok,sol,nd=exact_cover(set(range(K)),pcs,limit=6_000_000)
            print("   degrees %-22s cone angles %-28s %3d hats  %d placements -> %s  [%d nodes, %.1fs]"
                  % (dict(sig), ca, K//8, len(pcs), ok, nd, time.time()-t))
            if ok: pickle.dump((tris,[set(p) for p in sol]),open('conetorus_m%d.pkl'%m,'wb'))
            sys.stdout.flush()
