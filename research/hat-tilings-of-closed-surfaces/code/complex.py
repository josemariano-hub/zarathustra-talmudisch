"""Closed surfaces as equilateral triangulations, their kite complexes, and hat
placements on them.

A closed surface built from equilateral triangles is a flat cone surface: every
vertex of degree d has cone angle 60d, so degree 6 is flat, 5 is a +60 deg
disclination, 7 is -60 deg.  Splitting each triangle into 3 kites reproduces the
kite lattice away from the cone points, so the hat lives on it verbatim.

Kite (t,k) = corner k of triangle t.  Sides, cyclically:
   0: V - M1   (half of triangle edge k -> k+1)
   1: M1 - G
   2: G  - M2
   3: M2 - V   (half of triangle edge k-1 -> k)
Side 1 pairs with side 2 inside a triangle; sides 0 and 3 pair across triangle
edges.  In every case the partner side is 3 - side.
"""
import pickle
from collections import defaultdict

class KiteComplex:
    def __init__(s, tris):
        """tris: list of (v0,v1,v2), consistently oriented, closed surface."""
        s.tris=tris
        s.kites=[(t,k) for t in range(len(tris)) for k in range(3)]
        s.kid={kk:i for i,kk in enumerate(s.kites)}
        edge={}
        for t,(a,b,c) in enumerate(tris):
            for k,(p,q) in enumerate(((a,b),(b,c),(c,a))):
                if (p,q) in edge: raise ValueError("edge %s used twice - orientation is wrong"%str((p,q)))
                edge[(p,q)]=(t,k)
        s.nbr={}
        for t,tv in enumerate(tris):
            for k in range(3):
                i=s.kid[(t,k)]
                s.nbr[(i,1)]=(s.kid[(t,(k+1)%3)],2)
                s.nbr[(i,2)]=(s.kid[(t,(k-1)%3)],1)
                # side 0 lies on triangle edge (v_k, v_{k+1})
                p,q=tv[k],tv[(k+1)%3]
                t2,k2=edge[(q,p)]
                j=s.tris[t2].index(p)
                s.nbr[(i,0)]=(s.kid[(t2,j)],3)
                # side 3 lies on triangle edge (v_{k-1}, v_k)
                p,q=tv[(k-1)%3],tv[k]
                t2,k2=edge[(q,p)]
                j=s.tris[t2].index(q)
                s.nbr[(i,3)]=(s.kid[(t2,j)],0)
        for (i,sd),(j,td) in s.nbr.items():
            assert s.nbr[(j,td)]==(i,sd), "kite gluing not involutive"
            assert td==3-sd, "partner side must be 3-side"
        deg=defaultdict(int)
        for t,(a,b,c) in enumerate(tris):
            for v in (a,b,c): deg[v]+=1
        s.deg=dict(deg)
    def cone_angles(s): return {v:60*d for v,d in s.deg.items()}
    def euler(s):
        V=len(s.deg); F=len(s.tris); E=3*F//2
        return V-E+F

def hat_word():
    """The hat's 8 kites as a rooted spanning tree of side crossings, plus every
    internal adjacency, expressed in the (kite, side) language above."""
    import math
    ns={}
    exec(open('/home/user/hat-surfaces/kites.py').read().split("# ---- build")[0], ns)
    xy=ns['xy']; ptype=ns['ptype']; kites_of=ns['kites_of']; tri_pts=ns['tri_pts']
    H=pickle.load(open('/home/user/hat-surfaces/hat.pkl','rb'))
    cells=[tuple(c) for c in H['cells']]
    # locate each hat kite as (triangle, corner) in the plane lattice
    tri_of={}
    for a in range(-6,7):
        for b in range(-6,7):
            for kind in ('u','d'):
                A,B,C,G = tri_pts((kind,a,b))
                verts=(A,B,C) if _ccw(xy,(A,B,C)) else (A,C,B)
                for k in range(3):
                    V=verts[k]; M1=_mid(V,verts[(k+1)%3]); M2=_mid(V,verts[(k-1)%3])
                    tri_of[tuple(sorted((V,M1,G,M2)))]=((kind,a,b),verts,k,G)
    info=[tri_of[c] for c in cells]
    key={}
    for idx,(tri,verts,k,G) in enumerate(info): key[(tri,k)]=idx
    def nb(idx, side):
        tri,verts,k,G = info[idx]
        if side==1: return (tri,(k+1)%3)
        if side==2: return (tri,(k-1)%3)
        if side==0: p,q=verts[k],verts[(k+1)%3]
        else:       p,q=verts[(k-1)%3],verts[k]
        for (tri2,verts2,k2,G2) in _alltri(xy,tri_pts):
            if verts2[k2]==(p if side==0 else q) and _mid(p,q) in (_mid(verts2[k2],verts2[(k2+1)%3]),
                                                                  _mid(verts2[k2],verts2[(k2-1)%3])):
                if tri2!=tri: return (tri2,k2)
        return None
    return info, key, nb

def _ccw(xy,V):
    (x1,y1),(x2,y2),(x3,y3)=[xy(p) for p in V]
    return (x2-x1)*(y3-y1)-(y2-y1)*(x3-x1) > 0
def _mid(p,q): return ((p[0]+q[0])//2,(p[1]+q[1])//2)
_ALL=None
def _alltri(xy,tri_pts):
    global _ALL
    if _ALL is None:
        _ALL=[]
        for a in range(-7,8):
            for b in range(-7,8):
                for kind in ('u','d'):
                    A,B,C,G=tri_pts((kind,a,b))
                    verts=(A,B,C) if _ccw(xy,(A,B,C)) else (A,C,B)
                    for k in range(3): _ALL.append(((kind,a,b),verts,k,G))
    return _ALL

# ---------------------------------------------------------------- surfaces
def flat_torus(m):
    """Triangular lattice modulo m*Z^2: every vertex degree 6, so a FLAT torus."""
    V=lambda i,j:(i%m)*m+(j%m)
    T=[]
    for i in range(m):
        for j in range(m):
            T.append((V(i,j),V(i+1,j),V(i,j+1)))
            T.append((V(i+1,j),V(i+1,j+1),V(i,j+1)))
    return T

def flip_edge(tris, e=0):
    """One diagonal flip turns four degree-6 vertices into 5,5,7,7:
    a cone torus with two +60 and two -60 disclinations, total charge 0."""
    tris=[tuple(t) for t in tris]
    edge={}
    for t,(a,b,c) in enumerate(tris):
        for (p,q) in ((a,b),(b,c),(c,a)): edge[(p,q)]=t
    for (p,q),t1 in sorted(edge.items()):
        t2=edge.get((q,p))
        if t2 is None or t2==t1: continue
        A=[v for v in tris[t1] if v not in (p,q)]
        B=[v for v in tris[t2] if v not in (p,q)]
        if len(A)!=1 or len(B)!=1: continue
        c,d=A[0],B[0]
        if c==d: continue
        new=list(tris)
        new[t1]=(c,d,q); new[t2]=(d,c,p)
        try:
            KiteComplex(new); 
        except ValueError:
            continue
        if e==0: return new
        e-=1
    raise RuntimeError("no flippable edge")

ICO_F=[(0,11,5),(0,5,1),(0,1,7),(0,7,10),(0,10,11),(1,5,9),(5,11,4),(11,10,2),(10,7,6),(7,1,8),
       (3,9,4),(3,4,2),(3,2,6),(3,6,8),(3,8,9),(4,9,5),(2,4,11),(6,2,10),(8,6,7),(9,8,1)]
OCT_F=[(0,1,2),(0,2,3),(0,3,4),(0,4,1),(5,2,1),(5,3,2),(5,4,3),(5,1,4)]
def subdivide(FACES, n):
    """Each face cut into n^2 equilateral triangles.  Original polyhedron
    vertices keep their degree (a cone point); everything else is flat."""
    def gid(f,j,k):
        a,b,c=FACES[f]; i=n-j-k
        if i==n: return ('c',a)
        if j==n: return ('c',b)
        if k==n: return ('c',c)
        if i==0: return ('e',)+(tuple(sorted((b,c)))+((k,) if b<c else (j,)))
        if j==0: return ('e',)+(tuple(sorted((c,a)))+((i,) if c<a else (k,)))
        if k==0: return ('e',)+(tuple(sorted((a,b)))+((j,) if a<b else (i,)))
        return ('i',f,j,k)
    T=[]
    for f in range(len(FACES)):
        for j in range(n+1):
            for k in range(n+1-j):
                if j+k<=n-1: T.append((gid(f,j,k),gid(f,j+1,k),gid(f,j,k+1)))
                if j+k<=n-2: T.append((gid(f,j+1,k),gid(f,j+1,k+1),gid(f,j,k+1)))
    keys={}
    return [tuple(keys.setdefault(v,len(keys)) for v in t) for t in T], keys

def octasphere(n): return subdivide(OCT_F, n)

def icosphere(n):
    """Icosahedron with each face cut into n^2 equilateral triangles.
    12 vertices keep degree 5 (cone angle 300 deg, charge +1); all others are
    flat.  Total charge 12 -- the minimum a sphere allows."""
    vid={}
    def gid(f,j,k):
        a,b,c=ICO_F[f]; i=n-j-k
        if i==n: return ('c',a)
        if j==n: return ('c',b)
        if k==n: return ('c',c)
        if i==0: return ('e',)+ (tuple(sorted((b,c))) + ((k,) if b<c else (j,)))
        if j==0: return ('e',)+ (tuple(sorted((c,a))) + ((i,) if c<a else (k,)))
        if k==0: return ('e',)+ (tuple(sorted((a,b))) + ((j,) if a<b else (i,)))
        return ('i',f,j,k)
    T=[]
    for f in range(20):
        for j in range(n+1):
            for k in range(n+1-j):
                if j+k<=n-1: T.append((gid(f,j,k),gid(f,j+1,k),gid(f,j,k+1)))
                if j+k<=n-2: T.append((gid(f,j+1,k),gid(f,j+1,k+1),gid(f,j,k+1)))
    keys={}; out=[]
    for t in T: out.append(tuple(keys.setdefault(v,len(keys)) for v in t))
    return out, keys

# ------------------------------------------------------- hat placements
def placements(kc, info, key, nb):
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
            sg=(lambda s: s) if c==0 else (lambda s: 3-s)
            pos={0:root}; bad=False
            for j in order[1:]:
                i,side=tree[j]
                pos[j]=kc.nbr[(pos[i],sg(side))][0]
            if len(set(pos.values()))!=8: continue
            for (i,side,j) in adj:
                if kc.nbr[(pos[i],sg(side))]!=(pos[j],3-sg(side)): bad=True; break
            if bad: continue
            # the image must have EXACTLY the hat's internal adjacencies -- an
            # extra one means the patch has wrapped around a cone point and is
            # not an isometric copy of the hat
            S=set(pos.values()); extra=0
            for i in range(8):
                for side in range(4):
                    if kc.nbr[(pos[i],sg(side))][0] in S: extra+=1
            if extra!=len(adj): continue
            out.append(frozenset(pos[i] for i in range(8)))
    return list(dict.fromkeys(out))

def exact_cover(universe, pieces, limit=8_000_000):
    from collections import defaultdict
    c2p=defaultdict(list)
    for i,p in enumerate(pieces):
        for c in p: c2p[c].append(i)
    unc=set(universe); used=set(); sol=[]; nodes=[0]
    def go():
        nodes[0]+=1
        if nodes[0]>limit: raise TimeoutError
        if not unc: return True
        c=min(unc,key=lambda c: sum(1 for i in c2p[c] if not (pieces[i]&used)))
        for i in c2p[c]:
            if pieces[i]&used: continue
            used.update(pieces[i]); unc.difference_update(pieces[i]); sol.append(i)
            if go(): return True
            used.difference_update(pieces[i]); unc.update(pieces[i]); sol.pop()
        return False
    try: return go(), [pieces[i] for i in sol], nodes[0]
    except TimeoutError: return None, [], nodes[0]
