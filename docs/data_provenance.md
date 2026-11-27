# Data provenance and verified numbers

Source: COSMIC `CosmicMutantExport.tsv` (release v99 per the authors; the version is not recorded inside the file, GRCh38).
Filter: `Mutation Description == "Substitution - Missense"`; gene panel matched by **exact** symbol.

Rows with Ensembl-transcript suffixes (e.g. `ARRB1_ENST00000360025`) are alternative transcripts with shifted
residue numbering and are excluded, not collapsed (P360S on the canonical transcript = P352S on ENST00000360025).

| Quantity | Value |
|---|---|
| ARRB1 missense records / unique substitutions / samples | 159 / 126 / 154 |
| ARRB2 missense records / unique substitutions / samples | 160 / 122 / 149 |
| Samples with missense in the 15-gene panel | 6,152 |
| Samples carrying both ARRB1 and ARRB2 missense | 4 (ID_sample 1783335, 2013571, 2121726, 2640423) |
| Lung sample with ARRB1 p.T224N + ARRB2 p.T268I | ID_sample 2640423 (sample "019") |
| ARRB1 most recurrent substitution | p.P360S (4); p.T224N is one of seven substitutions at 3 |
| Pairwise tests (Fisher, 27 strata x 105 pairs) | 2,835; ARRB1-ARRB2 pan-cancer OR 1.08, p 0.789, q 0.888; lung OR 1.50, p 0.519, q 1.00 |

Reproduced from `cosmiccleaned_07_24.csv` by `src/02_arrestin_candidates.py` and `notebooks/statistical_co_mutation_analysis.ipynb`.

## Caveats
- The unit is the COSMIC `ID_sample`, not a patient.
- Absence of a record is treated as wild-type; it cannot be told apart from "not sequenced".
- Pan-cancer exclusivity involving GNAS/GNAQ/GNA11 is confounded by tissue of origin; use the tissue-stratified results.
- Raw COSMIC data is licensed and not redistributed here; obtain it from https://cancer.sanger.ac.uk/cosmic.

## Cross-database check (TCGA / AACR GENIE)
`src/05_cross_database_check.py` compares COSMIC's top-5 substitutions per gene with the cBioPortal exports.
- The TCGA export has **no ARRB1** rows and the GENIE export contains only GNAS, GNAQ, GNA11 and GNB1, so ARRB1
  (and ARRB2 for GENIE) is **not validated** by either; ARRB2 p.T268I is not confirmed externally.
- Residue numbering is transcript-dependent: COSMIC reports the GNAS hotspot as p.R844C/H, which is R201C/H on the
  canonical transcript used by cBioPortal. Overlap counts for GNAS are therefore not meaningful without mapping.
- The TCGA workbook (`external_data/`) is a hand-assembled cBioPortal export with some untidy gene names
  (e.g. `GNB4    `, `Gna 13`); the script strips whitespace. The AACR GENIE export is not redistributed here
  (GENIE data-use terms); pass it locally with `--genie`.
