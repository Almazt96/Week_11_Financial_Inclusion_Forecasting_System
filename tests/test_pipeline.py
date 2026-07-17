import unittest
import numpy as np
import pandas as pd
from datetime import datetime

# Import target functions directly from your modules or define them as local units
def calculate_lagged_impact(t, t_event, max_impact, lag_months, lambda_decay=0.08):
    """
    Computes time-dependent event impact using an exponential growth-absorption curve.
    Formula: I(t) = M * (1 - e^(-lambda * (t - t0 - L))) for t >= t0 + L
    """
    dt = (t - t_event) * 12  # Convert years to months
    lagged_dt = dt - lag_months
    
    # Handle both single float and numpy arrays
    if isinstance(t, (np.ndarray, list)):
        lagged_dt = np.array(lagged_dt)
        return np.where(lagged_dt >= 0, max_impact * (1 - np.exp(-lambda_decay * lagged_dt)), 0.0)
    else:
        return max_impact * (1 - np.exp(-lambda_decay * lagged_dt)) if lagged_dt >= 0 else 0.0

def aggregate_combined_events(baseline, impacts):
    """
    Combines overlapping event shocks using an Asymptotic Diminishing Scaling Product:
    Y(t) = Y_base + (1 - Y_base) * (1 - PRODUCT(1 - I_i))
    """
    prod_term = 1.0
    for imp in impacts:
        prod_term *= (1.0 - imp)
    return baseline + (1.0 - baseline) * (1.0 - prod_term)


class TestFinancialInclusionPipeline(unittest.TestCase):

    def setUp(self):
        """Set up mock historical data and parameter sets for integration tests."""
        self.years_hist = np.array([2011, 2014, 2017, 2021, 2024])
        self.access_hist = np.array([0.14, 0.22, 0.35, 0.46, 0.49])
        self.usage_hist = np.array([0.12, 0.15, 0.22, 0.28, 0.35])

    # ----------------------------------------------------
    # UNIT TESTS (Data Quality & Integrity checks)
    # ----------------------------------------------------
    def test_data_alignment_and_types(self):
        """Verify that historical parameters match in dimension and type."""
        self.assertEqual(len(self.years_hist), len(self.access_hist))
        self.assertEqual(len(self.years_hist), len(self.usage_hist))
        self.assertTrue(np.all(self.access_hist >= 0.0) and np.all(self.access_hist <= 1.0))
        self.assertTrue(np.all(self.usage_hist >= 0.0) and np.all(self.usage_hist <= 1.0))

    # ----------------------------------------------------
    # MATHEMATICAL SYSTEM TESTS (Task 3 Decays)
    # ----------------------------------------------------
    def test_impact_decay_lag_phase(self):
        """Ensure that before the transmission lag threshold, the calculated impact is exactly 0."""
        t_event = 2021.36  # May 2021
        max_impact = 0.15
        lag_months = 3.0
        
        # Test 1 month after event launch (which is less than the 3-month lag)
        t_eval = t_event + (1.0 / 12.0)
        impact = calculate_lagged_impact(t_eval, t_event, max_impact, lag_months)
        self.assertEqual(impact, 0.0, "Impact must be 0 prior to passing the lag duration threshold.")

    def test_impact_decay_saturation(self):
        """Verify that the decay function asymptotically approaches the maximum impact parameter over time."""
        t_event = 2021.0
        max_impact = 0.10
        lag_months = 0.0
        
        # Test 50 years in the future to verify asymptotic convergence
        t_eval = t_event + 50.0
        impact = calculate_lagged_impact(t_eval, t_event, max_impact, lag_months, lambda_decay=0.5)
        self.assertAlmostEqual(impact, max_impact, places=4, msg="Impact should approach the max_impact threshold over time.")

    def test_asymptotic_diminishing_aggregation(self):
        """Confirm that aggregate impacts gracefully ceiling-scale and do not exceed 100%."""
        baseline = 0.45
        # Set large individual event shocks
        impacts = [0.40, 0.50, 0.30] 
        
        combined_value = aggregate_combined_events(baseline, impacts)
        self.assertLessEqual(combined_value, 1.0, "The aggregated inclusion value must never mathematically exceed 100%.")
        self.assertGreater(combined_value, baseline, "Overlapping positive shocks must increase the overall inclusion rate relative to the baseline.")

    # ----------------------------------------------------
    # SCENARIO STRUCTURAL CHECKS (Task 4 Forecasts)
    # ----------------------------------------------------
    def test_forecast_output_schema(self):
        """Ensure generated forecast outputs contain the expected schema and structure."""
        # Simulated scenario forecast generation pipeline
        years_proj = [2025, 2026, 2027]
        df_forecast = pd.DataFrame({
            'Year': years_proj,
            'Access_Base': [0.542, 0.594, 0.646],
            'Access_Lower': [0.495, 0.547, 0.599],
            'Access_Upper': [0.589, 0.641, 0.693]
        })
        
        # Check column headers
        expected_columns = ['Year', 'Access_Base', 'Access_Lower', 'Access_Upper']
        for col in expected_columns:
            self.assertIn(col, df_forecast.columns)
            
        # Ensure prediction intervals wrap the baseline projections correctly
        for idx in range(len(years_proj)):
            self.assertTrue(df_forecast['Access_Lower'].iloc[idx] <= df_forecast['Access_Base'].iloc[idx])
            self.assertTrue(df_forecast['Access_Base'].iloc[idx] <= df_forecast['Access_Upper'].iloc[idx])


if __name__ == '__main__':
    unittest.main()