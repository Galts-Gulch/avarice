#
# Everything below is fully documented in
# http://galts-gulch.github.io/avarice/configuring
#
import genconfig


class API:
  Verbose = False
  Exchange = 'okcoin'
  TradePair = 'btc_cny'
  Asset = TradePair[:3]
  Currency = TradePair[-3:]
  apikey = 'stub'
  secretkey = 'stub'
  AssetTradeMin = 0.01


class Candles:
  Verbose = True
  Size = 15


class Trader:
  Enabled = False
  Verbose = True
  # All of the following is also used by Simulator
  TradeIndicators = ['EMA']
  AdvancedStrategy = 'Default'
  TradeVolume = 99
  SingleTrade = True
  TradePersist = False
  TradeDelay = 3
  ReIssueSlippage = 0.12
  ReIssueDelay = 5


class Simulator:
  Verbose = True
  Asset = 1
  Currency = 3000


class Notifier:

  class TextFile:
    TradeRecord = True
    SimulatorRecord = True
    RolloverTime = 24
    Path = './recorded'
    TradeName = 'trader.log'
    SimName = 'simulator.log'


class Database:
  Debug = False
  Path = "./database"


class Grapher:
  Enabled = True
  Path = './charts'
  Theme = 'DarkSolarized'
  Indicators = genconfig.Trader.TradeIndicators
  ShowTime = False
  MaxLookback = 30

#
# Indicators
# All diff applicability are dependent on CandleSize
#

# NEVER modify
IndicatorList = ['RSI', 'FastStochRSIK', 'FastStochRSID', 'FullStochRSID',
                 'SMA', 'EMA', 'EMAwbic', 'DEMA', 'FRAMA', 'MACD', 'DMACD',
                 'FastStochK', 'FastStochD', 'FullStochD', 'KDJ', 'StdDev',
                 'Aroon', 'Ichimoku', 'BollBands', 'BollBandwidth', 'SROC',
                 'ATR', 'DMI', 'ChandExit']

# How many indicator threads can we create?
MaxThreads = 4

# Indicators which should be verbose each candle. By default, we only print
# the trades if all conditions are met.
# Example: ['MACD', 'EMA', 'FRAMA']
VerboseIndicators = []


class SMA:
  # We support both CD and Diff IndicatorStrategies
  IndicatorStrategy = 'CD'
  ShortPeriod = 15
  LongPeriod = 50
  DiffDown = -0.025
  DiffUp = 0.025

  class Trader:
    TradeVolume = 99
    SingleTrade = True
    TradePersist = False
    TradeDelay = 3


class EMA:
  # We support both CD and Diff IndicatorStrategies
  IndicatorStrategy = 'CD'
  ShortPeriod = 10
  LongPeriod = 21
  DiffDown = -0.025
  DiffUp = 0.025

  class Trader:
    TradeVolume = 99
    SingleTrade = True
    TradePersist = False
    TradeDelay = 3


class DEMA:
  # Uses both EMA.LongPeriod and EMA.ShortPeriod from above
  # We support both CD and Diff IndicatorStrategies
  IndicatorStrategy = 'CD'
  DiffDown = -0.025
  DiffUp = 0.025

  class Trader:
    TradeVolume = 99
    SingleTrade = True
    TradePersist = False
    TradeDelay = 3


class EMAwbic:
  Period = 60
  # Buy when price is <Bid % of EMA
  Bid = -75
  # Sell when price is >Ask % of EMA
  Ask = 95

  class Trader:
    TradeVolume = 99
    SingleTrade = True
    TradePersist = False
    TradeDelay = 3


class FRAMA:
  IndicatorStrategy = 'CD'
  ShortPeriod = 10
  LongPeriod = 21
  AlphaConstant = -4.6
  DiffDown = -0.025
  DiffUp = 0.025

  class Trader:
    TradeVolume = 99
    SingleTrade = True
    TradePersist = False
    TradeDelay = 3


class MACD:
  # NOTE: Mike Bruns' agressive 3/11/16 are also recommended
  # We support both CD and Diff IndicatorStrategies
  IndicatorStrategy = 'CD'
  ShortPeriod = 12
  LongPeriod = 26
  SignalPeriod = 9
  DiffDown = -0.1
  DiffUp = 0.1

  class Trader:
    TradeVolume = 99
    SingleTrade = True
    TradePersist = False
    TradeDelay = 3


class DMACD:
  # Uses MACDLong, MACDShort, and MACDSignal
  # We support both CD and Diff IndicatorStrategies
  IndicatorStrategy = 'CD'
  DiffDown = -0.1
  DiffUp = 0.1

  class Trader:
    TradeVolume = 99
    SingleTrade = True
    TradePersist = False
    TradeDelay = 3


class RSI:
  # Period can never be less than 3, but 14
  # or higher is generally recommended.
  # NOTE: Period is also used for RS calculations.
  Period = 14
  Ask = 70
  Bid = 30

  class Trader:
    TradeVolume = 20
    SingleTrade = False
    TradePersist = False
    TradeDelay = 3


class FastStochRSIK:
  # NOTE: %D uses %K periods, %D periods are SMA periods of %K
  Period = 14
  Ask = 80
  Bid = 20

  class Trader:
    TradeVolume = 20
    SingleTrade = False
    TradePersist = False
    TradeDelay = 3


class FastStochRSID:
  # %D uses %K periods, %D periods are SMA periods of %K
  Period = 3
  Ask = 80
  Bid = 20

  class Trader:
    TradeVolume = 20
    SingleTrade = False
    TradePersist = False
    TradeDelay = 3


class FullStochRSID:
  # Full %D uses Fast %D periods, Full %D periods are SMA periods of Fast %D
  # We support both CD and Diff (standard) IndicatorStrategies
  IndicatorStrategy = 'Diff'
  Period = 3
  Ask = 80
  Bid = 20

  class Trader:
    # SingleTrade should be True and TradeVolume should be higher if
    # IndicatorStrategy is CD
    TradeVolume = 20
    SingleTrade = False
    TradePersist = False
    TradeDelay = 3


class FastStochK:
  Period = 14
  Ask = 95
  Bid = 5

  class Trader:
    TradeVolume = 20
    SingleTrade = False
    TradePersist = False
    TradeDelay = 3


class FastStochD:
  # %D uses %K periods, %D periods are SMA periods of %K
  Period = 3
  Ask = 80
  Bid = 20

  class Trader:
    TradeVolume = 20
    SingleTrade = False
    TradePersist = False
    TradeDelay = 3


class FullStochD:
  # Full %D uses Fast %D periods, Full %D periods are SMA periods of Fast %D
  Period = 3
  Ask = 80
  Bid = 20

  class Trader:
    TradeVolume = 20
    SingleTrade = False
    TradePersist = False
    TradeDelay = 3


class KDJ:
  # We support both CD and Diff off J IndicatorStrategies
  IndicatorStrategy = 'CD'
  FastKPeriod = 9
  FullKPeriod = 3
  FullDPeriod = 3
  Ask = 100
  Bid = 0

  class Trader:
    TradeVolume = 99
    SingleTrade = True
    TradePersist = False
    TradeDelay = 3


class Aroon:
  # We support both CD (when Aroon is > or < 0) and Diff off bid/ask
  # This is because zero line is where AroonUp and AroonDown converge/diverge
  IndicatorStrategy = 'CD'
  Period = 25
  Bid = -90
  Ask = 90

  class Trader:
    TradeVolume = 99
    SingleTrade = True
    TradePersist = False
    TradeDelay = 3


class Ichimoku:
  # Check galts-gulch.io/avarice/indicators for info on supported strategies.
  IndicatorStrategy = 'Optimized'
  TenkanSenPeriod = 9
  # Only used on Span B since SpanA just uses Tenkan-sen and Kijnun-sen
  SenkouSpanPeriod = 52
  KijunSenPeriod = 26
  # Only determines how far to place Senkou Spans in the future
  ChikouSpanPeriod = 26

  class Trader:
    TradeVolume = 99
    SingleTrade = True
    TradePersist = False
    TradeDelay = 3


class StdDev:
  VolatilityThresholdOver = True
  Period = 10
  Threshold = 0.4


class BollBands:
  Period = 20


class BollBandwidth:
  # NOTE: uses BollBand Period. Threshold should be adjusted based on
  # CandleSize and intended use.
  VolatilityThresholdOver = True
  Threshold = 1


class ATR:
  VolatilityThresholdOver = True
  Period = 14
  # Threshold should be adjusted based on CandleSize and intended use.
  Threshold = 10


class ChandExit:
  # We require running long enough for price to pass Short or Long exits before
  # determining which trend line to use.
  # TODO: Add Stop Loss indicator support.
  Period = 22
  Multiplier = 3

  # Despite the below, Chandelier Exits should only be used when combined
  # with another indicator.
  class Trader:
    TradeVolume = 99
    SingleTrade = True
    TradePersist = False
    TradeDelay = 3


class DMI:
  # Uses ATR period.
  # 'Full' uses ADX threshold, and +DI -DI crossovers to determine signal.
  # 'Volatility' only uses threshold with ADX as a volatility indicator (must be combined).
  IndicatorStrategy = 'Volatility'
  VolatilityThresholdOver = True
  Threshold = 20

  # Only used on "Full" IndicatorStrategy and when an independent indicator.
  class Trader:
    TradeVolume = 99
    SingleTrade = True
    TradePersist = False
    TradeDelay = 3


class SROC:
  Period = 12

  class Trader:
    TradeVolume = 99
    SingleTrade = True
    TradePersist = False
    TradeDelay = 3
