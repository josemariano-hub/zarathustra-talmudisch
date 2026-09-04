"""Can the hat cover a neighbourhood of a cone point of angle 60*d, sitting at a
vertex of the underlying triangular lattice?  d=6 is the flat case."""
from complex import KiteComplex, hat_word, exact_cover
from collections import defaultdict, Counter

class PatchComplex(KiteComplex):
    def __init__(s, tris):
        s.tris=[tuple(t) for t in tris]
        s.kites=[(t,k) for t in range(len(s.tris)) for k in range(3)]
        s.kid={kk:i for i,kk in enumerate(s.kites)}
        edge={}
        for t,(a,b,c) in enumerate(s.tris):
            for k,(p,q) in enumerate(((a,b),(b,c),(c,a))):
                assert (p,q) not in edge, "orientation clash on %s"%str((p,q))
                edge[(p,q)]=(t,k)
        s.nbr={}
        for t,tv in enumerate(s.tris):
            for k in range(3):
                i=s.kid[(t,k)]
                s.nbr[(i,1)]=(s.kid[(t,(k+1)%3)],2)
                s.nbr[(i,2)]=(s.kid[(t,(k-1)%3)],1)
                p,q=tv[k],tv[(k+1)%3]
                if (q,p) in edge:
                    t2,_=edge[(q,p)]; s.nbr[(i,0)]=(s.kid[(t2,s.tris[t2].index(p))],3)
                p,q=tv[(k-1)%3],tv[k]
                if (q,p) in edge:
                    t2,_=edge[(q,p)]; s.nbr[(i,3)]=(s.kid[(t2,s.tris[t2].index(q))],0)
        deg=defaultdict(int)
        for (a,b,c) in s.tris:
            for v in (a,b,c): deg[v]+=1
        s.deg=dict(deg)

def cone_patch(d, R):
    """Apex of degree d, then R-1 further rings of the triangular lattice."""
    A=('a',)
    V=lambda k,i:('r',k,i%(d*k))
    T=[]
    for i in range(d): T.append((A, V(1,i), V(1,i+1)))
    for k in range(1,R):
        for s0 in range(d):
            for j in range(k):
                T.append((V(k,s0*k+j),   V(k+1,s0*(k+1)+j),   V(k+1,s0*(k+1)+j+1)))
                T.append((V(k,s0*k+j),   V(k+1,s0*(k+1)+j+1), V(k,s0*k+j+1)))
            T.append((V(k,s0*k+k), V(k+1,s0*(k+1)+k), V(k+1,s0*(k+1)+k+1)))
    ids={}
    return [tuple(ids.setdefault(v,len(ids)) for v in t) for t in T], ids, A

def placements_patch(kc, info, key, nb):
    adj=[]
    for i in range(8):
        for side in range(4):
            r=nb(i,side)
            if r in key: adj.append((i,side,key[r]))
    tree=[None]*8; order=[0]; seen={0}
    while len(seen)<8:
        for (i,side,j) in adj:
            if i in seen and j not in seen:
                tree[j]=(i,side); seen.add(j); order.append(j); break
    out=[]
    for root in range(len(kc.kites)):
        for c in (0,1):
            sg=(lambda s:s) if c==0 else (lambda s:3-s)
            pos={0:root}; ok=True
            for j in order[1:]:
                i,side=tree[j]
                nxt=kc.nbr.get((pos[i],sg(side)))
                if nxt is None: ok=False; break
                pos[j]=nxt[0]
            if not ok or len(set(pos.values()))!=8: continue
            for (i,side,j) in adj:
                if kc.nbr.get((pos[i],sg(side)))!=(pos[j],3-sg(side)): ok=False; break
            if not ok: continue
            S=set(pos.values()); extra=0
            for i in range(8):
                for side in range(4):
                    n2=kc.nbr.get((pos[i],sg(side)))
                    if n2 and n2[0] in S: extra+=1
            if extra!=len(adj): continue
            out.append(frozenset(S))
    return list(dict.fromkeys(out))

if __name__=="__main__":
    info,key,nb = hat_word()
    print("cover the kites within 2 rings of a cone point of angle 60*d")
    print(" d   cone angle   kites to cover   placements   coverable?")
    for d in (3,4,5,6,7,8,9,10):
        tris,ids,A = cone_patch(d, 6)
        kc=PatchComplex(tris)
        pcs=placements_patch(kc,info,key,nb)
        apex=ids[A]
        # target: every kite of every triangle incident to a vertex within 1 ring
        near=set()
        for t,(a,b,c) in enumerate(kc.tris):
            if apex in (a,b,c):
                for k in range(3): near.add(kc.kid[(t,k)])
        ring2=set(near)
        for t,(a,b,c) in enumerate(kc.tris):
            if any(kc.kid[(t,k)] in near for k in range(3)):
                pass
        ok,sol,nd = exact_cover(near, [p for p in pcs], limit=2_000_000)
        print(" %2d      %4d           %3d          %5d        %s   [%d nodes]" %
              (d, 60*d, len(near), len(pcs), ok, nd))
