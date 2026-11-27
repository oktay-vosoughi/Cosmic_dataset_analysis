"""Step 3: exploratory sample-level screen - which COSMIC samples carry missense in >=2 panel genes.

Replaces the old 'final cosmic.ipynb', which omitted ARRB1 and had an empty GNB1 list (typo 'GNAB1').
Here all 15 panel genes are included.

Usage: python src/03_sample_screen.py --cosmic data/cosmic_panel_missense.csv --outdir results
"""
import argparse, os
from itertools import combinations
import pandas as pd
from common import PANEL


def main(cosmic, outdir):
    os.makedirs(outdir, exist_ok=True)
    df = pd.read_csv(cosmic)
    df = df.loc[:, ~df.columns.str.startswith('Unnamed')]  # drop legacy index columns
    df = df[df['Gene name'].isin(PANEL)]
    sets = {g: set(df.loc[df['Gene name'] == g, 'ID_sample']) for g in PANEL}
    rows = [{'gene1': a, 'gene2': b, 'n_shared_samples': len(sets[a] & sets[b]),
             'shared_ID_samples': ';'.join(map(str, sorted(sets[a] & sets[b])))}
            for a, b in combinations(PANEL, 2)]
    pd.DataFrame(rows).sort_values('n_shared_samples', ascending=False).to_csv(
        f'{outdir}/pairwise_shared_samples.csv', index=False)
    per = (df.groupby('ID_sample')['Gene name'].agg(lambda s: ';'.join(sorted(set(s)))).to_frame('genes'))
    per['n_genes'] = per['genes'].str.count(';') + 1
    multi = per[per['n_genes'] >= 2].sort_values('n_genes', ascending=False)
    multi.to_csv(f'{outdir}/samples_with_multiple_panel_genes.csv')
    print('samples with panel missense:', len(per), '| with >=2 panel genes:', len(multi))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--cosmic', default='data/cosmic_panel_missense.csv')
    ap.add_argument('--outdir', default='results')
    a = ap.parse_args()
    main(a.cosmic, a.outdir)
