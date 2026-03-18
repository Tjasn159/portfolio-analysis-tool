from pathlib import Path
import pandas as pd
import yfinance as yf
from config import TICKERS

tickers = TICKERS

DATA_RAW = Path("data/raw")

def fetch_prices(tickers, start="2023-01-01", end=None):
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    raw = yf.download(tickers=tickers, start=start, end=end, interval="1d", auto_adjust=True, progress=False)

    prices = raw["Close"]
    prices.to_csv(DATA_RAW / "prices.csv", index=True) 
    return prices

if __name__ == "__main__":
    prices1 = fetch_prices(tickers)
    print("Downloaded price data")
    print(prices1.head())
    