import pandas as pd
from datetime import datetime
import re

def to_quarterly(df: pd.DataFrame) -> pd.DataFrame:
    results = []
    for (country, indicator), group in df.groupby(["COUNTRY", "INDICATOR"]):
        # Convert only this group's TIME_PERIOD
        group["TIME_PERIOD"] = pd.to_datetime(group["TIME_PERIOD"], errors="coerce")

        # Set datetime index
        group = group.set_index("TIME_PERIOD")

        # Resample quarterly (calendar quarter end)
        group_q = group["value"].resample("QE").mean().reset_index()

        # Add identifiers
        group_q["COUNTRY"] = country
        group_q["INDICATOR"] = indicator

        results.append(group_q)

    return pd.concat(results, ignore_index=True)


def to_monthly(df: pd.DataFrame) -> pd.DataFrame:
    results = []
    for (country, indicator), group in df.groupby(["COUNTRY", "INDICATOR"]):
        # Convert only this group's TIME_PERIOD
        group["TIME_PERIOD"] = pd.to_datetime(group["TIME_PERIOD"], errors="coerce")

        # Set datetime index
        group = group.set_index("TIME_PERIOD")

        # Resample quarterly (calendar quarter end)
        group_q = group["value"].resample("M").mean().reset_index()

        # Add identifiers
        group_q["COUNTRY"] = country
        group_q["INDICATOR"] = indicator

        results.append(group_q)

    return pd.concat(results, ignore_index=True)

def to_yearly(df: pd.DataFrame) -> pd.DataFrame:
    results = []
    for (country, indicator), group in df.groupby(["COUNTRY", "INDICATOR"]):
        # Convert only this group's TIME_PERIOD
        group["TIME_PERIOD"] = pd.to_datetime(group["TIME_PERIOD"], errors="coerce")

        # Set datetime index
        group = group.set_index("TIME_PERIOD")

        # Resample quarterly (calendar quarter end)
        group_q = group["value"].resample("A").mean().reset_index()

        # Add identifiers
        group_q["COUNTRY"] = country
        group_q["INDICATOR"] = indicator

        results.append(group_q)

    return pd.concat(results, ignore_index=True)

def parse_date(x):
    if pd.isna(x):
        return None   # use None instead of NaT for datetime

    x = str(x).strip()

    # Match quarterly: 2020-Q1 or 2020Q1
    q_match = re.match(r"^(\d{4})-?Q([1-4])$", x)
    if q_match:
        year, q = q_match.groups()
        year, q = int(year), int(q)
        month = 3 * (q - 1) + 1
        return datetime(year=year, month=month, day=1)

    # Match yearly: 2020
    if re.match(r"^\d{4}$", x):
        return datetime(year=int(x), month=1, day=1)

    # Match year-month: 2020-05 or 2020-5
    ym_match = re.match(r"^(\d{4})-(\d{1,2})$", x)
    if ym_match:
        year, month = map(int, ym_match.groups())
        return datetime(year=year, month=month, day=1)

    # Match full date: 2020-05-15 (and variants)
    try:
        return datetime.strptime(x, "%Y-%m-%d")
    except Exception:
        try:
            # fallback to pandas' parser, then convert to datetime
            dt = pd.to_datetime(x, errors="coerce")
            return None if pd.isna(dt) else dt.to_pydatetime()
        except Exception:
            return None
