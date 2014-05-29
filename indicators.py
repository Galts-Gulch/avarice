import math
import sqlite3

import genconfig
import loggerdb

## Indicator Helper Functions
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
def RSI(ExternalIndicator=False):
    price_list = MakeCandlePriceList()
    # We need a minimum of 2 candles to start RSI calculations
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

    if not ExternalIndicator:
        if len(RSI_list) < 1:
            print('RSI: Not yet enough data to calculate')
        else:
            # RSI_list is externally accessible, so return NULL
            print('RSI:', RSI_list[-1])

# StochRSI
StochRSI_list = []
def StochRSI():
    # Call RSI
    RSI(ExternalIndicator=True)
    if len(RSI_list) >= genconfig.StochRSIPeriod:
        LowestPeriodRSI = min(float(s) for s in RSI_list[(\
                genconfig.StochRSIPeriod * -1):])
        HighestPeriodRSI = max(float(s) for s in RSI_list[(\
                genconfig.StochRSIPeriod * -1):])
        # Calculate and append current StochRSI to StochRSI_list
        StochRSI_list.append(((RSI_list[-1] - LowestPeriodRSI) / (\
                HighestPeriodRSI - LowestPeriodRSI)) * 100)
    if len(StochRSI_list) < 1:
        print('StochRSI: Not yet enough data to calculate')
    else:
        # StochRSI_list is externally accessible, so return NULL
        print('StochRSI:', StochRSI_list[-1])
