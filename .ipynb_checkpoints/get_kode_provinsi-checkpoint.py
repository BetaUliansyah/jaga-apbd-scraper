import requests
import json
import pandas as pd
from time import perf_counter

# Start time for performance measurement
start_time = perf_counter()
print('Bismillah. Perkiraan berjalan 1 detik. Mohon tunggu.')

# Disable SSL warnings and initialize session
requests.packages.urllib3.disable_warnings()
s = requests.Session()

# Fetch the webpage
r = s.get('https://jaga.id/api/v5/kemenkeu-apbd/get-wilayah', verify=False)
response_json = r.json()

# Membuat DataFrame langsung dari data JSON
provinsi_df = pd.DataFrame.from_records(response_json['data'])

# Convert the list of dictionaries to DataFrame once
# provinsi_df = pd.DataFrame(provinsi_data)

# Save the results to CSV
provinsi_df['provinsi'] = provinsi_df.loc[:, 'namapemda']
provinsi_df.to_csv('kode_provinsi.csv', index=False)

# Calculate and print elapsed time
end_time = perf_counter()
total_time = end_time - start_time
rows = len(provinsi_df)
print(f"\n---Finished scraping {rows} rows in: {total_time:.2f} seconds---")