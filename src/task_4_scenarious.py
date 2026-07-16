import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import os

# Ensure visualization and processed directories exist
os.makedirs("data/processed", exist_ok=True)
os.makedirs("reports/figures", exist_ok=True)

# -------------------------------------------------------------------------
# 1. DEFINE HISTORICAL BASELINE DATA (Findex Core Points)
# -------------------------------------------------------------------------
years_hist = np.array([2011, 2014, 2017, 2021, 2024]).reshape(-1, 1)
# Account Ownership (Access)
access_hist = np.array([0.14, 0.22, 0.35, 0.46, 0.49]) # Findex historical [cite: 432]
# Made/Received Digital Payments (Usage)
usage_hist = np.array([0.12, 0.15, 0.22, 0.28, 0.35]) # Findex proxy baseline [cite: 437]

years_pred = np.array([2025, 2026, 2027]).reshape(-1, 1)
all_years = np.concatenate([years_hist.flatten(), years_pred.flatten()])

# -------------------------------------------------------------------------
# 2. RUN BASELINE TREND REGRESSION (Task 4.2 & 4.3)
# -------------------------------------------------------------------------
def fit_and_predict_trend(X_train, y_train, X_pred):
    model = LinearRegression()
    model.fit(X_train, y_train)
    trend_hist = model.predict(X_train)
    trend_pred = model.predict(X_pred)
    
    # Calculate Residual Standard Error (RSE) for prediction intervals
    residuals = y_train - trend_hist
    rse = np.sqrt(np.sum(residuals**2) / (len(y_train) - 2))
    
    # Generate 95% Confidence / Prediction Interval bounds
    # Margin of error approx 1.96 * RSE for illustrative predictive bounds
    margin = 1.96 * rse
    return trend_hist, trend_pred, margin

access_trend_hist, access_trend_pred, access_margin = fit_and_predict_trend(years_hist, access_hist, years_pred)
usage_trend_hist, usage_trend_pred, usage_margin = fit_and_predict_trend(years_hist, usage_hist, years_pred)

# -------------------------------------------------------------------------
# 3. APPLY EVENT-AUGMENTED ADJUSTMENTS (Task 4.3)
# -------------------------------------------------------------------------
# Modeling cumulative event shocks from Task 3 (e.g., Fayda ID Rollout, M-Pesa entry, etc.) [cite: 639]
# Shocks are expressed as percentage point additions over baseline trend
shocks = {
    'base': {
        'access': {2025: 0.02, 2026: 0.04, 2027: 0.06}, # Fayda ID e-KYC ease starts feeding [cite: 549]
        'usage':  {2025: 0.03, 2026: 0.06, 2027: 0.09}  # M-Pesa & Telebirr merchant growth [cite: 416, 549]
    },
    'optimistic': {
        'access': {2025: 0.05, 2026: 0.09, 2027: 0.13}, # Accelerated digital ID onboarding [cite: 549]
        'usage':  {2025: 0.07, 2026: 0.12, 2027: 0.17}  # Seamless system interoperability
    },
    'pessimistic': {
        'access': {2025: -0.01, 2026: -0.02, 2027: -0.03}, # Regulatory bottlenecks, network issues
        'usage':  {2025: -0.02, 2026: -0.03, 2027: -0.04}  # Stagnant smartphone adoption
    }
}

# -------------------------------------------------------------------------
# 4. GENERATE SCENARIOS (Task 4.3)
# -------------------------------------------------------------------------
def build_scenario_forecasts(trend_pred, shock_dict, margin):
    forecasts = {}
    for scenario in ['base', 'optimistic', 'pessimistic']:
        # Baseline + Shock (bounded strictly between 0 and 1.0)
        scenario_pred = np.zeros(len(trend_pred))
        for idx, yr in enumerate([2025, 2026, 2027]):
            # Access the year directly from shock_dict, since 'base' was already resolved outside
            scenario_pred[idx] = np.clip(trend_pred[idx] + shock_dict.get(yr, 0.0), 0.0, 1.0)
            # scenario_pred[idx] = np.clip(trend_pred[idx] + shock_dict[scenario][yr], 0.0, 1.0)
            
        forecasts[scenario] = scenario_pred
        forecasts[f'{scenario}_lower'] = np.clip(scenario_pred - margin, 0.0, 1.0)
        forecasts[f'{scenario}_upper'] = np.clip(scenario_pred + margin, 0.0, 1.0)
    return forecasts

# Pass the whole shocks dictionary, defaulting to an empty dict if it's None
access_forecasts = build_scenario_forecasts(access_trend_pred, shocks if shocks else {}, access_margin)
# access_forecasts = build_scenario_forecasts(access_trend_pred, shocks['base'] if 'base' in shocks else {}, access_margin)
# Overwrite specific scenario lists for multi-path dictionary structures
access_scenarios = {
    'base': build_scenario_forecasts(access_trend_pred, shocks['base'], access_margin),
    'optimistic': build_scenario_forecasts(access_trend_pred, shocks['optimistic'], access_margin),
    'pessimistic': build_scenario_forecasts(access_trend_pred, shocks['pessimistic'], access_margin)
}

usage_scenarios = {
    'base': build_scenario_forecasts(usage_trend_pred, shocks['base'], usage_margin),
    'optimistic': build_scenario_forecasts(usage_trend_pred, shocks['optimistic'], usage_margin),
    'pessimistic': build_scenario_forecasts(usage_trend_pred, shocks['pessimistic'], usage_margin)
}

# -------------------------------------------------------------------------
# 5. EXPORT THE FORECAST TABLE (Task 4.4 / Minimum Essential)
# -------------------------------------------------------------------------
forecast_rows = []
for i, yr in enumerate([2025, 2026, 2027]):
    forecast_rows.append({
        'Year': yr,
        'Access_Base': access_scenarios['base']['base'][i],
        'Access_Base_Lower': access_scenarios['base']['base_lower'][i],
        'Access_Base_Upper': access_scenarios['base']['base_upper'][i],
        'Access_Optimistic': access_scenarios['optimistic']['optimistic'][i],
        'Access_Pessimistic': access_scenarios['pessimistic']['pessimistic'][i],
        
        'Usage_Base': usage_scenarios['base']['base'][i],
        'Usage_Base_Lower': usage_scenarios['base']['base_lower'][i],
        'Usage_Base_Upper': usage_scenarios['base']['base_upper'][i],
        'Usage_Optimistic': usage_scenarios['optimistic']['optimistic'][i],
        'Usage_Pessimistic': usage_scenarios['pessimistic']['pessimistic'][i]
    })

df_forecast = pd.DataFrame(forecast_rows)
# Save predictions
df_forecast.to_csv("data/processed/financial_inclusion_forecasts_2025_2027.csv", index=False)

print("\n=== GENERATED FORECAST TABLE (2025-2027) ===")
print(df_forecast[['Year', 'Access_Base', 'Access_Base_Lower', 'Access_Base_Upper', 'Usage_Base', 'Usage_Base_Lower', 'Usage_Base_Upper']].to_string(index=False))

# -------------------------------------------------------------------------
# 6. SCENARIO VISUALIZATION (Task 4.4)
# -------------------------------------------------------------------------
plt.figure(figsize=(12, 6))

# Plot Access Progress Series
plt.subplot(1, 2, 1)
plt.plot(years_hist, access_hist * 100, 'ko-', label='Historical Findex', linewidth=2)
# Append 2024 to predictions to plot a continuous line
years_plot = np.array([2024, 2025, 2026, 2027])
base_line = np.insert(access_scenarios['base']['base'], 0, access_hist[-1]) * 100
opt_line = np.insert(access_scenarios['optimistic']['optimistic'], 0, access_hist[-1]) * 100
pess_line = np.insert(access_scenarios['pessimistic']['pessimistic'], 0, access_hist[-1]) * 100

plt.plot(years_plot, base_line, 'b--', label='Base Forecast')
plt.plot(years_plot, opt_line, 'g--', label='Optimistic Forecast')
plt.plot(years_plot, pess_line, 'r--', label='Pessimistic Forecast')

# Add Shaded prediction interval for Base Scenario
lower_bounds = np.insert(access_scenarios['base']['base_lower'], 0, access_hist[-1]) * 100
upper_bounds = np.insert(access_scenarios['base']['base_upper'], 0, access_hist[-1]) * 100
plt.fill_between(years_plot, lower_bounds, upper_bounds, color='blue', alpha=0.1, label='95% Base CI')

plt.title("Account Ownership Rate (Access) Projections", fontsize=11, fontweight='bold')
plt.ylabel("Inclusion Rate (%)")
plt.xlabel("Year")
plt.grid(True, alpha=0.3)
plt.legend(loc='upper left')

# Plot Usage Progress Series
plt.subplot(1, 2, 2)
plt.plot(years_hist, usage_hist * 100, 'ko-', label='Historical Findex', linewidth=2)
base_line_u = np.insert(usage_scenarios['base']['base'], 0, usage_hist[-1]) * 100
opt_line_u = np.insert(usage_scenarios['optimistic']['optimistic'], 0, usage_hist[-1]) * 100
pess_line_u = np.insert(usage_scenarios['pessimistic']['pessimistic'], 0, usage_hist[-1]) * 100

plt.plot(years_plot, base_line_u, 'b--')
plt.plot(years_plot, opt_line_u, 'g--')
plt.plot(years_plot, pess_line_u, 'r--')

lower_bounds_u = np.insert(usage_scenarios['base']['base_lower'], 0, usage_hist[-1]) * 100
upper_bounds_u = np.insert(usage_scenarios['base']['base_upper'], 0, usage_hist[-1]) * 100
plt.fill_between(years_plot, lower_bounds_u, upper_bounds_u, color='blue', alpha=0.1)

plt.title("Digital Payment Adoption (Usage) Projections", fontsize=11, fontweight='bold')
plt.ylabel("Inclusion Rate (%)")
plt.xlabel("Year")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("reports/figures/task4_scenario_forecasts.png")
plt.close()
print("\nScenario visualization plot saved successfully under 'reports/figures/'.")