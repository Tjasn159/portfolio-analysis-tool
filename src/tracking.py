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



def load_opening_holdings(path:str):
    opening_holdings = pd.read_csv(path)

    opening_holdings["date"] = pd.to_datetime(opening_holdings["date"])
    opening_holdings["quantity"] = pd.to_numeric(opening_holdings["quantity"])

    opening_holdings = opening_holdings.sort_values(["date", "ticker"])
    opening_holdings = opening_holdings.reset_index(drop=True)

    return opening_holdings

def apply_opening_holdings(holdings: pd.DataFrame, opening_holdings: pd.DataFrame):
    opening = opening_holdings.copy()

    opening = opening.groupby(["date", "ticker"], as_index=False)["quantity"].sum()

    opening = opening.pivot(index="date", columns="ticker", values="quantity")
    opening = opening.fillna(0)

    all_dates = holdings.index.union(opening.index).sort_values()
    all_tickers = holdings.columns.union(opening.columns)

    holdings = holdings.reindex(index=all_dates, columns=all_tickers, fill_value=0)
    opening = opening.reindex(index=all_dates, columns=all_tickers, fill_value=0)

    opening = opening.cumsum()

    final_holdings = opening + holdings

    return final_holdings



def map_holdings_to_price_tickers(holdings: pd.DataFrame, ticker_map: dict[str, str]):
    mapped_holdings = holdings.copy()

    mapped_holdings = mapped_holdings.rename(columns=ticker_map)

    mapped_holdings = mapped_holdings.T.groupby(level=0).sum().T

    return mapped_holdings


def check_price_coverage(holdings: pd.DataFrame, prices: pd.DataFrame):
    matched = [ticker for ticker in holdings.columns if ticker in prices.columns]
    missing = [ticker for ticker in holdings.columns if ticker not in prices.columns]

    return matched, missing


def align_holdings_to_prices(holdings: pd.DataFrame, prices: pd.DataFrame):
    common_tickers = holdings.columns.intersection(prices.columns)

    aligned_holdings = holdings[common_tickers].copy()
    aligned_holdings = aligned_holdings.reindex(prices.index)
    aligned_holdings = aligned_holdings.ffill().fillna(0)

    return aligned_holdings
def compute_position_values(holdings: pd.DataFrame, prices: pd.DataFrame):
    common_tickers = holdings.columns.intersection(prices.columns)

    position_values = holdings[common_tickers] * prices[common_tickers]

    return position_values


def compute_total_portfolio_value(position_values: pd.DataFrame):
    total_value = position_values.sum(axis=1)
    total_value.name = "portfolio_value"

    return total_value


def build_daily_cash_balance(transactions: pd.DataFrame, prices: pd.DataFrame):
    cash = transactions.copy()

    cash = cash[["date", "balance"]]
    cash = cash.groupby("date")["balance"].last()

    cash = cash.reindex(prices.index)
    cash = cash.ffill().fillna(0)

    cash.name = "cash_balance"

    return cash

def compute_total_account_value(portfolio_value: pd.Series, cash_balance: pd.Series):
    total_account_value = portfolio_value + cash_balance
    total_account_value.name = "total_account_value"

    return total_account_value


def load_and_combine_transactions(paths: list[str]):
    frames = [load_transactions(path) for path in paths]

    combined = pd.concat(frames, ignore_index=True)
    combined = combined.drop_duplicates()
    combined = combined.sort_values("date")
    combined = combined.reset_index(drop=True)

    return combined