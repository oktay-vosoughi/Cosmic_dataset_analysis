# Cosmic_dataset_analysis

COSMIC analysis behind the beta-arrestin 1/2 (ARRB1 p.T224N / ARRB2 p.T268I) candidate-mutation selection:
missense extraction for a 15-gene GPCR-signaling panel (GNAS, GNAQ, GNA11, GNA13, GNA14, GNA15, GNAI1, GNAI2,
GNB1, GNB3, GNB5, ARR3, SAG, ARRB1, ARRB2), ARRB1/ARRB2 recurrence and same-sample co-occurrence, and
pairwise co-mutation statistics (Fisher's exact, Haldane-Anscombe OR, Benjamini-Hochberg).
Originally part of the TUBITAK 2209-A GPCR project. This version replaces the earlier incomplete notebook.

## Pipeline
| Step | File | Output |
|---|---|---|
| 1 | `src/01_preprocess_cosmic.py` | `data/cosmic_panel_missense.csv` (from raw `CosmicMutantExport.tsv`, chunked) |
| 2 | `src/02_arrestin_candidates.py` | ARRB1/ARRB2 recurrence tables, same-sample co-mutations |
| 3 | `src/03_sample_screen.py` | samples mutated in >=2 panel genes |
| 4 | `src/04_gene_substitution_counts.py` | per-gene substitution counts for the whole panel |
| 5 | `src/05_cross_database_check.py` | COSMIC vs TCGA/GENIE comparison (see caveats in `docs/data_provenance.md`) |
| 6 | `notebooks/statistical_co_mutation_analysis.ipynb` | `results/CoMutation_Statistical_Results_FULL.csv` |

```bash
pip install -r requirements.txt
python src/01_preprocess_cosmic.py --raw /path/to/CosmicMutantExport.tsv
python src/02_arrestin_candidates.py
python src/03_sample_screen.py
python src/04_gene_substitution_counts.py
python src/05_cross_database_check.py   # optionally --genie <file>
jupyter nbconvert --to notebook --execute --inplace notebooks/statistical_co_mutation_analysis.ipynb
```

`results/` holds the outputs from the authors' run; numbers and caveats are in `docs/data_provenance.md`.

## Data
The raw COSMIC export (about 17 GB) and record-level extracts are licensed by COSMIC and are **not** included
(`data/` is git-ignored). `external_data/` holds the open-access TCGA cBioPortal export. Download COSMIC yourself (release v99 was used).

## Differences from the old code
Exact gene-symbol matching (the old substring match also caught SAGE1, CSAG1/2, GNB1L), ARRB1 and GNB1 now
included in the sample screen, no hard-coded Windows paths, scripts runnable from the command line.

## Change log (Nov 2026 rewrite)
**Removed** (old, non-working uploads from 2024; still in git history):
`cosmic.ipynb`, `cosmic preprocess.ipynb`, `final cosmic.ipynb`, `preproseccing 2.ipynb`.

**Added**
- `src/01-05` scripts (preprocessing, ARRB1/ARRB2 candidates, sample screen, per-gene counts, cross-database check) and `src/common.py`.
- `notebooks/statistical_co_mutation_analysis.ipynb` (executed; Fisher / Haldane-Anscombe / Benjamini-Hochberg).
- `results/` (statistics for 2,835 tests, ARRB recurrence tables, same-sample co-mutations, panel counts, cross-database table).
- `external_data/GPCR_Mutations_in_TCGA.xlsx`, `docs/data_provenance.md`, `requirements.txt`, `.gitignore`.

**Verified** against `cosmiccleaned_07_24.csv`: ARRB1 159 records / 126 substitutions / 154 samples; ARRB2 160 / 122 / 149;
6,152 panel samples; 4 samples with ARRB1+ARRB2 missense (incl. lung sample 2640423, T224N + T268I);
the statistics table is identical to the earlier run. Step 1 (raw file) was tested on a synthetic file only.

**Known limitations**
- TCGA has no ARRB1 and GENIE has no arrestins, so the cross-check does not validate the arrestin candidates.
- Residue numbering differs between transcripts/databases (e.g. GNAS R844 in COSMIC = R201 canonical).
- COSMIC raw data, the AACR GENIE export, and unpublished manuscript files are intentionally not included.
