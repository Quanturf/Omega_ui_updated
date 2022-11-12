import numpy as np
import backtrader as bt
import pandas as pd
import os
import matplotlib.pyplot as plt
import yfinance as yf
from .BaseStrategy import *


class LeveragedEtfPair(Strategy):
    """
    Use as data two oposing weighted ETFs, ex: SSO & SDS

    :data: 2 datafeeds, the first a positive leveraged ETF, and the second negatively leveraged.
    """

    params = {
        'leverages': [1, 1],
        'rebalance_days': 21,
        'target_percent': -0.95
    }

    def __init__(self):
        Strategy.__init__(self)
        assert len(self.datas) == 2, "Exactly 2 datafeeds needed for this strategy!"

        self.leverages = np.abs(self.params.leverages)
        self.leverages = self.params.target_percent * self.leverages / sum(self.leverages)

    def rebalance(self):
        for i, d in enumerate(self.datas):
            self.order_target_percent(d, self.leverages[i])

    def next(self):
        if self.order:
            # Skip if order is pending
            return

        # Rebalance portfolio
        if len(self) % self.params.rebalance_days == 0:
            self.rebalance()

        # Retry order on next day if rejected
        elif self.order_rejected:
            self.rebalance()
            self.order_rejected = False
