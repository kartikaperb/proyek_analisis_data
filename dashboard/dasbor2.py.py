import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi dasar Streamlit
st.set_page_config(page_title="Analisis PM2.5", layout="centered")

# Judul Dashboard
st.title("🌍 Analisis Kualitas Udara: Tren PM2.5")

# Baca dataset langsung dari GitHub
url = "https://raw.githubusercontent.com/kartikaperb/proyek_analisis_data/main/PRSA_Data_Tiantan_20130301-20170228.csv"

try:
    # Load dataset
    df = pd.read_csv(url)
    st.success("✅ Dataset berhasil dimuat dari GitHub!")

    # Pastikan kolom yang diperlukan tersedia
    required_cols = {'year', 'month', 'day', 'hour', 'PM2.5'}
    if not required_cols.issubset(df.columns):
        st.error("Dataset tidak memiliki kolom yang diperlukan.")
    else:
        # Konversi waktu ke datetime
        df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
        df['year'] = df['datetime'].dt.year

        # Tambahkan kolom 'season' berdasarkan bulan
        season_mapping = {12: "Winter", 1: "Winter", 2: "Winter",
                          3: "Spring", 4: "Spring", 5: "Spring",
                          6: "Summer", 7: "Summer", 8: "Summer",
                          9: "Autumn", 10: "Autumn", 11: "Autumn"}
        df['season'] = df['month'].map(season_mapping)

        # Preview Data
        st.write("### 📊 Data Preview")
        st.dataframe(df.head())

        # **Analisis Tren Tahunan PM2.5**
        st.write("### 📈 Tren PM2.5 dari Tahun ke Tahun")

        # Hitung rata-rata tahunan PM2.5
        pm25_yearly = df.groupby('year')['PM2.5'].mean()

        # Plot dengan Seaborn
        plt.figure(figsize=(10, 5))
        sns.lineplot(x=pm25_yearly.index, y=pm25_yearly.values, marker='o', label="PM2.5 per Tahun", color='blue')

        # Tambahkan garis tren (moving average 3 tahun)
        pm25_yearly_smooth = pm25_yearly.rolling(window=3).mean()
        sns.lineplot(x=pm25_yearly.index, y=pm25_yearly_smooth, linestyle='dashed', label="Tren 3 Tahun", color='red')

        # Tambahkan label
        plt.title("Tren PM2.5 dari Tahun ke Tahun")
        plt.xlabel("Tahun")
        plt.ylabel("Konsentrasi PM2.5 (µg/m³)")
        plt.legend()
        plt.grid(True)

        # Tampilkan di Streamlit
        st.pyplot(plt)

        # **Analisis otomatis**
        latest_year = pm25_yearly.index.max()
        earliest_year = pm25_yearly.index.min()
        diff_pm25 = pm25_yearly[latest_year] - pm25_yearly[earliest_year]

        # Menampilkan hasil analisis
        st.write("### 📌 Analisis Singkat:")
        if diff_pm25 > 0:
            st.warning(
                f"⚠️ **Kualitas udara memburuk!** Konsentrasi PM2.5 meningkat sebesar {diff_pm25:.2f} µg/m³ dari {earliest_year} ke {latest_year}.")
            st.write("""
            - Peningkatan ini bisa disebabkan oleh peningkatan aktivitas industri, kendaraan bermotor, atau pembakaran biomassa.
            - Faktor cuaca seperti kurangnya hujan juga bisa memperburuk polusi udara.
            - Kebijakan pengendalian emisi yang kurang efektif dapat menyebabkan tren meningkat.
            """)
        else:
            st.success(
                f"✅ **Kualitas udara membaik!** Konsentrasi PM2.5 menurun sebesar {-diff_pm25:.2f} µg/m³ dari {earliest_year} ke {latest_year}.")
            st.write("""
            - Penurunan ini mungkin disebabkan oleh kebijakan lingkungan yang lebih ketat, seperti pengurangan kendaraan berbahan bakar fosil dan pembatasan emisi industri.
            - Program penghijauan dan peningkatan transportasi umum juga bisa membantu mengurangi polusi udara.
            """)

        # **Tombol Explanation**
        if st.button("🔍 Explanation: Mengapa PM2.5 Penting?"):
            st.write("""
            - **PM2.5 (Particulate Matter 2.5)** adalah partikel udara yang sangat kecil (diameter < 2.5 µm) yang dapat masuk ke dalam paru-paru dan menyebabkan masalah kesehatan.
            - Paparan PM2.5 yang tinggi dikaitkan dengan penyakit pernapasan, kardiovaskular, dan bahkan kematian dini.
            - Polusi udara yang tinggi juga bisa berdampak pada perubahan iklim dan berkurangnya kualitas hidup masyarakat perkotaan.
            """)

        # **Distribusi PM2.5 Berdasarkan Musim**
        st.write("### 📊 Distribusi PM2.5 Berdasarkan Musim")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.boxplot(x='season', y='PM2.5', data=df, ax=ax, palette="coolwarm")
        ax.set_xlabel("Musim")
        ax.set_ylabel("PM2.5 (µg/m³)")
        ax.set_title("Distribusi PM2.5 Berdasarkan Musim")
        st.pyplot(fig)

        # **Tombol Penjelasan Musiman**
        if st.button("🔍 Explanation: Musim dan PM2.5"):
            st.write("""
            - Polusi udara bisa berubah sesuai musim. Biasanya, musim dingin memiliki tingkat PM2.5 lebih tinggi.
            - Hal ini disebabkan oleh inversi suhu yang menjebak polutan di permukaan.
            - Musim hujan cenderung memiliki PM2.5 lebih rendah karena curah hujan membantu membersihkan udara.
            - Musim kemarau sering memiliki PM2.5 lebih tinggi karena debu dan polusi dari kebakaran lahan atau transportasi meningkat.
            """)

        # **Kesimpulan**
        st.write("### 📌 Kesimpulan")
        st.write("""
        - Secara keseluruhan, kualitas udara mengalami perubahan dari tahun ke tahun dengan pola fluktuasi.
        - Tren menunjukkan faktor-faktor eksternal seperti kebijakan lingkungan dan perubahan iklim mempengaruhi konsentrasi PM2.5.
        - Perubahan musim juga berdampak signifikan pada tingkat polusi udara.
        """)

except Exception as e:
    st.error(f"🚨 Terjadi kesalahan saat membaca dataset: {e}")
