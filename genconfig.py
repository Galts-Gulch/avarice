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
# NOTE: this is percentage of asset and currency.
# This is re-evaluated for each trade
TradeVolume = 40

# Should we only do a single consecutive sell or buy?
# NOTE: Still uses above percentage to determine sell/buy.
# If the previous trade was a buy, and buy is still recommended, we
# will wait for sell before trading again.
# This is useful for MA style strategies ((D)EMA, MACD), whereas Osc
# style should set to False.
SingleTrade = True

# How many candles with indicator info before
# allowing trades?
# NOTE: must be greater than 1, and an integer
TradeDelay = 3

# In minutes; used for all indicator assessments/trade freq
CandleSize = 10

# API secret + partner key
partner = 111111111
secret_key = 'stub'

# How long in seconds should we wait between secure API commands?
APIWait = 1.5

# Record trades and simulations in a text file?
RecordPath = './recorded'
RecordTrades = True
RecordSimName = 'simulator.txt'
RecordTradeName = 'trader.txt'
# False deletes the text files on each new run.
PersistTrades = False
# Debug flag only used to avoid dropping db table.
# Makes development easier/faster.
# NOTE: only ever run if developing, not for accuracy.
Debug = False


#
### Indicators - See README.md for more info
## All diff applicability are dependent on CandleSize
#

# List of all indicators which should run
# NOTE: Order matters
IndicatorList = ['RSI','FastStochRSIK','FastStochRSID','FullStochRSID',\
        'SMA','EMA','DEMA','MACD','DMACD','FastStochK','FastStochD',\
        'FullStochD','KDJ','StdDev','Aroon','Ichimoku','BollBands',\
        'BollBandwidth']

# The indicator that should be traded off
Indicator = 'MACD'

# Strategy used on various indicators (EMA, DEMA, MACD, KDJ).
# Support two strategies; CD (convergence/divergence) and Diff
# (uses *DiffDown and *DiffUp thresholds).
IndicatorStrategy = 'CD'

# SMA Periods
# NOTE: We support both CD and Diff IndicatorStrategies
SMAShortPeriod = 15
SMALongPeriod = 50
SMADiffDown = -0.025
SMADiffUp = 0.025

# EMA short and long periods, ema strategy, and diff thresholds
# NOTE: EMA trade strategies have been split into two trading
# strategies; CD and Diff.
EMAShort = 10
EMALong = 21
EMADiffDown = -0.025
EMADiffUp = 0.025

# DEMA Diffs. Uses both EMALong and EMAShort from above.
# NOTE: uses IndicatorStrategy from above
DEMADiffDown = -0.025
DEMADiffUp = 0.025

# MACD Periods and Diffs
# NOTE: industry standard are 12/26/9, however we use Mike Bruns'
# more agressive values
MACDShort = 3
MACDLong = 11
MACDSignal = 16
MACDDiffDown = -0.1
MACDDiffUp = 0.1

# DMACD Diffs. Uses MACDLong, MACDShort, and MACDSignal
# NOTE: uses IndicatorStrategy from above
DMACDDiffDown = -0.1
DMACDDiffUp = 0.1

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

# KDJ Periods, and ask/bid triggers
# NOTE: We support both CD (when K/D converge/diverge), and Diff off J
KDJFastKPeriod = 9
KDJFullKPeriod = 3
KDJFullDPeriod = 3
KDJJAsk = 100
KDJJBid = 0

# Aroon Oscillator Period
# NOTE: We support both CD (when Aroon is > or < 0), and Diff off bid/ask
# This is because zero line is where AroonUp and AroonDown converge/diverge
AroonPeriod = 25
AroonBid = -90
AroonAsk = 90

# Ichimoku Cloud Periods and Strategy
# NOTE: We support Strong and Weak Ichi strategies. Check README.md for info. 
IchimokuStrategy = 'Strong'
TenkanSenPeriod = 9
# Only used on Span B since SpanA just uses Tenkan-sen and Kijnun-sen
SenkouSpanPeriod = 52
KijunSenPeriod = 26
# Only determines how far to place Senkou Spans in the future
ChikouSpanPeriod = 26

# StdDev Sample
StdDevSample = 10

# BollBand Period
BollBandPeriod = 20

#
### Unused (but planned) configurables
#

# Max slippage percentage from market bid/ask
# Spreads the order points up/down
# NOTE: uses ADX and asset/currency TradeVolume
TradeMaxSlippage = 0.2
