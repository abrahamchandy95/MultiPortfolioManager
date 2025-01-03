class CostCalculator:

    def __init__(self, trades):
        self.trades = trades
        self.stock_costs = {}

    def __len__(self):
        return len(self.trades['ticker'].unique())

    def __str__(self):

        if self.stock_costs is None:
            self.calculate_stock_costs()

        return f"{self.stock_costs}"

    def calculate_total_spent(self):

        total = (self.trades['quantity'] * self.trades['price']).sum()

        return round(float(total), 2)

    def calculate_stock_costs(self):

        self.trades['total_cost'] = self.trades['quantity'] * self.trades['price']
        trades = self.trades.groupby('ticker')
        costs = trades['total_cost'].sum()
        self.stock_costs = costs.round(2).to_dict()

    def calculate_average_cost_per_share(self, ticker):

        if not self.stock_costs:
            self.calculate_stock_costs()

        if ticker in self.stock_costs:

            t_trades = self.trades[self.trades['ticker'] == ticker]
            num_stocks = float(t_trades['quantity'].sum())
            total_cost = self.stock_costs[ticker]

            return round(total_cost/num_stocks, 2)

        else:

            return 0

    def summarize_costs(self):

        self.trades['total_cost'] = self.trades['quantity'] *\
            self.trades['price']

        trades = self.trades.groupby('ticker')
        trades = trades.agg(
            total_quantity=('quantity', 'sum'),
            total_cost=('total_cost', 'sum')
        )
        trades['average_cost'] = trades['total_cost'] / trades['total_quantity']
        trades['average_cost'] = trades['average_cost'].round(2)

        return trades.reset_index()
