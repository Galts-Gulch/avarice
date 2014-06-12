import math
import sqlite3

import genconfig
import loggerdb
import indicators

## Sqlite Accessibility Functions
price_list = []
def MakeCandlePriceList():
    '''Accesses MarketHistory sqlite database, and
    makes an ordered list of all prices.
    Returns: None'''

    conn = sqlite3.connect(loggerdb.sqlite_file)
    db = conn.cursor()

    db.execute("SELECT * from '{tn}'".format(tn=loggerdb.table_name))

    # extract column names
    column_names = [d[0] for d in db.description]

    # clear external list since we read all rows of this column
    indicators.price_list = []

    for row in db:
        # build dict
        info = dict(zip(column_names, row))
        # Build ordered price list
        price_list.append(info[loggerdb.column1])

    conn.close()
    # list is externally accessible, so return None

## Indicators

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

SMA_list = []
def SMA():
    # We can start SMA calculations once we have SMAPeriod
    # candles, otherwise we append None until met
    if len(price_list) >= genconfig.SMAPeriod:
        SMA_list.append(SMAHelper(price_list, genconfig.SMAPeriod))


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

def PrintMATrend(short_list, long_list, diff_list = None, DiffDown = None, DiffUp = None):
    if genconfig.MAStrategy == 'CD':
        if short_list[-1] > long_list[-1]:
            trend = 'a downtrend'
        elif short_list[-1] < long_list[-1]:
            trend = 'an uptrend'
    elif genconfig.MAStrategy == 'Diff':
        if diff_list[-1] < DiffDown:
            trend = 'a downtrend'
        elif diff_list[-1] > DiffUp:
            trend = 'an uptrend'
    if not 'trend' in locals():
        trend = 'no trend'

    print(genconfig.Indicator,': We are in', trend, '| Diff:', diff_list[-1])


def EMA():
    if len(price_list) >= genconfig.SMAPeriod:
        # We can start EMAs once we have EMALong candles
        if len(price_list) >= genconfig.EMALong:
            EMAShort_list.append(EMAHelper(price_list, EMAShort_list,\
                    genconfig.EMAShort))

            EMALong_list.append(EMAHelper(price_list, EMALong_list,\
                    genconfig.EMALong))

        # We can calculate EMADiff when we have both EMALong and EMAShort
        if len(EMALong_list) >= 1:
            EMADiff_list.append(100 * (EMAShort_list[-1]\
                    - EMALong_list[-1]) / ((EMAShort_list[-1]\
                    + EMALong_list[-1]) / 2))

        if genconfig.Indicator == 'EMA':
            if len(EMALong_list) < 1:
                print('EMA: Not yet enough data to determine trend')
            else:
                PrintMATrend(EMAShort_list, EMALong_list, EMADiff_list,\
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
                PrintMATrend(DEMAShort_list, DEMALong_list, DEMADiff_list,\
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
                PrintMATrend(MACDSignal_list, MACD_list, MACD_list,\
                        genconfig.MACDDiffDown, genconfig.MACDDiffUp)

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

