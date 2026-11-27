# Cosmic_dataset_analysis

COSMIC analysis behind the beta-arrestin 1/2 (ARRB1 p.T224N / ARRB2 p.T268I) candidate-mutation selection.
Part of the TUBITAK 2209-A GPCR project.

It covers: missense extraction for a 15-gene GPCR-signaling panel
(GNAS, GNAQ, GNA11, GNA13, GNA14, GNA15, GNAI1, GNAI2, GNB1, GNB3, GNB5, ARR3, SAG, ARRB1, ARRB2),
ARRB1/ARRB2 recurrence and same-sample co-occurrence, per-gene substitution counts, pairwise co-mutation
statistics (Fisher's exact test, Haldane-Anscombe odds ratio, Benjamini-Hochberg FDR), and a comparison with TCGA/GENIE.

## Repository contents

### `src/` - analysis scripts (run in order)
| File | What it does |
|---|---|
| `common.py` | Panel gene list, retained columns, missense label |
| `01_preprocess_cosmic.py` | Raw `CosmicMutantExport.tsv` (read in chunks) -> missense rows of the 15 panel genes, exact gene-symbol match, no `_ENST` transcript rows |
| `02_arrestin_candidates.py` | ARRB1/ARRB2 record, substitution and sample counts; substitution recurrence; samples carrying both genes |
| `03_sample_screen.py` | Pairwise shared samples between all 15 genes; samples mutated in 2 or more panel genes |
| `04_gene_substitution_counts.py` | Count, number of samples and primary sites for every substitution of every panel gene |
| `05_cross_database_check.py` | COSMIC top-5 substitutions per gene vs. TCGA (and optionally AACR GENIE) |

### `notebooks/`
| File | What it does |
|---|---|
| `statistical_co_mutation_analysis.ipynb` | Sample x gene binary matrix (6,152 samples); Fisher's exact test on all 105 gene pairs at pan-cancer level, in lung, and in 25 other primary sites with >=50 samples (27 strata, 2,835 tests); BH correction per stratum. Executed, outputs included |

### `results/` - outputs
| File | Content |
|---|---|
| `CoMutation_Statistical_Results_FULL.csv` | All 2,835 tests: counts, odds ratios, p, q, direction |
| `ARRB1_substitution_recurrence.csv`, `ARRB2_substitution_recurrence.csv` | Substitution counts, samples, primary sites per arrestin gene |
| `arrestin_summary.csv` | Records / unique substitutions / unique samples for ARRB1 and ARRB2 |
| `arrb1_arrb2_same_sample.csv` | The 4 samples with both an ARRB1 and an ARRB2 missense (includes lung sample 2640423: T224N + T268I) |
| `pairwise_shared_samples.csv` | Shared-sample count for every gene pair |
| `samples_with_multiple_panel_genes.csv` | 420 samples mutated in >=2 panel genes |
| `panel_substitution_counts.csv` | Substitution counts for the whole panel |
| `cross_database_check.csv` | COSMIC vs. TCGA overlap per gene |

### Other
| File | Content |
|---|---|
| `external_data/GPCR_Mutations_in_TCGA.xlsx` | TCGA cBioPortal export (open access) |
| `docs/data_provenance.md` | Verified numbers, data lineage, caveats |
| `requirements.txt`, `.gitignore` | Dependencies; `data/` and raw COSMIC files are ignored |

## Run
```bash
pip install -r requirements.txt
python src/01_preprocess_cosmic.py --raw /path/to/CosmicMutantExport.tsv   # writes data/cosmic_panel_missense.csv
python src/02_arrestin_candidates.py
python src/03_sample_screen.py
python src/04_gene_substitution_counts.py
python src/05_cross_database_check.py          # optionally --genie <file>
jupyter nbconvert --to notebook --execute --inplace notebooks/statistical_co_mutation_analysis.ipynb
```

## Key numbers (COSMIC v99, missense only)
- ARRB1: 159 records, 126 unique substitutions, 154 samples. ARRB2: 160 records, 122 unique substitutions, 149 samples.
- 6,152 samples carry a missense in the panel; 4 carry both ARRB1 and ARRB2.
- ARRB1-ARRB2 co-mutation: pan-cancer OR 1.08, q 0.888; lung OR 1.50, q 1.00 (not significant).

## Data and limitations
- The raw COSMIC export (~17 GB) and record-level extracts are licensed by COSMIC and are not included (`data/` is git-ignored).
  Download COSMIC yourself (release v99 was used). The AACR GENIE export is not included either; pass it locally with `--genie`.
- Step 1 was tested on a small synthetic file; steps 2-5 were run on the cleaned COSMIC file.
- TCGA has no ARRB1 rows and GENIE has no arrestin rows, so the cross-check does not validate the arrestin candidates.
- Residue numbering depends on the transcript (e.g. COSMIC GNAS R844 = canonical R201), so cross-database matching of GNAS is incomplete.
- The sample unit is the COSMIC `ID_sample`, not a patient; a missing record is treated as wild-type.
