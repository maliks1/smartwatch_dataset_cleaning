import pandas as pd

# Memuat dataset
data = pd.read_csv('unclean_smartwatch_health_data.csv')

# Mengecek nilai yang hilang (missing values)
missing_values_summary = data.isnull().sum()
print("\nJumlah nilai kosong per kolom:\n", missing_values_summary)

# Menghapus baris yang memiliki nilai kosong (alternatif: bisa juga menggunakan imputasi)
data_cleaned = data.dropna()

# Menghapus baris yang mengandung kata "ERROR"
# Semua nilai dikonversi menjadi string terlebih dahulu untuk menghindari error saat pengecekan
data_cleaned = data_cleaned[~data_cleaned.astype(str).apply(lambda row: row.str.contains("ERROR").any(), axis=1)]

# Menghapus kolom 'User ID' karena tidak dibutuhkan dalam analisis umum
if 'User ID' in data_cleaned.columns:
    data_cleaned.drop(columns=['User ID'], inplace=True)

# Membulatkan nilai pada kolom Heart Rate (BPM) dan Step Count ke bilangan bulat
data_cleaned['Heart Rate (BPM)'] = data_cleaned['Heart Rate (BPM)'].round(0).astype(int)
data_cleaned['Step Count'] = data_cleaned['Step Count'].round(0).astype(int)

# Menangani nilai "Very High" pada kolom Stress Level dengan menggantinya menjadi 10
data_cleaned['Stress Level'] = data_cleaned['Stress Level'].replace('Very High', 10)

# Konversi Sleep Duration dan Stress level menjadi numerik (float)
data_cleaned['Sleep Duration (hours)'] = pd.to_numeric(data_cleaned['Sleep Duration (hours)'], errors='coerce')
data_cleaned['Stress Level'] = pd.to_numeric(data_cleaned['Stress Level'], errors='coerce')

# Membatasi nilai Sleep Duration dan Blood Oxygen Level menjadi 2 angka di belakang koma
data_cleaned['Blood Oxygen Level (%)'] = data_cleaned['Blood Oxygen Level (%)'].round(2)
data_cleaned['Sleep Duration (hours)'] = data_cleaned['Sleep Duration (hours)'].round(2)

# Menghapus baris dengan Step Count di bawah 100
data_cleaned = data_cleaned[data_cleaned['Step Count'] >= 100]

# Memperbaiki kesalahan penulisan (typo) pada kolom Activity Level
if 'Activity Level' in data_cleaned.columns:
    data_cleaned['Activity Level'] = data_cleaned['Activity Level'].replace({
        'Actve': 'Active',
        'Highly_Active': 'Highly Active',
        'Seddentary': 'Sedentary'
    })

# Mereset indeks (opsional agar data terlihat rapi)
data_cleaned.reset_index(drop=True, inplace=True)

# Menampilkan jumlah baris dan kolom awal dan setelah dibersihkan
print("\nUkuran data awal:", data.shape)
print("\nUkuran data setelah dibersihkan:", data_cleaned.shape)
print(data_cleaned.info())

# Menyimpan dataset yang telah dibersihkan ke file baru
data_cleaned.to_csv('smartwatch_data_cleaned.csv', index=False)