import requests
import json
import pandas as pd
from time import perf_counter

# Start time for performance measurement
start_time = perf_counter()
tahun = 2018
print('Bismillah. Perkiraan berjalan 40-60 detik. Mohon tunggu.')

# Disable SSL warnings and initialize session
requests.packages.urllib3.disable_warnings()
s = requests.Session()

# ambil data kode_provinsi
kabkota_df = pd.read_csv('kode_kabkota.csv', dtype=object)

# Fetch the webpage and collect data as a list of dictionaries
data_list = []

# make tuple pairs of kodewilayah and kodepemdaa
pemda_list = []
for kodepemda in kabkota_df['kodepemda']:
    pemda_list.append((kabkota_df.query(f'kodepemda == "{kodepemda}"')['kodewilayah'].values[0], kodepemda))
for kodewilayah, kodepemda in pemda_list:
    r = s.get(f'https://jaga.id/api/v5/kemenkeu-apbd/get-apbd?tipe=apbd&tahun={tahun}&kodewilayah={kodewilayah}&kodesubwilayah={kodepemda}', verify=False)
    response_json = r.json()
    namapemda = kabkota_df.query(f'kodepemda == "{kodepemda}"')['namapemda'].values[0]
    provinsi = kabkota_df.query(f'kodepemda == "{kodepemda}"')['provinsi'].values[0]
    for i in response_json['data']:
        for j in response_json['data'][i]['level2']:
            for k in response_json['data'][i]['level2'][j]['level3']:
                data_list.append({'namapemda' : namapemda,
                                  'provinsi' : provinsi,
                                  'tahun' : tahun,
                                  'level1coa90' : k['level1coa90'],
                                  'level2coa90' : k['level2coa90'],
                                  'level3coa90' : k['level3coa90'],
                                  'jenis': 'Anggaran',
                                  'nilai' : k['nilaianggaran']})
                data_list.append({'namapemda' : namapemda,
                                  'provinsi' : provinsi,
                                  'tahun' : tahun,
                                  'level1coa90' : k['level1coa90'],
                                  'level2coa90' : k['level2coa90'],
                                  'level3coa90' : k['level3coa90'],
                                  'jenis': 'Realisasi',
                                  'nilai' : k['nilairealisasi']})

# Convert the list of dictionaries to DataFrame once
data_df = pd.DataFrame(data_list)

# Save the results to CSV
data_df.to_csv(f'data_apbd_kabkota_level3-{tahun}.csv', index=False)

# Calculate and print elapsed time
end_time = perf_counter()
total_time = end_time - start_time
rows = len(data_df)
print(f"\n---Finished scraping {rows} rows in: {total_time:.2f} seconds---")