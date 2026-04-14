import pandas as pd

files = [
    "Forest_merged.csv",
    "Peat_merged.csv",
    "Bogpine_merged.csv"
]

for file in files:
    df = pd.read_csv(file)

    dt = pd.to_datetime(df['system:time_start'], errors='coerce')

    df['year'] = dt.dt.year
    df['month'] = dt.dt.month
    df['day'] = dt.dt.day

    df.to_csv(file, index=False)

print("Done")