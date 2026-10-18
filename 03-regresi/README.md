# Analisis Regresi Linear Berganda — 38 Provinsi Indonesia

Proyek ini menganalisis pengaruh **tingkat pengangguran** dan **PDRB per kapita** terhadap **persentase penduduk miskin** di 38 provinsi Indonesia menggunakan regresi linear berganda (metode *Ordinary Least Squares* / OLS) dengan Python.

---

## 1. Data

**Sumber data:** Badan Pusat Statistik (BPS) —
<https://www.bps.go.id/id/statistics-table/2/NDU1IzI=/angkaharapan-hidup--ahh--menurut-kabupaten-kota-dan-jenis-kelamin.html>

File: `data_regresi_38_provinsi.xlsx` (1 sheet, 38 baris, 4 kolom)

| Kolom | Simbol | Keterangan | Satuan |
|---|---|---|---|
| `Provinsi` | – | Nama provinsi (unit observasi) | – |
| `Y_Kemiskinan` | Y | Persentase penduduk miskin (variabel terikat) | % |
| `X1_Pengangguran` | X1 | Tingkat Pengangguran Terbuka (variabel bebas) | % |
| `X2_PDRB_Per_Kapita` | X2 | PDRB per kapita (variabel bebas) | juta rupiah |

Model yang diestimasi:

```
Y = β0 + β1·X1 + β2·X2 + ε
```

---

## 2. Cara Menjalankan

Proyek ini memakai [uv](https://docs.astral.sh/uv/) untuk mengelola Python dan library.

```powershell
# 1. Pasang uv (sekali saja), jika belum ada
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. Masuk ke folder proyek
cd 03-regresi

# 3. Pasang semua library sesuai pyproject.toml / uv.lock
uv sync

# 4. Jalankan analisis
uv run python main.py
```

Hasil:
- Semua angka (ringkasan model, uji F, uji t, uji asumsi) tampil di terminal.
- Grafik diagnostik residual disimpan ke `grafik_diagnostik.png`.

> Tanpa uv: buat virtual environment biasa lalu
> `pip install pandas openpyxl statsmodels scipy matplotlib`, kemudian `python main.py`.

---

## 3. Library yang Dibutuhkan dan Alasannya

| Library | Dipakai untuk | Kenapa library ini |
|---|---|---|
| **pandas** | Membaca Excel, menyimpan data dalam bentuk tabel (`DataFrame`), statistik deskriptif | Standar de-facto untuk mengolah data tabel di Python; kolom bisa dipanggil dengan nama (`df["Y_Kemiskinan"]`) sehingga kode mudah dibaca |
| **openpyxl** | "Mesin" pembaca file `.xlsx` | pandas tidak bisa membuka file Excel sendiri — `pd.read_excel()` memanggil openpyxl di belakang layar. Tidak di-`import` langsung di kode, tapi wajib terpasang |
| **statsmodels** | Estimasi model OLS, uji F, uji t, R², VIF, Breusch-Pagan, Durbin-Watson, Ramsey RESET, Q-Q plot | Library khusus **statistika/ekonometrika**. Outputnya (`model.summary()`) mirip SPSS/EViews: lengkap dengan koefisien, standard error, t, p-value. Berbeda dengan scikit-learn yang fokus ke prediksi dan **tidak** menyediakan uji hipotesis |
| **scipy** | Uji normalitas (Shapiro-Wilk, Kolmogorov-Smirnov), mencari nilai **F tabel** dan **t tabel** | `scipy.stats` berisi distribusi peluang dan uji statistik dasar; dipakai agar kita tidak perlu membuka tabel F/t manual |
| **matplotlib** | Membuat grafik residual (scatter, Q-Q plot, histogram) | Library grafik paling umum di Python, dan statsmodels juga menggambar Q-Q plot memakai matplotlib |

### Fungsi yang diimpor secara spesifik

```python
import statsmodels.api as sm                                              # OLS, add_constant, qqplot
from statsmodels.stats.diagnostic import het_breuschpagan, linear_reset   # uji heteroskedastisitas & linearitas
from statsmodels.stats.outliers_influence import variance_inflation_factor # uji multikolinearitas (VIF)
from statsmodels.stats.stattools import durbin_watson                      # uji autokorelasi
import scipy.stats as stats                                               # shapiro, kstest, f.ppf, t.ppf
```

---

## 4. Cara Membaca Kode `main.py`

Kode dibaca dari atas ke bawah, dibagi menjadi 6 bagian yang ditandai komentar `# ----`.

### Bagian awal: konstanta dan fungsi bantu

```python
ALPHA = 0.05
```
Tingkat signifikansi 5%. Semua uji memakai nilai ini.

```python
def garis(judul): ...      # hanya mencetak judul bagian agar output rapi
def keputusan(p_value):    # aturan keputusan uji hipotesis
    return "Tolak H0" if p_value < ALPHA else "Gagal tolak H0"
```
Aturan umum: **jika p-value < 0,05 → tolak H0**.

### Bagian 1 — Baca data

```python
df = pd.read_excel("data_regresi_38_provinsi.xlsx")
y = df["Y_Kemiskinan"]                                  # variabel terikat
X = df[["X1_Pengangguran", "X2_PDRB_Per_Kapita"]]       # variabel bebas (2 kolom)
print(df.describe())
```
`describe()` menampilkan count, mean, std, min, kuartil, dan max tiap variabel → dipakai untuk bagian *Data dan Variabel* di laporan.

### Bagian 2 — Estimasi model OLS

```python
X_const = sm.add_constant(X)        # tambah kolom berisi angka 1 untuk intersep β0
model = sm.OLS(y, X_const).fit()    # hitung koefisien dengan metode kuadrat terkecil
print(model.summary())
```
`add_constant` **wajib**: tanpa itu statsmodels membuat model tanpa intersep (garis dipaksa lewat titik nol).

Objek `model` menyimpan semua hasil, antara lain:

| Atribut | Isi |
|---|---|
| `model.params` | koefisien β0, β1, β2 |
| `model.rsquared`, `model.rsquared_adj` | R² dan Adjusted R² |
| `model.fvalue`, `model.f_pvalue` | statistik F dan p-value-nya |
| `model.tvalues`, `model.pvalues` | statistik t dan p-value tiap koefisien |
| `model.resid` | residual (ε = Y − Ŷ) |
| `model.fittedvalues` | nilai prediksi Ŷ |
| `model.df_model`, `model.df_resid` | derajat bebas (k = 2 dan n − k − 1 = 35) |

Kemudian persamaan regresi dicetak dalam bentuk `Y_hat = b0 + b1 X1 + b2 X2`.

### Bagian 3 — Uji simultan (uji F)

- H0: β1 = β2 = 0 (X1 dan X2 bersama-sama tidak berpengaruh)
- H1: minimal satu βj ≠ 0

```python
f_tabel = stats.f.ppf(1 - ALPHA, model.df_model, model.df_resid)
```
`f.ppf` = kebalikan fungsi distribusi F, yaitu nilai **F tabel**. Tolak H0 jika F hitung > F tabel (setara dengan p-value < 0,05).

### Bagian 4 — Uji parsial (uji t)

- H0: βj = 0 (variabel Xj tidak berpengaruh)
- H1: βj ≠ 0

```python
t_tabel = stats.t.ppf(1 - ALPHA / 2, model.df_resid)   # dua sisi → alpha dibagi 2
for nama in model.params.index:
    ...
```
Perulangan mencetak t hitung, p-value, dan keputusan untuk setiap koefisien. Tolak H0 jika |t hitung| > t tabel.

### Bagian 5 — Uji asumsi klasik

Semua uji asumsi dilakukan pada **residual** (`model.resid`).

| Asumsi | Kode | H0 | Asumsi terpenuhi jika |
|---|---|---|---|
| Residual normal | `stats.shapiro(residual)`, `stats.kstest(...)` | residual berdistribusi normal | p > 0,05 |
| Homoskedastisitas | `het_breuschpagan(residual, X_const)` | varians residual konstan | p > 0,05 |
| Tidak ada multikolinearitas | `variance_inflation_factor(X_const.values, i)` | – | VIF < 10 |
| Tidak ada autokorelasi | `durbin_watson(residual)` | – | DW mendekati 2 (kira-kira 1,5–2,5) |
| Linearitas | `linear_reset(model, power=2, use_f=True)` | bentuk linear sudah tepat | p > 0,05 |

Catatan:
- Untuk uji KS, residual distandarkan dulu (`(residual - mean) / std`) karena `kstest(..., "norm")` membandingkan dengan normal baku N(0,1).
- VIF dihitung untuk tiap variabel bebas; kolom `const` dilewati karena VIF intersep tidak bermakna.
- Data ini *cross-section* (antarprovinsi, bukan deret waktu), sehingga autokorelasi bukan asumsi utama. Nilai DW tetap bisa rendah jika data diurutkan menurut wilayah.

### Bagian 6 — Grafik diagnostik

```python
fig, ax = plt.subplots(1, 3, figsize=(15, 4.5))   # 1 baris, 3 grafik
```

| Grafik | Cara membaca |
|---|---|
| **Residual vs Fitted** | Titik menyebar acak di sekitar garis 0 → linear & homoskedastis. Pola corong/kurva → ada masalah |
| **Normal Q-Q Plot** | Titik mengikuti garis diagonal → residual normal. Ujung yang melenceng → ada pencilan/skew |
| **Histogram Residual** | Bentuk mendekati lonceng simetris → normal |

`plt.savefig("grafik_diagnostik.png", dpi=150)` menyimpan grafik agar bisa langsung dimasukkan ke laporan.

---

## 5. Cara Membaca Output `model.summary()`

| Bagian output | Arti |
|---|---|
| `R-squared` | Proporsi variasi Y yang dijelaskan model (0–1) |
| `Adj. R-squared` | R² yang dikoreksi jumlah variabel; dipakai untuk membandingkan model |
| `F-statistic`, `Prob (F-statistic)` | Uji simultan |
| `coef` | Taksiran koefisien β |
| `std err` | Standard error koefisien |
| `t`, `P>|t|` | Uji parsial |
| `[0.025 0.975]` | Selang kepercayaan 95%; jika melewati 0 → tidak signifikan |
| `Durbin-Watson` | Uji autokorelasi |
| `Jarque-Bera (JB)`, `Prob(JB)` | Uji normalitas tambahan |
| `Cond. No.` | Indikasi multikolinearitas (sangat besar → waspada) |

**Interpretasi koefisien:** misalnya β1 = −0,664 berarti setiap kenaikan pengangguran 1 poin persen, persentase penduduk miskin diperkirakan **turun** 0,664 poin persen, dengan asumsi X2 tetap (*ceteris paribus*). Interpretasi ini hanya bermakna jika koefisiennya signifikan.

---

## 6. Struktur Folder

```
03-regresi/
├── data_regresi_38_provinsi.xlsx   # data mentah
├── main.py                         # skrip analisis
├── grafik_diagnostik.png           # output grafik (dibuat saat main.py dijalankan)
├── pyproject.toml                  # daftar library yang dibutuhkan
├── uv.lock                         # versi persis setiap library
├── todo.md                         # instruksi tugas
└── README.md                       # dokumen ini
```
