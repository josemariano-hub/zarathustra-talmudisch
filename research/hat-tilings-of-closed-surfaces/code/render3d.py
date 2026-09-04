import math
def render(P, tris, tilepolys, fname, W=900, Hh=900, elev=22, azim=35, bg=(255,255,255),
           palette=None, edge=(20,20,20), lw=1):
    ca,sa=math.cos(math.radians(azim)),math.sin(math.radians(azim))
    ce,se=math.cos(math.radians(elev)),math.sin(math.radians(elev))
    cx=sum(p[0] for p in P)/len(P); cy=sum(p[1] for p in P)/len(P); cz=sum(p[2] for p in P)/len(P)
    def view(p):
        x,y,z=p[0]-cx,p[1]-cy,p[2]-cz
        x1= ca*x+sa*y; y1=-sa*x+ca*y
        y2= ce*y1+se*z; z2=-se*y1+ce*z
        return (x1,y2,z2)
    Q=[view(p) for p in P]
    mx=max(max(abs(q[0]),abs(q[1])) for q in Q)
    S=0.42*min(W,Hh)/mx
    def scr(q): return (W/2+q[0]*S, Hh/2-q[1]*S)
    img=[[bg for _ in range(W)] for _ in range(Hh)]
    zb=[[-1e18]*W for _ in range(Hh)]
    if palette is None:
        palette=[(232,196,150),(150,196,232),(196,232,150),(232,150,196),
                 (150,232,214),(214,150,232),(232,214,150),(170,210,240)]
    L=(0.45,0.5,0.74)
    order=sorted(range(len(tris)), key=lambda i: sum(Q[v][2] for v in tris[i][:3])/3)
    for i in order:
        a,b,c,t=tris[i]
        A,B,C=Q[a],Q[b],Q[c]
        ux,uy,uz=B[0]-A[0],B[1]-A[1],B[2]-A[2]
        vx,vy,vz=C[0]-A[0],C[1]-A[1],C[2]-A[2]
        nx,ny,nz=uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx
        nl=math.sqrt(nx*nx+ny*ny+nz*nz) or 1e-9
        if nz<0: continue                          # back face
        sh=0.42+0.58*max(0.0,(nx*L[0]+ny*L[1]+nz*L[2])/nl)
        col=palette[t%len(palette)]
        col=tuple(min(255,int(ch*sh)) for ch in col)
        p1,p2,p3=scr(A),scr(B),scr(C)
        ys=[p1[1],p2[1],p3[1]]
        for yi in range(max(0,int(min(ys))),min(Hh-1,int(max(ys)))+1):
            xs=[]
            for (s1,s2,q1,q2) in ((p1,p2,A,B),(p2,p3,B,C),(p3,p1,C,A)):
                if (s1[1]<=yi<s2[1]) or (s2[1]<=yi<s1[1]):
                    u=(yi-s1[1])/(s2[1]-s1[1])
                    xs.append((s1[0]+u*(s2[0]-s1[0]), q1[2]+u*(q2[2]-q1[2])))
            xs.sort()
            for k in range(0,len(xs)-1,2):
                x0,z0=xs[k]; x1,z1=xs[k+1]
                n=max(1,int(x1-x0))
                for xi in range(max(0,int(x0)),min(W-1,int(x1))+1):
                    u=(xi-x0)/(x1-x0) if x1>x0 else 0
                    z=z0+u*(z1-z0)
                    if z>zb[yi][xi]: zb[yi][xi]=z; img[yi][xi]=col
    # tile outlines, depth tested against the z-buffer
    for poly in tilepolys:
        n=len(poly)
        for i in range(n):
            A,B=Q[poly[i]],Q[poly[(i+1)%n]]
            p1,p2=scr(A),scr(B)
            steps=int(max(abs(p2[0]-p1[0]),abs(p2[1]-p1[1])))+1
            for s in range(steps+1):
                u=s/steps
                x=p1[0]+u*(p2[0]-p1[0]); y=p1[1]+u*(p2[1]-p1[1]); z=A[2]+u*(B[2]-A[2])
                for dx in range(-lw,lw+1):
                    for dy in range(-lw,lw+1):
                        xi,yi=int(x)+dx,int(y)+dy
                        if 0<=xi<W and 0<=yi<Hh and z>zb[yi][xi]-0.35:
                            img[yi][xi]=edge
    exec(open('/home/user/hat-surfaces/png.py').read(), globals())
    write_png(fname,W,Hh,img)
    return fname
