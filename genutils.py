import os
import threading

import genconfig


def do_every(interval, worker_func, iterations=0):
    ''' Basic support for configurable/iterable threading'''
    if iterations != 1:
        threading.Timer(
            interval,
            do_every, [interval, worker_func,
                       0 if iterations == 0 else iterations - 1]
        ).start()
    worker_func()


def RoundIfGreaterThan(num, place):
    if len(str(num).split('.')[1]) > place:
        rounded = round(num, place)
    else:
        rounded = num
    return rounded


def PrettyMinutes(seconds, place):
    minutes = seconds / 60
    pm = RoundIfGreaterThan(minutes, place)
    return pm


def PrepareRecord():
    if not genconfig.TradeRecorder.Persist:
        try:
            os.rmdir(genconfig.TradeRecorder.Path)
        except Exception:
            pass
    os.makedirs(genconfig.TradeRecorder.Path, exist_ok=True)


def RecordTrades(action, price, amount):
    if genconfig.Simulator.Enabled:
        f = open(genconfig.TradeRecorder.Path + '/' +
                 genconfig.TradeRecorder.SimName, 'a')
    else:
        f = open(genconfig.TradeRecorder.Path + '/' +
                 genconfig.TradeRecorder.TradeName, 'a')
    line = action + ' ' + str(amount) + genconfig.API.Asset + ' at ' + str(price)\
        + genconfig.API.Currency
    f.write(line + '\n')
    f.close


def PrintIndicatorTrend(caller, short_list, long_list, diff_list=None, DiffDown=None, DiffUp=None,
                        DiffTrend=True):
    if getattr(genconfig, caller).IndicatorStrategy == 'CD':
        if short_list[-1] < long_list[-1]:
            trend = 'in a Downtrend'
        elif short_list[-1] > long_list[-1]:
            trend = 'in an Uptrend'
    elif getattr(genconfig, caller).IndicatorStrategy == 'Diff':
        if diff_list[-1] < DiffDown:
            if DiffTrend:
                trend = 'in a Downtrend'
            else:
                trend = 'Undersold'
        elif diff_list[-1] > DiffUp:
            if DiffTrend:
                trend = 'in an Uptrend'
            else:
                trend = 'Oversold'
    if not 'trend' in locals():
        if DiffTrend:
            trend = 'in no trend'
        else:
            trend = 'not Oversold or Undersold'

    if DiffTrend:
        DiffString = 'Diff:'
    else:
        DiffString = caller + ':'

    print(caller, ': We are', trend, '|', DiffString, diff_list[-1])
