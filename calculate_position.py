import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import norgatedata
from datetime import datetime

from load_data import securities_pct, securities_df

sma_asset = 'SPY'
sma_lookback = 200

# creating the
securities_df['sma'] = securities_df[sma_asset].rolling(sma_lookback).mean()

# using .copy() avoids set with copy warnings
securities_df = securities_df[sma_lookback:].copy()
securities_pct = securities_pct[sma_lookback:].copy()

# default is position of 0, this is when sma_asset < moving average
securities_df['position'] = 0

# when sma_asset > moving average we are long
securities_df.loc[securities_df[sma_asset] > securities_df['sma'], 'position'] = 1

returns = securities_pct

returns[sma_asset] *= securities_df['position']


test = np.cumprod(1 + returns['SPY'])

# just by this we can tell that the strategy has lookahead bias - generated from line 23
# need to add a 1 day delay to making change to fix this
test.plot()
plt.show()


