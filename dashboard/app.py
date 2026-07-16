import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Ethiopia Financial Inclusion Forecasting System",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------------
# MOCK DATA GENERATORS (Enabling self-contained deployment)
# -------------------------------------------------------------------------
@st.cache_data
def load_historical_data():
    # Core Findex and administrative historical observations
    years = [2011, 2014, 2017, 2021, 2024]
    data = {
        "Year": years,
        "Account_Ownership": [0.14, 0.22, 0.35, 0.46, 0.49],
        "Digital_Payments": [0.02, 0.05, 0.12, 0.28, 0.35],
        "Mobile_Money_Share": [0.00, 0.01, 0.04, 0.07, 0.0945],
        "ATM_Withdrawals_Billions": [5.0, 12.0, 35.0, 85.0, 120.0],
        "P2P_Transfers_Billions": [0.1, 1.5, 10.0, 72.0, 168.0] # Showing crossover
    }
    return pd.DataFrame(data)

@st.cache_data
def get_forecast_scenarios():
    # Forecast years
    years = [2024, 2025, 2026, 2027]
    
    # Access Projections (Account Ownership)
    access_data = {
        "Year": years,
        "Base": [0.49, 0.542, 0.594, 0.646],
        "Base_Lower": [0.49, 0.495, 0.547, 0.599],
        "Base_Upper": [0.49, 0.589, 0.641, 0.693],
        "Optimistic": [0.49, 0.572, 0.644, 0.716],
        "Pessimistic": [0.49, 0.512, 0.534, 0.556]
    }
    
    # Usage Projections (Digital Payments)
    usage_data = {
        "Year": years,
        "Base": [0.35, 0.404, 0.458, 0.512],
        "Base_Lower": [0.35, 0.348, 0.402, 0.456],
        "Base_Upper": [0.35, 0.460, 0.514, 0.568],
        "Optimistic": [0.35, 0.454, 0.538, 0.622],
        "Pessimistic": [0.35, 0.364, 0.378, 0.392]
    }
    return pd.DataFrame(access_data), pd.DataFrame(usage_data)

# Load data
df_hist = load_historical_data()
df_forecast_access, df_forecast_usage = get_forecast_scenarios()

# -------------------------------------------------------------------------
# SIDEBAR CONTROLS
# -------------------------------------------------------------------------
st.sidebar.title("Configuration & Parameters")
st.sidebar.markdown("Configure scenario conditions and models for downstream projections.")

# App Navigation
page = st.sidebar.radio(
    "Select Dashboard Section",
    ["Overview Page", "Historical Trends", "Inclusion Projections"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Global Scenario Settings")
scenario_sel = st.sidebar.selectbox(
    "Forecasting Scenario",
    ["Base Scenario", "Optimistic Pathway", "Pessimistic Pathway"]
)

model_sel = st.sidebar.selectbox(
    "Core Regression Model",
    ["Event-Augmented Regression", "Standard Trend continuation"]
)

st.sidebar.info(
    "**System Status:** Running locally.\n\n"
    "Data Source: World Bank Findex & Administrative Reports (NBE, EthSwitch)."
)

# -------------------------------------------------------------------------
# 1. OVERVIEW PAGE
# -------------------------------------------------------------------------
if page == "Overview Page":
    st.title("🇪🇹 Ethiopia Financial Inclusion Dashboard")
    st.markdown(
        "Welcome to the forecasting platform developed by **Selam Analytics**. "
        "This tool supports development finance institutions, mobile operators, "
        "and the National Bank of Ethiopia in tracking and projecting digital financial transformation."
    )
    
    # Metric Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Account Ownership (2024)", "49.0%", "+3.0 pp vs 2021")
    with col2:
        st.metric("Digital Payments (2024)", "35.0%", "+7.0 pp vs 2021")
    with col3:
        # Latest crossover ratio calculation
        latest_atm = df_hist["ATM_Withdrawals_Billions"].iloc[-1]
        latest_p2p = df_hist["P2P_Transfers_Billions"].iloc[-1]
        ratio = latest_p2p / latest_atm
        st.metric("P2P/ATM Crossover Ratio", f"{ratio:.2f}x", "P2P Transfers > ATM")
    with col4:
        st.metric("Telebirr Active Users", "54.0M", "Launched May 2021")

    st.markdown("---")
    
    # Main grid split
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("The Historic P2P vs. ATM Crossover")
        st.markdown(
            "For the first time in Ethiopia's history, interoperable digital Peer-to-Peer (P2P) transfers "
            "have bypassed physical cash withdrawals at ATMs. This marks a critical transition "
            "from a cash-out economy to digital payment circulation."
        )
        
        # Interactive Plotly Crossover Chart (Visualization #1)
        fig_cross = go.Figure()
        fig_cross.add_trace(go.Scatter(x=df_hist["Year"], y=df_hist["ATM_Withdrawals_Billions"], name="ATM Cash Withdrawals (Bn ETB)", line=dict(color="#FF4B4B", width=3)))
        fig_cross.add_trace(go.Scatter(x=df_hist["Year"], y=df_hist["P2P_Transfers_Billions"], name="P2P Digital Transfers (Bn ETB)", line=dict(color="#00CC96", width=3)))
        fig_cross.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=40, b=40),
            yaxis_title="Volume (Billions of ETB)"
        )
        st.plotly_chart(fig_cross, use_container_width=True)

    with col_right:
        st.subheader("Historical Growth Rates (Access vs. Usage)")
        st.markdown(
            "While transaction volumes have scaled rapidly, unique demand-side account growth "
            "has slowed (+3 percentage points between 2021 and 2024). This divergence highlights "
            "the challenge of multi-homing among already-banked individuals."
        )
        
        # Periodic Rate Calculations Bar Chart (Visualization #2)
        periods = ["2011-2014", "2014-2017", "2017-2021", "2021-2024"]
        growth_rates = [8.0, 13.0, 11.0, 3.0]
        
        fig_bar = px.bar(
            x=periods, y=growth_rates,
            labels={'x': 'Findex Survey Interval', 'y': 'Inclusion Growth Rate (percentage points)'},
            color=growth_rates,
            color_continuous_scale="Viridis"
        )
        fig_bar.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_bar, use_container_width=True)

# -------------------------------------------------------------------------
# 2. HISTORICAL TRENDS PAGE
# -------------------------------------------------------------------------
elif page == "Historical Trends":
    st.title("📊 Historical Deep Dive & Channel Comparison")
    st.markdown("Explore indicators across different transaction channels and timeframes.")

    # Date / Year Multi-selector slider
    year_range = st.slider("Select Coverage Range", 2011, 2024, (2011, 2024))
    df_filtered = df_hist[(df_hist["Year"] >= year_range[0]) & (df_hist["Year"] <= year_range[1])]

    # Column split for interactive analytics
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Global Findex Framework Growth Track")
        
        # Trajectory Visualization (Visualization #3)
        fig_traj = go.Figure()
        fig_traj.add_trace(go.Scatter(x=df_filtered["Year"], y=df_filtered["Account_Ownership"] * 100, name="Account Ownership (Access)", marker=dict(size=10), line=dict(width=2.5)))
        fig_traj.add_trace(go.Scatter(x=df_filtered["Year"], y=df_filtered["Digital_Payments"] * 100, name="Digital Payments Adoption (Usage)", marker=dict(size=10), line=dict(width=2.5)))
        fig_traj.update_layout(
            yaxis_title="Percent of Adult Population (%)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_traj, use_container_width=True)

    with col_right:
        st.subheader("Mobile Money's Share of Inclusions")
        st.markdown(
            "Despite high overall wallet registrations, unique, active mobile money-only users "
            "represent a smaller share of the population (~9.45% in 2024), illustrating "
            "that banking services remain a primary entry point for inclusion."
        )
        
        # Interactive Bar/Area breakdown (Visualization #4)
        fig_mm = px.area(
            df_filtered, x="Year", y="Mobile_Money_Share",
            labels={"Mobile_Money_Share": "Mobile Money Penetration (%)"},
            title="Mobile Money Account Penetration Rate"
        )
        st.plotly_chart(fig_mm, use_container_width=True)

# -------------------------------------------------------------------------
# 3. INCLUSION PROJECTIONS PAGE
# -------------------------------------------------------------------------
elif page == "Inclusion Projections":
    st.title("🔮 Scenario Forecasts (2025–2027)")
    st.markdown(
        "Model forecasts based on macroeconomic trends and event shocks. "
        "Adjust scenarios in the sidebar to test policy impacts on national targets."
    )
    
    # Map selection sidebar values
    scenario_key = "Base" if "Base" in scenario_sel else ("Optimistic" if "Optimistic" in scenario_sel else "Pessimistic")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Account Ownership Rate (Access) Forecast")
        
        # Scenario projection with confidence intervals (Visualization #5)
        fig_fore_acc = go.Figure()
        # History
        fig_fore_acc.add_trace(go.Scatter(x=df_hist["Year"], y=df_hist["Account_Ownership"] * 100, name="Historical", mode="lines+markers", line=dict(color="black", width=3)))
        
        # Scenario line
        proj_years = df_forecast_access["Year"]
        proj_vals = df_forecast_access[scenario_key] * 100
        fig_fore_acc.add_trace(go.Scatter(x=proj_years, y=proj_vals, name=f"Forecast ({scenario_key})", line=dict(dash="dash", width=2.5)))
        
        # If Base is chosen, add the 95% shaded Prediction Limits
        if scenario_key == "Base":
            fig_fore_acc.add_trace(go.Scatter(
                x=np.concatenate([proj_years, proj_years[::-1]]),
                y=np.concatenate([df_forecast_access["Base_Upper"] * 100, (df_forecast_access["Base_Lower"] * 100)[::-1]]),
                fill='toself',
                fillcolor='rgba(0,100,250,0.15)',
                line=dict(color='rgba(255,255,255,0)'),
                hoverinfo="skip",
                name="95% Confidence Interval"
            ))
            
        # Target Line at 60% (National Financial Inclusion Strategy II)
        fig_fore_acc.add_hline(y=60.0, line_dash="dot", line_color="red", annotation_text="NFIS-II 60% Target")
        
        fig_fore_acc.update_layout(yaxis_title="Percent (%)", legend=dict(orientation="h", y=1.02))
        st.plotly_chart(fig_fore_acc, use_container_width=True)

    with col_right:
        st.subheader("Digital Payment Adoption (Usage) Forecast")
        
        # Usage Scenario projections (Visualization #6)
        fig_fore_usg = go.Figure()
        fig_fore_usg.add_trace(go.Scatter(x=df_hist["Year"], y=df_hist["Digital_Payments"] * 100, name="Historical", mode="lines+markers", line=dict(color="black", width=3)))
        
        proj_vals_usg = df_forecast_usage[scenario_key] * 100
        fig_fore_usg.add_trace(go.Scatter(x=proj_years, y=proj_vals_usg, name=f"Forecast ({scenario_key})", line=dict(dash="dash", width=2.5)))
        
        if scenario_key == "Base":
            fig_fore_usg.add_trace(go.Scatter(
                x=np.concatenate([proj_years, proj_years[::-1]]),
                y=np.concatenate([df_forecast_usage["Base_Upper"] * 100, (df_forecast_usage["Base_Lower"] * 100)[::-1]]),
                fill='toself',
                fillcolor='rgba(0,100,250,0.15)',
                line=dict(color='rgba(255,255,255,0)'),
                hoverinfo="skip",
                name="95% Confidence Interval"
            ))
            
        fig_fore_usg.update_layout(yaxis_title="Percent (%)", legend=dict(orientation="h", y=1.02))
        st.plotly_chart(fig_fore_usg, use_container_width=True)

    st.markdown("---")
    st.subheader("📥 Export & Download Center")
    
    # Data download block
    df_export = pd.DataFrame({
        "Year": [2025, 2026, 2027],
        "Access_Base_Forecast": df_forecast_access["Base"].iloc[1:].values * 100,
        "Access_Base_Lower_CI": df_forecast_access["Base_Lower"].iloc[1:].values * 100,
        "Access_Base_Upper_CI": df_forecast_access["Base_Upper"].iloc[1:].values * 100,
        "Usage_Base_Forecast": df_forecast_usage["Base"].iloc[1:].values * 100,
    })
    
    csv_data = df_export.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Forecast Output Table (CSV)",
        data=csv_data,
        file_name="ethiopia_financial_inclusion_projections.csv",
        mime="text/csv"
    )

    st.markdown("---")
    st.subheader("💬 Executive Answers to Key Stakeholder Questions")
    
    with st.expander("Q1: What is driving Ethiopia's rapid financial inclusion trajectory?"):
        st.markdown(
            "**Answer:** The primary driver is digital payment ecosystem expansion—specifically "
            "high-frequency utility payments and peer-to-peer transfers. Mobile network expansion "
            "and competitive pressure from entry of private operators like Safaricom/M-Pesa "
            "have significantly reduced transactional friction."
        )
        
    with st.expander("Q2: Why did unique account ownership grow only 3 percentage points (2021–2024) despite millions of new wallets?"):
        st.markdown(
            "**Answer:** This divergence is driven by *multi-homing*. Already-banked urban consumers "
            "frequently open multiple digital accounts (e.g., holding both a bank account and a "
            "telebirr wallet), inflating total registrations without adding new, historically "
            "unbanked populations to the formal system."
        )