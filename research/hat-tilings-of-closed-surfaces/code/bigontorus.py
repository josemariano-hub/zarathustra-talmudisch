"""Complexes with an EXPLICIT side pairing, so bigons (parallel edges) are legal.

Insert a bigon on every edge of a closed cycle in the flat torus.  Each bigon
is a +1 disclination (240 deg at its centre); each vertex of the cycle gains
two faces, going from degree 6 to degree 8, a -1 disclination (480 deg).  With
a cycle of length L that is L positive and L negative charges: total zero, a
torus.  This mirrors the 6-hat sphere, whose positive charge also lives on
bigons rather than on low-degree vertices.
"""
from collections import defaultdict, Counter

class PairedComplex:
    def __init__(s, faces, pair):
        s.faces=[tuple(f) for f in faces]          # f = tuple of vertex ids
        s.pair=dict(pair)                          # (face,side) -> (face,side)
        s.kites=[(t,k) for t,f in enumerate(s.faces) for k in range(len(f))]
        s.kid={kk:i for i,kk in enumerate(s.kites)}
        for a,b in s.pair.items(): assert s.pair[b]==a, "pairing not involutive"
        s.nbr={}
        for t,f in enumerate(s.faces):
            n=len(f)
            for k in range(n):
                i=s.kid[(t,k)]
                s.nbr[(i,1)]=(s.kid[(t,(k+1)%n)],2)
                s.nbr[(i,2)]=(s.kid[(t,(k-1)%n)],1)
                # side 0 of kite k lies on face-side k (from f[k] to f[k+1])
                t2,k2=s.pair[(t,k)]
                s.nbr[(i,0)]=(s.kid[(t2,(k2+1)%len(s.faces[t2]))],3)
                t3,k3=s.pair[(t,(k-1)%n)]
                s.nbr[(i,3)]=(s.kid[(t3,k3)],0)
        for (i,sd),(j,td) in s.nbr.items():
            assert s.nbr[(j,td)]==(i,sd), "kite gluing not involutive at %s"%str((i,sd))
            assert td==3-sd
        # vertex classes: walk the corner cycles
        s.vclass={}; c=0
        seen=set()
        for t,f in enumerate(s.faces):
            for k in range(len(f)):
                if (t,k) in seen: continue
                cyc=[]; cur=(t,k)
                while cur not in seen:
                    seen.add(cur); cyc.append(cur)
                    tt,kk=cur
                    t2,k2=s.pair[(tt,(kk-1)%len(s.faces[tt]))]
                    cur=(t2,k2)
                for x in cyc: s.vclass[x]=c
                c+=1
        s.vdeg=Counter(s.vclass.values())
    def euler(s):
        V=len(s.vdeg); F=len(s.faces); E=len(s.pair)//2
        return V-E+F
    def cone_angles(s):
        out={('V',v):60*d for v,d in s.vdeg.items()}
        for t,f in enumerate(s.faces): out[('G',t)]=120*len(f)
        return out

def bigon_torus(m, row=0):
    V=lambda i,j:(i%m)*m+(j%m)
    tris=[]
    for i in range(m):
        for j in range(m):
            tris.append((V(i,j),V(i+1,j),V(i,j+1)))
            tris.append((V(i+1,j),V(i+1,j+1),V(i,j+1)))
    side_of={}
    for t,f in enumerate(tris):
        for k in range(3): side_of[(f[k],f[(k+1)%3])]=(t,k)
    cyc=[(V(i,row),V(i+1,row)) for i in range(m)]
    faces=[list(f) for f in tris]; pair={}
    done=set()
    for (u,v) in cyc:
        t1,k1=side_of[(u,v)]; t2,k2=side_of[(v,u)]
        b=len(faces); faces.append([u,v])           # bigon: sides 0=(u,v), 1=(v,u)
        pair[(t1,k1)]=(b,1); pair[(b,1)]=(t1,k1)
        pair[(t2,k2)]=(b,0); pair[(b,0)]=(t2,k2)
        done|={(u,v),(v,u)}
    for (p,q),(t,k) in side_of.items():
        if (p,q) in done: continue
        t2,k2=side_of[(q,p)]
        pair[(t,k)]=(t2,k2)
    return faces, pair
