# General configurables
import genconfig


class API:
  # Exchange to use
  # SUPPORTED: okcoin.com and okcoin.cn
  Exchange = 'okcoin'
  # Asset_currency to trade in.
  # NOTE: cny pairs for okcoin.cn and usd pairs for okcoin.com
  TradePair = 'btc_usd'
  Asset = TradePair[:3]
  Currency = TradePair[-3:]
  apikey = 'stub'
  secretkey = 'stub'

  # How long in seconds should we wait between secure API commands?
  # NOTE: OKCoin uses 2s limit
  APIWait = 2

  # What is the minimum we can trade of our asset?
  # NOTE: 0.01 for btc and 0.1 for ltc on OKCoin
  AssetTradeMin = 0.01


class Candles:
  # Print every candle?
  Verbose = True
  # In minutes; used for all indicator assessments/trade freq
  Size = 15


class Trader:
  # Live trade with REAL MONEY?
  # NOTE: Always sells/buys at market bid/ask
  Enabled = False

  #
  # All of the following is also used by Simulator:
  #

  # Indicators which should be traded off.
  # NOTE: view IndicatorList below to see available options, and check
  # README.md for info.
  # You may set multiple indicators, i.e: ['MACD','KDJ']
  TradeIndicators = ['EMA']

  # Percentage of total (so 50 is 50%).
  # NOTE: this is percentage of asset and currency.
  # This is re-evaluated for each trade.
  # It is recommended to set this to a lower value if not running CD
  TradeVolume = 99
  # Should we only do a single consecutive sell or buy?
  # NOTE: Still uses above percentage to determine sell/buy.
  # If the previous trade was a buy, and buy is still recommended, we
  # will wait for sell before trading again.
  # This is useful for MA style strategies ((D)EMA, MACD), whereas Osc
  # style should set to False.
  SingleTrade = True
  # Should the signal persist for two candles before acting on it?
  TradePersist = False
  # How many candles with indicator info before
  # allowing trades?
  # NOTE: must be greater than 1, and an integer
  TradeDelay = 3
  # Should we ReIssue trades with tradeSlippage and ReIssueDelay until
  # a trade goes through?
  ReIssue = True
  # What % order price delta should we continue trying to get an order
  # through for?
  ReIssueSlippage = 0.04
  # How many seconds should we wait for an order to clear and re-order it?
  # NOTE: uses TradeSlippage
  ReIssueDelay = 15
  # Maximum ReIssue attempts to make (0 for infinite (not recommended))
  ReIssueMax = 5


class Simulator:
  # Simulate Trades without live trading?
  # NOTE: Always sells/buys at market bid/ask
  Enabled = True
  # Print profit/holdings info every candle if true. False prints on trades.
  Verbose = False
  Asset = 1
  Currency = 3000


class TradeRecorder:
  # Record trades and simulations in a text file?
  Enabled = True
  Path = './recorded'
  SimName = 'simulator.txt'
  TradeName = 'trader.txt'
  # False deletes the text files on each new run.
  Persist = False


class Database:
  # Debug flag only used to avoid dropping db table.
  # Makes development easier/faster.
  # NOTE: only ever run if developing, not for accuracy.
  Debug = False
  Path = "./sqlite"


class Grapher:
  # NOTE: requires pygal and lxml
  Enabled = True
  Path = './charts'
  # Choose between the following: Default, Neon, DarkSolarized,
  # LightSolarized, Light, Clean, Red Blue, DarkColorized, LightColorized,
  # Turquoise, LightGreen, DarkGreen, DarkGreenBlue, Blue.
  Theme = 'DarkSolarized'
  # Default is to graph indicators set as TradeIndicators. Make the following
  # into a list to better suit your needs.
  Indicators = genconfig.Trader.TradeIndicators
  # Show time, or show candle numbers as x axis labels?
  ShowTime = False
  # How many candles should we show on the graph (x-axis)?
  MaxLookback = 30

#
# Indicators - See README.md for more info
# All diff applicability are dependent on CandleSize
#

# List of all indicators which should run
# NOTE: Order matters
IndicatorList = ['RSI', 'FastStochRSIK', 'FastStochRSID', 'FullStochRSID',
                 'SMA', 'EMA', 'EMAwbic', 'DEMA', 'FRAMA', 'MACD', 'DMACD',
                 'FastStochK', 'FastStochD', 'FullStochD', 'KDJ', 'StdDev',
                 'Aroon', 'Ichimoku', 'BollBands', 'BollBandwidth', 'SROC']

# Indicators which should be verbose each candle. By default, we only print
# the trades if all conditions are met.
# NOTE: if you want the TradeIndicators to be verbose, set
# VerboseIndicators = genconfig.Trader.TradeIndicators below
VerboseIndicators = []


class SMA:
  # We support both CD and Diff IndicatorStrategies
  IndicatorStrategy = 'CD'
  ShortPeriod = 15
  LongPeriod = 50
  DiffDown = -0.025
  DiffUp = 0.025


class EMA:
  # We support both CD and Diff IndicatorStrategies
  IndicatorStrategy = 'CD'
  ShortPeriod = 10
  LongPeriod = 21
  DiffDown = -0.025
  DiffUp = 0.025


class DEMA:
  # Uses both EMA.LongPeriod and EMA.ShortPeriod from above
  # We support both CD and Diff IndicatorStrategies
  IndicatorStrategy = 'CD'
  DiffDown = -0.025
  DiffUp = 0.025


class EMAwbic:
  Period = 60
  # Buy when price is <Bid % of EMA
  Bid = -75
  # Sell when price is >Ask % of EMA
  Ask = 95


class FRAMA:
  IndicatorStrategy = 'CD'
  ShortPeriod = 10
  LongPeriod = 21
  AlphaConstant = -4.6
  DiffDown = -0.025
  DiffUp = 0.025


class MACD:
  # NOTE: Mike Bruns' agressive 3/11/16 are also recommended
  # We support both CD and Diff IndicatorStrategies
  IndicatorStrategy = 'CD'
  ShortPeriod = 12
  LongPeriod = 26
  SignalPeriod = 9
  DiffDown = -0.1
  DiffUp = 0.1


class DMACD:
  # Uses MACDLong, MACDShort, and MACDSignal
  # We support both CD and Diff IndicatorStrategies
  IndicatorStrategy = 'CD'
  DiffDown = -0.1
  DiffUp = 0.1


class RSI:
  # Period can never be less than 3, but 14
  # or higher is generally recommended.
  # NOTE: Period is also used for RS calculations.
  Period = 14
  Ask = 70
  Bid = 30


class FastStochRSIK:
  # NOTE: %D uses %K periods, %D periods are SMA periods of %K
  Period = 14
  Ask = 80
  Bid = 20


class FastStochRSID:
  # %D uses %K periods, %D periods are SMA periods of %K
  Period = 3
  Ask = 80
  Bid = 20


class FullStochRSID:
  # Full %D uses Fast %D periods, Full %D periods are SMA periods of Fast %D
  Period = 3
  Ask = 80
  Bid = 20


class FastStochK:
  Period = 14
  Ask = 95
  Bid = 5


class FastStochD:
  # %D uses %K periods, %D periods are SMA periods of %K
  Period = 3
  Ask = 80
  Bid = 20


class FullStochD:
  # Full %D uses Fast %D periods, Full %D periods are SMA periods of Fast %D
  Period = 3
  Ask = 80
  Bid = 20


class KDJ:
  # We support both CD and Diff off J IndicatorStrategies
  IndicatorStrategy = 'CD'
  FastKPeriod = 9
  FullKPeriod = 3
  FullDPeriod = 3
  Ask = 100
  Bid = 0


class Aroon:
  # We support both CD (when Aroon is > or < 0) and Diff off bid/ask
  # This is because zero line is where AroonUp and AroonDown converge/diverge
  IndicatorStrategy = 'CD'
  Period = 25
  Bid = -90
  Ask = 90


class Ichimoku:
  # NOTE: We support 'Strong' and 'Weak' IndicatorStrategies. Check
  # README.md for info.
  IndicatorStrategy = 'Strong'
  TenkanSenPeriod = 9
  # Only used on Span B since SpanA just uses Tenkan-sen and Kijnun-sen
  SenkouSpanPeriod = 52
  KijunSenPeriod = 26
  # Only determines how far to place Senkou Spans in the future
  ChikouSpanPeriod = 26


class StdDev:
  Period = 10


class BollBands:
  Period = 20


class SROC:
  Period = 12
