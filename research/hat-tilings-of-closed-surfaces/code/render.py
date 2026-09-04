exec(open('/home/user/hat-surfaces/kites.py').read().split("# ---- build")[0])
exec(open('/home/user/hat-surfaces/png.py').read())
import pickle
from math import sqrt, atan2, degrees, pi
cands = pickle.load(open('/home/user/hat-surfaces/cands.pkl','rb'))
def signed_area(path):
    s=0
    for i in range(len(path)):
        (x1,y1)=xy(path[i]); (x2,y2)=xy(path[(i+1)%len(path)]); s+=x1*y2-x2*y1
    return s/2
def angles(path):
    n=len(path)
    if signed_area(path)<0: path=path[::-1]
    out=[]
    for i in range(n):
        p=xy(path[i-1]); q=xy(path[i]); r=xy(path[(i+1)%n])
        a1=atan2(p[1]-q[1],p[0]-q[0]); a2=atan2(r[1]-q[1],r[0]-q[0])
        out.append(round(degrees((a1-a2)%(2*pi))))
    return path,out

sel=[]
for idx,(cells,path) in enumerate(cands):
    p,a = angles(path)
    if sum(1 for x in a if x==180)==1: sel.append((idx,cells,p,a))

S=42; PAD=30
COLS=len(sel)
# bounding box over all
allpts=[xy(q) for _,_,p,_ in sel for q in p]
W=int(max(x for x,y in allpts)*S-min(x for x,y in allpts)*S)+2*PAD
H=int(max(y for x,y in allpts)*S-min(y for x,y in allpts)*S)+2*PAD
IW=W*COLS; IH=H
img=[[(255,255,255) for _ in range(IW)] for _ in range(IH)]
minx=min(x for x,y in allpts); maxy=max(y for x,y in allpts)
def px(pt,col):
    x,y=xy(pt); return (col*W+PAD+(x-minx)*S, PAD+(maxy-y)*S)
def fill(poly,col,color):
    P=[px(q,col) for q in poly]
    ys=[p[1] for p in P]
    for yi in range(int(min(ys)),int(max(ys))+1):
        xs=[]
        for i in range(len(P)):
            x1,y1=P[i]; x2,y2=P[(i+1)%len(P)]
            if (y1<=yi<y2) or (y2<=yi<y1):
                xs.append(x1+(yi-y1)*(x2-x1)/(y2-y1))
        xs.sort()
        for k in range(0,len(xs)-1,2):
            for xi in range(int(xs[k]),int(xs[k+1])+1):
                if 0<=yi<IH and 0<=xi<IW: img[yi][xi]=color
def line(p,q,col,color):
    x1,y1=px(p,col); x2,y2=px(q,col)
    n=int(max(abs(x2-x1),abs(y2-y1)))+1
    for i in range(n+1):
        x=x1+(x2-x1)*i/n; y=y1+(y2-y1)*i/n
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                xi,yi=int(x)+dx,int(y)+dy
                if 0<=yi<IH and 0<=xi<IW: img[yi][xi]=color
for col,(idx,cells,p,a) in enumerate(sel):
    fill(p,col,(190,220,190))
    for c in cells:
        k=KITES_LOOKUP[c] if False else c
    for i in range(len(p)):
        line(p[i],p[(i+1)%len(p)],col,(0,0,0))
write_png('/home/user/hat-surfaces/candidates.png',IW,IH,img)
for idx,cells,p,a in sel:
    print("cand",idx,"angle cycle:",a)
print("wrote candidates.png, order:", [s[0] for s in sel])
