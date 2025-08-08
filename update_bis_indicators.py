import os
import pandasdmx
import pandas as pd

CSV_DIR = "data/bis/"

INDICATORS = {
    "Central_bank_policy_rates": "WS_CBPOL",
    "Central_bank_total_assets": "WS_CBTA",
}

COUNTRY_CODES = ["US", "CA", "GB", "JP", "FR", "DE", "IT"]

def fetch_bis_data (indicator, country_code):
    bis = pandasdmx.Request("BIS")
    data_msg = bis.data(indicator, key = {"REF_AREA": country_code})
    df = data_msg.to_pandas()
    return df

def save_to_csv(df, name):
    os.makedirs(CSV_DIR, exist_ok=True)
    path = os.path.join(CSV_DIR, f"{name}.csv")
    df.to_csv(path)
    print(f"Saved: {path}")

def main():
    for (name, indicator) in INDICATORS.items():
        for country in COUNTRY_CODES:
            df = fetch_bis_data(indicator, country)
            save_to_csv(df, f"{name}_{country}")

if __name__ == "__main__":
    main()

