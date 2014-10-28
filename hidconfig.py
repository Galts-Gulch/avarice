import genconfig as gc
import indicators as ind


# This file is not to be edited like gc is

# Due to external calling and varying indicator types,
# we can't use concat or getattr here.
# BidAskList is used to determine if Bid and Ask are lists.
# BidAskReverse is used to determine if Bid and Ask trades
# should be reversed (useful for diff trend trading)


class EMA:
    if gc.EMA.IndicatorStrategy == 'CD':
        BidAskList = True
        IndicatorList = ind.EMA.Long_list
        IndicatorBid = ind.EMA.Short_list
        IndicatorAsk = ind.EMA.Short_list
    elif gc.EMA.IndicatorStrategy == 'Diff':
        TradeReverse = True
        IndicatorList = ind.EMA.Diff_list
        IndicatorBid = gc.EMA.DiffUp
        IndicatorAsk = gc.EMA.DiffDown
    Graphl_list = [ind.EMA.Short_list, ind.EMA.Long_list]
    Graphn_list = ['Short', 'Long']


class DEMA:
    if gc.DEMA.IndicatorStrategy == 'CD':
        BidAskList = True
        IndicatorList = ind.DEMA.Long_list
        IndicatorBid = ind.DEMA.Short_list
        IndicatorAsk = ind.DEMA.Short_list
    elif gc.DEMA.IndicatorStrategy == 'Diff':
        TradeReverse = True
        IndicatorList = ind.DEMA.Diff_list
        IndicatorBid = gc.DEMA.DiffUp
        IndicatorAsk = gc.DEMA.DiffDown
    Graphl_list = [ind.DEMA.Short_list, ind.DEMA.Long_list]
    Graphn_list = ['Short', 'Long']


class FRAMA:
    if gc.FRAMA.IndicatorStrategy == 'CD':
        BidAskList = True
        IndicatorList = ind.FRAMA.Long_list
        IndicatorBid = ind.FRAMA.Short_list
        IndicatorAsk = ind.FRAMA.Short_list
    elif gc.FRAMA.IndicatorStrategy == 'Diff':
        TradeReverse = True
        IndicatorList = ind.FRAMA.Diff_list
        IndicatorBid = gc.FRAMA.DiffUp
        IndicatorAsk = gc.FRAMA.DiffDown
    Graphl_list = [ind.FRAMA.Short_list, ind.FRAMA.Long_list]
    Graphn_list = ['Short', 'Long']


class MACD:
    if gc.MACD.IndicatorStrategy == 'CD':
        BidAskList = True
        TradeReverse = True
        IndicatorList = ind.MACD.ind_list
        IndicatorBid = ind.MACD.Signal_list
        IndicatorAsk = ind.MACD.Signal_list
    elif gc.MACD.IndicatorStrategy == 'Diff':
        TradeReverse = True
        IndicatorList = ind.ind_list
        IndicatorBid = gc.MACD.DiffUp
        IndicatorAsk = gc.MACD.DiffDown
    Graphl_list = [ind.MACD.Signal_list, ind.MACD.ind_list]
    Graphn_list = ['Signal', 'MACD']


class DMACD:
    if gc.DMACD.IndicatorStrategy == 'CD':
        BidAskList = True
        TradeReverse = True
        IndicatorList = ind.DMACD.ind_list
        IndicatorBid = ind.DMACD.Signal_list
        IndicatorAsk = ind.DMACD.Signal_list
    elif gc.DMACD.IndicatorStrategy == 'Diff':
        TradeReverse = True
        IndicatorList = ind.ind_list
        IndicatorBid = gc.DMACD.DiffUp
        IndicatorAsk = gc.DMACD.DiffDown
    Graphl_list = [ind.DMACD.Signal_list, ind.DMACD.ind_list]
    Graphn_list = ['Signal', 'DMACD']


class SMA:
    if gc.SMA.IndicatorStrategy == 'CD':
        BidAskList = True
        IndicatorList = ind.SMA.Long_list
        IndicatorBid = ind.SMA.Short_list
        IndicatorAsk = ind.SMA.Short_list
    elif gc.SMA.IndicatorStrategy == 'Diff':
        TradeReverse = True
        IndicatorList = ind.SMA.Diff_list
        IndicatorBid = gc.SMA.DiffUp
        IndicatorAsk = gc.SMA.DiffDown
    Graphl_list = [ind.SMA.Short_list, ind.SMA.Long_list]
    Graphn_list = ['Short', 'Long']


class KDJ:
    if gc.KDJ.IndicatorStrategy == 'CD':
        BidAskList = True
        TradeReverse = True
        IndicatorList = ind.KDJ.FullK_list
        IndicatorBid = ind.KDJ.FullD_list
        IndicatorAsk = ind.KDJ.FullD_list
    elif gc.KDJ.IndicatorStrategy == 'Diff':
        IndicatorList = ind.KDJ.J_list
        IndicatorAsk = gc.KDJ.Ask
        IndicatorBid = gc.KDJ.Bid
    Graphl_list = [ind.KDJ.FullK_list, ind.KDJ.FullD_list, ind.KDJ.J_list]
    Graphn_list = ['K', 'D', 'J']


class Aroon:
    IndicatorList = ind.Aroon.ind_list
    if gc.Aroon.IndicatorStrategy == 'CD':
        TradeReverse = True
        IndicatorBid = 0
        IndicatorAsk = 0
    elif gc.Aroon.IndicatorStrategy == 'Diff':
        IndicatorBid = gc.Aroon.Bid
        IndicatorAsk = gc.Aroon.Ask
    Graphl_list = [ind.Aroon.ind_list]
    Graphn_list = ['Aroon']


class Ichimoku:
    if gc.Ichimoku.IndicatorStrategy == 'Strong':
        IndicatorList = ind.Ichimoku.Strong_list
    elif gc.Ichimoku.IndicatorStrategy == 'Weak':
        IndicatorList = ind.Ichimoku.Weak_list
    IndicatorBid = 0
    IndicatorAsk = 0
    Graphl_list = [ind.Ichimoku.KijunSen_list, ind.Ichimoku.TenkanSen_list,
                   ind.Ichimoku.SenkouSpanA_list, ind.Ichimoku.SenkouSpanB_list]
    Graphn_list = ['KijunSen', 'TenkanSen', 'SenkouSpanA', 'SenkouSpanB']


class RSI:
    IndicatorList = ind.RSI.ind_list
    IndicatorAsk = gc.RSI.Ask
    IndicatorBid = gc.RSI.Bid
    Graphl_list = [ind.RSI.ind_list]
    Graphn_list = ['RSI']


class FastStochRSIK:
    IndicatorList = ind.FastStochRSIK.ind_list
    IndicatorAsk = gc.FastStochRSIK.Ask
    IndicatorBid = gc.FastStochRSIK.Bid
    Graphl_list = [ind.FastStochRSIK.ind_list]
    Graphn_list = ['FastStochRSIK']


class FastStochRSID:
    IndicatorList = ind.FastStochRSID.ind_list
    IndicatorAsk = gc.FastStochRSID.Ask
    IndicatorBid = gc.FastStochRSID.Bid
    Graphl_list = [ind.FastStochRSID.ind_list]
    Graphn_list = ['FastStochRSID']


class FullStochRSID:
    IndicatorList = ind.FullStochRSID.ind_list
    IndicatorAsk = gc.FullStochRSID.Ask
    IndicatorBid = gc.FullStochRSID.Bid
    Graphl_list = [ind.FullStochRSID.ind_list]
    Graphn_list = ['FullStochRSID']


class FastStochK:
    IndicatorList = ind.FastStochK.ind_list
    IndicatorAsk = gc.FastStochK.Ask
    IndicatorBid = gc.FastStochK.Bid
    Graphl_list = [ind.FastStochK.ind_list]
    Graphn_list = ['FastStochK']


class FastStochD:
    IndicatorList = ind.FastStochD.ind_list
    IndicatorAsk = gc.FastStochD.Ask
    IndicatorBid = gc.FastStochD.Bid
    Graphl_list = [ind.FastStochD.ind_list]
    Graphn_list = ['FastStochD']


class FullStochD:
    IndicatorList = ind.FullStochD.ind_list
    IndicatorAsk = gc.FullStochD.Ask
    IndicatorBid = gc.FullStochD.Bid
    Graphl_list = [ind.FullStochD.ind_list]
    Graphn_list = ['FullStochD']


class SROC:
    IndicatorList = ind.SROC.ind_list
    IndicatorBid = 0
    IndicatorAsk = 0
    Graphl_list = [ind.SROC.ind_list]
    Graphn_list = ['SROC']
