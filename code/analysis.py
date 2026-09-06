import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.stattools import durbin_watson
import warnings
warnings.filterwarnings('ignore')

# 1. DATA LOADING & CLEANING
print("--- 1. LOADING DATA ---")
df = pd.read_excel('Thesis_Master_Data.xlsx')
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
df_clean = df.dropna()

CORE_VARS = ['GSVI_SIP', 'AMFI_Equity_Flows_Cr', 'NIFTY_50_Return']

# 2. DESCRIPTIVE STATISTICS (Table 4.1)
print("\n--- 2. DESCRIPTIVE STATISTICS (Table 4.1) ---")
desc = df_clean[CORE_VARS].describe().T
desc['skew'] = df_clean[CORE_VARS].skew()
desc['kurtosis'] = df_clean[CORE_VARS].kurt()
print(desc)

# 3. STATIONARITY: AUGMENTED DICKEY-FULLER TEST (Table 4.2)
print("\n--- 3. ADF STATIONARITY TESTS (Table 4.2) ---")
adf_results = []
for col in CORE_VARS:
    stat, pval, *_ = adfuller(df_clean[col], regression='c', autolag='AIC')
    status = "Stationary" if pval < 0.05 else "Non-Stationary (Trended)"
    adf_results.append({"Variable": col, "ADF Statistic": stat, "p-value": pval, "Status": status})
adf_table = pd.DataFrame(adf_results)
print(adf_table.round(4))
# NOTE: your paper states GSVI_SIP and AMFI_Equity_Flows_Cr are retained in LEVELS
# despite non-stationarity (interpretability rationale). NIFTY_50_Return is already
# a log return and should test stationary. Compare the printed stats/p-values above
# against Table 4.2 (-0.566/0.878 for SIP, -2.227/0.196 for AMFI, -12.934/0.000 for NIFTY).
# If regression='c' doesn't match, your original test likely used regression='ct' (with trend) —
# try that if these numbers don't line up.

# 4. OPTIMAL LAG LENGTH SELECTION (Table 4.3)
print("\n--- 4. VAR LAG ORDER SELECTION (Table 4.3) ---")
model = VAR(df_clean[CORE_VARS])
lag_selection = model.select_order(maxlags=6)
print(lag_selection.summary())
# Your paper reports all four criteria (AIC, BIC, FPE, HQIC) selecting lag 1,
# with the final model conservatively run at lag 2. Confirm that holds here.

# 5. VAR(2) MODEL ESTIMATION (Table 4.4)
print("\n--- 5. VAR(2) MODEL: FULL COEFFICIENT OUTPUT (Table 4.4) ---")
results = model.fit(2)
print(results.summary())
print(f"\nModel is Stable: {results.is_stable()}")
# Cross-check the AMFI_Equity_Flows_Cr equation's GSVI_SIP.L1 coefficient
# against your reported 206.54 (p=0.013).

# 6. GRANGER CAUSALITY: DOES SIP SEARCH INTEREST CAUSE FUND FLOWS? (Table 4.5)
print("\n--- 6. GRANGER CAUSALITY: GSVI_SIP -> AMFI FLOWS (Table 4.5) ---")
g_test = results.test_causality('AMFI_Equity_Flows_Cr', ['GSVI_SIP'], kind='f')
print(g_test.summary())
print(f"F-statistic: {g_test.test_statistic:.3f}, p-value: {g_test.pvalue:.4f}")
# Compare against your reported F=8.344, df=(2,438), p=0.000.

# 7. IMPULSE RESPONSE FUNCTION (Figure 4.1)
print("\n--- 7. IMPULSE RESPONSE FUNCTIONS ---")
irf = results.irf(12)
irf.plot(orth=True, figsize=(10, 8))
plt.suptitle("Orthogonalized Impulse Response of AMFI Flows to GSVI_SIP Shock")
plt.tight_layout()
plt.show()

# 8. PLACEBO ROBUSTNESS CHECK: CRICKET (Table 4.6)
print("\n--- 8. PLACEBO TEST: GSVI_CRICKET -> AMFI FLOWS (Table 4.6) ---")
placebo_vars = ['GSVI_Cricket', 'AMFI_Equity_Flows_Cr', 'NIFTY_50_Return']
placebo_model = VAR(df_clean[placebo_vars])
placebo_results = placebo_model.fit(2)
placebo_test = placebo_results.test_causality('AMFI_Equity_Flows_Cr', ['GSVI_Cricket'], kind='f')
print(placebo_test.summary())
print(f"F-statistic: {placebo_test.test_statistic:.3f}, p-value: {placebo_test.pvalue:.4f}")
# Compare against your reported F=1.178, df=(2,296), p=0.309 (Fail to Reject H0).

# 9. ROLLING CORRELATION (Figure 4.2)
print("\n--- 9. ROLLING CORRELATION: MARKET MATURITY ---")
plt.figure(figsize=(12, 4))
rolling_corr = df_clean['GSVI_SIP'].rolling(window=12).corr(df_clean['AMFI_Equity_Flows_Cr'])
plt.plot(rolling_corr, color='#2E86C1', label='12M Rolling Corr (SIP vs Flows)')
plt.axhline(rolling_corr.mean(), color='red', linestyle='--', label='Average')
plt.title('Dynamic 12-Month Rolling Correlation (SIP vs Flows)')
plt.legend()
plt.show()

# 10. RESIDUAL DIAGNOSTICS: DURBIN-WATSON
print("\n--- 10. RESIDUAL AUTOCORRELATION CHECK (Durbin-Watson) ---")
dw_stats = durbin_watson(results.resid)
for col, dw in zip(CORE_VARS, dw_stats):
    print(f"{col}: DW = {dw:.3f}  (~2.0 = no autocorrelation)")
