exec(open('/home/user/hat-surfaces/double.py').read().split("tiles=[poly_of")[0])
exec(open('/home/user/hat-surfaces/png.py').read())
tiles=[poly_of(pc) for pc in sol]
S=30; PAD=20
allp=[xy(v) for P in tiles for v in P]
mnx=min(x for x,y in allp); mxx=max(x for x,y in allp)
mny=min(y for x,y in allp); mxy=max(y for x,y in allp)
IW=int((mxx-mnx)*S)+2*PAD; IH=int((mxy-mny)*S)+2*PAD
img=[[(255,255,255) for _ in range(IW)] for _ in range(IH)]
def T(v):
    x,y=xy(v); return (PAD+(x-mnx)*S, PAD+(mxy-y)*S)
import random
random.seed(7)
def orient(P):
    # reflected or not: compare cyclic angle sequence to the reference
    return 0
for P in tiles:
    Q=[T(v) for v in P]
    # colour by chirality: use signed order of the 270-270 separation
    col=(196,222,196)
    ys=[p[1] for p in Q]
    for yi in range(int(min(ys)),int(max(ys))+1):
        xs=[]
        for i in range(len(Q)):
            x1,y1=Q[i]; x2,y2=Q[(i+1)%len(Q)]
            if (y1<=yi<y2) or (y2<=yi<y1): xs.append(x1+(yi-y1)*(x2-x1)/(y2-y1))
        xs.sort()
        for k in range(0,len(xs)-1,2):
            for xi in range(int(xs[k]),int(xs[k+1])+1):
                if 0<=yi<IH and 0<=xi<IW: img[yi][xi]=col
    for i in range(len(Q)):
        x1,y1=Q[i]; x2,y2=Q[(i+1)%len(Q)]
        n=int(max(abs(x2-x1),abs(y2-y1)))+1
        for t in range(n+1):
            x=x1+(x2-x1)*t/n; y=y1+(y2-y1)*t/n
            for dx in(0,1):
                for dy in(0,1):
                    xi,yi=int(x)+dx,int(y)+dy
                    if 0<=yi<IH and 0<=xi<IW: img[yi][xi]=(0,0,0)
write_png('/home/user/hat-surfaces/patch.png',IW,IH,img)
print("wrote patch.png", IW, IH, len(tiles),"tiles")
