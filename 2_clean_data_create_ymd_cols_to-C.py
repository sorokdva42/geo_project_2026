import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------
# 1. Load data
# -------------------------
df_forest = pd.read_csv("Bogpine_merged.csv")

print(df_forest.head())
print(df_forest.dtypes)


df_forest["system_time_start"] = pd.to_datetime(
    df_forest["system_time_start"]
)

df_forest["year"] = df_forest["system_time_start"].dt.year
df_forest["month"] = df_forest["system_time_start"].dt.month
df_forest["day"] = df_forest["system_time_start"].dt.day
df_forest

lst_cols = ["LST_L5", "LST_L7", "LST_L8", "LST_L9"]

print(df_forest.dtypes)

for col in lst_cols:
    df_forest[col] = df_forest[col] - 273.15

df_forest


df_forest.to_csv("Bogpine_YMD_Celsius.csv", index=False)



