import logging
import os
import pandas as pd

import backtrader as bt
import yfinance as yf


class StatsTest(bt.Strategy):
    """
    Test Strategy to check some statistics

    This strategy should be used with TestData.csv

    TestData.csv will rise from 1 dollar to 101 dollars over 20 bars then fall
    from 101 to 1 over the next 20 bars. (40 bar round trip). The pattern will
    repeat in a loop until the end of the data set.

    The first two bars close/open at 1 dollar to ease testing with market orders
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.date = self.datas[0].datetime.date
        self.dataclose = self.datas[0].close
        self.buy_bars = [1, 21, 41, 61]
        self.close_bars = [20, 40, 60, 80]
        self.sell_bars = []
        self.log(logging.INFO, 'Strategy Initialized!')

    def next(self):
        bar = len(self.data)
        if bar in self.buy_bars:
            print('Buying On Bar {} Price = {}'.format(bar, self.dataclose[0]))
            self.buy(stake=1)
            self.log(logging.INFO, 'Buy @ {}'.format(self.dataclose[0]))
        elif bar in self.close_bars:
            print('Closing On Bar {} Price = {}'.format(bar, self.dataclose[0]))
            self.close(stake=1)
            self.log(logging.INFO, 'Exit @ {}'.format(self.dataclose[0]))
        else:
            pass

    def log(self, level, message):
        self.logger.log(level, '{} - {}'.format(self.date(0), message))




                

def backtest():
    cash = 10000
    symbols = None
    #start_date = '2018-01-01'
    path_dir = 'D:\Python\OmegaUI_codeGenerator\omega_ui'                
    ticker = None
    df = si.get_analysts_info(ticker)['EPS Trend'].assign(hack='').set_index('hack')

    ticker = 10000
    df = si.get_analysts_info(ticker)['Growth Estimates'].assign(hack='').set_index('hack')

    ticker = 'None'
    df = si.get_analysts_info(ticker)['Earnings Estimate'].assign(hack='').set_index('hack')
           
                