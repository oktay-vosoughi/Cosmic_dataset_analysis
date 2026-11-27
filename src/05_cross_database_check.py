"""Step 5: compare COSMIC panel substitutions with TCGA (and optionally AACR GENIE) cBioPortal exports.

For each panel gene present in the external file, reports how many external missense records exist and how many of
COSMIC's top-5 recurrent substitutions are also seen there. Genes absent from an external dataset are listed
explicitly (TCGA export: no ARRB1; GENIE export: only GNAS, GNAQ, GNA11, GNB1) - so for ARRB1 nothing is validated.

Usage:
  python src/05_cross_database_check.py --cosmic data/cosmic_panel_missense.csv \
      --tcga external_data/GPCR_Mutations_in_TCGA.xlsx [--genie /path/to/GPCR_Mutations_in_AACR_GENIE.xlsx]
"""
import argparse, os
import pandas as pd
from common import PANEL


def load_ext(path):
    d = pd.read_excel(path)
    d['Hugo_Symbol'] = d['Hugo_Symbol'].astype(str).str.strip().str.upper().str.replace(' ', '', regex=False)
    d = d[d['Variant_Classification'] == 'Missense_Mutation'].copy()
    h = d['HGVSp_Short'].astype(str).str.strip()
    d['Mutation AA'] = h.where(h.str.startswith('p.'), 'p.' + h)   # cBioPortal omits the 'p.' prefix COSMIC uses
    return d


def main(cosmic, datasets, outdir):
    os.makedirs(outdir, exist_ok=True)
    c = pd.read_csv(cosmic)
    c = c[c['Gene name'].isin(PANEL)]
    rows = []
    for name, path in datasets.items():
        e = load_ext(path)
        for g in PANEL:
            top = c[c['Gene name'] == g]['Mutation AA'].value_counts().head(5).index
            eg = e[e['Hugo_Symbol'] == g]
            rows.append({'dataset': name, 'gene': g, 'external_missense_records': len(eg),
                         'cosmic_top5_seen_in_external': int(pd.Series(top).isin(eg['Mutation AA']).sum()) if len(eg) else None,
                         'status': 'present' if len(eg) else 'absent from external export'})
    out = pd.DataFrame(rows)
    out.to_csv(f'{outdir}/cross_database_check.csv', index=False)
    print(out.to_string(index=False))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--cosmic', default='data/cosmic_panel_missense.csv')
    ap.add_argument('--tcga', default='external_data/GPCR_Mutations_in_TCGA.xlsx')
    ap.add_argument('--genie', default=None)
    ap.add_argument('--outdir', default='results')
    a = ap.parse_args()
    ds = {'TCGA': a.tcga}
    if a.genie:
        ds['AACR_GENIE'] = a.genie
    main(a.cosmic, ds, a.outdir)
