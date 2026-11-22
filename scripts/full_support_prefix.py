"""Full-support sharp upper bound for fixed-acceptance paths with unsafe suffixes.
New synthetic experiments; no real image data. Numerical convolution (not interval-certified).
"""
import json, math, time, platform
from pathlib import Path
from itertools import product
import numpy as np
from certified_endpoint_check import cutoff

def cdfs(E,w,C):
    return [np.cumsum(np.bincount(E[:,j],weights=w,minlength=int(c)+1))[:-1].clip(0,1) for j,c in enumerate(C)]

def quantile_coupling(F):
    knots=np.unique(np.clip(np.concatenate(([0.,1.],*F)),0,1))
    u=(knots[:-1]+knots[1:])/2
    return np.array([[np.searchsorted(f,v,side='left') for f in F] for v in u],dtype=int), np.diff(knots)

def calc(E,w,C,n):
    E=np.asarray(E,dtype=int); a=np.array([cutoff(int(c*n)) for c in C]);
    if np.any(a<0):return 0.,0
    p=np.zeros(tuple(a+1));p[(0,)*len(a)]=1.;mx=E.max(axis=0)
    for i in range(n):
        q=np.zeros_like(p)
        for e,v in zip(E,w):
            if v<=0 or np.any(e>a):continue
            lim=np.minimum(a-e,i*mx)+1
            src=tuple(slice(0,int(l)) for l in lim);dst=tuple(slice(int(s),int(s+l)) for s,l in zip(e,lim))
            q[dst]+=v*p[src]
        p=q
    return float(p.sum()),p.size

def bound_known(E,w,C,n):
    E=np.array(E);C=np.array(C);w=np.array(w)
    F=[np.round(f,14) for f in cdfs(E,w,C)]
    Z,p=quantile_coupling(F)
    assert np.all(np.diff(Z,axis=1)>=0) and np.all(np.diff(C-Z,axis=1)>=0)
    assert all(np.allclose(f,g,atol=1e-13) for f,g in zip(F,cdfs(Z,p,C)))
    risks=w@E/C;assert np.all(risks[:-1]<.30) and risks[-1]>.30
    original,states=calc(E,w,C,n);upper,_=calc(Z,p,C,n)
    marginal=[calc(Z[:,j:j+1],p,C[j:j+1],n)[0] for j in range(len(C))]
    assert original<=upper+1e-10 and upper<=min(marginal)+1e-10
    return dict(n=n,G=len(C),risks=risks.tolist(),original=original,sharp_upper=upper,event_only_upper=min(marginal),event_only_lower=max(0.,sum(marginal)-len(C)+1),quantile_atoms=Z.tolist(),weights=p.tolist(),dense_states=int(states))

def band_interval(F,C,n,m,eta=.05):
    # Simultaneous DKW bands on the per-cluster error-count CDFs, union bound across G.
    G=len(C);eps=math.sqrt(math.log(2*G/eta)/(2*m));lo=[np.maximum(0,f-eps) for f in F];hi=[np.minimum(1,f+eps) for f in F]
    ru=np.array([sum(1-f)/c for f,c in zip(lo,C)]);rl=np.array([sum(1-f)/c for f,c in zip(hi,C)])
    possible=np.flatnonzero(ru>.30-1e-12);k=int(possible[0])+1 if len(possible) else None
    if k is None:upper=0.
    else:
        # Prospective upper bound; artificial quantile atoms need not satisfy nesting.
        Z,p=quantile_coupling(hi[:k]);upper=calc(Z,p,C[:k],n)[0]
    # A prefix ending at the start of a definitely unsafe terminal suffix ensures unsafe final selection.
    h=G
    while h>0 and rl[h-1]>.30+1e-12:h-=1
    lower=0.
    if h<G:
        # union-bound lower endpoint using stochastically larger error-count margins.
        vals=[]
        for j in range(h+1):
            Z,p=quantile_coupling([lo[j]]);vals.append(calc(Z,p,C[j:j+1],n)[0])
        lower=max(0.,sum(vals)-h)
    L,U=min(lower,1.),min(upper,1.)
    if L>U: L,U=0.,1.
    return L,U,eps,k,h+1 if h<G else None

def increments(G,p):
    B=np.array(list(product([0,1],repeat=G)));return B.cumsum(1),np.prod(np.where(B,p,1-p),axis=1),np.arange(1,G+1)

def main():
    rows=[]
    E=np.array([(0,0),(0,1),(1,1),(0,2),(1,2),(1,3)]);C=np.array([1,3]);w=np.array([.44,.02,.24,.25,0,.05]);w1=np.array([.44,.26,0,.01,.24,.05]);
    for p in [w,w1]:
        start=time.perf_counter();r=bound_known(E,p,C,784);r.update(model='original two-threshold',seconds=time.perf_counter()-start);rows.append(r);print(r,flush=True)
    E3=np.array([(0,0,0),(0,1,1),(0,1,2),(1,1,1),(1,1,2),(1,2,3)]);C3=np.array([1,4,5]);p3=np.array([.05,.59,.07,0,.09,.20]);
    for n in (7,20,40,120):
        start=time.perf_counter();r=bound_known(E3,p3,C3,n);r.update(model='three-threshold restricted upper law',seconds=time.perf_counter()-start);rows.append(r);print(r,flush=True)
    for G in (2,3,4,5):
        E,w,C=increments(G,np.array([.22]*(G-1)+[.80]));
        for n in (7,10):
            start=time.perf_counter();r=bound_known(E,w,C,n);r.update(model='Bernoulli increments',seconds=time.perf_counter()-start);rows.append(r);print(r,flush=True)
    rng=np.random.default_rng(20261122); experiments=[]
    for name,prob in [('well_separated',[.12,.12,.95]),('moderate_margin',[.20,.20,.60])]:
        E,w,C=increments(3,np.array(prob));n=40;truth=bound_known(E,w,C,n);unknown=[]
        for m in (261,1044,4176):
            for rep in range(20):
                obs=rng.multinomial(m,w)/m; F=cdfs(E,obs,C);L,U,eps,k,h=band_interval(F,C,n,m)
                unknown.append(dict(m=m,rep=rep,L=L,U=U,epsilon=eps,first_possible_unsafe=k,first_definite_suffix=h,contains_true=bool(L-1e-10<=truth['original']<=U+1e-10),contains_sharp_upper=bool(U+1e-10>=truth['sharp_upper'])))
        summary=[dict(m=m,mean_lower=float(np.mean([r['L'] for r in unknown if r['m']==m])),mean_upper=float(np.mean([r['U'] for r in unknown if r['m']==m])),covers_true=sum(r['contains_true'] for r in unknown if r['m']==m),reps=20) for m in (261,1044,4176)]
        print(name,truth,summary,flush=True);experiments.append(dict(model=name,increment_probabilities=prob,truth=truth,rows=unknown,summary=summary))
    Path('full_support_prefix.json').write_text(json.dumps(dict(provenance='new synthetic analysis, no image validation',python=platform.python_version(),numpy=np.__version__,known=rows,unknown_experiments=experiments,seed=20261122),indent=2)+'\n')

if __name__=='__main__':main()
