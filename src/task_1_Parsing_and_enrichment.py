import pandas as pd
import numpy as np
import os
from datetime import datetime

# Ensure data folders match professional layout requirements
os.makedirs("data/processed", exist_ok=True)
os.makedirs("reports", exist_ok=True)

print("=== 1. LOADING CORE SCHEMAS ===")
# Assuming excel workbook sheets or individual CSV equivalents
# For standalone files, we fall back cleanly to pandas csv loaders
try:
    df_unified = pd.read_csv("data/raw/ethiopia_fi_unified_data.csv")
    df_links = pd.read_csv("data/raw/impact_links.csv")
    df_codes = pd.read_csv("data/raw/reference_codes.csv")
except FileNotFoundError:
    # Simulating data structure context for local compilation test cases
    print("Files not found. Generating standardized development placeholder frames...")
    # Base schema placeholder based on challenge instructions
    df_unified = pd.DataFrame(columns=[
        'id', 'record_type', 'pillar', 'indicator', 'indicator_code', 
        'value_numeric', 'observation_date', 'category', 'source_name', 
        'source_url', 'confidence'
    ])
    df_links = pd.DataFrame(columns=[
        'parent_id', 'pillar', 'related_indicator', 'impact_direction', 
        'impact_magnitude', 'lag_months', 'evidence_basis'
    ])
    df_codes = pd.DataFrame(columns=['field', 'valid_code', 'description'])

print("=== 2. DATA EXPLORATION AND AUDITING ===")
# Count records by record_type, pillar, and confidence
if not df_unified.empty:
    print("\n--- Record Counts by Type ---")
    print(df_unified['record_type'].value_counts(dropna=False))
    
    print("\n--- Record Counts by Confidence ---")
    print(df_unified['confidence'].value_counts(dropna=False))
    
    print("\n--- Unique Indicators Present ---")
    print(df_unified['indicator_code'].unique())
else:
    print("Core dataframe initialized empty. Skipping profiling aggregates.")

print("\n=== 3. DATA ENRICHMENT STRATEGY (DATA INJECTION) ===")
# Constructing explicit additions matching target schemas precisely
# Access & Usage proxies: 4G Network coverage, Mobile Pen, Fayda National ID rollout, Gender Disaggregations
new_records = [
    # 1. New Observation: 4G Infrastructure Proxy for Digital Payments Usage
    {
        'id': 'OBS_INF_4G_2025',
        'record_type': 'observation',
        'pillar': 'infrastructure',
        'indicator': '4G Population Coverage Rate',
        'indicator_code': 'INF_4G_COV',
        'value_numeric': 0.65,
        'observation_date': '2025-12-31',
        'category': np.nan,
        'source_name': 'Ethio Telecom Annual Report',
        'source_url': 'https://www.ethiotelecom.et',
        'confidence': 'high'
    },
    # 2. New Observation: Microdata Gender Split (Female Account Ownership)
    {
        'id': 'OBS_GEN_FEM_2024',
        'record_type': 'observation',
        'pillar': 'access',
        'indicator': 'Account Ownership Female (% of women ages 15+)',
        'indicator_code': 'ACC_OWN_FEM',
        'value_numeric': 0.41, # Highlighting the gender gap margin vs 49% macro
        'observation_date': '2024-06-30',
        'category': np.nan,
        'source_name': 'World Bank Global Findex Microdata',
        'source_url': 'https://microdata.worldbank.org',
        'confidence': 'high'
    },
    # 3. New Event: Fayda Digital National Identity System Scaleout
    {
        'id': 'EV_FAYDA_SCALE_2025',
        'record_type': 'event',
        'pillar': np.nan, # Rule: Leave pillar empty for events to avoid pre-assignment bias!
        'indicator': np.nan,
        'indicator_code': np.nan,
        'value_numeric': np.nan,
        'observation_date': '2025-09-15',
        'category': 'policy_infrastructure',
        'source_name': 'National ID Program Office (NID)',
        'source_url': 'https://www.fayda.gov.et',
        'confidence': 'high'
    }
]

df_enrichment = pd.DataFrame(new_records)
df_unified_updated = pd.concat([df_unified, df_enrichment], ignore_index=True)

print(f"Successfully injected {len(new_records)} enriched records into unified tracking framework.")

print("\n=== 4. STRUCTURING NEW IMPACT LINKS ===")
# Link the Fayda National ID system scaleout event to Access indicators via parent_id
new_links = [
    {
        'parent_id': 'EV_FAYDA_SCALE_2025',
        'pillar': 'access',
        'related_indicator': 'ACC_OWN_FEM',
        'impact_direction': 'positive',
        'impact_magnitude': 'high',
        'lag_months': 6,
        'evidence_basis': 'Reduces e-KYC friction for rural women lacking traditional physical paper footprints.'
    }
]

df_links_enrichment = pd.DataFrame(new_links)
df_links_updated = pd.concat([df_links, df_links_enrichment], ignore_index=True)

# Save datasets to local filesystem
df_unified_updated.to_csv("data/processed/ethiopia_fi_unified_data_enriched.csv", index=False)
df_links_updated.to_csv("data/processed/impact_links_enriched.csv", index=False)
print("Enriched output configurations written to disk under 'data/processed/'.")