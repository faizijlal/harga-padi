import pandas as pd
import streamlit as st
import plotly.express as px

# Load Dataset
data = pd.read_csv('datahargapadijawa.csv', sep=';')

# Konversi kolom 'Tanggal' ke format datetime
data['Tanggal'] = pd.to_datetime(data['Tanggal'], dayfirst=True)

# Ubah nilai 0 menjadi NaN (kosong) untuk semua kolom numerik
data.replace(0, pd.NA, inplace=True)

# Mapping bulan dalam bahasa Inggris ke bahasa Indonesia
bulan_mapping = {
    "January": "Januari", "February": "Februari", "March": "Maret",
    "April": "April", "May": "Mei", "June": "Juni",
    "July": "Juli", "August": "Agustus", "September": "September",
    "October": "Oktober", "November": "November", "December": "Desember"
}

# Tambahkan kolom 'month', 'day', dan 'year' untuk filtering
data['month'] = data['Tanggal'].dt.month_name().map(bulan_mapping)  # Nama bulan dalam bahasa Indonesia
data['day'] = data['Tanggal'].dt.day
data['year'] = data['Tanggal'].dt.year

# Ubah dataset menjadi long format untuk memudahkan visualisasi
data_long = data.melt(id_vars=['Tanggal', 'month', 'day', 'year'], var_name='province', value_name='price')

# Filter data untuk provinsi di Pulau Jawa
java_provinces = ['Banten', 'DKI Jakarta', 'Jawa Barat', 'Jawa Tengah', 'DI Yogyakarta', 'Jawa Timur']
data_long = data_long[data_long['province'].isin(java_provinces)]

# Filter data hanya untuk tahun 2021-2024
data_long = data_long[data_long['year'].isin([2021, 2022, 2023, 2024])]

# Streamlit app
st.title("Analisis Harga Rata-rata Padi di Pulau Jawa")

# Month Selection dengan urutan bulan
month_order = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 
               'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
selected_month = st.selectbox("Pilih Bulan", options=month_order)

# Region Selection
selected_province = st.selectbox("Pilih Provinsi", options=java_provinces)

# Filter data by selected month and province
filtered_data = data_long[(data_long['month'] == selected_month) & (data_long['province'] == selected_province)]

# Periksa apakah data tidak kosong
if filtered_data.empty:
    st.warning(f"Tidak ada data untuk {selected_province} pada bulan {selected_month}.")
    st.stop()

# Line chart for daily price changes
graph = px.line(
    filtered_data,
    x='day',
    y='price',
    color='year',
    title=f"Perubahan Harga Harian Padi di {selected_province} pada Bulan {selected_month} (Tahun 2021-2024)",
    labels={'day': 'Tanggal', 'price': 'Harga (Rp)', 'year': 'Tahun'},
    template="plotly"
)

# Atur sumbu x untuk menampilkan tanggal dari 1 sampai akhir bulan
graph.update_xaxes(tickmode='linear', tick0=1, dtick=1)

# Tampilkan grafik
st.plotly_chart(graph)

# Hitung rata-rata harga
average_price = filtered_data['price'].mean()

# Display prediksi harga
st.subheader(f"Prediksi Harga Padi di {selected_province} pada Bulan {selected_month}")
st.markdown(
    f"""
    <div style="text-align: center;">
        <h3 style="color: green; font-size: 60px;"><b>Rp {average_price:,.0f}</b></h3>
    </div>
    """,
    unsafe_allow_html=True
)
