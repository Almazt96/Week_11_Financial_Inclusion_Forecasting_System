# Week_11_Financial_Inclusion_Forecasting_System
# Ethiopia Financial Inclusion Forecasting System (2025–2027)

This repository houses the end-to-end forecasting, analytical, and visualization system tracking **Ethiopia's digital financial transformation**. Developed for a stakeholder consortium comprising development finance institutions (DFIs), mobile money operators, and the National Bank of Ethiopia (NBE), the platform combines baseline trend models with time-decay event shock layers to predict access and usage trends.

---

## Repository Structure

The code and reports are organized according to the following directory structure:

```text
ethiopia-fi-forecast/
├── .github/workflows/
│   └── unittests.yml             # Automated CI pipeline configuration
├── data/
│   ├── raw/                      # Starter datasets
│   │   ├── ethiopia_fi_unified_data.csv
│   │   └── reference_codes.csv
│   └── processed/                # Unified, enriched, and clean forecast datasets
│       ├── ethiopia_fi_unified_data_enriched.csv
│       ├── impact_links_enriched.csv
│       └── financial_inclusion_forecasts_2025_2027.csv
├── notebooks/
│   ├── eda_analysis.ipynb        # Data profiling & historical visualization
│   ├── forecasting_analysis.ipynb# Multi-scenario predictive engines
│   └── impact_modeling.ipynb     # Exponential event-impact model tests
├── src/
│   ├── __init__.py
│   └── task1_exploration.py      # Schema parser & core extraction pipelines
├── dashboard/
│   └── app.py                    # Streamlit interactive application
├── tests/
│   ├── __init__.py
│   └── test_pipeline.py          # Unified testing pipeline script
├── reports/
│   ├── figures/                  # Visualization outputs (PNG format)
│   ├── data_enrichment_log.md    # Log file tracking injected proxies
│   ├── eda_key_insights.md       # Insights explaining the +3pp growth drag
│   ├── impact_modeling_methodology.md  # Structural math documentation
│   └── forecasting_interpretation.md   # Projections interpretation
├── requirements.txt              # Standard python dependencies
├── README.md                     # Main repository guide
└── .gitignore                    # Local storage exclusion rules

```

---

## Summary of Tasks & Architectural Components

### Task 1: Data Exploration and Enrichment

* **Objective:** Parse a unified tabular database schema containing **Observations**, **Events**, and **Targets**.
* **Relational Mapping:** Used `parent_id` foreign-key associations in `impact_links` to map qualitative national events to specific quantitative indicators.
* **Enriched Indicators:** Supplemented sparse 3-year Global Findex targets with high-frequency proxy metrics, logged in `reports/data_enrichment_log.md`:
* `INF_MOBILE_PEN`: Mobile Subscription Density (ITU / Ethio Telecom).
* `INF_4G_COV`: 4G Population Coverage Rate (%).
* `AG_DENSITY`: Mobile Money Agent Density (National Bank of Ethiopia).
* `EV_FAYDA_ROLL`: National Fayda Digital ID Integration.



---

### Task 2: Exploratory Data Analysis (EDA)

* **Objective:** Profile historical Findex trends (2011–2024) and isolate barriers to financial inclusion.
* **Key Findings:** Documented 5 strategic insights in `reports/eda_key_insights.md`:
1. **The +3pp Deceleration Paradox:** Why unique account ownership grew by only 3 percentage points (from 46% in 2021 to 49% in 2024) despite Telebirr scaling past 54M users and M-Pesa hitting 10M. This gap is driven by urban *multi-homing* (users holding multiple duplicate bank and digital wallet accounts).
2. **The P2P/ATM Crossover:** Peer-to-peer digital transfers surpassed physical cash ATM withdrawals for the first time, signaling a structural transition to digital money circulation.
3. **The Persistent Gender Gap:** Unique account ownership features a persistent 12-15 percentage point gap penalizing female adults.
4. **Infrastructure Correlation:** Localized 4G LTE network coverage shows a strong correlation with active mobile wallet usage ($r = 0.84$), making infrastructure expansion a key leading indicator.
5. **Low Credit Integration:** Transactional usage is deep, but core credit and insurance access remain below 3%.



---

### Task 3: Event Impact Modeling

* **Objective:** Quantify how policy, product, and infrastructure developments affect financial inclusion indicators over time.
* **Mathematical Decay:** Implemented an exponential growth-absorption curve to model delayed transmission effects:

$$I_i(t) = M_i \cdot \left(1 - e^{-\lambda_i \cdot \left(12 \cdot (t - t_i) - L_i\right)}\right)$$

* **Overlapping Shocks:** Combined overlapping event impacts using an asymptotic diminishing scaling model to keep projections realistically bounded below 100%:

$$Y(t) = Y_{\text{baseline}}(t) + \left(1 - Y_{\text{baseline}}(t)\right) \cdot \left(1 - \prod_{i} (1 - I_i(t))\right)$$

* **Validation:** Tested against historical data from the 2021 Telebirr launch (mobile money accounts rose from 4.7% in 2021 to 9.45% in 2024) to calibrate the impact decay factor ($\lambda_i$) and account for duplicate wallets.

---

### Task 4: Forecasting Access and Usage (2025–2027)

* **Objective:** Project **Account Ownership (Access)** and **Digital Payment Usage (Usage)** under different scenario pathways.
* **Forecasting Method:** Applied an **Event-Augmented Trend Regression Model**:

$$Y_t = \beta_0 + \beta_1 \cdot t + \sum_{i} I_i(t) + \epsilon_t$$

* **Generated Scenarios:**
* **Base Case Scenario:** Achieves **59.4%** unique account ownership by late 2026, putting Ethiopia on track to hit the NFIS-II **60% target** by early 2027.
* **Optimistic Scenario:** Assumes accelerated onboarding via Fayda Digital ID and expanded agent networks, pushing Access to **64.0%** by 2027.
* **Pessimistic Scenario:** Policy and connectivity bottlenecks flatten growth, leaving Access at **52.0%** by 2027.



---

### Task 5: Interactive Dashboard Development

* **Objective:** Build an interactive Streamlit application to help stakeholders explore historical data, inspect event impacts, and test forecasting scenarios.
* **Dashboard Features:**
* **Overview Page:** Key metric summary cards, the P2P/ATM crossover chart, and growth rate trends.
* **Historical Trends:** Multi-channel filters, date-range selectors, and mobile money adoption trends.
* **Inclusion Projections:** Scenario selection toggles, confidence intervals, and tracking against the 60% national target.
* **Data Export:** Integrated button to download forecast tables as CSV files.
* **Answers to Key Questions:** Structured explanations for the consortium's core questions.



---

## Setup & Running the Project Locally

Follow these steps to configure your environment and launch the project:

### 1. Installation & Environment Configuration

```bash
# Clone the repository
git clone https://github.com/username/ethiopia-fi-forecast.git
cd ethiopia-fi-forecast

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt

```

### 2. Running the Unified Test Suite

Verify that data transformations, mathematical decay models, and forecasting pipelines function correctly:

```bash
# Run tests with verbose outputs
python -m unittest -v tests/test_pipeline.py

```

### 3. Deploying the Interactive Dashboard

Launch the local Streamlit development server:

```bash
streamlit run dashboard/app.py

```

Open your web browser and navigate to the default port: `http://localhost:8501`.

---

## Continuous Integration Pipeline

The repository includes a GitHub Actions configuration file under `.github/workflows/unittests.yml`. This pipeline runs automated checks on every push or pull request to the `main` branch to verify code quality and mathematical consistency:

```yaml
name: Python Testing Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
    - name: Check out repository code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Execute Pipeline Unit Tests
      run: |
        python -m unittest discover -s tests -p "test_pipeline.py"

```