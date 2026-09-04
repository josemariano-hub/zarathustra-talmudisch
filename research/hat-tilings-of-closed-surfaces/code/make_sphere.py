import sys, math, pickle, collections
sys.path.insert(0,'/home/user/hat-surfaces')
exec(open('/home/user/hat-surfaces/build3d.py').read())
exec(open('/home/user/hat-surfaces/render3d.py').read())
from glue_search import find
N=int(sys.argv[1]); chi=int(sys.argv[2]); mt=int(sys.argv[3]); out=sys.argv[4]
shape='sphere' if chi==2 else 'torus'
pairs,th,nd,sd = find(N,chi,mt,tries=200,node_limit=250000)
if not pairs: print("no gluing found for N=%d chi=%d"%(N,chi)); sys.exit(1)
print("N=%d chi=%+d  cone angles: %s"%(N,chi,dict(sorted(collections.Counter(th).items()))))
print("   total defect = %+d deg (Gauss-Bonnet needs %+d)"%(sum(360-t for t in th),360*chi))
nv,tris,cons,tp = build(pairs,N)
print("   mesh: %d vertices, %d triangles, %d length constraints"%(nv,len(tris),len(cons)))
P,emax,eavg = embed(nv,tris,cons,shape,iters=5000)
print("   3D embedding: max edge error %.3f%%, mean %.3f%%"%(100*emax,100*eavg))
pickle.dump((P,tris,tp,pairs,th),open(out+'.pkl','wb'))
for az,el,tag in ((35,22,'a'),(155,-18,'b')):
    render(P,tris,tp,out+'_'+tag+'.png',elev=el,azim=az)
print("   wrote", out+'_a.png', out+'_b.png')
