import asyncio
import ast
from time import sleep

import avarice
import exchangelayer as el
import genutils as gu
import hidconfig
import indicators
import loggerdb as ldb
import notifier as no
import simulator as sim
import strategies
import storage
import trader as trd
from storage import config

conf = config()
pgerr = 'WARNING: Avarice needs pygal and lxml to support graphing. Fix or disable in config.ini'
nograph = False
if ast.literal_eval(config.gc['Grapher']['Enabled']):
  try:
    import grapher
  except ImportError:
    print(pgerr)
    nograph = True

RCruns = 0
MaxCandleDepends = 0
indlist = []


def PrintEstimate():
  CandleDepends_list = []
  for indicator in ast.literal_eval(config.gc['Trader']['Trade Indicators']):
    if isinstance(indicator, list):
      for i in indicator:
        try:
          CandleDepends_list.append(getattr(indicators, i).CandleDepends)
        except AttributeError:
          try:
            CandleDepends_list.append(
                getattr(indicators, hidconfig.IndicatorAlias_dict[i]).CandleDepends)
          except AttributeError:
            try:
              CandleDepends_list.append(
                  getattr(indicators, hidconfig.IndicatorAlias2_dict[i]).CandleDepends)
            except AttributeError:
              print(
                  'ERROR: Indicator does not exist, please see documentation.')
    else:
      try:
        CandleDepends_list.append(getattr(indicators, indicator).CandleDepends)
      except AttributeError:
        try:
          CandleDepends_list.append(
              getattr(indicators, hidconfig.IndicatorAlias_dict[indicator]).CandleDepends)
        except AttributeError:
          try:
            CandleDepends_list.append(
                getattr(indicators, hidconfig.IndicatorAlias2_dict[indicator]).CandleDepends)
          except AttributeError:
            print('ERROR: Indicator does not exist, please see documentation.')
  esttime = max(CandleDepends_list) * float(config.gc['Candles']['Size'])
  # For minimal database storage
  avarice.MaxCandleDepends = max(CandleDepends_list)
  if not ldb.ThreadWait:
    print('Approximately', esttime,
          'minutes to get enough info to trade on all TradeIndicators')


def RunIndicator(indicator):
  try:
    ind = getattr(indicators, indicator)
  except AttributeError:
    try:
      ind = getattr(indicators, hidconfig.IndicatorAlias_dict[indicator])
    except AttributeError:
      ind = getattr(indicators, hidconfig.IndicatorAlias2_dict[indicator])
  if hasattr(ind, 'IndicatorDepends'):
    for i in getattr(ind, 'IndicatorDepends'):
      if i not in avarice.indlist:
        getattr(indicators, i).indicator()
        avarice.indlist.append(i)
  if indicator not in avarice.indlist:
    avarice.indlist.append(indicator)
    ind.indicator()


def RunCommon():
  '''Do the following forever:
  - Configure DB
  - Make candles based on config.ini Candles Size.
  - Make a candle price list
  - Run indicators and depends in config.ini Trader Trade Indicators'''
  avarice.RCruns += 1
  if el.GetMarketPrice('bid') is not None:
    ldb.PopulateRow()
    ldb.ExtractUsefulLists()
    avarice.indlist = []
    for indicator in ast.literal_eval(config.gc['Trader']['Trade Indicators']):
      if isinstance(indicator, list):
        for i in indicator:
          RunIndicator(i)
      else:
        RunIndicator(indicator)
    getattr(strategies, config.gc['Trader']['Advanced Strategy'])()
    sim.SimulateFromStrategy()
    if ast.literal_eval(config.gc['Trader']['Enabled']):
      trd.TradeFromStrategy()
    if ast.literal_eval(config.gc['Grapher']['Enabled']) and not nograph:
      grapher.Price()
      grapher.Indicator()


def RCWrapper():
  if avarice.RCruns < 2:
    if avarice.RCruns == 1:
      PrintEstimate()
      storage.indicators.CreateShelveName()
      no.Wrapper.Run()
      if not ast.literal_eval(config.gc['API']['Verbose']):
        print('Connecting to OKCoin WebSocket(s)...')
    RunCommon()
  else:
    if ldb.ThreadWait > 0:
      print('Waiting', gu.PrettyMinutes(ldb.ThreadWait - 6, 2),
            'minutes to resume on schedule')
      if ldb.ThreadWait - 6 > 0:
        sleep(ldb.ThreadWait - 6)
    elif not ast.literal_eval(config.gc['Database']['Debug']):
      gu.SilentRemove(storage.indicators.indshelve)
      for i in ['trader', 'simulator']:
        gu.SilentRemove(config.gc['Database']['Path'] + '/' + i + '.shelve')
    gu.do_every(ldb.CandleSizeSeconds, RunCommon)


def RunAll():
  # Sometimes we do not want to drop table for debugging.
  # This *should never* be used in standard runtime
  if not ast.literal_eval(config.gc['Database']['Debug']):
    ldb.ConfigureDatabase()
  RCWrapper()
  gu.do_every(6, RCWrapper, 2)
  loop = asyncio.get_event_loop()
  if ast.literal_eval(config.gc['Trader']['Enabled']):
    asyncio.async(trd.TradeWrapper())
  if el.AdditionalAsync:
    for i in el.AdditionalAsync:
      asyncio.async(i)
  loop.run_forever()

# RunAll automatically if avarice is run directly
if __name__ == '__main__':
  RunAll()
