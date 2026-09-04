"""(1) All cone angles realizable around a point by hat corners (edge-length matching).
   (2) Vertex statistics of a genuine plane hat tiling patch."""
exec(open('/home/user/hat-surfaces/kites.py').read().split("# ---- build")[0])
import pickle
from math import sqrt, atan2, degrees, pi
from collections import Counter, defaultdict
H=pickle.load(open('/home/user/hat-surfaces/hat.pkl','rb'))
ANG,LEN=H['ANG'],H['LEN']
S=lambda l: 'a' if abs(l-1)<1e-6 else 'b'
# corner presented CCW: first arm = e_i, second arm = e_{i-1}
corners=set()
for i in range(14):
    corners.add((ANG[i], S(LEN[i]), S(LEN[i-1])))          # unreflected
    corners.add((ANG[i], S(LEN[i-1]), S(LEN[i])))          # reflected
corners=sorted(corners)
print("distinct hat corner types (angle, first arm, second arm):")
for c in corners: print("   ",c)

# reachable total angles by cyclic edge-matched sequences
MAX=1080
reach=defaultdict(set)   # (start_arm, cur_arm, total) reachable ; count tiles
best={}
from functools import lru_cache
states={}
for (a,l1,l2) in corners:
    states.setdefault((l1,l1,0),set())
# BFS over (start_arm, current_arm, total, ntiles)
frontier={}
for (a,l1,l2) in corners:
    frontier.setdefault((l1,l2,a,1),None)
seen=dict(frontier)
closed=defaultdict(set)
while frontier:
    nxt={}
    for (s,c,t,n) in frontier:
        if c==s: closed[t].add(n)
        for (a,l1,l2) in corners:
            if l1!=c: continue
            t2=t+a
            if t2>MAX: continue
            k=(s,l2,t2,n+1)
            if k not in seen: seen[k]=None; nxt[k]=None
    frontier=nxt
print("\nrealizable cone angles theta (deg) around a single point, with tile counts:")
for t in sorted(closed):
    print("   theta=%4d  defect=%+5d  tiles=%s" % (t, 360-t, sorted(closed[t])))
