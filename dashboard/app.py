import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Ethiopia Financial Inclusion Forecast", layout="wide")

st.title("Ethiopia Financial Inclusion Forecasting System") # [cite: 4]
st.markdown("Developed for the Financial Inclusion Consortium (DFIs, Mobile Money Operators, NBE)") # [cite: 9]

# Sidebar Controls 
st.sidebar.header("Scenario Configuration")
scenario = st.sidebar.selectbox(
    "Select Forecasting Scenario",
    ["Base Case", "Optimistic (High Adoption)", "Pessimistic (Stagnant Growth)"] # [cite: 268]
)

# Simulated Historical and Forecast Data [cite: 26, 282]
years = np.array([2011, 2014, 2017, 2021, 2024, 2025, 2026, 2027]) # [cite: 17, 26]
historical_len = 5

# Set scenario vectors [cite: 268]
if scenario == "Base Case":
    access_values = [14, 22, 35, 46, 49, 52.5, 56.0, 59.5]
    usage_values = [5, 10, 18, 28, 35, 39.0, 43.5, 48.0] # [cite: 31]
elif scenario == "Optimistic (High Adoption)":
    access_values = [14, 22, 35, 46, 49, 54.0, 59.0, 64.0]
    usage_values = [5, 10, 18, 28, 35, 41.0, 48.0, 55.0] # [cite: 31]
else:
    access_values = [14, 22, 35, 46, 49, 50.0, 51.0, 52.0]
    usage_values = [5, 10, 18, 28, 35, 36.0, 37.5, 39.0] # [cite: 31]

# --- 1. Metric Summary Row [cite: 294] ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("2024 Account Ownership", "49.0%", "+3.0% (vs 2021)") # [cite: 13, 26]
col2.metric("2024 Digital Payments Usage", "35.0%", "+7.0% (vs 2021)") # [cite: 31]
col3.metric("P2P to ATM Cash Ratio", "1.24x", "Interoperable Crossover", help="P2P digital transfers now surpass physical ATM cash withdrawals.") #      [cite: 11, 295]
col4.metric("2027 Projected Access", f"{access_values[-1]}%", f"Scenario: {scenario.split()[0]}")

st.markdown("---") #     [cite: 307]

# --- 2. Interactive Time-Series Plots [cite: 298] ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Access: Account Ownership Projection (Findex)") #[cite: 19, 22]
    fig_access = go.Figure()
    # Historical
    fig_access.add_trace(go.Scatter(x=years[:historical_len], y=access_values[:historical_len], name="Historical", mode="lines+markers", line=dict(color="#2b5c8f", width=3)))
    # Forecast
    fig_access.add_trace(go.Scatter(x=years[historical_len-1:], y=access_values[historical_len-1:], name="Forecasted", mode="lines+markers", line=dict(color="#2b5c8f", dash="dash", width=3)))
    # Target Reference
    fig_access.add_trace(go.Scatter(x=[2027], y=[60], mode="markers", marker=dict(color="red", size=12), name="NFIS-II 60% Target")) #[cite: 46, 311]
    fig_access.update_layout(yaxis=dict(ticksuffix="%"), margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_access, use_container_width=True)

with col_right:
    st.subheader("Usage: Digital Payments Adoption Projection") #[cite: 20]
    fig_usage = go.Figure()
    # Historical
    fig_usage.add_trace(go.Scatter(x=years[:historical_len], y=usage_values[:historical_len], name="Historical", mode="lines+markers", line=dict(color="#117a65", width=3)))
    # Forecast
    fig_usage.add_trace(go.Scatter(x=years[historical_len-1:], y=usage_values[historical_len-1:], name="Forecasted", mode="lines+markers", line=dict(color="#117a65", dash="dash", width=3)))
    fig_usage.update_layout(yaxis=dict(ticksuffix="%"), margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_usage, use_container_width=True)

# --- 3. Dynamic Scenario Data & Export [cite: 308] ---
st.subheader(f"Detailed Projections: {scenario}")
df_display = pd.DataFrame({
    "Year": years,
    "Access (Account Ownership) %": access_values,
    "Usage (Digital Payments) %": usage_values
}).set_index("Year")

st.dataframe(df_display.loc[2024:])

# Data Download Option [cite: 308]
csv = df_display.to_csv().encode('utf-8')
st.download_button(
    label="📥 Download Projection Data (CSV)",
    data=csv,
    file_name=f"ethiopia_fi_projections_{scenario.lower().replace(' ', '_')}.csv",
    mime="text/csv"
)