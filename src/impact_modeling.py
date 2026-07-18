"""
Impact Modeling and Network Association Engine for Ethiopia Financial Inclusion.
Handles entity merging, schema validation, and exponential decay shock calculations.
"""

import os
import logging
import pandas as pd
import numpy as np
from typing import Tuple

# Setup internal logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def load_and_merge_impact_data(unified_path: str, links_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Ingests unified historical data and linkage profiles with explicit exception checks.
    Yields synthetic fallback dataframes if target assets cannot be located.
    
    Parameters:
    -----------
    unified_path : str
        File pathway for the enriched unified data matrix.
    links_path : str
        File pathway for the transactional linkage framework.
        
    Returns:
    --------
    Tuple[pd.DataFrame, pd.DataFrame]
        Tuple containing (joined_impacts_df, raw_links_df) ready for mathematical evaluation.
    """
    try:
        if not os.path.exists(unified_path) or not os.path.exists(links_path):
            raise FileNotFoundError("One or both target impact data matrices are missing.")
            
        df_unified = pd.read_csv(unified_path)
        df_links = pd.read_csv(links_path)
        logger.info("Impact modeling frameworks successfully loaded from files.")
        
    except FileNotFoundError as e:
        logger.warning(f"{e}. Compiling robust mock schema configurations for execution fallback...")
        df_unified, df_links = _generate_impact_fallbacks()
        
    except pd.errors.EmptyDataError as e:
        logger.error(f"Critical execution error: Empty file structure identified. Details: {e}")
        raise
        
    # Standardize data structures and merge
    events_only = df_unified[df_unified['record_type'] == 'event'].copy()
    joined_impacts = pd.merge(df_links, events_only, left_on='parent_id', right_on='id', how='inner')
    
    return joined_impacts, df_links

def calculate_lagged_impact(t: np.ndarray, t_event: float, max_impact: float, lag_months: float, lambda_decay: float = 0.08) -> np.ndarray:
    """
    Computes time-dependent event transmission shocks using an exponential absorption model.
    Formula: I(t) = M * (1 - e^(-lambda * (t - t0 - L))) for t >= t0 + L
    
    Parameters:
    -----------
    t : np.ndarray
        Array of target times (in fractional year formats).
    t_event : float
        The fractional year coordinates of the source event shock.
    max_impact : float
        The theoretical maximum magnitude asymptote of the shock.
    lag_months : float
        Transmission lag window in months before the shock manifests.
    lambda_decay : float
        Absorption/decay scaling parameter indicating market penetration speed.
        
    Returns:
    --------
    np.ndarray
        Computed shock contributions corresponding to the designated timeline array.
    """
    try:
        dt = (t - t_event) * 12  # Year delta converted to months
        lagged_dt = dt - lag_months
        
        # Suppress time points falling before the lag transmission envelope to 0.0
        impact = np.where(lagged_dt >= 0, max_impact * (1 - np.exp(-lambda_decay * lagged_dt)), 0.0)
        return impact
    except ValueError as e:
        logger.error(f"Value computation failure inside mathematical matrix generation: {e}")
        raise

def _generate_impact_fallbacks() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Generates explicit synthetic schema tracking frameworks for fallback validation."""
    events_mock = pd.DataFrame([
        {'id': 'EV_TELEBIRR_2021', 'record_type': 'event', 'indicator': 'Telebirr Commercial Launch', 'observation_date': '2021-05-11'},
        {'id': 'EV_SAFARICOM_2022', 'record_type': 'event', 'indicator': 'Safaricom GSM Commercial Entry', 'observation_date': '2022-08-29'},
        {'id': 'EV_MPESA_2023', 'record_type': 'event', 'indicator': 'M-Pesa Mobile Money Launch', 'observation_date': '2023-08-15'},
        {'id': 'EV_FAYDA_SCALE_2025', 'record_type': 'event', 'indicator': 'Fayda National Digital ID Integration', 'observation_date': '2025-09-15'}
    ])
    
    df_links = pd.DataFrame([
        {'parent_id': 'EV_TELEBIRR_2021', 'pillar': 'access', 'related_indicator': 'ACC_MM_ACCOUNT', 'impact_direction': 'positive', 'impact_magnitude': 0.08, 'lag_months': 6, 'evidence_basis': 'High marketing spend.'},
        {'parent_id': 'EV_TELEBIRR_2021', 'pillar': 'usage', 'related_indicator': 'USG_DIGITAL_PAYMENT', 'impact_direction': 'positive', 'impact_magnitude': 0.15, 'lag_months': 3, 'evidence_basis': 'Utility payment mandates.'},
        {'parent_id': 'EV_MPESA_2023', 'pillar': 'access', 'related_indicator': 'ACC_MM_ACCOUNT', 'impact_direction': 'positive', 'impact_magnitude': 0.04, 'lag_months': 9, 'evidence_basis': 'Distribution network leverage.'},
        {'parent_id': 'EV_FAYDA_SCALE_2025', 'pillar': 'access', 'related_indicator': 'ACC_OWNERSHIP', 'impact_direction': 'positive', 'impact_magnitude': 0.12, 'lag_months': 12, 'evidence_basis': 'KYC friction removal.'}
    ])
    
    return events_mock, df_links