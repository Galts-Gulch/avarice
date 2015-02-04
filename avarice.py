import asyncio
import time

import exchangelayer as el
import genconfig as gc
import genutils as gu
import indicators
import loggerdb as ldb
import simulator as sim
import strategies
import trader as trd

pgerr = 'WARNING: Avarice needs pygal and lxml to support graphing. Fix or disable in genconfig'
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
  if el.GetMarketPrice('bid') is not None:
    ldb.PopulateRow()
    ldb.ExtractUsefulLists()
    for indicator in gc.IndicatorList:
      getattr(indicators, indicator).indicator()
    getattr(strategies, gc.Trader.AdvancedStrategy)()
    if gc.Simulator.Enabled:
      sim.SimulateFromStrategy()
    if gc.Trader.Enabled:
      trd.TradeFromStrategy()
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
    # TODO: fix resumption when threading before asyncio.
    # time.sleep(ldb.ThreadWait)
  gu.do_every(ldb.CandleSizeSeconds, RunCommon)
  loop = asyncio.get_event_loop()
  if gc.Trader.Enabled:
    asyncio.async(trd.TradeWrapper())
  if el.AdditionalAsync:
    for i in el.AdditionalAsync:
      asyncio.async(i)
  loop.run_forever()
