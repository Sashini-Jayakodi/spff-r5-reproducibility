# Release preparation and citation

Private FYP development is authorized by the owner. This guide concerns later
public distribution and citation; it does not authorize publication or a Zenodo
upload. See `FYP_SETUP_CHECKLIST.md` for ordinary private setup.

## Authorization and metadata

Before public distribution, review creator and coauthor rights, third-party
notices, dataset terms, and any actual institutional or manuscript-sharing
conditions that apply. Obtain permission where those terms require it. No
unverified university policy or blanket written-clearance requirement is asserted.
Earlier self-imposed private setup holds were removed at the owner's direction;
this does not establish institutional permission or waive real rights.

The draft `CITATION.cff` uses the local account name Sashini Jayakodi as a proposed
creator. Confirm spelling, full creator list and order, affiliations, and optional
ORCIDs with the authors before release. No version, release date, repository URL,
DOI, or licence is asserted because these have not been established. Add actual
values when known and validate the final CFF against its official schema:
https://citation-file-format.github.io/ . Citation metadata grants no licence.

There is deliberately no active LICENSE. For the rights holder's consideration,
MIT is one possible code licence and CC BY 4.0 one possible licence for original
synthetic data/documentation. These are conditional options, not grants or a
determination of ownership. Review institutional requirements and dependency
licences before choosing. Keep software and data licence scopes explicit and
preserve required third-party notices. Avoid relicensing dependencies as project
code. No manuscript licence is granted by a repository licence. Review the
official terms at https://opensource.org/license/mit and
https://creativecommons.org/licenses/by/4.0/ before approval.

## Private GitHub setup

Install GitHub CLI from https://cli.github.com/ if needed. Run `gh auth status`
and authenticate as the intended owner. Check that the repository name is free.
Create an empty private repository without uploading local files:

```powershell
gh repo create Sashini-Jayakodi/spff-r5-reproducibility --private
```

Review the manifest's explicit file list plus `SHA256SUMS.txt`; exclude generated
evidence, environments, raw datasets, weights, and credentials. Follow
`FYP_SETUP_CHECKLIST.md`, inspect the staged diff and
`git diff --cached --check`, then push `main` to the confirmed private remote.
Do not infer remote existence from the planned URL.

Validate a fresh local clone with the lock file and both runners. A local copy
run is useful but must not be described as a clean clone. Review the complete
release tree and scan for secrets again. Private setup does not authorize public
distribution or a Zenodo transfer.

## Obtain a Zenodo DOI after explicit publication approval

1. Freeze an approved version, for example `v1.0.0`, with actual creator metadata,
   chosen licences, passing checks, release notes, commit hash and SHA-256
   inventory. Treat code and the synthetic expected JSONs as distinct research
   objects if separate software/data records are useful for the approved release.
2. Choose one archiving route for the software. For GitHub integration, first
   approve public visibility and release publication. In Zenodo, connect GitHub,
   open the GitHub page, sync repositories, and enable this repository. Creating
   the approved GitHub release then triggers archival automatically. Keep this
   integration OFF until publication is explicitly approved. Follow
   https://help.zenodo.org/docs/github/enable-repository/ and
   https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content .
3. Alternatively, after explicit approval for a Zenodo upload, create a manual Zenodo
   software upload draft. Select No for an existing DOI and Get a DOI now to
   reserve one. A reserved identifier is not a published, resolving record. Add
   it to the approved metadata before the final manifest/commit if desired,
   upload the exact approved release archive, review the metadata and files,
   and publish only with explicit approval. DOI pre-reservation is unavailable
   through the GitHub integration; do not duplicate the same software release
   through both routes. See
   https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/ and
   https://support.zenodo.org/help/en-gb/24-github-integration/73-can-i-pre-reserved-a-doi-before-a-github-release .
4. If archiving data separately, prepare a dataset record for the approved JSONs
   and their dictionary/checksums. Record the exact
   software version that generated them and link the software and dataset
   records using related identifiers. Do not use the article DOI as the
   software or dataset DOI. Confirm creator, resource type, version, licence,
   funding and access metadata on each record before approved publication.
5. Verify the published files and DOI landing pages. Cite each specific version
   DOI used for the reported findings, rather than the concept DOI for all
   versions: https://zenodo.org/help/versioning . Update `CITATION.cff` and the
   README with the issued software DOI and link the dataset DOI. If this is a
   later metadata commit, distinguish it from the frozen archived commit.

## IEEE Access citation after publication

Use each published Zenodo record's citation export, verify creators, title,
version and year against its landing page, and format it for the IEEE Access
template. A software reference can follow this pattern, replacing every bracketed
field with actual metadata:

> [Authors], "[Software record title]," ver. [version], Zenodo, [year], doi: [version DOI].

Cite the dataset record separately with its actual metadata and version DOI.
In the manuscript's availability statement, identify the exact software version,
synthetic dataset and persistent links. State that these are synthetic numerical
experiments and contain no real sign-image observations. Until records are
published, retain a truthful private-development statement and do not claim
public availability. Link the manuscript DOI back from the Zenodo records once
the article has its real DOI. IEEE Access also permits supplemental code/data
with the submission; that route needs the same rights clearance:
https://ieeeaccess.ieee.org/authors/preparing-your-article/ .
