import time

import genconfig as gc
import genutils as gu
import indicators
import loggerdb as ldb
import simulator as sim
import strategies
import trader as trd

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

  ldb.PopulateRow()
  ldb.ExtractUsefulLists()

  for indicator in gc.IndicatorList:
    getattr(indicators, indicator).indicator()

  strategies.Generic()

  if gc.Simulator.Enabled:
    sim.SimulateFromStrategy()
  if gc.Trader.Enabled:
    trd.TradeFromStrategy()
    if gc.Trader.ReIssue:
      if not trd.LastOrder == 'N':
        gu.do_every(gc.Trader.ReIssueDelay, trd.ReIssueTrade,
                    gc.Trader.ReIssueMax)
  if gc.Grapher.Enabled and not nograph:
    grapher.Price()
    grapher.Indicator()

# RunAll automatically if avarice is run directly
if __name__ == '__main__':
  # Sometimes we do not want to drop table for debugging.
  # This *should never* be used in standard runtime
  if not gc.Database.Debug:
    ldb.ConfigureDatabase()
  if gc.TradeRecorder.Enabled:
    gu.PrepareRecord()
  if ldb.ThreadWait > 0:
    print('Waiting', gu.PrettyMinutes(ldb.ThreadWait, 2),
          'minutes to resume on schedule')
    time.sleep(ldb.ThreadWait)
  gu.do_every(ldb.CandleSizeSeconds, RunCommon)
