import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
os.getcwd()

files = [
    "Forest_YMD_Celsius.csv",
    "Meadow_YMD_Celsius.csv",
    "Peat_YMD_Celsius.csv",
    "Shrub_YMD_Celsius.csv"
]

lst_columns = ["LST_L5", "LST_L7", "LST_L8", "LST_L9"]

colors = {
    "Forest": "darkgreen",
    "Meadow": "gold",
    "Peat": "brown",
    "Shrub": "olive"
}

plt.figure(figsize=(12, 6))

for file in files:

    class_name = file.replace("_YMD_Celsius.csv", "")
    color = colors[class_name]

    df = pd.read_csv(file)
    df["system_time_start"] = pd.to_datetime(df["system_time_start"])

    # Filter growing season
    df = df[df["month"].isin([5, 6, 7, 8, 9, 10])]

    # Merge satellites (mean ignoring NaN)
    df["LST_mean"] = df[lst_columns].mean(axis=1)

    # Remove unrealistic values
    df["LST_mean"] = df["LST_mean"].where(
        (df["LST_mean"] >= 2) & (df["LST_mean"] <= 42)
    )

    # Drop missing
    df = df.dropna(subset=["LST_mean"])

    # Convert date to numeric for regression
    df["date_num"] = df["system_time_start"].map(pd.Timestamp.toordinal)

    # Linear regression
    z = np.polyfit(df["date_num"], df["LST_mean"], 1)
    p = np.poly1d(z)

    # Plot data
    plt.scatter(df["system_time_start"], df["LST_mean"],
                color=color, alpha=0.4)

    # Plot trend line
    plt.plot(df["system_time_start"],
             p(df["date_num"]),
             color=color,
             linewidth=2,
             label=f"{class_name} trend")

    # Print slope in °C per year
    slope_per_day = z[0]
    slope_per_year = slope_per_day * 365
    print(f"{class_name} trend: {slope_per_year:.3f} °C/year")

plt.xlabel("Date")
plt.ylabel("Mean LST (°C)")
plt.title("LST Trend Rolava")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



# -------------------------

for file in files:

    class_name = file.replace("_YMD_Celsius.csv", "")
    color = colors[class_name]

    df = pd.read_csv(file)
    df["system_time_start"] = pd.to_datetime(df["system_time_start"])

    # Extract month
    df["month"] = df["system_time_start"].dt.month

    # Filter growing season
    df = df[df["month"].isin([5, 6, 7, 8, 9, 10])]

    # Merge satellites (mean ignoring NaN)
    df["LST_mean"] = df[lst_columns].mean(axis=1)

    # Remove unrealistic values
    df["LST_mean"] = df["LST_mean"].where(
        (df["LST_mean"] >= 2) & (df["LST_mean"] <= 42)
    )

    # Drop missing
    df = df.dropna(subset=["LST_mean"])

    # Extract year
    df["year"] = df["system_time_start"].dt.year

    # Compute yearly growing-season mean
    df_yearly = (
        df.groupby("year")["LST_mean"]
        .mean()
        .reset_index()
    )

    # Linear regression (year vs yearly mean)
    z = np.polyfit(df_yearly["year"], df_yearly["LST_mean"], 1)
    p = np.poly1d(z)

    # Scatter yearly means
    plt.scatter(
        df_yearly["year"],
        df_yearly["LST_mean"],
        color=color,
        alpha=0.8
    )

    # Trend line
    plt.plot(
        df_yearly["year"],
        p(df_yearly["year"]),
        color=color,
        linewidth=2,
        label=f"{class_name} trend"
    )

    # Slope directly in °C per year
    slope_per_year = z[0]
    print(f"{class_name} yearly trend: {slope_per_year:.3f} °C/year")

plt.xlabel("Year")
plt.ylabel("Growing Season Mean LST (°C)")
plt.title("Yearly Growing Season LST Trend  Rolava")
plt.legend()
plt.tight_layout()
plt.show()