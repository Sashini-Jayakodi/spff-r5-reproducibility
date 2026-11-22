"""New restricted-model decision analysis; no image-based experiments."""
import json, platform
import numpy as np, scipy
from scipy.stats import binom, beta
from scipy.optimize import brentq
from spff_r5_conditional_pilot_prototype import full_path, boundaries
n,m,alpha,delta,eta,tau=784,261,.30,.10,.05,.05
a,b=boundaries(n,alpha,delta)
p=np.array([1.]); law=np.array([.44,.26,.25,.05])
for _ in range(n): p=np.convolve(p,law)
ps=float(binom.cdf(b,n,.29)); pl=float(p[:a+1].sum()); lo=max(0,ps+pl-1); hi=min(ps,pl)
f=lambda t:full_path(t,n,alpha,delta)['loose_unsafe']
root=brentq(lambda t:f(t)-tau,0,1,xtol=1e-10)
F0,F1=f(0),f(1); mid=(F0+F1)/2
# conditional binomial probabilities integrated over N; no simulated pilots
N=np.arange(m+1); mass=binom.pmf(N,m,.24)
rows=[]
for t in [0,.25,.5,.75,1.]:
    supported=exceeded=0.
    for j,w in zip(N,mass):
        if j==0: continue
        k=np.arange(j+1); lower=np.zeros(j+1); upper=np.ones(j+1)
        lower[1:]=beta.ppf(eta/2,k[1:],j-k[1:]+1)
        upper[:-1]=beta.ppf(1-eta/2,k[:-1]+1,j-k[:-1])
        probs=binom.pmf(k,j,t)
        supported+=w*probs[upper<=root].sum(); exceeded+=w*probs[lower>root].sum()
    inconclusive=1-supported-exceeded
    val=f(t); assert min(supported,exceeded,inconclusive)>-1e-12
    wrong=exceeded if val<=tau else supported
    assert wrong<=eta+1e-12
    rows.append(dict(t=t,F=val,supported=supported,exceeded=exceeded,inconclusive=max(0.,inconclusive),wrong=wrong))
report=dict(provenance='New 2026-11-22 restricted synthetic analysis; numerical evaluation, not certified interval arithmetic',python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,n=n,m=m,alpha=alpha,delta=delta,eta=eta,tau=tau,strict_pass=ps,loose_pass=pl,frechet=[lo,hi],independence_product=ps*pl,sharp=[F0,F1],midpoint=mid,root=root,rows=rows)
print(json.dumps(report,indent=2)); open('decision_analysis.json','w').write(json.dumps(report,indent=2)+'\n')
