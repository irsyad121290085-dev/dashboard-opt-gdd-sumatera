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
    background:
        radial-gradient(circle at top left, rgba(45, 106, 79, 0.16), transparent 32%),
        radial-gradient(circle at bottom right, rgba(183, 228, 199, 0.32), transparent 35%),
        linear-gradient(135deg, #f6faf5 0%, #eef7ef 45%, #ffffff 100%);
}

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 3rem;
    max-width: 1160px;
}

h1, h2, h3 {
    color: #102a1f;
    letter-spacing: -0.3px;
}

hr {
    border: none;
    border-top: 1px solid rgba(45, 106, 79, 0.15);
    margin: 30px 0;
}

/* =========================
   SIDEBAR
========================= */
section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #eaf5ec 0%, #f8fbf7 100%);
    border-right: 1px solid rgba(45, 106, 79, 0.18);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #103d2c;
    font-weight: 800;
}

section[data-testid="stSidebar"] label {
    color: #244538;
    font-weight: 700;
    font-size: 14px;
}

section[data-testid="stSidebar"] [data-baseweb="select"] {
    border-radius: 14px;
}

/* =========================
   HEADER CARD
========================= */
.header-card {
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(circle at 8% 15%, rgba(255,255,255,0.25), transparent 26%),
        radial-gradient(circle at 90% 20%, rgba(183,228,199,0.22), transparent 26%),
        linear-gradient(135deg, #0b2f22 0%, #145038 48%, #2d6a4f 100%);
    padding: 46px 34px;
    border-radius: 30px;
    color: white;
    text-align: center;
    margin-bottom: 38px;
    box-shadow:
        0 28px 60px rgba(15, 61, 46, 0.26),
        inset 0 1px 0 rgba(255,255,255,0.18);
}

.header-card::after {
    content: "";
    position: absolute;
    width: 260px;
    height: 260px;
    border-radius: 50%;
    right: -80px;
    bottom: -120px;
    background: rgba(255,255,255,0.08);
}

.header-card h1 {
    margin: 0;
    color: white;
    font-size: 38px;
    font-weight: 900;
    letter-spacing: 2.5px;
}

.header-card p {
    margin-top: 16px;
    font-size: 17px;
    color: #eaf7ef;
    font-weight: 500;
}

/* =========================
   INFO BOX
========================= */
.info-box {
    background: rgba(255,255,255,0.82);
    backdrop-filter: blur(10px);
    padding: 24px 26px;
    border-radius: 22px;
    border-left: 7px solid #2d6a4f;
    margin-bottom: 24px;
    box-shadow:
        0 18px 40px rgba(18, 64, 43, 0.08),
        inset 0 1px 0 rgba(255,255,255,0.8);
}

.info-box b {
    color: #103d2c;
}

.small-note {
    display: inline-block;
    margin-top: 8px;
    font-size: 13px;
    color: #63776c;
}

/* =========================
   STATUS CARD
========================= */
.status-card {
    padding: 30px;
    border-radius: 26px;
    font-size: 28px;
    font-weight: 900;
    text-align: center;
    margin: 24px 0 30px 0;
    box-shadow: 0 20px 46px rgba(0,0,0,0.10);
    letter-spacing: 0.6px;
}

.status-green {
    background:
        linear-gradient(135deg, #d8f3dc, #b7e4c7);
    color: #073b22;
    border: 1px solid #95d5b2;
}

.status-yellow {
    background:
        linear-gradient(135deg, #fff3cd, #ffe08a);
    color: #704c00;
    border: 1px solid #ffd166;
}

.status-red {
    background:
        linear-gradient(135deg, #f8d7da, #f1aeb5);
    color: #741616;
    border: 1px solid #ea868f;
}

/* =========================
   METRIC CARDS
========================= */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.86);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 22px;
    box-shadow:
        0 14px 34px rgba(18, 64, 43, 0.08),
        inset 0 1px 0 rgba(255,255,255,0.8);
    border: 1px solid rgba(45, 106, 79, 0.10);
}

[data-testid="stMetricLabel"] {
    color: #5c7065;
    font-weight: 800;
}

[data-testid="stMetricValue"] {
    color: #103d2c;
    font-weight: 900;
}

/* =========================
   ALERTS
========================= */
[data-testid="stAlert"] {
    border-radius: 18px;
    border: none;
    box-shadow: 0 10px 26px rgba(0,0,0,0.06);
}

/* =========================
   INTERVENTION BOX
========================= */
.intervention-box {
    background: rgba(255,255,255,0.88);
    backdrop-filter: blur(10px);
    padding: 26px 30px;
    border-radius: 24px;
    border: 1px solid rgba(45, 106, 79, 0.12);
    box-shadow:
        0 18px 42px rgba(18, 64, 43, 0.08),
        inset 0 1px 0 rgba(255,255,255,0.8);
    margin-bottom: 24px;
}

/* =========================
   CHART / DATAFRAME
========================= */
[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 16px 36px rgba(18, 64, 43, 0.08);
    border: 1px solid rgba(45, 106, 79, 0.10);
}

[data-testid="stVerticalBlock"] > div {
    border-radius: 18px;
}

.footer-note {
    color: #667085;
    font-size: 13px;
    text-align: center;
    margin-top: 34px;
}
</style>
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
# PARAMETER UMUM KOMODITAS
# =====================================================
parameter_umum = {
    "Karet": {
        "tbase": 10,
        "gdd_kuning": 1200,
        "gdd_merah": 2500
    },
    "Kelapa Sawit": {
        "tbase": 12,
        "gdd_kuning": 1000,
        "gdd_merah": 2200
    },
    "Kopi": {
        "tbase": 15,
        "gdd_kuning": 900,
        "gdd_merah": 1800
    }
}

def ambil_parameter_umum(nama_komoditas):
    return parameter_umum.get(nama_komoditas, {
        "tbase": 10,
        "gdd_kuning": 1200,
        "gdd_merah": 2500
    })

param = ambil_parameter_umum(komoditas)

tbase = param["tbase"]
gdd_kuning = param["gdd_kuning"]
gdd_merah = param["gdd_merah"]

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
    Ambang Kuning: <b>{gdd_kuning}</b><br>
    Ambang Merah: <b>{gdd_merah}</b><br>
    <span class="small-note">
    Catatan: Jika parameter spesifik OPT belum tersedia, sistem memakai parameter umum berdasarkan komoditas.
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

def warna_status(status):
    if status == "Merah":
        return [220, 53, 69, 180]
    elif status == "Kuning":
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
    status_prediksi = status_dari_gdd(prediksi_akumulasi)

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
# NARASI OTOMATIS HASIL ANALISIS
# =====================================================
st.subheader("Analisis")

def buat_narasi(status, provinsi, tahun, triwulan, komoditas, opt, gdd_akhir, tbase, hujan_total):
    if status == "Hijau":
        makna = (
            "Akumulasi GDD masih berada di bawah ambang waspada, sehingga kondisi "
            "relatif belum mendukung peningkatan risiko OPT secara signifikan."
        )
        tindakan = (
            "Tindakan yang disarankan adalah monitoring rutin, pencatatan gejala awal, "
            "dan menjaga sanitasi lahan atau kebun."
        )

    elif status == "Kuning":
        makna = (
            "Akumulasi GDD telah mendekati ambang waspada, sehingga kondisi mulai "
            "perlu diperhatikan karena potensi perkembangan OPT dapat meningkat."
        )
        tindakan = (
            "Tindakan yang disarankan adalah meningkatkan frekuensi pengamatan lapangan, "
            "memeriksa bagian tanaman yang rentan terserang, dan menyiapkan pengendalian terpadu."
        )

    else:
        makna = (
            "Akumulasi GDD telah mencapai atau melewati ambang bahaya, sehingga kondisi "
            "berpotensi mendukung peningkatan risiko serangan OPT."
        )
        tindakan = (
            "Tindakan yang disarankan adalah melakukan pengamatan intensif, identifikasi tingkat serangan, "
            "sanitasi lahan, dan pengendalian terpadu sesuai kondisi lapangan."
        )

    narasi = f"""
    Berdasarkan hasil analisis pada **Provinsi {provinsi}** tahun **{int(tahun)}** 
    **Triwulan {int(triwulan)}**, komoditas **{komoditas}** dengan OPT **{opt}** 
    berada pada status **{status}**.

    Nilai akumulasi GDD yang diperoleh adalah **{gdd_akhir:.2f} GDD** dengan 
    nilai Tbase yang digunakan sebesar **{tbase} °C**. Curah hujan pada periode ini 
    tercatat sebesar **{hujan_total:.2f} mm**.

    {makna}

    {tindakan}
    """

    return narasi

narasi_hasil = buat_narasi(
    status=status,
    provinsi=provinsi,
    tahun=tahun,
    triwulan=triwulan,
    komoditas=komoditas,
    opt=opt,
    gdd_akhir=gdd_akhir,
    tbase=tbase,
    hujan_total=data_akhir["hujan_total"]
)

st.markdown(narasi_hasil)
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

st.markdown(
    f"""
    <div class="intervention-box">
    {intervensi_umum(komoditas, opt, status)}
    </div>
    """,
    unsafe_allow_html=True
)

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
    **Growing Degree Days (GDD)** dihitung menggunakan suhu maksimum dan minimum rata-rata triwulan.

    Rumus dasar:

    `GDD = ((Tmax + Tmin) / 2 - Tbase) × jumlah hari`

    Jika hasil GDD bernilai negatif, maka nilainya dianggap 0.

    **Status risiko:**

    - **Hijau**: Akumulasi GDD masih rendah.
    - **Kuning**: Akumulasi GDD mendekati ambang waspada.
    - **Merah**: Akumulasi GDD mencapai atau melewati ambang bahaya.

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
