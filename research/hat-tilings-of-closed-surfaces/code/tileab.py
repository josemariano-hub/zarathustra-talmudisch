"""Decisive test: the hat belongs to a CONTINUUM Tile(a,b). A 14-gon whose edges
are labelled 'a' (the 8 short ones) and 'b' (the 6 long ones) survives arbitrary
independent rescaling of a and b iff  sum(unit vectors of a-edges) = 0  AND
sum(unit vectors of b-edges) = 0.  Only the Tile(a,b) family satisfies this."""
exec(open('/home/user/hat-surfaces/kites.py').read().split("# ---- build")[0])
import pickle
from math import sqrt, atan2, degrees, pi, cos, sin
cands = pickle.load(open('/home/user/hat-surfaces/cands.pkl','rb'))
def signed_area(path):
    s=0
    for i in range(len(path)):
        (x1,y1)=xy(path[i]); (x2,y2)=xy(path[(i+1)%len(path)]); s+=x1*y2-x2*y1
    return s/2
def prep(path):
    if signed_area(path)<0: path=path[::-1]
    n=len(path); out=[]
    for i in range(n):
        p=xy(path[i]); q=xy(path[(i+1)%n])
        L=sqrt((q[0]-p[0])**2+(q[1]-p[1])**2)
        d=((q[0]-p[0])/L,(q[1]-p[1])/L)
        out.append(('a' if abs(L-1)<1e-9 else 'b', d, round(degrees(atan2(d[1],d[0])))%360))
    return path,out
def angseq(path):
    if signed_area(path)<0: path=path[::-1]
    n=len(path); out=[]
    for i in range(n):
        p=xy(path[i-1]); q=xy(path[i]); r=xy(path[(i+1)%n])
        out.append(round(degrees((atan2(p[1]-q[1],p[0]-q[0])-atan2(r[1]-q[1],r[0]-q[0]))%(2*pi))))
    return out
print("idx  |sum a-dirs|  |sum b-dirs|   in Tile(a,b) family?")
winners=[]
for idx,(cells,path) in enumerate(cands):
    p,ed = prep(path)
    sa=(sum(d[0] for t,d,_ in ed if t=='a'), sum(d[1] for t,d,_ in ed if t=='a'))
    sb=(sum(d[0] for t,d,_ in ed if t=='b'), sum(d[1] for t,d,_ in ed if t=='b'))
    na=sqrt(sa[0]**2+sa[1]**2); nb=sqrt(sb[0]**2+sb[1]**2)
    ok = na<1e-9 and nb<1e-9
    if ok: winners.append((idx,cells,p,ed))
    print("%3d  %9.5f  %9.5f   %s"%(idx,na,nb,"YES" if ok else "no"))
print()
for idx,cells,p,ed in winners:
    print("=== candidate",idx,"===")
    print(" interior angles (cyclic):", angseq(p))
    print(" edge type sequence     :", ''.join(t for t,_,_ in ed))
    print(" edge directions (deg)  :", [h for _,_,h in ed])
pickle.dump([(i,c,p) for i,c,p,_ in winners], open('/home/user/hat-surfaces/tileab.pkl','wb'))
