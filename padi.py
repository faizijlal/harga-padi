import pandas as pd
import streamlit as st
import plotly.express as px

# Load Dataset
data = pd.read_csv('datahargapadijawa.csv', sep=';')

# Konversi kolom 'Tanggal' ke format datetime
data['Tanggal'] = pd.to_datetime(data['Tanggal'], dayfirst=True)

# Tambahkan kolom 'month', 'day', dan 'year'
data['month'] = data['Tanggal'].dt.strftime('%B')  # Nama bulan
data['day'] = data['Tanggal'].dt.day               # Tanggal (1, 2, ..., 31)
data['year'] = data['Tanggal'].dt.year             # Tahun

# Ubah data menjadi long format
data_long = data.melt(id_vars=['Tanggal', 'month', 'day', 'year'], var_name='province', value_name='price')

# Abaikan nilai 0 pada kolom 'price'
data_long = data_long[data_long['price'] > 0]

# Filter data untuk provinsi di Pulau Jawa
java_provinces = ['Banten', 'DKI Jakarta', 'Jawa Barat', 'Jawa Tengah', 'DI Yogyakarta', 'Jawa Timur']
data_long = data_long[data_long['province'].isin(java_provinces)]

# Streamlit app
st.title("Analisis Harga Padi di Pulau Jawa Berbasis Big Data")

# Pilihan Bulan dan Provinsi
selected_month = st.selectbox("Pilih Bulan", options=sorted(data_long['month'].unique()))
selected_province = st.selectbox("Pilih Provinsi", options=java_provinces)

# Filter data berdasarkan pilihan bulan dan provinsi
filtered_data = data_long[(data_long['month'] == selected_month) & (data_long['province'] == selected_province)]

# Jika tidak ada data
if filtered_data.empty:
    st.warning(f"Tidak ada data untuk {selected_province} pada bulan {selected_month}.")
    st.stop()

# Grafik perubahan harga harian dengan garis untuk setiap tahun
fig = px.line(
    filtered_data,
    x='day',
    y='price',
    color='year',
    title=f"Perubahan Harga Harian Padi di {selected_province} pada Bulan {selected_month}",
    labels={'day': 'Tanggal', 'price': 'Harga (Rp)', 'year': 'Tahun'},
    markers=True
)
fig.update_layout(xaxis=dict(tickmode='linear', tick0=1, dtick=1))  # Set setiap hari di sumbu x
st.plotly_chart(fig)

# Hitung rata-rata harga
average_price = filtered_data['price'].mean()
formatted_average_price = f"Rp {average_price:,.0f}".replace(',', '.')

# Tampilkan rata-rata harga
st.subheader(f"Rata-rata Harga Padi di {selected_province} pada Bulan {selected_month}")
st.markdown(f"<h2 style='color:green;'>Rata-rata harga: {formatted_average_price}</h2>", unsafe_allow_html=True)
