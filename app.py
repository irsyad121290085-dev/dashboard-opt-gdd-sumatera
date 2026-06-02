import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard OPT GDD Sumatera",
    layout="wide"
)

st.title("🌿 Dashboard OPT GDD Sumatera")
st.write("Digital Monitoring Card berbasis GDD dan curah hujan.")

@st.cache_data
def load_data():
    return pd.read_csv("dataset_final_dashboard_opt_gdd_sumatera.csv")

df = load_data()

st.success("✅ Data berhasil dibaca!")

st.write("Jumlah baris:", len(df))
st.write("Jumlah kolom:", len(df.columns))

st.subheader("Kolom Dataset")
st.write(df.columns.tolist())

st.subheader("Preview Data")
st.dataframe(df.head(20))

st.sidebar.header("Filter Dashboard")

provinsi = st.sidebar.selectbox(
    "Pilih Provinsi",
    sorted(df["provinsi"].dropna().unique())
)

df_prov = df[df["provinsi"] == provinsi]

tahun = st.sidebar.selectbox(
    "Pilih Tahun",
    sorted(df_prov["tahun"].dropna().unique())
)

df_tahun = df_prov[df_prov["tahun"] == tahun]

komoditas = st.sidebar.selectbox(
    "Pilih Komoditas",
    sorted(df_tahun["komoditas"].dropna().unique())
)

df_komoditas = df_tahun[df_tahun["komoditas"] == komoditas]

opt = st.sidebar.selectbox(
    "Pilih OPT",
    sorted(df_komoditas["opt"].dropna().unique())
)

df_pilih = df_komoditas[df_komoditas["opt"] == opt]

st.subheader(f"📍 {provinsi} | {tahun} | {komoditas} | {opt}")

st.dataframe(df_pilih)

if "status" in df_pilih.columns:
    status_akhir = df_pilih["status"].dropna().iloc[-1]

    if str(status_akhir).lower() == "merah":
        st.error("🔴 Status: MERAH - Risiko tinggi")
    elif str(status_akhir).lower() == "kuning":
        st.warning("🟡 Status: KUNING - Perlu waspada")
    elif str(status_akhir).lower() == "hijau":
        st.success("🟢 Status: HIJAU - Relatif aman")
    else:
        st.info(f"Status: {status_akhir}")

if "intervensi" in df_pilih.columns:
    st.subheader("📋 Rekomendasi Intervensi")
    st.write(df_pilih["intervensi"].dropna().iloc[-1])
