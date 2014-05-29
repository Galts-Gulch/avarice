import threading

import genconfig
import indicators
import loggerdb
import okcoin
import trader

def do_every (interval, worker_func, iterations = 0):
    ''' Basic support for configurable/iterable threading'''
    if iterations != 1:
        threading.Timer (
            interval,
            do_every, [interval, worker_func,\
                    0 if iterations == 0 else iterations-1]
        ).start ();
    worker_func ();

def RunAll(debug=False):
    '''Do the following forever:
    - Configure DB
    - Make candles based on genconfig.CandleSize.
    - Make a candle price list
    - Run indicator specified on genconfig.Indicator'''
    if not debug:
        loggerdb.ConfigureDatabase()

    CandleSizeSeconds = genconfig.CandleSize * 60

    do_every(CandleSizeSeconds, loggerdb.PopulateRow)
    do_every(CandleSizeSeconds, indicators.MakeCandlePriceList)
    # NOTE: using getattr for this unfortunately doesn't work due
    # to external calls. And we need to have database configured
    # prior to running.
    if genconfig.Indicator == 'RSI':
        do_every(CandleSizeSeconds, indicators.RSI)
    elif genconfig.Indicator == 'StochRSI':
        do_every(CandleSizeSeconds, indicators.StochRSI)
    elif genconfig.Indicator == 'SMA':
        do_every(CandleSizeSeconds, indicators.SMA)

    if genconfig.LiveTrading:
        do_every(CandleSizeSeconds, trader.TradeFromIndicator)

# RunAll automatically if avarice is run directly
if __name__ == '__main__':
    # Sometimes we do not want to drop table for debugging.
    # This *should never* be used in standard runtime
    if genconfig.Debug:
        RunAll(debug=True)
    else:
        RunAll()
