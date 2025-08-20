from src.fetch.update_fred_indicators import fetch_fred
from src.fetch.update_imf_indicators import fetch_imf
from src.fetch.update_bis_indicators import fetch_bis

if __name__ == "__main__":
    print("Fetching FRED...")
    #fetch_fred()
    print("Fetching IMF...")
    #fetch_imf()
    print("Fetching BIS...")
    fetch_bis()
    print("All data updated")
