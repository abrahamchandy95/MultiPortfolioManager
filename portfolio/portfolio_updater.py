import pandas as pd

from utils.utils import convert_to_ny_datetime

class PortfolioUpdater:
    def __init__(self, trades: pd.DataFrame):
        trades['date'] = pd.to_datetime(trades['date'])
        self.trades = trades

    def __str__(self, date=None):
        if date is not None:
            date = pd.to_datetime(date)
            trades = self.trades[self.trades['date']> date]
            return trades.to_string()
        return f"No date mentioned, see last trades: \n{self.trades.tail()}"

    def add_entry(self, date, ticker, amount, quantity, price):
        entry = pd.DataFrame(
            {
                'date': [pd.to_datetime(date)],
                'ticker': [ticker],
                'amount': [amount],
                'quantity': [quantity],
                'price': [price]
            }
        )
        self.trades = pd.concat([self.trades, entry], ignore_index=True)
        self.trades.sort_values('date', inplace=True)

    def add_entries_from_file(self, path):

        if str(path).endswith(".csv"):
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)

        df['date'] = pd.to_datetime(df['date'])
        self.trades = pd.concat([self.trades, df], ignore_index=True)
        self.trades.sort_values('date', inplace=True)

    def get_updated_trades_data(self):
        return self.trades

class StockSplitAdjuster:
    def __init__(self, original_trades, split_fetcher):
        self.trades = original_trades
        self.fetcher = split_fetcher
        self.adjusted_trades = None

    def __str__(self):

        return self.summarize_adjustments()

    def summarize_adjustments(self):

        if self.adjusted_trades is None:
            self.adjust_for_splits()

        if not self.fetcher.is_valid():
            self.fetcher.fetch_all_splits()

        tkrs = [t for t, s in self.fetcher.split_cache.items() if not s.empty]

        if tkrs:
            return f"Adjustments made for {len(tkrs)} tickers {', '.join(tkrs)}"
        else:
            return "StockSplitAdjustor: No Adjustments made."

    def adjust_for_splits(self):

        df = self.trades.copy()
        df['date'] = convert_to_ny_datetime(df['date'])

        if not self.fetcher.is_valid():
            self.fetcher.fetch_all_splits()

        for ticker, splits in self.fetcher.split_cache.items():
            if not splits.empty:
                for date, ratio in splits.items():
                    date = convert_to_ny_datetime(date)
                    rows = df[(df['ticker']==ticker) & (df['date'] < date)]
                    df.loc[rows.index, 'quantity'] *= ratio
                    df.loc[rows.index, 'price'] /= ratio
        self.adjusted_trades = df

    def get_adjusted_trades(self):
        if self.adjusted_trades is None or not self.fetcher.is_valid():
            if not self.fetcher.is_valid():
                self.fetcher.fetch_all_splits()
            self.adjust_for_splits()
        return self.adjusted_trades
