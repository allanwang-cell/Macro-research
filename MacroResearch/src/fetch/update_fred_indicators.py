import os
import pandas as pd
from fredapi import Fred
from src.config import FRED_API_KEY
from src.utils.io import save_csv, get_data_dir

fred = Fred(api_key=FRED_API_KEY)

INDICATORS = {
    "real_gdp": "GDPC1",
    "unemployment_rate": "UNRATE",
    "participation_rate": "CIVPART",
    "urban_consumers_cpi_all_items": "CPIAUCSL",
    "federal_funds_rate": "FEDFUNDS",
    "m2_money_supply": "M2SL"
}

def fetch_fred():
    out_dir = get_data_dir("fred")
    for indicator, code in INDICATORS.items():
        try:
            series = fred.get_series(code)
            df = pd.DataFrame(series, columns = ["value"])
            df.index.name = "TIME_PERIOD"
            df["FREQUENCY"] = "M"
            save_csv(df, os.path.join(out_dir, f"{indicator}_US.csv"))
            print(f"[FRED] Saved {indicator}")
        except Exception as e:
            print(f"[FRED] Failed for {indicator}: {e}")