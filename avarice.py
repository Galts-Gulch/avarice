import asyncio
import time

import avarice
import exchangelayer as el
import genconfig as gc
import genutils as gu
import indicators
import loggerdb as ldb
import notifier as no
import simulator as sim
import strategies
import storage
import trader as trd

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
    for indicator in gc.IndicatorList:
      getattr(indicators, indicator).indicator()
    getattr(strategies, gc.Trader.AdvancedStrategy)()
    sim.SimulateFromStrategy()
    if gc.Trader.Enabled:
      trd.TradeFromStrategy()
    if gc.Grapher.Enabled and not nograph:
      grapher.Price()
      grapher.Indicator()


def RCWrapper():
  if avarice.RCruns < 2:
    if avarice.RCruns == 1:
      no.Wrapper.Run()
      if not gc.API.Verbose:
        print('Connecting to OKCoin WebSocket(s)...')
    RunCommon()
  else:
    if ldb.ThreadWait > 0:
      print('Waiting', gu.PrettyMinutes(ldb.ThreadWait - 6, 2),
            'minutes to resume on schedule')
      if ldb.ThreadWait - 6 > 0:
        time.sleep(ldb.ThreadWait - 6)
    elif not gc.Database.Debug:
      gu.SilentRemove(storage.indicators.indshelve)
    gu.do_every(ldb.CandleSizeSeconds, RunCommon)

# RunAll automatically if avarice is run directly
if __name__ == '__main__':
  # Sometimes we do not want to drop table for debugging.
  # This *should never* be used in standard runtime
  if not gc.Database.Debug:
    ldb.ConfigureDatabase()
  RCWrapper()
  gu.do_every(6, RCWrapper, 2)
  loop = asyncio.get_event_loop()
  if gc.Trader.Enabled:
    asyncio.async(trd.TradeWrapper())
  if el.AdditionalAsync:
    for i in el.AdditionalAsync:
      asyncio.async(i)
  loop.run_forever()
