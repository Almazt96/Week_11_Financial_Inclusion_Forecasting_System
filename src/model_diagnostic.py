import os
import sys
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from pathlib import Path

def evaluate_model_diagnostics(model_results):
    """Generates formal diagnostic plots and prints statistical test metrics
    for time-series forecasting models.
    """
    print("=" * 60)
    print(" FORMAL MODEL DIAGNOSTIC METRICS ")
    print("=" * 60)

    # 1. Ljung-Box Test for Autocorrelation
    lb_test = sm.stats.acorr_ljungbox(model_results.resid, lags=[10], return_df=True)
    p_val = lb_test["lb_pvalue"].values[0]
    print(f"Ljung-Box Test (Lag 10) p-value: {p_val:.4f}")
    if p_val > 0.05:
        print("-> Success: Residuals show no significant serial correlation (White Noise).")
    else:
        print("-> Warning: Significant residual autocorrelation detected. Consider adjusting lags.")

    # 2. Jarque-Bera Test for Normality
    jb_test = sm.stats.stattools.jarque_bera(model_results.resid)
    print(f"Jarque-Bera Test p-value: {jb_test[1]:.4f}")
    if jb_test[1] > 0.05:
        print("-> Success: Residuals are normally distributed.")
    else:
        print("-> Note: Residuals are not perfectly normally distributed (common in real-world financial data).")

    print("\nGenerating Diagnostic Plots...")
    
    # Ensure the directory to save the image exists
    os.makedirs("reports/figures", exist_ok=True)
    
    fig = model_results.plot_diagnostics(figsize=(12, 8))
    plt.tight_layout()
    plt.savefig("reports/figures/model_formal_diagnostics.png", dpi=300)
    print("Diagnostic plots successfully saved to: reports/figures/model_formal_diagnostics.png")
    plt.show()
    
    return model_results


# =============================================================================
# EXECUTION BLOCK 
# =============================================================================
if __name__ == "__main__":
    # Ensure project root is in the path for safe importing
    script_dir = Path(__file__).resolve().parent
    if str(script_dir.parent) not in sys.path:
        sys.path.append(str(script_dir.parent))
        
    from src.data_processing import load_financial_inclusion_data
    from src.config import RAW_DATA_PATH

    model_path = "models/sarimax_model.pkl"
    
    # OPTION A: If you saved your model as a file from your notebook, load it:
    if os.path.exists(model_path):
        print(f"Loading pre-trained model from {model_path}...")
        model_results = sm.load(model_path)
        
    # OPTION B: If no saved model exists, we fit a quick one on the fly to test it:
    else:
        print("No saved model found. Preparing pipeline data to train a baseline model...")
        
        try:
            # Use pipeline function directly instead of reading a missing processed CSV
            df = load_financial_inclusion_data(str(RAW_DATA_PATH))
            print(f"Successfully loaded and processed {len(df)} rows for diagnostics.")
        except Exception as e:
            print(f"Pipeline loading failed: {e}. Falling back to synthetic generator...")
            from src.data_processing import _generate_synthetic_fallback
            df = _generate_synthetic_fallback()

        # Fit a quick baseline SARIMAX model to make 'model_results' valid
        # Identify the first numeric column to use as the target variable
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if not numeric_cols:
            raise ValueError("No numeric columns found in data to fit a fallback time-series model.")
        
        target_variable = numeric_cols[0]
        print(f"Fitting temporary fallback SARIMAX(1, 0, 0) model on: '{target_variable}'")
        
        # Train a basic AR(1) model to populate residuals
        endog = df[target_variable]
        fallback_model = sm.tsa.statespace.SARIMAX(endog, order=(1, 0, 0), trend='c')
        model_results = fallback_model.fit(disp=False)

    # Run the diagnostic test metrics suite safely
    evaluate_model_diagnostics(model_results)