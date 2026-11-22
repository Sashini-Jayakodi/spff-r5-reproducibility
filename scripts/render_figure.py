"""Generate figure from the same numerical results as Table V (no fitting)."""
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
p=Path('decision_analysis.json'); rows=json.loads(p.read_text())['rows']
fig,ax=plt.subplots(figsize=(3.35,2.35),layout='constrained')
ax.plot([r['t'] for r in rows],[100*r['F'] for r in rows],marker='o',ms=3.5,lw=1.3,color='#205c93')
ax.set(xlabel='Coupling parameter t',ylabel='Unsafe final selection (%)',xticks=[0,.25,.5,.75,1.]);ax.grid(alpha=.25);ax.tick_params(labelsize=8);ax.xaxis.label.set_size(8);ax.yaxis.label.set_size(8)
fig.savefig('figure1.png',dpi=600);fig.savefig('figure1.pdf');plt.close(fig)
