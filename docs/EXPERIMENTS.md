# Experiments, configurations, and implementation map

The implemented component operates on synthetic cluster signatures and finite
probability laws. It does not read images. Scientific parameters are embedded
in the scripts, not loaded from YAML or command-line experiment configurations.
The wrappers' `--output` option chooses only a fresh output directory.

## Probability engines and experiment reports

| Script | Role | Configuration / output |
|---|---|---|
| `spff_r5_conditional_pilot_prototype.py` | Restricted fixed-marginal two-threshold FFT engine, conditional Clopper-Pearson interval, pilot replay | Defaults: n=784, m=261, alpha=.30, delta=.10, eta=.05; runner uses reps=15, seed=20261119 |
| `spff_r5_fft_path_experiment.py` | Padded FFT convolution for two endpoint laws | n=7,20,120,784; prints selection probabilities and numerical diagnostics |
| `new_decision_analysis.py` | Known-marginal tolerance decisions and event-only comparison | n=784, m=261, tau=.05; `decision_analysis.json` |
| `certified_endpoint_check.py` | Outward-rounded binary64 endpoint enclosures | n=7,784; endpoint t=0,1; `certified_endpoints.json` |
| `three_threshold_coupling.py` | Fixed-support three-threshold coupling example | n=7,20,40,120; t=0,.25,.5,.75,1; `three_threshold_coupling.json` |
| `pilot_size_sensitivity.py` | Pilot budget sensitivity and decision frequencies | m=65,131,261,522,1044; n=784; `pilot_size_sensitivity.json` |
| `boundary_inversion.py` | One-threshold unknown-marginal inversion | n=784; m=261,1044,4176; `boundary_inversion.json` |
| `full_support_prefix.py` | Known-marginal coupling upper bounds and pilot-band examples | Two/three-threshold laws and Bernoulli increments; pilot m=261,1044,4176, 20 reps, seed=20261122; `full_support_prefix.json` |
| `spff_r5_nonfft_recurrence_check.py` | Nonnegative recurrence compared with FFT, including derivative | n=784, cutoffs (676,218), five t settings; `nonfft_reproduction_results.json` |
| `nonterminal_exact_verification.py` | Exact-rational nonterminal-unsafe example | n=10, counts [1,5,6], alpha=.35, delta=.10; `nonterminal_exact_results.json` compared with `expected/review6_nonterminal_exact.json` |

These configurations describe existing experiments; they are not a recommended
empirical protocol. Review each script for its complete signatures, weights,
ordering conventions, parameter grid, and assumptions. In particular, the
two-threshold engine stores loose/strict count coordinates while testing the
strict threshold first. A future data adapter must preserve the intended order.

## Additional verification and visualization

- `spff_r5_fft_verify.py`: compares FFT probabilities with 350,000 multinomial
  draws for each of two laws, seed=20261119. It prints z scores but has no
  statistical acceptance assertion.
- `spff_r5_conditional_pilot_verify.py`: 12 derivative checks, 126 conditional
  coverage settings, and fixed-marginal checks.
- `spff_r5_generality_probe.py`: nested variable-acceptance three-threshold
  composition enumeration for n=7,10 and boundary-width examples.
- `render_figure.py`: reads `decision_analysis.json` and writes `figure1.png`
  and `figure1.pdf`, without fitting new data.

## Reproduction outputs and comparison

`quick_check.py` checks the full-support report and original endpoint values.
`run_supplement.py` executes 13 scientific script entries plus the 15-repetition
pilot replay (14 subprocesses total). It compares seven numerical JSON reports,
the historical pilot rows, and the exact Review 6 report: nine expected files.
The prototype's direct default is 40 pilot repetitions, so invoking it directly
does not reproduce the archived 15-repetition report.

Inspect `verification_summary.json` and each `.log` file in the selected output
directory. Runtime, environment and provenance fields are excluded from numerical
comparison. Exact-rational results require exact parsed JSON equality. Numerical
agreement is not independent proof review, a universal inference guarantee, or
real-image validation. The endpoint interval computation relies on its stated
binary64 rounding and underflow assumptions.

Run through the wrappers to keep generated files outside the scientific source
tree. Source and expected files are frozen for this preparation. Any later
scientific change needs an explained experiment version and separately reviewed
results; checksum regeneration alone does not validate a scientific change.
