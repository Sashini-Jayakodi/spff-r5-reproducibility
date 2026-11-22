# FYP private repository and evaluation checklist

The priority is university evaluation and private FYP development. The owner has
authorized local staging, committing, private repository creation, and upload of
this reviewed package. No independently verified policy requiring separate written
institutional permission was supplied or found in the package. This checklist
does not assert university permission or waive actual third-party rights,
copyright, confidentiality duties, or institutional policies.

## Private setup

- Use the existing standalone Git root and `main`; do not create a nested repo.
- Review source, documentation, expected outputs, and checksum inventory.
- Exclude environments, caches, credentials, raw datasets, checkpoints, and
  generated outputs. Never upload a token or credential file.
- Run `pip check`, `verify_manifest.py`, and both reproduction wrappers in fresh
  output directories. Confirm scientific source and expected results are unchanged.
- Stage only the manifest's intended files plus `SHA256SUMS.txt`.
- Inspect `git diff --cached --stat` and `git diff --cached --check`.
- Commit with `Initial FYP research implementation and reproducibility package`.
- Install GitHub CLI by an official method and authenticate interactively.
- Create `Sashini-Jayakodi/spff-r5-reproducibility` as PRIVATE, push `main`,
  and verify owner, private visibility, remote commit, and clean working tree.

## University evaluation

- Review the README and `docs/EXPERIMENTS.md` for the implemented component.
- Review `docs/VERIFICATION_STATUS.md` for evidence and limitations.
- Use `docs/FYP_COMPLETENESS.md` to plan real-dataset integration.
- Keep the current synthetic results distinct from future empirical results.
- Record dataset provenance, settings, split IDs, checkpoint identity,
  dependencies, and output hashes for the real-data pipeline.
- Do not label the FYP implementation complete before the real-dataset path is
  implemented, tested, executed, and documented for evaluation.

## Separate future decisions

Do not make this repository public, create a release, or upload to Zenodo without
explicit approval. Review actual rights and choose appropriate licence scopes
before public distribution. Confirm the complete creator list in `CITATION.cff`.
No DOI, university endorsement, or public availability is claimed today.
