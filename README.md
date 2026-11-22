# SPFF-R5: FYP research implementation and reproducibility

**PRIVATE FYP DEVELOPMENT — REAL-DATASET INTEGRATION INCOMPLETE**

Research idea: **When Threshold-Wise Audits Mislead: Paired-Cluster Identification of Unsafe Final Selections.**

Manuscript: **Forecasting False Certificates Along Fixed-Sequence Paths: Sharp Coupling Bounds, a General Inference Barrier, and Pilot-Honest Auditing.**

This standalone repository is the mathematical and synthetic-experiment component of the university Final Year Project (FYP). It supports evaluation and development of that component. It contains no previous POC Git history. The FYP's required real-dataset implementation is not complete here.

## Current status

The owner has authorized ordinary local Git operations and private GitHub setup. Earlier self-imposed setup holds have been removed; no university policy or institutional permission is asserted by that change. Respect actual copyright, third-party terms, confidentiality duties, and applicable institutional policies. This project grants no public software or data licence and contains no DOI. Keep it PRIVATE. Public visibility, GitHub releases, and Zenodo uploads require separate explicit approval. Do not enable automated GitHub-to-Zenodo archiving.

## Research problem and methodology

A fixed-sequence procedure tests thresholds in a predetermined order, continues while tests pass, and returns the last passing threshold. The event of interest is that this final selection is unsafe under its population risk. Threshold-wise audits can hide dependence between thresholds and fail to identify this final-selection probability.

The experiments preserve paired per-cluster acceptance/error counts across thresholds. Synthetic finite-support laws hold threshold-wise marginals fixed while varying their joint coupling. FFT, nonnegative recurrence, and exact-rational calculations evaluate unsafe-selection probabilities and compare coupling bounds with event-only bounds. Pilot experiments evaluate uncertainty and tolerance decisions. Restricted-model results are not a general solution for arbitrary image data.

## Implementation architecture

```text
Synthetic signatures, weights, thresholds, seeds (inside experiment scripts)
    -> FFT / recurrence / exact-rational probability engines
    -> coupling, endpoint, and pilot reports
    -> comparisons with frozen expected JSONs
    -> logs, summaries, and figure in a fresh output directory
```

The wrappers verify checksums and copy scientific scripts to fresh output directories. No external dataset or GPU is needed for the current experiments. The real-data path (images -> classifier predictions -> paired cluster counts -> empirical path auditing) remains to be implemented.

## What is included

- `scripts/`: 14 Python experiment and verification scripts, including the Review 6 exact-rational nonterminal example.
- `quick_check.py`, `run_supplement.py`: standalone experimental reproduction wrappers.
- `expected/`: nine expected synthetic numerical JSON files, including the Review 6 exact-rational example.
- `docs/DATA_DICTIONARY.md`: description of the numerical outputs.
- `docs/VERIFICATION_STATUS.md`: reproduced calculations versus prior reported tests.
- `SHA256SUMS.txt`: file integrity manifest (checked before runner execution).
- `requirements.txt`: pinned numerical packages.
- `requirements-lock.txt`: complete dependency versions used for the local verification.
- `CITATION.cff`: draft citation metadata, pending creator and rights review.
- `docs/RELEASE_GUIDE.md`: gated GitHub, licensing, Zenodo, and manuscript citation steps.
- `docs/EXPERIMENTS.md`: script map, embedded configurations, and output semantics.
- `docs/FYP_COMPLETENESS.md`: real-dataset gaps and recommended GTSRB development work.
- `FYP_SETUP_CHECKLIST.md`: private repository and university evaluation checklist.

**No GTSRB, BelgiumTSC, other real image dataset, trained classifier, POC 1–3 codebase, or real traffic-sign track is included.** The numerical results come from synthetic mathematical models, not from image-track validation.

## Reproduce locally (Windows, in the new folder)

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe verify_manifest.py
.\.venv\Scripts\python.exe quick_check.py --output local_outputs/quick
.\.venv\Scripts\python.exe run_supplement.py --output local_outputs/supplement
```

The full runner executes the Review 6 exact-rational experiment and checks all nine expected JSON reports (exact equality for Review 6; numerical tolerances for the other reports, excluding runtime/environment metadata). It also generates the figure. The conditional pilot prototype is exercised with 15 repetitions to match the archived output; its standalone default of 40 repetitions is a different experiment. The FFT Monte Carlo script prints diagnostics and has no statistical pass/fail assertion; successful execution alone does not certify those diagnostics.

Generated directories are ignored by `.gitignore`. Runners refuse to overwrite existing output directories. To preserve prior evidence, use a new directory under `local_outputs/`, for example `--output local_outputs/supplement_repeat`. Python 3.13.14 on Windows was used for the current local checks; historical expected metadata records Python 3.13.5. `requirements.txt` retains the three original numerical pins; the lock file also pins their transitive dependencies.

On Linux/macOS use `python3 -m venv .venv` and `.venv/bin/python`; those platforms have not been verified here. Experiment parameters and seeds are embedded in the scripts, with no external configuration loader. See `docs/EXPERIMENTS.md` before changing settings.

After an intentional, reviewed package change, run `.\.venv\Scripts\python.exe verify_manifest.py --update`, then rerun validation. Never regenerate expected outputs merely to satisfy a check. The manifest covers the explicit source/documentation/expected-data inventory and excludes itself, `.git`, environments, and generated evidence.

## Provenance and limitations

The source files and expected JSONs were extracted from the author's two local-only Zenodo candidate packages. The revised `SHA256SUMS.txt` describes this combined clean workspace, not the earlier 99-file staged snapshot. Historical execution evidence remains in the separate private local supplement; do not claim this new repository has a public clean-clone run or that all earlier tests were rerun here. Proof originality and third-party rights require separate review.

## Subsequent release workflow (only after permission)

The current synthetic package does not satisfy the FYP real-dataset requirement by itself. See `docs/FYP_COMPLETENESS.md` for missing ingestion, model inference, leakage controls, cluster adapter, and empirical evaluation.

For later publication, review actual rights, choose suitable code/data licences, run a clean-clone reproduction, and obtain explicit approval before public visibility, a release, or a Zenodo upload. See `docs/RELEASE_GUIDE.md`.
