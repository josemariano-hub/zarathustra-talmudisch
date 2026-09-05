"""Kite complexes over surfaces whose faces are arbitrary polygons.

A face with n sides splits into n kites (centroid, edge midpoints, corners).
Cone angles in the kite lattice:
    vertex V        60 * (number of faces meeting there)
    face centre G  120 * (number of sides of the face)     -> 360 iff triangle
    edge midpoint M 180 * (number of faces on the edge)    -> 360 always
So non-triangular faces ARE cone points: a quadrilateral is 480 deg (charge -1),
a bigon is 240 deg (charge +1).  That gives a second, easier way to place
curvature than bending vertex degrees.
"""
from collections import defaultdict, Counter

class PolyKiteComplex:
    def __init__(s, faces):
        s.faces=[tuple(f) for f in faces]
        s.kites=[(t,k) for t,f in enumerate(s.faces) for k in range(len(f))]
        s.kid={kk:i for i,kk in enumerate(s.kites)}
        edge={}
        for t,f in enumerate(s.faces):
            n=len(f)
            for k in range(n):
                p,q=f[k],f[(k+1)%n]
                assert (p,q) not in edge, "orientation clash on %s"%str((p,q))
                edge[(p,q)]=(t,k)
        s.nbr={}
        for t,f in enumerate(s.faces):
            n=len(f)
            for k in range(n):
                i=s.kid[(t,k)]
                s.nbr[(i,1)]=(s.kid[(t,(k+1)%n)],2)
                s.nbr[(i,2)]=(s.kid[(t,(k-1)%n)],1)
                p,q=f[k],f[(k+1)%n]
                t2,_=edge[(q,p)]; s.nbr[(i,0)]=(s.kid[(t2,s.faces[t2].index(p))],3)
                p,q=f[(k-1)%n],f[k]
                t2,_=edge[(q,p)]; s.nbr[(i,3)]=(s.kid[(t2,s.faces[t2].index(q))],0)
        for (i,sd),(j,td) in s.nbr.items():
            assert s.nbr[(j,td)]==(i,sd) and td==3-sd
        s.vdeg=Counter()
        for f in s.faces:
            for v in f: s.vdeg[v]+=1
    def euler(s):
        V=len(s.vdeg); F=len(s.faces); E=sum(len(f) for f in s.faces)//2
        return V-E+F
    def cone_angles(s):
        out={('V',v):60*d for v,d in s.vdeg.items()}
        for t,f in enumerate(s.faces): out[('G',t)]=120*len(f)
        return out

def merge_cycle_torus(m, row=0):
    """Flat torus from the triangular lattice mod m, then delete every edge of
    one straight lattice line, merging each adjacent triangle pair into a quad.
    Each vertex on the line loses exactly two faces -> degree 4 (240 deg);
    each quad centre is 480 deg.  Charges +1 and -1, m of each, summing to 0."""
    V=lambda i,j:(i%m)*m+(j%m)
    tris=[]
    for i in range(m):
        for j in range(m):
            tris.append((V(i,j),V(i+1,j),V(i,j+1)))
            tris.append((V(i+1,j),V(i+1,j+1),V(i,j+1)))
    kill=[(V(i,row),V(i+1,row)) for i in range(m)]        # one straight line
    killset={frozenset(e) for e in kill}
    used=set(); faces=[]
    idx={}
    for t,f in enumerate(tris):
        for k in range(3): idx[frozenset((f[k],f[(k+1)%3]))]=idx.get(frozenset((f[k],f[(k+1)%3])),[])+[t]
    for e in killset:
        a,b=idx[e]
        assert a not in used and b not in used, "two killed edges share a triangle"
        used|={a,b}
        fa,fb=tris[a],tris[b]
        p,q=tuple(e)
        # orient: fa contains directed (p,q) or (q,p)
        if (fa.index(q)-fa.index(p))%3!=1: p,q=q,p
        c=[v for v in fa if v not in (p,q)][0]
        d=[v for v in fb if v not in (p,q)][0]
        faces.append((p,d,q,c))          # quad: p -> d -> q -> c
    for t,f in enumerate(tris):
        if t not in used: faces.append(f)
    return faces
