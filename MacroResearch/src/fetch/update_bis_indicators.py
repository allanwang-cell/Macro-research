import os
import pandasdmx
import pandas as pd
from src.utils.io import save_csv, get_data_dir

INDICATORS = {
    "central_bank_policy_rates": "WS_CBPOL",
    "central_bank_total_assets": "WS_CBTA",
}

COUNTRY_CODES = ["US", "CA", "GB", "JP", "FR", "DE", "IT"]

def fetch_bis():
    bis = pandasdmx.Request("BIS")
    out_dir = get_data_dir("bis")

    for indicator, code in INDICATORS.items():
        for country in COUNTRY_CODES:
            try:
                if code == "WS_CBTA":
                    key = f"M.{country}.B.USD._Z.B"
                    if country == "US":
                        key = f"M.{country}.B.XDC.USD.B"
                elif code == "WS_CBPOL":
                    key = f"M.{country}"
                data_msg = bis.data(code, key=key)
                df = data_msg.to_pandas()
                save_csv(df, os.path.join(out_dir, f"{indicator}_{country}.csv"))
                print(f"[BIS] Saved {country} {indicator}")
            except Exception as e:
                print(f"[BIS] Failed for {country} {indicator}: {e}")