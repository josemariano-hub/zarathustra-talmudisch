"""Take a gluing, build the exact triangulated metric surface, embed it in R^3
by constraint relaxation, and render it."""
exec(open('/home/user/hat-surfaces/kites.py').read().split("# ---- build")[0])
exec(open('/home/user/hat-surfaces/png.py').read())
import pickle, math, random
H=pickle.load(open('/home/user/hat-surfaces/hat.pkl','rb'))
PATH=H['path']; CELLS=[tuple(c) for c in H['cells']]

def kcycle(k):
    """kite corners in CCW order V, M, G, M -- orientation matters, the mesh
    normals are built from it."""
    V=[p for p in k if ptype(p)=='V']; M=[p for p in k if ptype(p)=='M']; G=[p for p in k if ptype(p)=='G']
    c=(V[0],M[0],G[0],M[1])
    a=0.0
    for i in range(4):
        (x1,y1)=xy(c[i]); (x2,y2)=xy(c[(i+1)%4]); a+=x1*y2-x2*y1
    return c if a>0 else (V[0],M[1],G[0],M[0])

class DSU:
    def __init__(s): s.p={}
    def add(s,x): s.p.setdefault(x,x)
    def f(s,x):
        s.add(x)
        while s.p[x]!=x: s.p[x]=s.p[s.p[x]]; x=s.p[x]
        return x
    def u(s,a,b): s.p[s.f(a)]=s.f(b)

def build(pairs, N):
    d=DSU()
    for t in range(N):
        for k in CELLS:
            for p in k: d.add((t,p))
    for (t,i),(u,j) in pairs:
        d.u((t,PATH[i]),        (u,PATH[(j+1)%14]))
        d.u((t,PATH[(i+1)%14]), (u,PATH[j]))
    idx={}; 
    def gid(t,p):
        r=d.f((t,p))
        if r not in idx: idx[r]=len(idx)
        return idx[r]
    tris=[]; tilepolys=[]
    for t in range(N):
        for k in CELLS:
            V,M1,G,M2 = kcycle(k)
            a,b,c,e = gid(t,V),gid(t,M1),gid(t,G),gid(t,M2)
            tris.append((a,b,c,t)); tris.append((a,c,e,t))
        tilepolys.append([gid(t,p) for p in PATH])
    # exact target lengths from the local planar geometry
    cons={}
    for t in range(N):
        for k in CELLS:
            V,M1,G,M2 = kcycle(k)
            for (p,q) in ((V,M1),(M1,G),(G,M2),(M2,V),(V,G)):
                a,b=gid(t,p),gid(t,q)
                cons[(min(a,b),max(a,b))]=dist(p,q)
    return len(idx), tris, [(a,b,L) for (a,b),L in cons.items()], tilepolys

def embed(nv, tris, cons, shape, iters=6000, seed=1, verbose=False):
    """Realize the metric in R^3: exact edge lengths, plus a decaying radial
    inflation and short-range repulsion that steer the relaxation to the
    embedded (star-shaped / convex) branch instead of a crumpled immersion."""
    rng=random.Random(seed)
    nbr=set()
    for (a,b,L) in cons: nbr.add((min(a,b),max(a,b)))
    Lmax=max(L for _,_,L in cons)
    P=[[rng.gauss(0,1) for _ in range(3)] for _ in range(nv)]
    if shape!='sphere':
        for i in range(nv):
            th=rng.uniform(0,2*math.pi); ph=rng.uniform(0,2*math.pi); R,rr=7.0,3.0
            P[i]=[(R+rr*math.cos(ph))*math.cos(th),(R+rr*math.cos(ph))*math.sin(th),rr*math.sin(ph)]
    for it in range(iters):
        frac=it/iters
        cx=sum(p[0] for p in P)/nv; cy=sum(p[1] for p in P)/nv; cz=sum(p[2] for p in P)/nv
        if shape=='sphere' and frac<0.55:            # radial inflation
            k=Lmax*0.30*(1-frac/0.55)
            for p in P:
                dx,dy,dz=p[0]-cx,p[1]-cy,p[2]-cz
                r=math.sqrt(dx*dx+dy*dy+dz*dz) or 1e-9
                p[0]+=k*dx/r; p[1]+=k*dy/r; p[2]+=k*dz/r
        if frac<0.55:                                # untangle
            rep=Lmax*0.85
            for i in range(nv):
                for j in range(i+1,nv):
                    if (i,j) in nbr: continue
                    dx=P[j][0]-P[i][0]; dy=P[j][1]-P[i][1]; dz=P[j][2]-P[i][2]
                    d2=dx*dx+dy*dy+dz*dz
                    if 1e-12<d2<rep*rep:
                        d=math.sqrt(d2); f=0.08*(rep-d)/d
                        P[i][0]-=f*dx; P[i][1]-=f*dy; P[i][2]-=f*dz
                        P[j][0]+=f*dx; P[j][1]+=f*dy; P[j][2]+=f*dz
        for _ in range(4):                           # exact edge lengths
            for (a,b,L) in cons:
                dx=P[b][0]-P[a][0]; dy=P[b][1]-P[a][1]; dz=P[b][2]-P[a][2]
                cur=math.sqrt(dx*dx+dy*dy+dz*dz) or 1e-9
                f=0.5*(cur-L)/cur
                P[a][0]+=f*dx; P[a][1]+=f*dy; P[a][2]+=f*dz
                P[b][0]-=f*dx; P[b][1]-=f*dy; P[b][2]-=f*dz
    V=0.0
    for (a,b,c,_) in tris:
        A,B,C=P[a],P[b],P[c]
        V+=(A[0]*(B[1]*C[2]-B[2]*C[1])+A[1]*(B[2]*C[0]-B[0]*C[2])+A[2]*(B[0]*C[1]-B[1]*C[0]))
    if V<0:
        for i in range(len(tris)):
            a,b,c,t=tris[i]; tris[i]=(a,c,b,t)
    err=[abs(math.dist(P[a],P[b])-L)/L for (a,b,L) in cons]
    return P, max(err), sum(err)/len(err)
