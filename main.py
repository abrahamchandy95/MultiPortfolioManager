import argparse
import json
import os
import pandas as pd

from portfolio.portfolio_updater import PortfolioUpdater, StockSplitAdjuster
from api_fetcher import StockSplitFetcher, StockPriceFetcher
from calculations import (
    CostCalculator, MarketValuator, DividendCalculator
)

def get_user_files(user):
    data_path = "data"
    trades_path = os.path.join(data_path, "trades", f"{user}Trades.json")
    return trades_path

def load_user_trades(trades_path) -> pd.DataFrame:
    try:
        with open(trades_path, 'r') as f:
            df = pd.DataFrame(json.load(f))
            df['date'] = pd.to_datetime(df['date'], unit='ms')
            return df
    except FileNotFoundError:
        return pd.DataFrame(
            columns=['date', 'ticker', 'amount', 'quantity', 'price'] #type: ignore
        )

def save_user_trades(df: pd.DataFrame, trades_path):
    os.makedirs(os.path.dirname(trades_path), exist_ok=True)
    df.to_json(trades_path, orient='records', indent=4)

def do_data_entry(trades):
    updater = PortfolioUpdater(trades)
    print(
        """
        Choose an option:
            1. Add a single entry
            2. Add entries from csv or excel
        """
    )
    choice = input("Enter choice")
    if choice == "1":
        date = input("Enter date (YYYY-MM-DD): ")
        ticker = input("Enter ticker: ")
        amount = float(input("Enter amount spent: "))
        quantity = float(input("Enter quantity: "))
        price = float(input("Enter price during purchase: "))
        updater.add_entry(date, ticker, amount, quantity, price)
    elif choice == "2":
        path = input("Enter file path: ").strip()
        updater.add_entries_from_file(path)
    else:
        print("Invalid choice.")
    return updater.get_updated_trades_data()

def display_profit(trade_summary):
    net_worth = float(trade_summary['market_value'].sum())
    agg_cost = float(trade_summary['total_cost'].sum())
    profit = net_worth - agg_cost
    print(
        f"Total Value: ${net_worth: .2f} | "
        f"Total Spent: ${agg_cost: .2f} | "
        f"Profit: ${profit: .2f}"
    )

def display_dividends(adjusted_trades):
    dividendor = DividendCalculator(adjusted_trades)
    dividends = dividendor.aggregate_dividends()
    print(f"Total Dividends: ${dividends: .2f}")

def create_summary(coster, valuator):
    costs = coster.summarize_costs()
    values = valuator.get_valuation()
    summary = pd.merge(costs, values, on=['ticker', 'total_quantity'], how='inner')
    summary['profit_loss'] = summary['market_value'] - summary['total_cost']
    # remove entries where all stocks have been sold
    summary = summary[summary['quantity'].round(3) > 0.000]
    return summary

def main():
    parser = argparse.ArgumentParser(description="Manage your portfolio.")
    parser.add_argument(
        "user", help="Specify the user"
    )
    parser.add_argument(
        "action", choices=[
            "data_entry",
            "profit",
            "dividends",
            "summary"
        ],
        help="Action to perform."
    )
    args = parser.parse_args()

    trades_file = get_user_files(args.user)
    trades = load_user_trades(trades_file)

    if trades.empty:
        print("No trades found. Please add trades using 'data_entry'.")
        return

    # get trades after adjusting for splits
    splits_fetcher = StockSplitFetcher(trades)
    splits_adjustor = StockSplitAdjuster(trades, splits_fetcher)
    adjusted_trades = splits_adjustor.get_adjusted_trades()

    # get current price
    price_fetcher = StockPriceFetcher(adjusted_trades)
    cur_prices = price_fetcher.get_current_prices()

    # get summary - cost and value
    coster = CostCalculator(adjusted_trades)
    valuator = MarketValuator(cur_prices, adjusted_trades)
    summary = create_summary(coster, valuator)

    if args.action == "data_entry":
        trades = do_data_entry(trades)
        save_user_trades(trades, trades_file)

    elif args.action == "profit":
        display_profit(summary)

    elif args.action == "dividends":
        display_dividends(adjusted_trades)

    elif args.action == "summary":
        print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
