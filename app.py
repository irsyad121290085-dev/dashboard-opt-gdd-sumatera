import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Dashboard OPT GDD Sumatera",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}

.header-card {
    background: linear-gradient(135deg, #1b4332, #2d6a4f);
    padding: 28px;
    border-radius: 18px;
    color: white;
    text-align: center;
    margin-bottom: 25px;
}

.header-card h1 {
    margin: 0;
    font-size: 34px;
}

.header-card p {
    margin-top: 8px;
    font-size: 16px;
}

.status-green {
    background-color: #d8f3dc;
    color: #1b4332;
    padding: 22px;
    border-radius: 16px;
    font-size: 24px;
    font-weight: bold;
    text-align: center;
}

.status-yellow {
    background-color: #fff3cd;
    color: #856404;
    padding: 22px;
    border-radius: 16px;
    font-size: 24px;
    font-weight: bold;
    text-align: center;
}

.status-red {
    background-color: #f8d7da;
    color: #842029;
    padding: 22px;
    border-radius: 16px;
    font-size: 24px;
    font-weight: bold;
    text-align: center;
}

.info-box {
    background-color: #f8f9fa;
    padding: 18px;
    border-radius: 14px;
    border-left: 6px solid #2d6a4f;
    margin-bottom: 18px;
}

.small-note {
    font-size: 13px;
    color: #6c757d;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================
st.markdown("""
<div class="header-card">
    <h1>🌿 DIGITAL MONITORING CARD OPT SUMATERA</h1>
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
st.sidebar.title("🔎 Filter Dashboard")

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
st.subheader(f"📍 {provinsi} | {int(tahun)} | {komoditas} | {opt}")

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
    st.markdown('<div class="status-red">🔴 MERAH - Risiko Tinggi</div>', unsafe_allow_html=True)
elif status == "Kuning":
    st.markdown('<div class="status-yellow">🟡 KUNING - Perlu Waspada</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-green">🟢 HIJAU - Relatif Aman</div>', unsafe_allow_html=True)

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
st.subheader("🔮 Prediksi Triwulan Berikutnya")

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
        st.error("🔴 Prediksi Status: MERAH - Risiko tinggi pada triwulan berikutnya")
    elif status_prediksi == "Kuning":
        st.warning("🟡 Prediksi Status: KUNING - Perlu kewaspadaan pada triwulan berikutnya")
    else:
        st.success("🟢 Prediksi Status: HIJAU - Risiko relatif rendah pada triwulan berikutnya")

    st.caption("Prediksi dihitung dari rata-rata historis GDD pada triwulan yang sama dalam dataset.")
else:
    st.info("Data historis untuk prediksi triwulan berikutnya belum tersedia.")

# =====================================================
# INTERVENSI UNTUK SEMUA KOMODITAS / OPT
# =====================================================
st.subheader("📋 Rekomendasi Intervensi")

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

st.markdown(intervensi_umum(komoditas, opt, status))

# =====================================================
# GRAFIK GDD
# =====================================================
st.subheader("📈 Grafik Akumulasi GDD per Triwulan")

fig_gdd = px.line(
    df_pilih,
    x="triwulan",
    y="gdd_akumulasi_dashboard",
    markers=True,
    title=f"Akumulasi GDD {opt} pada {komoditas} di {provinsi} Tahun {int(tahun)}"
)

fig_gdd.update_layout(
    xaxis_title="Triwulan",
    yaxis_title="Akumulasi GDD"
)

st.plotly_chart(fig_gdd, use_container_width=True)

# =====================================================
# GRAFIK HUJAN
# =====================================================
st.subheader("🌧️ Curah Hujan per Triwulan")

fig_hujan = px.bar(
    df_pilih,
    x="triwulan",
    y="hujan_total",
    title=f"Curah Hujan Triwulan di {provinsi} Tahun {int(tahun)}"
)

fig_hujan.update_layout(
    xaxis_title="Triwulan",
    yaxis_title="Curah Hujan"
)

st.plotly_chart(fig_hujan, use_container_width=True)

# =====================================================
# GRAFIK SERANGAN
# =====================================================
if "total_serangan" in df_pilih.columns:
    st.subheader("🐛 Total Luas Serangan per Triwulan")

    fig_serangan = px.bar(
        df_pilih,
        x="triwulan",
        y="total_serangan",
        title=f"Total Luas Serangan {opt} di {provinsi} Tahun {int(tahun)}"
    )

    fig_serangan.update_layout(
        xaxis_title="Triwulan",
        yaxis_title="Total Serangan (ha)"
    )

    st.plotly_chart(fig_serangan, use_container_width=True)

# =====================================================
# DATA DETAIL
# =====================================================
st.subheader("📄 Data Detail")

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
with st.expander("ℹ️ Metodologi Perhitungan"):
    st.markdown("""
    **Growing Degree Days (GDD)** dihitung menggunakan suhu maksimum dan minimum rata-rata triwulan.

    Rumus dasar:

    `GDD = ((Tmax + Tmin) / 2 - Tbase) × jumlah hari`

    Jika hasil GDD bernilai negatif, maka nilainya dianggap 0.

    **Status risiko:**

    - 🟢 **Hijau**: Akumulasi GDD masih rendah.
    - 🟡 **Kuning**: Akumulasi GDD mendekati ambang waspada.
    - 🔴 **Merah**: Akumulasi GDD mencapai atau melewati ambang bahaya.

    **Prediksi triwulan berikutnya** dihitung menggunakan rata-rata historis GDD pada triwulan yang sama dalam dataset.
    """)
