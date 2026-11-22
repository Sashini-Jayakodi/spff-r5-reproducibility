# Scientific execution evidence and its limits

The author's archived local verification dated 2026-11-22 reports a quick check, full supplement runner (13 executions, six expected JSON comparisons), and 140 focused tests passing, with maximum absolute numerical difference approximately 5.33e-14 across reported comparisons. The Review 6 nonterminal example was separately checked with exact rational arithmetic. Those successes **precede** this clean packaging and do not represent a verified clean clone from the new GitHub remote.

This repository has no real sign-image observations. The algorithms and results are a synthetic mathematical audit of the final selection event; they should not be presented as traffic-sign classifier accuracy or automotive safety validation.

The manifest uses SHA-256 to detect file modifications. Changing any inventoried source or expected output requires regenerating `SHA256SUMS.txt` before rerunning. Scientific results should not be altered merely to make the check pass.

## Current local preparation (2026-11-22, Asia/Colombo)

The original 33-entry SHA-256 manifest passed before changes. All 14 scientific
scripts and all nine expected JSONs remain byte-for-byte identical to that
original inventory. The package contains no supplied 140-test suite; the earlier
140-test claim above remains historical evidence, not a current test count.

A new `.venv` uses Python 3.13.14 on Windows with the three original numerical
pins. Installation succeeded after the sandbox blocked network access and the
dependency download was allowed through execution approval. `pip check` passed.
`requirements-lock.txt` records all 12 installed numerical/plotting dependencies
including transitive packages; it excludes pip itself.

The original quick check and original supplement runner both passed in fresh
output directories. The quick endpoints were 0.035340709976372696 and
0.07456656990588527. The original runner executed 13 subprocesses, compared six
JSON reports, and checked the historical pilot counts [15, 14, 15]. Its figure
renderer produced its files but logged a user-profile font-cache permission
warning. The wrapper now confines that cache to its output directory; a separate
renderer rerun passed without stderr and generated nonempty PDF/PNG files.

The revised runner adds the exact-rational subprocess and compares all nine
expected reports, including the non-FFT report and every historical pilot row
field. Review 6 requires exact parsed JSON equality. Other comparisons retain
the original relative tolerance 5e-8 and absolute tolerance 5e-11, skipping
runtime/environment/provenance metadata. The previously unused hand-copied pilot
approximations were removed; no expected output was changed.

The revised run completed successfully in `local_outputs/verified_supplement/`:
14 subprocess executions, all nine expected reports matched, exact Review 6
JSON equality, endpoint enclosure checks, and pilot counts [15, 14, 15]. The
updated quick runner also passed in `local_outputs/verified_quick/`. The wrapper
cache fix was separately exercised against the renderer because the completed
full run had already loaded its earlier wrapper. A final SHA-256 inventory
verification passed after documentation was finalized. These are fresh-directory
local runs, not a GitHub clean-clone verification.

Current numerical execution evidence lives in ignored `quick_reproduction/`,
`reproduction_run/`, and `local_outputs/`. The original checksum inventory is
preserved in `local_outputs/original_SHA256SUMS.txt`. The revised package manifest
is maintained by `verify_manifest.py`; it covers the explicit intended package
inventory and excludes itself, Git state, environments, and generated evidence.

The Monte Carlo FFT verification prints diagnostic z scores and does not assert
a statistical acceptance criterion. Its successful execution is not a formal
statistical certification. The conditional verifier checks 12 derivative
settings, 126 coverage settings, and fixed marginals. Specialist proof review,
originality/rights review, manuscript-table comparison (manuscript not supplied),
cross-platform testing, and a clean Git clone run remain outstanding.

At the initial preparation checkpoint, Git was on unborn `main` with an empty
index and no remote. GitHub CLI was not then installed. These are historical
setup observations, not restrictions on subsequent Git operations. The parent
folder has no `.git`; the child is the standalone Git root alongside starter
materials in its parent. The layout was retained.

Inspection of all original package file types found no apparent credentials,
absolute personal paths, real image datasets, trained models, or unrelated POC
code. This is a content review, not a guarantee about rights or originality.
The proposed creator name in `CITATION.cff` is inferred from local account/setup
metadata and still needs author confirmation; full CFF schema validation is
also a release prerequisite. No active licence, DOI, or release date was invented.

## FYP development scope

At the owner's direction, obsolete self-imposed authorization holds were removed
and replaced with `FYP_SETUP_CHECKLIST.md`. No independent university policy was
identified in those documents, and no institutional permission is claimed.
Ordinary Git operations and private GitHub storage are authorized by the owner;
public visibility, releases, and Zenodo uploads remain separate decisions.
Historical comments about release rights in frozen scientific scripts are not
private Git setup barriers. Scientific scripts and expected JSONs are preserved
unchanged. Current real-dataset gaps are in `docs/FYP_COMPLETENESS.md`.

The FYP setup verification rerun passed using the final wrapper:

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe verify_manifest.py
.\.venv\Scripts\python.exe quick_check.py --output local_outputs/fyp_setup_quick
.\.venv\Scripts\python.exe run_supplement.py --output local_outputs/fyp_setup_supplement
```

All 14 subprocesses completed; all nine expected reports matched, including exact
Review 6 JSON equality and pilot counts [15, 14, 15]. Figure generation completed
with the output-local cache and an empty renderer log. The 14 scientific scripts
and nine expected reports still match the original checksums byte-for-byte.
Python syntax parsing passed for all 17 Python files and all nine expected JSONs
parsed successfully. The updated manifest covers 38 package files plus its own
uninventoried manifest file (39 files intended for Git). Staged blob checks also
confirmed that Git's normalized contents match the manifest. A package scan
found no apparent credentials or personal absolute paths. No raw dataset, model
checkpoint, environment, or generated output is included in the Git inventory.
