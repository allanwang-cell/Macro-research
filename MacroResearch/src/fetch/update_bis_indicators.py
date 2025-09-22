import os
import requests
import pandas as pd
from src.utils.io import save_csv, get_data_dir

INDICATORS = {
    "central_bank_policy_rates": "WS_CBPOL_D",
}

url = "https://stats.bis.org/api/v1/data/WS_CBPOL_D/US"

COUNTRY_CODE = "US"

params = {
    "startPeriod": "2020-01-01",
    "detail": "dataonly",
    "format": "json"   # ask BIS to return JSON instead of XML
}

def fetch_bis():
    bis = sdmx.Client("BIS")
    out_dir = get_data_dir("bis")

    for indicator, code in INDICATORS.items():
        try:
            data_msg = bis.data(code, key={"REF_AREA": "US"}, params={"startPeriod": "2020-01-01"})
            df = data_msg.to_pandas()
            save_csv(df, os.path.join(out_dir, f"{indicator}.csv"))
            print(f"[BIS] Saved {indicator}")
        except Exception as e:
            print(f"[BIS] Failed for {indicator}: {e}")

if __name__ == "__main__":
    response = requests.get(url, params=params)
    response.raise_for_status()  # error if failed

    data = response.json()

    series = data["data"]["series"]
    time_periods = data["structure"]["dimensions"]["observation"][0]["values"]

    rows = []
    for series_key, series_data in series.items():
        obs = series_data["observations"]
        for time_idx, val in obs.items():
            rows.append({
                "date": time_periods[int(time_idx)]["id"],
                "value": val[0]
            })

    df = pd.DataFrame(rows)
    print(df.head())