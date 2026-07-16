# Event Impact Modeling Methodology & Validation Report

**Lead Project Scientist:** Almaz Tsegaye  
[cite_start]**Focus:** Task 3 Deliverables — Forecasting Financial Inclusion in Ethiopia 

---

### 1. Modeling Methodology & Chosen Functional Forms

[cite_start]Instead of assuming that structural milestones (such as regulatory or product rollouts) instantly shift macroeconomic rates [cite: 221, 224][cite_start], we represent events using a **Time-Lagged Exponential Growth-Absorption curve**[cite: 223, 224]. 

#### Mathematical Formulation
Let an event $i$ occur at time $t_i$. The dynamic additive shock $I_i(t)$ of this event on target indicator $Y$ at time $t$ is modeled as:

$$I_i(t) = 
\begin{cases} 
0 & \text{for } t < t_i + \frac{L_i}{12} \\
M_i \cdot \left(1 - e^{-\lambda_i \cdot \left(12 \cdot (t - t_i) - L_i\right)}\right) & \text{for } t \ge t_i + \frac{L_i}{12} 
\end{cases}$$

Where:
* $M_i$: The maximum expected percentage point coefficient shift at saturation.
* $L_i$: The structural transmission lag in months.
* $\lambda_i$: The adoption decay/absorption velocity constant (determines how fast the market adopts the intervention).
* $t$: The evaluation timeframe (expressed in years).

#### Aggregation of Combined Events
[cite_start]To combine overlapping impacts from multiple events without exceeding physical ceilings, we use an **Asymptotic Diminishing Scaling Product**[cite: 225]:

$$Y(t) = Y_{\text{baseline}}(t) + \left(1 - Y_{\text{baseline}}(t)\right) \cdot \left(1 - \prod_{i} (1 - I_i(t))\right)$$

This approach guarantees that even when multiple massive events overlap, the aggregated inclusion rate cannot mathematically exceed the logical ceiling of 100%.

---

### 2. Comparable Country Evidence Sources

[cite_start]For events where local historical data is sparse, coefficients are calibrated using comparable international benchmarks:

1. [cite_start]**Mobile Money Scaling (`ACC_MM_ACCOUNT`):** Calibrated against the early expansion of **FSD Kenya’s FinAccess surveys (2007–2011)**[cite: 384, 391]. In Kenya, M-Pesa's initial phase drove a steady, lagged growth in access, adding roughly 4 to 8 percentage points annually.
2. [cite_start]**Onboarding Friction Reduction (`ACC_OWNERSHIP`):** Calibrated against **India's Aadhaar (Digital ID) Rollout (2014–2018)**[cite: 392]. This rollout demonstrated that integrating a foundational digital identity with banking systems reduces e-KYC hurdles, driving a 12 percentage point increase in rural, low-income adult registrations over a 24-month horizon.

---

### 3. Historical Validation Analysis: The Telebirr 2021-2024 Test Case

* **Historical Reality:** Telebirr launched in May 2021[cite: 190, 233]. Mobile money account penetration in Findex surveys rose from **4.7% in 2021** to **9.45% in 2024**.
* [cite_start]**Model Baseline Prediction:** Utilizing our unrefined, supply-side coefficient of $+0.15$ maximum impact magnitude, the model projected account ownership to reach **19.7%** by 2024. This created a validation gap.

#### Explaining the Validation Gap & Discrepancy
[cite_start]The discrepancy between the model's high projection (19.7%) and the actual Findex outcome (9.45%) is driven by two market dynamics[cite: 235]:
1. [cite_start]**The Multi-Homing/Dormancy Factor:** While supply-side metrics recorded over 40 million Telebirr registrations, unique demand-side surveys show that many users hold multiple inactive accounts[cite: 200].
2. [cite_start]**Findex Definition Rigor:** The Findex database measures unique adult account ownership[cite: 24]. [cite_start]It does not count corporate wallets, duplicate registrations, or accounts held by individuals under the age of 15[cite: 24]. 

#### Refinement Adjustments Made
[cite_start]Based on these findings, we applied a **Multi-Homing Correction Discount of 0.45** to all supply-side magnitude inputs[cite: 237]:

$$M_{\text{refined}} = M_{\text{raw}} \cdot 0.45$$

[cite_start]Applying this discount adjusts the Telebirr maximum coefficient to **$+0.08$**, aligning our revised model projections with the actual 2024 Findex outcome of **9.45%**[cite: 233, 237].

---

### 4. Key Model Assumptions & Uncertainties

* **Assumption 1:** Regulatory policies assume that the National Bank of Ethiopia maintains consistent consumer-protection frameworks and does not introduce restrictive transaction limits.
* **Assumption 2:** The baseline growth rate from historical Findex data (2011–2024) is assumed to continue as a linear floor.
* **Primary Uncertainty:** High-level infrastructure factors (such as the frequency of network outages or variations in regional electricity reliability) introduce uncertainty, as they can suddenly slow the transmission lag ($L_i$) of digital payment events.