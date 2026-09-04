"""Unfold a hat-glued surface into a planar net: hats laid out in the plane along
a spanning tree of the gluing, with the remaining identifications labelled.
Exact -- no numerics."""
import pickle, math
from collections import defaultdict
ns={}
exec(open('/home/user/hat-surfaces/kites.py').read().split("# ---- build")[0], ns)
xy=ns['xy']
exec(open('/home/user/hat-surfaces/png.py').read())
H=pickle.load(open('/home/user/hat-surfaces/hat.pkl','rb'))
PATH=[xy(p) for p in H['path']]

def iso_from(p0,p1,q0,q1):
    """the isometry taking p0->q0, p1->q1 (lengths equal); returns (a,b,c,d,e,f)"""
    ux,uy=p1[0]-p0[0],p1[1]-p0[1]; vx,vy=q1[0]-q0[0],q1[1]-q0[1]
    L=math.hypot(ux,uy)
    cs=(ux*vx+uy*vy)/(L*L); sn=(ux*vy-uy*vx)/(L*L)
    a,b,c,d=cs,-sn,sn,cs
    e=q0[0]-(a*p0[0]+b*p0[1]); f=q0[1]-(c*p0[0]+d*p0[1])
    return (a,b,c,d,e,f)
def refl_from(p0,p1,q0,q1):
    m=(1,0,0,-1,0,0)                      # reflect in the x-axis, then move
    P0=(p0[0],-p0[1]); P1=(p1[0],-p1[1])
    a,b,c,d,e,f = iso_from(P0,P1,q0,q1)
    return (a*1+b*0, a*0+b*(-1), c*1+d*0, c*0+d*(-1), e, f)
def ap(T,p): return (T[0]*p[0]+T[1]*p[1]+T[4], T[2]*p[0]+T[3]*p[1]+T[5])

KCEN=[]
for k in H['cells']:
    pts=[xy(p) for p in k]
    KCEN.append((sum(p[0] for p in pts)/4, sum(p[1] for p in pts)/4))
def kite_ids(T):
    """the 8 kites a placed hat occupies, as rounded lattice keys -- the hat is
    non-convex, so a separating-axis test is invalid; kite occupancy is exact."""
    out=set()
    for c in KCEN:
        p=ap(T,c); out.add((round(p[0]*1000), round(p[1]*1000)))
    return out

def unfold(pairs, N):
    glue=defaultdict(list)
    for (t,i),(u,j) in pairs:
        glue[t].append((i,u,j)); glue[u].append((j,t,i))
    T={0:(1,0,0,1,0,0)}; placed=[0]; used_tree=set()
    frontier=True
    while frontier and len(placed)<N:
        frontier=False
        for t in list(placed):
            for (i,u,j) in glue[t]:
                if u in T: continue
                p0,p1 = ap(T[t],PATH[i]), ap(T[t],PATH[(i+1)%14])
                occupied=set()
                for v in T: occupied|=kite_ids(T[v])
                for mk in (refl_from, iso_from):
                    cand=mk(PATH[j],PATH[(j+1)%14],p1,p0)
                    if kite_ids(cand) & occupied: continue
                    T[u]=cand; placed.append(u); used_tree.add(((t,i),(u,j))); used_tree.add(((u,j),(t,i)))
                    frontier=True; break
                if u in T: break
    return T, used_tree

def draw(pairs, N, fname, title=""):
    T,tree = unfold(pairs,N)
    polys={t:[ap(T[t],p) for p in PATH] for t in T}
    allp=[p for q in polys.values() for p in q]
    mnx=min(x for x,y in allp); mxx=max(x for x,y in allp)
    mny=min(y for x,y in allp); mxy=max(y for x,y in allp)
    S=46; PAD=44
    W=int((mxx-mnx)*S)+2*PAD; Hh=int((mxy-mny)*S)+2*PAD
    img=[[(255,255,255) for _ in range(W)] for _ in range(Hh)]
    def scr(p): return (PAD+(p[0]-mnx)*S, PAD+(mxy-p[1])*S)
    pal=[(226,205,163),(168,201,226),(196,224,178),(228,178,205),(176,222,214),(210,186,228)]
    def fill(poly,col):
        Q=[scr(p) for p in poly]; ys=[q[1] for q in Q]
        for yi in range(int(min(ys)),int(max(ys))+1):
            xs=[]
            for i in range(len(Q)):
                x1,y1=Q[i]; x2,y2=Q[(i+1)%len(Q)]
                if (y1<=yi<y2) or (y2<=yi<y1): xs.append(x1+(yi-y1)*(x2-x1)/(y2-y1))
            xs.sort()
            for k in range(0,len(xs)-1,2):
                for xi in range(int(xs[k]),int(xs[k+1])+1):
                    if 0<=yi<Hh and 0<=xi<W: img[yi][xi]=col
    def seg(p,q,col,w=1):
        x1,y1=scr(p); x2,y2=scr(q); n=int(max(abs(x2-x1),abs(y2-y1)))+1
        for s in range(n+1):
            x=x1+(x2-x1)*s/n; y=y1+(y2-y1)*s/n
            for dx in range(-w,w+1):
                for dy in range(-w,w+1):
                    xi,yi=int(x)+dx,int(y)+dy
                    if 0<=xi<W and 0<=yi<Hh: img[yi][xi]=col
    for t,poly in polys.items(): fill(poly,pal[t%len(pal)])
    for t,poly in polys.items():
        for i in range(14): seg(poly[i],poly[(i+1)%14],(0,0,0),1)
    # mark the identifications that are NOT realised in the plane
    free=[pr for pr in pairs if (pr[0],pr[1]) not in tree]
    marks=[(255,0,0),(0,140,255),(0,170,60),(220,0,220),(255,150,0),(120,60,200),
           (0,190,190),(180,90,0),(90,90,255),(200,0,90),(60,160,120),(150,150,0),(0,0,0),(120,120,120)]
    for n,((t,i),(u,j)) in enumerate(free):
        col=marks[n%len(marks)]
        for (a,b) in (((t,i)),)*0 or [(t,i),(u,j)]:
            if a not in polys: continue
            P=polys[a]; seg(P[b],P[(b+1)%14],col,2)
    write_png(fname,W,Hh,img)
    return len(T), len(free)
