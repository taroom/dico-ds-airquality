import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st 
sns.set(style='dark')

st.title('Analisis Data Kualitas Udara 2013-2017')

# dataframe exist
# df1 = pd.read_csv("dataset/PRSA_Data_Aotizhongxin_20130301-20170228.csv")
# df2 = pd.read_csv("dataset/PRSA_Data_Changping_20130301-20170228.csv")
# df3 = pd.read_csv("dataset/PRSA_Data_Dingling_20130301-20170228.csv")
# df4 = pd.read_csv("dataset/PRSA_Data_Dongsi_20130301-20170228.csv")
# df5 = pd.read_csv("dataset/PRSA_Data_Guanyuan_20130301-20170228.csv")
# df6 = pd.read_csv("dataset/PRSA_Data_Gucheng_20130301-20170228.csv")
# df7 = pd.read_csv("dataset/PRSA_Data_Huairou_20130301-20170228.csv")
# df8 = pd.read_csv("dataset/PRSA_Data_Nongzhanguan_20130301-20170228.csv")
# df9 = pd.read_csv("dataset/PRSA_Data_Shunyi_20130301-20170228.csv")
# df10 = pd.read_csv("dataset/PRSA_Data_Tiantan_20130301-20170228.csv")
# df11 = pd.read_csv("dataset/PRSA_Data_Wanliu_20130301-20170228.csv")
# df12 = pd.read_csv("dataset/PRSA_Data_Wanshouxigong_20130301-20170228.csv")
# df_kualitas_udara = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12], axis=0)
df_kualitas_udara = pd.read_csv('cleaned_air_quality_data.csv')
df_kualitas_udara = df_kualitas_udara.reset_index()
df_kualitas_udara.drop(columns=['level_0', 'index'], inplace=True)

# sidebar
with st.sidebar:
    st.image("icon.png")
    
    unique_years = sorted(df_kualitas_udara['year'].unique())
    tahun = st.slider(
        label='Tentukan Jangkauan Tahun',
        min_value=min(unique_years),
        max_value=max(unique_years),
        value=(min(unique_years), max(unique_years))
    )
    st.write(f'Jangkauan Tahun: {tahun[0]}-{tahun[1]}')

    kota = df_kualitas_udara['station'].unique()

    selected_kota = st.selectbox('Pilih Kota:', ['Semua Kota'] + list(kota))
    st.text(selected_kota)


st.write(
    """
    Hello, para calon praktisi data masa depan!
    """
)

# cleaning
# df_kualitas_udara = df_kualitas_udara.drop('No', axis=1 )
# df_kualitas_udara = df_kualitas_udara.rename(columns={'PM2.5': 'PM2_5', 'wd': 'WD'})
# df_kualitas_udara.fillna({'PM2_5': df_kualitas_udara['PM2_5'].mode()[0]}, inplace=True)
# df_kualitas_udara.fillna({'PM10': df_kualitas_udara['PM10'].mode()[0]}, inplace=True)
# df_kualitas_udara.fillna({'SO2': df_kualitas_udara['SO2'].mode()[0]}, inplace=True)
# df_kualitas_udara.fillna({'NO2': df_kualitas_udara['NO2'].mode()[0]}, inplace=True)
# df_kualitas_udara.fillna({'CO': df_kualitas_udara['CO'].mode()[0]}, inplace=True)
# df_kualitas_udara.fillna({'O3': df_kualitas_udara['O3'].ffill()}, inplace=True)

# df_kualitas_udara.fillna({'TEMP': df_kualitas_udara['TEMP'].mode()[0]}, inplace=True)
# df_kualitas_udara['PRES'] = df_kualitas_udara['PRES'].interpolate(method='linear')
# df_kualitas_udara.fillna({'DEWP': df_kualitas_udara['DEWP'].ffill()}, inplace=True)
# df_kualitas_udara.fillna({'RAIN': df_kualitas_udara['RAIN'].ffill()}, inplace=True)
# df_kualitas_udara.fillna({'WD': df_kualitas_udara['WD'].ffill()}, inplace=True)
# df_kualitas_udara['WSPM'] = df_kualitas_udara['WSPM'].interpolate(method='linear')
# df_kualitas_udara.to_csv('cleaned_air_quality_data.csv', index=False)


# Teknik Cluster Binning
#batasan/standard setiap faktor untuk menentukan kualitas udara
def tentukan_kualitas_udara(PM25, PM10, SO2, NO2, CO, O3):
    standar = {
        'PM2_5': [(0, 12), (12, 35), (35, float('inf'))],
        'PM10': [(0, 50), (50, 100), (100, float('inf'))],
        'SO2': [(0, 20), (20, 100), (100, float('inf'))],
        'NO2': [(0, 40), (40, 100), (100, float('inf'))],
        'CO': [(0, 1000), (1000, 5000), (5000, float('inf'))],
        'O3': [(0, 100), (100, 180), (180, float('inf'))]
    }

    # Fungsi untuk menentukan kualitas udara
    def tentukan_kualitas(nilai, parameter):
        for kualitas, batas in enumerate(standar[parameter], start=1):
            if isinstance(batas, tuple):
                if batas[0] <= nilai < batas[1]:
                    return kualitas
            else:
                if nilai == batas:
                    return kualitas
        return 3  # Jika tidak ada yang cocok, maka kualitas dianggap "Buruk"

    # Menentukan kualitas untuk setiap parameter dengan mengonversi ke float
    kualitas_PM25 = tentukan_kualitas(float(PM25), 'PM2_5')
    kualitas_PM10 = tentukan_kualitas(float(PM10), 'PM10')
    kualitas_SO2 = tentukan_kualitas(float(SO2), 'SO2')
    kualitas_NO2 = tentukan_kualitas(float(NO2), 'NO2')
    kualitas_CO = tentukan_kualitas(float(CO), 'CO')
    kualitas_O3 = tentukan_kualitas(float(O3), 'O3')

    # Menghitung rata-rata dari nilai-nilai kualitas
    rata_rata_kualitas = (kualitas_PM25 + kualitas_PM10 + kualitas_SO2 + kualitas_NO2 + kualitas_CO + kualitas_O3) / 6

    if rata_rata_kualitas < 2:  # Misalnya, jika rata-rata kurang dari 2, dianggap "Baik"
        return 'Baik'
    elif rata_rata_kualitas < 2.5:  # Jika rata-rata antara 2 dan 2.5, dianggap "Sedang"
        return 'Sedang'
    else:
        return 'Buruk'


df_kualitas_udara['kualitas_udara'] = df_kualitas_udara.apply(
    lambda row: tentukan_kualitas_udara(
        row['PM2_5'],
        row['PM10'],
        row['SO2'],
        row['NO2'],
        row['CO'],
        row['O3']
    ),
    axis=1
)
df_kualitas_udara['kualitas_udara'] = df_kualitas_udara.kualitas_udara.astype('category')


# st.text(df_kualitas_udara.dtypes)
# menampilkan informasi tipe data per kolom


if(selected_kota == 'Semua Kota'):
    # memaki
    print ('Semua Kota')
else:
    df_kualitas_udara = df_kualitas_udara[(df_kualitas_udara['station'] == selected_kota)]

df_kualitas_udara = df_kualitas_udara[(df_kualitas_udara['year'].between(tahun[0], tahun[1]))]

# Display the filtered DataFrame
st.dataframe(df_kualitas_udara)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Tahun", f"{tahun[0]} - {tahun[1]}")
    
with col2:
    st.metric("Kota", selected_kota)

with col3:
    st.metric("Total Data", f"{len(df_kualitas_udara):,}".replace(",", "."))


polutan_list = ["PM2_5", "PM10", "SO2", "NO2", "CO", "O3"]
yearly_avg = df_kualitas_udara.groupby("year")[polutan_list].mean();


tab1, tab2, tab3, tab4 = st.tabs(["Data Kualitas Udara Terbaik", "Heatmap Korelasi", "Curah Hujan Vs. Polutan", "Tren Rata-rata Kualitas Udara dari Tahun ke Tahun"])
 
with tab1:
    st.header("Data Kualitas Udara Terbaik")
    if(selected_kota == 'Semua Kota'):
        df_kualitas_udara["index_kualitas_udara"] = df_kualitas_udara["kualitas_udara"]
        df_kualitas_udara["index_kualitas_udara"] = df_kualitas_udara["index_kualitas_udara"].map({"Baik": 1, "Sedang": 0, "Buruk": -1})
        df_kualitas_udara["index_kualitas_udara"] = df_kualitas_udara["index_kualitas_udara"].astype("int")

        daerah_df = df_kualitas_udara.groupby("station").index_kualitas_udara.sum().sort_values(ascending=False).reset_index() #membuat dataframe yang berisi index_kualitas_udara berdasarkan tempat station
        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

        # Membuat template color untuk visualisasi
        colors1 = ["#00FF00" , "#D3D3D9", "#D3D3D9", "#D3D3D9", "#D3D3D9"]
        colors2 = ["#1E90FF" , "#D3D3D9", "#D3D3D9", "#D3D3D9", "#D3D3D9"]

        # Membuat barplot dengan inisialisasi ax[0]
        sns.barplot(x="index_kualitas_udara", y="station", data=daerah_df.head(5), palette=colors1, ax=ax[0])
        ax[0].set_ylabel(None)
        ax[0].set_xlabel(None)
        ax[0].set_title("Kualitas Udara Terbaik", loc="center", fontsize=15)
        ax[0].tick_params(axis='y', labelsize=12)

        # Membuat barplot dengan inisialisasi ax[1]
        sns.barplot(x="index_kualitas_udara", y="station", data=daerah_df.sort_values(by="index_kualitas_udara", ascending=True).head(5), palette=colors2, ax=ax[1])
        ax[1].set_ylabel(None)
        ax[1].set_xlabel(None)
        ax[1].invert_xaxis()
        ax[1].yaxis.set_label_position("right")
        ax[1].yaxis.tick_right()
        ax[1].set_title("Kualitas Udara Terburu", loc="center", fontsize=15)
        ax[1].tick_params(axis='y', labelsize=12)

        # Menambahkan main title
        plt.suptitle("Terbaik dan Terburuk dalam kualitas udara pada 5 kota", fontsize=20)

        # Menampilkan plot di Streamlit
        st.pyplot(fig)
with tab2:
    st.header("Heatmap Korelasi")
    selected_columns = st.multiselect('Pilih Kolom Polutan', df_kualitas_udara.columns, default=['PM2_5', 'NO2', 'TEMP', 'PRES', 'DEWP'])
    corr = df_kualitas_udara[selected_columns].corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, ax=ax)
    st.pyplot(fig)
 
with tab3:
    st.header("Curah Hujan Vs. Polutan")
    # Buat figure untuk subplots curah hujan
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    axes = axes.flatten()  # Flatten axes untuk iterasi lebih mudah

    # Plot scatter untuk setiap polutan terhadap curah hujan (RAIN)
    for i, polutan in enumerate(polutan_list):
        sns.scatterplot(ax=axes[i], data=df_kualitas_udara, x="RAIN", y=polutan)
        axes[i].set_title(f'Curah Hujan vs {polutan}')
        axes[i].set_xlabel('Curah Hujan (mm)')
        axes[i].set_ylabel(f'{polutan} (µg/m³)')

    # Tambahkan layout yang rapih
    plt.tight_layout()
    fig.suptitle(f'Pengaruh Curah Hujan terhadap Polutan Udara di {selected_kota}', fontsize=16, y=1.02)

    # Tampilkan plot di Streamlit
    st.pyplot(fig)
with tab4:
    # Buat figure untuk plot
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot data untuk setiap polutan
    for polutan in polutan_list:
        ax.plot(yearly_avg.index, yearly_avg[polutan], marker='o', label=polutan)

    # Tambahkan judul, label, dan legenda

    ax.set_title(f'Tren Rata-rata Kualitas Udara dari Tahun ke Tahun di {selected_kota}')
    ax.set_xlabel('Tahun')
    ax.set_ylabel('Rata-rata Konsentrasi Polutan')
    ax.legend(title='Polutan')
    ax.grid(True)

    # Tampilkan plot di Streamlit
    st.pyplot(fig)