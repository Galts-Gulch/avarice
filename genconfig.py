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
CandleSize = 5

# API secret + partner key
partner = 
secret_key = ''

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
## StochRSI (Stochastic RSI Oscillator)
# NOTE: lowest/highest are from RSIPeriod
# StochRSI = (RSI - Lowest RSI) / (Highest RSI - Lowest RSI)
#
## SMA (Simple Movement Average)
# NOTE: trading with SMA only is unsupported because it's a bad idea
# SMA = (Sum of last SMAPeriod candles) / SMAPeriod
Indicator = 'StochRSI'

# RSI Period and ask/bid triggers
# RSI Period can never be less than 3, but 14
# or higher is generally recommended.
# NOTE: RSI period is also used for RS calculations.
RSIPeriod = 14
RSIAsk = 70
RSIBid = 30

# StochRSI Period and ask/bid triggers
# NOTE: StochRSI requires RSIPeriod + StochRSIPeriod to begin
StochRSIPeriod = 14
StochRSIAsk = 95
StochRSIBid = 5

# SMA Period
SMAPeriod = 5

#
### Unused (but planned) configurables
#

# Max slippage percentage from market bid/ask
# Spreads the order points up/down
# NOTE: uses ADX and asset/currency TradeVolume
TradeMaxSlippage = 0.2
