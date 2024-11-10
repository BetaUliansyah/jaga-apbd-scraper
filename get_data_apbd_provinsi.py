import requests
import json
import pandas as pd
from time import perf_counter

# Start time for performance measurement
start_time = perf_counter()
tahun = 2024
print('Bismillah. Perkiraan berjalan 9 detik. Mohon tunggu.')

# Disable SSL warnings and initialize session
requests.packages.urllib3.disable_warnings()
s = requests.Session()

# ambil data kode_provinsi
provinsi_df = pd.read_csv('kode_provinsi.csv')
kode_pemda_provinsi = provinsi_df['kodepemda']

# Fetch the webpage and collect data as a list of dictionaries
data_list = []

for kodepemda in kode_pemda_provinsi:
    kodepemda = str(kodepemda)+'0'
    print('kodepemda:', kodepemda)
    r = s.get(f'https://jaga.id/api/v5/kemenkeu-apbd/get-apbd?tipe=apbd&tahun={tahun}&kodewilayah={kodepemda}', verify=False)
    response_json = r.json()
    row_df = pd.json_normalize(response_json['data'])
    print('row_df:', row_df)
    row_dict = row_df.to_dict()
    print('row_dict:', row_dict)
    data_list.append(row_dict)

# Convert the list of dictionaries to DataFrame once
data_apbd_provinsi_df = pd.DataFrame(data_list)

# Save the results to CSV
data_apbd_provinsi_df.to_csv(f'data_apbd_provinsi-{tahun}.csv', index=False)

# Calculate and print elapsed time
end_time = perf_counter()
total_time = end_time - start_time
rows = len(data_apbd_provinsi_df)
print(f"\n---Finished scraping {rows} rows in: {total_time:.2f} seconds---")