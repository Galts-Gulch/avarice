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
# Simulate or Live Trade?
SimulatorTrading = True
SimulatorAsset = 1
SimulatorCurrency = 3000

# Percentage of total (so 50 is 50%).
# NOTE: this is percentage of asset and currency
# This is re-evaluated for each trade
TradeVolume = 40

# How many candles with indicator info before
# allowing trades?
# NOTE: must be greater than 1, and an integer
TradeDelay = 3

# In minutes; used for all indicator assessments/trade freq
CandleSize = 15

# API secret + partner key
partner = 111111111
secret_key = 'stub'

# Debug flag only used to avoid dropping db table.
# Makes development easier/faster.
# NOTE: only ever run if developing, not for accuracy.
Debug = False


#
### Indicators - See README.md for more info
#

# List of all indicators which should run
# NOTE: Order matters
IndicatorList = ['RSI','FastStochRSIK','FastStochRSID',\
        'FullStochRSID','SMA','EMA','DEMA','FastStochK','FastStochD',\
        'FullStochD','StdDev','BollBands','BollBandwidth']

# The indicator that should be traded off
Indicator = 'FastStochRSID'

# SMA Period
SMAPeriod = 10

# EMA short and long periods, ema strategy, and diff thresholds
# NOTE: EMA trade strategies have been split into two trading
# strategies; CD and Diff.
EMAShort = 10
EMALong = 21
EMADiffDown = -0.025
EMADiffUp = 0.025
EMAStrategy = 'CD'

# DEMA Diffs. Uses both EMALong and EMAShort from above.
# NOTE: uses EMAStrategy from above
DEMADiffDown = -0.025
DEMADiffUp = 0.025

# RSI Period and ask/bid triggers
# RSI Period can never be less than 3, but 14
# or higher is generally recommended.
# NOTE: RSI period is also used for RS calculations.
RSIPeriod = 14
RSIAsk = 70
RSIBid = 30

# FastStochRSI Oscillator Period and ask/bid triggers
# NOTE: We do not use 80/20 for Stoch %K due to oscillator volatility
# NOTE: FastStochRSIK requires RSIPeriod + FastStochRSIPeriod + 2 to begin
# NOTE: %D uses %K periods, %D periods are SMA periods of %K
# FastStochDRSI requires FastStochRSIK * FastStochRSIDPeriod
FastStochRSIKPeriod = 14
FastStochRSIKAsk = 95
FastStochRSIKBid = 5
FastStochRSIDPeriod = 3
FastStochRSIDAsk = 80
FastStochRSIDBid = 20

# FullStochRSI Oscillator Period and ask/bid triggers
FullStochRSIDPeriod = 3
FullStochRSIDAsk = 80
FullStochRSIDBid = 20

# FastStoch Oscillator Periods and ask/bid triggers
FastStochKPeriod = 14
FastStochKAsk = 95
FastStochKBid = 5
FastStochDPeriod = 3
FastStochDAsk = 80
FastStochDBid = 20

# FullStoch Oscillator Period and ask/bid triggers
FullStochDPeriod = 3
FullStochDAsk = 80
FullStochDBid = 20

# StdDev Sample
StdDevSample = 10

# BollBand Period
BollBandPeriod = 20

#
### Unused (but planned) configurables
#

# Strategy to trade off (Only Generic supported for now)
TradeStrategy = 'Generic'

# Max slippage percentage from market bid/ask
# Spreads the order points up/down
# NOTE: uses ADX and asset/currency TradeVolume
TradeMaxSlippage = 0.2
