import numpy as np
import pandas as pd

TRADING_DAYS_PER_YEAR = 252


def simple_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Convert price levels into daily percentage returns.

    Returns measure relative change from one day to the next and
    allow meaningful comparison between assets with different prices.
    """
    returns = prices.pct_change()
    returns = returns.dropna(how="all")
    return returns


def log_returns(simple_rets: pd.DataFrame) -> pd.DataFrame:
    """
    Convert simple returns into log returns using ln(1 + r).

    Log returns are commonly used in finance because they are
    additive across time and convenient for modeling.
    """
    return np.log1p(simple_rets)


def annualized_return(simple_rets: pd.DataFrame) -> pd.Series:
    """
    Estimate annual return by scaling the mean daily return by
    the typical number of trading days in a year (252).
    """
    return simple_rets.mean() * TRADING_DAYS_PER_YEAR


def annualized_volatility(simple_rets: pd.DataFrame) -> pd.Series:
    """
    Measure annualized volatility of returns. Volatility reflects
    how much returns fluctuate and is a common proxy for risk.
    """
    return simple_rets.std() * np.sqrt(TRADING_DAYS_PER_YEAR)


def sharpe_ratio(simple_rets: pd.DataFrame, risk_free_rate: float = 0.0) -> pd.Series:
    """
    Compute the Sharpe ratio, which measures return earned per unit
    of risk by comparing annualized return to annualized volatility.
    """
    ann_ret = annualized_return(simple_rets)
    ann_vol = annualized_volatility(simple_rets)
    return (ann_ret - risk_free_rate) / ann_vol


def drawdown_series(values: pd.Series) -> pd.Series:
    """
    Compute the drawdown series, showing how far the value has fallen
    from its previous peak at each point in time.
    """
    running_max = values.cummax()
    return values / running_max - 1


def max_drawdown(values: pd.Series) -> float:
    """
    Return the largest peak-to-trough loss observed in the series.
    """
    dd = drawdown_series(values)
    return dd.min()