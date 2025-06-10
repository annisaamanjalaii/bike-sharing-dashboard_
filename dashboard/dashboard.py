import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set judul halaman
st.set_page_config(page_title="Dashboard Analisis Data Bike Sharing", layout="centered")

st.title("Dashboard Analisis Data Bike Sharing")
st.write("Dashboard ini menyajikan insight dari data peminjaman sepeda berdasarkan dataset `main_data.csv`.")

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    return df

data = load_data()

# Tampilkan kolom
st.subheader("Kolom dalam Dataset")
st.write(data.columns.tolist())

# Cek kolom 'hr'
if 'hr' not in data.columns:
    st.error("Kolom 'hr' tidak ditemukan dalam dataset. Periksa file hour.csv.")
else:
    st.subheader("Data Awal (10 baris)")
    st.dataframe(data.head(10))

    # Sidebar Filter
    st.sidebar.header("Filter Data")

    # Filter Jam
    jam = st.sidebar.slider("Pilih rentang jam", 0, 23, (0, 23))

    # Filter Cuaca
    cuaca_dict = {
        1: 'Clear',
        2: 'Mist',
        3: 'Light Rain',
        4: 'Heavy Rain'
    }
    pilihan_cuaca = st.sidebar.multiselect(
        "Pilih kondisi cuaca", options=list(cuaca_dict.keys()),
        format_func=lambda x: cuaca_dict[x],
        default=list(cuaca_dict.keys())
    )

    # Filter data
    filtered = data[
        (data['hr'] >= jam[0]) & (data['hr'] <= jam[1]) &
        (data['weathersit'].isin(pilihan_cuaca))
    ]

    st.subheader("Data Setelah Filter")
    st.write(f"Jumlah baris data: {filtered.shape[0]}")
    st.dataframe(filtered.head(10))

    # Pertanyaan 1: Kapan waktu terbaik menambah armada?
    st.subheader("Waktu Terbaik Menambah Armada Sepeda")

    permintaan_per_jam = filtered.groupby('hr')['cnt'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=permintaan_per_jam, x='hr', y='cnt', marker='o', ax=ax)
    ax.set_title("Total Peminjaman Sepeda per Jam")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Jumlah Peminjaman")
    ax.set_xticks(range(0, 24))
    ax.grid(True)
    st.pyplot(fig)

    # Pertanyaan 2: Pengaruh cuaca
    st.subheader("Pengaruh Kondisi Cuaca terhadap Peminjaman Sepeda")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=filtered, x='weathersit', y='cnt', ax=ax)
    ax.set_title("Peminjaman Berdasarkan Kondisi Cuaca")
    ax.set_xlabel("Cuaca")
    ax.set_ylabel("Jumlah Peminjaman")
    ax.set_xticklabels([cuaca_dict[i] for i in sorted(filtered['weathersit'].unique())], rotation=25)
    ax.grid(True)
    st.pyplot(fig)

    # Pertanyaan 3: Perbandingan casual vs registered
    st.subheader("Perbandingan Pola Peminjaman Casual vs Registered")

    per_jam = filtered.groupby('hr')[['casual', 'registered']].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    per_jam.set_index('hr')[['casual', 'registered']].plot(kind='bar', ax=ax)
    ax.set_title("Perbandingan Jumlah Peminjaman Antara Casual dan Registered")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Jumlah Peminjaman")
    ax.legend(["Casual", "Registered"])
    ax.grid(True)
    st.pyplot(fig)

    # Kesimpulan
    st.markdown("---")
    st.header("📌 Kesimpulan")
    st.write("""
    - Peminjaman tertinggi terjadi antara jam 17:00 hingga 19:00 — waktu ideal untuk menambah armada.
    - Cuaca cerah mendorong peminjaman lebih tinggi dibanding cuaca buruk.
    - Pengguna registered cenderung meminjam saat jam sibuk (kerja), sedangkan pengguna casual lebih fleksibel.
    """)