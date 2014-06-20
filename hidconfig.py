import genconfig
import indicators

# This file is not to be edited like genconfig is

# OKCoin minimum asset trade values
if genconfig.TradePair == 'btc_cny':
    AssetTradeMin = 0.01
elif genconfig.TradePair == 'ltc_cny':
    AssetTradeMin = 0.1

# Due to external calling and varying indicator types,
# we can't use concat or getattr here.
# BidAskList is used to determine if Bid and Ask are lists.
# BidAskReverse is used to determine if Bid and Ask trades
# should be reversed (useful for diff trend trading)
if genconfig.Indicator == 'EMA':
    if genconfig.IndicatorStrategy == 'CD':
        BidAskList = True
        IndicatorList = indicators.EMAShort_list
        IndicatorBid = indicators.EMALong_list
        IndicatorAsk = IndicatorBid
    elif genconfig.IndicatorStrategy == 'Diff':
        TradeReverse = True
        IndicatorList = indicators.EMADiff_list
        IndicatorBid = genconfig.EMADiffUp
        IndicatorAsk = genconfig.EMADiffDown
elif genconfig.Indicator == 'DEMA':
    if genconfig.IndicatorStrategy == 'CD':
        BidAskList = True
        IndicatorList = indicators.DEMAShort_list
        IndicatorBid = indicators.DEMALong_list
        IndicatorAsk = IndicatorBid
    elif genconfig.IndicatorStrategy == 'Diff':
        TradeReverse = True
        IndicatorList = indicators.DEMADiff_list
        IndicatorBid = genconfig.DEMADiffUp
        IndicatorAsk = genconfig.DEMADiffDown
elif genconfig.Indicator == 'MACD':
    if genconfig.IndicatorStrategy == 'CD':
        BidAskList = True
        TradeReverse = True
        IndicatorList = indicators.MACD_list
        IndicatorBid = indicators.MACDSignal_list
        IndicatorAsk = IndicatorBid
    elif genconfig.IndicatorStrategy == 'Diff':
        TradeReverse = True
        IndicatorList = indicators.MACD_list
        IndicatorBid = genconfig.MACDDiffUp
        IndicatorAsk = genconfig.MACDDiffDown
if genconfig.Indicator == 'SMA':
    if genconfig.IndicatorStrategy == 'CD':
        BidAskList = True
        IndicatorList = indicators.SMAShort_list
        IndicatorBid = indicators.SMALong_list
        IndicatorAsk = IndicatorBid
    elif genconfig.IndicatorStrategy == 'Diff':
        TradeReverse = True
        IndicatorList = indicators.SMADiff_list
        IndicatorBid = genconfig.SMADiffUp
        IndicatorAsk = genconfig.SMADiffDown
elif genconfig.Indicator == 'KDJ':
    if genconfig.IndicatorStrategy == 'CD':
        BidAskList = True
        TradeReverse = True
        IndicatorList = indicators.KDJFullK_list
        IndicatorBid = indicators.KDJFullD_list
        IndicatorAsk = IndicatorBid
    elif genconfig.IndicatorStrategy == 'Diff':
        IndicatorList = indicators.KDJJ_list
        IndicatorAsk = genconfig.KDJJAsk
        IndicatorBid = genconfig.KDJJBid
elif genconfig.Indicator == 'Aroon':
    IndicatorList = indicators.Aroon_list
    if genconfig.IndicatorStrategy == 'CD':
        TradeReverse = True
        IndicatorBid = 0
        IndicatorAsk = 0
    elif genconfig.IndicatorStrategy == 'Diff':
        IndicatorBid = genconfig.AroonBid
        IndicatorAsk = genconfig.AroonAsk
elif genconfig.Indicator == 'Ichimoku':
    if genconfig.IchimokuStrategy == 'Strong':
        IndicatorList = indicators.IchimokuStrong_list
    elif genconfig.IchimokuStrategy == 'Weak':
        IndicatorList = indicators.IchimokuWeak_list
    IndicatorBid = 0
    IndicatorAsk = 0
elif genconfig.Indicator == 'RSI':
    IndicatorList = indicators.RSI_list
    IndicatorAsk = genconfig.RSIAsk
    IndicatorBid = genconfig.RSIBid
elif genconfig.Indicator == 'FastStochRSIK':
    IndicatorList = indicators.FastStochRSIK_list
    IndicatorAsk = genconfig.FastStochRSIKAsk
    IndicatorBid = genconfig.FastStochRSIKBid
elif genconfig.Indicator == 'FastStochRSID':
    IndicatorList = indicators.FastStochRSID_list
    IndicatorAsk = genconfig.FastStochRSIDAsk
    IndicatorBid = genconfig.FastStochRSIDBid
elif genconfig.Indicator == 'FullStochRSID':
    IndicatorList = indicators.FullStochRSID_list
    IndicatorAsk = genconfig.FullStochRSIDAsk
    IndicatorBid = genconfig.FullStochRSIDBid
elif genconfig.Indicator == 'FastStochK':
    IndicatorList = indicators.FastStochK_list
    IndicatorAsk = genconfig.FastStochKAsk
    IndicatorBid = genconfig.FastStochKBid
elif genconfig.Indicator == 'FastStochD':
    IndicatorList = indicators.FastStochD_list
    IndicatorAsk = genconfig.FastStochDAsk
    IndicatorBid = genconfig.FastStochDBid
elif genconfig.Indicator == 'FullStochD':
    IndicatorList = indicators.FullStochD_list
    IndicatorAsk = genconfig.FullStochDAsk
    IndicatorBid = genconfig.FullStochDBid

if not 'BidAskList' in locals():
    BidAskList = False
if not 'TradeReverse' in locals():
    TradeReverse = False
