# avarice
*(noun) extreme greed for wealth or material gain.*

*Greed captures the essence of the evolutionary spirit.*
-Gordon Gekko

## Disclaimer
- This software is in a very WIP state.
- It is not recommended to live trade at all, and any assets you may lose are your own responsibility.

## Notes
- This software is expected to run continuously to get valid data. We dropped support for database resuming, but *may* bring it back at some point.
- All (very minimal) testing is done on current Python3.5.
- Though all indicators run all the time, only one may **currently** be actively traded on. This will change soon.

## Indicators
**SMA (Simple Movement Average)**
- NOTE: SMA is only here to be used by other indicators
- SMA = (Sum of last SMAPeriod candles) / SMAPeriod

**EMA (Exponential Movement Average)**
- NOTE: does two calculations using EMAShort and EMALong.
- We trade this as a crossover (convergence/divergence) indicator. This is the correct strategy for EMA, and those expecting buy/sell thresholds are thinking of DEMA. On 10/21, when EMA10 > EMA21, we sell (and visa versa). Differs from MACD due to lack of third signal line.
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

**StdDev (Sampled Standard Deviation)**
- NOTE: Only here to be used by other volatility indexes
- The following is ripped/edited from stockcharts.com since it summarizes the Std Dev calculations quite well:
1. Calculate the average (mean) price for the number of periods or observations.
2. Determine each period's deviation (close less average price).
3. Square each period's deviation.
4. Sum the squared deviations.
5. Divide this sum by the number of samples.
6. The standard deviation is then equal to the square root of that number.

## TODO
- Add PeriodDivisor support, modify indicator periods based on a volatility index (bollinger bandwidth to start). In a lot of research, this gets rid of the need for "stop loss" in most cases for going into "uncharted" territory.
- More indicators
- Separate strategies from trader
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

## Donations
Donations are not at all required, or even really requested. If you want to show a "thank you," and can't contribute code, then feel free to donate.
BTC: 18XCHsFFpnSWv2GZTbQbXtGTSQGrZABueZ
