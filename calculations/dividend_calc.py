import pandas as pd
from api_fetcher import DividendFetcher

class DividendCalculator:
    def __init__(self, trades: pd.DataFrame):

        self.trades = trades.copy()
        self.normalize_dates()
        self.dividends: pd.DataFrame = pd.DataFrame()

    def normalize_dates(self):
            """
            Ensure dates are timezone-aware and normalized to 'America/New_York'.
            """
            if self.trades['date'].dt.tz is None:
                self.trades['date'] = self.trades['date'].dt.tz_localize('America/New_York')
            else:
                self.trades['date'] = self.trades['date'].dt.tz_convert('America/New_York')

    def get_earliest_date(self):

        return self.trades['date'].min()

    def fetch_dividends(self):
        """
        Fetch dividends for all tickers in the portfolio.
        """
        tickers = self.trades['ticker'].unique()
        start_date = self.get_earliest_date()
        fetcher = DividendFetcher(tickers)
        self.dividends = fetcher.fetch_all_dividends(start_date)

    def calculate_dividends_per_stock(self):
        if self.dividends.empty:
            self.fetch_dividends()

        if self.dividends.empty:
            return {}

        total_dividends = {}

        for ticker in self.trades['ticker'].unique():
            trades = self.trades[self.trades['ticker'] == ticker]
            dividends = self.dividends[self.dividends['ticker'] == ticker]

            total = 0

            for _, row in dividends.iterrows():
                issue_date = row['date']
                amt = row['dividend']
                shares_owned = trades[trades['date'] < issue_date]['quantity'].sum()

                total += (shares_owned * amt)

            total_dividends[ticker] = round(float(total), 2)

        return total_dividends

    def aggregate_dividends(self):
        divs = self.calculate_dividends_per_stock()
        summ = 0
        for ticker in divs:
            summ += divs[ticker]
        return summ
