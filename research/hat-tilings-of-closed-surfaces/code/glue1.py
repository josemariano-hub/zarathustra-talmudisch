"""All closed surfaces obtained by gluing ONE hat to itself along its own edges.

Hat = 14-gon, directed CCW edges e_0..e_13, e_i from vertex v_i to v_{i+1}.
Glue edges in 7 length-matched pairs.
  orientation-preserving (surface orientable at that edge): v_i ~ v_{j+1}, v_{i+1} ~ v_j
  orientation-reversing  : v_i ~ v_j,     v_{i+1} ~ v_{j+1}
chi = V - E + F = V - 7 + 1 = V - 6.
"""
exec(open('/home/user/hat-surfaces/kites.py').read().split("# ---- build")[0])
import pickle
from math import sqrt, atan2, degrees, pi
from itertools import product
from collections import Counter

winners=dict((i,(c,p)) for i,c,p in pickle.load(open('/home/user/hat-surfaces/tileab.pkl','rb')))
cells,path = winners[8]
def signed_area(P):
    s=0
    for i in range(len(P)):
        (x1,y1)=xy(P[i]); (x2,y2)=xy(P[(i+1)%len(P)]); s+=x1*y2-x2*y1
    return s/2
if signed_area(path)<0: path=path[::-1]
n=14
LEN=[round(dist(path[i],path[(i+1)%n]),6) for i in range(n)]
ANG=[]
for i in range(n):
    p=xy(path[i-1]); q=xy(path[i]); r=xy(path[(i+1)%n])
    ANG.append(round(degrees((atan2(p[1]-q[1],p[0]-q[0])-atan2(r[1]-q[1],r[0]-q[0]))%(2*pi))))
SHORT=[i for i in range(n) if abs(LEN[i]-1)<1e-6]
LONG =[i for i in range(n) if abs(LEN[i]-sqrt(3))<1e-6]
print("HAT  area = 8*sqrt(3) = %.6f" % (8*sqrt(3)))
print("  interior angles v_0..v_13 :", ANG, " sum", sum(ANG))
print("  edge lengths     e_0..e_13:", ['1' if abs(l-1)<1e-6 else 'S3' for l in LEN])
print("  short edges", SHORT, " long edges", LONG)

def matchings(lst):
    if not lst: yield []; return
    a=lst[0]
    for k in range(1,len(lst)):
        b=lst[k]; rest=lst[1:k]+lst[k+1:]
        for m in matchings(rest): yield [(a,b)]+m

class DSU:
    def __init__(s,n): s.p=list(range(n))
    def f(s,x):
        while s.p[x]!=x: s.p[x]=s.p[s.p[x]]; x=s.p[x]
        return x
    def u(s,a,b): s.p[s.f(a)]=s.f(b)

results=Counter(); examples={}
allm=[ms+ml for ms in matchings(SHORT) for ml in matchings(LONG)]
print("edge pairings (length-respecting):", len(allm))
for pairing in allm:
    for flags in product((0,1), repeat=7):
        d=DSU(14); orientable=True
        for (i,j),f in zip(pairing,flags):
            if f==0:   # orientation-preserving gluing
                d.u(i,(j+1)%14); d.u((i+1)%14, j)
            else:      # orientation-reversing
                d.u(i,j); d.u((i+1)%14,(j+1)%14)
                orientable=False
        cls={}
        for v in range(14): cls.setdefault(d.f(v),[]).append(v)
        V=len(cls); chi=V-6
        cone=sorted(sum(ANG[v] for v in g) for g in cls.values())
        if orientable:
            g=(2-chi)//2; name="orientable genus %d"%g if chi<=2 else "?"
            if chi==2: name="SPHERE"
            elif chi==0: name="TORUS"
        else:
            k=2-chi; name="non-orientable genus %d"%k
            if k==1: name="PROJECTIVE PLANE"
            elif k==2: name="KLEIN BOTTLE"
        key=(name,tuple(cone))
        results[key]+=1
        if key not in examples: examples[key]=(pairing,flags)

print("\n=== closed surfaces from a SINGLE hat ===")
bysurf={}
for (name,cone),cnt in results.items(): bysurf.setdefault(name,[]).append((cone,cnt))
for name in sorted(bysurf, key=lambda s:(len(s),s)):
    lst=sorted(bysurf[name])
    tot=sum(c for _,c in lst)
    print("\n%-26s  %6d gluings, %d distinct cone-angle spectra" % (name,tot,len(lst)))
    for cone,cnt in lst[:200]:
        defect=sum(360-a for a in cone)
        flag=" [all cone angles < 360 -> convex polyhedron by Alexandrov]" if all(a<360 for a in cone) else ""
        print("    angles %-52s  sum(defects)=%+5d  x%d%s" % (str(list(cone)), defect, cnt, flag))
pickle.dump({'ANG':ANG,'LEN':LEN,'SHORT':SHORT,'LONG':LONG,'path':path,'cells':cells},
            open('/home/user/hat-surfaces/hat.pkl','wb'))
