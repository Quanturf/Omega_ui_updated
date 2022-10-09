import logging
import os
import pandas as pd

import backtrader as bt
import yfinance as yf
import matplotlib.pyplot as plt


class TestStrategy(bt.Strategy):
    """Test Strategy to check data is loaded correctly"""
    params = (('param1', 10), ('param2', 20))

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.date = self.datas[0].datetime.date
        self.dataclose = self.datas[0].close
        self.order = None  # To keep track of pending orders
        self.log(logging.INFO, 'Strategy Initialized!')
        self.log(logging.INFO, 'Param1: {} - Param2: {}'.format(self.p.param1, self.p.param2))

    def log(self, level, message):
        self.logger.log(level, '{} - {}'.format(self.date(0), message))

    def next(self):
        if self.order:
            return
        # Debugging
        self.log(logging.DEBUG, 'Close price: {}'.format(self.dataclose[0]))

        # Current close less than previous close
        if self.dataclose[0] < self.dataclose[-1]:
            # Previous close less than the previous close
            if self.dataclose[-1] < self.dataclose[-2]:
                self.log(logging.INFO, 'Buy @ {}'.format(self.dataclose[0]))
                self.order_target_percent(target=0.25)
        # Current close greater than previous close
        if self.dataclose[0] > self.dataclose[-1]:
            # Previous close greater than the previous close
            if self.dataclose[-1] > self.dataclose[-2]:
                self.log(logging.INFO, 'Sell @ {}'.format(self.dataclose[0]))
                self.order_target_percent(target=-0.25)
                

def backtest():
    cash = 10000
    symbols = ['AMZN', 'AAPL', 'MSFT']
    #start_date = '2018-01-01'
    path_dir = 'D:\Python\OmegaUI_codeGenerator\omega_ui'  

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(cash)

    for s in symbols:            
            df = pd.read_csv(os.path.join(path_dir, s+".csv"), parse_dates=True, index_col=0)
            data = bt.feeds.PandasData(dataname=df)
            cerebro.adddata(data)
    # Strategy
    cerebro.addstrategy(TestStrategy)


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

#end of function for '['AMZN', 'AAPL', 'MSFT']' with capital '['AMZN', 'AAPL', 'MSFT']'
           
                