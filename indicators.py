import math

import genconfig as gc
import genutils as gu
import loggerdb as ldb


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
    alpha = math.exp(gc.FRAMA.AlphaConstant
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
  RS_list = []
  ind_list = []
  RS_gain_list = []
  RS_loss_list = []
  avg_gain_list = []
  avg_loss_list = []

  def indicator():
    # We need a minimum of 2 candles to start RS calculations
    if len(ldb.price_list) >= 2:
      if ldb.price_list[-1] > ldb.price_list[-2]:
        gain = ldb.price_list[-1] - ldb.price_list[-2]
        RSI.RS_gain_list.append(gain)
        RSI.RS_loss_list.append(0)
      elif ldb.price_list[-1] < ldb.price_list[-2]:
        loss = ldb.price_list[-2] - ldb.price_list[-1]
        RSI.RS_loss_list.append(loss)
        RSI.RS_gain_list.append(0)

      # Do RS calculations if we have all requested periods
      if len(RSI.RS_gain_list) >= gc.RSI.Period:
        if len(RSI.avg_gain_list) > 1:
          RSI.avg_gain_list.append(((RSI.avg_gain_list[-1] *
                                     (gc.RSI.Period - 1)) + RSI.RS_gain_list[-1])
                                   / gc.RSI.Period)
          RSI.avg_loss_list.append(((RSI.avg_loss_list[-1] *
                                     (gc.RSI.Period - 1)) + RSI.RS_loss_list[-1])
                                   / gc.RSI.Period)
        # Fist run, can't yet apply smoothing
        else:
          RSI.avg_gain_list.append(math.fsum(RSI.RS_gain_list[(
              gc.RSI.Period * -1):]) / gc.RSI.Period)
          RSI.avg_loss_list.append(math.fsum(RSI.RS_loss_list[(
              gc.RSI.Period * -1):]) / gc.RSI.Period)

        # Calculate and append current RS to RS_list
        RSI.RS_list.append(
            RSI.avg_gain_list[-1] / RSI.avg_loss_list[-1])

        # Calculate and append current RSI to ind_list
        RSI.ind_list.append(100 - (100 / (1 + RSI.RS_list[-1])))

    if 'RSI' in gc.VerboseIndicators:
      if len(RSI.ind_list) < 1:
        print('RSI: Not yet enough data to calculate')
      else:
        # ind_list is externally accessible, so return None
        print('RSI:', RSI.ind_list[-1])


# Simple Movement Average
class SMA:
  Short_list = []
  Long_list = []
  Diff_list = []

  def indicator():
    # We can start SMA calculations once we have max period candles
    if len(ldb.price_list) >= max(gc.SMA.LongPeriod, gc.SMA.ShortPeriod):
      SMA.Short_list.append(
          Helpers.SMA(ldb.price_list, gc.SMA.ShortPeriod))
      SMA.Long_list.append(
          Helpers.SMA(ldb.price_list, gc.SMA.LongPeriod))
      SMA.Diff_list.append(
          Helpers.ListDiff(SMA.Short_list, SMA.Long_list))

    if 'SMA' in gc.VerboseIndicators:
      if len(SMA.Long_list) < 1:
        print('SMA: Not yet enough data to determine trend')
      else:
        gu.PrintIndicatorTrend('SMA', SMA.Short_list, SMA.Long_list,
                               SMA.Diff_list, gc.SMA.DiffDown, gc.SMA.DiffUp)


# Exponential Movement Average
class EMA:
  Short_list = []
  Long_list = []
  Diff_list = []

  def indicator():
    # We can start EMAs once we have max period candles
    if len(ldb.price_list) >= max(gc.EMA.LongPeriod, gc.EMA.ShortPeriod):
      EMA.Short_list.append(Helpers.EMA(ldb.price_list, EMA.Short_list,
                                        gc.EMA.ShortPeriod))
      EMA.Long_list.append(Helpers.EMA(ldb.price_list, EMA.Long_list,
                                       gc.EMA.LongPeriod))
      EMA.Diff_list.append(
          Helpers.ListDiff(EMA.Short_list, EMA.Long_list))

    if 'EMA' in gc.VerboseIndicators:
      if len(EMA.Long_list) < 1:
        print('EMA: Not yet enough data to determine trend')
      else:
        gu.PrintIndicatorTrend('EMA', EMA.Short_list, EMA.Long_list,
                               EMA.Diff_list, gc.EMA.DiffDown, gc.EMA.DiffUp)


# Double Exponential Movement Average
class DEMA:
  Short_list = []
  Long_list = []
  Diff_list = []

  def indicator():
    # We can start DEMAs once we have max period candles
    if len(EMA.Long_list) >= max(gc.EMA.LongPeriod, gc.EMA.ShortPeriod):
      DEMA.Short_list.append(Helpers.DEMA(EMA.Short_list, DEMA.Short_list,
                                          gc.EMA.ShortPeriod))
      DEMA.Long_list.append(Helpers.DEMA(EMA.Long_list, DEMA.Long_list,
                                         gc.EMA.LongPeriod))
      DEMA.Diff_list.append(
          Helpers.ListDiff(DEMA.Short_list, DEMA.Long_list))

    if 'DEMA' in gc.VerboseIndicators:
      if len(DEMA.Long_list) < 1:
        print('DEMA: Not yet enough data to determine trend')
      else:
        gu.PrintIndicatorTrend('DEMA', DEMA.Short_list, DEMA.Long_list,
                               DEMA.Diff_list, gc.DEMA.DiffDown, gc.DEMA.DiffUp)


# Exponential Movement Average (using wbic16's logic)
class EMAwbic:
  ind_list = []
  EMA_list = []

  def indicator():
    if len(ldb.price_list) >= gc.EMAwbic.Period:
      EMAwbic.EMA_list.append(Helpers.EMA(ldb.price_list, EMAwbic.EMA_list,
                                          gc.EMAwbic.Period))
      EMAwbic.ind_list.append(
          ((ldb.price_list[-1] - EMAwbic.EMA_list[-1])
           / EMAwbic.EMA_list[-1]) * 100)

    if 'EMAwbic' in gc.VerboseIndicators:
      if len(EMAwbic.ind_list) < 1:
        print('EMAwbic: Not yet enough data to calculate')
      else:
        # ind_list is externally accessible, so return None
        print('EMAwbic:', EMAwbic.ind_list[-1], '%')


# Fractal Adaptive Moving Average
class FRAMA:
  Short_list = []
  Long_list = []
  Diff_list = []

  def indicator():
    # We can start FRAMAs once we have max period candles
    if len(ldb.price_list) >= (max(gc.FRAMA.LongPeriod, gc.FRAMA.ShortPeriod)):
      FRAMA.Short_list.append(Helpers.FRAMA(ldb.price_list, FRAMA.Short_list,
                                            gc.FRAMA.ShortPeriod))
      FRAMA.Long_list.append(Helpers.FRAMA(ldb.price_list, FRAMA.Long_list,
                                           gc.FRAMA.LongPeriod))
      FRAMA.Diff_list.append(
          Helpers.ListDiff(FRAMA.Short_list, FRAMA.Long_list))

    if 'FRAMA' in gc.VerboseIndicators:
      if len(FRAMA.Long_list) < 1:
        print('FRAMA: Not yet enough data to determine trend')
      else:
        gu.PrintIndicatorTrend('FRAMA', FRAMA.Short_list, FRAMA.Long_list,
                               FRAMA.Diff_list, gc.FRAMA.DiffDown, gc.FRAMA.DiffUp)


# Movement Average Convergence Divergence
class MACD:
  Short_list = []
  Long_list = []
  Signal_list = []
  Histogram_list = []
  ind_list = []

  def indicator():
    # We can start MACD EMAs once we have max period candles
    if len(ldb.price_list) >= max(gc.MACD.LongPeriod, gc.MACD.ShortPeriod):
      MACD.Short_list.append(Helpers.EMA(ldb.price_list, MACD.Short_list,
                                         gc.MACD.ShortPeriod))
      MACD.Long_list.append(Helpers.EMA(ldb.price_list, MACD.Long_list,
                                        gc.MACD.LongPeriod))
      MACD.ind_list.append(MACD.Short_list[-1] - MACD.Long_list[-1])

      # We need SignalPeriod MACDs before generating MACDSignal
      if len(MACD.Long_list) >= gc.MACD.SignalPeriod:
        MACD.Signal_list.append(Helpers.EMA(MACD.ind_list, MACD.Signal_list,
                                            gc.MACD.SignalPeriod))
        MACD.Histogram_list.append(MACD.ind_list[-1] - MACD.Signal_list[-1])

      if 'MACD' in gc.VerboseIndicators:
        if len(MACD.Signal_list) < 1:
          print('MACD: Not yet enough data to determine trend')
        else:
          gu.PrintIndicatorTrend('MACD', MACD.ind_list, MACD.Signal_list,
                                 MACD.ind_list, gc.MACD.DiffDown,
                                 gc.MACD.DiffUp)
          print('MACD Hist:', MACD.Histogram_list[-1])


# Double Movement Average Convergence Divergence
class DMACD:
  Short_list = []
  Long_list = []
  Signal_list = []
  Histogram_list = []
  ind_list = []

  def indicator():
    # We can start DEMAs once we have max period candles
    if len(MACD.Long_list) >= max(gc.MACD.LongPeriod, gc.MACD.ShortPeriod):
      DMACD.Short_list.append(Helpers.DEMA(MACD.Short_list, DMACD.Short_list,
                                           gc.MACD.ShortPeriod))
      DMACD.Long_list.append(Helpers.DEMA(MACD.Long_list, DMACD.Long_list,
                                          gc.MACD.LongPeriod))
      DMACD.ind_list.append(DMACD.Short_list[-1] - DMACD.Long_list[-1])

      # We need MACDSignal DMACDs before generating Signal
      if len(DMACD.Long_list) >= (gc.MACD.SignalPeriod +
                                  (abs(gc.MACD.SignalPeriod - gc.MACD.LongPeriod))):
        DMACD.Signal_list.append(Helpers.DEMA(MACD.Signal_list,
                                              DMACD.Signal_list, gc.MACD.SignalPeriod))
        DMACD.Histogram_list.append(
            DMACD.ind_list[-1] - DMACD.Signal_list[-1])

      if 'DMACD' in gc.VerboseIndicators:
        if len(DMACD.Signal_list) < 1:
          print('DMACD: Not yet enough data to determine trend')
        else:
          gu.PrintIndicatorTrend('DMACD', DMACD.ind_list, DMACD.Signal_list,
                                 DMACD.ind_list, gc.DMACD.DiffDown,
                                 gc.DMACD.DiffUp)


# Fast Stochastic %K
class FastStochK:
  ind_list = []

  def indicator():
    # We can start FastStochK calculations once we have FastStochKPeriod
    # candles, otherwise we append None until met
    if len(ldb.price_list) >= gc.FastStochK.Period:
      FastStochK.ind_list.append(Helpers.FastStochK(ldb.price_list,
                                                    gc.FastStochK.Period))

    if 'FastStochK' in gc.VerboseIndicators:
      if len(FastStochK.ind_list) < 1:
        print('FastStochK: Not yet enough data to calculate')
      else:
        # ind_list is externally accessible, so return None
        print('FastStochK:', FastStochK.ind_list[-1])


# Fast Stochastic %D
class FastStochD:
  ind_list = []

  def indicator():
    # We can start FastStochD calculations once we have FastStochDPeriod
    # candles, otherwise we append None until met
    if len(FastStochD.ind_list) >= gc.FastStochD.Period:
      FastStochD.ind_list.append(Helpers.SMA(FastStochK.ind_list,
                                             gc.FastStochD.Period))

    if 'FastStochD' in gc.VerboseIndicators:
      if len(FastStochD.ind_list) < 1:
        print('FastStochD: Not yet enough data to calculate')
      else:
        # ind_list is externally accessible, so return None
        print('FastStochD:', FastStochD.ind_list[-1])


# Full Stochastic %D
class FullStochD:
  ind_list = []

  def indicator():
    # We can start FullStochD calculations once we have FullStochDPeriod
    # candles, otherwise we append None until met
    if len(FastStochD.ind_list) >= gc.FullStochD.Period:
      FullStochD.ind_list.append(Helpers.SMA(FastStochD.ind_list,
                                             gc.FullStochD.Period))

    if 'FullStochD' in gc.VerboseIndicators:
      if len(FullStochD.ind_list) < 1:
        print('FullStochD: Not yet enough data to calculate')
      else:
        # ind_list is externally accessible, so return None
        print('FullStochD:', FullStochD.ind_list[-1])


# Fast Stochastic RSI %K
class FastStochRSIK:
  ind_list = []

  def indicator():
    # We can start FastStochRSIK calculations once we have
    # FastStochRSIKPeriod candles, otherwise we append None until met
    if len(RSI.ind_list) >= gc.FastStochRSIK.Period:
      FastStochRSIK.ind_list.append(Helpers.FastStochK(RSI.ind_list,
                                                       gc.FastStochRSIK.Period))

    if 'FastStochRSIK' in gc.VerboseIndicators:
      if len(FastStochRSIK.ind_list) < 1:
        print('FastStochRSIK: Not yet enough data to calculate')
      else:
        # ind_list is externally accessible, so return None
        print('FastStochRSIK:', FastStochRSIK.ind_list[-1])


# Fast Stochastic RSI %D
class FastStochRSID:
  ind_list = []

  def indicator():
    # We can start FastStochRSID calculations once we have
    # FastStochRSIDPeriod candles, otherwise we append None until met
    if len(FastStochRSIK.ind_list) >= gc.FastStochRSID.Period:
      FastStochRSID.ind_list.append(Helpers.SMA(FastStochRSIK.ind_list,
                                                gc.FastStochRSID.Period))

    if 'FastStochRSID' in gc.VerboseIndicators:
      if len(FastStochRSID.ind_list) < 1:
        print('FastStochRSID: Not yet enough data to calculate')
      else:
        # ind_list is externally accessible, so return None
        print('FastStochRSID:', FastStochRSID.ind_list[-1])


# Fast Stochastic RSI %D
class FullStochRSID:
  ind_list = []

  def indicator():
    # We can start FullStochRSID calculations once we have
    # FullStochRSIDPeriod candles, otherwise we append None until met
    if len(FastStochRSID.ind_list) >= gc.FullStochRSID.Period:
      FullStochRSID.ind_list.append(Helpers.SMA(FastStochRSID.ind_list,
                                                gc.FastStochRSID.Period))

    if 'FullStochRSID' in gc.VerboseIndicators:
      if len(FullStochRSID.ind_list) < 1:
        print('FullStochRSID: Not yet enough data to calculate')
      else:
        # ind_list is externally accessible, so return None
        print('FullStochRSID:', FullStochRSID.ind_list[-1])


# KDJ
class KDJ:
  FastK_list = []
  FullK_list = []
  FullD_list = []
  J_list = []

  def indicator():
    if len(ldb.price_list) >= gc.KDJ.FastKPeriod:
      KDJ.FastK_list.append(Helpers.FastStochK(ldb.price_list,
                                               gc.KDJ.FastKPeriod))
    if len(KDJ.FastK_list) >= gc.KDJ.FullKPeriod:
      KDJ.FullK_list.append(Helpers.SMA(KDJ.FastK_list,
                                        gc.KDJ.FullKPeriod))
    if len(KDJ.FullK_list) >= gc.KDJ.FullDPeriod:
      KDJ.FullD_list.append(Helpers.SMA(KDJ.FullK_list,
                                        gc.KDJ.FullDPeriod))
    if len(KDJ.FullD_list) >= 1:
      KDJ.J_list.append(
          (3 * KDJ.FullD_list[-1]) - (2 * KDJ.FullK_list[-1]))

    if 'KDJ' in gc.VerboseIndicators:
      if len(KDJ.J_list) < 1:
        print(
            'KDJ: Not yet enough data to determine trend or calculate')
      else:
        gu.PrintIndicatorTrend('KDJ', KDJ.FullK_list, KDJ.FullD_list,
                               KDJ.J_list, gc.KDJ.Bid, gc.KDJ.Ask, False)


# Aroon Oscillator
class Aroon:
  Up_list = []
  Down_list = []
  ind_list = []

  def indicator():
    # We must have AroonPeriod ldb.price_list candles
    if len(ldb.price_list) >= gc.Aroon.Period:
      Aroon.Up_list.append(100 * (gc.Aroon.Period -
                                  (gc.Aroon.Period - ([i for i, x in enumerate(ldb.price_list)
                                                       if x == max(ldb.price_list[(gc.Aroon.Period * -1):])][0] + 1
                                                      )) / gc.Aroon.Period))
      Aroon.Down_list.append(100 * (gc.Aroon.Period -
                                    (gc.Aroon.Period - ([i for i, x in enumerate(ldb.price_list)
                                                         if x == min(ldb.price_list[(gc.Aroon.Period * -1):])][0] + 1
                                                        )) / gc.Aroon.Period))
      Aroon.ind_list.append(Aroon.Up_list[-1] - Aroon.Down_list[-1])

    if 'Aroon' in gc.VerboseIndicators:
      if len(Aroon.ind_list) < 1:
        print(
            'Aroon: Not yet enough data to determine trend or calculate')
      else:
        gu.PrintIndicatorTrend('Aroon', Aroon.Up_list, Aroon.Down_list,
                               Aroon.ind_list, gc.Aroon.Bid, gc.Aroon.Ask, False)


# Ichimoku Cloud
class Ichimoku:
  TenkanSen_list = []
  KijunSen_list = []
  SenkouSpanART_list = []
  SenkouSpanBRT_list = []
  SenkouSpanA_list = []
  SenkouSpanB_list = []
  CloudHistory_list = []
  # Signal lists
  Strong_list = []
  Optimized_list = []
  Weak_list = []
  CloudOnly_list = []

  def indicator():
    # We must have SenkouSpanPeriod price candles before starting
    # calculations, otherwise we append None
    # NOTE: Chikou Span's cool and all, but we don't care. We want to trade in
    # real time, and price list 26 periods behind only confirms if we *were*
    # right or wrong
    if len(ldb.price_list) >= gc.Ichimoku.SenkouSpanPeriod:
      Ichimoku.TenkanSen_list.append(Helpers.Ichimoku(ldb.price_list,
                                                      gc.Ichimoku.TenkanSenPeriod))
      Ichimoku.KijunSen_list.append(Helpers.Ichimoku(ldb.price_list,
                                                     gc.Ichimoku.KijunSenPeriod))
      Ichimoku.SenkouSpanART_list.append((Ichimoku.TenkanSen_list[-1]
                                          + Ichimoku.KijunSen_list[-1]) / 2)
      Ichimoku.SenkouSpanBRT_list.append(Helpers.Ichimoku(ldb.price_list,
                                                          gc.Ichimoku.SenkouSpanPeriod))
    # We need SenkouSpan to be ChikouSpanPeriod in the future
    if len(Ichimoku.SenkouSpanBRT_list) >= gc.Ichimoku.ChikouSpanPeriod:
      Ichimoku.SenkouSpanA_list.append(
          Ichimoku.SenkouSpanART_list[-gc.Ichimoku.ChikouSpanPeriod])
      Ichimoku.SenkouSpanB_list.append(
          Ichimoku.SenkouSpanBRT_list[-gc.Ichimoku.ChikouSpanPeriod])
    # Don't want to implement a new trade strategy, so just treat
    # Ichimoku lists as threshold strategies for IndicatorList.
    if len(Ichimoku.SenkouSpanB_list) >= 1:
      CloudMin = min(
          Ichimoku.SenkouSpanA_list[-1], Ichimoku.SenkouSpanB_list[-1])
      CloudMax = max(
          Ichimoku.SenkouSpanA_list[-1], Ichimoku.SenkouSpanB_list[-1])

      CP = ldb.price_list[-1]
      KS = Ichimoku.KijunSen_list[-1]
      TS = Ichimoku.TenkanSen_list[-1]
      CH = Ichimoku.CloudHistory_list

      # Strong Signals
      if CP > CloudMin and CP < KS and CP > TS:
        # BUY!
        Ichimoku.Strong_list.append(-1)
        StrongTrend = 'Bullish'
      elif CP < CloudMax and CP > KS and CP < TS:
        # SELL!
        Ichimoku.Strong_list.append(1)
        StrongTrend = 'Bearish'
      else:
        Ichimoku.Strong_list.append(0)
        StrongTrend = 'No trend'
      # Optimized Signals
      if CP > CloudMin and TS > KS:
        # BUY!
        Ichimoku.Optimized_list.append(-1)
        OptimizedTrend = 'Bullish'
      elif CP < CloudMax and KS > TS:
        # SELL!
        Ichimoku.Optimized_list.append(1)
        OptimizedTrend = 'Bearish'
      else:
        Ichimoku.Optimized_list.append(0)
        OptimizedTrend = 'No trend'
      # Weak Signals
      if TS > KS:
        # BUY!
        Ichimoku.Weak_list.append(-1)
        WeakTrend = 'Bullish'
      elif KS > TS:
        # SELL!
        Ichimoku.Weak_list.append(1)
        WeakTrend = 'Bearish'
      else:
        Ichimoku.Weak_list.append(0)
        WeakTrend = 'No trend'

      # Store price cloud history
      if CP < CloudMin:
        # Below
        CH.append(-1)
      elif CP > CloudMin and CP < CloudMax:
        # Inside
        CH.append(0)
      elif CP > CloudMax:
        # Above
        CH.append(1)

      # CloudOnly signals
      if len(CH) > 1:
        if CH[-2] == -1 and CH[-1] == 0:
          # Buy
          Ichimoku.CloudOnly_list.append(-1)
          CloudOnlyTrend = 'Bullish'
        elif CH[-2] == 0 and CH[-1] == 1:
          # Buy
          Ichimoku.CloudOnly_list.append(-1)
          CloudOnlyTrend = 'Bullish'
        elif CH[-2] == 1 and CH[-1] == 0:
          # Sell
          Ichimoku.CloudOnly_list.append(1)
          CloudOnlyTrend = 'Bearish'
        elif CH[-2] == 0 and CH[-1] == -1:
          # Sell
          Ichimoku.CloudOnly_list.append(1)
          CloudOnlyTrend = 'Bearish'
        else:
          # No signal
          # Support persistence
          if len(Ichimoku.CloudOnly_list) > 1:
            Ichimoku.CloudOnly_list.append(Ichimoku.CloudOnly_list[-2])
          else:
            Ichimoku.CloudOnly_list.append(0)
          CloudOnlyTrend = 'No new signal'
      else:
        # Generate initial CloudOnly signal
        if CH[-1] == -1:
          # Sell
          Ichimoku.CloudOnly_list.append(1)
          CloudOnlyTrend = 'Bearish'
        elif CH[-1] == 1:
          # Buy
          Ichimoku.CloudOnly_list.append(-1)
          CloudOnlyTrend = 'Bullish'
        else:
          Ichimoku.CloudOnly_list.append(0)
          CloudOnlyTrend = 'Need more cloud history'

      if gc.Ichimoku.IndicatorStrategy == 'Strong':
        trend = StrongTrend
      elif gc.Ichimoku.IndicatorStrategy == 'Weak':
        trend = WeakTrend
      elif gc.Ichimoku.IndicatorStrategy == 'Optimized':
        trend = OptimizedTrend
      elif gc.Ichimoku.IndicatorStrategy == 'CloudOnly':
        trend = CloudOnlyTrend
      if 'Ichimoku' in gc.VerboseIndicators:
        print('Ichimoku:', trend)
    else:
      if 'Ichimoku' in gc.VerboseIndicators:
        print(
            'Ichimoku: Not yet enough data to determine trend or calculate')


# Volatility/Movement Strength Indicators/Indexes

# Sample Standard Deviation
class StdDev:
  ind_list = []

  def indicator():
    # We can start StdDev calculations once we have StdDevSample
    # candles, otherwise we append None until met
    if len(ldb.price_list) >= gc.StdDev.Period:
      StdDev.ind_list.append(Helpers.StdDev(ldb.price_list,
                                            gc.StdDev.Period))
    if 'StdDev' in gc.VerboseIndicators:
      if StdDev.ind_list:
        print('StdDev:', StdDev.ind_list[-1])
      else:
        print('StdDev: Not yet enough data to calculate')


# Bollinger Bands
class BollBands:
  Middle_list = []
  Upper_list = []
  Lower_list = []

  def indicator():
    # We can start BollBand calculations once we have BollBandPeriod
    # candles, otherwise we append None until met
    if len(ldb.price_list) >= gc.BollBands.Period:
      BollBands.Middle_list.append(Helpers.SMA(ldb.price_list,
                                               gc.BollBands.Period))
      BollBands.Upper_list.append(BollBands.Middle_list[-1] +
                                  (Helpers.StdDev(ldb.price_list, gc.BollBands.Period) * 2))
      BollBands.Lower_list.append(BollBands.Middle_list[-1] -
                                  (Helpers.StdDev(ldb.price_list, gc.BollBands.Period) * 2))


# Bollinger Bandwidth
class BollBandwidth:
  ind_list = []

  def indicator():
    # We can start BollBandwidth calculations once we have BollBands
    if len(BollBands.Lower_list) >= 1:
      BollBandwidth.ind_list.append((BollBands.Upper_list[-1]
                                     - BollBands.Lower_list[-1]) / BollBands.Middle_list[-1])
    if 'BollBandwidth' in gc.VerboseIndicators:
      if BollBandwidth.ind_list:
        print('BollBandwidth:', BollBandwidth.ind_list[-1])
      else:
        print('BollBandwidth: Not yet enough data to calculate')


# Average True Range
class ATR:
  ind_list = []
  TR_list = []

  def indicator():
    # We can start ATR calculations once we have two periods
    if len(ldb.price_list) >= (gc.ATR.Period * 2):
      ATR.TR_list.append(Helpers.TrueRange(ldb.price_list, gc.ATR.Period))
      if len(ATR.TR_list) >= gc.ATR.Period:
        ATR.ind_list.append(
            Helpers.WMA(ATR.TR_list, ATR.ind_list, gc.ATR.Period))

    if 'ATR' in gc.VerboseIndicators:
      if ATR.ind_list:
        print('ATR:', ATR.ind_list[-1])
      else:
        print('ATR: Not yet enough data to calculate')


# Directional Movement
class DMI:
  ind_list = []
  DMISignal_list = []
  PosDI_list = []
  NegDI_list = []
  PosDM_list = []
  NegDM_list = []
  PosDMWMA_list = []
  NegDMWMA_list = []
  DX_list = []
  DMITrend = 'No Trend'

  def indicator():
    # We can start DMI calculations once we have two ATR periods
    if len(ldb.price_list) >= (gc.ATR.Period * 2):
      UpMove = max(ldb.price_list[-gc.ATR.Period:]) - max(
          ldb.price_list[(len(ldb.price_list) - (gc.ATR.Period * 2)):-gc.ATR.Period])
      DownMove = min(ldb.price_list[-gc.ATR.Period:]) - min(
          ldb.price_list[(len(ldb.price_list) - (gc.ATR.Period * 2)):-gc.ATR.Period])
      if UpMove < 0 and DownMove < 0:
        DMI.PosDM_list.append(0)
        DMI.NegDM_list.append(0)
      elif UpMove > DownMove:
        DMI.PosDM_list.append(UpMove)
        DMI.NegDM_list.append(0)
      elif UpMove < DownMove:
        DMI.PosDM_list.append(0)
        DMI.NegDM_list.append(DownMove)

      if len(DMI.PosDM_list) >= gc.ATR.Period and len(ATR.TR_list) >= gc.ATR.Period:
        DMI.PosDMWMA_list.append(
            Helpers.WMA(DMI.PosDM_list, DMI.PosDMWMA_list, gc.ATR.Period))
        DMI.NegDMWMA_list.append(
            Helpers.WMA(DMI.NegDM_list, DMI.NegDMWMA_list, gc.ATR.Period))
        DMI.PosDI_list.append(DMI.PosDMWMA_list[-1] / ATR.ind_list[-1])
        DMI.NegDI_list.append(DMI.NegDMWMA_list[-1] / ATR.ind_list[-1])

        DIDiff = abs(DMI.PosDI_list[-1] - DMI.NegDI_list[-1])
        DMI.DX_list.append(DIDiff / (DMI.PosDI_list[-1] + DMI.NegDI_list[-1]))
        # ADX
        if len(DMI.DX_list) >= (gc.ATR.Period * 2):
          DMI.ind_list.append(
              Helpers.WMA(DMI.DX_list, DMI.ind_list, gc.ATR.Period))

        # Hack for trading with both DI crossovers and ADX threshold.
        if DMI.ind_list:
          if DMI.ind_list[-1] > gc.DMI.Threshold:
            if DMI.PosDI_list[-1] > DMI.NegDI_list[-1]:
              # Buy
              DMI.DMISignal_list.append(-1)
              DMI.DMITrend = 'Uptrend'
            elif DMI.PosDI_list[-1] < DMI.NegDI_list[-1]:
              # Sell
              DMI.DMISignal_list.append(1)
              DMI.DMITrend = 'Downtrend'
            else:
              DMI.DMISignal_list.append(0)
              DMI.DMITrend = 'No trend'
          else:
            DMI.DMISignal_list.append(0)
            DMI.DMITrend = 'No trend'

    if 'DMI' in gc.VerboseIndicators:
      if DMI.ind_list:
        if gc.DMI.IndicatorStrategy == 'Full':
          print('DMI:', DMI.DMITrend)
        else:
          print('ADX:', DMI.ind_list[-1])
      else:
        print('DMI: Not yet enough data to calculate')


# (Simple) Rate of Change (Momentum)
class SROC:
  ind_list = []
  SROC_list = []

  def indicator():
    # We can start ROC calculations once we have SROC Periods of Price
    s = SROC.SROC_list
    if len(ldb.price_list) >= gc.SROC.Period:
      s.append(ldb.price_list[-1] - ldb.price_list[
          -gc.SROC.Period])

    # Treat as a diff strat so we don't need to add strategy support
    if len(s) >= 2:
      if s[-1] > 0 and s[-2] <= 0:
        # BUY!
        SROC.ind_list.append(-1)
        trend = 'an Uptrend'
      elif s[-1] < 0 and s[-2] >= 0:
        # SELL!
        SROC.ind_list.append(1)
        trend = 'a Downtrend'
      else:
        # No signal
        SROC.ind_list.append(0)
        trend = 'No trend'
      if 'SROC' in gc.VerboseIndicators:
        print('SROC: We are in ', trend)
