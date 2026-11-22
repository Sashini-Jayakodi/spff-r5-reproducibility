"""Outward-rounded binary64 enclosures; restricted two-threshold model.
Assumes correctly rounded binary64 add/multiply, gradual underflow and no fast math.
"""
import json, platform, time
from pathlib import Path
import numpy as np

def cutoff(n):
    den=10**n; total=0; term=7**n; k=-1
    for j in range(n+1):
        total+=term
        if 10*total>den: break
        k=j
        if j<n: term=term*(n-j)*3//((j+1)*7)
    return k

def down(x): return np.maximum(0.,np.nextafter(x,-np.inf))
def up(x): return np.nextafter(x,np.inf)
def sum_interval(lo,hi):
    lo=lo.ravel();hi=hi.ravel()
    while len(lo)>1:
        k=len(lo)//2
        a=down(lo[:2*k:2]+lo[1:2*k:2]);b=up(hi[:2*k:2]+hi[1:2*k:2])
        if len(lo)%2: a=np.append(a,lo[-1]);b=np.append(b,hi[-1])
        lo,hi=a,b
    return [float(lo[0]),float(hi[0])]
def enclosure(n,t_percent):
    a,b=cutoff(3*n),cutoff(n)
    assert t_percent in (0,25,50,75,100)
    d=24*t_percent//100
    weights=(44,2+d,24-d,25-d,d,5)
    assert sum(weights)==100
    lo=np.zeros((a+1,b+1));hi=lo.copy();lo[0,0]=hi[0,0]=1.
    for i in range(n):
        nl=np.zeros_like(lo);nh=np.zeros_like(hi)
        for (l,s),w in zip(((0,0),(1,0),(1,1),(2,0),(2,1),(3,1)),weights):
            if not w or l>a or s>b:continue
            v=w/100.;vl=down(v);vh=up(v)
            x=min(a-l,3*i)+1;y=min(b-s,i)+1
            dest=(slice(l,l+x),slice(s,s+y));src=(slice(0,x),slice(0,y))
            nl[dest]=down(nl[dest]+down(lo[src]*vl));nh[dest]=up(nh[dest]+up(hi[src]*vh))
        lo,hi=nl,nh
    return a,b,sum_interval(lo,hi)
def main():
    assert np.finfo(np.float64).nmant==52
    assert np.nextafter(0.,1.)>0 and np.nextafter(0.,1.)*1.==np.nextafter(0.,1.)
    rows=[]
    for n,t in [(7,0),(7,100),(784,0),(784,100)]:
        start=time.perf_counter();a,b,iv=enclosure(n,t)
        row=dict(n=n,t=t/100,cutoffs=[a,b],enclosure=iv,width=iv[1]-iv[0],seconds=time.perf_counter()-start)
        print(row,flush=True);rows.append(row)
    result=dict(provenance='New directed-rounding audit; not historical execution or external certification',python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),rows=rows)
    Path('certified_endpoints.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
