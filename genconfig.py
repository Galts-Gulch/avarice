## General configurables

# Database path
DatabasePath = "./sqlite"

# Asset_currency to trade in.
# May additionally be ltc_cny
# NOTE: change asset with pair
TradePair = 'btc_cny'
Asset = TradePair[:3]
Currency = TradePair[-3:]

# NOTE: Always sells/buys at market bid/ask
LiveTrading = False

# Percentage of total (so 50 is 50%).
# NOTE: this is percentage of asset and currency
# This is re-evaluated for each trade
TradeVolume = 50

# How many candles with indicator info before
# allowing trades?
# NOTE: must be greater than 1, and an integer
TradeDelay = 3

# In minutes; used for all indicator assessments/trade freq
CandleSize = 10

# API secret + partner key
partner = 111111111
secret_key = 'stub'

# Debug flag only used to avoid dropping db table.
# Makes development easier/faster.
# NOTE: only ever run if developing, not for accuracy.
Debug = False


#
### Indicators
#

## RSI (Relative Strength Index Oscillator)
# NOTE: avg gains andlosses are smoothed after first iteration
# RS = avg_gain / avg_loss
# RSI = 100 - (100 / (1 + RSI))
#
## StochRSIK (StochasticK RSI Oscillator)
# NOTE: lowest/highest are from RSIPeriod
# StochRSIK = ((RSI - Lowest RSI) / (Highest RSI - Lowest RSI)) * 100
#
## SMA (Simple Movement Average)
# NOTE: SMA is only here to be used by other indicators
# SMA = (Sum of last SMAPeriod candles) / SMAPeriod
#
## FastStochK (Fast Stochastic Oscillator %K)
# FastStochasticK = ((Current Close - Low) / (High - Low)) * 100
#
## TODO: FastStochD
# FastStochasticD = FastStochDPeriod SMA of %K

# List of all indicators which should run
# NOTE: Order matters
IndicatorList = ['RSI','FastStochRSIK','FastStochRSID','SMA',\
        'FastStochK','FastStochD']

# The indicator that should be traded off
# TODO: implement trade strategies separately
Indicator = 'FastStochRSIK'

# RSI Period and ask/bid triggers
# RSI Period can never be less than 3, but 14
# or higher is generally recommended.
# NOTE: RSI period is also used for RS calculations.
RSIPeriod = 14
RSIAsk = 70
RSIBid = 30

# FastStochRSI Oscillator Period and ask/bid triggers
# NOTE: FastStochRSIK requires RSIPeriod + FastStochRSIPeriod + 2 to begin
# FastStochDRSI requires FastStochRSIK * FastStochRSIDPeriod
FastStochRSIKPeriod = 14
FastStochRSIKAsk = 95
FastStochRSIKBid = 5
FastStochRSIDPeriod = 3
FastStochRSIDAsk = 95
FastStochRSIDBid = 5

# SMA Period
SMAPeriod = 10

# FastStoch Oscillator Periods and ask/bid triggers
FastStochKPeriod = 14
FastStochKAsk = 95
FastStochKBid = 5
FastStochDPeriod = 3
FastStochDAsk = 90
FastStochDBid = 10

#
### Unused (but planned) configurables
#

# Max slippage percentage from market bid/ask
# Spreads the order points up/down
# NOTE: uses ADX and asset/currency TradeVolume
TradeMaxSlippage = 0.2
