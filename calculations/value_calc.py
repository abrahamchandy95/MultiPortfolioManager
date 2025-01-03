class MarketValuator:
    def __init__(self, cur_prices, adjusted_trades):
        self.prices = cur_prices
        self.trades = adjusted_trades.copy()

    def __len__(self):
        return len(self.prices)

    def __str__(self):
        total_value = self.calculate_total()
        return f"Total Market Value of Portfolio: ${total_value:,.2f}"

    def get_valuation(self):

        self.trades['current_price'] = self.trades['ticker'].map(self.prices)
        self.trades['market_value'] = self.trades['current_price'] *\
            self.trades['quantity']
        grouped = self.trades.groupby('ticker')
        summary = grouped.agg(
            total_quantity=('quantity', 'sum'),
            current_price=('current_price', 'first'),
            market_value =('market_value', 'sum')
        ).reset_index()
        return summary

    def calculate_total(self):
        valuation = self.get_valuation()
        return round(float(valuation['market_value'].sum()), 2)
