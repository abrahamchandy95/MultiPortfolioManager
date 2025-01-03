import yfinance as yf

class StockPriceFetcher:
    def __init__(self, adjusted_trades):
        self.adjusted_trades = adjusted_trades
        self.cur_index = 0

    def __len__(self):
        return len(set(self.adjusted_trades['ticker']))

    def __str__(self):
        prices = self.get_current_prices()
        return f"{prices}"

    def __getitem__(self, ticker):
        return self.get_open_price(ticker)

    def __iter__(self):
        self.cur_index = 0
        self.tickers = list(self.adjusted_trades['ticker'].unique())
        return self

    def __next__(self):
        if self.cur_index < len(self.tickers):
            ticker = self.tickers[self.cur_index]
            self.cur_index +=1
            return ticker
        else:
            raise StopIteration

    def get_open_price(self, ticker):
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get("regularMarketOpen")
        if price is None:
            raise ValueError(f"Unable to fetch price for ticker {ticker}")
        return price

    def get_current_prices(self):
        prices = {}
        tickers = list(self.adjusted_trades['ticker'].unique())
        for ticker in tickers:
            prices[ticker] = self.get_open_price(ticker)
        return prices
