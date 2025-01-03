import pandas as pd
import yfinance as yf

class DividendFetcher:
    def __init__(self, tickers):
        self.tickers = tickers
        self.dividend_tickers = set()

    def __str__(self):
        return f"Tracking dividends for: {', '.join(self.tickers)}"

    def __len__(self):
        if not self.dividend_tickers:
            self.fetch_all_dividends()
        return len(self.dividend_tickers)

    def fetch_all_dividends(self, start_date=None):
        all_dividends = []

        for ticker in self.tickers:
            stock = yf.Ticker(ticker)
            dividends = stock.dividends
            if isinstance(dividends.index, pd.DatetimeIndex):
                if dividends.index.tz is None:
                    dividends.index = dividends.index.tz_localize('America/New_York')

            if start_date:
                start_date = pd.to_datetime(start_date)

                # If start_date is tz-naive, localize it; otherwise, convert its timezone
                if start_date.tzinfo is None:
                    start_date = start_date.tz_localize('America/New_York')
                else:
                    start_date = start_date.tz_convert('America/New_York')

                # Filter dividends
                dividends = dividends[dividends.index > start_date]

            if not dividends.empty:
                dividends_df= pd.DataFrame(
                    {
                        'date': dividends.index,
                        'dividend': dividends.values
                    }
                )
                dividends_df['ticker'] = ticker
                all_dividends.append(dividends_df)
        if all_dividends:
            return pd.concat(all_dividends, ignore_index=True)
        return pd.DataFrame()
