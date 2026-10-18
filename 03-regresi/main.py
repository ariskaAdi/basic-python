"""
Analisis Regresi Linear Berganda
Y  = Persentase penduduk miskin (%)
X1 = Tingkat Pengangguran Terbuka (%)
X2 = PDRB per kapita (juta rupiah)
Unit observasi: 38 provinsi di Indonesia
"""

import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan, linear_reset
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson

ALPHA = 0.05


def garis(judul):
    print("\n" + "=" * 60)
    print(judul)
    print("=" * 60)


def keputusan(p_value):
    return "Tolak H0" if p_value < ALPHA else "Gagal tolak H0"


# ---------------------------------------------------------------
# 1. Baca data
# ---------------------------------------------------------------
df = pd.read_excel("data_regresi_38_provinsi.xlsx")
y = df["Y_Kemiskinan"]
X = df[["X1_Pengangguran", "X2_PDRB_Per_Kapita"]]

garis("1. STATISTIK DESKRIPTIF")
print(df.describe().round(2))

# ---------------------------------------------------------------
# 2. Estimasi model: Y = b0 + b1*X1 + b2*X2 + e  (metode OLS)
# ---------------------------------------------------------------
X_const = sm.add_constant(X)
model = sm.OLS(y, X_const).fit()

garis("2. RINGKASAN MODEL OLS")
print(model.summary())

b = model.params
garis("3. TAKSIRAN PERSAMAAN REGRESI")
print(
    f"Y_hat = {b['const']:.4f} "
    f"{b['X1_Pengangguran']:+.4f} X1 "
    f"{b['X2_PDRB_Per_Kapita']:+.4f} X2"
)
print(f"R-squared          = {model.rsquared:.4f}")
print(f"Adjusted R-squared = {model.rsquared_adj:.4f}")

# ---------------------------------------------------------------
# 3. Uji simultan (uji F)
#    H0: b1 = b2 = 0   vs   H1: minimal satu bj != 0
# ---------------------------------------------------------------
garis("4. UJI SIMULTAN (UJI F)")
f_tabel = stats.f.ppf(1 - ALPHA, model.df_model, model.df_resid)
print(f"F hitung = {model.fvalue:.4f}, F tabel = {f_tabel:.4f}")
print(f"p-value  = {model.f_pvalue:.4f} -> {keputusan(model.f_pvalue)}")

# ---------------------------------------------------------------
# 4. Uji parsial (uji t)
#    H0: bj = 0   vs   H1: bj != 0
# ---------------------------------------------------------------
garis("5. UJI PARSIAL (UJI t)")
t_tabel = stats.t.ppf(1 - ALPHA / 2, model.df_resid)
print(f"t tabel (alpha={ALPHA}, df={int(model.df_resid)}) = {t_tabel:.4f}")
for nama in model.params.index:
    t, p = model.tvalues[nama], model.pvalues[nama]
    print(f"{nama:20s} t = {t:8.4f}  p = {p:.4f}  -> {keputusan(p)}")

# ---------------------------------------------------------------
# 5. Uji asumsi klasik
# ---------------------------------------------------------------
residual = model.resid
garis("6. UJI ASUMSI KLASIK")

# a. Normalitas residual  (H0: residual berdistribusi normal)
sw_stat, sw_p = stats.shapiro(residual)
print(f"[Normalitas] Shapiro-Wilk  W = {sw_stat:.4f}, p = {sw_p:.4f} -> {keputusan(sw_p)}")
ks_stat, ks_p = stats.kstest(
    (residual - residual.mean()) / residual.std(ddof=1), "norm"
)
print(f"[Normalitas] Kolmogorov-S  D = {ks_stat:.4f}, p = {ks_p:.4f} -> {keputusan(ks_p)}")

# b. Homoskedastisitas  (H0: varians residual konstan)
bp_lm, bp_p, _, _ = het_breuschpagan(residual, X_const)
print(f"[Heteroskedastisitas] Breusch-Pagan LM = {bp_lm:.4f}, p = {bp_p:.4f} -> {keputusan(bp_p)}")

# c. Non-multikolinearitas  (VIF > 10 -> ada multikolinearitas)
print("[Multikolinearitas] VIF:")
for i, nama in enumerate(X_const.columns):
    if nama != "const":
        print(f"    {nama:20s} VIF = {variance_inflation_factor(X_const.values, i):.4f}")

# d. Non-autokorelasi  (DW mendekati 2 -> tidak ada autokorelasi)
dw = durbin_watson(residual)
print(f"[Autokorelasi] Durbin-Watson = {dw:.4f}")
print("    (catatan: data cross-section, autokorelasi biasanya bukan masalah utama)")

# e. Linearitas  (H0: bentuk fungsi linear sudah tepat)
reset = linear_reset(model, power=2, use_f=True)
print(f"[Linearitas] Ramsey RESET F = {reset.fvalue:.4f}, p = {reset.pvalue:.4f} -> {keputusan(reset.pvalue)}")

# ---------------------------------------------------------------
# 6. Grafik diagnostik (disimpan untuk laporan)
# ---------------------------------------------------------------
fig, ax = plt.subplots(1, 3, figsize=(15, 4.5))

ax[0].scatter(model.fittedvalues, residual)
ax[0].axhline(0, color="red", linestyle="--")
ax[0].set_title("Residual vs Fitted")
ax[0].set_xlabel("Nilai prediksi")
ax[0].set_ylabel("Residual")

sm.qqplot(residual, line="s", ax=ax[1])
ax[1].set_title("Normal Q-Q Plot Residual")

ax[2].hist(residual, bins=10, edgecolor="black")
ax[2].set_title("Histogram Residual")

plt.tight_layout()
plt.savefig("grafik_diagnostik.png", dpi=150)
print("\nGrafik disimpan ke grafik_diagnostik.png")
