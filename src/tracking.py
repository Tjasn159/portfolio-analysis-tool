import pandas as pd
import numpy as np

def load_transactions(path:str):
    """ Loads csv transactions file and cleans it up. Returns the dataframe"""
    transactions = pd.read_csv(path)
    transactions["date"] = pd.to_datetime(transactions["date"])
    transactions["amount"] = pd.to_numeric(transactions["amount"])
    transactions["balance"] = pd.to_numeric(transactions["balance"])

    transactions = transactions.sort_values("date")
    transactions = transactions.reset_index(drop=True)

    return transactions

def extract_trades(transactions:pd.DataFrame):
    trades = transactions[transactions["transaction"].isin(["BUY", "SELL"])]
    trades = trades[["date", "transaction", "description", "amount", "currency"]]
    trades = trades.reset_index(drop=True)

    trades["ticker"] = trades["description"].str.split(" - ").str[0]
    trades["quantity"] = trades["description"].str.extract(r"(?:Bought|Sold)\s+([0-9.]+)")[0]
    trades["quantity"] = pd.to_numeric(trades["quantity"])
    return trades
        
    
def build_holdings_over_time(trades:pd.DataFrame):
    holdings = trades.copy()

    holdings["signed_quantity"] = np.where(
        holdings["transaction"] == "BUY",
        holdings["quantity"],
        -holdings["quantity"]
    )

    holdings = holdings[["date", "ticker", "signed_quantity"]]
    holdings = holdings.groupby(["date", "ticker"], as_index=False)["signed_quantity"].sum()
    holdings = holdings.pivot(index="date", columns="ticker", values="signed_quantity")
    holdings = holdings.fillna(0)
    holdings = holdings.cumsum()


    return holdings