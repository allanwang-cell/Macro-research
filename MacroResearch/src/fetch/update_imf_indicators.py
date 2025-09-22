import os
import sdmx
from src.utils.io import save_csv, get_data_dir

INDICATORS = {
    "expenditure_general_government_percent_of_gdp": "USA.GGX_NGDP.A",
    "revenue_general_government_percent_of_gdp": "USA.GGR_NGDP.A",
    "net_debt_general_government_percent_of_gdp": "USA.GGXWDN_NGDP.A"
}

COUNTRY_CODE: "USA"
DATABASE_ID = "WEO"

def fetch_imf():
    out_dir = get_data_dir("imf")
    for indicator, code in INDICATORS.items():
        try:
            key = f"{code}"
            IMF_DATA = sdmx.Client("IMF_DATA")
            data_msg = IMF_DATA.data(DATABASE_ID, key=key)
            df = sdmx.to_pandas(data_msg)
            save_csv(df, os.path.join(out_dir, f"{indicator}.csv"))
            print(f"[IMF] Saved {indicator}")
        except Exception as e:
            print(f"[IMF] Failed for {indicator}: {e}")

if __name__ == "__main__":
    fetch_imf()
