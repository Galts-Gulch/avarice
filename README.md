# avarice
*(noun) extreme greed for wealth or material gain.*

*Greed captures the essence of the evolutionary spirit.*
-Gordon Gekko

## Disclaimer
- This software is in a very WIP state.
- It is not recommended to live trade at all, and any assets you may lose are your own responsibility.

## Notes
- All (very minimal) testing is done on current Python3.5.
- Though all indicators run all the time, only one may **currently** be actively traded on. This will change soon.

## Indicators
**SMA (Simple Movement Average)**
- NOTE: SMA is only here to be used by other indicators
- SMA = (Sum of last SMAPeriod candles) / SMAPeriod

**EMA (Exponential Movement Average)**
- NOTE: does two calculations using EMAShort and EMALong.
- We trade this as a crossover (convergence) indicator. On 10/21, when EMA10 > EMA21, we sell (and visa versa).
- The first iteration uses SMA to generate the first EMA.
- Multiplier = (2 / EMAPeriod) + 1
- EMA = ((Current Close - Previous EMA) * Multiplier) + Previous EMA

**RSI (Relative Strength Index Oscillator)**
- NOTE: avg gains andlosses are smoothed after first iteration
- RS = avg_gain / avg_loss
- RSI = 100 - (100 / (1 + RSI))

**FastStochRSI (Stochastic RSI Oscillator)**
- NOTE: lowest/highest are from RSIPeriod
- FastStochRSIK = ((RSI - Lowest RSI) / (Highest RSI - Lowest RSI)) * 100
- FastStochRSID = FastStochRSIDPeriod SMA of FastStochRSIK

**FullStochRSID**
- FullStochasticRSID = FullStochRSIDPeriod SMA of FastStochRSID

**FastStochK (Fast Stochastic Oscillator %K)**
- FastStochasticK = ((Current Close - Low) / (High - Low)) * 100

**FastStochD**
- FastStochasticD = FastStochDPeriod SMA of %K

**FullStochD**
- NOTE: FullStochK is not includes since it's equivalent to FastStochD
- FullStochasticD = FullStochDPeriod SMA of Fast %D

## TODO
- More indicators
- Implement a few well tested multi-indicator strategies from my c++ trade infrastructure, including bayesian targeted, bfsg optimized spread code (the latter might be done via non python since it's already c++ and I'm lazy)
- Support "Max Trade Slippage" using ADX and asset + currency trade volume, and bollinger bands with bollbandwidth = (PeriodBandHigh - PeriodBandLow) / (PeriodBandSum / Period) to verify
- Clean up a lot
- Record at candle market depth in a new sqlite table, break markets into child markets for better economic significance backtesting (cryptotrader "at market" style backtesting is a joke in the economics world).
- Probably rework into real classes

## Contributing
- Ensure your editor is set to use 4 spaces for tab (smartindent, tabstop=4, shiftwidth=4 in vim)
- Please no lines greater than 75char, with <= 70 preferred (in rare cases, exceeding can aid readability)
- Fork, commit, submit pull request.

## Running
- Be sure you have simplejson, if not install it for python3.y (API dependency)
- Clone
- Edit genconfig.py; find your own successful configuration
- Run avarice.py - This software is meant to be run continuously, and will take awhile to generate valid info depending on configuration.
