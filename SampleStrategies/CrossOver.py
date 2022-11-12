import backtrader as bt
import pandas as pd
import os
import matplotlib.pyplot as plt
import yfinance as yf
from .BaseStrategy import *
#base.Strategy

class CrossOver(Strategy):
    params = {
        'target_percent': 0.95
    }

    def __init__(self):
        Strategy.__init__(self)

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
