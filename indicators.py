import math
import sqlite3

import genconfig
import loggerdb

## Sqlite Accessibility Functions
def MakeCandlePriceList():
    '''Accesses MarketHistory sqlite database, and
    makes an ordered list of all prices.
    Returns: list'''

    conn = sqlite3.connect(loggerdb.sqlite_file)
    db = conn.cursor()

    db.execute("SELECT * from '{tn}'".format(tn=loggerdb.table_name))

    # extract column names
    column_names = [d[0] for d in db.description]

    price_list = []

    for row in db:
        # build dict
        info = dict(zip(column_names, row))
        # Build ordered price list
        price_list.append(info[loggerdb.column1])

    conn.close()
    return price_list

## Indicators

# RS(I)
RS_list = []
RSI_list = []
RS_gain_list = []
RS_loss_list = []
avg_gain_list = []
avg_loss_list = []
def RSI():
    price_list = MakeCandlePriceList()
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
            # RSI_list is externally accessible, so return NULL
            print('RSI:', RSI_list[-1])


# SMA
def SMAHelper(list1, period):
    if len(list1) >= period:
        SMA = math.fsum(list1[(period * -1):]) / period

        return SMA

SMA_list = []
def SMA():
    price_list = MakeCandlePriceList()
    # We can start SMA calculations once we have SMAPeriod
    # candles, otherwise we append None until met
    if len(price_list) >= genconfig.SMAPeriod:
        SMA_list.append(SMAHelper(price_list, genconfig.SMAPeriod))


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
    price_list = MakeCandlePriceList()
    # We can start FastStochK calculations once we have FastStochKPeriod
    # candles, otherwise we append None until met
    if len(price_list) >= genconfig.FastStochKPeriod:
        FastStochK_list.append(FastStochKHelper(price_list,\
                genconfig.FastStochKPeriod))

    if genconfig.Indicator == 'FastStochK':
        if len(FastStochK_list) < 1:
            print('FastStochK: Not yet enough data to calculate')
        else:
            # FastStochK_list is externally accessible, so return NULL
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
            # FastStochD_list is externally accessible, so return NULL
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
            # FullStochD_list is externally accessible, so return NULL
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
            # FastStochRSIK_list is externally accessible, so return NULL
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
            # FastStochRSID_list is externally accessible, so return NULL
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
            # FullStochRSID_list is externally accessible, so return NULL
            print('FullStochRSID:', FullStochRSID_list[-1])
