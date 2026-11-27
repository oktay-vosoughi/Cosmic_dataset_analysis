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
