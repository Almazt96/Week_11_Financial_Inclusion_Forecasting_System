import numpy as np
import pandas as pd

# Define timeline: 2011 to 2027
years = np.arange(2011, 2028)
t = years - 2011

# 1. Fit historical baseline trend (2011-2024)
historical_years = np.array([2011, 2014, 2017, 2021, 2024]) [cite: 26]
historical_y = np.array([0.14, 0.22, 0.35, 0.46, 0.49]) [cite: 26]

slope, intercept = np.polyfit(historical_years, historical_y, 1)

# Generate baseline projection
baseline_forecast = intercept + slope * years

# 2. Layer scenario interventions for 2025-2027
# Assume combined event effects kick in from 2025 onwards (e.g., Fayda + interoperability)
event_impact_base = np.zeros(len(years))
event_impact_opt  = np.zeros(len(years))
event_impact_pess = np.zeros(len(years))

for idx, yr in enumerate(years):
    if yr >= 2025:
        # Base Scenario: Gradual event impact
        event_impact_base[idx] = 0.025 * (yr - 2024)
        # Optimistic Scenario: Accelerated adoption
        event_impact_opt[idx] = 0.045 * (yr - 2024)
        # Pessimistic Scenario: Infrastructure/operational delays
        event_impact_pess[idx] = 0.005 * (yr - 2024)

forecast_base = baseline_forecast + event_impact_base
forecast_opt  = baseline_forecast + event_impact_opt
forecast_pess = baseline_forecast + event_impact_pess

# Enforce a 100% mathematical ceiling
forecast_base = np.clip(forecast_base, 0, 1.0)
forecast_opt = np.clip(forecast_opt, 0, 1.0)
forecast_pess = np.clip(forecast_pess, 0, 1.0)

# Build the forecast table [cite: 282]
df_forecast = pd.DataFrame({
    'Year': years,
    'Pessimistic Scenario (%)': np.round(forecast_pess * 100, 2),
    'Base Scenario (%)': np.round(forecast_base * 100, 2),
    'Optimistic Scenario (%)': np.round(forecast_opt * 100, 2)
}).set_index('Year')

print(df_forecast.loc[2024:2027])