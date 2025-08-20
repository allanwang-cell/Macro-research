import os
import sdmx
import pandas as pd
from src.utils.io import save_csv, get_data_dir

INDICATORS = {
    "gross_domestic_product_constant_prices": "NGDP_R",
    "unemployment_rate": "LUR",
    "inflation_average_consumer_prices": "PCPI"
}

COUNTRY_CODES = ["CAN", "USA", "DEU", "FRA", "ITA", "GBR", "JPN"]
DATABASE_ID = "WEO"

def fetch_imf():
    out_dir = get_data_dir("imf")

    for indicator, code, in INDICATORS.items():
        for country in COUNTRY_CODES:
            try:
                key = f"{country}.{code}"
                IMF_DATA = sdmx.Client("IMF_DATA")
                data_msg = IMF_DATA.data(DATABASE_ID, key = key)
                df = sdmx.to_pandas(data_msg)
                save_csv(df, os.path.join(out_dir, f"{indicator}_{country}.csv"))
                print(f"[IMF] Saved {country} {indicator}")
            except Exception as e:
                print(f"[IMF] Failed for {country} {indicator}: {e}")