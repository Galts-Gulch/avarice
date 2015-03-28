import ast
import os
import pygal as pg

import hidconfig as hc
import loggerdb as ldb
from storage import indicators as storage
from storage import config


theme = getattr(pg.style, config.gc['Grapher']['Theme'] + 'Style')


def getxaxis():
  if ast.literal_eval(config.gc['Grapher']['Show Time']):
    label = ldb.time_list
  else:
    label = ldb.candle_list
  return label


def Price():
  os.makedirs(config.gc['Grapher']['Path'], exist_ok=True)
  pc = pg.Line(style=theme)
  pc.title = 'Prices across candles in ' + \
      config.gc['API']['Trade Pair'][-3:].upper()
  if len(ldb.price_list) > config.gc['Grapher']['Max Lookback']:
    lb = config.gc['Grapher']['Max Lookback']
  else:
    lb = len(ldb.price_list)
  pc.x_labels = getxaxis()[-lb:]
  pc.add(config.gc['API']['Trade Pair'][:3].upper(), ldb.price_list[-lb:])
  pc.render_to_file(config.gc['Grapher']['Path'] + '/price_chart.svg')


# TODO: cleanup duplication in another function
def Indicator():
  if isinstance(config.gc['Grapher']['Indicators'], list):
    for i in config.gc['Grapher']['Indicators']:
      if isinstance(i, list):
        for l in i:
          hidind = getattr(hc, l)
          ic = pg.Line(style=theme)
          ic.title = l + ' across candles'
          # Unlike prices : candles, we don't always have the same element
          # count for each of our lists.
          minsize = min(map(len, hidind.Graphl_list))
          if minsize > config.gc['Grapher']['Max Lookback']:
            minsize = config.gc['Grapher']['Max Lookback']
          ic.x_labels = getxaxis()[-minsize:]
          if minsize > 0:
            for li in hidind.Graphl_list:
              pos = hidind.Graphl_list.index(li)
              ic.add(hidind.Graphn_list[pos], storage.getlist(li)[-minsize:])
            ic.render_to_file(
                config.gc['Grapher']['Path'] + '/' + l + '_chart.svg')
      else:
        hidind = getattr(hc, i)
        ic = pg.Line(style=theme)
        ic.title = i + ' across candles'
        # Unlike prices : candles, we don't always have the same element
        # count for each of our lists.
        minsize = min(map(len, hidind.Graphl_list))
        if minsize > config.gc['Grapher']['Max Lookback']:
          minsize = config.gc['Grapher']['Max Lookback']
        ic.x_labels = getxaxis()[-minsize:]
        if minsize > 0:
          for li in hidind.Graphl_list:
            pos = hidind.Graphl_list.index(li)
            ic.add(hidind.Graphn_list[pos], storage.getlist(li)[-minsize:])
          ic.render_to_file(
              config.gc['Grapher']['Path'] + '/' + i + '_chart.svg')
  elif not config.gc['Grapher']['Indicators'] == 'stub':
    hidind = getattr(hc, config.gc['Grapher']['Indicators'])
    ic = pg.Line(style=theme)
    ic.title = config.gc['Grapher']['Indicators'] + ' across candles'
    # Unlike prices : candles, we don't always have the same element
    # count for each of our lists.
    minsize = min(map(len, hidind.Graphl_list))
    if minsize > config.gc['Grapher']['Max Lookback']:
      minsize = config.gc['Grapher']['Max Lookback']
    ic.x_labels = getxaxis()[-minsize:]
    if minsize > 0:
      for li in hidind.Graphl_list:
        pos = hidind.Graphl_list.index(li)
        ic.add(hidind.Graphn_list[pos], storage.getlist(li)[-minsize:])
      ic.render_to_file(config.gc['Grapher'][
                        'Path'] + '/' + config.gc['Grapher']['Indicators'] + '_chart.svg')
