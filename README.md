# 🏠 Boston House Price Predictor

Aplikasi prediksi harga rumah berbasis **Machine Learning** menggunakan Boston Housing Dataset. Dibangun dengan Python + Tkinter sebagai bagian dari proyek mata kuliah Kecerdasan Buatan.

**Tim DAPUR MBG — Kelompok MBG.CO**

| Nama | NIM |
|------|-----|
| Muhammad Azza Arsyada Roziqi | 245150200111062 |
| Teuku Muhammad Panji Fachroni | 245150200111052 |
| Ahmad Hilalul Fadli | 245150201111045 |
| Rusdiansyah Alief Prasetya | 245150207111073 |
| Richard Samuel Hatane | 245150200111061 |
| Aqeela Sahla | 245150201111039 |

---

## 📋 Deskripsi Proyek

Proyek ini membangun sistem prediksi harga median rumah di wilayah Boston menggunakan algoritma **Multiple Linear Regression**. Sistem ini hadir sebagai solusi atas penilaian properti manual yang sering kali subjektif, lambat, dan tidak konsisten.

### Problem Statement

Penilaian harga properti secara tradisional bergantung pada inspeksi manual oleh penilai (appraiser) yang membutuhkan waktu lama dan rentan terhadap bias subjektif. Proyek ini mengotomasi proses tersebut dengan memanfaatkan data historis Boston Housing untuk membangun model prediksi berbasis data.

### Input & Output

| Jenis | Variabel | Deskripsi |
|-------|----------|-----------|
| Input | **RM** | Rata-rata jumlah kamar per unit rumah |
| Input | **LSTAT** | Persentase penduduk berpenghasilan rendah di lingkungan (%) |
| Input | **PTRATIO** | Rasio murid terhadap guru di area tersebut |
| Output | **MEDV** | Estimasi harga median rumah (dalam USD) |

---

## 📁 Struktur Repositori

```
boston-house-app/
│
├── data/
│   └── housing.csv           # Dataset Boston Housing (490 baris, 4 fitur)
│
├── model/
│   ├── train.py              # Script pelatihan model & ekspor .pkl
│   └── boston_model.pkl      # Model terlatih (dibuat setelah menjalankan train.py)
│
├── gui/
│   └── app.py                # Aplikasi GUI Tkinter
│
├── assets/                   # Ikon dan aset visual aplikasi
│
├── requirements.txt          # Daftar dependensi Python
│
└── README.md
```

---

## ⚙️ Cara Menjalankan

### 1. Clone Repository

```bash
git clone https://github.com/RusdiansyahAlief19/boston-house-app.git
cd boston-house-app
```

### 2. Install Dependensi

```bash
pip install -r requirements.txt
```

### 3. Latih Model (wajib dilakukan sekali sebelum menjalankan GUI)

```bash
python model/train.py
```

Script ini akan membaca `data/housing.csv`, melakukan preprocessing, melatih model, lalu menyimpan `boston_model.pkl` ke folder `model/`.

### 4. Jalankan Aplikasi GUI

```bash
python gui/app.py
```

---

## 🔬 Metodologi

### 1. Eksplorasi Data
- Analisis statistik deskriptif (mean, std, min, max)
- Visualisasi distribusi fitur menggunakan histogram dan boxplot
- Identifikasi outlier dan pola korelasi antar fitur

### 2. Preprocessing Data

| Tahap | Metode | Alasan |
|-------|--------|--------|
| Penanganan Missing Value | Class-Conditional Mean Imputation | Mempertahankan karakteristik distribusi per kelompok MEDV, lebih representatif dibanding mean global |
| Normalisasi | Z-Score Normalization | Stabil terhadap outlier (yang ada di fitur LSTAT), menghasilkan mean=0 dan std=1, cocok untuk regresi linear |
| Pemisahan Data | Train-Test Split 80:20 | Proporsi standar yang memberikan cukup data training sambai tetap menyisakan data uji yang representatif |

### 3. Pemodelan

Algoritma: **Multiple Linear Regression**

Model mempelajari bobot (koefisien) dari tiga variabel input secara simultan untuk memprediksi MEDV:

```
MEDV = β₀ + β₁(RM) + β₂(LSTAT) + β₃(PTRATIO) + ε
```

Dipilih karena: interpretabilitas koefisien tinggi, kompleksitas sesuai jumlah fitur, dan hubungan antar fitur yang cukup linear berdasarkan eksplorasi awal.

### 4. Evaluasi Model

| Metrik | Deskripsi | Alasan Dipilih |
|--------|-----------|----------------|
| **RMSE** (Root Mean Squared Error) | Rata-rata besar error prediksi | Memberikan penalti lebih besar pada error besar — relevan karena kesalahan prediksi harga ratusan juta lebih merugikan |
| **R²** (R-squared) | Seberapa besar variasi harga yang dijelaskan model | Melengkapi RMSE: RMSE mengukur besarnya error, R² mengukur kemampuan model memahami pola data |

---

## 📊 Dataset

**Boston Housing Dataset** — 490 entri, 4 fitur numerik (float64)

| Fitur | Mean | Std | Min | Max |
|-------|------|-----|-----|-----|
| RM | 6.24 | 0.64 | 3.56 | 8.78 |
| LSTAT | 12.92 | 7.08 | 1.98 | 37.97 |
| PTRATIO | 18.52 | 2.11 | 12.60 | 22.00 |
| MEDV (USD) | $454,354 | $165,171 | $105,000 | $1,024,800 |

---

## 🛠️ Teknologi

- **Python 3.x**
- **pandas** — manipulasi data
- **numpy** — komputasi numerik
- **scikit-learn** — model regresi dan preprocessing
- **matplotlib / seaborn** — visualisasi data
- **tkinter** — GUI desktop
- **joblib** — serialisasi model

---

## 📦 requirements.txt

Lihat file `requirements.txt` untuk daftar lengkap versi dependensi.

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan akademik. Dataset Boston Housing bersumber dari Harrison, D. & Rubinfeld, D.L. (1978), *Hedonic prices and the demand for clean air*, Journal of Environmental Economics and Management.
