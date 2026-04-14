from collections import defaultdict
import glob
import os
import pandas as pd

# Step 1: Find ALL files starting with LST_ and ending in .csv
# This will now find "Cikanska_slat", "Javori", or any other area!
file_pattern = "LST_*.csv"
all_files = glob.glob(file_pattern)

# This dictionary will hold lists of files, grouped by site name
grouped_files = defaultdict(list)

# Step 2: Extract the site name and group the files
for file_path in all_files:
    filename = os.path.basename(file_path)

    # Example: "LST_L5-Cikanska_slat_Bogpine.csv"
    # Remove '.csv' -> "LST_L5-Cikanska_slat_Bogpine"
    base_name = filename.replace(".csv", "")

    # Split by the last underscore to grab the site (e.g., "Bogpine")
    site_name = base_name.split("_")[-1]

    # Add the file to that site's group
    grouped_files[site_name].append(file_path)

# Step 3: Loop through each site, merge the files, and save!
for site, files in grouped_files.items():


    # Read all CSVs for this site into a list of dataframes
    df_list = [pd.read_csv(f) for f in files]

    # Concatenate them all together
    merged_df = pd.concat(df_list, ignore_index=True)

    # Convert the time column to datetime and sort
    if "system:time_start" in merged_df.columns:
        merged_df["system:time_start"] = pd.to_datetime(
            merged_df["system:time_start"]
        )
        merged_df.sort_values(by="system:time_start", inplace=True)
    else:
        print(
            f"Warning: 'system:time_start' column not found for {site}. Skipping sort."
        )

    # Save to a new CSV file
    output_filename = f"{site}_merged.csv"
    merged_df.to_csv(output_filename, index=False)
    print(
        f"Successfully merged {len(files)} files into {output_filename}\n"
    )