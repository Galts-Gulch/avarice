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


@asyncio.coroutine
def RunCommon():
  '''Do the following forever:
  - Configure DB
  - Make candles based on gc.Candles.Size.
  - Make a candle price list
  - Run indicators specified in gc.IndicatorList'''
  while True:
    if el.GetMarketPrice('bid') is None:
      # Sometimes we do not want to drop table for debugging.
      # This *should never* be used in standard runtime
      if not gc.Database.Debug:
        ldb.ConfigureDatabase()
      if gc.TradeRecorder.Enabled:
        gu.PrepareRecord()
      if ldb.ThreadWait > 0:
        print('Waiting', gu.PrettyMinutes(ldb.ThreadWait, 2),
              'minutes to resume on schedule')
        time.sleep(ldb.ThreadWait - 5)
    else:
      ldb.PopulateRow()
      ldb.ExtractUsefulLists()
      for indicator in gc.IndicatorList:
        getattr(indicators, indicator).indicator()
      strategies.Generic()
      if gc.Simulator.Enabled:
        sim.SimulateFromStrategy()
      if gc.Trader.Enabled:
        trd.TradeFromStrategy()
      if gc.Grapher.Enabled and not nograph:
        grapher.Price()
        grapher.Indicator()
    if el.GetMarketPrice('bid') is None:
      yield from asyncio.sleep(5)
    else:
      yield from asyncio.sleep(ldb.CandleSizeSeconds)

# RunAll automatically if avarice is run directly
if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  asyncio.async(RunCommon())
  if el.AdditionalAsync:
    for i in el.AdditionalAsync:
      asyncio.async(i)
  loop.run_forever()
