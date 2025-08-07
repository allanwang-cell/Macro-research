import os
import sdmx
import pandas as pd

COUNTRY_CODES = ["CAN", "USA", "DEU", "FRA", "ITA", "GRB", "JPN"]

INDICATORS = {
    "Gross domestic product, constant prices": "NGDP_R",
    "Unemployment rate": "LUR",
    "Inflation, average consumer prices": "PCPI"
}

DATABASE_ID = "WEO"
CSV_DIR = "data/imf/"

def fetch_imf_data(database_id, indicator, country_code):
    key = f"{country_code}.{indicator}"
    IMF_DATA = sdmx.Client("IMF_DATA")
    data_msg = IMF_DATA.data(database_id, key = key)
    df = sdmx.to_pandas(data_msg)
    return df


def save_to_csv(df, name):
    os.makedirs(CSV_DIR, exist_ok=True)
    path = os.path.join(CSV_DIR, f"{name}.csv")
    df.to_csv(path)
    print(f"Saved: {path}")

def main():
    for (name, indicator) in INDICATORS.items():
        for country in COUNTRY_CODES:
            df = fetch_imf_data(DATABASE_ID, indicator, country)
            save_to_csv(df, f"{indicator}_{country}")
    IMF_DATA = sdmx.Client("IMF_DATA")
    data_msg = IMF_DATA.data(DATABASE_ID, key = 'JPN.NGDP_R')
    df = sdmx.to_pandas(data_msg)
    print(df.head())

if __name__ == "__main__":
    main()