import pandas as pd
df = pd.read_json (r'data.json')
export_csv = df.to_csv (r'data.csv', index = None, header=True)