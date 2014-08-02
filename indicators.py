import math

import genconfig
import genutils as gu
import loggerdb as ldb

## Indicators

# Misc Indicator Helpers
class Helpers:
    def SMA(list1, period):
        if len(list1) >= period:
            SMA = math.fsum(list1[(period * -1):]) / period
            return SMA

    def EMA(list1, list2, period1):
        if len(list1) >= period1:
            Multi = 2 / (period1 + 1)
            if len(list2) > 1:
                EMA = ((list1[-1] - list2[-1]) * Multi) + list2[-1]
            # First run, must use SMA to get started
            elif len(list1) >= period1:
                EMA = ((list1[-1] - Helpers.SMA(list1, period1)) * Multi)\
                        + Helpers.SMA(list1, period1)
            return EMA

    def DEMA(list1, list2, period1):
        if len(list1) >= 1:
            DEMA = ((2 * list1[-1]) - Helpers.EMA(list1, list2, period1))
            return DEMA

    def FastStochK(list1, period):
        if len(list1) >= period:
            LowestPeriod = min(float(s) for s in list1[(period * -1):])
            HighestPeriod = max(float(s) for s in list1[(period * -1):])
            FastStochK = ((list1[-1] - LowestPeriod) / (HighestPeriod\
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
            if len(RSI.RS_gain_list) >= genconfig.RSI.Period:
                if len(RSI.avg_gain_list) > 1:
                    RSI.avg_gain_list.append(((RSI.avg_gain_list[-1] *\
                            (genconfig.RSI.Period - 1)) + RSI.RS_gain_list[-1])\
                            / genconfig.RSI.Period)
                    RSI.avg_loss_list.append(((RSI.avg_loss_list[-1] *\
                            (genconfig.RSI.Period - 1)) + RSI.RS_loss_list[-1])\
                            / genconfig.RSI.Period)
                # Fist run, can't yet apply smoothing
                else:
                    RSI.avg_gain_list.append(math.fsum(RSI.RS_gain_list[(\
                            genconfig.RSI.Period * -1):]) / genconfig.RSI.Period)
                    RSI.avg_loss_list.append(math.fsum(RSI.RS_loss_list[(\
                            genconfig.RSI.Period * -1):]) / genconfig.RSI.Period)

                # Calculate and append current RS to RS_list
                RSI.RS_list.append(RSI.avg_gain_list[-1] / RSI.avg_loss_list[-1])

                # Calculate and append current RSI to ind_list
                RSI.ind_list.append(100 - (100 / (1 + RSI.RS_list[-1])))

        if 'RSI' in genconfig.VerboseIndicators:
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
        # We can start SMA calculations once we have SMALongPeriod
        # price candles, otherwise we append None until met
        if len(ldb.price_list) >= genconfig.SMA.LongPeriod:
            SMA.Short_list.append(Helpers.SMA(ldb.price_list, genconfig.SMA.ShortPeriod))
            SMA.Long_list.append(Helpers.SMA(ldb.price_list, genconfig.SMA.LongPeriod))

        if len(SMA.Long_list) >= 1:
            SMA.Diff_list.append(Helpers.ListDiff(SMA.Short_list, SMA.Long_list[-1]))

        if 'SMA' in genconfig.VerboseIndicators:
            if len(SMA.Long_list) < 1:
                print('SMA: Not yet enough data to determine trend')
            else:
                gu.PrintIndicatorTrend('SMA', SMA.Short_list, SMA.Long_list,\
                        SMA.Diff_list, genconfig.SMA.DiffDown,genconfig.SMA.DiffUp)


# Exponential Movement Average
class EMA:
    Short_list = []
    Long_list = []
    Diff_list = []
    def indicator():
        # We can start EMAs once we have EMALong candles
        if len(ldb.price_list) >= genconfig.EMA.LongPeriod:
            EMA.Short_list.append(Helpers.EMA(ldb.price_list, EMA.Short_list,\
                    genconfig.EMA.ShortPeriod))
            EMA.Long_list.append(Helpers.EMA(ldb.price_list, EMA.Long_list,\
                    genconfig.EMA.LongPeriod))

        # We can calculate Diff when we have both EMALong and EMAShort
        if len(EMA.Long_list) >= 1:
            EMA.Diff_list.append(Helpers.ListDiff(EMA.Short_list, EMA.Long_list))

        if 'EMA' in genconfig.VerboseIndicators:
            if len(EMA.Long_list) < 1:
                print('EMA: Not yet enough data to determine trend')
            else:
                gu.PrintIndicatorTrend('EMA', EMA.Short_list, EMA.Long_list,\
                        EMA.Diff_list, genconfig.EMA.DiffDown,\
                        genconfig.EMA.DiffUp)

# Double Exponential Movement Average
class DEMA:
    Short_list = []
    Long_list = []
    Diff_list = []
    def indicator():
        # We can start DEMAs once we have an EMALong candles
        if len(EMA.Long_list) >= genconfig.EMA.LongPeriod:
            DEMA.Short_list.append(Helpers.DEMA(EMA.Short_list, DEMA.Short_list,\
                    genconfig.EMA.ShortPeriod))
            DEMA.Long_list.append(Helpers.DEMA(EMA.Long_list, DEMA.Long_list,\
                    genconfig.EMA.LongPeriod))

        # We can calculate Diff when we have both LongPeriod and ShortPeriod
        if len(DEMA.Long_list) >= 1:
            DEMA.Diff_list.append(Helpers.ListDiff(DEMA.Short_list, DEMA.Long_list))

            if 'DEMA' in genconfig.VerboseIndicators:
                if len(DEMA.Long_list) < 1:
                    print('DEMA: Not yet enough data to determine trend')
                else:
                    gu.PrintIndicatorTrend('DEMA', DEMA.Short_list, DEMA.Long_list,\
                            DEMA.Diff_list, genconfig.DEMA.DiffDown,\
                            genconfig.DEMA.DiffUp)

# Movement Average Convergence Divergence
class MACD:
    Short_list = []
    Long_list = []
    Signal_list = []
    Histogram_list = []
    ind_list = []
    def indicator():
        # We can start MACD EMAs once we have LongPeriod candles
        if len(ldb.price_list) >= genconfig.MACD.LongPeriod:
            MACD.Short_list.append(Helpers.EMA(ldb.price_list, MACD.Short_list,\
                    genconfig.MACD.ShortPeriod))
            MACD.Long_list.append(Helpers.EMA(ldb.price_list, MACD.Long_list,\
                    genconfig.MACD.LongPeriod))
            MACD.ind_list.append(MACD.Short_list[-1] - MACD.Long_list[-1])

            # We need SignalPeriod MACDs before generating MACDSignal
            if len(MACD.Long_list) >= genconfig.MACD.SignalPeriod:
                MACD.Signal_list.append(Helpers.EMA(MACD.ind_list, MACD.Signal_list,\
                        genconfig.MACD.SignalPeriod))

                # TODO: use this someday...
                MACD.Histogram_list.append(MACD.ind_list[-1] - MACD.Signal_list[-1])

            if 'MACD' in genconfig.VerboseIndicators:
                if len(MACD.Signal_list) < 1:
                    print('MACD: Not yet enough data to determine trend')
                else:
                    gu.PrintIndicatorTrend('MACD', MACD.Signal_list, MACD.ind_list,\
                            MACD.ind_list, genconfig.MACD.DiffDown,\
                            genconfig.MACD.DiffUp)

# Double Movement Average Convergence Divergence
class DMACD:
    Short_list = []
    Long_list = []
    Signal_list = []
    Histogram_list = []
    ind_list = []
    def indicator():
        # We can start DMACD EMAs once we have MACDLong candles
        if len(MACD.Long_list) >= genconfig.MACD.LongPeriod:
            DMACD.Short_list.append(Helpers.DEMA(MACD.Short_list, DMACD.Short_list,\
                    genconfig.MACD.ShortPeriod))
            DMACD.Long_list.append(Helpers.DEMA(MACD.Long_list, DMACD.Long_list,\
                    genconfig.MACD.LongPeriod))
            DMACD.ind_list.append(DMACD.Short_list[-1] - DMACD.Long_list[-1])

            # We need MACDSignal DMACDs before generating Signal
            if len(DMACD.Long_list) >= (genconfig.MACD.SignalPeriod +\
                    (abs(genconfig.MACD.SignalPeriod - genconfig.MACD.LongPeriod))):
                DMACD.Signal_list.append(Helpers.DEMA(MACD.Signal_list,\
                        DMACD.Signal_list, genconfig.MACD.SignalPeriod))
                DMACD.Histogram_list.append(DMACD.ind_list[-1] - DMACD.Signal_list[-1])

            if 'DMACD' in genconfig.VerboseIndicators:
                if len(DMACD.Signal_list) < 1:
                    print('DMACD: Not yet enough data to determine trend')
                else:
                    gu.PrintIndicatorTrend('DMACD', DMACD.Signal_list, DMACD.ind_list,\
                            DMACD.ind_list, genconfig.DMACD.DiffDown,\
                            genconfig.DMACD.DiffUp)

# Fast Stochastic %K
class FastStochK:
    ind_list = []
    def indicator():
        # We can start FastStochK calculations once we have FastStochKPeriod
        # candles, otherwise we append None until met
        if len(ldb.price_list) >= genconfig.FastStochK.Period:
            FastStochK.ind_list.append(Helpers.FastStochK(ldb.price_list,\
                    genconfig.FastStochK.Period))

        if 'FastStochK' in genconfig.VerboseIndicators:
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
        if len(FastStochD.ind_list) >= genconfig.FastStochD.Period:
            FastStochD.ind_list.append(Helpers.SMA(FastStochK.ind_list,\
                    genconfig.FastStochD.Period))

        if 'FastStochD' in genconfig.VerboseIndicators:
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
        if len(FastStochD.ind_list) >= genconfig.FullStochD.Period:
            FullStochD.ind_list.append(Helpers.SMA(FastStochD.ind_list,\
                    genconfig.FullStochD.Period))

        if 'FullStochD' in genconfig.VerboseIndicators:
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
        if len(RSI.ind_list) >= genconfig.FastStochRSIK.Period:
            FastStochRSIK.ind_list.append(Helpers.FastStochK(RSI.ind_list,\
                    genconfig.FastStochRSIK.Period))

        if 'FastStochRSIK' in genconfig.VerboseIndicators:
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
        if len(FastStochRSIK.ind_list) >= genconfig.FastStochRSID.Period:
            FastStochRSID.ind_list.append(Helpers.SMA(FastStochRSIK.ind_list,\
                    genconfig.FastStochRSID.Period))

        if 'FastStochRSID' in genconfig.VerboseIndicators:
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
        if len(FastStochRSID.ind_list) >= genconfig.FullStochRSID.Period:
            FullStochRSID.ind_list.append(Helpers.SMA(FastStochRSID.ind_list,\
                    genconfig.FastStochRSID.Period))

        if 'FullStochRSID' in genconfig.VerboseIndicators:
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
        if len(ldb.price_list) >= genconfig.KDJ.FastKPeriod:
            KDJ.FastK_list.append(Helpers.FastStochK(ldb.price_list,\
                    genconfig.KDJ.FastKPeriod))
        if len(KDJ.FastK_list) >= genconfig.KDJ.FullKPeriod:
            KDJ.FullK_list.append(Helpers.SMA(KDJ.FastK_list,\
                    genconfig.KDJ.FullKPeriod))
        if len(KDJ.FullK_list) >= genconfig.KDJ.FullDPeriod:
            KDJ.FullD_list.append(Helpers.SMA(KDJ.FullK_list,\
                    genconfig.KDJ.FullDPeriod))
        if len(KDJ.FullD_list) >= 1:
            KDJ.J_list.append((3 * KDJ.FullD_list[-1]) - (2 * KDJ.FullK_list[-1]))

        if 'KDJ' in genconfig.VerboseIndicators:
            if len(KDJ.J_list) < 1:
                print('KDJ: Not yet enough data to determine trend or calculate')
            else:
                gu.PrintIndicatorTrend('KDJ', KDJ.FullD_list, KDJ.FullK_list,\
                        KDJ.J_list, genconfig.KDJ.Bid, genconfig.KDJ.Ask, False)


# Aroon Oscillator
class Aroon:
    Up_list = []
    Down_list = []
    ind_list = []
    def indicator():
        # We must have AroonPeriod ldb.price_list candles
        if len(ldb.price_list) >= genconfig.Aroon.Period:
            Aroon.Up_list.append(100 * (genconfig.Aroon.Period -\
                    (genconfig.Aroon.Period - ([i for i,x in enumerate(ldb.price_list)\
                    if x == max(ldb.price_list[(genconfig.Aroon.Period * -1):])][0] + 1\
                    )) / genconfig.Aroon.Period))
            Aroon.Down_list.append(100 * (genconfig.Aroon.Period -\
                    (genconfig.Aroon.Period - ([i for i,x in enumerate(ldb.price_list)\
                    if x == min(ldb.price_list[(genconfig.Aroon.Period * -1):])][0] + 1\
                    )) / genconfig.Aroon.Period))
            Aroon.ind_list.append(Aroon.Up_list[-1] - Aroon.Down_list[-1])

        if 'Aroon' in genconfig.VerboseIndicators:
            if len(Aroon.ind_list) < 1:
                print('Aroon: Not yet enough data to determine trend or calculate')
            else:
                gu.PrintIndicatorTrend('Aroon', Aroon.Down_list, Aroon.Up_list,\
                        Aroon.ind_list, genconfig.Aroon.Bid, genconfig.Aroon.Ask, False)


# Ichimoku Cloud
class Ichimoku:
    TenkanSen_list = []
    KijunSen_list = []
    SenkouSpanART_list = []
    SenkouSpanBRT_list = []
    SenkouSpanA_list = []
    SenkouSpanB_list = []
    Strong_list = []
    Weak_list = []

    def indicator():
        # We must have SenkouSpanPeriod price candles before starting
        # calculations, otherwise we append None
        # NOTE: Chikou Span's cool and all, but we don't care. We want to trade in
        # real time, and price list 26 periods behind only confirms if we *were*
        # right or wrong
        if len(ldb.price_list) >= genconfig.Ichimoku.SenkouSpanPeriod:
            Ichimoku.TenkanSen_list.append(Helpers.Ichimoku(ldb.price_list,\
                    genconfig.Ichimoku.TenkanSenPeriod))
            Ichimoku.KijunSen_list.append(Helpers.Ichimoku(ldb.price_list,\
                    genconfig.Ichimoku.KijunSenPeriod))
            Ichimoku.SenkouSpanART_list.append((Ichimoku.TenkanSen_list[-1]\
                    + Ichimoku.KijunSen_list[-1]) / 2)
            Ichimoku.SenkouSpanBRT_list.append(Helpers.Ichimoku(ldb.price_list,\
                    genconfig.Ichimoku.SenkouSpanPeriod))
        # We need SenkouSpan to be ChikouSpanPeriod in the future
        if len(Ichimoku.SenkouSpanBRT_list) >= genconfig.Ichimoku.ChikouSpanPeriod:
            Ichimoku.SenkouSpanA_list.append(Ichimoku.SenkouSpanART_list[(\
                    genconfig.Ichimoku.ChikouSpanPeriod * -1)])
            Ichimoku.SenkouSpanB_list.append(Ichimoku.SenkouSpanBRT_list[(\
                    genconfig.Ichimoku.ChikouSpanPeriod * -1)])
        # Don't want to implement a new trade strategy, so just treat
        # Ichimoku lists as threshold strategies for IndicatorList.
        if len(Ichimoku.SenkouSpanB_list) >= 1:
            CloudMin = min([min(Ichimoku.TenkanSen_list), min(\
                    Ichimoku.KijunSen_list), min(Ichimoku.SenkouSpanA_list),\
                    min(Ichimoku.SenkouSpanB_list)])

            CP = ldb.price_list[-1]
            KS = Ichimoku.KijunSen_list[-1]
            TS = Ichimoku.TenkanSen_list[-1]

            # Strong Signals
            if CP > CloudMin and CP < KS and CP > TS:
                # BUY!
                Ichimoku.Strong_list.append(-1)
                StrongTrend = 'Bullish'
            elif CP < CloudMin and CP > KS and CP < TS:
                # SELL!
                Ichimoku.Strong_list.append(1)
                StrongTrend = 'Bearish'
            else:
                Ichimoku.Strong_list.append(0)
                StrongTrend = 'No trend'
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

            if genconfig.Ichimoku.IndicatorStrategy == 'Strong':
                trend = StrongTrend
            elif genconfig.Ichimoku.IndicatorStrategy == 'Weak':
                trend = WeakTrend
            if 'Ichimoku' in genconfig.VerboseIndicators:
                print('Ichimoku:', trend)
        else:
            if 'Ichimoku' in genconfig.VerboseIndicators:
                print('Ichimoku: Not yet enough data to determine trend or calculate')


## Volatility/Movement Strength Indicators/Indexes

# Sample Standard Deviation
class StdDev:
    ind_list = []
    def indicator():
        # We can start StdDev calculations once we have StdDevSample
        # candles, otherwise we append None until met
        if len(ldb.price_list) >= genconfig.StdDev.Period:
            StdDev.ind_list.append(Helpers.StdDev(ldb.price_list,\
                    genconfig.StdDev.Period))

# Bollinger Bands
class BollBands:
    Middle_list = []
    Upper_list = []
    Lower_list = []
    def indicator():
        # We can start BollBand calculations once we have BollBandPeriod
        # candles, otherwise we append None until met
        if len(ldb.price_list) >= genconfig.BollBands.Period:
            BollBands.Middle_list.append(Helpers.SMA(ldb.price_list,\
                    genconfig.BollBands.Period))
            BollBands.Upper_list.append(BollBands.Middle_list[-1] + \
                    (Helpers.StdDev(ldb.price_list, genconfig.BollBands.Period) * 2))
            BollBands.Lower_list.append(BollBands.Middle_list[-1] - \
                    (Helpers.StdDev(ldb.price_list, genconfig.BollBands.Period) * 2))

# Bollinger Bandwidth
class BollBandwidth:
    ind_list = []
    def indicator():
        # We can start BollBandwidth calculations once we have BollBands
        if len(BollBands.Lower_list) >= 1:
            BollBandwidth.ind_list.append((BollBands.Upper_list[-1]\
                    - BollBands.Lower_list[-1]) / BollBands.Middle_list[-1])

# (Simple) Rate of Change (Momentum)
class SROC:
    ind_list = []
    SROC_list = []
    def indicator():
        # We can start ROC calculations once we have SROC Periods of Price
        s = SROC.SROC_list
        if len(ldb.price_list) >= genconfig.SROC.Period:
            s.append(ldb.price_list[-1] - ldb.price_list[\
                    -genconfig.SROC.Period])

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
            if 'SROC' in genconfig.VerboseIndicators:
                print('SROC: We are in ', trend)
