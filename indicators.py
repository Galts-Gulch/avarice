import math
import sqlite3

import genconfig
import loggerdb

## Indicators
price_list = loggerdb.price_list

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
            # RSI_list is externally accessible, so return NULL
            print('RSI:', RSI_list[-1])


# SMA
SMA_list = []
RSI_SMA_list = []
StochRSI_SMA_list = []
Stochastic_SMA_list = []
def SMA(list1=price_list, list2=SMA_list, period=genconfig.SMAPeriod):
    # We can start start SMA calculations once we have SMAPeriod candles 
    if len(list1) >= period:
        list2.append(math.fsum(list1[(period * -1):])\
                / period)


# StochRSIK
StochRSIK_list = []
def StochRSIK():
    # Call RSI
    RSI()
    if len(RSI_list) >= genconfig.StochRSIKPeriod:
        LowestPeriodRSI = min(float(s) for s in RSI_list[(\
                genconfig.StochRSIKPeriod * -1):])
        HighestPeriodRSI = max(float(s) for s in RSI_list[(\
                genconfig.StochRSIKPeriod * -1):])
        # Calculate and append current StochRSIK to StochRSIK_list
        StochRSIK_list.append(((RSI_list[-1] - LowestPeriodRSI) / (\
                HighestPeriodRSI - LowestPeriodRSI)) * 100)
    if genconfig.Indicator == 'StochRSIK':
        if len(StochRSIK_list) < 1:
            print('StochRSIK: Not yet enough data to calculate')
        else:
            # StochRSIK_list is externally accessible, so return NULL
            print('StochRSIK:', StochRSIK_list[-1])


# FastStochK
FastStochK_list = []
def FastStochK():
    # We can start FastStochK calculations once we have FastStochKPeriod
    # candles
    if len(price_list) >= genconfig.FastStochKPeriod:
        LowestPeriodPrice = min(float(s) for s in price_list[(\
                genconfig.FastStochKPeriod * -1):])
        HighestPeriodPrice = max(float(s) for s in price_list[(\
                genconfig.FastStochKPeriod * -1):])
        # Calculate and append current FastStochK to FastStochK_list
        FastStochK_list.append(((price_list[-1] - LowestPeriodPrice) / (\
                HighestPeriodPrice - LowestPeriodPrice)) * 100)
    if genconfig.Indicator == 'FastStochK':
        if len(FastStochK_list) < 1:
            print('FastStochK: Not yet enough data to calculate')
        else:
            # FastStochK_list is externally accessible, so return NULL
            print('FastStochK:', FastStochK_list[-1])
