import ast
from configobj import ConfigObj

import avarice
import shelve


class indicators:

  indshelve = ''

  def CreateShelveName():
    configurables = ['Short Period', 'Long Period', 'Period', 'Alpha Constant',
                     'Signal Period', 'Fast K Period', 'Full K Period',
                     'Full D Period', 'Tenkan-Sen Period', 'Senkou Span Period',
                     'Kijun-Sen Period', 'Chikou Span Period', 'Multiplier']
    configurable_values = []
    # Hack for single indicator configuration
    if isinstance(config.gc['Trader']['Trade Indicators'], list):
      tradeindicators = config.gc['Trader']['Trade Indicators']
    else:
      tradeindicators = [config.gc['Trader']['Trade Indicators']]
    for indicator in tradeindicators:
      if isinstance(indicator, list):
        for i in indicator:
          for c in configurables:
            try:
              configurable_values.append(config.gc['Indicators'][i][c])
            except KeyError:
              pass
      else:
        for c in configurables:
          try:
            configurable_values.append(config.gc['Indicators'][indicator][c])
          except KeyError:
            pass
    indicators.indshelve = config.gc['Database']['Path'] + '/' + \
        config.gc['API']['Trade Pair'] + config.gc['Candles']['Size'] + \
        ''.join(x for x in configurable_values) + 'indicators.shelve'

  def writelist(ln, key):
    if not key == None:
      db = shelve.open(indicators.indshelve, writeback=True)
      if ln not in db:
        db[ln] = [key]
      else:
        temp = db[ln]
        temp.append(key)
        if ast.literal_eval(config.gc['Database']['Store All']):
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


class config:
  gc = {}

  def __init__(self):
    config.gc = ConfigObj("config.ini")
