"""Step 2: ARRB1 / ARRB2 summary, substitution recurrence and same-sample co-mutation.

Usage:
    python src/02_arrestin_candidates.py --cosmic data/cosmic_panel_missense.csv --outdir results
Writes ARRB1/ARRB2 recurrence tables and the samples carrying both genes.
"""
import argparse, os
import pandas as pd


def main(cosmic, outdir):
    os.makedirs(outdir, exist_ok=True)
    df = pd.read_csv(cosmic)
    df = df.loc[:, ~df.columns.str.startswith('Unnamed')]  # drop legacy index columns
    df = df[df['Gene name'].isin(['ARRB1', 'ARRB2'])]

    summary = []
    for g in ['ARRB1', 'ARRB2']:
        d = df[df['Gene name'] == g]
        rec = (d.groupby('Mutation AA')
                 .agg(count=('ID_sample', 'size'),
                      n_samples=('ID_sample', 'nunique'),
                      primary_sites=('Primary site', lambda s: ';'.join(sorted(map(str, s.unique())))))
                 .sort_values(['count'], ascending=False))
        rec.to_csv(f'{outdir}/{g}_substitution_recurrence.csv')
        top = rec['count'].max()
        summary.append({'gene': g, 'records': len(d), 'unique_substitutions': d['Mutation AA'].nunique(),
                        'unique_samples': d['ID_sample'].nunique(), 'max_recurrence': top,
                        'n_substitutions_at_max': int((rec['count'] == top).sum())})
        print(g, summary[-1])
        print(rec.head(10).to_string(), '\n')
    pd.DataFrame(summary).to_csv(f'{outdir}/arrestin_summary.csv', index=False)

    # samples with a missense in BOTH genes
    genes_per_sample = df.groupby('ID_sample')['Gene name'].nunique()
    both = genes_per_sample[genes_per_sample == 2].index
    det = df[df['ID_sample'].isin(both)].sort_values(['ID_sample', 'Gene name'])
    det.to_csv(f'{outdir}/arrb1_arrb2_same_sample.csv', index=False)
    print('samples with ARRB1+ARRB2 missense:', len(both))
    print(det.to_string(index=False))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--cosmic', default='data/cosmic_panel_missense.csv')
    ap.add_argument('--outdir', default='results')
    a = ap.parse_args()
    main(a.cosmic, a.outdir)
