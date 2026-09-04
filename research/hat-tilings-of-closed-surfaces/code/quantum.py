exec(open('/home/user/hat-surfaces/kites.py').read().split("# ---- build")[0])
import pickle
from math import sqrt, atan2, degrees, pi
from collections import Counter, defaultdict
H=pickle.load(open('/home/user/hat-surfaces/hat.pkl','rb'))
ANG,LEN=H['ANG'],H['LEN']

def spectrum(label, arm):
    corners=set()
    for i in range(14):
        corners.add((ANG[i], arm(LEN[i]), arm(LEN[i-1])))
        corners.add((ANG[i], arm(LEN[i-1]), arm(LEN[i])))
    frontier={(l1,l2,a,1):None for (a,l1,l2) in corners}; seen=dict(frontier)
    closed=defaultdict(set)
    while frontier:
        nxt={}
        for (s,c,t,n) in frontier:
            if c==s: closed[t].add(n)
            for (a,l1,l2) in corners:
                if l1!=c or t+a>720: continue
                k=(s,l2,t+a,n+1)
                if k not in seen: seen[k]=None; nxt[k]=None
        frontier=nxt
    ts=sorted(closed)
    import math
    g=0
    for t in ts: g=math.gcd(g,t)
    print("%-42s realizable theta: %s" % (label, ts))
    print("%-42s gcd of realizable cone angles = %d deg  ->  curvature quantum" % ("", g))
    return ts

print("== hat  = Tile(1,sqrt3): two edge lengths, matching enforced ==")
spectrum("hat (a=1, b=sqrt3 distinguishable)", lambda l: 'a' if abs(l-1)<1e-6 else 'b')
print()
print("== Tile(1,1) / Spectre: all 14 edges congruent, any edge matches any edge ==")
spectrum("Tile(1,1) (all edges interchangeable)", lambda l: 'x')

print("""
Proof of the 60 deg quantum for the hat
---------------------------------------
Hat corner types (angle ; arms):
  90 :(a,b)   120:(a,a)   180:(a,a)   240:(a,a)   270:(a,b)
  90 :(b,a)   120:(b,b)               240:(b,b)   270:(b,a)
A corner with angle 90 or 270 always joins one short (a) arm to one long (b) arm:
it SWITCHES edge class.  Corners of 120/180/240 PRESERVE it.
Around any vertex the arm class must return to its start, so the number s of
switching corners is even.  Modulo 60:  90 = 270 = 30, and 120 = 180 = 240 = 0.
Hence theta = 30*s = 0 (mod 60).   QED
The same argument applies verbatim to every Tile(a,b) with a != b, since the
angle sequence and the a/b edge labelling are constant along the continuum.
""")
