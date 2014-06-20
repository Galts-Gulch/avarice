import math
import sqlite3

import genconfig
import loggerdb
import indicators

## General Helper Functions
def PrintIndicatorTrend(short_list, long_list, diff_list = None, DiffDown = None, DiffUp = None, DiffTrend=True):
    if genconfig.IndicatorStrategy == 'CD':
        if short_list[-1] > long_list[-1]:
            trend = 'in a Downtrend'
        elif short_list[-1] < long_list[-1]:
            trend = 'in an Uptrend'
    elif genconfig.IndicatorStrategy == 'Diff':
        if diff_list[-1] < DiffDown:
            if DiffTrend:
                trend = 'in a Downtrend'
            else:
                trend = 'Undersold'
        elif diff_list[-1] > DiffUp:
            if DiffTrend:
                trend = 'in an Uptrend'
            else:
                trend = 'Oversold'
    if not 'trend' in locals():
        if DiffTrend:
            trend = 'in no trend'
        else:
            trend = 'not Oversold or Undersold'

    if DiffTrend:
        DiffString = 'Diff:'
    else:
        DiffString = genconfig.Indicator + ':'

    print(genconfig.Indicator,': We are', trend, '|', DiffString, diff_list[-1])

## Indicators
# price_list = loggerdb.price_list
price_list = []

# RS(I)
RS_list = []
RSI_list = []
RS_gain_list = []
RS_loss_list = []
avg_gain_list = []
avg_loss_list = []
def RSI():
    # We need a minimum of 2 candles to start RS calculations
    if len(price_list) >= 2:
        if price_list[-1] > price_list[-2]:
            gain = price_list[-1] - price_list[-2]
            RS_gain_list.append(gain)
            RS_loss_list.append(0)
        elif price_list[-1] < price_list[-2]:
            loss = price_list[-2] - price_list[-1]
            RS_loss_list.append(loss)
            RS_gain_list.append(0)

        # Do RS calculations if we have all requested periods
        if len(RS_gain_list) >= genconfig.RSIPeriod:
            if len(avg_gain_list) > 1:
                avg_gain_list.append(((avg_gain_list[-1] *\
                        (genconfig.RSIPeriod - 1)) + RS_gain_list[-1])\
                        / genconfig.RSIPeriod)
                avg_loss_list.append(((avg_loss_list[-1] *\
                        (genconfig.RSIPeriod - 1)) + RS_loss_list[-1])\
                        / genconfig.RSIPeriod)
            # Fist run, can't yet apply smoothing
            else:
                avg_gain_list.append(math.fsum(RS_gain_list[(\
                        genconfig.RSIPeriod * -1):]) / genconfig.RSIPeriod)
                avg_loss_list.append(math.fsum(RS_loss_list[(\
                        genconfig.RSIPeriod * -1):]) / genconfig.RSIPeriod)

            # Calculate and append current RS to RS_list
            RS_list.append(avg_gain_list[-1] / avg_loss_list[-1])

            # Calculate and append current RSI to RSI_list
            RSI_list.append(100 - (100 / (1 + RS_list[-1])))

    if genconfig.Indicator == 'RSI':
        if len(RSI_list) < 1:
            print('RSI: Not yet enough data to calculate')
        else:
            # RSI_list is externally accessible, so return None
            print('RSI:', RSI_list[-1])


# Simple Movement Average
def SMAHelper(list1, period):
    if len(list1) >= period:
        SMA = math.fsum(list1[(period * -1):]) / period

        return SMA

SMAShort_list = []
SMALong_list = []
SMADiff_list = []
def SMA():
    # We can start SMA calculations once we have SMALongPeriod
    # price candles, otherwise we append None until met
    if len(price_list) >= genconfig.SMALongPeriod:
        SMAShort_list.append(SMAHelper(price_list, genconfig.SMAShortPeriod))
        SMALong_list.append(SMAHelper(price_list, genconfig.SMALongPeriod))

    if len(SMALong_list) >= 1:
        SMADiff_list.append(100 * (SMAShort_list[-1] - SMALong_list[-1])\
                / ((SMAShort_list[-1] + SMALong_list[-1]) / 2))

    if genconfig.Indicator == 'SMA':
        if len(SMALong_list) < 1:
            print('SMA: Not yet enough data to determine trend')
        else:
            PrintIndicatorTrend(SMAShort_list, SMALong_list, SMADiff_list,\
                    genconfig.SMADiffDown,genconfig.SMADiffUp)


# Exponential Movement Averages
EMAShort_list = []
EMALong_list = []
EMADiff_list = []
DEMAShort_list = []
DEMALong_list = []
DEMADiff_list = []
MACDShort_list = []
MACDLong_list = []
MACDSignal_list = []
MACDHistogram_list = []
MACD_list = []
DMACDShort_list = []
DMACDLong_list = []
DMACDSignal_list = []
DMACDHistogram_list = []
DMACD_list = []
def EMAHelper(list1, list2, period1):
    if len(list1) >= period1:
        Multi = 2 / (period1 + 1)
        if len(list2) > 1:
            EMA = ((list1[-1] - list2[-1]) * Multi) + list2[-1]
        # First run, must use SMA to get started
        elif len(list1) >= period1:
            EMA = ((list1[-1] - SMAHelper(list1, period1)) * Multi)\
                    + SMAHelper(list1, period1)
        return EMA

def EMA():
    # We can start EMAs once we have EMALong candles
    if len(price_list) >= genconfig.EMALong:
        EMAShort_list.append(EMAHelper(price_list, EMAShort_list,\
                genconfig.EMAShort))
        EMALong_list.append(EMAHelper(price_list, EMALong_list,\
                genconfig.EMALong))

    # We can calculate EMADiff when we have both EMALong and EMAShort
    if len(EMALong_list) >= 1:
        EMADiff_list.append(100 * (EMAShort_list[-1] - EMALong_list[-1])\
                / ((EMAShort_list[-1] + EMALong_list[-1]) / 2))

    if genconfig.Indicator == 'EMA':
        if len(EMALong_list) < 1:
            print('EMA: Not yet enough data to determine trend')
        else:
            PrintIndicatorTrend(EMAShort_list, EMALong_list, EMADiff_list,\
                    genconfig.EMADiffDown,genconfig.EMADiffUp)

def DEMAHelper(list1, list2, period1):
    if len(list1) >= 1:
        DEMA = ((2 * list1[-1]) - EMAHelper(list1, list2, period1))

    return DEMA

def DEMA():
    # We can start DEMA EMAs once we have an EMALong candles
    if len(EMALong_list) >= genconfig.EMALong:
        DEMAShort_list.append(DEMAHelper(EMAShort_list, DEMAShort_list,\
                genconfig.EMAShort))
        DEMALong_list.append(DEMAHelper(EMALong_list, DEMALong_list,\
                genconfig.EMALong))

    # We can calculate DEMADiff when we have both DEMALong and DEMAShort
    if len(DEMALong_list) >= 1:
        DEMADiff_list.append(100 * (DEMAShort_list[-1]\
                - DEMALong_list[-1]) / ((DEMAShort_list[-1]\
                + DEMALong_list[-1]) / 2))

        if genconfig.Indicator == 'DEMA':
            if len(DEMALong_list) < 1:
                print('DEMA: Not yet enough data to determine trend')
            else:
                PrintIndicatorTrend(DEMAShort_list, DEMALong_list, DEMADiff_list,\
                        genconfig.DEMADiffDown, genconfig.DEMADiffUp)

def MACD():
    # We can start MACD EMAs once we have MACDLong candles
    if len(price_list) >= genconfig.MACDLong:
        MACDShort_list.append(EMAHelper(price_list, MACDShort_list,\
                genconfig.MACDShort))
        MACDLong_list.append(EMAHelper(price_list, MACDLong_list,\
                genconfig.MACDLong))
        MACD_list.append(MACDShort_list[-1] - MACDLong_list[-1])

        # We need MACDSignal MACDs before generating MACDSignal
        if len(MACDLong_list) >= genconfig.MACDSignal:
            MACDSignal_list.append(EMAHelper(MACD_list, MACDSignal_list,\
                    genconfig.MACDSignal))

            # TODO: use this someday...
            MACDHistogram_list.append(MACD_list[-1] - MACDSignal_list[-1])

        if genconfig.Indicator == 'MACD':
            if len(MACDSignal_list) < 1:
                print('MACD: Not yet enough data to determine trend')
            else:
                PrintIndicatorTrend(MACDSignal_list, MACD_list, MACD_list,\
                        genconfig.MACDDiffDown, genconfig.MACDDiffUp)

def DMACD():
    # We can start DMACD EMAs once we have MACDLong candles
    if len(MACDLong_list) >= genconfig.MACDLong:
        DMACDShort_list.append(DEMAHelper(MACDShort_list, DMACDShort_list,\
                genconfig.MACDShort))
        DMACDLong_list.append(DEMAHelper(MACDLong_list, DMACDLong_list,\
                genconfig.MACDLong))
        DMACD_list.append(DMACDShort_list[-1] - DMACDLong_list[-1])

        # We need MACDSignal DMACDs before generating DMACDSignal
        if len(DMACDLong_list) >= (genconfig.MACDSignal +\
                (abs(genconfig.MACDSignal - genconfig.MACDLong))):
            DMACDSignal_list.append(DEMAHelper(MACDSignal_list,\
                    DMACDSignal_list, genconfig.MACDSignal))
            DMACDHistogram_list.append(DMACD_list[-1] - DMACDSignal_list[-1])

        if genconfig.Indicator == 'DMACD':
            if len(DMACDSignal_list) < 1:
                print('DMACD: Not yet enough data to determine trend')
            else:
                PrintIndicatorTrend(DMACDSignal_list, DMACD_list, DMACD_list,\
                        genconfig.DMACDDiffDown, genconfig.DMACDDiffUp)


# Stochastic Oscillator
def FastStochKHelper(list1, period):
    if len(list1) >= period:
        LowestPeriod = min(float(s) for s in list1[(period * -1):])
        HighestPeriod = max(float(s) for s in list1[(period * -1):])
        FastStochK = ((list1[-1] - LowestPeriod) / (HighestPeriod\
                - LowestPeriod)) * 100

        return FastStochK

FastStochK_list = []
def FastStochK():
    # We can start FastStochK calculations once we have FastStochKPeriod
    # candles, otherwise we append None until met
    if len(price_list) >= genconfig.FastStochKPeriod:
        FastStochK_list.append(FastStochKHelper(price_list,\
                genconfig.FastStochKPeriod))

    if genconfig.Indicator == 'FastStochK':
        if len(FastStochK_list) < 1:
            print('FastStochK: Not yet enough data to calculate')
        else:
            # FastStochK_list is externally accessible, so return None
            print('FastStochK:', FastStochK_list[-1])

FastStochD_list = []
def FastStochD():
    # We can start FastStochD calculations once we have FastStochDPeriod
    # candles, otherwise we append None until met
    if len(FastStochK_list) >= genconfig.FastStochDPeriod:
        FastStochD_list.append(SMAHelper(FastStochK_list,\
                genconfig.FastStochDPeriod))

    if genconfig.Indicator == 'FastStochD':
        if len(FastStochD_list) < 1:
            print('FastStochD: Not yet enough data to calculate')
        else:
            # FastStochD_list is externally accessible, so return None
            print('FastStochD:', FastStochD_list[-1])

FullStochD_list = []
def FullStochD():
    # We can start FullStochD calculations once we have FullStochDPeriod
    # candles, otherwise we append None until met
    if len(FastStochD_list) >= genconfig.FullStochDPeriod:
        FullStochD_list.append(SMAHelper(FastStochD_list,\
                genconfig.FullStochDPeriod))

    if genconfig.Indicator == 'FullStochD':
        if len(FullStochD_list) < 1:
            print('FullStochD: Not yet enough data to calculate')
        else:
            # FullStochD_list is externally accessible, so return None
            print('FullStochD:', FullStochD_list[-1])

# Stochastic RSI
FastStochRSIK_list = []
def FastStochRSIK():
    # We can start FastStochRSIK calculations once we have
    # FastStochRSIKPeriod candles, otherwise we append None until met
    if len(RSI_list) >= genconfig.FastStochRSIKPeriod:
        FastStochRSIK_list.append(FastStochKHelper(RSI_list,\
                genconfig.FastStochRSIKPeriod))

    if genconfig.Indicator == 'FastStochRSIK':
        if len(FastStochRSIK_list) < 1:
            print('FastStochRSIK: Not yet enough data to calculate')
        else:
            # FastStochRSIK_list is externally accessible, so return None
            print('FastStochRSIK:', FastStochRSIK_list[-1])

FastStochRSID_list = []
def FastStochRSID():
    # We can start FastStochRSID calculations once we have
    # FastStochRSIDPeriod candles, otherwise we append None until met
    if len(FastStochRSIK_list) >= genconfig.FastStochRSIDPeriod:
        FastStochRSID_list.append(SMAHelper(FastStochRSIK_list,\
                genconfig.FastStochRSIDPeriod))

    if genconfig.Indicator == 'FastStochRSID':
        if len(FastStochRSID_list) < 1:
            print('FastStochRSID: Not yet enough data to calculate')
        else:
            # FastStochRSID_list is externally accessible, so return None
            print('FastStochRSID:', FastStochRSID_list[-1])

FullStochRSID_list = []
def FullStochRSID():
    # We can start FullStochRSID calculations once we have
    # FullStochRSIDPeriod candles, otherwise we append None until met
    if len(FastStochRSID_list) >= genconfig.FullStochRSIDPeriod:
        FullStochRSID_list.append(SMAHelper(FastStochRSID_list,\
                genconfig.FastStochRSIDPeriod))

    if genconfig.Indicator == 'FullStochRSID':
        if len(FullStochRSID_list) < 1:
            print('FastStochRSID: Not yet enough data to calculate')
        else:
            # FullStochRSID_list is externally accessible, so return None
            print('FullStochRSID:', FullStochRSID_list[-1])


# KDJ
KDJFastK_list = []
KDJFullK_list = []
KDJFullD_list = []
KDJJ_list = []
def KDJ():
    if len(price_list) >= genconfig.KDJFastKPeriod:
        KDJFastK_list.append(FastStochKHelper(price_list,\
                genconfig.KDJFastKPeriod))
    if len(KDJFastK_list) >= genconfig.KDJFullKPeriod:
        KDJFullK_list.append(SMAHelper(KDJFastK_list,\
                genconfig.KDJFullKPeriod))
    if len(KDJFullK_list) >= genconfig.KDJFullDPeriod:
        KDJFullD_list.append(SMAHelper(KDJFullK_list,\
                genconfig.KDJFullDPeriod))
    if len(KDJFullD_list) >= 1:
        KDJJ_list.append((3 * KDJFullD_list[-1]) - (2 * KDJFullK_list[-1]))

    if genconfig.Indicator == 'KDJ':
        if len(KDJJ_list) < 1:
            print('KDJ: Not yet enough data to determine trend or calculate')
        else:
            PrintIndicatorTrend(KDJFullD_list, KDJFullK_list, KDJJ_list,\
                    genconfig.KDJJBid, genconfig.KDJJAsk, False)


# Aroon Oscillator
AroonUp_list = []
AroonDown_list = []
Aroon_list = []
def Aroon():
    # We must have AroonPeriod price_list candles
    if len(price_list) >= genconfig.AroonPeriod:
        AroonUp_list.append(100 * (genconfig.AroonPeriod -\
                (genconfig.AroonPeriod - ([i for i,x in enumerate(price_list)\
                if x == max(price_list[(genconfig.AroonPeriod * -1):])][0] + 1\
                )) / genconfig.AroonPeriod))
        AroonDown_list.append(100 * (genconfig.AroonPeriod -\
                (genconfig.AroonPeriod - ([i for i,x in enumerate(price_list)\
                if x == min(price_list[(genconfig.AroonPeriod * -1):])][0] + 1\
                )) / genconfig.AroonPeriod))
        Aroon_list.append(AroonUp_list[-1] - AroonDown_list[-1])

    if genconfig.Indicator == 'Aroon':
        if len(Aroon_list) < 1:
            print('Aroon: Not yet enough data to determine trend or calculate')
        else:
            PrintIndicatorTrend(AroonDown_list, AroonUp_list, Aroon_list,\
                    genconfig.AroonBid, genconfig.AroonAsk, False)


# Ichimoku Cloud
TenkanSen_list = []
KijunSen_list = []
SenkouSpanART_list = []
SenkouSpanBRT_list = []
SenkouSpanA_list = []
SenkouSpanB_list = []
IchimokuStrong_list = []
IchimokuWeak_list = []
def IchimokuHelper(list1, period1):
    PeriodList = list1[(period1 * -1):]
    Ichi = (max(PeriodList) + min(PeriodList)) / 2
    return Ichi

def Ichimoku():
    # We must have SenkouSpanPeriod price candles before starting
    # calculations, otherwise we append None
    # NOTE: Chikou Span's cool and all, but we don't care. We want to trade in
    # real time, and price list 26 periods behind only confirms if we *were*
    # right or wrong
    if len(price_list) >= genconfig.SenkouSpanPeriod:
        TenkanSen_list.append(IchimokuHelper(price_list,\
                genconfig.TenkanSenPeriod))
        KijunSen_list.append(IchimokuHelper(price_list,\
                genconfig.KijunSenPeriod))
        SenkouSpanART_list.append((TenkanSen_list[-1] + KijunSen_list[-1]) / 2)
        SenkouSpanBRT_list.append(IchimokuHelper(price_list,\
                genconfig.SenkouSpanPeriod))
    # We need SenkouSpan to be ChikouSpanPeriod in the future
    if len(SenkouSpanBRT_list) >= genconfig.ChikouSpanPeriod:
        SenkouSpanA_list.append(SenkouSpanART_list[(\
                genconfig.ChikouSpanPeriod * -1)])
        SenkouSpanB_list.append(SenkouSpanBRT_list[(\
                genconfig.ChikouSpanPeriod * -1)])
    # Don't want to implement a new trade strategy, so just treat
    # Ichimoku lists as threshold strategies for IndicatorList.
    if len(SenkouSpanB_list) >= 1:
        CloudMin = min([min(TenkanSen_list), min(KijunSen_list), min(\
                SenkouSpanA_list), min(SenkouSpanB_list)])
        CloudMax = max([max(TenkanSen_list), max(KijunSen_list), max(\
                SenkouSpanA_list), max(SenkouSpanB_list)])

        CP = price_list[-1]
        KS = KijunSen_list[-1]
        TS = TenkanSen_list[-1]

        # Strong Signals
        if CP > CloudMin and CP < KS and CP > TS:
            # BUY!
            IchimokuStrong_list.append(-1)
            StrongTrend = 'Bullish'
        elif CP < CloudMin and CP > KS and CP < TS:
            # SELL!
            IchimokuStrong_list.append(1)
            StrongTrend = 'Bearish'
        else:
            IchimokuStrong_list.append(0)
            StrongTrend = 'No trend'
        # Weak Signals
        if TS > KS:
            # BUY!
            IchimokuWeak_list.append(-1)
            WeakTrend = 'Bullish'
        elif KS > TS:
            # SELL!
            IchimokuWeak_list.append(1)
            WeakTrend = 'Bearish'
        else:
            IchimokuWeak_list.append(0)
            WeakTrend = 'No trend'

        if genconfig.IchimokuStrategy == 'Strong':
            trend = StrongTrend
        elif genconfig.IchimokuStrategy == 'Weak':
            trend = WeakTrend
        if genconfig.Indicator == 'Ichimoku':
            print('Ichimoku:', trend)
    else:
        if genconfig.Indicator == 'Ichimoku':
            print('Ichimoku: Not yet enough data to determine trend or calculate')


## Volatility/Movement Strength Indicators/Indexes

# Population Standard Deviation
def StdDevHelper(list1, period):
    if len(list1) >= period:
        MeanAvg = math.fsum(list1[(period * -1):]) / period
        Deviation_list = [(i - MeanAvg) for i in list1[(period * -1):]]
        DeviationSq_list = [i ** 2 for i in Deviation_list]
        DeviationSqAvg = math.fsum(DeviationSq_list[(period * -1):])\
                / period
        StandardDeviation = math.sqrt(DeviationSqAvg)

        return StandardDeviation

StdDev_list = []
def StdDev():
    # We can start StdDev calculations once we have StdDevSample
    # candles, otherwise we append None until met
    if len(price_list) >= genconfig.StdDevSample:
        StdDev_list.append(StdDevHelper(price_list,\
                genconfig.StdDevSample))

# Bollinger Bands
BollBandMiddle_list = []
BollBandUpper_list = []
BollBandLower_list = []
def BollBands():
    # We can start BollBand calculations once we have BollBandPeriod
    # candles, otherwise we append None until met
    if len(price_list) >= genconfig.BollBandPeriod:
        BollBandMiddle_list.append(SMAHelper(price_list,\
                genconfig.BollBandPeriod))
        BollBandUpper_list.append(BollBandMiddle_list[-1] + (StdDevHelper(\
                price_list, genconfig.BollBandPeriod) * 2))
        BollBandLower_list.append(BollBandMiddle_list[-1] - (StdDevHelper(\
                price_list, genconfig.BollBandPeriod) * 2))

# Bollinger Bandwidth
BollBandwidth_list = []
def BollBandwidth():
    # We can start BollBandwidth calculations once we have BollBands
    if len(BollBandLower_list) >= 1:
        BollBandwidth_list.append((BollBandUpper_list[-1]\
                - BollBandLower_list[-1]) / BollBandMiddle_list[-1])
