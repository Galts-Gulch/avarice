import avarice
import shelve
import genconfig as gc


class indicators:

  indshelve = ''

  def CreateShelveName():
    configurables = ['ShortPeriod', 'LongPeriod', 'Period', 'AlphaConstant',
                     'SignalPeriod', 'FastKPeriod', 'FullKPeriod', 'FullDPeriod',
                     'TenkanSenPeriod', 'SenkouSpanPeriod', 'KijunSenPeriod',
                     'ChikouSpanPeriod', 'Multiplier']
    configurable_values = []
    for indicator in gc.Trader.TradeIndicators:
      if isinstance(indicator, list):
        for i in indicator:
          for c in configurables:
            try:
              configurable_values.append(getattr(getattr(gc, i), c))
            except AttributeError:
              pass
      else:
        for c in configurables:
          try:
            configurable_values.append(getattr(getattr(gc, indicator), c))
          except AttributeError:
            pass
    indicators.indshelve = gc.Database.Path + '/' + gc.API.TradePair + \
        str(gc.Candles.Size) + ''.join(str(x)
                                       for x in configurable_values) + 'indicators.shelve'

  def writelist(ln, key):
    if not key == None:
      db = shelve.open(indicators.indshelve, writeback=True)
      if ln not in db:
        db[ln] = [key]
      else:
        temp = db[ln]
        temp.append(key)
        if gc.Database.StoreAll:
          db[ln] = temp
        else:
          db[ln] = temp[-avarice.MaxCandleDepends:]
      db.close()

  def getlist(ln):
    db = shelve.open(indicators.indshelve, writeback=True)
    if ln not in db:
      temp = []
    else:
      try:
        temp = db[ln]
      except EOFError:
        try:
          temp = db[ln]
        except EOFError:
          temp = []
    db.close
    return temp
