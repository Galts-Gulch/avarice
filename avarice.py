import genconfig
import genutils
import indicators
import loggerdb
import simulator
import strategies
import time
import trader

def RunCommon():
    '''Do the following forever:
    - Configure DB
    - Make candles based on genconfig.Candles.Size.
    - Make a candle price list
    - Run indicators specified in genconfig.IndicatorList'''

    loggerdb.PopulateRow()
    loggerdb.ExtractUsefulLists()

    for indicator in genconfig.IndicatorList:
        getattr(indicators, indicator).indicator()

    strategies.Generic()

    if genconfig.Simulator.Enabled:
        simulator.SimulateFromIndicator()
    if genconfig.Trader.Enabled:
        trader.TradeFromIndicator()

# RunAll automatically if avarice is run directly
if __name__ == '__main__':
    # Sometimes we do not want to drop table for debugging.
    # This *should never* be used in standard runtime
    if not genconfig.Database.Debug:
        loggerdb.ConfigureDatabase()
    if genconfig.TradeRecorder.Enabled:
        genutils.PrepareRecord()
    if loggerdb.ThreadWait > 0:
        print('Waiting', genutils.PrettyMinutes(loggerdb.ThreadWait, 2), 'minutes to resume on schedule')
        time.sleep(loggerdb.ThreadWait)
    genutils.do_every(loggerdb.CandleSizeSeconds, RunCommon)
