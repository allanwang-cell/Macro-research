import os
from bls import get_series
import pandas as pd
from src.config import BLS_API_KEY
from src.utils.io import save_csv, get_data_dir

INDICATORS = {
    "output_per_hour_nonfarm_business_productivity": "PRS85006092",
    "employment_population_ratio": "LNS12300000",
    "total_nonfarm_employment_seasonally_adjusted": "CES0000000001",
    "nonfarm_business_real_hourly_compensation": "PRS85006152",
    "job_openings_level_total_nonfarm_seasonally_adjusted": "JTS000000000000000JOL"
}

def fetch_bls():
    out_dir = get_data_dir("bls")
    for indicator, code in INDICATORS.items():
        try:
            series = pd.Series(get_series(code, startyear=2020, key=BLS_API_KEY), name = "value")
            df = series.to_frame()
            df.index.name = 'TIME_PERIOD'
            save_csv(df, os.path.join(out_dir, f"{indicator}.csv"))
            print(f"[BLS] Saved {indicator}")
        except Exception as e:
            print(f"[BLS] Failed for {indicator}: {e}")

if __name__ == "__main__":
    fetch_bls()

