import os
import pandas as pd
from fredapi import Fred

INDICATORS = {
    "real_gdp": "GDPC1",
    "unemployment_rate": "UNRATE",
    "participation_rate": "CIVPART",
    "urban_consumers_cpi_all_items": "CPIAUCSL",
    "federal_funds_rate": "FEDFUNDS",
    "m2_money_supply": "M2SL"
}


CSV_DIR = "data/fred/"
FRED_API_KEY = "e3366a9df22a3a1cbc47df9e247e59de"
fred = Fred(api_key=FRED_API_KEY)

def fetch_series(series_id):
    data = fred.get_series(series_id)
    df = pd.DataFrame(data)
    df.columns = ['value']
    df.index.name = 'date'
    df = df.sort_index()
    return df

def save_to_csv(df, name):
    os.makedirs(CSV_DIR, exist_ok=True)
    path = os.path.join(CSV_DIR, f"{name}.csv")
    df.to_csv(path)
    print(f"Saved: {path}")

def main():
    for (name, series_id) in INDICATORS.items():
        print(f"Fetching {name} ({series_id})...")
        df = fetch_series(series_id)
        save_to_csv(df, name)

if __name__ == "__main__":
    main()