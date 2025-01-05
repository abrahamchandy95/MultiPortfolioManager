import pandas as pd
import yfinance as yf

from utils.utils import convert_to_ny_datetime

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
            new_index = convert_to_ny_datetime(dividends.index)
            # Assert that the converted index is indeed a DatetimeIndex
            assert isinstance(new_index, pd.DatetimeIndex), "Index type error"
            # Assign the converted index back to dividends
            dividends.index = new_index
            if start_date:
                start_date = convert_to_ny_datetime(start_date)
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
