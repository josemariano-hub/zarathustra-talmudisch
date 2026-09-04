exec(open('/home/user/hat-surfaces/kites.py').read().split("# ---- build")[0])
import pickle
from math import sqrt, atan2, degrees, pi
cands = pickle.load(open('/home/user/hat-surfaces/cands.pkl','rb'))

def signed_area(path):
    s=0
    for i in range(len(path)):
        (x1,y1)=xy(path[i]); (x2,y2)=xy(path[(i+1)%len(path)])
        s += x1*y2-x2*y1
    return s/2

def angles(path):
    n=len(path); out=[]
    if signed_area(path)<0: path=path[::-1]
    for i in range(n):
        p=xy(path[i-1]); q=xy(path[i]); r=xy(path[(i+1)%n])
        v1=(p[0]-q[0], p[1]-q[1]); v2=(r[0]-q[0], r[1]-q[1])
        a1=atan2(v1[1],v1[0]); a2=atan2(v2[1],v2[0])
        ang=(a1-a2) % (2*pi)
        out.append(round(degrees(ang)))
    return path, out

keep=[]
for cells,path in cands:
    p2,ang = angles(path)
    nstraight = sum(1 for a in ang if a==180)
    L=[round(dist(p2[i],p2[(i+1)%14]),4) for i in range(14)]
    keep.append((cells,p2,ang,L,nstraight))

print("candidate | #180deg | sorted angle multiset")
for i,(c,p,a,L,ns) in enumerate(keep):
    print(i, ns, sorted(a), "sum=",sum(a))
