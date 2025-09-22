import os
import pandas as pd
from src.config import DATA_DIR

def save_csv(df, path):
    df.to_csv(path, index=True)

def load_csv(path):
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    return df

def get_data_dir(source: str):
    out_dir = os.path.join(DATA_DIR, source)
    os.makedirs(out_dir, exist_ok=True)
    return out_dir