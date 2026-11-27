"""Shared constants for the COSMIC GPCR-signaling panel analysis."""

# 15-gene panel; matched by EXACT gene symbol (no substring matching, no *_ENST transcript rows).
PANEL = ['GNAS', 'GNAQ', 'GNA11', 'GNA13', 'GNA14', 'GNA15', 'GNAI1', 'GNAI2',
         'GNB1', 'GNB3', 'GNB5', 'ARR3', 'SAG', 'ARRB1', 'ARRB2']

# Columns retained from CosmicMutantExport.tsv
KEEP_COLS = ['Gene name', 'Sample name', 'ID_sample', 'MUTATION_ID',
             'Primary site', 'Mutation AA', 'Tumour origin', 'Age']

MISSENSE = 'Substitution - Missense'
