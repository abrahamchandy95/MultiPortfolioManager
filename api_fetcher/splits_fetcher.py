import pandas as pd
import yfinance as yf

class StockSplitFetcher:
    def __init__(self, all_trades):
        self.trades = all_trades
        self.tickers = list(all_trades['ticker'].unique())
        self.split_cache = {}
        self.cache_date = None

    def __len__(self):
        return sum(1 for val in self.split_cache.values() if not val.empty)

    def __str__(self):
        if not self.split_cache:
            self.fetch_all_splits()
        return f"{self.split_cache}"

    def is_valid(self):
        "cache expires when not refreshed today"
        today = pd.Timestamp.now().normalize()
        if self.cache_date is None or self.cache_date < today:
            self.cache_date = today
            return False

        return True

    def clear_cache(self):
        self.split_cache = {}

    def fetch_splits(self, ticker, earliest):

        earliest = pd.Timestamp(earliest).tz_localize("America/New_York")

        if not self.is_valid():
            self.clear_cache()

        if ticker not in self.split_cache:

            stock = yf.Ticker(ticker)
            splits = stock.splits
            splits_after_purchase = splits.index > earliest
            relevant_splits = splits[splits_after_purchase]
            self.split_cache[ticker] = relevant_splits

        else:

            relevant_splits = self.split_cache[ticker]

        return relevant_splits

    def fetch_all_splits(self):
        for ticker in self.tickers:
            earliest_date = self.trades[self.trades['ticker'] == ticker]['date'].min()
            self.fetch_splits(ticker, earliest_date)
