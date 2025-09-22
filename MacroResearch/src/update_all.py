from src.fetch.update_fred_indicators import fetch_fred
from src.fetch.update_imf_indicators import fetch_imf
from src.fetch.update_bls_indicators import fetch_bls

if __name__ == "__main__":
    print("Fetching FRED...")
    fetch_fred()
    print("Fetching IMF...")
    fetch_imf()
    print("Fetching BLS...")
    fetch_bls()
    print("All data updated")
