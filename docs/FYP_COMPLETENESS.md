# FYP completeness and real-dataset integration plan

## Current evaluation scope

Research idea: **When Threshold-Wise Audits Mislead: Paired-Cluster Identification
of Unsafe Final Selections.** SPFF-R5 supplies mathematical models, coupling
experiments, numerical probability engines, and pilot-inference illustrations.
This is an implemented research component, but it does not yet fulfil the
university FYP requirement to implement and evaluate on a real dataset.

| Evaluation material | Present in this standalone repository? |
|---|---|
| Scientific source and experiment scripts | Yes: 14 Python scripts |
| Numerical/plotting dependencies | Yes: original pins and full environment lock |
| Verification wrappers and checksums | Yes |
| Frozen expected results | Yes: nine synthetic JSON reports |
| Reproduction and experiment documentation | Yes |
| Synthetic experiment configurations | Embedded constants and seeds; no config loader |
| Real dataset ingestion and metadata validation | No |
| Real-image model training or checkpoint acquisition | No |
| Reproducible real-image inference and predictions | No |
| Real-data train/pilot/evaluation split protocol | No |
| Paired-cluster empirical SPFF-R5 adapter and audit | No |
| End-to-end real-data tests, results, tables, and demo | No |
| Complete manuscript, university rubric, and final FYP report | Not supplied here |

## GTSRB requirements

The original GTSRB training data provides tracks of images of physical signs;
the benchmark test data does not provide equivalent track grouping. The official
benchmark documentation describes this distinction:
https://benchmark.ini.rub.de/ and
https://github.com/houbensebastian/GermanTrafficSignBenchmarks .
Do not treat the mixed test images as observed 30-frame tracks or invent track
identifiers. Confirm dataset terms and cite the benchmark when using it. Keep
raw images and model weights outside Git; record acquisition steps and hashes.

A real implementation needs the following, with choices frozen before evaluating:

1. **Ingestion and provenance.** Parse official image/annotation archives, validate
   labels and frame membership, and construct track IDs from class plus track
   prefix so repeated prefixes across classes are not merged. Record dataset
   version, archive hashes, class mapping, preprocessing and sample exclusions.
2. **Leakage-controlled protocol.** Split physical tracks, not individual frames,
   into model development, threshold selection/pilot, and held-out evaluation
   roles as appropriate. Identify cross-release duplicate images. Keep held-out
   labels out of model tuning and threshold ordering. A pilot-honest claim needs
   the specified independence conditions, not just random split code.
3. **Model and prediction artifact.** Supply reproducible training or documented
   checkpoint acquisition, architecture and class order, checkpoint hash, pinned
   image-model dependencies, and deterministic evaluation preprocessing. Export
   per-frame scores/predictions joined to truth and original track/frame IDs.
4. **Paired-cluster adapter.** Define the application-specific error event, risk
   estimand, acceptance rule, threshold grid/order, stopping rule, and no-certificate
   case. For each physical track i retain the whole vector `(C_ij,E_ij)` over
   thresholds j. Test `0 <= E_ij <= C_ij` and all nesting assumptions required by
   the selected method. Do not replace paired vectors with unpaired marginals.
5. **Empirical audit.** Implement threshold-wise comparisons, final-selection
   outcomes, uncertainty and pilot decisions for the actual data model. The
   synthetic fixed-support/fixed-count FFT engine is not automatically valid for
   variable real-track acceptance counts. Check assumptions, or use a separately
   justified estimator/bound. Do not present a fitted empirical distribution as
   known population truth. Report sampling uncertainty and limitations.
6. **Evaluation and deliverables.** Provide small loader/adapter tests, group
   overlap and duplicate checks, a smoke command using user-supplied local data,
   full experiment configs/seeds, comparison tables and figures, measured results,
   run logs/hashes, and a demonstrable end-to-end command. Repeated splits or
   corruption conditions of the same tracks are not new independent observations.

## Read-only review of an existing local POC

A separate `Speed/osr-speed-limit` checkout was inspected read-only. No files,
datasets, checkpoints, configuration values, results, or Git history were copied.
Its source was not executed or validated as part of this standalone package.

| Candidate from that checkout | Potential contribution | Review before incorporation |
|---|---|---|
| `src/data.py` | Official ZIP/CSV ingestion and class-plus-prefix track IDs | Dataset terms, preprocessing, schema, identity assertions and tests |
| `src/splits.py` | Reproducible class-stratified assignment of whole tracks | Extend to independent development/pilot/evaluation roles; review class sizes |
| `scripts/extract_poc_probs.py` | Checkpoint-based prediction export with track/frame IDs and checkpoint hash | Remove hard-coded POC paths/conditions; verify class mapping and model/split provenance |
| `scripts/make_poc_splits.py` | Frozen split matrices with hashes | POC-specific counts and frozen protocol are not SPFF-R5 defaults |
| Existing data/split/model tests | Candidate behavior checks | Select relevant tests and adapt to the new module boundaries |

The old configuration contains a machine-specific data path and describes its
classifier as fine-tuned on the benchmark test release. This changes the meaning
of any test-release evaluation: it cannot be advertised as untouched benchmark
test performance. Its intended track-holdout design and duplicate exclusions
need review before reuse. The extraction code has POC-specific GPU, class and
condition assumptions. Its dependency versions differ from this package's lock.
No ownership/licence conclusion is inferred merely because a local file exists.

## Recommended next development sequence

First agree the empirical estimand, scope of classes, track-based split design,
and evaluation criteria with the supervisor. Then selectively adapt an ingestion
module and schema tests, add independently frozen prediction and split artifacts,
build and test the paired-count adapter, and implement the justified empirical
audit. Finally run on actual GTSRB data and document measured outputs in a
separate empirical results area. Keep the existing nine synthetic reports and
their reproduction path unchanged as the mathematical reference suite.

Potential new modules such as `src/datasets/`, `src/inference/`, `src/audit/`,
`configs/`, and `tests/` are a proposed architecture, not existing implementation.
No dataset download is needed to review or reproduce the current package.
