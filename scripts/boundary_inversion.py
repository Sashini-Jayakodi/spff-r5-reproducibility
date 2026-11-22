"""One-threshold unknown-marginal control example; theoretical CP validity, numeric evaluation."""
import json, platform
from pathlib import Path
import numpy as np, scipy
from scipy.stats import binom, beta
from certified_endpoint_check import cutoff

def main():
    n=784; a=.30; eta=.05; k=cutoff(n); bn=binom.cdf(k,n,a);rows=[]
    for m in (261,1044,4176):
        K=np.arange(m+1); lo=np.zeros(m+1); hi=np.ones(m+1)
        lo[1:]=beta.ppf(eta/2,K[1:],m-K[1:]+1)
        hi[:-1]=beta.ppf(1-eta/2,K[:-1]+1,m-K[:-1])
        L=np.where(lo>a,binom.cdf(k,n,hi),0.)
        U=np.where(hi<=a,0.,binom.cdf(k,n,np.maximum(lo,a)))
        for p in (.25,.29,.30,.301,.31,.35):
            F=float(binom.cdf(k,n,p)) if p>a else 0.
            w=binom.pmf(K,m,p); cov=float(w[(L<=F)&(F<=U)].sum());width=float(w@(U-L))
            assert cov>=.95-1e-10
            if p==a:assert width>=(1-2*eta)*bn-1e-12
            rows.append(dict(m=m,p=p,F=F,coverage=cov,mean_width=width))
    d=dict(provenance='New unknown-marginal one-threshold inversion illustration, deterministic finite sums',python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,n=n,alpha=a,eta=eta,cutoff=k,bound=float((1-2*eta)*bn),rows=rows)
    Path('boundary_inversion.json').write_text(json.dumps(d,indent=2)+'\n')
    for row in rows:print(row)
if __name__=='__main__':main()
