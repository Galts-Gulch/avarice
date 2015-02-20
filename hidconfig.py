import genconfig as gc

# This file is not to be edited like genconfig is
#
# BidAskList is used to determine if Bid and Ask are lists.
# BidAskReverse is used to determine if Bid and Ask trades
# should be reversed (useful for diff trend trading)


class EMA:
  if gc.EMA.IndicatorStrategy == 'CD':
    BidAskList = True
    IndicatorList = 'EMA_Long_list'
    IndicatorBid = 'EMA_Short_list'
    IndicatorAsk = 'EMA_Short_list'
  elif gc.EMA.IndicatorStrategy == 'Diff':
    TradeReverse = True
    IndicatorList = 'EMA_Diff_list'
    IndicatorBid = gc.EMA.DiffUp
    IndicatorAsk = gc.EMA.DiffDown
  Graphl_list = [
      'EMA_Short_list', 'EMA_Long_list']
  Graphn_list = ['Short', 'Long']


class DEMA:
  if gc.DEMA.IndicatorStrategy == 'CD':
    BidAskList = True
    IndicatorList = 'DEMA_Long_list'
    IndicatorBid = 'DEMA_Short_list'
    IndicatorAsk = 'DEMA_Short_list'
  elif gc.DEMA.IndicatorStrategy == 'Diff':
    TradeReverse = True
    IndicatorList = 'DEMA_Diff_list'
    IndicatorBid = gc.DEMA.DiffUp
    IndicatorAsk = gc.DEMA.DiffDown
  Graphl_list = [
      'DEMA_Short_list', 'DEMA_Long_list']
  Graphn_list = ['Short', 'Long']


class EMAwbic:
  IndicatorList = 'EMAwbic_ind_list'
  IndicatorBid = gc.EMAwbic.Bid
  IndicatorAsk = gc.EMAwbic.Ask
  Graphl_list = ['EMAwbic_ind_list']
  Graphn_list = ['Price : EMA percent delta']


class FRAMA:
  if gc.FRAMA.IndicatorStrategy == 'CD':
    BidAskList = True
    IndicatorList = 'FRAMA_Long_list'
    IndicatorBid = 'FRAMA_Short_list'
    IndicatorAsk = 'FRAMA_Short_list'
  elif gc.FRAMA.IndicatorStrategy == 'Diff':
    TradeReverse = True
    IndicatorList = 'FRAMA_Diff_list'
    IndicatorBid = gc.FRAMA.DiffUp
    IndicatorAsk = gc.FRAMA.DiffDown
  Graphl_list = [
      'FRAMA_Short_list', 'FRAMA_Long_list']
  Graphn_list = ['Short', 'Long']


class MACD:
  if gc.MACD.IndicatorStrategy == 'CD':
    BidAskList = True
    TradeReverse = True
    IndicatorList = 'MACD_ind_list'
    IndicatorBid = 'MACD_Signal_list'
    IndicatorAsk = 'MACD_Signal_list'
  elif gc.MACD.IndicatorStrategy == 'Diff':
    TradeReverse = True
    IndicatorList = 'MACD_ind_list'
    IndicatorBid = gc.MACD.DiffUp
    IndicatorAsk = gc.MACD.DiffDown
  Graphl_list = [
      'MACD_Signal_list', 'MACD_ind_list']
  Graphn_list = ['Signal', 'MACD']


class DMACD:
  if gc.DMACD.IndicatorStrategy == 'CD':
    BidAskList = True
    TradeReverse = True
    IndicatorList = 'DMACD_ind_list'
    IndicatorBid = 'DMACD_Signal_list'
    IndicatorAsk = 'DMACD_Signal_list'
  elif gc.DMACD.IndicatorStrategy == 'Diff':
    TradeReverse = True
    IndicatorList = 'DMACD_ind_list'
    IndicatorBid = gc.DMACD.DiffUp
    IndicatorAsk = gc.DMACD.DiffDown
  Graphl_list = [
      'DMACD_Signal_list', 'DMACD_ind_list']
  Graphn_list = ['Signal', 'DMACD']


class SMA:
  if gc.SMA.IndicatorStrategy == 'CD':
    BidAskList = True
    IndicatorList = 'SMA_Long_list'
    IndicatorBid = 'SMA_Short_list'
    IndicatorAsk = 'SMA_Short_list'
  elif gc.SMA.IndicatorStrategy == 'Diff':
    TradeReverse = True
    IndicatorList = 'SMA_Diff_list'
    IndicatorBid = gc.SMA.DiffUp
    IndicatorAsk = gc.SMA.DiffDown
  Graphl_list = [
      'SMA_Short_list', 'SMA_Long_list']
  Graphn_list = ['Short', 'Long']


class KDJ:
  if gc.KDJ.IndicatorStrategy == 'CD':
    BidAskList = True
    TradeReverse = True
    IndicatorList = 'KDJ_FullK_list'
    IndicatorBid = 'KDJ_FullD_list'
    IndicatorAsk = 'KDJ_FullD_list'
  elif gc.KDJ.IndicatorStrategy == 'Diff':
    IndicatorList = 'KDJ_J_list'
    IndicatorAsk = gc.KDJ.Ask
    IndicatorBid = gc.KDJ.Bid
  Graphl_list = ['KDJ_FullK_list',
                 'KDJ_FullD_list', 'KDJ_J_list']
  Graphn_list = ['K', 'D', 'J']


class Aroon:
  IndicatorList = 'Aroon_ind_list'
  if gc.Aroon.IndicatorStrategy == 'CD':
    TradeReverse = True
    IndicatorBid = 0
    IndicatorAsk = 0
  elif gc.Aroon.IndicatorStrategy == 'Diff':
    IndicatorBid = gc.Aroon.Bid
    IndicatorAsk = gc.Aroon.Ask
  Graphl_list = ['Aroon_ind_list']
  Graphn_list = ['Aroon']


class Ichimoku:
  if gc.Ichimoku.IndicatorStrategy == 'Strong':
    IndicatorList = 'Ichimoku_Strong_list'
  elif gc.Ichimoku.IndicatorStrategy == 'Optimized':
    IndicatorList = 'Ichimoku_Optimized_list'
  elif gc.Ichimoku.IndicatorStrategy == 'Weak':
    IndicatorList = 'Ichimoku_Weak_list'
  elif gc.Ichimoku.IndicatorStrategy == 'CloudOnly':
    IndicatorList = 'Ichimoku_CloudOnly_list'
  IndicatorBid = 0
  IndicatorAsk = 0
  Graphl_list = ['Ichimoku_KijunSen_list', 'Ichimoku_TenkanSenSen_list',
                 'Ichimoku_SenkouSpanA_list', 'Ichimoku_SenkouSpanB_list']
  Graphn_list = ['KijunSen', 'TenkanSen', 'SenkouSpanA', 'SenkouSpanB']


class RSI:
  IndicatorList = 'RSI_ind_list'
  IndicatorAsk = gc.RSI.Ask
  IndicatorBid = gc.RSI.Bid
  Graphl_list = ['RSI_ind_list']
  Graphn_list = ['RSI']


class FastStochRSIK:
  IndicatorList = 'FastStochRSIK_ind_list'
  IndicatorAsk = gc.FastStochRSIK.Ask
  IndicatorBid = gc.FastStochRSIK.Bid
  Graphl_list = ['FastStochRSIK_ind_list']
  Graphn_list = ['FastStochRSIK']


class FastStochRSID:
  IndicatorList = 'FastStochRSID_ind_list'
  IndicatorAsk = gc.FastStochRSID.Ask
  IndicatorBid = gc.FastStochRSID.Bid
  Graphl_list = ['FastStochRSID_ind_list']
  Graphn_list = ['FastStochRSID']


class FullStochRSID:
  Graphl_list = ['FullStochRSID_ind_list']
  Graphn_list = ['FullStochRSID']
  if gc.FullStochRSID.IndicatorStrategy == 'Diff':
    IndicatorList = 'FullStochRSID_ind_list'
    IndicatorAsk = gc.FullStochRSID.Ask
    IndicatorBid = gc.FullStochRSID.Bid
  elif gc.FullStochRSID.IndicatorStrategy == 'CD':
    BidAskList = True
    IndicatorList = 'FullStochRSID_ind_list'
    IndicatorBid = 'FastStochRSID_ind_list'
    IndicatorAsk = 'FastStochRSID_ind_list'
    Graphl_list.append('FastStochRSID_ind_list')
    Graphn_list.append('FastStochRSID')


class FastStochK:
  IndicatorList = 'FastStochK_ind_list'
  IndicatorAsk = gc.FastStochK.Ask
  IndicatorBid = gc.FastStochK.Bid
  Graphl_list = ['FastStochK_ind_list']
  Graphn_list = ['FastStochK']


class FastStochD:
  IndicatorList = 'FastStochD_ind_list'
  IndicatorAsk = gc.FastStochD.Ask
  IndicatorBid = gc.FastStochD.Bid
  Graphl_list = ['FastStochD_ind_list']
  Graphn_list = ['FastStochD']


class FullStochD:
  IndicatorList = 'FullStochD_ind_list'
  IndicatorAsk = gc.FullStochD.Ask
  IndicatorBid = gc.FullStochD.Bid
  Graphl_list = ['FullStochD_ind_list']
  Graphn_list = ['FullStochD']


class SROC:
  IndicatorList = 'SROC_ind_list'
  IndicatorBid = 0
  IndicatorAsk = 0
  Graphl_list = ['SROC_ind_list']
  Graphn_list = ['Simple Rate of Change']


class StdDev:
  VolatilityIndicator = True
  IndicatorList = 'StdDev_ind_list'
  Threshold = gc.StdDev.Threshold
  Graphl_list = ['StdDev.ind_list']
  Graphn_list = ['Standard Deviation']


class BollBandwidth:
  VolatilityIndicator = True
  IndicatorList = 'BollBandwidth_ind_list'
  Threshold = gc.BollBandwidth.Threshold
  Graphl_list = ['BollBandwidth_ind_list']
  Graphn_list = ['Bollinger Bandwidth']


class ATR:
  VolatilityIndicator = True
  IndicatorList = 'ATR_ind_list'
  Threshold = gc.ATR.Threshold
  Graphl_list = ['ATR.ind_list']
  Graphn_list = ['Average True Range']


class ChandExit:
  IndicatorList = 'ChandExit_signal_list'
  IndicatorBid = 0
  IndicatorAsk = 0
  Graphl_list = [
      'ChandExit_Long_list', 'ChandExit_Short_list']
  Graphn_list = ['Chandelier Exit Long', 'Chandelier Exit Short']


class DMI:
  if gc.DMI.IndicatorStrategy == 'Full':
    IndicatorList = 'DMI_DMISignal_list'
    IndicatorBid = 0
    IndicatorAsk = 0
    Graphl_list = [
        'DMI_PosDI_list', 'DMI_NegDI_list']
    Graphn_list = ['+DI', '-DI']
  else:
    VolatilityIndicator = True
    IndicatorList = 'DMI_ind_list'
    Threshold = gc.DMI.Threshold
    Graphl_list = ['DMI_ind_list']
    Graphn_list = ['ADX']
