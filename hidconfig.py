import genconfig
import indicators

# This file is not to be edited like genconfig is

# Due to external calling and varying indicator types,
# we can't use concat or getattr here.
# BidAskList is used to determine if Bid and Ask are lists.
# BidAskReverse is used to determine if Bid and Ask trades
# should be reversed (useful for diff trend trading)
class EMA:
    trade_list = []
    if genconfig.EMA.IndicatorStrategy == 'CD':
        BidAskList = True
        IndicatorList = indicators.EMA.Short_list
        IndicatorBid = indicators.EMA.Long_list
        IndicatorAsk = indicators.EMA.Long_list
    elif genconfig.EMA.IndicatorStrategy == 'Diff':
        TradeReverse = True
        IndicatorList = indicators.EMA.Diff_list
        IndicatorBid = genconfig.EMA.DiffUp
        IndicatorAsk = genconfig.EMA.DiffDown
class DEMA:
    trade_list = []
    if genconfig.DEMA.IndicatorStrategy == 'CD':
        BidAskList = True
        IndicatorList = indicators.DEMA.Short_list
        IndicatorBid = indicators.DEMA.Long_list
        IndicatorAsk = indicators.DEMA.Long_list
    elif genconfig.DEMA.IndicatorStrategy == 'Diff':
        TradeReverse = True
        IndicatorList = indicators.DEMA.Diff_list
        IndicatorBid = genconfig.DEMA.DiffUp
        IndicatorAsk = genconfig.DEMA.DiffDown
class MACD:
    trade_list = []
    if genconfig.MACD.IndicatorStrategy == 'CD':
        BidAskList = True
        TradeReverse = True
        IndicatorList = indicators.MACD.ind_list
        IndicatorBid = indicators.MACD.Signal_list
        IndicatorAsk = indicators.MACD.Signal_list
    elif genconfig.MACD.IndicatorStrategy == 'Diff':
        TradeReverse = True
        IndicatorList = indicators.ind_list
        IndicatorBid = genconfig.MACD.DiffUp
        IndicatorAsk = genconfig.MACD.DiffDown
class DMACD:
    trade_list = []
    if genconfig.DMACD.IndicatorStrategy == 'CD':
        BidAskList = True
        TradeReverse = True
        IndicatorList = indicators.DMACD.ind_list
        IndicatorBid = indicators.DMACD.Signal_list
        IndicatorAsk = indicators.DMACD.Signal_list
    elif genconfig.DMACD.IndicatorStrategy == 'Diff':
        TradeReverse = True
        IndicatorList = indicators.ind_list
        IndicatorBid = genconfig.DMACD.DiffUp
        IndicatorAsk = genconfig.DMACD.DiffDown
class SMA:
    trade_list = []
    if genconfig.SMA.IndicatorStrategy == 'CD':
        BidAskList = True
        IndicatorList = indicators.SMA.Short_list
        IndicatorBid = indicators.SMA.Long_list
        IndicatorAsk = indicators.SMA.Long_list
    elif genconfig.SMA.IndicatorStrategy == 'Diff':
        TradeReverse = True
        IndicatorList = indicators.SMA.Diff_list
        IndicatorBid = genconfig.SMA.DiffUp
        IndicatorAsk = genconfig.SMA.DiffDown
class KDJ:
    trade_list = []
    if genconfig.KDJ.IndicatorStrategy == 'CD':
        BidAskList = True
        TradeReverse = True
        IndicatorList = indicators.KDJ.FullK_list
        IndicatorBid = indicators.KDJ.FullD_list
        IndicatorAsk = indicators.KDJ.FullD_list
    elif genconfig.KDJ.IndicatorStrategy == 'Diff':
        IndicatorList = indicators.KDJ.J_list
        IndicatorAsk = genconfig.KDJ.Ask
        IndicatorBid = genconfig.KDJ.Bid
class Aroon:
    trade_list = []
    IndicatorList = indicators.Aroon.ind_list
    if genconfig.Aroon.IndicatorStrategy == 'CD':
        TradeReverse = True
        IndicatorBid = 0
        IndicatorAsk = 0
    elif genconfig.Aroon.IndicatorStrategy == 'Diff':
        IndicatorBid = genconfig.Aroon.Bid
        IndicatorAsk = genconfig.Aroon.Ask
class Ichimoku:
    trade_list = []
    if genconfig.Ichimoku.IndicatorStrategy == 'Strong':
        IndicatorList = indicators.Ichimoku.Strong_list
    elif genconfig.Ichimoku.IndicatorStrategy == 'Weak':
        IndicatorList = indicators.Ichimoku.Weak_list
    IndicatorBid = 0
    IndicatorAsk = 0
class RSI:
    trade_list = []
    IndicatorList = indicators.RSI.ind_list
    IndicatorAsk = genconfig.RSI.Ask
    IndicatorBid = genconfig.RSI.Bid
class FastStochRSIK:
    trade_list = []
    IndicatorList = indicators.FastStochRSIK.ind_list
    IndicatorAsk = genconfig.FastStochRSIK.Ask
    IndicatorBid = genconfig.FastStochRSIK.Bid
class FastStochRSID:
    trade_list = []
    IndicatorList = indicators.FastStochRSID.ind_list
    IndicatorAsk = genconfig.FastStochRSID.Ask
    IndicatorBid = genconfig.FastStochRSID.Bid
class FullStochRSID:
    trade_list = []
    IndicatorList = indicators.FullStochRSID.ind_list
    IndicatorAsk = genconfig.FullStochRSID.Ask
    IndicatorBid = genconfig.FullStochRSID.Bid
class FastStochK:
    trade_list = []
    IndicatorList = indicators.FastStochK.ind_list
    IndicatorAsk = genconfig.FastStochK.Ask
    IndicatorBid = genconfig.FastStochK.Bid
class FastStochD:
    trade_list = []
    IndicatorList = indicators.FastStochD.ind_list
    IndicatorAsk = genconfig.FastStochD.Ask
    IndicatorBid = genconfig.FastStochD.Bid
class FullStochD:
    trade_list = []
    IndicatorList = indicators.FullStochD.ind_list
    IndicatorAsk = genconfig.FullStochD.Ask
    IndicatorBid = genconfig.FullStochD.Bid

if not 'BidAskList' in locals():
    BidAskList = False
if not 'TradeReverse' in locals():
    TradeReverse = False
