import streamlit as st
import pandas as pd
import pydeck as pdk

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Dashboard OPT GDD Sumatera",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================
st.markdown("""
<style>
/* =========================
   GLOBAL BACKGROUND
========================= */
.stApp {
    background: linear-gradient(135deg, #f4f7f2 0%, #eef5ec 45%, #ffffff 100%);
    color: #17231b;
}

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 3rem;
    max-width: 1160px;
}

/* =========================
   DEFAULT TEXT FIX
========================= */
html, body, [class*="css"] {
    color: #17231b !important;
}

p, span, div, label {
    color: #17231b;
}

h1, h2, h3, h4, h5, h6 {
    color: #102a1f !important;
    letter-spacing: -0.3px;
}

hr {
    border: none;
    border-top: 1px solid #d6e2d3;
    margin: 30px 0;
}

/* =========================
   SIDEBAR
========================= */
section[data-testid="stSidebar"] {
    background: #f5faf4 !important;
    border-right: 1px solid #cfded0;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #103d2c !important;
    font-weight: 800;
}

section[data-testid="stSidebar"] label {
    color: #17231b !important;
    font-weight: 700;
    font-size: 14px;
}

section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #17231b !important;
    border: 1px solid #cfded0 !important;
    border-radius: 12px !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] span {
    color: #17231b !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] svg {
    color: #17231b !important;
    fill: #17231b !important;
}

div[data-baseweb="popover"] {
    background-color: #ffffff !important;
}

div[data-baseweb="popover"] * {
    color: #17231b !important;
    background-color: #ffffff !important;
}

div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] div:hover {
    background-color: #eef5ec !important;
    color: #17231b !important;
}

/* =========================
   HEADER CARD
========================= */
.header-card {
    background: linear-gradient(135deg, #0f3d2e 0%, #1b5e3f 55%, #2d6a4f 100%);
    padding: 42px 34px;
    border-radius: 28px;
    color: #ffffff !important;
    text-align: center;
    margin-bottom: 34px;
    box-shadow: 0 18px 42px rgba(15, 61, 46, 0.24);
}

.header-card h1 {
    margin: 0;
    color: #ffffff !important;
    font-size: 36px;
    font-weight: 900;
    letter-spacing: 2px;
}

.header-card p {
    margin-top: 14px;
    font-size: 17px;
    color: #eef8f1 !important;
    font-weight: 500;
}

/* =========================
   INFO BOX
========================= */
.info-box {
    background: #ffffff;
    padding: 24px 26px;
    border-radius: 20px;
    border-left: 7px solid #2d6a4f;
    margin-bottom: 24px;
    box-shadow: 0 10px 26px rgba(18, 64, 43, 0.08);
    color: #17231b !important;
}

.info-box,
.info-box p,
.info-box span,
.info-box div {
    color: #17231b !important;
}

.info-box b {
    color: #103d2c !important;
}

.small-note {
    display: inline-block;
    margin-top: 8px;
    font-size: 13px;
    color: #4d5f54 !important;
}

/* =========================
   STATUS CARD
========================= */
.status-card {
    padding: 28px;
    border-radius: 24px;
    font-size: 28px;
    font-weight: 900;
    text-align: center;
    margin: 24px 0 30px 0;
    box-shadow: 0 14px 34px rgba(0,0,0,0.10);
    letter-spacing: 0.6px;
}

.status-green {
    background: #d8f3dc;
    color: #073b22 !important;
    border: 1px solid #95d5b2;
}

.status-yellow {
    background: #fff3cd;
    color: #704c00 !important;
    border: 1px solid #ffd166;
}

.status-red {
    background: #f8d7da;
    color: #741616 !important;
    border: 1px solid #ea868f;
}

/* =========================
   METRIC CARDS
========================= */
[data-testid="stMetric"] {
    background: #ffffff;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0 10px 26px rgba(18, 64, 43, 0.08);
    border: 1px solid #dfe8dc;
}

[data-testid="stMetric"] * {
    color: #17231b !important;
}

[data-testid="stMetricLabel"] {
    color: #405247 !important;
    font-weight: 800;
}

[data-testid="stMetricValue"] {
    color: #103d2c !important;
    font-weight: 900;
}

/* =========================
   ALERTS
========================= */
[data-testid="stAlert"] {
    border-radius: 18px;
    border: 1px solid #d9e2d8;
    box-shadow: 0 8px 22px rgba(0,0,0,0.06);
}

[data-testid="stAlert"] * {
    color: #17231b !important;
}

/* =========================
   INTERVENTION BOX
========================= */
.intervention-box {
    background-color: #ffffff !important;
    padding: 26px 30px;
    border-radius: 22px;
    border: 1px solid #dfe8dc;
    box-shadow: 0 12px 30px rgba(18, 64, 43, 0.08);
    margin-bottom: 24px;
    color: #17231b !important;
}

.intervention-box,
.intervention-box *,
.intervention-box p,
.intervention-box li,
.intervention-box ul,
.intervention-box ol,
.intervention-box strong,
.intervention-box em,
.intervention-box div,
.intervention-box span {
    color: #17231b !important;
    background-color: transparent !important;
}

.intervention-box strong {
    color: #103d2c !important;
    font-weight: 800 !important;
}

.intervention-box ul {
    margin-top: 10px !important;
    padding-left: 22px !important;
}

.intervention-box li {
    margin-bottom: 6px !important;
    line-height: 1.55 !important;
}

/* =========================
   CHART / DATAFRAME
========================= */
[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 12px 28px rgba(18, 64, 43, 0.08);
    border: 1px solid #dfe8dc;
}

[data-testid="stDataFrame"] * {
    color: #17231b !important;
}

[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] * {
    color: #405247 !important;
}

[data-testid="stExpander"] {
    background: #ffffff;
    border-radius: 16px;
    border: 1px solid #dfe8dc;
}

[data-testid="stExpander"] * {
    color: #17231b !important;
}

[data-testid="stMarkdownContainer"] {
    color: #17231b !important;
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] strong {
    color: #17231b !important;
}

.stDownloadButton button {
    background-color: #1b5e3f !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    border: none !important;
    font-weight: 700 !important;
}

.stDownloadButton button:hover {
    background-color: #0f3d2e !important;
    color: #ffffff !important;
}

.stButton button {
    background-color: #1b5e3f !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    border: none !important;
    font-weight: 700 !important;
}

.footer-note {
    color: #405247 !important;
    font-size: 13px;
    text-align: center;
    margin-top: 34px;
}

@media screen and (max-width: 768px) {
    .header-card {
        padding: 30px 20px;
        border-radius: 22px;
    }

    .header-card h1 {
        font-size: 26px;
        letter-spacing: 1px;
    }

    .header-card p {
        font-size: 14px;
    }

    .status-card {
        font-size: 22px;
        padding: 22px;
    }

    [data-testid="stMetric"] {
        padding: 16px;
    }
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================
st.markdown("""
<div class="header-card">
    <h1>DIGITAL MONITORING CARD OPT SUMATERA</h1>
    <p>Analisis Risiko Organisme Pengganggu Tanaman Berbasis Growing Degree Days dan Curah Hujan</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data
def load_data():
    df = pd.read_csv("dataset_final_dashboard_opt_gdd_sumatera.csv")
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("File dataset_final_dashboard_opt_gdd_sumatera.csv tidak ditemukan. Pastikan file CSV sudah di-upload ke GitHub.")
    st.stop()
except Exception as e:
    st.error("Data gagal dibaca.")
    st.write(e)
    st.stop()

# =====================================================
# VALIDASI KOLOM WAJIB
# =====================================================
required_columns = [
    "provinsi", "tahun", "triwulan", "komoditas", "opt",
    "tmax_rata", "tmin_rata", "suhu_rata", "hujan_total", "jumlah_hari"
]

missing_cols = [col for col in required_columns if col not in df.columns]

if missing_cols:
    st.error("Ada kolom wajib yang tidak ditemukan di dataset:")
    st.write(missing_cols)
    st.write("Kolom yang tersedia:")
    st.write(df.columns.tolist())
    st.stop()

# =====================================================
# BERSIHKAN TIPE DATA
# =====================================================
df["tahun"] = pd.to_numeric(df["tahun"], errors="coerce")
df["triwulan"] = pd.to_numeric(df["triwulan"], errors="coerce")
df["tmax_rata"] = pd.to_numeric(df["tmax_rata"], errors="coerce")
df["tmin_rata"] = pd.to_numeric(df["tmin_rata"], errors="coerce")
df["suhu_rata"] = pd.to_numeric(df["suhu_rata"], errors="coerce")
df["hujan_total"] = pd.to_numeric(df["hujan_total"], errors="coerce")
df["jumlah_hari"] = pd.to_numeric(df["jumlah_hari"], errors="coerce")

if "total_serangan" in df.columns:
    df["total_serangan"] = pd.to_numeric(df["total_serangan"], errors="coerce").fillna(0)

df = df.dropna(subset=["provinsi", "tahun", "triwulan", "komoditas", "opt"])

# =====================================================
# SIDEBAR FILTER
# =====================================================
st.sidebar.title("Filter Dashboard")

provinsi_list = sorted(df["provinsi"].dropna().unique())
provinsi = st.sidebar.selectbox("Pilih Provinsi", provinsi_list)

df_prov = df[df["provinsi"] == provinsi]

tahun_list = sorted(df_prov["tahun"].dropna().unique())
tahun = st.sidebar.selectbox("Pilih Tahun", tahun_list)

df_tahun = df_prov[df_prov["tahun"] == tahun]

triwulan_list = sorted(df_tahun["triwulan"].dropna().unique())
triwulan = st.sidebar.selectbox(
    "Pilih Triwulan",
    triwulan_list,
    format_func=lambda x: f"Triwulan {int(x)}"
)

df_triwulan = df_tahun[df_tahun["triwulan"] == triwulan]

komoditas_list = sorted(df_triwulan["komoditas"].dropna().unique())
komoditas = st.sidebar.selectbox("Pilih Komoditas", komoditas_list)

df_komoditas = df_triwulan[df_triwulan["komoditas"] == komoditas]

opt_list = sorted(df_komoditas["opt"].dropna().unique())
opt = st.sidebar.selectbox("Pilih OPT", opt_list)

df_pilih = df_komoditas[df_komoditas["opt"] == opt].copy()

df_grafik = df_tahun[
    (df_tahun["komoditas"] == komoditas) &
    (df_tahun["opt"] == opt)
].copy()

if df_pilih.empty:
    st.warning("Data tidak tersedia untuk pilihan ini.")
    st.stop()

# =====================================================
# PARAMETER BERDASARKAN OPT
# =====================================================
def ambil_parameter_opt(nama_komoditas, nama_opt):
    opt_lower = str(nama_opt).lower()
    komoditas_lower = str(nama_komoditas).lower()

    if "ulat api" in opt_lower or "ulat" in opt_lower:
        return {
            "tbase": 12,
            "gdd_kuning": 1000,
            "gdd_merah": 2200,
            "dasar_tbase": "Pendekatan Tbase OPT serangga daun/ulat"
        }

    elif "oryctes" in opt_lower or "kumbang" in opt_lower:
        return {
            "tbase": 12,
            "gdd_kuning": 1000,
            "gdd_merah": 2200,
            "dasar_tbase": "Pendekatan Tbase OPT kumbang/Oryctes"
        }

    elif "penggerek buah" in opt_lower or "pbko" in opt_lower:
        return {
            "tbase": 15,
            "gdd_kuning": 900,
            "gdd_merah": 1800,
            "dasar_tbase": "Pendekatan Tbase OPT penggerek buah kopi"
        }

    elif "penggerek" in opt_lower:
        return {
            "tbase": 15,
            "gdd_kuning": 900,
            "gdd_merah": 1800,
            "dasar_tbase": "Pendekatan Tbase OPT penggerek"
        }

    elif "karat" in opt_lower:
        return {
            "tbase": 15,
            "gdd_kuning": 900,
            "gdd_merah": 1800,
            "dasar_tbase": "Pendekatan Tbase OPT penyakit daun kopi"
        }

    elif "jamur" in opt_lower or "busuk" in opt_lower or "akar" in opt_lower or "ganoderma" in opt_lower:
        return {
            "tbase": 10,
            "gdd_kuning": 1200,
            "gdd_merah": 2500,
            "dasar_tbase": "Pendekatan Tbase OPT penyakit/jamur"
        }

    elif "tikus" in opt_lower or "babi" in opt_lower:
        if "sawit" in komoditas_lower:
            tbase_default = 12
            kuning = 1000
            merah = 2200
        elif "kopi" in komoditas_lower:
            tbase_default = 15
            kuning = 900
            merah = 1800
        else:
            tbase_default = 10
            kuning = 1200
            merah = 2500

        return {
            "tbase": tbase_default,
            "gdd_kuning": kuning,
            "gdd_merah": merah,
            "dasar_tbase": "OPT vertebrata tidak memiliki Tbase GDD spesifik; memakai pendekatan komoditas"
        }

    else:
        if "sawit" in komoditas_lower:
            return {
                "tbase": 12,
                "gdd_kuning": 1000,
                "gdd_merah": 2200,
                "dasar_tbase": "Parameter spesifik OPT belum tersedia; memakai pendekatan komoditas kelapa sawit"
            }

        elif "kopi" in komoditas_lower:
            return {
                "tbase": 15,
                "gdd_kuning": 900,
                "gdd_merah": 1800,
                "dasar_tbase": "Parameter spesifik OPT belum tersedia; memakai pendekatan komoditas kopi"
            }

        else:
            return {
                "tbase": 10,
                "gdd_kuning": 1200,
                "gdd_merah": 2500,
                "dasar_tbase": "Parameter spesifik OPT belum tersedia; memakai pendekatan komoditas karet"
            }

param = ambil_parameter_opt(komoditas, opt)

tbase = param["tbase"]
gdd_kuning = param["gdd_kuning"]
gdd_merah = param["gdd_merah"]
dasar_tbase = param["dasar_tbase"]

# =====================================================
# HITUNG GDD DASHBOARD UNTUK SEMUA OPT
# =====================================================
df_pilih = df_pilih.sort_values(["tahun", "triwulan"])

df_pilih["gdd_triwulan_dashboard"] = (
    (((df_pilih["tmax_rata"] + df_pilih["tmin_rata"]) / 2) - tbase)
    * df_pilih["jumlah_hari"]
).clip(lower=0)

df_pilih["gdd_akumulasi_dashboard"] = (
    df_pilih
    .groupby(["provinsi", "komoditas", "opt", "tahun"])["gdd_triwulan_dashboard"]
    .cumsum()
)

df_grafik = df_grafik.sort_values(["tahun", "triwulan"])

df_grafik["gdd_triwulan_dashboard"] = (
    (((df_grafik["tmax_rata"] + df_grafik["tmin_rata"]) / 2) - tbase)
    * df_grafik["jumlah_hari"]
).clip(lower=0)

df_grafik["gdd_akumulasi_dashboard"] = (
    df_grafik
    .groupby(["provinsi", "komoditas", "opt", "tahun"])["gdd_triwulan_dashboard"]
    .cumsum()
)

data_akhir = df_pilih.iloc[-1]
gdd_akhir = data_akhir["gdd_akumulasi_dashboard"]

def status_dari_gdd(gdd):
    if gdd >= gdd_merah:
        return "Merah"
    elif gdd >= gdd_kuning:
        return "Kuning"
    else:
        return "Hijau"

status = status_dari_gdd(gdd_akhir)

# =====================================================
# RINGKASAN PILIHAN
# =====================================================
st.subheader(f"{provinsi} | {int(tahun)} | Triwulan {int(triwulan)} | {komoditas} | {opt}")

st.markdown(f"""
<div class="info-box">
    <b>Parameter GDD yang digunakan:</b><br>
    Tbase: <b>{tbase} °C</b><br>
    Dasar Tbase: <b>{dasar_tbase}</b><br>
    Ambang Kuning: <b>{gdd_kuning}</b><br>
    Ambang Merah: <b>{gdd_merah}</b><br>
    <span class="small-note">
    Catatan: Sistem memprioritaskan Tbase berdasarkan OPT. Jika parameter spesifik OPT belum tersedia, sistem memakai pendekatan kelompok OPT atau komoditas.
    </span>
</div>
""", unsafe_allow_html=True)

# =====================================================
# STATUS CARD
# =====================================================
if status == "Merah":
    st.markdown('<div class="status-card status-red">MERAH - Risiko Tinggi</div>', unsafe_allow_html=True)
elif status == "Kuning":
    st.markdown('<div class="status-card status-yellow">KUNING - Perlu Waspada</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-card status-green">HIJAU - Relatif Aman</div>', unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# METRIC CARDS
# =====================================================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Tahun", int(data_akhir["tahun"]))
col2.metric("Triwulan Dipilih", int(data_akhir["triwulan"]))
col3.metric("Suhu Rata-rata", f"{data_akhir['suhu_rata']:.2f} °C")
col4.metric("Curah Hujan", f"{data_akhir['hujan_total']:.2f} mm")

col5, col6, col7, col8 = st.columns(4)

col5.metric("Tbase", f"{tbase} °C")
col6.metric("GDD Triwulan", f"{data_akhir['gdd_triwulan_dashboard']:.2f}")
col7.metric("Akumulasi GDD", f"{data_akhir['gdd_akumulasi_dashboard']:.2f}")

if "total_serangan" in df_pilih.columns:
    col8.metric("Total Serangan", f"{data_akhir['total_serangan']:.2f} ha")
else:
    col8.metric("Total Serangan", "-")

# =====================================================
# RINGKASAN MONITORING SEMUA PROVINSI
# =====================================================
st.subheader("Ringkasan Monitoring Semua Provinsi")

df_ringkasan = df[
    (df["tahun"] == tahun) &
    (df["triwulan"] == triwulan) &
    (df["komoditas"] == komoditas) &
    (df["opt"] == opt)
].copy()

if not df_ringkasan.empty:
    df_ringkasan["gdd_triwulan_dashboard"] = (
        (((df_ringkasan["tmax_rata"] + df_ringkasan["tmin_rata"]) / 2) - tbase)
        * df_ringkasan["jumlah_hari"]
    ).clip(lower=0)

    df_ringkasan = df_ringkasan.sort_values(["provinsi", "tahun", "triwulan"])

    df_ringkasan["gdd_akumulasi_dashboard"] = (
        df_ringkasan
        .groupby(["provinsi", "komoditas", "opt", "tahun"])["gdd_triwulan_dashboard"]
        .cumsum()
    )

    df_ringkasan["status_dashboard"] = df_ringkasan["gdd_akumulasi_dashboard"].apply(status_dari_gdd)

    kolom_ringkasan = [
        "provinsi",
        "tahun",
        "triwulan",
        "komoditas",
        "opt",
        "suhu_rata",
        "hujan_total",
        "gdd_triwulan_dashboard",
        "gdd_akumulasi_dashboard",
        "status_dashboard"
    ]

    if "total_serangan" in df_ringkasan.columns:
        kolom_ringkasan.append("total_serangan")

    df_ringkasan_tampil = df_ringkasan[kolom_ringkasan].copy()

    df_ringkasan_tampil = df_ringkasan_tampil.rename(columns={
        "provinsi": "Provinsi",
        "tahun": "Tahun",
        "triwulan": "Triwulan",
        "komoditas": "Komoditas",
        "opt": "OPT",
        "suhu_rata": "Suhu Rata-rata (°C)",
        "hujan_total": "Curah Hujan (mm)",
        "gdd_triwulan_dashboard": "GDD Triwulan",
        "gdd_akumulasi_dashboard": "Akumulasi GDD",
        "status_dashboard": "Status",
        "total_serangan": "Total Serangan (ha)"
    })

    st.dataframe(df_ringkasan_tampil, use_container_width=True)

    jumlah_hijau = (df_ringkasan["status_dashboard"] == "Hijau").sum()
    jumlah_kuning = (df_ringkasan["status_dashboard"] == "Kuning").sum()
    jumlah_merah = (df_ringkasan["status_dashboard"] == "Merah").sum()

    colr1, colr2, colr3 = st.columns(3)

    colr1.metric("Provg
