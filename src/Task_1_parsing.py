import pandas as pd
import numpy as np

# Load the core unified dataset
df_unified = pd.read_excel("./data/raw/ethiopia_fi_unified_data.xlsx") # [cite: 97]

# Partition by record_type to preserve logical segregation
observations = df_unified[df_unified['record_type'] == 'observation'].copy() # [cite: 46]
events = df_unified[df_unified['record_type'] == 'event'].copy() # [cite: 46]
targets = df_unified[df_unified['record_type'] == 'target'].copy() # [cite: 46]

# Load the separate impact_links mapping file/sheet
impact_links = pd.read_excel("./data/processed/impact_links.xlsx") # Or parsed from secondary sheet