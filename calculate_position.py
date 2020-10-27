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

# when sma_asset > moving average we are long - adding shift to remove lookahead bias
# take a look at everything again this seems strange
securities_df.loc[securities_df[sma_asset].shift(1) > securities_df['sma'], 'position'] = 1

# the percentage returns that we'll multiply the position by to get the daily returns for the position
returns = securities_pct

# multiplying the returns of the asset we're testing the sma on, by the position value
# if long position = 1*return, if not long = 0*return
returns[sma_asset] *= securities_df['position']




