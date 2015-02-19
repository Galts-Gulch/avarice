import asyncio
import time

import avarice
import exchangelayer as el
import genconfig as gc
import genutils as gu
import indicators
import loggerdb as ldb
import simulator as sim
import strategies
import trader as trd
import concurrent.futures

pgerr = 'WARNING: Avarice needs pygal and lxml to support graphing. Fix or disable in genconfig'
nograph = False
if gc.Grapher.Enabled:
  try:
    import grapher
  except ImportError:
    print(pgerr)
    nograph = True

RCruns = 0


def RunCommon():
  '''Do the following forever:
  - Configure DB
  - Make candles based on gc.Candles.Size.
  - Make a candle price list
  - Run indicators specified in gc.IndicatorList'''
  avarice.RCruns += 1
  if el.GetMarketPrice('bid') is not None:
    ldb.PopulateRow()
    ldb.ExtractUsefulLists()
    with concurrent.futures.ThreadPoolExecutor(max_workers=gc.MaxThreads) as executor:
      {executor.submit(getattr(indicators, ind).indicator): ind for ind in gc.IndicatorList}
    getattr(strategies, gc.Trader.AdvancedStrategy)()
    if gc.Simulator.Enabled:
      sim.SimulateFromStrategy()
    if gc.Trader.Enabled:
      trd.TradeFromStrategy()
    if gc.Grapher.Enabled and not nograph:
      grapher.Price()
      grapher.Indicator()


def RCWrapper():
  if avarice.RCruns < 2:
    # gu.do_every(6, RunCommon, 2)
    RunCommon()
  else:
    if ldb.ThreadWait > 0:
      print('Waiting', gu.PrettyMinutes(ldb.ThreadWait - 6, 2),
            'minutes to resume on schedule')
      if ldb.ThreadWait - 6 > 0:
        time.sleep(ldb.ThreadWait - 6)
    gu.do_every(ldb.CandleSizeSeconds, RunCommon)

# RunAll automatically if avarice is run directly
if __name__ == '__main__':
  # Sometimes we do not want to drop table for debugging.
  # This *should never* be used in standard runtime
  if not gc.Database.Debug:
    ldb.ConfigureDatabase()
  if gc.TradeRecorder.Enabled:
    gu.PrepareRecord()
  RCWrapper()
  gu.do_every(6, RCWrapper, 2)
  loop = asyncio.get_event_loop()
  if gc.Trader.Enabled:
    asyncio.async(trd.TradeWrapper())
  if el.AdditionalAsync:
    for i in el.AdditionalAsync:
      asyncio.async(i)
  loop.run_forever()
