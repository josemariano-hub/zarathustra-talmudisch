"""Kite complexes and hat placements, with a CORRECT validity test.

A kite complex is just a map (kite, side) -> (kite, 3-side), involutive.
Kite corners, in cyclic order: 0 = V (60 deg), 1 = M1 (90), 2 = G (120), 3 = M2 (90).
Crossing a side identifies corners like this:
    side 0 or 3 :  V ~ V   and  M1 ~ M2
    side 1 or 2 :  G ~ G   and  M1 ~ M2
so surface vertices are the corner classes, and a vertex's cone angle is the sum
of its corner angles.

A placement of the hat is valid iff
  (a) its 8 kites are distinct, and
  (b) every internal adjacency of the hat is realised on the surface, and
  (c) at every surface vertex, the angle the placement subtends is at most that
      vertex's cone angle.
(c) is what stops a tile from wrapping around a cone point.  The old test --
"no adjacency beyond the hat's own" -- also forbade a tile whose boundary is
glued to itself, which is legitimate, and so wrongly rejected real tilings.
"""
from collections import defaultdict
CORNER_ANGLE={0:60,1:90,2:120,3:90}

def corner_classes(nbr, nk):
    """works for complexes with boundary too: missing neighbours are skipped"""
    par={}
    def f(x):
        par.setdefault(x,x)
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    def u(a,b): par[f(a)]=f(b)
    for k in range(nk):
        for c in range(4): f((k,c))
    for (k,s),(k2,s2) in nbr.items():
        if s in (0,3):
            u((k,0),(k2,0))
            u((k,1),(k2,3)) if s==0 else u((k,3),(k2,1))
        else:
            u((k,2),(k2,2))
            u((k,1),(k2,3)) if s==1 else u((k,3),(k2,1))
    cls={}
    for k in range(nk):
        for c in range(4): cls[(k,c)]=f((k,c))
    ang=defaultdict(int)
    for (k,c),r in cls.items(): ang[r]+=CORNER_ANGLE[c]
    return cls, dict(ang)

def hat_pattern(nb, key):
    adj=[]
    for i in range(8):
        for side in range(4):
            r=nb(i,side)
            if r in key: adj.append((i,side,key[r]))
    tree=[None]*8; order=[0]; seen={0}
    while len(seen)<8:
        for (i,side,j) in adj:
            if i in seen and j not in seen:
                tree[j]=(i,side); seen.add(j); order.append(j); break
    return adj, tree, order

def placements(nbr, nk, adj, tree, order):
    cls, ang = corner_classes(nbr, nk)
    out=[]
    for root in range(nk):
        for ch in (0,1):
            sg=(lambda s:s) if ch==0 else (lambda s:3-s)
            cg=(lambda c:c) if ch==0 else (lambda c:(-c)%4)   # mirror swaps M1<->M2
            pos={0:root}; ok=True
            for j in order[1:]:
                i,side=tree[j]
                nx=nbr.get((pos[i],sg(side)))
                if nx is None: ok=False; break
                pos[j]=nx[0]
            if not ok or len(set(pos.values()))!=8: continue
            for (i,side,j) in adj:
                if nbr.get((pos[i],sg(side)))!=(pos[j],3-sg(side)): ok=False; break
            if not ok: continue
            load=defaultdict(int)
            for i in range(8):
                for c in range(4): load[cls[(pos[i],cg(c))]]+=CORNER_ANGLE[c]
            if any(v>ang[r] for r,v in load.items()): continue     # would wrap a cone point
            out.append(frozenset(pos.values()))
    return list(dict.fromkeys(out))

def exact_cover(universe, pieces, limit=20_000_000):
    c2p=defaultdict(list)
    for i,p in enumerate(pieces):
        for c in p: c2p[c].append(i)
    unc=set(universe); used=set(); sol=[]; nodes=[0]
    def go():
        nodes[0]+=1
        if nodes[0]>limit: raise TimeoutError
        if not unc: return True
        c=min(unc,key=lambda c: sum(1 for i in c2p[c] if not (pieces[i]&used)))
        for i in c2p[c]:
            if pieces[i]&used: continue
            used.update(pieces[i]); unc.difference_update(pieces[i]); sol.append(i)
            if go(): return True
            used.difference_update(pieces[i]); unc.update(pieces[i]); sol.pop()
        return False
    try: return go(), [pieces[i] for i in sol], nodes[0]
    except TimeoutError: return None, [], nodes[0]
