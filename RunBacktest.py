
class ExampleBacktest(ob.Backtest):
    def get_symbols(self):
        return ['AAPL', 'MSFT', 'TestData']

    def get_parameters(self, strategy, symbols):
        return {'param1': 10, 'param2': 20}

    def run(self, symbols, cash, strategy, **params):
        path_dir = os.path.dirname(os.path.realpath(__file__))
        # Setup Cerebro
        #cerebro = ob.Backtest.setup_cerebro(cash)
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(cash)
        # Add Data
        for s in symbols:
            df = pd.read_csv(os.path.join(path_dir, '{}.csv'.format(s)), parse_dates=True, index_col=0)
            data = bt.feeds.PandasData(dataname=df)
            cerebro.adddata(data)

        data = bt.feeds.PandasData(dataname=yf.download('TSLA', '2018-01-01', '2018-01-10'))
        cerebro.adddata(data)

        # Strategy
        cerebro.addstrategy(strategy, **params)
        
        
        cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        cerebro.addanalyzer(bt.analyzers.SQN, _name='SQN')
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
        #cerebro.adddata(data)
        # Backtest
        results = cerebro.run()
        pnl = cerebro.broker.getvalue() - cash

        return pnl, results[0]
