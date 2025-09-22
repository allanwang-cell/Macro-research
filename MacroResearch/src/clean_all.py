import os
import pandas as pd
from src.utils.clean import tidy_dataframe, flag_anomalies
from src.utils.io import get_data_dir, save_csv
from src.utils.dates import parse_date, to_quarterly, to_yearly

DATA_DIRS = {
    "fred": get_data_dir("fred"),
    "imf": get_data_dir("imf"),
    "bls": get_data_dir("bls")
}

OUTPUT_DIR = get_data_dir("cleaned")
os.makedirs(OUTPUT_DIR, exist_ok=True)

DATE_COL = "date"

def clean_source(source_name: str, dir_path: str):
    #print(os.listdir(dir_path))
    for fname in os.listdir(dir_path):
        if fname.endswith(".csv"):
            file_path = os.path.join(dir_path, fname)
            # Infer indicator from filename
            indicator = fname.replace(".csv","")
            print(f"{indicator}_{source_name}_cleaned")
            df = pd.read_csv(file_path)
            df_tidy = tidy_dataframe(df, indicator_name=indicator)
            df_flagged = flag_anomalies(df_tidy)
            df_flagged = df_flagged[["missing", "anomaly"]]
            df_combined = pd.concat([df_tidy, df_flagged], axis=1)
            save_csv(df_combined, os.path.join(OUTPUT_DIR, f"{indicator}_{source_name}_cleaned.csv"))

def clean_all():
    for source_name, dir_path in DATA_DIRS.items():
        #print(f"Cleaning {source_name.upper()} data...")
        clean_source(source_name, dir_path)

if __name__ == "__main__":
    clean_all()
