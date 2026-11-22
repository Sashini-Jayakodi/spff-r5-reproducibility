"""Scoped fresh-directory reproduction: full-support experiment and original headline endpoints."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys,platform,math
from run_supplement import compare
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--output',default='quick_reproduction');a=p.parse_args();out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=False)
for line in (ROOT/'SHA256SUMS.txt').read_text().splitlines():
    h,n=line.split('  ',1);assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,n
print('PASS manifest',flush=True)
for f in (ROOT/'scripts').glob('*.py'):shutil.copy2(f,out/f.name)
with (out/'full_support_prefix.log').open('w') as log:subprocess.run([sys.executable,'-B','full_support_prefix.py'],cwd=out,stdout=log,stderr=subprocess.STDOUT,check=True)
r=json.loads((out/'full_support_prefix.json').read_text());compare(json.loads((ROOT/'expected/full_support_prefix.json').read_text()),r)
lo,hi=r['known'][0]['original'],r['known'][1]['original'];assert math.isclose(lo,.035340709976372696,abs_tol=1e-11);assert math.isclose(hi,.07456656990588575,abs_tol=1e-11)
s={'status':'PASS scoped new experiment and original endpoint reproduction only','python':sys.version,'platform':platform.platform(),'endpoints':[lo,hi],'width':hi-lo,'minimax_error':(hi-lo)/2,'new_report_numeric_match':True,'full_suite_rerun':False}
(out/'quick_summary.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps(s,indent=2),flush=True)
