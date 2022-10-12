import backtrader as bt

from . import BaseStrategy as base


class CrossOver(base.Strategy):
    params = {
        'target_percent': 0.95
    }

    def __init__(self):
        base.Strategy.__init__(self)

        # Define Indicators
        self.sma5 = bt.indicators.MovingAverageSimple(period=5)
        self.sma30 = bt.indicators.MovingAverageSimple(period=30)
        self.buysell = bt.indicators.CrossOver(self.sma5, self.sma30, plot=True)

    def next(self):
        if self.order:
            # Skip if order is pending
            return

        if not self.position:
            if self.buysell > 0 or self.order_rejected:
                # Buy the up crossover
                self.log('BUY CREATE, {:.2f}'.format(self.data.close[0]))
                self.order = self.order_target_percent(target=self.params.target_percent)
                self.order_rejected = False
        else:
            if self.buysell < 0:
                # Sell the down crossover
                self.log('SELL CREATE, {:.2f}'.format(self.data.close[0]))
                self.order = self.close()

                

def backtest():
    cash = 10000
    symbols = None
    #start_date = '2018-01-01'
    data_dir = "Data/"  

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(cash)

    for s in symbols:            
            df = pd.read_csv(os.path.join(data_dir, s+".csv"), parse_dates=True, index_col=0)
            data = bt.feeds.PandasData(dataname=df)
            cerebro.adddata(data)
    # Strategy
    cerebro.addstrategy(CrossOver)


    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.SQN, _name='SQN')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
    
    # Backtest 
    
    print('Starting Portfolio Value: ',  cerebro.broker.getvalue())
    plt.rcParams['figure.figsize']=[10,6]
    plt.rcParams["font.size"]="12"

    # Run over everything
    results = cerebro.run()
    pnl = cerebro.broker.getvalue() - cash
    #cerebro.plot()
    # Print out the final result
    print('Final Portfolio Value: ',  cerebro.broker.getvalue()) 
    
    return pnl, results[0]    

#end of function for 'None' with capital '10000'
           
                