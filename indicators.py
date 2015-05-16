import math

import genutils as gu
import loggerdb as ldb
from storage import indicators as storage
from storage import config


# Misc Indicator Helpers
class Helpers:

  def SMA(list1, period):
    if len(list1) >= period:
      SMA = math.fsum(list1[-period:]) / period
      return SMA

  def EMA(list1, list2, period1):
    if len(list1) >= period1:
      Multi = 2 / (period1 + 1)
      if list2:
        EMA = ((list1[-1] - list2[-1]) * Multi) + list2[-1]
      # First run, must use SMA to get started
      elif len(list1) >= period1:
        EMA = ((list1[-1] - Helpers.SMA(list1, period1)) * Multi)\
            + Helpers.SMA(list1, period1)
      return EMA

  def WMA(list1, list2, period):
    '''Wilders Moving Average'''
    if not list2:
      WMA = Helpers.SMA(list1, period)
    else:
      WMA = ((list2[-1] * (period - 1)) + list1[-1]) / period
    return WMA

  def DEMA(list1, list2, period1):
    if len(list1) >= 1:
      DEMA = ((2 * list1[-1]) - Helpers.EMA(list1, list2, period1))
      return DEMA

  def FractalDimension(list1, period1):
    sp = int(period1 / 2)
    spe = len(list1) - sp
    N1 = (max(list1[-sp:]) - min(list1[-sp:])) / sp
    N2 = (max(list1[(abs(spe - sp)):spe]) -
          min(list1[(spe - sp):spe])) / sp
    N3 = (max(list1[-period1:]) - min(list1[-period1:])) / period1
    D = (math.log(N1 + N2) - math.log(N3)) / math.log(2)
    return D

  def FRAMA(list1, list2, period1):
    alpha = math.exp(float(config.gc['Indicators']['FRAMA']['Alpha Constant'])
                     * (Helpers.FractalDimension(list1, period1) - 1))
    if alpha < 0.01:
      alpha = 0.01
    elif alpha > 1:
      alpha = 1
    # If first run, use price instead of prev FRAMA before smoothing
    if len(list2) > 1:
      frama2 = list2[-2]
    else:
      frama2 = list1[-2]
    frama = alpha * list1[-1] + (1 - alpha) * frama2
    return frama

  def FastStochK(list1, period):
    if len(list1) >= period:
      LowestPeriod = min(float(s) for s in list1[(period * -1):])
      HighestPeriod = max(float(s) for s in list1[(period * -1):])
      FastStochK = ((list1[-1] - LowestPeriod) / (HighestPeriod
                                                  - LowestPeriod)) * 100
      return FastStochK

  def Ichimoku(list1, period1):
    PeriodList = list1[(period1 * -1):]
    Ichi = (max(PeriodList) + min(PeriodList)) / 2
    return Ichi

  def StdDev(list1, period):
    if len(list1) >= period:
      MeanAvg = math.fsum(list1[(period * -1):]) / period
      Deviation_list = [(i - MeanAvg) for i in list1[(period * -1):]]
      DeviationSq_list = [i ** 2 for i in Deviation_list]
      DeviationSqAvg = math.fsum(DeviationSq_list[(period * -1):])\
          / period
      StandardDeviation = math.sqrt(DeviationSqAvg)
      return StandardDeviation

  def TrueRange(list1, period):
    method1 = max(list1[-period:]) - min(list1[-period:])
    method2 = abs(max(list1[-period:]) - list1[-period - 1])
    method3 = abs(min(list1[-period:]) - list1[-period - 1])
    truerange = max(method1, method2, method3)
    return truerange

  def ListDiff(list1, list2):
    diff = 100 * (list1[-1] - list2[-1]) / ((list1[-1] + list2[-1]) / 2)
    return diff


# Relative Strength Index
class RSI:
  CandleDepends = (int(config.gc['Indicators']['RSI'][
                   'Period']) * float(config.gc['Indicators']['RSI']['Candle Size Multiplier'])) + 1

  def indicator():
    Period = int(config.gc['Indicators']['RSI'][
                 'Period']) * float(config.gc['Indicators']['RSI']['Candle Size Multiplier'])
    # We need a minimum of 2 candles to start RS calculations
    if len(ldb.price_list) >= 2:
      if ldb.price_list[-1] > ldb.price_list[-2]:
        gain = ldb.price_list[-1] - ldb.price_list[-2]
        storage.writelist('RSI_RS_gain_list', gain)
        storage.writelist('RSI_RS_loss_list', 0)
      elif ldb.price_list[-1] < ldb.price_list[-2]:
        loss = ldb.price_list[-2] - ldb.price_list[-1]
        storage.writelist('RSI_RS_loss_list', loss)
        storage.writelist('RSI_RS_gain_list', 0)

      # Do RS calculations if we have all requested periods
      if len(storage.getlist('RSI_RS_gain_list')) >= Period:
        if len(storage.getlist('RSI_avg_gain_list')) > 1:
          storage.writelist('RSI_avg_gain_list', ((storage.getlist('RSI_avg_gain_list')[-1] *
                                                   (Period - 1))
                                                  + storage.getlist('RSI_RS_gain_list')[-1])
                            / Period)
          storage.writelist('RSI_avg_loss_list', ((storage.getlist('RSI_avg_loss_list')[-1] *
                                                   (Period - 1))
                                                  + storage.getlist('RSI_RS_loss_list')[-1])
                            / Period)
        # Fist run, can't yet apply smoothing
        else:
          storage.writelist('RSI_avg_gain_list', math.fsum(
              storage.getlist('RSI_RS_gain_list')[(Period * -1):]) / Period)
          storage.writelist('RSI_avg_loss_list', math.fsum(
              storage.getlist('RSI_RS_loss_list')[(Period * -1):]) / Period)

        # Calculate and append current RS to RS_list
        storage.writelist('RSI_RS_list', storage.getlist(
            'RSI_avg_gain_list')[-1] / storage.getlist('RSI_avg_loss_list')[-1])

        # Calculate and append current RSI to ind_list
        storage.writelist(
            'RSI_ind_list', 100 - (100 / (1 + storage.getlist('RSI_RS_list')[-1])))

    if 'RSI' in config.gc['Trader']['Verbose Indicators']:
      if not storage.getlist('RSI_ind_list'):
        print('RSI: Not yet enough data to calculate')
      else:
        print('RSI:', storage.getlist('RSI_ind_list')[-1])


# Simple Movement Average
class SMA:
  CandleDepends = int(config.gc['Indicators']['SMA'][
                      'Long Period']) * float(config.gc['Indicators']['SMA']['Candle Size Multiplier'])

  def indicator():
    LongPeriod = int(config.gc['Indicators']['SMA'][
                     'Long Period']) * float(config.gc['Indicators']['SMA']['Candle Size Multiplier'])
    ShortPeriod = int(config.gc['Indicators']['SMA'][
                      'Short Period']) * float(config.gc['Indicators']['SMA']['Candle Size Multiplier'])
    # We can start SMA calculations once we have max period candles
    if len(ldb.price_list) >= max(LongPeriod, ShortPeriod):
      storage.writelist(
          'SMA_Short_list', Helpers.SMA(ldb.price_list, ShortPeriod))
      storage.writelist(
          'SMA_Long_list', Helpers.SMA(ldb.price_list, LongPeriod))
      storage.writelist('SMA_Diff_list', Helpers.ListDiff(
          storage.getlist('SMA_Short_list'), storage.getlist('SMA_Long_list')))

    if 'SMA' in config.gc['Trader']['Verbose Indicators']:
      if not storage.getlist('SMA_Long_list'):
        print('SMA: Not yet enough data to determine trend')
      else:
        gu.PrintIndicatorTrend('SMA', storage.getlist('SMA_Short_list'),
                               storage.getlist('SMA_Long_list'),
                               storage.getlist('SMA_Diff_list'),
                               float(
            config.gc['Indicators']['SMA']['Diff Down']),
            float(config.gc['Indicators']['SMA']['Diff Up']))


# Exponential Movement Average
class EMA:
  CandleDepends = int(config.gc['Indicators']['EMA'][
                      'Long Period']) * float(config.gc['Indicators']['EMA']['Candle Size Multiplier'])

  def indicator():
    LongPeriod = int(config.gc['Indicators']['EMA'][
                     'Long Period']) * float(config.gc['Indicators']['EMA']['Candle Size Multiplier'])
    ShortPeriod = int(config.gc['Indicators']['EMA'][
                      'Short Period']) * float(config.gc['Indicators']['EMA']['Candle Size Multiplier'])
    # We can start EMAs once we have max period candles
    if len(ldb.price_list) >= max(LongPeriod, ShortPeriod):
      storage.writelist('EMA_Short_list', Helpers.EMA(
          ldb.price_list, storage.getlist('EMA_Short_list'), ShortPeriod))
      storage.writelist('EMA_Long_list', Helpers.EMA(
          ldb.price_list, storage.getlist('EMA_Long_list'), LongPeriod))
      storage.writelist('EMA_Diff_list', Helpers.ListDiff(
          storage.getlist('EMA_Short_list'), storage.getlist('EMA_Long_list')))

    if 'EMA' in config.gc['Trader']['Verbose Indicators']:
      if not storage.getlist('EMA_Long_list'):
        print('EMA: Not yet enough data to determine trend')
      else:
        gu.PrintIndicatorTrend('EMA', storage.getlist('EMA_Short_list'), storage.getlist(
            'EMA_Long_list'), storage.getlist('EMA_Diff_list'),
            float(config.gc['Indicators']['EMA']['Diff Down']),
            float(config.gc['Indicators']['EMA']['Diff Up']))


# Double Exponential Movement Average
class DEMA:
  CandleDepends = int(config.gc['Indicators']['EMA'][
                      'Long Period']) + (int(config.gc[
                          'Indicators']['EMA']['Short Period']) * 2) * float(config.gc['Indicators']['EMA']['Candle Size Multiplier'])
  IndicatorDepends = ['EMA']

  def indicator():
    LongPeriod = int(config.gc['Indicators']['EMA'][
                     'Long Period']) * float(config.gc['Indicators']['EMA']['Candle Size Multiplier'])
    ShortPeriod = int(config.gc['Indicators']['EMA'][
                      'Short Period']) * float(config.gc['Indicators']['EMA']['Candle Size Multiplier'])
    # We can start DEMAs once we have max period candles
    if len(storage.getlist('EMA_Long_list')) >= max(LongPeriod, ShortPeriod):
      storage.writelist('DEMA_Short_list', Helpers.DEMA(storage.getlist(
          'EMA_Short_list'), storage.getlist('DEMA_Short_list'), ShortPeriod))
      storage.writelist('DEMA_Long_list', Helpers.DEMA(storage.getlist(
          'EMA_Long_list'), storage.getlist('DEMA_Long_list'), LongPeriod))
      storage.writelist('DEMA_Diff_list', Helpers.ListDiff(
          storage.getlist('DEMA_Short_list'), storage.getlist('DEMA_Long_list')))

    if 'DEMA' in config.gc['Trader']['Verbose Indicators']:
      if not storage.getlist('DEMA_Long_list'):
        print('DEMA: Not yet enough data to determine trend')
      else:
        gu.PrintIndicatorTrend('DEMA', storage.getlist('DEMA_Short_list'), storage.getlist(
            'DEMA_Long_list'), storage.getlist('DEMA_Diff_list'),
            float(config.gc['Indicators']['DEMA']['Diff Down']),
            float(config.gc['Indicators']['DEMA']['Diff Up']))


# Exponential Movement Average (using wbic16's logic)
class EMAwbic:
  CandleDepends = int(config.gc['Indicators']['EMAwbic'][
                      'Period']) * float(config.gc['Indicators']['EMA']['Candle Size Multiplier'])

  def indicator():
    Period = int(config.gc['Indicators']['EMA'][
                 'Period']) * float(config.gc['Indicators']['EMA']['Candle Size Multiplier'])
    if len(ldb.price_list) >= Period:
      storage.writelist('EMAwbic_EMA_list', Helpers.EMA(
          ldb.price_list, storage.getlist('EMAwbic_EMA_list'), Period))
      storage.writelist('EMAwbic_ind_list', ((ldb.price_list[-1] - storage.getlist(
          'EMAwbic_EMA_list')[-1]) / storage.getlist('EMAwbic_EMA_list')[-1]) * 100)

    if 'EMAwbic' in config.gc['Trader']['Verbose Indicators']:
      if not storage.getlist('EMAwbic_ind_list'):
        print('EMAwbic: Not yet enough data to calculate')
      else:
        print('EMAwbic:', storage.getlist('EMAwbic_ind_list')[-1], '%')


# Fractal Adaptive Moving Average
class FRAMA:
  CandleDepends = int(config.gc['Indicators']['FRAMA'][
                      'Long Period']) * float(config.gc['Indicators']['FRAMA']['Candle Size Multiplier'])

  def indicator():
    LongPeriod = int(config.gc['Indicators']['FRAMA'][
                     'Long Period']) * float(config.gc['Indicators']['FRAMA']['Candle Size Multiplier'])
    ShortPeriod = int(config.gc['Indicators']['FRAMA'][
                      'Short Period']) * float(config.gc['Indicators']['FRAMA']['Candle Size Multiplier'])
    # We can start FRAMAs once we have max period candles
    if len(ldb.price_list) >= (max(LongPeriod, ShortPeriod)):
      try:
        storage.writelist('FRAMA_Short_list', Helpers.FRAMA(
            ldb.price_list, storage.getlist('FRAMA_Short_list'), ShortPeriod))
        storage.writelist('FRAMA_Long_list', Helpers.FRAMA(
            ldb.price_list, storage.getlist('FRAMA_Long_list'), LongPeriod))
        storage.writelist('FRAMA_Diff_list', Helpers.ListDiff(
            storage.getlist('FRAMA_Short_list'), storage.getlist('FRAMA_Long_list')))
      # For a math domain error from log operations at low volatility or high
      # frequency
      except ValueError:
        pass

    if 'FRAMA' in config.gc['Trader']['Verbose Indicators']:
      if not storage.getlist('FRAMA_Long_list'):
        print('FRAMA: Not yet enough data to determine trend')
      else:
        gu.PrintIndicatorTrend('FRAMA', storage.getlist('FRAMA_Short_list'), storage.getlist(
            'FRAMA_Long_list'), storage.getlist('FRAMA_Diff_list'),
            float(config.gc['Indicators']['FRAMA']['Diff Down']),
            float(config.gc['Indicators']['FRAMA']['Diff Up']))


# Movement Average Convergence Divergence
class MACD:
  CandleDepends = int(config.gc['Indicators']['MACD']['Long Period']) + (int(
      config.gc['Indicators']['MACD']['Short Period']) / 2) * float(config.gc['Indicators']['MACD']['Candle Size Multiplier'])

  def indicator():
    LongPeriod = int(config.gc['Indicators']['MACD'][
                     'Long Period']) * float(config.gc['Indicators']['MACD']['Candle Size Multiplier'])
    ShortPeriod = int(config.gc['Indicators']['MACD'][
                      'Short Period']) * float(config.gc['Indicators']['MACD']['Candle Size Multiplier'])
    SignalPeriod = int(config.gc['Indicators']['MACD']['Signal Period'])
    # We can start MACD EMAs once we have max period candles
    if len(ldb.price_list) >= max(LongPeriod, ShortPeriod):
      storage.writelist('MACD_Short_list', Helpers.EMA(
          ldb.price_list, storage.getlist('MACD_Short_list'), ShortPeriod))
      storage.writelist('MACD_Long_list', Helpers.EMA(
          ldb.price_list, storage.getlist('MACD_Long_list'), LongPeriod))
      storage.writelist('MACD_ind_list', storage.getlist(
          'MACD_Short_list')[-1] - storage.getlist('MACD_Long_list')[-1])

      # We need SignalPeriod MACDs before generating MACDSignal
      if len(storage.getlist('MACD_Long_list')) >= SignalPeriod:
        storage.writelist('MACD_Signal_list', Helpers.EMA(storage.getlist(
            'MACD_ind_list'), storage.getlist('MACD_Signal_list'), SignalPeriod))
        storage.writelist('MACD_Histogram_list', storage.getlist(
            'MACD_ind_list')[-1] - storage.getlist('MACD_Signal_list')[-1])

      if 'MACD' in config.gc['Trader']['Verbose Indicators']:
        if not storage.getlist('MACD_Signal_list'):
          print('MACD: Not yet enough data to determine trend')
        else:
          gu.PrintIndicatorTrend('MACD', storage.getlist('MACD_ind_list'), storage.getlist(
              'MACD_Signal_list'), storage.getlist('MACD_ind_list'),
              float(config.gc['Indicators']['MACD']['Diff Down']),
              float(config.gc['Indicators']['MACD']['Diff Up']))
          print('MACD Hist:', storage.getlist('MACD_Histogram_list')[-1])


# Double Movement Average Convergence Divergence
class DMACD:
  IndicatorDepends = ['MACD']
  CandleDepends = ((int(config.gc['Indicators']['MACD']['Long Period']) + (int(
      config.gc['Indicators']['MACD']['Short Period']) / 2)) * 2) * float(config.gc['Indicators']['MACD']['Candle Size Multiplier'])

  def indicator():
    LongPeriod = int(config.gc['Indicators']['MACD'][
                     'Long Period']) * float(config.gc['Indicators']['MACD']['Candle Size Multiplier'])
    ShortPeriod = int(config.gc['Indicators']['MACD'][
                      'Short Period']) * float(config.gc['Indicators']['MACD']['Candle Size Multiplier'])
    SignalPeriod = int(config.gc['Indicators']['MACD']['Signal Period'])
    # We can start DEMAs once we have max period candles
    if len(storage.getlist('MACD_Long_list')) >= max(LongPeriod, ShortPeriod):
      storage.writelist('DMACD_Short_list', Helpers.DEMA(storage.getlist(
          'MACD_Short_list'), storage.getlist('DMACD_Short_list'), ShortPeriod))
      storage.writelist('DMACD_Long_list', Helpers.DEMA(storage.getlist(
          'MACD_Long_list'), storage.getlist('DMACD_Long_list'), LongPeriod))
      storage.writelist('DMACD_ind_list', storage.getlist(
          'DMACD_Short_list')[-1] - storage.getlist('DMACD_Long_list')[-1])

      # We need MACDSignal DMACDs before generating Signal
      if len(storage.getlist('DMACD_Long_list')) >= (SignalPeriod +
                                                     (abs(SignalPeriod - LongPeriod))):
        storage.writelist('DMACD_Signal_list', Helpers.DEMA(storage.getlist(
            'MACD_Signal_list'), storage.getlist('DMACD_Signal_list'), SignalPeriod))
        storage.writelist('DMACD_Histogram_list', storage.getlist(
            'DMACD_ind_list')[-1] - storage.getlist('DMACD_Signal_list')[-1])

      if 'DMACD' in config.gc['Trader']['Verbose Indicators']:
        if not storage.getlist('DMACD_Signal_list'):
          print('DMACD: Not yet enough data to determine trend')
        else:
          gu.PrintIndicatorTrend('DMACD', storage.getlist('DMACD_ind_list'), storage.getlist(
              'DMACD_Signal_list'), storage.getlist('DMACD_ind_list'),
              float(config.gc['Indicators']['DMACD']['Diff Down']),
              float(config.gc['Indicators']['DMACD']['Diff Up']))


# Fast Stochastic %K
class FastStochK:
  CandleDepends = int(config.gc['Indicators']['Fast Stochastic %K'][
                      'Period']) * float(config.gc['Indicators']['Fast Stochastic %K']['Candle Size Multiplier'])

  def indicator():
    Period = int(config.gc['Indicators']['Fast Stochastic %K'][
                 'Period']) * float(config.gc['Indicators']['Fast Stochastic %K']['Candle Size Multiplier'])
    # We can start FastStochK calculations once we have FastStochKPeriod
    # candles, otherwise we append None until met
    if len(ldb.price_list) >= Period:
      try:
        storage.writelist('FastStochK_ind_list', Helpers.FastStochK(
            ldb.price_list, Period))
      except ZeroDivisionError:
        pass

    if 'FastStochK' in config.gc['Trader']['Verbose Indicators']:
      if not storage.getlist('FastStochK_ind_list'):
        print('FastStochK: Not yet enough data to calculate')
      else:
        print('FastStochK:', storage.getlist('FastStochK_ind_list')[-1])


# Fast Stochastic %D
class FastStochD:
  IndicatorDepends = ['FastStochK']
  CandleDepends = int(config.gc['Indicators']['Fast Stochastic %K'][
                      'Period']) + (int(config.gc['Indicators'][
                          'Fast Stochastic %D']['Period']) - 1)

  def indicator():
    Period = int(config.gc['Indicators']['Fast Stochastic %D']['Period'])
    # We can start FastStochD calculations once we have FastStochDPeriod
    # candles, otherwise we append None until met
    if len(ldb.price_list) >= Period:
      storage.writelist('FastStochD_ind_list', Helpers.SMA(
          storage.getlist('FastStochK_ind_list'), Period))

    if 'FastStochD' in config.gc['Trader']['Verbose Indicators']:
      if not storage.getlist('FastStochD_ind_list'):
        print('FastStochD: Not yet enough data to calculate')
      else:
        print('FastStochD:', storage.getlist('FastStochD_ind_list')[-1])


# Full Stochastic %D
class FullStochD:
  IndicatorDepends = ['FastStochK', 'FastStochD']
  CandleDepends = int(config.gc['Indicators']['Fast Stochastic %K'][
                      'Period']) + (int(config.gc['Indicators'][
                          'Fast Stochastic %D']['Period']) - 1) + (int(
                              config.gc['Indicators']['Full Stochastic %D'][
                                  'Period']) - 1)

  def indicator():
    Period = int(config.gc['Indicators']['Full Stochastic %D']['Period'])
    # We can start FullStochD calculations once we have FullStochDPeriod
    # candles, otherwise we append None until met
    if len(storage.getlist('FastStochD_ind_list')) >= Period:
      storage.writelist('FullStochD_ind_list', Helpers.SMA(
          storage.getlist('FastStochD_ind_list'), Period))

    if 'FullStochD' in config.gc['Trader']['Verbose Indicators']:
      if not storage.getlist('FullStochD_ind_list'):
        print('FullStochD: Not yet enough data to calculate')
      else:
        print('FullStochD:', storage.getlist('FullStochD_ind_list')[-1])


# Fast Stochastic RSI %K
class FastStochRSIK:
  IndicatorDepends = ['RSI']
  CandleDepends = (int(config.gc['Indicators']['RSI']['Period']) * 2) + (
      int(config.gc['Indicators']['Fast Stochastic RSI %K']['Period']) - 1)

  def indicator():
    Period = int(config.gc['Indicators']['Fast Stochastic RSI %K']['Period'])

    # We can start FastStochRSIK calculations once we have
    # FastStochRSIKPeriod candles, otherwise we append None until met
    if len(storage.getlist('RSI_ind_list')) >= Period:
      try:
        storage.writelist('FastStochRSIK_ind_list', Helpers.FastStochK(
            storage.getlist('RSI_ind_list'), Period))
      except ZeroDivisionError:
        pass

    if 'FastStochRSIK' in config.gc['Trader']['Verbose Indicators']:
      if not storage.getlist('FastStochRSIK_ind_list'):
        print('FastStochRSIK: Not yet enough data to calculate')
      else:
        print('FastStochRSIK:', storage.getlist('FastStochRSIK_ind_list')[-1])


# Fast Stochastic RSI %D
class FastStochRSID:
  IndicatorDepends = ['RSI', 'FastStochRSIK']
  CandleDepends = (int(config.gc['Indicators']['RSI']['Period']) * 2) + (
      int(config.gc['Indicators']['Fast Stochastic RSI %K']['Period']) - 1) + (
      int(config.gc['Indicators']['Fast Stochastic RSI %D']['Period']) - 1)

  def indicator():
    Period = int(config.gc['Indicators']['Fast Stochastic RSI %D']['Period'])
    # We can start FastStochRSID calculations once we have
    # FastStochRSIDPeriod candles, otherwise we append None until met
    if len(storage.getlist('FastStochRSIK_ind_list')) >= Period:
      storage.writelist('FastStochRSID_ind_list', Helpers.SMA(
          storage.getlist('FastStochRSIK_ind_list'), Period))

    if 'FastStochRSID' in config.gc['Trader']['Verbose Indicators']:
      if not storage.getlist('FastStochRSID_ind_list'):
        print('FastStochRSID: Not yet enough data to calculate')
      else:
        print('FastStochRSID:', storage.getlist('FastStochRSID_ind_list')[-1])


# Fast Stochastic RSI %D
class FullStochRSID:
  IndicatorDepends = ['RSI', 'FastStochRSIK', 'FastStochRSID']
  CandleDepends = (int(config.gc['Indicators']['RSI']['Period']) * 2) + (
      int(config.gc['Indicators']['Fast Stochastic RSI %K']['Period']) - 1) + (
      int(config.gc['Indicators']['Fast Stochastic RSI %D']['Period']) - 1) + (
      int(config.gc['Indicators']['Full Stochastic RSI %D']['Period']) - 1)

  def indicator():
    Period = int(config.gc['Indicators']['Full Stochastic RSI %D']['Period'])
    # We can start FullStochRSID calculations once we have
    # FullStochRSIDPeriod candles, otherwise we append None until met
    if len(storage.getlist('FastStochRSID_ind_list')) >= Period:
      storage.writelist('FullStochRSID_ind_list', Helpers.SMA(
          storage.getlist('FastStochRSID_ind_list'), Period))

    if 'FullStochRSID' in config.gc['Trader']['Verbose Indicators']:
      if not storage.getlist('FullStochRSID_ind_list'):
        print('FullStochRSID: Not yet enough data to calculate')
      else:
        print('FullStochRSID:', storage.getlist('FullStochRSID_ind_list')[-1])


# KDJ
class KDJ:
  CandleDepends = int(config.gc['Indicators']['KDJ']['Fast K Period']) + int(
      config.gc['Indicators']['KDJ']['Full K Period']) + (int(config.gc[
          'Indicators']['KDJ']['Full D Period']) - 2) * float(config.gc['Indicators']['KDJ']['Candle Size Multiplier'])

  def indicator():
    FastKPeriod = int(config.gc['Indicators']['KDJ'][
                      'Fast K Period']) * float(config.gc['Indicators']['KDJ']['Candle Size Multiplier'])
    FullKPeriod = int(config.gc['Indicators']['KDJ'][
                      'Full K Period']) * float(config.gc['Indicators']['KDJ']['Candle Size Multiplier'])
    FullDPeriod = int(config.gc['Indicators']['KDJ'][
                      'Full D Period']) * float(config.gc['Indicators']['KDJ']['Candle Size Multiplier'])
    if len(ldb.price_list) >= FastKPeriod:
      try:
        storage.writelist(
            'KDJ_FastK_list', Helpers.FastStochK(ldb.price_list, FastKPeriod))
      except ZeroDivisionError:
        pass
    if len(storage.getlist('KDJ_FastK_list')) >= FullKPeriod:
      storage.writelist('KDJ_FullK_list', Helpers.SMA(
          storage.getlist('KDJ_FastK_list'), FullKPeriod))
    if len(storage.getlist('KDJ_FullK_list')) >= FullDPeriod:
      storage.writelist('KDJ_FullD_list', Helpers.SMA(
          storage.getlist('KDJ_FullK_list'), FullDPeriod))
    if storage.getlist('KDJ_FullD_list'):
      storage.writelist('KDJ_J_list', (3 * storage.getlist('KDJ_FullD_list')
                                       [-1]) - (2 * storage.getlist('KDJ_FullK_list')[-1]))

    if 'KDJ' in config.gc['Trader']['Verbose Indicators']:
      if not storage.getlist('KDJ_J_list'):
        print('KDJ: Not yet enough data to determine trend or calculate')
      else:
        gu.PrintIndicatorTrend('KDJ', storage.getlist('KDJ_FullK_list'), storage.getlist(
            'KDJ_FullD_list'), storage.getlist('KDJ_J_list'), float(config.gc[
                'Indicators']['KDJ']['Bid']), float(config.gc['Indicators'][
                    'KDJ']['Ask']), False)


# Aroon Oscillator
class Aroon:
  CandleDepends = int(config.gc['Indicators']['Aroon'][
                      'Period']) * float(config.gc['Indicators']['Aroon']['Candle Size Multiplier'])

  def indicator():
    Period = int(config.gc['Indicators']['Aroon'][
                 'Period']) * float(config.gc['Indicators']['Aroon']['Candle Size Multiplier'])
    # We must have AroonPeriod ldb.price_list candles
    if len(ldb.price_list) >= Period:
      storage.writelist('Aroon_Up_list', 100 * (Period -
                                                (Period - ([i for i, x in enumerate(ldb.price_list)
                                                            if x == max(ldb.price_list[(Period * -1):])][0] + 1
                                                           )) / Period))
      storage.writelist('Aroon_Down_list', 100 * (Period -
                                                  (Period - ([i for i, x in enumerate(ldb.price_list)
                                                              if x == min(ldb.price_list[(Period * -1):])][0] + 1
                                                             )) / Period))
      storage.writelist('Aroon_ind_list', storage.getlist(
          'Aroon_Up_list')[-1] - storage.getlist('Aroon_Down_list')[-1])

    if 'Aroon' in config.gc['Trader']['Verbose Indicators']:
      if not storage.getlist('Aroon_ind_list'):
        print('Aroon: Not yet enough data to determine trend or calculate')
      else:
        gu.PrintIndicatorTrend('Aroon', storage.getlist('Aroon_Up_list'), storage.getlist(
            'Aroon_Down_list'), storage.getlist('Aroon_ind_list'), float(config.gc[
                'Indicators']['Aroon']['Bid']), float(config.gc['Indicators'][
                    'Aroon']['Bid']), False)


# Ichimoku Cloud
class Ichimoku:
  CandleDepends = int(config.gc['Indicators']['Ichimoku']['Tenkan-Sen Period']) + \
      int(config.gc['Indicators']['Ichimoku']['Senkou Span Period']) + \
      int(config.gc['Indicators']['Ichimoku']['Kijun-Sen Period'])

  def indicator():
    TSP = int(config.gc['Indicators']['Ichimoku']['Tenkan-Sen Period']) * \
        float(config.gc['Indicators']['Ichimoku']['Candle Size Multiplier'])
    SSP = int(config.gc['Indicators']['Ichimoku']['Senkou Span Period']) * \
        float(config.gc['Indicators']['Ichimoku']['Candle Size Multiplier'])
    KSP = int(config.gc['Indicators']['Ichimoku']['Kijun-Sen Period']) * \
        float(config.gc['Indicators']['Ichimoku']['Candle Size Multiplier'])
    CSP = int(config.gc['Indicators']['Ichimoku']['Chikou Span Period']) * \
        float(config.gc['Indicators']['Ichimoku']['Candle Size Multiplier'])
    IS = config.gc['Indicators']['Ichimoku']['Indicator Strategy']
    # We must have SenkouSpanPeriod price candles before starting
    # calculations, otherwise we append None
    # NOTE: Chikou Span's cool and all, but we don't care. We want to trade in
    # real time, and price list 26 periods behind only confirms if we *were*
    # right or wrong
    if len(ldb.price_list) >= SSP:
      storage.writelist('Ichimoku_TenkanSen_list', Helpers.Ichimoku(
          ldb.price_list, TSP))
      storage.writelist('Ichimoku_KijunSen_list', Helpers.Ichimoku(
          ldb.price_list, KSP))
      storage.writelist('Ichimoku_SenkouSpanART_list', (storage.getlist(
          'Ichimoku_TenkanSen_list')[-1] + storage.getlist('Ichimoku_KijunSen_list')[-1]) / 2)
      storage.writelist('Ichimoku_SenkouSpanBRT_list', Helpers.Ichimoku(
          ldb.price_list, SSP))
    # We need SenkouSpan to be ChikouSpanPeriod in the future
    if len(storage.getlist('Ichimoku_SenkouSpanBRT_list')) >= CSP:
      storage.writelist('Ichimoku_SenkouSpanA_list', storage.getlist(
          'Ichimoku_SenkouSpanART_list')[-CSP])
      storage.writelist('Ichimoku_SenkouSpanB_list', storage.getlist(
          'Ichimoku_SenkouSpanBRT_list')[-CSP])
    # Don't want to implement a new trade strategy, so just treat
    # Ichimoku lists as threshold strategies for IndicatorList.
    if storage.getlist('Ichimoku_SenkouSpanB_list'):
      CloudMin = min(storage.getlist('Ichimoku_SenkouSpanA_list')
                     [-1], storage.getlist('Ichimoku_SenkouSpanB_list')[-1])
      CloudMax = max(storage.getlist('Ichimoku_SenkouSpanA_list')
                     [-1], storage.getlist('Ichimoku_SenkouSpanB_list')[-1])

      CP = ldb.price_list[-1]
      KS = storage.getlist('Ichimoku_KijunSen_list')[-1]
      TS = storage.getlist('Ichimoku_TenkanSen_list')[-1]

      # Strong Signals
      if CP > CloudMin and CP < KS and CP > TS:
        # BUY!
        storage.writelist('Ichimoku_Strong_list', -1)
        StrongTrend = 'Bullish'
      elif CP < CloudMax and CP > KS and CP < TS:
        # SELL!
        storage.writelist('Ichimoku_Strong_list', 1)
        StrongTrend = 'Bearish'
      else:
        storage.writelist('Ichimoku_Strong_list', 0)
        StrongTrend = 'No trend'
      # Optimized Signals
      if CP > CloudMin and TS > KS:
        # BUY!
        storage.writelist('Ichimoku_Optimized_list', -1)
        OptimizedTrend = 'Bullish'
      elif CP < CloudMax and KS > TS:
        # SELL!
        storage.writelist('Ichimoku_Optimized_list', 1)
        OptimizedTrend = 'Bearish'
      else:
        storage.writelist('Ichimoku_Optimized_list', 0)
        OptimizedTrend = 'No trend'
      # Weak Signals
      if TS > KS:
        # BUY!
        storage.writelist('Ichimoku_Weak_list', -1)
        WeakTrend = 'Bullish'
      elif KS > TS:
        # SELL!
        storage.writelist('Ichimoku_Weak_list', 1)
        WeakTrend = 'Bearish'
      else:
        storage.writelist('Ichimoku_Weak_list', 0)
        WeakTrend = 'No trend'

      # Store price cloud history
      if CP < CloudMin:
        # Below
        storage.writelist('Ichimoku_CloudHistory_list', -1)
      elif CP > CloudMin and CP < CloudMax:
        # Inside
        storage.writelist('Ichimoku_CloudHistory_list', 0)
      elif CP > CloudMax:
        # Above
        storage.writelist('Ichimoku_CloudHistory_list', 1)

      # CloudOnly signals
      CH = storage.getlist('Ichimoku_CloudHistory_list')
      if len(CH) > 1:
        if CH[-2] == -1 and CH[-1] == 0:
          # Buy
          storage.writelist('Ichimoku_CloudOnly_list', -1)
          CloudOnlyTrend = 'Bullish'
        elif CH[-2] == 0 and CH[-1] == 1:
          # Buy
          storage.writelist('Ichimoku_CloudOnly_list', -1)
          CloudOnlyTrend = 'Bullish'
        elif CH[-2] == -1 and CH[-1] == 1:
          # Buy
          storage.writelist('Ichimoku_CloudOnly_list', -1)
          CloudOnlyTrend = 'Bullish'
        elif CH[-2] == 1 and CH[-1] == 0:
          # Sell
          storage.writelist('Ichimoku_CloudOnly_list', 1)
          CloudOnlyTrend = 'Bearish'
        elif CH[-2] == 0 and CH[-1] == -1:
          # Sell
          storage.writelist('Ichimoku_CloudOnly_list', 1)
          CloudOnlyTrend = 'Bearish'
        elif CH[-2] == 1 and CH[-1] == -1:
          # Sell
          storage.writelist('Ichimoku_CloudOnly_list', 1)
          CloudOnlyTrend = 'Bearish'
        else:
          # No signal
          storage.writelist('Ichimoku_CloudOnly_list', 0)
          CloudOnlyTrend = 'No new signal'
      else:
        # Generate initial CloudOnly signal
        if CH[-1] == -1:
          # Sell
          storage.writelist('Ichimoku_CloudOnly_list', 1)
          CloudOnlyTrend = 'Bearish'
        elif CH[-1] == 1:
          # Buy
          storage.writelist('Ichimoku_CloudOnly_list', -1)
          CloudOnlyTrend = 'Bullish'
        else:
          storage.writelist('Ichimoku_CloudOnly_list', 0)
          CloudOnlyTrend = 'Need more cloud history'

      if IS == 'Strong':
        trend = StrongTrend
      elif IS == 'Weak':
        trend = WeakTrend
      elif IS == 'Optimized':
        trend = OptimizedTrend
      elif IS == 'CloudOnly':
        trend = CloudOnlyTrend
      if 'Ichimoku' in config.gc['Trader']['Verbose Indicators']:
        print('Ichimoku:', trend)
    else:
      if 'Ichimoku' in config.gc['Trader']['Verbose Indicators']:
        print('Ichimoku: Not yet enough data to determine trend or calculate')


# Volatility/Movement Strength Indicators/Indexes

# Sample Standard Deviation
class StdDev:
  CandleDepends = int(config.gc['Indicators']['Standard Deviation']['Period'])

  def indicator():
    Period = int(config.gc['Indicators']['Standard Deviation'][
                 'Period']) * float(config.gc['Indicators']['Standard Deviation']['Candle Size Multiplier'])
    # We can start StdDev calculations once we have StdDevSample
    # candles, otherwise we append None until met
    if len(ldb.price_list) >= Period:
      storage.writelist(
          'StdDev_ind_list', Helpers.StdDev(ldb.price_list, Period))

    if 'StdDev' in config.gc['Trader']['Verbose Indicators']:
      if storage.getlist('StdDev_ind_list'):
        print('StdDev:', storage.getlist('StdDev_ind_list')[-1])
      else:
        print('StdDev: Not yet enough data to calculate')


# Bollinger Bands
class BollBands:
  CandleDepends = int(config.gc['Indicators']['Bollinger Bands'][
                      'Period']) * float(config.gc['Indicators']['Bollinger Bands']['Candle Size Multiplier'])

  def indicator():
    Period = int(config.gc['Indicators']['Bollinger Bands']['Period'])
    # We can start BollBand calculations once we have BollBandPeriod candles
    if len(ldb.price_list) >= Period:
      storage.writelist(
          'BollBands_Middle_list', Helpers.SMA(ldb.price_list, Period))
      storage.writelist('BollBands_Upper_list', storage.getlist(
          'BollBands_Middle_list')[-1] + (Helpers.StdDev(ldb.price_list, Period) * 2))
      storage.writelist('BollBands_Lower_list', storage.getlist(
          'BollBands_Middle_list')[-1] - (Helpers.StdDev(ldb.price_list, Period) * 2))


# Bollinger Bandwidth
class BollBandwidth:
  CandleDepends = int(config.gc['Indicators']['Bollinger Bands'][
                      'Period']) * float(config.gc['Indicators']['Bollinger Bands']['Candle Size Multiplier'])
  IndicatorDepends = ['BollBands']

  def indicator():
    # We can start BollBandwidth calculations once we have BollBands
    if storage.getlist('BollBands_Lower_list'):
      storage.writelist('BollBandwidth_ind_list', (storage.getlist(
          'BollBands_Upper_list')[-1] - storage.getlist('BollBands_Lower_list')[-1]) / storage.getlist('BollBands_Middle_list')[-1])

    if 'BollBandwidth' in config.gc['Trader']['Verbose Indicators']:
      if storage.getlist('BollBandwidth_ind_list'):
        print('BollBandwidth:', storage.getlist('BollBandwidth_ind_list')[-1])
      else:
        print('BollBandwidth: Not yet enough data to calculate')


# Average True Range
class ATR:
  CandleDepends = ((int(config.gc['Indicators']['Average True Range'][
                   'Period']) * 3) - 1) * float(config.gc['Indicators']['Average True Range']['Candle Size Multiplier'])

  def indicator():
    Period = int(config.gc['Indicators']['Average True Range'][
                 'Period']) * float(config.gc['Indicators']['Average True Range']['Candle Size Multiplier'])
    # We can start ATR calculations once we have two periods
    if len(ldb.price_list) >= (Period * 2):
      storage.writelist(
          'ATR_TR_list', Helpers.TrueRange(ldb.price_list, Period))
      if len(storage.getlist('ATR_TR_list')) >= Period:
        storage.writelist('ATR_ind_list', Helpers.WMA(
            storage.getlist('ATR_TR_list'), storage.getlist('ATR_ind_list'), Period))

    if 'ATR' in config.gc['Trader']['Verbose Indicators']:
      if storage.getlist('ATR_ind_list'):
        print('ATR:', storage.getlist('ATR_ind_list')[-1])
      else:
        print('ATR: Not yet enough data to calculate')


# Chandelier Exit
class ChandExit:
  CandleDepends = ((int(config.gc['Indicators']['Chandelier Exit']['Period']) *
                    int(config.gc['Indicators']['Chandelier Exit']['Multiplier'])) - 1) * \
                    float(config.gc['Indicators']['Ichimoku']['Candle Size Multiplier'])

  def indicator():
    Period = int(config.gc['Indicators']['Chandelier Exit'][
                 'Period']) * float(config.gc['Indicators']['Chandelier Exit']['Candle Size Multiplier'])
    Multiplier = int(config.gc['Indicators']['Chandelier Exit']['Multiplier'])
    # We can start calculations once we have two periods
    if len(ldb.price_list) >= (Period * 2):
      storage.writelist(
          'ChandExit_TR_list', Helpers.TrueRange(ldb.price_list, Period))
      if len(storage.getlist('ChandExit_TR_list')) >= Period:
        try:
          storage.writelist('ChandExit_ATR_list', Helpers.WMA(storage.getlist(
              'ChandExit_TR_list'), storage.getlist('ChandExit_ATR_list'), Period))
          storage.writelist('ChandExit_Long_list', max(
              ldb.price_list[-Period:]) - storage.getlist('ChandExit_ATR_list')[-1] * Multiplier)
          storage.writelist('ChandExit_Short_list', min(
              ldb.price_list[-Period:]) + storage.getlist('ChandExit_ATR_list')[-1] * Multiplier)
        # For an empty sequence at low volatility or high frequency
        except ValueError:
          pass

        # Use a hack for determining signals despite it's intended confirmation
        # usage
        cp = ldb.price_list[-1]
        if cp < storage.getlist('ChandExit_Long_list')[-1]:
          storage.writelist('ChandExit_signal_list', 1)
        elif cp > storage.getlist('ChandExit_Short_list')[-1]:
          storage.writelist('ChandExit_signal_list', -1)

    if 'ChandExit' in config.gc['Trader']['Verbose Indicators']:
      if storage.getlist('ChandExit_Short_list'):
        print('ChandExit: Short:',
              storage.getlist('ChandExit_Short_list')[-1], 'Long:',
              storage.getlist('ChandExit_Long_list')[-1])
      else:
        print('ChandExit: Not yet enough data to calculate')


# Directional Movement
class DMI:
  CandleDepends = (int(config.gc['Indicators']['Average True Range'][
                   'Period']) * 5) * float(config.gc['Indicators']['Average True Range']['Candle Size Multiplier'])
  DMITrend = 'No Trend'

  def indicator():
    Period = int(config.gc['Indicators']['Average True Range'][
                 'Period']) * float(config.gc['Indicators']['Average True Range']['Candle Size Multiplier'])
    # We can start DMI calculations once we have two ATR periods
    if len(ldb.price_list) >= (Period * 2):
      UpMove = max(ldb.price_list[-Period:]) - max(
          ldb.price_list[(len(ldb.price_list) - (Period * 2)):-Period])
      DownMove = min(ldb.price_list[-Period:]) - min(
          ldb.price_list[(len(ldb.price_list) - (Period * 2)):-Period])
      if UpMove < 0 and DownMove < 0:
        storage.writelist('DMI_PosDM_list', 0)
        storage.writelist('DMI_NegDM_list', 0)
      elif UpMove > DownMove:
        storage.writelist('DMI_PosDM_list', UpMove)
        storage.writelist('DMI_NegDM_list', 0)
      elif UpMove < DownMove:
        storage.writelist('DMI_PosDM_list', 0)
        storage.writelist('DMI_NegDM_list', DownMove)

      if len(storage.getlist('DMI_PosDM_list')) >= Period and len(storage.getlist('ATR_TR_list')) >= Period:
        storage.writelist('DMI_PosDMWMA_list',
                          Helpers.WMA(storage.getlist('DMI_PosDM_list'),
                                      storage.getlist('DMI_PosDMWMA_list'), Period))
        storage.writelist('DMI_NegDMWMA_list',
                          Helpers.WMA(storage.getlist('DMI_NegDM_list'),
                                      storage.getlist('DMI_NegDMWMA_list'), Period))
        storage.writelist('DMI_PosDI_list',
                          storage.getlist('DMI_PosDMWMA_list')[-1]
                          / storage.getlist('ATR_ind_list')[-1])
        storage.writelist('DMI_NegDI_list',
                          storage.getlist('DMI_NegDMWMA_list')[-1]
                          / storage.getlist('ATR_ind_list')[-1])

        DIDiff = abs(storage.getlist('DMI_PosDI_list')[-1]
                     - storage.getlist('DMI_NegDI_list')[-1])
        try:
          storage.writelist('DMI_DX_list', DIDiff
                            / (storage.getlist('DMI_PosDI_list')[-1]
                               + storage.getlist('DMI_NegDI_list')[-1]))
          # ADX
          if len(storage.getlist('DMI_DX_list')) >= (Period * 2):
            storage.writelist('DMI_ind_list',
                              Helpers.WMA(storage.getlist('DMI_DX_list'),
                                          storage.getlist('DMI_ind_list'), Period))
        except ZeroDivisionError:
          pass

        # Hack for trading with both DI crossovers and ADX threshold.
        if storage.getlist('DMI_ind_list'):
          if storage.getlist('DMI_ind_list')[-1] > float(config.gc['Indicators']['Directional Movment Index']['Threshold']):
            if storage.getlist('DMI_PosDI_list')[-1] > storage.getlist('DMI_NegDI_list')[-1]:
              # Buy
              storage.writelist('DMI_DMISignal_list', -1)
              DMI.DMITrend = 'Uptrend'
            elif storage.getlist('DMI_PosDI_list')[-1] < storage.getlist('DMI_NegDI_list')[-1]:
              # Sell
              storage.writelist('DMI_DMISignal_list', 1)
              DMI.DMITrend = 'Downtrend'
            else:
              storage.writelist('DMI_DMISignal_list', 0)
              DMI.DMITrend = 'No trend'
          else:
            storage.writelist('DMI_DMISignal_list', 0)
            DMI.DMITrend = 'No trend'

    if 'DMI' in config.gc['Trader']['Verbose Indicators']:
      if storage.getlist('DMI_ind_list'):
        if config.gc['Indicators']['Directional Movement Index']['Indicator Strategy'] == 'Full':
          print('DMI:', DMI.DMITrend)
        else:
          print('ADX:', storage.getlist('DMI_ind_list')[-1])
      else:
        print('DMI: Not yet enough data to calculate')


# (Simple) Rate of Change (Momentum)
class SROC:
  CandleDepends = (int(config.gc['Indicators']['Simple Rate of Change'][
                   'Period']) + 1) * float(config.gc['Indicators']['Simple Rate of Change']['Candle Size Multiplier'])

  def indicator():
    Period = int(config.gc['Indicators']['Simple Rate of Change'][
                 'Period']) * float(config.gc['Indicators']['Simple Rate of Change']['Candle Size Multiplier'])
    # We can start ROC calculations once we have SROC Periods of Price
    if len(ldb.price_list) >= Period:
      storage.writelist(
          'SROC_SROC_list', ldb.price_list[-1] - ldb.price_list[-Period])

    # Treat as a diff strat so we don't need to add strategy support
    if len(storage.getlist('SROC_SROC_list')) >= 2:
      s = storage.getlist('SROC_SROC_list')
      if s[-1] > 0 and s[-2] <= 0:
        # BUY!
        storage.writelist('SROC_ind_list', -1)
        trend = 'an Uptrend'
      elif s[-1] < 0 and s[-2] >= 0:
        # SELL!
        storage.writelist('SROC_ind_list', 1)
        trend = 'a Downtrend'
      else:
        # No signal
        storage.writelist('SROC_ind_list', 0)
        trend = 'No trend'
      if 'SROC' in config.gc['Trader']['Verbose Indicators']:
        print('SROC: We are in ', trend)
