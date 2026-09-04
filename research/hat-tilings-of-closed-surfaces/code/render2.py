exec(open('/home/user/hat-surfaces/kites.py').read().split("# ---- build")[0])
exec(open('/home/user/hat-surfaces/png.py').read())
import pickle
from math import sqrt, atan2, degrees, pi, cos, sin, radians
winners = pickle.load(open('/home/user/hat-surfaces/tileab.pkl','rb'))
sel=[(i,c,p) for i,c,p in winners if i in (8,22)]
S=46; PAD=26
def rotpts(pts,ang,flip):
    out=[]
    for (x,y) in pts:
        if flip: x=-x
        out.append((x*cos(ang)-y*sin(ang), x*sin(ang)+y*cos(ang)))
    return out
rows=[]
for idx,cells,path in sel:
    poly=[xy(q) for q in path]
    kits=[[xy(q) for q in KITE4[c]] for c in cells] if False else None
    for flip in (0,1):
        for r in range(6):
            rows.append((idx,flip,r,rotpts(poly, radians(60*r), flip)))
# layout grid: 2 tiles x 2 flips x 6 rots -> 4 rows of 6
allp=[p for _,_,_,poly in rows for p in poly]
w=max(x for x,y in allp)-min(x for x,y in allp); h=max(y for x,y in allp)-min(y for x,y in allp)
CW=int(w*S)+2*PAD; CH=int(h*S)+2*PAD
IW=CW*6; IH=CH*4
img=[[(255,255,255) for _ in range(IW)] for _ in range(IH)]
def draw(poly,cx,cy,color):
    mx=min(x for x,y in poly); My=max(y for x,y in poly)
    P=[(cx*CW+PAD+(x-mx)*S, cy*CH+PAD+(My-y)*S) for x,y in poly]
    ys=[p[1] for p in P]
    for yi in range(int(min(ys)),int(max(ys))+1):
        xs=[]
        for i in range(len(P)):
            x1,y1=P[i]; x2,y2=P[(i+1)%len(P)]
            if (y1<=yi<y2) or (y2<=yi<y1): xs.append(x1+(yi-y1)*(x2-x1)/(y2-y1))
        xs.sort()
        for k in range(0,len(xs)-1,2):
            for xi in range(int(xs[k]),int(xs[k+1])+1):
                if 0<=yi<IH and 0<=xi<IW: img[yi][xi]=color
    for i in range(len(P)):
        x1,y1=P[i]; x2,y2=P[(i+1)%len(P)]
        n=int(max(abs(x2-x1),abs(y2-y1)))+1
        for t in range(n+1):
            x=x1+(x2-x1)*t/n; y=y1+(y2-y1)*t/n
            for dx in(-1,0,1):
                for dy in(-1,0,1):
                    xi,yi=int(x)+dx,int(y)+dy
                    if 0<=yi<IH and 0<=xi<IW: img[yi][xi]=(0,0,0)
for n,(idx,flip,r,poly) in enumerate(rows):
    row = (0 if idx==8 else 2)+flip
    draw(poly, r, row, (190,220,190) if idx==8 else (220,200,190))
write_png('/home/user/hat-surfaces/orient.png',IW,IH,img)
print("rows 0-1: candidate 8 (unflipped/flipped); rows 2-3: candidate 22")
