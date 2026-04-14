import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# имя папки
folder_name = os.path.basename(os.getcwd())

files = [
    "Forest_merged.csv",
    "Peat_merged.csv",
    "Bogpine_merged.csv"
]

colors = {
    "Forest": "green",
    "Peat": "brown",
    "Bogpine": "orange"
}

lst_columns = ["LST_C_L5", "LST_C_L7", "LST_C_L8"]

plt.figure(figsize=(12, 6))

# сюда будем сохранять тренды
trend_results = []

for file in files:

    class_name = file.replace("_merged.csv", "")
    color = colors.get(class_name, "black")

    df = pd.read_csv(file)

    df["system:time_start"] = pd.to_datetime(df["system:time_start"], errors="coerce")

    # сезон
    df = df[df["month"].isin([5, 6, 7, 8, 9, 10])]

    # mean LST
    df["LST_mean"] = df[lst_columns].mean(axis=1)

    # фильтр
    df["LST_mean"] = df["LST_mean"].where(
        (df["LST_mean"] >= 2) & (df["LST_mean"] <= 42)
    )

    df = df.dropna(subset=["LST_mean", "system:time_start"])

    df["date_num"] = df["system:time_start"].map(pd.Timestamp.toordinal)

    z = np.polyfit(df["date_num"], df["LST_mean"], 1)
    trend_model = np.poly1d(z)

    # график
    plt.scatter(df["system:time_start"], df["LST_mean"],
                color=color, alpha=0.4)

    plt.plot(df["system:time_start"],
             trend_model(df["date_num"]),
             color=color,
             linewidth=2,
             label=f"{class_name}")

    # тренд
    slope_per_year = z[0] * 365
    trend_results.append((class_name, slope_per_year))

    print(f"{class_name} trend: {slope_per_year:.3f} °C/year")

# оформление
plt.xlabel("Date")
plt.ylabel("Mean LST (°C)")
plt.title(f"LST Trend — {folder_name}")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# === создаём текст для окошка ===
text_str = "\n".join(
    [f"{name}: {value:.3f} °C/year" for name, value in trend_results]
)

# === inset box ===
plt.gca().text(
    0.02, 0.98,              # положение (левый верх)
    text_str,
    transform=plt.gca().transAxes,
    fontsize=10,
    verticalalignment='top',
    bbox=dict(
        boxstyle="round",
        facecolor="white",
        alpha=0.8
    )
)

# сохранить
output_file = f"LST_trend_{folder_name}.png"
plt.savefig(output_file, dpi=300)

plt.show()

print(f"Saved as: {output_file}")