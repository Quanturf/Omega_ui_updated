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
