import os
import pygal as pg

import genconfig as gc
import genconfig as gc
import loggerdb as ldb
import hidconfig as hc

theme = getattr(pg.style, gc.Grapher.Theme + 'Style')

def getxaxis():
    if gc.Grapher.ShowTime:
        label = ldb.time_list
    else:
        label = ldb.candle_list
    return label

def Price():
    os.makedirs(gc.Grapher.Path, exist_ok=True)
    pc = pg.Line(style=theme)
    pc.title = 'Prices across candles in ' + gc.API.Currency.upper()
    if len(ldb.price_list) > gc.Grapher.MaxLookback:
        lb = gc.Grapher.MaxLookback
    else:
        lb = len(ldb.price_list)
    pc.x_labels = getxaxis()[-lb:]
    pc.add(gc.API.Asset.upper(), ldb.price_list[-lb:])
    pc.render_to_file(gc.Grapher.Path + '/price_chart.svg')

def Indicator():
    for i in gc.Grapher.Indicators:
        hidind = getattr(hc, i)
        ic = pg.Line(style=theme)
        ic.title = i + ' across candles'
        # Unlike prices : candles, we don't always have the same element
        # count for each of our lists.
        minsize = min(map(len, hidind.Graphl_list))
        if minsize > gc.Grapher.MaxLookback:
            minsize = gc.Grapher.MaxLookback
        ic.x_labels = getxaxis()[-minsize:]
        if minsize > 0:
            for l in hidind.Graphl_list:
                pos = hidind.Graphl_list.index(l)
                ic.add(hidind.Graphn_list[pos], l[-minsize:])
            ic.render_to_file(gc.Grapher.Path + i + '_chart.svg')
