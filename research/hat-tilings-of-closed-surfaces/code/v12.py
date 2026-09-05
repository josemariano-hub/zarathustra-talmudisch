"""Exhaustive flip BFS at V=12 (24 triangles, 72 kites, 9 hats): enumerate every
even-degree cone torus reachable within a few flips and try to tile each.

Fast path: a flip is rejected by a cheap directed-edge check; the full
KiteComplex is only built for the even-degree survivors.
"""
from complex import KiteComplex, hat_word
from kcx import hat_pattern, placements, exact_cover, corner_classes
from collections import Counter
import sys, time, pickle

def flat_torus_lat(a,b,c):
    def red(i,j):
        q=j//c; return ((i-q*b)%a, j-q*c)
    ids={}; V=lambda i,j: ids.setdefault(red(i,j), len(ids)); T=[]
    for j in range(c):
        for i in range(a):
            T.append((V(i,j),V(i+1,j),V(i,j+1))); T.append((V(i+1,j),V(i+1,j+1),V(i,j+1)))
    for t in T:
        if len(set(t))<3: return None
    try: KiteComplex(T)
    except Exception: return None
    return T

def emap(tris):
    e={}
    for t,f in enumerate(tris):
        for k in range(3):
            p,q=f[k],f[(k+1)%3]
            if (p,q) in e: return None
            e[(p,q)]=t
    return e

def flip_fast(tris, p, q, e):
    t1=e.get((p,q)); t2=e.get((q,p))
    if t1 is None or t2 is None or t1==t2: return None
    A=[v for v in tris[t1] if v not in (p,q)]; B=[v for v in tris[t2] if v not in (p,q)]
    if len(A)!=1 or len(B)!=1: return None
    c,d=A[0],B[0]
    if c==d or (c,d) in e or (d,c) in e: return None
    new=list(tris); new[t1]=(c,d,q); new[t2]=(d,c,p)
    return new if emap(new) else None

def degs(tris):
    dg=Counter()
    for f in tris:
        for v in f: dg[v]+=1
    return dg

if __name__=="__main__":
    info,key,nb=hat_word(); adj,tree,order=hat_pattern(nb,key)
    seeds=[]
    for (a,b,c) in [(3,0,4),(4,0,3),(2,0,6),(6,0,2),(4,1,3),(4,2,3),(6,1,2),(6,3,2),(12,0,1),(1,0,12)]:
        T=flat_torus_lat(a,b,c)
        if T: seeds.append(((a,b,c),T))
    print("V=12 seeds (flat tori from index-12 sublattices): %d"%len(seeds))
    allevens={}
    for (a,b,c),T in seeds:
        base=tuple(tuple(t) for t in T)
        seen={frozenset(base)}; frontier=[list(base)]
        for depth in range(1,5):
            nf=[]
            for tris in frontier:
                e=emap(tris)
                if e is None: continue
                for (p,q) in list(e):
                    f=flip_fast(tris,p,q,e)
                    if f is None: continue
                    g=frozenset(f)
                    if g in seen: continue
                    seen.add(g); nf.append(f)
                    dg=degs(f)
                    if all(x%2==0 for x in dg.values()) and set(dg.values())!={6}:
                        allevens.setdefault(tuple(sorted(Counter(dg.values()).items())), f)
            frontier=nf
            if len(seen)>120000: break
        print("  lat(%d,%d,%d): %6d triangulations to depth %d, %d even profiles so far"
              %(a,b,c,len(seen),depth,len(allevens)))
        sys.stdout.flush()
    print()
    print("distinct even-degree cone tori at 9 hats: %d"%len(allevens))
    for sig,tris in sorted(allevens.items()):
        kc=KiteComplex(tris); nk=len(kc.kites)
        cls,ang=corner_classes(kc.nbr,nk)
        pcs=placements(kc.nbr,nk,adj,tree,order)
        t0=time.time(); ok,sol,nd=exact_cover(set(range(nk)),pcs,10_000_000)
        print("  degrees %-26s cone %-28s -> %-5s [%d nodes %.1fs]"
              %(dict(sig),dict(sorted(Counter(ang.values()).items())),ok,nd,time.time()-t0))
        sys.stdout.flush()
        if ok:
            pickle.dump((tris,sol),open('KTORUS_FOUND.pkl','wb')); print("  *** TORUS FOUND ***"); break
