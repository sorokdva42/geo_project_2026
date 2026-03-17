import os 

os.getcwd()




import pandas as pd
import matplotlib.pyplot as plt






files = [
    "Forest_YMD_Celsius.csv",
    "Meadow_YMD_Celsius.csv",
    "Peat_YMD_Celsius.csv",
    "Bogpine_YMD_Celsius.csv"
]
lst_columns = ["LST_L5", "LST_L7", "LST_L8", "LST_L9"]

months_selected = [5, 6, 7, 8, 9, 10]

for file in files:
    
    df = pd.read_csv(file)
    
    # Keep only selected months
    df = df[df["month"].isin(months_selected)]
    
    # Convert to long format
    df_long = df.melt(
        id_vars=["month"],
        value_vars=lst_columns,
        var_name="Satellite",
        value_name="LST"
    )
    
    # Remove NaN
    df_long = df_long.dropna(subset=["LST"])
    
    # 🔹 Cut extreme values
    df_long = df_long[
        (df_long["LST"] >= 2) & 
        (df_long["LST"] <= 42)
    ]
    
    # Create boxplot
    plt.figure()
    df_long.boxplot(column="LST", by="month")
    
    plt.title(f"Monthly LST Boxplot ({file.split('_')[0]})")
    plt.suptitle("")
    plt.xlabel("Month")
    plt.ylabel("LST (°C)")
    
    plt.show()



# everything in one plot

# Create one figure with 4 subplots (2x2 grid)
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()  # makes indexing easier

for i, file in enumerate(files):
    
    df = pd.read_csv(file)
    
    # Keep only selected months
    df = df[df["month"].isin(months_selected)]
    
    # Convert to long format
    df_long = df.melt(
        id_vars=["month"],
        value_vars=lst_columns,
        var_name="Satellite",
        value_name="LST"
    )
    
    # Remove NaN
    df_long = df_long.dropna(subset=["LST"])
    
    # Cut extreme values
    df_long = df_long[
        (df_long["LST"] >= 2) & 
        (df_long["LST"] <= 42)
    ]
    
    # Plot on corresponding subplot
    df_long.boxplot(column="LST", by="month", ax=axes[i])
    
    axes[i].set_title(file.split('_')[0])
    axes[i].set_xlabel("Month")
    axes[i].set_ylabel("LST (°C)")

# Remove automatic pandas title
plt.suptitle("")

plt.tight_layout()
plt.show()