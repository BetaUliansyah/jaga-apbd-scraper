import requests
import json
import pandas as pd
from time import perf_counter

# Start time for performance measurement
start_time = perf_counter()
print('Bismillah. Perkiraan berjalan 3 detik. Mohon tunggu.')

# Disable SSL warnings and initialize session
requests.packages.urllib3.disable_warnings()
s = requests.Session()

# ambil data kode_provinsi
provinsi_df = pd.read_csv('kode_provinsi.csv', index_col=0)
kode_provinsi = provinsi_df['kodeprovinsi']

# Fetch the webpage
# Collect data as a list of dictionaries
data_list = []

for kodeprovinsi in kode_provinsi:
    r = s.get(f'https://jaga.id/api/v5/kemenkeu-apbd/get-sub-wilayah?kodeprovinsi={kodeprovinsi}', verify=False)
    response_json = r.json()

    for i in response_json['data']:
        data_list.append(i)

# Create a DataFrame from list of dictionaries
kabkota_df = pd.DataFrame(data_list)
provinsi_df = pd.read_csv('kode_provinsi.csv', dtype=object)
kabkota_df['provinsi'] = kabkota_df.merge(provinsi_df, on='kodeprovinsi', how='left')['namapemda_y']
kabkota_df['kodewilayah'] = kabkota_df.merge(provinsi_df, on='kodeprovinsi', how='left')['kodepemda_y']
# Convert the list of dictionaries to DataFrame once

# Save the results to CSV
kabkota_df.to_csv('kode_kabkota.csv', index=False)

# Calculate and print elapsed time
end_time = perf_counter()
total_time = end_time - start_time
rows = len(kabkota_df)
print(f"\n---Finished scraping {rows} rows in: {total_time:.2f} seconds---")