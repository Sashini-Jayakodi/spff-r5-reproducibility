"""Run the manuscript's supplemental and archived standalone verifications in a fresh directory.
No writes to historical archives; this does not run the unrelated historical training suite.
"""
import argparse, json, math, os, shutil, subprocess, sys, hashlib, platform
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SCRIPTS=ROOT/'scripts'; EXPECTED=ROOT/'expected'
SKIP={'seconds','time_s','runtime_s','runtime_seconds','python','numpy','scipy','platform','provenance','elapsed_seconds'}
def compare(a,b,path=''):
    if isinstance(a,dict):
        for k,v in a.items():
            if k in SKIP or any(x in k.lower() for x in ['runtime','elapsed','seconds','version']):continue
            if k not in b:raise AssertionError(f'{path}.{k} absent')
            compare(v,b[k],path+'.'+k)
    elif isinstance(a,list):
        assert len(a)==len(b),path
        for i,(v,w) in enumerate(zip(a,b)):compare(v,w,f'{path}[{i}]')
    elif isinstance(a,bool):assert a==b,path
    elif isinstance(a,(int,float)):
        assert math.isclose(a,b,rel_tol=5e-8,abs_tol=5e-11),(path,a,b)
    else:assert a==b,(path,a,b)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='reproduction_run');args=parser.parse_args()
    out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=False)
    for p in SCRIPTS.glob('*.py'):shutil.copy2(p,out/p.name)
    # Validate the input archive before running; a manifest covers scripts and expected JSON.
    for line in (ROOT/'SHA256SUMS.txt').read_text().splitlines():
        sha,name=line.split('  ',1);assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,name
    results=[]
    def run(script,command=None):
        target=out/(script.replace('.py','')+'.log')
        environment=os.environ.copy()
        if script=='render_figure.py':
            environment['MPLCONFIGDIR']=str(out/'.matplotlib')
        with target.open('w') as log:subprocess.run([sys.executable,'-B',*([script] if command is None else command)],cwd=out,env=environment,stdout=log,stderr=subprocess.STDOUT,check=True)
        results.append(script);print('PASS execution:',script,flush=True)
    for script in ['new_decision_analysis.py','certified_endpoint_check.py','three_threshold_coupling.py','pilot_size_sensitivity.py','boundary_inversion.py','full_support_prefix.py','spff_r5_fft_path_experiment.py','spff_r5_fft_verify.py','spff_r5_conditional_pilot_verify.py','spff_r5_generality_probe.py','spff_r5_nonfft_recurrence_check.py','nonterminal_exact_verification.py','render_figure.py']:
        run(script)
    run('historical_pilot_15.py',['-c','import json; from spff_r5_conditional_pilot_prototype import run; rows,secs=run(reps=15,m=261,n=784,seed=20261119); open("historical_pilot_15.json","w").write(json.dumps(rows,indent=2)); print(rows,secs)'])
    # Check new JSON reports against archived values. Do not compare platform/runtimes.
    for name in ['decision_analysis.json','certified_endpoints.json','three_threshold_coupling.json','pilot_size_sensitivity.json','boundary_inversion.json','full_support_prefix.json','nonfft_reproduction_results.json']:
        a=json.loads((EXPECTED/name).read_text());b=json.loads((out/name).read_text());compare(a,b,name);print('PASS archived numerical match:',name,flush=True)
    # This rational-arithmetic report is deterministic, so require exact JSON equality.
    exact=json.loads((out/'nonterminal_exact_results.json').read_text())
    assert exact==json.loads((EXPECTED/'review6_nonterminal_exact.json').read_text()), 'review6_nonterminal_exact.json'
    print('PASS exact archived match: review6_nonterminal_exact.json',flush=True)
    # Explicit endpoint and rounding evidence. Use recurrence, not FFT precision.
    r=json.loads((out/'certified_endpoints.json').read_text())['rows'][-2:]
    assert r[0]['cutoffs']==r[1]['cutoffs']==[676,218]
    assert r[0]['enclosure'][0] <= .035340709976372696 <= r[0]['enclosure'][1]
    assert r[1]['enclosure'][0] <= .07456656990588575 <= r[1]['enclosure'][1]
    # The source audit has historical conditional pilot table with keys depending on archive format.
    rows=json.loads((out/'historical_pilot_15.json').read_text()); assert [x['coverage_count'] for x in rows]==[15,14,15]
    for row in rows:
        assert row['reps']==15 and row['m']==261 and row['n']==784
    old=json.loads((EXPECTED/'spff_r5_conditional_pilot_results.json').read_text())['rows']
    compare(old,rows,'historical_pilot')
    print('PASS archived numerical match: spff_r5_conditional_pilot_results.json',flush=True)
    (out/'verification_summary.json').write_text(json.dumps({'python':sys.version,'platform':platform.platform(),'scripts_executed':results,'expected_json_reports_matched':9,'historical_pilot_counts':[15,14,15],'status':'PASS scoped standalone supplemental runner; not a full repository or specialist audit'},indent=2)+'\n')
    print('PASS scoped supplemental reproduction; see logs and JSON.',flush=True)
if __name__=='__main__':main()
