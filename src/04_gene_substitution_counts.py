"""Step 4: per-gene amino-acid substitution counts (replaces the hand-made cosmicMutations_07_2024.xlsx).

Usage: python src/04_gene_substitution_counts.py --cosmic data/cosmic_panel_missense.csv --outdir results
Writes results/panel_substitution_counts.csv (gene, Mutation AA, count, n_samples, primary sites).
"""
import argparse, os
import pandas as pd
from common import PANEL


def main(cosmic, outdir):
    os.makedirs(outdir, exist_ok=True)
    df = pd.read_csv(cosmic)
    df = df[df['Gene name'].isin(PANEL)]
    out = (df.groupby(['Gene name', 'Mutation AA'])
             .agg(count=('ID_sample', 'size'), n_samples=('ID_sample', 'nunique'),
                  primary_sites=('Primary site', lambda s: ';'.join(sorted(map(str, s.unique())))))
             .reset_index().sort_values(['Gene name', 'count'], ascending=[True, False]))
    out.to_csv(f'{outdir}/panel_substitution_counts.csv', index=False)
    print(out.groupby('Gene name').size().rename('unique_substitutions').to_string())


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--cosmic', default='data/cosmic_panel_missense.csv')
    ap.add_argument('--outdir', default='results')
    a = ap.parse_args()
    main(a.cosmic, a.outdir)
