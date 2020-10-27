import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import norgatedata
from datetime import datetime

from load_data import securities_pct, securities_df
from perf_funcs import *

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

if __name__ == '__main__':

    invested = 1000

    portfolio_value = invested * np.cumprod(1 + returns[sma_asset])

    # creating the index to compare our strategy to
    index = create_index(start=portfolio_value.index[0],
                         end=portfolio_value.index[-1],
                         index_ticker='SPY')

    # same initial investment as our backtested strategy
    index = index * invested

    # CAGR
    strat_cagr = cagr(portfolio_value)
    strat_cagr = '{:.2%}'.format(strat_cagr)

    # drawdowns
    drawdowns = drawdowns(portfolio_value)
    max_dd = min(drawdowns.fillna(0))
    max_dd = '{:.2%}'.format(max_dd)

    # volatility
    vol = volatility(portfolio_value)
    vol = '{:.2%}'.format(vol)

    strat_start = portfolio_value.index[0].strftime('%Y-%m-%d')
    strat_end = portfolio_value.index[-1].strftime('%Y-%m-%d')

    # plotting the performance of our backtest with an index
    perf_chart = backtest_perf_plot(equity_curve=portfolio_value,
                                    rolling_dd=drawdowns,
                                    comparison=True,
                                    index=index)
    plt.show()

    print('The CAGR for SPY 200d MA from {} to {} was {} with an annualized volatility of {}'.format(strat_start,
                                                                                                    strat_end,
                                                                                                    strat_cagr,
                                                                                                    vol))

    print('The Max Drawdown for SPY 200d MA between {} and {} was {}'.format(strat_start,
                                                                            strat_end,
                                                                            max_dd))




