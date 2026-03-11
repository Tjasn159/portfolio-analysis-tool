import pandas as pd

from features import (
    annualized_return,
    annualized_volatility,
    sharpe_ratio,
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

    return pd.Series({
        "Annual Return": annualized_return(portfolio_df)["portfolio"],
        "Annual Volatility": annualized_volatility(portfolio_df)["portfolio"],
        "Sharpe": sharpe_ratio(portfolio_df, risk_free_rate)["portfolio"],
    })