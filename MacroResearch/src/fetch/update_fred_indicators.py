import os
import pandas as pd
from fredapi import Fred
from src.config import FRED_API_KEY
from src.utils.io import save_csv, get_data_dir

fred = Fred(api_key=FRED_API_KEY)

INDICATORS = {
    "nominal_gdp": "GDP",
    "real_gdp": "GDPC1",
    "real_gdp_per_capita": "A939RX0Q048SBEA",
    "industrial_production_total_index": "INDPRO",
    "advance_retail_sales_retail_trade": "RSXFS",
    "urban_consumers_cpi_all_items": "CPIAUCSL",
    "urban_consumers_cpi_all_items_less_food_and_energy": "CPILFESL",
    "personal_consumption_expenditures_chain_type_price_index": "PCEPI",
    "personal_consumption_expenditures_excluding_food_and_energy": "PCEPILFE",
    "personal_consumption_expenditures_services_health_care": "DHLCRC1Q027SBEA",
    "producer_price_index_by_commodity_all_commodities": "PPIACO",
    "university_of_michigan_inflation_expectation": "MICH",
    "unemployment_rate": "UNRATE",
    "participation_rate": "CIVPART",
    "continued_claims_insured_unemployment": "CCSA",
    "effective_federal_funds_rate": "EFFR",
    "total_assets_less_eliminations_from_consolidation_wednesday_level": "WALCL",
    "m1_money_supply": "WM1NS",
    "m2_money_supply": "WM2NS"
}

def fetch_fred():
    out_dir = get_data_dir("fred")
    for indicator, code in INDICATORS.items():
        try:
            series = fred.get_series(code)
            info = fred.get_series_info(code)

            df = pd.DataFrame(series, columns = ["value"])
            df.index.name = "TIME_PERIOD"
            df["FREQUENCY"] = info['frequency_short']
            save_csv(df, os.path.join(out_dir, f"{indicator}.csv"))
            print(f"[FRED] Saved {info['title']}")
        except Exception as e:
            print(f"[FRED] Failed for {info['title']}: {e}")
