# exports 
import pandas as pd

df_forest = pd.read_csv('Forest.csv') # here reading the first dataset, which contains the forest data

print(df_forest.head())
print(df_forest.dtypes)


df_forest["system_time_start"] = pd.to_datetime(
    df_forest["system_time_start"],
    format="%b %d, %Y"
)



df_forest_l9 = pd.read_csv("Forest_l9.csv") # here changing the name of the second dataset to avoid confusion


df_forest_l9["system_time_start"] = pd.to_datetime(
    df_forest_l9["system_time_start"],
    format="%b %d, %Y"
)

print(df_forest_l9.head())
print(df_forest_l9.dtypes)


df_forest_all = pd.merge(
    df_forest,
    df_forest_l9,
    on="system_time_start",
    how="outer"
)

print(df_forest_all.head())
print(df_forest_all.dtypes)

df_forest_all = df_forest_all.sort_values("system_time_start")

df_forest_all.to_csv("Forest_merged.csv", index=False) # here exporting the merged dataset to a new CSV file


