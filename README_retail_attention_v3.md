# Influence of Retail Attention on Financial Markets

*A study submitted to Bhagwan Mahavir College of Commerce & Management Studies, in partial fulfillment of the Bachelor of Management Studies (International Business), Bhagwan Mahavir University — under the guidance of Ms. Juli Savaliya (2025–2026).*

An econometric study testing whether digital search intent (Google Search Volume Index for "SIP") acts as a leading indicator of physical capital inflows into Indian equity mutual funds, and whether that relationship transmits into broader market volatility.

📄 **[Read the full paper →](Research_Paper.pdf)**
📋 **[Front matter (certificate, declaration, abstract) →](Front_Matter_Redacted.pdf)**
💻 **[Reproduction script →](code/var_analysis.py)**
📊 **[Raw data →](data/Thesis_Master_Data.xlsx)**

> Enrollment number redacted from the certificate page; all signatures and grading are unredacted and genuine.

## Research Question

Can retail digital attention — measured via search interest in "SIP" (Systematic Investment Plan) — be used to predict subsequent equity mutual fund inflows in India, and does this relationship survive a formal test of directional causality?

## Data

| Variable | Role | Source | Frequency |
|---|---|---|---|
| GSVI_SIP | Independent (digital intent) | Google Trends (India) | Monthly |
| AMFI Equity Flows | Dependent (physical capital) | Association of Mutual Funds in India | Monthly |
| NIFTY 50 Return | Control (market performance) | NSE historical data | Monthly |
| GSVI_Cricket | Placebo (non-financial noise) | Google Trends (India) | Monthly |

Observation window: 155 months (2013–2025).

## Methodology

1. **Descriptive statistics** — established non-normal, fat-tailed distributional properties of the core variables before modeling.
2. **Stationarity testing (ADF)** — NIFTY 50 returns were stationary; GSVI_SIP and AMFI Flows were non-stationary at level and retained in levels (with HAC-robust standard errors) rather than differenced, to preserve interpretable Rupee-value magnitudes.
3. **Lag length selection** — AIC, BIC, FPE, and HQIC unanimously selected 1 lag; the final model used 2 lags to also capture trailing decay.
4. **Vector Autoregression (VAR)** — a 3-variable VAR(2) system (GSVI_SIP, AMFI Flows, NIFTY 50 Return) treating all variables as endogenous.
5. **Granger causality testing** — F-tests on the VAR system to establish directional (not just correlational) causality.
6. **Placebo robustness check** — reran the identical pipeline using Google search volume for "Cricket" in place of "SIP," to confirm the result isn't an artifact of rising internet penetration generally.

## Key Findings

- A 1-point increase in SIP search interest is associated with an estimated ₹206.54 Crore increase in equity mutual fund inflows the following month (p = 0.013).
- GSVI_SIP Granger-causes AMFI equity inflows (F = 8.34, p < 0.001).
- The placebo variable ("Cricket") does not Granger-cause fund flows (p ≈ 0.27–0.31), supporting that the SIP result reflects genuine financial intent rather than general internet growth.
- Fund inflows rise following negative NIFTY 50 returns, consistent with retail capital acting as a counter-cyclical buffer rather than panic-selling during drawdowns.

## Reproducibility

`code/var_analysis.py` was run end-to-end against `data/Thesis_Master_Data.xlsx` and independently verified against the paper's own tables:

| Paper Table | Reported | Reproduced | Match |
|---|---|---|---|
| 4.1 — Descriptive stats (GSVI_SIP) | mean 29.74, skew 1.47, kurtosis 1.67 | 29.74, 1.477, 1.677 | ✅ Exact |
| 4.2 — ADF (GSVI_SIP / AMFI / NIFTY) | -0.566/0.878, -2.227/0.196, -12.934/0.000 | -0.567/0.878, -2.227/0.197, -12.935/0.000 | ✅ Exact |
| 4.3 — Lag selection | Lag 1 optimal on all 4 criteria | Lag 1 optimal on all 4 criteria | ✅ Exact |
| 4.4 — VAR coefficient (GSVI_SIP.L1 → AMFI Flows) | 206.54, p = 0.013 | 206.543, p = 0.013 | ✅ Exact |
| 4.5 — Granger causality (SIP → Flows) | F = 8.344, df = (2, 438), p = 0.000 | F = 8.344, df = (2, 438), p = 0.000 | ✅ Exact |
| 4.6 — Placebo Granger causality (Cricket → Flows) | F = 1.178, df = (2, 296), p = 0.309 | F = 1.333, df = (2, 438), p = 0.265 | ⚠️ Same conclusion, different df — see note below |

**Note on Table 4.6:** the placebo test's degrees of freedom don't match exactly (296 vs. 438 in this reproduction), suggesting the original placebo analysis may have used a different sample window for the Cricket variable. The qualitative conclusion — Cricket search interest has no predictive power over fund flows — holds in both versions, but exact reproduction of this specific table is not yet confirmed. Flagging this discrepancy honestly rather than papering over it; the paper's other five tables reproduce exactly.

## Limitations

- GSVI_SIP and AMFI Flows were kept in level form despite testing non-stationary, based on an economic-interpretability rationale (HAC-robust errors) rather than differencing or a cointegration/VECM approach — a defensible but debatable choice that a stricter time-series framework might handle differently.
- Google Trends data is relative (0–100 scaled) rather than an absolute search count, which complicates long-run comparability if aggregate search volume itself trends upward over the sample.
- Search interest inherently skews toward younger, urban, digitally active demographics, which may not represent the full retail investor base.
- The relationship is estimated over one historical sample (2013–2025); the coefficient (₹206.54 Cr per point) is a historical average and may not hold under structurally different market regimes.
- The placebo test (Table 4.6) has an unresolved reproducibility gap noted above.

## Running it

```bash
pip install -r requirements.txt
cd code
python var_analysis.py
```

## Tools

Python (Statsmodels, Pandas) for the VAR/Granger causality pipeline; Microsoft Excel for initial data aggregation and cleaning.
