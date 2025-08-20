import pandas as pd
from src.utils.dates import parse_date, to_quarterly, to_yearly

def tidy_dataframe(df: pd.DataFrame, country: str, indicator_name: str) -> pd.DataFrame:
    df["INDICATOR"] = indicator_name
    df["COUNTRY"] = country

    if "FREQ" in df.columns:
        freq_column_name = "FREQ"

    if "FREQUENCY" in df.columns:
        freq_column_name = "FREQUENCY"

    df["TIME_PERIOD"] = df["TIME_PERIOD"].apply(parse_date)

    df = df[["TIME_PERIOD", freq_column_name, "COUNTRY", "INDICATOR", "value"]]

    return df

def flag_anomalies(df: pd.DataFrame, value_col: str = "value") -> pd.DataFrame:
    df = df.copy()
    df["missing"] = df[value_col].isna()

    # Sort for diff calculation
    df = df.sort_values(["COUNTRY", "INDICATOR", "TIME_PERIOD"])

    # Percent change
    df["pct_change"] = df.groupby(["COUNTRY", "INDICATOR"])[value_col].pct_change(fill_method=None).abs()

    # Flag jumps > 50%
    df["anomaly"] = df["pct_change"] > 0.5
    df.loc[df["missing"], "anomaly"] = True

    return df
