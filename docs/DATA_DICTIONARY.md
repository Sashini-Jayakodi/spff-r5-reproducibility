# Data dictionary — SPFF-R5 synthetic numerical outputs

The dataset is **not** an image collection. Each JSON encodes one synthetic mathematical verification or numerical experiment.

| Expected result | General role |
|---|---|
| `boundary_inversion.json` | One-threshold boundary/inversion studies and confidence-interval behaviour |
| `certified_endpoints.json` | Narrow outward-rounded enclosures for specified two-threshold endpoint probabilities (conditional on stated binary64 assumptions) |
| `decision_analysis.json` | Known-marginal tolerance decisions and event-only comparison |
| `full_support_prefix.json` | Full-support prefix and unsafe-terminal-suffix computations |
| `nonfft_reproduction_results.json` | Non-FFT cluster-count recurrence verification |
| `pilot_size_sensitivity.json` | Pilot-size sensitivity and inconclusive decision frequencies |
| `spff_r5_conditional_pilot_results.json` | Conditional pilot validation output |
| `three_threshold_coupling.json` | Three-threshold coupling example |
| `review6_nonterminal_exact.json` | New exact-rational three-threshold nonterminal-unsafe coupling verification (Review 6) |

These keys, fields, and assumptions should be checked against the corresponding schema emitted by the exact scripts prior to public release. If any numerical output is updated, publish it as a new archival version and record the new checksums.
