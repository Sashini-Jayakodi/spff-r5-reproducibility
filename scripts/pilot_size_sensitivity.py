"""New known-marginal synthetic sensitivity; matched model, different pilot budgets."""
import json, platform
from pathlib import Path
import numpy as np, scipy
from scipy.stats import binom, beta
from scipy.optimize import brentq
from spff_r5_conditional_pilot_prototype import full_path

def main():
    n,alpha,delta,eta,tau=784,.30,.10,.05,.05
    f=lambda t:full_path(t,n,alpha,delta)['loose_unsafe']
    root=brentq(lambda t:f(t)-tau,0,1,xtol=1e-10)
    ts=[0,.25,.5,.75,1.];fs=[f(t) for t in ts];rows=[]
    for m in (65,131,261,522,1044):
        totals=np.zeros((len(ts),3));mass=binom.pmf(np.arange(m+1),m,.24)
        # N=0 is inconclusive for this tolerance.
        totals[:,2]=mass[0]
        for N in range(1,m+1):
            k=np.arange(N+1)
            # Direct closed CP interval comparisons through binomial-tail inversion.
            sup=binom.cdf(k,N,root)<=eta/2
            exc=binom.sf(k-1,N,root)<eta/2
            assert not np.any(sup & exc)
            for i,t in enumerate(ts):
                p=binom.pmf(k,N,t)*mass[N]
                totals[i]+=[p[sup].sum(),p[exc].sum(),p[~(sup|exc)].sum()]
        for t,F,(s,e,u) in zip(ts,fs,totals):
            wrong=e if F<=tau else s
            assert abs(s+e+u-1)<1e-10 and wrong<=eta+1e-10
            rows.append(dict(m=m,t=t,F=F,supported=float(s),exceeded=float(e),inconclusive=float(u),wrong=float(wrong)))
    # Check directly all closed-limit endpoint conventions, for N=0..1044.
    for N in range(1,1045):
        assert beta.ppf(1-eta/2,1,N)>0 and beta.ppf(eta/2,N,1)<1
    report=dict(provenance='New restricted synthetic pilot-size sensitivity; no real image data',python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,n=n,alpha=alpha,delta=delta,eta=eta,tau=tau,root=root,rows=rows)
    Path('pilot_size_sensitivity.json').write_text(json.dumps(report,indent=2)+'\n')
    for row in rows:print(row)
if __name__=='__main__':main()
