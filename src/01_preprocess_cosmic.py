"""Step 1: raw CosmicMutantExport.tsv -> cleaned missense table for the 15-gene panel.

Usage:
    python src/01_preprocess_cosmic.py --raw CosmicMutantExport.tsv --out data/cosmic_panel_missense.csv

The raw file (~17 GB) is read in chunks. Rows are kept only if
  * 'Mutation Description' == 'Substitution - Missense', and
  * 'Gene name' is EXACTLY one of the panel symbols (so ARRB1_ENST... transcript rows,
    SAGE1, CSAG1/2 and GNB1L are NOT captured, unlike the original substring match).
The raw COSMIC file is licensed and is not distributed with this repository.
"""
import argparse
import pandas as pd
from common import PANEL, KEEP_COLS, MISSENSE


def main(raw, out, chunksize):
    parts, n_total, n_missense = [], 0, 0
    usecols = KEEP_COLS + ['Mutation Description']
    for chunk in pd.read_csv(raw, sep='\t', usecols=usecols, chunksize=chunksize, low_memory=False):
        n_total += len(chunk)
        chunk = chunk[chunk['Mutation Description'] == MISSENSE]
        n_missense += len(chunk)
        parts.append(chunk.loc[chunk['Gene name'].isin(PANEL), KEEP_COLS])
    df = pd.concat(parts, ignore_index=True)
    df.to_csv(out, index=False)
    print(f'rows read: {n_total:,} | missense: {n_missense:,} | panel missense kept: {len(df):,}')
    print(df['Gene name'].value_counts().to_string())


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--raw', required=True)
    ap.add_argument('--out', default='data/cosmic_panel_missense.csv')
    ap.add_argument('--chunksize', type=int, default=500_000)
    a = ap.parse_args()
    main(a.raw, a.out, a.chunksize)
