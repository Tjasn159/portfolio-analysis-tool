import pandas as pd

from features import (
    annualized_return,
    annualized_volatility,
    sharpe_ratio,
    drawdown_series,
    max_drawdown
)


def portfolio_returns(asset_returns: pd.DataFrame, weights: dict[str, float]) -> pd.Series:
    """
    Compute portfolio returns as the weighted sum of asset returns.

    The weights dictionary maps each ticker to its portfolio weight.
    The weights should sum to 1 for a fully invested portfolio.
    """
    weights_series = pd.Series(weights)
    return asset_returns[weights_series.index].mul(weights_series, axis=1).sum(axis=1)


def portfolio_growth(portfolio_rets: pd.Series, initial_value: float = 1.0) -> pd.Series:
    """
    Convert a return series into a growth series.

    This shows how an initial investment grows over time after
    compounding the portfolio's returns.
    """
    return initial_value * (1 + portfolio_rets).cumprod()


def portfolio_metrics(portfolio_rets: pd.Series, risk_free_rate: float = 0.0) -> pd.Series:
    """
    Compute basic portfolio-level performance metrics from a return series.

    Returns annualized return, annualized volatility, and Sharpe ratio.
    """
    portfolio_df = portfolio_rets.to_frame(name="portfolio")
    growth = portfolio_growth(portfolio_rets, 1.0)

    return pd.Series({
        "Annual Return": annualized_return(portfolio_df)["portfolio"],
        "Annual Volatility": annualized_volatility(portfolio_df)["portfolio"],
        "Sharpe": sharpe_ratio(portfolio_df, risk_free_rate)["portfolio"],
        "Max Drawdown": max_drawdown(growth)
    })


def portfolio_growth_df(portfolio_returns_df: pd.DataFrame, initial_value: float = 1.0) -> pd.DataFrame:
    """
    Convert a DataFrame of portfolio return series into cumulative growth curves.

    Each column is treated as a separate portfolio.
    """
    return initial_value * (1 + portfolio_returns_df).cumprod()

def compare_portfolios(asset_returns, porfolios):
    "Compare porfolio returnsin the form of Series"

    results = {}

    for name, weights in porfolios.items():
        returns = portfolio_returns(asset_returns, weights)

        results[name] = returns


    return pd.DataFrame(results)

def compare_portfolio_metrics(portfolio_returns_df):
    """
    Compute summary performance metrics for a single portfolio.

    Takes a portfolio return series and calculates annualized return,
    annualized volatility, Sharpe ratio, and maximum drawdown.
    """

    results = {}

    for name in portfolio_returns_df.columns:
        metrics = portfolio_metrics(portfolio_returns_df[name])

        results[name] = metrics

    return pd.DataFrame(results).T #transpose so it shows rows
    

