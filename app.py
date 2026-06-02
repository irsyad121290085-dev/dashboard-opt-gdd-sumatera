import streamlit as st
import pandas as pd

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
   GLOBAL
========================= */
.stApp {
    background: linear-gradient(135deg, #f3f7f1 0%, #eef5ec 45%, #ffffff 100%);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1180px;
}

h1, h2, h3 {
    color: #152536;
}

hr {
    border: none;
    border-top: 1px solid #dfe8dc;
    margin: 26px 0;
}

/* =========================
   SIDEBAR
========================= */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #edf6ef 0%, #f8faf7 100%);
    border-right: 1px solid #dbe7d7;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #143d2b;
}

section[data-testid="stSidebar"] label {
    color: #263238;
    font-weight: 600;
}

/* =========================
   HEADER
========================= */
.header-card {
    background:
        radial-gradient(circle at top left, rgba(255,255,255,0.20), transparent 32%),
        linear-gradient(135deg, #0f3d2e 0%, #1b5e3f 50%, #2d6a4f 100%);
    padding: 38px 30px;
    border-radius: 26px;
    color: white;
    text-align: center;
    margin-bottom: 32px;
    box-shadow: 0 16px 38px rgba(15, 61, 46, 0.22);
}

.header-card h1 {
    margin: 0;
    color: white;
    font-size: 36px;
    font-weight: 800;
    letter-spacing: 1px;
}

.header-card p {
    margin-top: 14px;
    font-size: 17px;
    color: #e6f4ec;
}

/* =========================
   INFO BOX
========================= */
.info-box {
    background: rgba(255,255,255,0.95);
    padding: 22px 24px;
    border-radius: 18px;
    border-left: 7px solid #2d6a4f;
    margin-bottom: 22px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
}

.info-box b {
    color: #143d2b;
}

.small-note {
    font-size: 13px;
    color: #6c757d;
}

/* =========================
   STATUS CARD
========================= */
.status-card {
    padding: 26px;
    border-radius: 22px;
    font-size: 26px;
    font-weight: 800;
    text-align: center;
    margin: 20px 0 26px 0;
    box-shadow: 0 10px 28px rgba(0,0,0,0.08);
}

.status-green {
    background: linear-gradient(135deg, #d8f3dc, #b7e4c7);
    color: #0b4228;
    border: 1px solid #95d5b2;
}

.status-yellow {
    background: linear-gradient(135deg, #fff3cd, #ffe69c);
    color: #7a5200;
    border: 1px solid #ffda6a;
}

.status-red {
    background: linear-gradient(135deg, #f8d7da, #f1aeb5);
    color: #7f1d1d;
    border: 1px solid #ea868f;
}

/* =========================
   STREAMLIT METRIC
========================= */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.95);
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.055);
    border: 1px solid #edf2ea;
}

[data-testid="stMetricLabel"] {
    color: #52675a;
    font-weight: 700;
}

[data-testid="stMetricValue"] {
    color: #143d2b;
}

/* =========================
   CHART / DATAFRAME
========================= */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 8px 22px rgba(0,0,0,0.04);
}

.intervention-box {
    background: rgba(255,255,255,0.95);
    padding: 22px 26px;
    border-radius: 18px;
    border: 1px solid #e3eadf;
    box-shadow: 0 8px 24px rgba(0,0,0,0.055);
    margin-bottom: 20px;
}

.footer-note {
    color: #667085;
    font-size: 13px;
    text-align: center;
    margin-top: 30px;
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

komoditas_list = sorted(df_tahun["komoditas"].dropna().unique())
komoditas = st.sidebar.selectbox("Pilih Komoditas", komoditas_list)

df_komoditas = df_tahun[df_tahun["komoditas"] == komoditas]

opt_list = sorted(df_komoditas["opt"].dropna().unique())
opt = st.sidebar.selectbox("Pilih OPT", opt_list)

df_pilih = df_komoditas[df_komoditas["opt"] == opt].copy()

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
st.subheader(f"{provinsi} | {int(tahun)} | {komoditas} | {opt}")

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
col2.metric("Triwulan Terakhir", int(data_akhir["triwulan"]))
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
# PREDIKSI GDD TRIWULAN BERIKUTNYA
# =====================================================
st.subheader("Prediksi Triwulan Berikutnya")

triwulan_saat_ini = int(data_akhir["triwulan"])

if triwulan_saat_ini < 4:
    triwulan_prediksi = triwulan_saat_ini + 1
else:
    triwulan_prediksi = 1

data_historis_next = df[
    (df["provinsi"] == provinsi) &
    (df["komoditas"] == komoditas) &
    (df["opt"] == opt) &
    (df["triwulan"] == triwulan_prediksi)
].copy()

if not data_historis_next.empty:
    data_historis_next["gdd_prediksi_basis"] = (
        (((data_historis_next["tmax_rata"] + data_historis_next["tmin_rata"]) / 2) - tbase)
        * data_historis_next["jumlah_hari"]
    ).clip(lower=0)

    rata_gdd_next = data_historis_next["gdd_prediksi_basis"].mean()
    prediksi_akumulasi = gdd_akhir + rata_gdd_next
    status_prediksi = status_dari_gdd(prediksi_akumulasi)

    colp1, colp2, colp3 = st.columns(3)

    colp1.metric("Prediksi Triwulan", int(triwulan_prediksi))
    colp2.metric("Tambahan GDD Prediksi", f"{rata_gdd_next:.2f}")
    colp3.metric("Prediksi Akumulasi GDD", f"{prediksi_akumulasi:.2f}")

    if status_prediksi == "Merah":
        st.error("Prediksi Status: MERAH - Risiko tinggi pada triwulan berikutnya")
    elif status_prediksi == "Kuning":
        st.warning("Prediksi Status: KUNING - Perlu kewaspadaan pada triwulan berikutnya")
    else:
        st.success("Prediksi Status: HIJAU - Risiko relatif rendah pada triwulan berikutnya")

    st.caption("Prediksi dihitung dari rata-rata historis GDD pada triwulan yang sama dalam dataset.")
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

grafik_gdd = df_pilih[["triwulan", "gdd_akumulasi_dashboard"]].copy()
grafik_gdd = grafik_gdd.groupby("triwulan", as_index=True)["gdd_akumulasi_dashboard"].mean()
st.line_chart(grafik_gdd)

st.subheader("Curah Hujan per Triwulan")

grafik_hujan = df_pilih[["triwulan", "hujan_total"]].copy()
grafik_hujan = grafik_hujan.groupby("triwulan", as_index=True)["hujan_total"].mean()
st.bar_chart(grafik_hujan)

if "total_serangan" in df_pilih.columns:
    st.subheader("Total Luas Serangan per Triwulan")

    grafik_serangan = df_pilih[["triwulan", "total_serangan"]].copy()
    grafik_serangan = grafik_serangan.groupby("triwulan", as_index=True)["total_serangan"].sum()
    st.bar_chart(grafik_serangan)

# =====================================================
# DATA DETAIL
# =====================================================
st.subheader("Data Detail")

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
    """)

st.markdown("""
<div class="footer-note">
    Dashboard Monitoring OPT Sumatera berbasis data suhu, curah hujan, dan serangan OPT.
</div>
""", unsafe_allow_html=True)
