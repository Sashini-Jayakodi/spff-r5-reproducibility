"""New restricted, predeclared-support three-threshold sharp identification example.
No image data. Cutoffs exact integers; convolution floating-point, not certified.
"""
import json, time, platform
from pathlib import Path
from fractions import Fraction
from itertools import product
import numpy as np
from certified_endpoint_check import cutoff

# Fixed counts C=(1,4,5), six physically feasible error signatures.
E=np.array([(0,0,0),(0,1,1),(0,1,2),(1,1,1),(1,1,2),(1,2,3)],dtype=int)
C=np.array([1,4,5])

def weights(t_percent):
    # denominator 10000; x=.09*t with t given as integer percentage
    x=9*t_percent
    return np.array([500,5000+x,1600-x,900-x,x,2000],dtype=int)

def oracle(n,t_percent):
    a=np.array([cutoff(int(c*n)) for c in C]);assert np.all(a>=0)
    p=np.zeros(tuple(a+1));p[(0,0,0)]=1
    w=weights(t_percent)/10000
    for i in range(n):
        q=np.zeros_like(p)
        for sig,v in zip(E,w):
            if v==0 or np.any(sig>a):continue
            lim=np.minimum(a-sig,i*E.max(axis=0))+1
            src=tuple(slice(0,int(x)) for x in lim)
            dest=tuple(slice(int(s),int(s+l)) for s,l in zip(sig,lim))
            q[dest]+=v*p[src]
        p=q
    return a,float(p.sum())

def exact_small(n,t_percent):
    a=np.array([cutoff(int(c*n)) for c in C]); w=weights(t_percent)
    pos=np.flatnonzero(w);num=0
    for path in product(pos,repeat=n):
        ix=np.array(path)
        if np.all(E[ix].sum(axis=0)<=a):
            term=1
            for j in path:term*=int(w[j])
            num+=term
    return Fraction(num,10000**n)

def main():
    assert np.all(np.diff(E,axis=1)>=0) and np.all(np.diff(C-E,axis=1)>=0)
    rows=[];marginals=None
    for t in (0,25,50,75,100):
        w=weights(t);assert w.sum()==10000 and min(w)>=0
        now=[{int(e):int(w[E[:,j]==e].sum()) for e in np.unique(E[:,j])} for j in range(3)]
        assert marginals is None or marginals==now;marginals=now
    for n in (7,20,40,120):
        prev=-1.
        for t in (0,25,50,75,100):
            start=time.perf_counter();a,F=oracle(n,t)
            assert F>=prev-1e-12;prev=F
            row=dict(n=n,t=t/100,cutoffs=a.tolist(),F=F,seconds=time.perf_counter()-start)
            if n==7 and t in (0,100):
                ex=exact_small(n,t);assert abs(F-float(ex))<1e-13
                row['exact_rational']=str(ex)
            print(row,flush=True);rows.append(row)
    risks=(weights(0)@E/10000/C).tolist();assert risks[0]<.30 and risks[1]<.30 and risks[2]>.30
    report=dict(provenance='New synthetic three-threshold predeclared-support coupling example; no image validation',python=platform.python_version(),numpy=np.__version__,accepted=C.tolist(),signatures=E.tolist(),weight_denominator=10000,marginals=marginals,risks=risks,rows=rows)
    Path('three_threshold_coupling.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
