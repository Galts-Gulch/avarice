import math

import genconfig
import indicators
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

# Relative Strength Index
class RSI:
    RS_list = []
    RSI_list = []
    RS_gain_list = []
    RS_loss_list = []
    avg_gain_list = []
    avg_loss_list = []
    def indicator():
        # We need a minimum of 2 candles to start RS calculations
        if len(ldb.price_list) >= 2:
            if ldb.price_list[-1] > ldb.price_list[-2]:
                gain = ldb.price_list[-1] - ldb.price_list[-2]
                RS_gain_list.append(gain)
                RS_loss_list.append(0)
            elif ldb.price_list[-1] < ldb.price_list[-2]:
                loss = ldb.price_list[-2] - ldb.price_list[-1]
                RS_loss_list.append(loss)
                RS_gain_list.append(0)

            # Do RS calculations if we have all requested periods
            if len(RS_gain_list) >= genconfig.RSIPeriod:
                if len(avg_gain_list) > 1:
                    avg_gain_list.append(((avg_gain_list[-1] *\
                            (genconfig.RSIPeriod - 1)) + RS_gain_list[-1])\
                            / genconfig.RSIPeriod)
                    avg_loss_list.append(((avg_loss_list[-1] *\
                            (genconfig.RSIPeriod - 1)) + RS_loss_list[-1])\
                            / genconfig.RSIPeriod)
                # Fist run, can't yet apply smoothing
                else:
                    avg_gain_list.append(math.fsum(RS_gain_list[(\
                            genconfig.RSIPeriod * -1):]) / genconfig.RSIPeriod)
                    avg_loss_list.append(math.fsum(RS_loss_list[(\
                            genconfig.RSIPeriod * -1):]) / genconfig.RSIPeriod)

                # Calculate and append current RS to RS_list
                RS_list.append(avg_gain_list[-1] / avg_loss_list[-1])

                # Calculate and append current RSI to RSI_list
                RSI_list.append(100 - (100 / (1 + RS_list[-1])))

        if genconfig.Indicator == 'RSI':
            if len(RSI_list) < 1:
                print('RSI: Not yet enough data to calculate')
            else:
                # RSI_list is externally accessible, so return None
                print('RSI:', RSI_list[-1])


# Simple Movement Average
class SMA:
    SMAShort_list = []
    SMALong_list = []
    SMADiff_list = []
    def indicator():
        # We can start SMA calculations once we have SMALongPeriod
        # price candles, otherwise we append None until met
        if len(ldb.price_list) >= genconfig.SMALongPeriod:
            SMAShort_list.append(Helpers.SMA(ldb.price_list, genconfig.SMAShortPeriod))
            SMALong_list.append(Helpers.SMA(ldb.price_list, genconfig.SMALongPeriod))

        if len(SMALong_list) >= 1:
            SMADiff_list.append(100 * (SMAShort_list[-1] - SMALong_list[-1])\
                    / ((SMAShort_list[-1] + SMALong_list[-1]) / 2))

        if genconfig.Indicator == 'SMA':
            if len(SMALong_list) < 1:
                print('SMA: Not yet enough data to determine trend')
            else:
                gu.PrintIndicatorTrend(SMAShort_list, SMALong_list, SMADiff_list,\
                        genconfig.SMADiffDown,genconfig.SMADiffUp)


# Exponential Movement Average
class EMA:
    EMAShort_list = []
    EMALong_list = []
    EMADiff_list = []
    def indicator():
        # We can start EMAs once we have EMALong candles
        if len(ldb.price_list) >= genconfig.EMALong:
            EMAShort_list.append(Helpers.EMA(ldb.price_list, EMAShort_list,\
                    genconfig.EMAShort))
            EMALong_list.append(Helpers.EMA(ldb.price_list, EMALong_list,\
                    genconfig.EMALong))

        # We can calculate EMADiff when we have both EMALong and EMAShort
        if len(EMALong_list) >= 1:
            EMADiff_list.append(100 * (EMAShort_list[-1] - EMALong_list[-1])\
                    / ((EMAShort_list[-1] + EMALong_list[-1]) / 2))

        if genconfig.Indicator == 'EMA':
            if len(EMALong_list) < 1:
                print('EMA: Not yet enough data to determine trend')
            else:
                gu.PrintIndicatorTrend(EMAShort_list, EMALong_list, EMADiff_list,\
                        genconfig.EMADiffDown,genconfig.EMADiffUp)

# Double Exponential Movement Average
class DEMA:
    DEMAShort_list = []
    DEMALong_list = []
    DEMADiff_list = []
    def indicator():
        # We can start DEMAs once we have an EMALong candles
        if len(EMALong_list) >= genconfig.EMALong:
            DEMAShort_list.append(Helpers.DEMA(EMAShort_list, DEMAShort_list,\
                    genconfig.EMAShort))
            DEMALong_list.append(Helpers.DEMA(EMALong_list, DEMALong_list,\
                    genconfig.EMALong))

        # We can calculate DEMADiff when we have both DEMALong and DEMAShort
        if len(DEMALong_list) >= 1:
            DEMADiff_list.append(100 * (DEMAShort_list[-1]\
                    - DEMALong_list[-1]) / ((DEMAShort_list[-1]\
                    + DEMALong_list[-1]) / 2))

            if genconfig.Indicator == 'DEMA':
                if len(DEMALong_list) < 1:
                    print('DEMA: Not yet enough data to determine trend')
                else:
                    gu.PrintIndicatorTrend(DEMAShort_list, DEMALong_list, DEMADiff_list,\
                            genconfig.DEMADiffDown, genconfig.DEMADiffUp)

# Movement Average Convergence Divergence
class MACD:
    MACDShort_list = []
    MACDLong_list = []
    MACDSignal_list = []
    MACDHistogram_list = []
    MACD_list = []
    def indicator():
        # We can start MACD EMAs once we have MACDLong candles
        if len(ldb.price_list) >= genconfig.MACDLong:
            MACDShort_list.append(Helpers.EMA(ldb.price_list, MACDShort_list,\
                    genconfig.MACDShort))
            MACDLong_list.append(Helpers.EMA(ldb.price_list, MACDLong_list,\
                    genconfig.MACDLong))
            MACD_list.append(MACDShort_list[-1] - MACDLong_list[-1])

            # We need MACDSignal MACDs before generating MACDSignal
            if len(MACDLong_list) >= genconfig.MACDSignal:
                MACDSignal_list.append(Helpers.EMA(MACD_list, MACDSignal_list,\
                        genconfig.MACDSignal))

                # TODO: use this someday...
                MACDHistogram_list.append(MACD_list[-1] - MACDSignal_list[-1])

            if genconfig.Indicator == 'MACD':
                if len(MACDSignal_list) < 1:
                    print('MACD: Not yet enough data to determine trend')
                else:
                    gu.PrintIndicatorTrend(MACDSignal_list, MACD_list, MACD_list,\
                            genconfig.MACDDiffDown, genconfig.MACDDiffUp)

# Double Movement Average Convergence Divergence
class DMACD:
    DMACDShort_list = []
    DMACDLong_list = []
    DMACDSignal_list = []
    DMACDHistogram_list = []
    DMACD_list = []
    def indicator():
        # We can start DMACD EMAs once we have MACDLong candles
        if len(MACDLong_list) >= genconfig.MACDLong:
            DMACDShort_list.append(Helpers.DEMA(MACDShort_list, DMACDShort_list,\
                    genconfig.MACDShort))
            DMACDLong_list.append(Helpers.DEMA(MACDLong_list, DMACDLong_list,\
                    genconfig.MACDLong))
            DMACD_list.append(DMACDShort_list[-1] - DMACDLong_list[-1])

            # We need MACDSignal DMACDs before generating DMACDSignal
            if len(DMACDLong_list) >= (genconfig.MACDSignal +\
                    (abs(genconfig.MACDSignal - genconfig.MACDLong))):
                DMACDSignal_list.append(Helpers.DEMA(MACDSignal_list,\
                        DMACDSignal_list, genconfig.MACDSignal))
                DMACDHistogram_list.append(DMACD_list[-1] - DMACDSignal_list[-1])

            if genconfig.Indicator == 'DMACD':
                if len(DMACDSignal_list) < 1:
                    print('DMACD: Not yet enough data to determine trend')
                else:
                    gu.PrintIndicatorTrend(DMACDSignal_list, DMACD_list, DMACD_list,\
                            genconfig.DMACDDiffDown, genconfig.DMACDDiffUp)


# Fast Stochastic %K
class FastStochK:
    FastStochK_list = []
    def indicator():
        # We can start FastStochK calculations once we have FastStochKPeriod
        # candles, otherwise we append None until met
        if len(ldb.price_list) >= genconfig.FastStochKPeriod:
            FastStochK_list.append(Helpers.FastStochK(ldb.price_list,\
                    genconfig.FastStochKPeriod))

        if genconfig.Indicator == 'FastStochK':
            if len(FastStochK_list) < 1:
                print('FastStochK: Not yet enough data to calculate')
            else:
                # FastStochK_list is externally accessible, so return None
                print('FastStochK:', FastStochK_list[-1])

# Fast Stochastic %D
class FastStochD:
    FastStochD_list = []
    def indicator():
        # We can start FastStochD calculations once we have FastStochDPeriod
        # candles, otherwise we append None until met
        if len(FastStochK_list) >= genconfig.FastStochDPeriod:
            FastStochD_list.append(Helpers.SMA(FastStochK_list,\
                    genconfig.FastStochDPeriod))

        if genconfig.Indicator == 'FastStochD':
            if len(FastStochD_list) < 1:
                print('FastStochD: Not yet enough data to calculate')
            else:
                # FastStochD_list is externally accessible, so return None
                print('FastStochD:', FastStochD_list[-1])

# Full Stochastic %D
class FullStochD:
    FullStochD_list = []
    def indicator():
        # We can start FullStochD calculations once we have FullStochDPeriod
        # candles, otherwise we append None until met
        if len(FastStochD_list) >= genconfig.FullStochDPeriod:
            FullStochD_list.append(Helpers.SMA(FastStochD_list,\
                    genconfig.FullStochDPeriod))

        if genconfig.Indicator == 'FullStochD':
            if len(FullStochD_list) < 1:
                print('FullStochD: Not yet enough data to calculate')
            else:
                # FullStochD_list is externally accessible, so return None
                print('FullStochD:', FullStochD_list[-1])

# Fast Stochastic RSI %K
class FastStochRSIK:
    FastStochRSIK_list = []
    def indicator():
        # We can start FastStochRSIK calculations once we have
        # FastStochRSIKPeriod candles, otherwise we append None until met
        if len(RSI_list) >= genconfig.FastStochRSIKPeriod:
            FastStochRSIK_list.append(Helpers.FastStochK(RSI_list,\
                    genconfig.FastStochRSIKPeriod))

        if genconfig.Indicator == 'FastStochRSIK':
            if len(FastStochRSIK_list) < 1:
                print('FastStochRSIK: Not yet enough data to calculate')
            else:
                # FastStochRSIK_list is externally accessible, so return None
                print('FastStochRSIK:', FastStochRSIK_list[-1])

# Fast Stochastic RSI %D
class FastStochRSID:
    FastStochRSID_list = []
    def indicator():
        # We can start FastStochRSID calculations once we have
        # FastStochRSIDPeriod candles, otherwise we append None until met
        if len(FastStochRSIK_list) >= genconfig.FastStochRSIDPeriod:
            FastStochRSID_list.append(Helpers.SMA(FastStochRSIK_list,\
                    genconfig.FastStochRSIDPeriod))

        if genconfig.Indicator == 'FastStochRSID':
            if len(FastStochRSID_list) < 1:
                print('FastStochRSID: Not yet enough data to calculate')
            else:
                # FastStochRSID_list is externally accessible, so return None
                print('FastStochRSID:', FastStochRSID_list[-1])


# Fast Stochastic RSI %D
class FullStochRSID:
    FullStochRSID_list = []
    def indicator():
        # We can start FullStochRSID calculations once we have
        # FullStochRSIDPeriod candles, otherwise we append None until met
        if len(FastStochRSID_list) >= genconfig.FullStochRSIDPeriod:
            FullStochRSID_list.append(Helpers.SMA(FastStochRSID_list,\
                    genconfig.FastStochRSIDPeriod))

        if genconfig.Indicator == 'FullStochRSID':
            if len(FullStochRSID_list) < 1:
                print('FullStochRSID: Not yet enough data to calculate')
            else:
                # FullStochRSID_list is externally accessible, so return None
                print('FullStochRSID:', FullStochRSID_list[-1])

# KDJ
class KDJ:
    KDJFastK_list = []
    KDJFullK_list = []
    KDJFullD_list = []
    KDJJ_list = []
    def indicator():
        if len(ldb.price_list) >= genconfig.KDJFastKPeriod:
            KDJFastK_list.append(Helpers.FastStochK(ldb.price_list,\
                    genconfig.KDJFastKPeriod))
        if len(KDJFastK_list) >= genconfig.KDJFullKPeriod:
            KDJFullK_list.append(Helpers.SMA(KDJFastK_list,\
                    genconfig.KDJFullKPeriod))
        if len(KDJFullK_list) >= genconfig.KDJFullDPeriod:
            KDJFullD_list.append(Helpers.SMA(KDJFullK_list,\
                    genconfig.KDJFullDPeriod))
        if len(KDJFullD_list) >= 1:
            KDJJ_list.append((3 * KDJFullD_list[-1]) - (2 * KDJFullK_list[-1]))

        if genconfig.Indicator == 'KDJ':
            if len(KDJJ_list) < 1:
                print('KDJ: Not yet enough data to determine trend or calculate')
            else:
                gu.PrintIndicatorTrend(KDJFullD_list, KDJFullK_list, KDJJ_list,\
                        genconfig.KDJJBid, genconfig.KDJJAsk, False)


# Aroon Oscillator
class Aroon:
    AroonUp_list = []
    AroonDown_list = []
    Aroon_list = []
    def indicator():
        # We must have AroonPeriod ldb.price_list candles
        if len(ldb.price_list) >= genconfig.AroonPeriod:
            AroonUp_list.append(100 * (genconfig.AroonPeriod -\
                    (genconfig.AroonPeriod - ([i for i,x in enumerate(ldb.price_list)\
                    if x == max(ldb.price_list[(genconfig.AroonPeriod * -1):])][0] + 1\
                    )) / genconfig.AroonPeriod))
            AroonDown_list.append(100 * (genconfig.AroonPeriod -\
                    (genconfig.AroonPeriod - ([i for i,x in enumerate(ldb.price_list)\
                    if x == min(ldb.price_list[(genconfig.AroonPeriod * -1):])][0] + 1\
                    )) / genconfig.AroonPeriod))
            Aroon_list.append(AroonUp_list[-1] - AroonDown_list[-1])

        if genconfig.Indicator == 'Aroon':
            if len(Aroon_list) < 1:
                print('Aroon: Not yet enough data to determine trend or calculate')
            else:
                gu.PrintIndicatorTrend(AroonDown_list, AroonUp_list, Aroon_list,\
                        genconfig.AroonBid, genconfig.AroonAsk, False)


# Ichimoku Cloud
class Ichimoku:
    TenkanSen_list = []
    KijunSen_list = []
    SenkouSpanART_list = []
    SenkouSpanBRT_list = []
    SenkouSpanA_list = []
    SenkouSpanB_list = []
    IchimokuStrong_list = []
    IchimokuWeak_list = []

    def indicator():
        # We must have SenkouSpanPeriod price candles before starting
        # calculations, otherwise we append None
        # NOTE: Chikou Span's cool and all, but we don't care. We want to trade in
        # real time, and price list 26 periods behind only confirms if we *were*
        # right or wrong
        if len(ldb.price_list) >= genconfig.SenkouSpanPeriod:
            TenkanSen_list.append(Helpers.Ichimoku(ldb.price_list,\
                    genconfig.TenkanSenPeriod))
            KijunSen_list.append(Helpers.Ichimoku(ldb.price_list,\
                    genconfig.KijunSenPeriod))
            SenkouSpanART_list.append((TenkanSen_list[-1] + KijunSen_list[-1]) / 2)
            SenkouSpanBRT_list.append(Helpers.Ichimoku(ldb.price_list,\
                    genconfig.SenkouSpanPeriod))
        # We need SenkouSpan to be ChikouSpanPeriod in the future
        if len(SenkouSpanBRT_list) >= genconfig.ChikouSpanPeriod:
            SenkouSpanA_list.append(SenkouSpanART_list[(\
                    genconfig.ChikouSpanPeriod * -1)])
            SenkouSpanB_list.append(SenkouSpanBRT_list[(\
                    genconfig.ChikouSpanPeriod * -1)])
        # Don't want to implement a new trade strategy, so just treat
        # Ichimoku lists as threshold strategies for IndicatorList.
        if len(SenkouSpanB_list) >= 1:
            CloudMin = min([min(TenkanSen_list), min(KijunSen_list), min(\
                    SenkouSpanA_list), min(SenkouSpanB_list)])
            CloudMax = max([max(TenkanSen_list), max(KijunSen_list), max(\
                    SenkouSpanA_list), max(SenkouSpanB_list)])

            CP = ldb.price_list[-1]
            KS = KijunSen_list[-1]
            TS = TenkanSen_list[-1]

            # Strong Signals
            if CP > CloudMin and CP < KS and CP > TS:
                # BUY!
                IchimokuStrong_list.append(-1)
                StrongTrend = 'Bullish'
            elif CP < CloudMin and CP > KS and CP < TS:
                # SELL!
                IchimokuStrong_list.append(1)
                StrongTrend = 'Bearish'
            else:
                IchimokuStrong_list.append(0)
                StrongTrend = 'No trend'
            # Weak Signals
            if TS > KS:
                # BUY!
                IchimokuWeak_list.append(-1)
                WeakTrend = 'Bullish'
            elif KS > TS:
                # SELL!
                IchimokuWeak_list.append(1)
                WeakTrend = 'Bearish'
            else:
                IchimokuWeak_list.append(0)
                WeakTrend = 'No trend'

            if genconfig.IchimokuStrategy == 'Strong':
                trend = StrongTrend
            elif genconfig.IchimokuStrategy == 'Weak':
                trend = WeakTrend
            if genconfig.Indicator == 'Ichimoku':
                print('Ichimoku:', trend)
        else:
            if genconfig.Indicator == 'Ichimoku':
                print('Ichimoku: Not yet enough data to determine trend or calculate')


## Volatility/Movement Strength Indicators/Indexes

# Sample Standard Deviation
class StdDev:
    StdDev_list = []
    def indicator():
        # We can start StdDev calculations once we have StdDevSample
        # candles, otherwise we append None until met
        if len(ldb.price_list) >= genconfig.StdDevSample:
            StdDev_list.append(Helpers.StdDev(ldb.price_list,\
                    genconfig.StdDevSample))

# Bollinger Bands
class BollBands:
    BollBandMiddle_list = []
    BollBandUpper_list = []
    BollBandLower_list = []
    def indicator():
        # We can start BollBand calculations once we have BollBandPeriod
        # candles, otherwise we append None until met
        if len(ldb.price_list) >= genconfig.BollBandPeriod:
            BollBandMiddle_list.append(Helpers.SMA(ldb.price_list,\
                    genconfig.BollBandPeriod))
            BollBandUpper_list.append(BollBandMiddle_list[-1] + (Helpers.StdDev(\
                    ldb.price_list, genconfig.BollBandPeriod) * 2))
            BollBandLower_list.append(BollBandMiddle_list[-1] - (Helpers.StdDev(\
                    ldb.price_list, genconfig.BollBandPeriod) * 2))

# Bollinger Bandwidth
class BollBandwidth:
    BollBandwidth_list = []
    def indicator():
        # We can start BollBandwidth calculations once we have BollBands
        if len(BollBandLower_list) >= 1:
            BollBandwidth_list.append((BollBandUpper_list[-1]\
                    - BollBandLower_list[-1]) / BollBandMiddle_list[-1])
