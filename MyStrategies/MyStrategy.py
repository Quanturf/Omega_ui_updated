import backtrader as bt
import pandas as pd
import os
import matplotlib.pyplot as plt
import yfinance as yf
from .BaseStrategy import *


class BuyAndHold(Strategy):
    params = (
        ('target_percent', 0.99),
    )

    def __init__(self):
        Strategy.__init__(self)

    def buy_and_hold(self):
        for d in self.datas:
            split_target = self.params.target_percent / len(self.datas)
            self.order_target_percent(d, target=split_target)

    def next(self):
        if not self.position:
            self.buy_and_hold()

        elif self.order_rejected:
            self.buy_and_hold()
            self.order_rejected = False

                

def backtest():
    cash = 10000
    symbols = ['AAPL']
    #start_date = '2018-01-01'
    data_dir = "Data/"  

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(cash)

    for s in symbols:
        data = bt.feeds.PandasData(dataname=yf.download(s, '2021-07-06', '2022-07-01', auto_adjust=True))
        cerebro.adddata(data)

    # Strategy
    cerebro.addstrategy(BuyAndHold)

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

#end of function for '['AAPL']' with capital '10000'
           
                