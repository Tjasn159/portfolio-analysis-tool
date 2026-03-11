# Portfolio Analysis Tool

A small Python project for analyzing asset performance and constructing simple portfolios from historical price data.

The goal of this project is to build a lightweight framework that can:
- download historical price data
- compute financial return metrics
- visualize asset performance
- simulate portfolio allocations
- compare portfolio performance against individual assets

This project is being built incrementally as a learning exercise in financial data analysis and Python project structure.

---

## Current Features

### Data Pipeline
- Download historical prices using yfinance
- Store raw price data locally
- Load price data for analysis

### Return Calculations
- Simple returns
- Log returns
- Annualized return
- Annualized volatility
- Sharpe ratio

### Asset Analysis
- Cumulative growth visualization
- Log return distribution analysis

### Portfolio Engine
- Construct portfolios from asset weights
- Compute portfolio return series
- Compute portfolio metrics
- Compare portfolio growth to individual assets

---

## Project Structure


portfolio-analysis-tool
│
├─ data
│  ├─ raw
│  │  └─ prices.csv
│
├─ notebooks
│  └─ 01_exploratory_analysis.ipynb
│
├─ src
│  ├─ config.py
│  ├─ data_load.py
│  ├─ features.py
│  └─ portfolio.py
│
├─ requirements.txt
└─ README.md


---

## Example Portfolio

Example portfolio allocation used in testing:

- AAPL 30%
- MSFT 30%
- GOOGL 20%
- AMZN 10%
- TSLA 10%

The portfolio return series is computed as the weighted sum of individual asset returns.

Portfolio growth is then obtained through cumulative compounding of the return series.
---

## Technologies Used

- Python
- pandas
- numpy
- matplotlib
- yfinance

---

## Future Work

Planned extensions include:

- portfolio comparison tools
- transaction ledger support
- portfolio rebalancing
- benchmark comparisons
- additional risk metrics
- portfolio optimization

---

## AI Assistance

Some code structure, debugging guidance, and design suggestions were developed with the assistance of AI tools. All code was reviewed, implemented, and tested manually as part of the learning process.