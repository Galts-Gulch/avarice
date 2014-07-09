import genconfig as gc
import genutils as gu
import indicators
import loggerdb
import simulator
import strategies
import time
import trader

pgerr = 'ERROR: Avarice needs pygal and lxml to support graphing. Fix or disable in genconfig'
nograph = False
if gc.Grapher.Enabled:
    try:
        import grapher
    except ImportError:
        print(pgerr)
        nograph = True

def RunCommon():
    '''Do the following forever:
    - Configure DB
    - Make candles based on gc.Candles.Size.
    - Make a candle price list
    - Run indicators specified in gc.IndicatorList'''

    loggerdb.PopulateRow()
    loggerdb.ExtractUsefulLists()

    for indicator in gc.IndicatorList:
        getattr(indicators, indicator).indicator()

    strategies.Generic()

    if gc.Simulator.Enabled:
        simulator.SimulateFromStrategy()
    if gc.Trader.Enabled:
        trader.TradeFromStrategy()
        if gc.Trader.ReOrder:
            if not trader.LastOrder == 'N':
                gu.do_every(gc.Trader.ReOrderDelay, trader.ReOrderTrade(),\
                        gc.Trader.ReOrderMax)
    if gc.Grapher.Enabled and not nograph:
        grapher.Price()
        grapher.Indicator()

# RunAll automatically if avarice is run directly
if __name__ == '__main__':
    # Sometimes we do not want to drop table for debugging.
    # This *should never* be used in standard runtime
    if not gc.Database.Debug:
        loggerdb.ConfigureDatabase()
    if gc.TradeRecorder.Enabled:
        gu.PrepareRecord()
    if loggerdb.ThreadWait > 0:
        print('Waiting', gu.PrettyMinutes(loggerdb.ThreadWait, 2), 'minutes to resume on schedule')
        time.sleep(loggerdb.ThreadWait)
    gu.do_every(loggerdb.CandleSizeSeconds, RunCommon)
