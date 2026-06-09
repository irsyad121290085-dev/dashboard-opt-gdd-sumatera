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
# PARAMETER MODEL RISIKO BERDASARKAN KARAKTER OPT
# =====================================================
def ambil_parameter_opt(nama_komoditas, nama_opt):
    opt_lower = str(nama_opt).lower()
    komoditas_lower = str(nama_komoditas).lower()

    # =================================================
    # 1. MODEL GDD SIKLUS HIDUP
    # Dipakai untuk OPT yang punya referensi degree-day lebih kuat.
    # =================================================
    if (
        "pbko" in opt_lower
        or "penggerek buah kopi" in opt_lower
        or "hypothenemus" in opt_lower
    ):
        return {
            "tipe_model": "GDD Siklus Hidup OPT",
            "tbase": 14.9,
            "gdd_fase_merusak": 262.47,
            "gdd_kuning": 262.47 * 0.6,
            "gdd_merah": 262.47,
            "fase_merusak": "Generasi baru / fase aktif merusak buah kopi",
            "dasar_model": "Model GDD siklus hidup PBKo; Tbase ±14,9°C dan kebutuhan panas ±262,47 degree-days.",
            "sumber_model": "Jaramillo et al. (2009); Hamilton et al. (2019)"
        }

    # =================================================
    # 2. MODEL GDD HISTORIS SERANGGA
    # Dipakai untuk serangga yang belum punya angka fase GDD spesifik.
    # Status dihitung dari pola historis dataset.
    # =================================================
    elif (
        "ulat api" in opt_lower
        or "ulat" in opt_lower
        or "oryctes" in opt_lower
        or "kumbang" in opt_lower
        or "penggerek" in opt_lower
    ):
        if "kopi" in komoditas_lower:
            tbase_default = 15
        elif "sawit" in komoditas_lower:
            tbase_default = 12
        else:
            tbase_default = 10

        return {
            "tipe_model": "GDD Historis Serangga",
            "tbase": tbase_default,
            "gdd_fase_merusak": None,
            "gdd_kuning": None,
            "gdd_merah": None,
            "fase_merusak": "Fase merusak spesifik belum dimasukkan; status dibaca dari pola historis GDD dataset.",
            "dasar_model": "OPT serangga dimodelkan dengan akumulasi GDD, tetapi ambang fase merusak spesifik belum tersedia.",
            "sumber_model": "Pendekatan historis dataset dan konsep GDD serangga."
        }

    # =================================================
    # 3. MODEL KONDISI LINGKUNGAN PENYAKIT / JAMUR
    # Tidak dipaksa pakai siklus GDD serangga.
    # =================================================
    elif (
        "karat" in opt_lower
        or "jamur" in opt_lower
        or "busuk" in opt_lower
        or "akar" in opt_lower
        or "ganoderma" in opt_lower
    ):
        return {
            "tipe_model": "Kondisi Lingkungan Penyakit",
            "tbase": 10,
            "gdd_fase_merusak": None,
            "gdd_kuning": None,
            "gdd_merah": None,
            "fase_merusak": "Penyakit/jamur lebih dipengaruhi kondisi suhu, kelembapan, dan curah hujan.",
            "dasar_model": "Model penyakit menggunakan kondisi lingkungan pendukung, bukan siklus GDD serangga.",
            "sumber_model": "Pendekatan agroklimat penyakit tanaman."
        }

    # =================================================
    # 4. MODEL MONITORING HISTORIS / LAPANGAN
    # Untuk OPT vertebrata.
    # =================================================
    elif "tikus" in opt_lower or "babi" in opt_lower:
        if "sawit" in komoditas_lower:
            tbase_default = 12
        elif "kopi" in komoditas_lower:
            tbase_default = 15
        else:
            tbase_default = 10

        return {
            "tipe_model": "Monitoring Historis/Lapangan",
            "tbase": tbase_default,
            "gdd_fase_merusak": None,
            "gdd_kuning": None,
            "gdd_merah": None,
            "fase_merusak": "OPT vertebrata tidak dimodelkan dengan fase GDD.",
            "dasar_model": "Tikus/babi lebih tepat dibaca dari riwayat serangan dan monitoring lapangan.",
            "sumber_model": "Pendekatan monitoring historis dan observasi lapangan."
        }

    # =================================================
    # FALLBACK
    # =================================================
    else:
        if "kopi" in komoditas_lower:
            tbase_default = 15
        elif "sawit" in komoditas_lower:
            tbase_default = 12
        else:
            tbase_default = 10

        return {
            "tipe_model": "Pendekatan Komoditas",
            "tbase": tbase_default,
            "gdd_fase_merusak": None,
            "gdd_kuning": None,
            "gdd_merah": None,
            "fase_merusak": "Jenis OPT belum dikenali spesifik oleh sistem.",
            "dasar_model": "Parameter spesifik OPT belum tersedia; sistem memakai pendekatan komoditas.",
            "sumber_model": "Pendekatan awal dashboard."
        }


param = ambil_parameter_opt(komoditas, opt)

tipe_model = param["tipe_model"]
tbase = param["tbase"]
gdd_fase_merusak = param["gdd_fase_merusak"]
gdd_kuning = param["gdd_kuning"]
gdd_merah = param["gdd_merah"]
fase_merusak = param["fase_merusak"]
dasar_model = param["dasar_model"]
sumber_model = param["sumber_model"]
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

def status_dari_model(gdd, suhu, hujan, total_serangan=0):
    # =================================================
    # MODEL 1: GDD SIKLUS HIDUP OPT
    # Hijau  = belum mendekati fase merusak
    # Kuning = mendekati fase merusak
    # Merah  = sudah mencapai/melewati fase merusak
    # =================================================
    if tipe_model == "GDD Siklus Hidup OPT":
        if gdd >= gdd_merah:
            return "Merah"
        elif gdd >= gdd_kuning:
            return "Kuning"
        else:
            return "Hijau"

    # =================================================
    # MODEL 2: GDD HISTORIS SERANGGA
    # Status dibaca dari pola historis GDD pada dataset
    # untuk OPT dan komoditas yang sama.
    # =================================================
    elif tipe_model == "GDD Historis Serangga":
        data_hist = df[
            (df["komoditas"] == komoditas) &
            (df["opt"] == opt)
        ].copy()

        if data_hist.empty:
            return "Hijau"

        data_hist["gdd_hist"] = (
            (((data_hist["tmax_rata"] + data_hist["tmin_rata"]) / 2) - tbase)
            * data_hist["jumlah_hari"]
        ).clip(lower=0)

        q60 = data_hist["gdd_hist"].quantile(0.60)
        q85 = data_hist["gdd_hist"].quantile(0.85)

        if gdd >= q85:
            return "Merah"
        elif gdd >= q60:
            return "Kuning"
        else:
            return "Hijau"

    # =================================================
    # MODEL 3: KONDISI LINGKUNGAN PENYAKIT / JAMUR
    # Menggunakan suhu dan curah hujan sebagai kondisi pendukung.
    # =================================================
    elif tipe_model == "Kondisi Lingkungan Penyakit":
        skor = 0

        # Suhu hangat-lembap umumnya mendukung banyak penyakit/jamur tropis.
        if 24 <= suhu <= 32:
            skor += 1

        # Curah hujan tinggi meningkatkan kelembapan lingkungan.
        if hujan >= 300:
            skor += 2
        elif hujan >= 150:
            skor += 1

        # Riwayat serangan memperkuat status.
        if total_serangan > 0:
            skor += 1

        if skor >= 3:
            return "Merah"
        elif skor >= 2:
            return "Kuning"
        else:
            return "Hijau"

    # =================================================
    # MODEL 4: MONITORING HISTORIS / LAPANGAN
    # Untuk tikus/babi dan OPT yang tidak cocok dimodelkan GDD.
    # =================================================
    elif tipe_model == "Monitoring Historis/Lapangan":
        if total_serangan > 0:
            return "Merah"
        elif hujan >= 250:
            return "Kuning"
        else:
            return "Hijau"

    # =================================================
    # FALLBACK
    # =================================================
    else:
        if total_serangan > 0:
            return "Kuning"
        else:
            return "Hijau"


total_serangan_akhir = 0

if "total_serangan" in df_pilih.columns:
    total_serangan_akhir = data_akhir["total_serangan"]

status = status_dari_model(
    gdd_akhir,
    data_akhir["suhu_rata"],
    data_akhir["hujan_total"],
    total_serangan_akhir
)

# =====================================================
# RINGKASAN PILIHAN
# =====================================================
st.subheader(f"{provinsi} | {int(tahun)} | Triwulan {int(triwulan)} | {komoditas} | {opt}")

st.markdown(f"""
<div class="info-box">
    <b>Model risiko yang digunakan:</b> {tipe_model}<br>
    Tbase: <b>{tbase} °C</b><br>
    Fase/indikator merusak: <b>{fase_merusak}</b><br>
    Dasar model: <b>{dasar_model}</b><br>
    Sumber/pendekatan: <b>{sumber_model}</b><br>
    <span class="small-note">
    Catatan: Status hijau, kuning, dan merah tidak lagi memakai ambang GDD umum.
    Status disesuaikan dengan karakter OPT: siklus hidup serangga, kondisi lingkungan penyakit, atau monitoring historis/lapangan.
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
    def hitung_status_ringkasan(row):
    total_serangan_row = 0

    if "total_serangan" in row.index:
        total_serangan_row = row["total_serangan"]

    return status_dari_model(
        row["gdd_akumulasi_dashboard"],
        row["suhu_rata"],
        row["hujan_total"],
        total_serangan_row
    )

df_ringkasan["status_dashboard"] = df_ringkasan.apply(hitung_status_ringkasan, axis=1)

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

    colr1.metric("Provinsi Status Hijau", int(jumlah_hijau))
    colr2.metric("Provinsi Status Kuning", int(jumlah_kuning))
    colr3.metric("Provinsi Status Merah", int(jumlah_merah))

else:
    st.info("Data ringkasan semua provinsi tidak tersedia untuk kombinasi pilihan ini.")

# =====================================================
# PETA STATUS BERWARNA PROVINSI SUMATERA
# =====================================================
st.subheader("Peta Monitoring Status Risiko Provinsi Sumatera")
st.caption("Warna titik menunjukkan status risiko: hijau = aman, kuning = waspada, merah = risiko tinggi.")

koordinat_provinsi = {
    "Aceh": [4.6951, 96.7494],
    "Sumatera Utara": [2.1154, 99.5451],
    "Sumatera Barat": [-0.7399, 100.8000],
    "Riau": [0.2933, 101.7068],
    "Jambi": [-1.6101, 103.6131],
    "Bengkulu": [-3.8004, 102.2655],
    "Sumatera Selatan": [-3.3194, 103.9144],
    "Lampung": [-4.5586, 105.4068],
    "Bangka Belitung": [-2.7411, 106.4406],
    "Kep. Riau": [3.9457, 108.1429]
}

def warna_status(status_value):
    if status_value == "Merah":
        return [220, 53, 69, 180]
    elif status_value == "Kuning":
        return [255, 193, 7, 180]
    else:
        return [40, 167, 69, 180]

if "df_ringkasan" in locals() and not df_ringkasan.empty:
    data_peta = df_ringkasan.copy()

    data_peta["lat"] = data_peta["provinsi"].map(
        lambda x: koordinat_provinsi.get(x, [None, None])[0]
    )

    data_peta["lon"] = data_peta["provinsi"].map(
        lambda x: koordinat_provinsi.get(x, [None, None])[1]
    )

    data_peta = data_peta.dropna(subset=["lat", "lon"])

    if not data_peta.empty:
        data_peta["warna"] = data_peta["status_dashboard"].apply(warna_status)

        data_peta["tooltip"] = (
            "Provinsi: " + data_peta["provinsi"].astype(str) +
            "<br>Komoditas: " + data_peta["komoditas"].astype(str) +
            "<br>OPT: " + data_peta["opt"].astype(str) +
            "<br>Status: " + data_peta["status_dashboard"].astype(str) +
            "<br>Akumulasi GDD: " + data_peta["gdd_akumulasi_dashboard"].round(2).astype(str)
        )

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=data_peta,
            get_position="[lon, lat]",
            get_fill_color="warna",
            get_radius=45000,
            pickable=True
        )

        view_state = pdk.ViewState(
            latitude=-0.8,
            longitude=102.5,
            zoom=4.4,
            pitch=0
        )

        deck = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={
                "html": "{tooltip}",
                "style": {
                    "backgroundColor": "white",
                    "color": "black"
                }
            }
        )

        st.pydeck_chart(deck)

        st.markdown("""
        **Keterangan warna:**

        - Hijau: Risiko rendah / relatif aman  
        - Kuning: Risiko sedang / perlu kewaspadaan  
        - Merah: Risiko tinggi / perlu intervensi  
        """)

        kolom_peta = [
            "provinsi",
            "komoditas",
            "opt",
            "status_dashboard",
            "gdd_akumulasi_dashboard"
        ]

        if "total_serangan" in data_peta.columns:
            kolom_peta.append("total_serangan")

        tabel_peta = data_peta[kolom_peta].copy()

        tabel_peta = tabel_peta.rename(columns={
            "provinsi": "Provinsi",
            "komoditas": "Komoditas",
            "opt": "OPT",
            "status_dashboard": "Status",
            "gdd_akumulasi_dashboard": "Akumulasi GDD",
            "total_serangan": "Total Serangan (ha)"
        })

        st.dataframe(tabel_peta, use_container_width=True)
    else:
        st.info("Koordinat provinsi tidak tersedia untuk data yang dipilih.")
else:
    st.info("Data ringkasan provinsi belum tersedia untuk ditampilkan pada peta.")

# =====================================================
# PREDIKSI GDD TRIWULAN BERIKUTNYA
# =====================================================
st.subheader("Prediksi Triwulan Berikutnya")

triwulan_saat_ini = int(data_akhir["triwulan"])
tahun_saat_ini = int(data_akhir["tahun"])

if triwulan_saat_ini < 4:
    triwulan_prediksi = triwulan_saat_ini + 1
    tahun_prediksi = tahun_saat_ini
else:
    triwulan_prediksi = 1
    tahun_prediksi = tahun_saat_ini + 1

data_historis_next = df[
    (df["provinsi"] == provinsi) &
    (df["komoditas"] == komoditas) &
    (df["opt"] == opt) &
    (df["triwulan"] == triwulan_prediksi) &
    (df["tahun"] < tahun_prediksi)
].copy()

if not data_historis_next.empty:
    data_historis_next["gdd_prediksi_basis"] = (
        (((data_historis_next["tmax_rata"] + data_historis_next["tmin_rata"]) / 2) - tbase)
        * data_historis_next["jumlah_hari"]
    ).clip(lower=0)

    rata_gdd_next = data_historis_next["gdd_prediksi_basis"].mean()
    prediksi_akumulasi = gdd_akhir + rata_gdd_next
    rata_suhu_prediksi = data_historis_next["suhu_rata"].mean()
rata_hujan_prediksi = data_historis_next["hujan_total"].mean()

if "total_serangan" in data_historis_next.columns:
    rata_serangan_prediksi = data_historis_next["total_serangan"].mean()
else:
    rata_serangan_prediksi = 0

status_prediksi = status_dari_model(
    prediksi_akumulasi,
    rata_suhu_prediksi,
    rata_hujan_prediksi,
    rata_serangan_prediksi
)

    colp1, colp2, colp3, colp4 = st.columns(4)

    colp1.metric("Tahun Prediksi", int(tahun_prediksi))
    colp2.metric("Prediksi Triwulan", int(triwulan_prediksi))
    colp3.metric("Tambahan GDD Prediksi", f"{rata_gdd_next:.2f} GDD")
    colp4.metric("Prediksi Akumulasi GDD", f"{prediksi_akumulasi:.2f} GDD")

    if status_prediksi == "Merah":
        st.error(f"Prediksi Status {tahun_prediksi} Triwulan {triwulan_prediksi}: MERAH - Risiko tinggi")
    elif status_prediksi == "Kuning":
        st.warning(f"Prediksi Status {tahun_prediksi} Triwulan {triwulan_prediksi}: KUNING - Perlu kewaspadaan")
    else:
        st.success(f"Prediksi Status {tahun_prediksi} Triwulan {triwulan_prediksi}: HIJAU - Risiko relatif rendah")

    st.caption(
        "Prediksi dihitung menggunakan rata-rata historis GDD pada triwulan yang sama "
        "berdasarkan data tahun-tahun sebelumnya dalam dataset."
    )
else:
    st.info("Data historis untuk prediksi triwulan berikutnya belum tersedia.")

# =====================================================
# INTERVENSI UNTUK SEMUA KOMODITAS / OPT
# =====================================================
st.subheader("Rekomendasi Intervensi")

def intervensi_umum(nama_komoditas, nama_opt, status_risiko):
    opt_lower = str(nama_opt).lower()
    komoditas_lower = str(nama_komoditas).lower()

    if status_risiko == "Hijau":
        return """
        **Status Hijau - Aman**
        - Lakukan monitoring rutin.
        - Catat kondisi tanaman dan gejala awal OPT.
        - Jaga sanitasi lahan/kebun.
        - Tidak perlu tindakan pengendalian intensif.
        """

    elif status_risiko == "Kuning":
        return """
        **Status Kuning - Hati-hati**
        - Tingkatkan frekuensi pengamatan lapangan.
        - Periksa bagian tanaman yang rentan terserang.
        - Identifikasi gejala awal dan populasi OPT.
        - Siapkan tindakan pengendalian terpadu bila serangan meningkat.
        """

    elif status_risiko == "Merah":
        if "kumbang" in opt_lower or "oryctes" in opt_lower:
            return """
            **Status Merah - Bahaya: Kumbang / Oryctes**
            - Lakukan sanitasi batang, tunggul, dan pelepah membusuk.
            - Kurangi tempat berkembang biak larva.
            - Gunakan perangkap feromon bila tersedia.
            - Pantau tanaman muda dengan gejala gerekan.
            - Terapkan pengendalian terpadu sesuai rekomendasi lapangan.
            """

        elif "ulat" in opt_lower:
            return """
            **Status Merah - Bahaya: Ulat**
            - Lakukan pengamatan intensif pada daun atau pelepah.
            - Identifikasi tingkat populasi larva.
            - Pertahankan musuh alami.
            - Lakukan pengendalian terpadu jika populasi melewati ambang kendali.
            """

        elif "penggerek" in opt_lower:
            return """
            **Status Merah - Bahaya: Penggerek**
            - Sanitasi bagian tanaman yang terserang.
            - Kumpulkan dan musnahkan bagian tanaman atau buah terserang.
            - Gunakan perangkap bila tersedia.
            - Lakukan pengendalian terpadu secara tepat sasaran.
            """

        elif "karat" in opt_lower or "jamur" in opt_lower or "busuk" in opt_lower:
            return """
            **Status Merah - Bahaya: Penyakit / Jamur**
            - Pangkas bagian tanaman yang terlalu rimbun.
            - Perbaiki sirkulasi udara dan drainase.
            - Sanitasi tanaman sakit.
            - Lakukan pengendalian penyakit sesuai rekomendasi teknis.
            """

        elif "babi" in opt_lower or "tikus" in opt_lower:
            return """
            **Status Merah - Bahaya: Hama Vertebrata**
            - Perkuat monitoring batas kebun/lahan.
            - Gunakan penghalang fisik atau perangkap sesuai ketentuan.
            - Bersihkan area yang menjadi tempat persembunyian.
            - Lakukan pengendalian terpadu berbasis kondisi lapangan.
            """

        else:
            if "karet" in komoditas_lower:
                return """
                **Status Merah - Bahaya pada Komoditas Karet**
                - Lakukan pengamatan intensif pada batang, daun, akar, dan area sekitar tanaman.
                - Identifikasi gejala serangan OPT.
                - Sanitasi kebun dan tanaman terserang.
                - Terapkan pengendalian terpadu sesuai kondisi lapangan.
                """

            elif "sawit" in komoditas_lower:
                return """
                **Status Merah - Bahaya pada Komoditas Kelapa Sawit**
                - Lakukan monitoring pelepah, pucuk, batang, dan tandan.
                - Bersihkan bahan organik membusuk yang dapat menjadi sumber OPT.
                - Gunakan perangkap atau pengendalian hayati bila tersedia.
                - Terapkan pengendalian terpadu sesuai ambang kendali.
                """

            elif "kopi" in komoditas_lower:
                return """
                **Status Merah - Bahaya pada Komoditas Kopi**
                - Periksa buah, daun, batang, dan cabang.
                - Lakukan sanitasi kebun dan pemangkasan bila diperlukan.
                - Kumpulkan bagian tanaman/buah terserang.
                - Terapkan pengendalian terpadu sesuai rekomendasi teknis.
                """

            else:
                return """
                **Status Merah - Bahaya**
                - Lakukan pengamatan intensif.
                - Identifikasi tingkat serangan.
                - Terapkan pengendalian terpadu.
                - Gunakan pestisida secara bijak hanya bila diperlukan dan sesuai rekomendasi.
                """

    return "Intervensi belum tersedia."

st.info(intervensi_umum(komoditas, opt, status))

# =====================================================
# GRAFIK BAWAAN STREAMLIT
# =====================================================
st.subheader("Grafik Akumulasi GDD per Triwulan")
st.caption("Satuan: GDD kumulatif. Sumbu X = Triwulan, Sumbu Y = Akumulasi GDD.")

grafik_gdd = df_grafik[["triwulan", "gdd_akumulasi_dashboard"]].copy()
grafik_gdd = grafik_gdd.groupby("triwulan", as_index=True)["gdd_akumulasi_dashboard"].mean()
grafik_gdd = grafik_gdd.reindex([1, 2, 3, 4])

st.line_chart(grafik_gdd)

st.subheader("Curah Hujan per Triwulan")
st.caption("Satuan: milimeter (mm). Sumbu X = Triwulan, Sumbu Y = Total curah hujan triwulan.")

grafik_hujan = df_grafik[["triwulan", "hujan_total"]].copy()
grafik_hujan = grafik_hujan.groupby("triwulan", as_index=True)["hujan_total"].mean()
grafik_hujan = grafik_hujan.reindex([1, 2, 3, 4])

st.bar_chart(grafik_hujan)

if "total_serangan" in df_grafik.columns:
    st.subheader("Total Luas Serangan per Triwulan")
    st.caption("Satuan: hektare (ha). Sumbu X = Triwulan, Sumbu Y = Total luas serangan OPT.")

    grafik_serangan = df_grafik[["triwulan", "total_serangan"]].copy()
    grafik_serangan = grafik_serangan.groupby("triwulan", as_index=True)["total_serangan"].sum()
    grafik_serangan = grafik_serangan.reindex([1, 2, 3, 4]).fillna(0)

    st.bar_chart(grafik_serangan)

# =====================================================
# DATA DETAIL
# =====================================================
st.subheader("Data Detail Triwulan Dipilih")

kolom_tampil = [
    "provinsi", "tahun", "triwulan", "komoditas", "opt",
    "tmax_rata", "tmin_rata", "suhu_rata", "hujan_total",
    "gdd_triwulan_dashboard", "gdd_akumulasi_dashboard"
]

if "total_serangan" in df_pilih.columns:
    kolom_tampil.append("total_serangan")

kolom_tampil = [kolom for kolom in kolom_tampil if kolom in df_pilih.columns]

st.dataframe(df_pilih[kolom_tampil], use_container_width=True)

# =====================================================
# DOWNLOAD HASIL ANALISIS
# =====================================================
st.subheader("Download Hasil Analisis")

csv_detail = df_pilih[kolom_tampil].to_csv(index=False).encode("utf-8-sig")

st.download_button(
    label="Download Data Detail Triwulan Dipilih",
    data=csv_detail,
    file_name=f"detail_{provinsi}_{tahun}_triwulan_{int(triwulan)}_{komoditas}_{opt}.csv",
    mime="text/csv"
)

if "df_ringkasan_tampil" in locals():
    csv_ringkasan = df_ringkasan_tampil.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="Download Ringkasan Semua Provinsi",
        data=csv_ringkasan,
        file_name=f"ringkasan_semua_provinsi_{tahun}_triwulan_{int(triwulan)}_{komoditas}_{opt}.csv",
        mime="text/csv"
    )

# =====================================================
# METODOLOGI SINGKAT
# =====================================================
with st.expander("Metodologi Perhitungan"):
    st.markdown("""
    **Konsep utama dashboard:**

    Dashboard ini memakai pendekatan risiko OPT berdasarkan karakter organisme, bukan lagi hanya ambang GDD umum.

    **1. Model GDD siklus hidup OPT**

    Dipakai untuk OPT serangga yang memiliki referensi degree-day spesifik.  
    Contoh: PBKo / penggerek buah kopi.

    Rumus dasar:

    `GDD = ((Tmax + Tmin) / 2 - Tbase) x jumlah hari`

    Jika hasil GDD bernilai negatif, maka nilainya dianggap 0.

    Pada model ini, status risiko dibaca sebagai kedekatan akumulasi GDD terhadap fase merusak:

    - **Hijau**: belum mendekati fase merusak.
    - **Kuning**: mendekati fase merusak.
    - **Merah**: sudah mencapai atau melewati fase merusak.

    **2. Model GDD historis serangga**

    Dipakai untuk OPT serangga yang belum memiliki angka GDD fase merusak spesifik di dashboard.  
    Status ditentukan dari posisi GDD terhadap pola historis dataset OPT yang sama.

    **3. Model kondisi lingkungan penyakit**

    Dipakai untuk penyakit/jamur seperti karat, busuk akar, dan Ganoderma.  
    Status lebih menekankan kombinasi suhu dan curah hujan sebagai kondisi pendukung penyakit, bukan fase hidup serangga.

    **4. Model monitoring historis/lapangan**

    Dipakai untuk OPT vertebrata seperti tikus atau babi.  
    GDD tidak digunakan sebagai indikator utama karena pola serangan lebih dipengaruhi riwayat serangan, kondisi lahan, dan monitoring lapangan.

    **Prediksi triwulan berikutnya** dihitung menggunakan rata-rata historis GDD pada triwulan yang sama dalam dataset.

    **Satuan grafik:**

    - Grafik Akumulasi GDD: satuan GDD kumulatif.
    - Grafik Curah Hujan: milimeter (mm).
    - Grafik Total Luas Serangan: hektare (ha).
    """)
st.markdown("""
<div class="footer-note">
    Dashboard Monitoring OPT Sumatera berbasis data suhu, curah hujan, dan serangan OPT.
</div>
""", unsafe_allow_html=True)
