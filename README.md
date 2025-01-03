# MultiPortfolioManager

MultiPortfolioManager is a Python-based application to manage multiple stock portfolios, 
including tracking trades, calculating profits, handling stock splits, and summing up dividends.

Use it to make a small mutual fund, or manage your family's stocks!

## Features
- **Trade Management**: Add, view, and manage stock trades.
- **Profit Calculation**: Calculate portfolio profit/loss.
- **Dividend Aggregation**: Summarize total dividends earned.
- **Stock Split Adjustment**: Automatically adjust trades for stock splits.

  ## Requirements
- Python 3.8+
- pandas
- yfinance

## Installation
Clone the repository and install the required dependencies:

```bash

git clone https://github.com/abrahamchandy95/MultiPortfolioManager.git
cd MultiPortfolioManager
pip install -r requirements.txt
```

## Usage
Run the following script on the terminal
```bash
python3 main.py <user> <action>
```
Action can be "data_entry", "profit", "dividends" or "summary"

Example:
```bash
python3 main.py mom summary
```
The trades information per user should be stored as a json file under data/trades/
but a csv/xlsx file can be used instead to upload all the trades done.
Columns of the file should include date, ticker, amount, quantity, price.
