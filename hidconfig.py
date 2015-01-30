import genconfig as gc
import indicators as ind
from storage import indicators as storage


# This file is not to be edited like gc is

# Due to external calling and varying indicator types,
# we can't use concat or getattr here.
# BidAskList is used to determine if Bid and Ask are lists.
# BidAskReverse is used to determine if Bid and Ask trades
# should be reversed (useful for diff trend trading)


class EMA:
  if gc.EMA.IndicatorStrategy == 'CD':
    BidAskList = True
    IndicatorList = storage.getlist('EMA_Long_list')
    IndicatorBid = storage.getlist('EMA_Short_list')
    IndicatorAsk = storage.getlist('EMA_Short_list')
  elif gc.EMA.IndicatorStrategy == 'Diff':
    TradeReverse = True
    IndicatorList = storage.getlist('EMA_Diff_list')
    IndicatorBid = gc.EMA.DiffUp
    IndicatorAsk = gc.EMA.DiffDown
  Graphl_list = [
      storage.getlist('EMA_Short_list'), storage.getlist('EMA_Long_list')]
  Graphn_list = ['Short', 'Long']


class DEMA:
  if gc.DEMA.IndicatorStrategy == 'CD':
    BidAskList = True
    IndicatorList = storage.getlist('DEMA_Long_list')
    IndicatorBid = storage.getlist('DEMA_Short_list')
    IndicatorAsk = storage.getlist('DEMA_Short_list')
  elif gc.DEMA.IndicatorStrategy == 'Diff':
    TradeReverse = True
    IndicatorList = storage.getlist('DEMA_Diff_list')
    IndicatorBid = gc.DEMA.DiffUp
    IndicatorAsk = gc.DEMA.DiffDown
  Graphl_list = [
      storage.getlist('DEMA_Short_list'), storage.getlist('DEMA_Long_list')]
  Graphn_list = ['Short', 'Long']


class EMAwbic:
  IndicatorList = storage.getlist('EMAwbic_ind_list')
  IndicatorBid = gc.EMAwbic.Bid
  IndicatorAsk = gc.EMAwbic.Ask
  Graphl_list = [storage.getlist('EMAwbic_ind_list')]
  Graphn_list = ['Price : EMA percent delta']


class FRAMA:
  if gc.FRAMA.IndicatorStrategy == 'CD':
    BidAskList = True
    IndicatorList = storage.getlist('FRAMA_Long_list')
    IndicatorBid = storage.getlist('FRAMA_Short_list')
    IndicatorAsk = storage.getlist('FRAMA_Short_list')
  elif gc.FRAMA.IndicatorStrategy == 'Diff':
    TradeReverse = True
    IndicatorList = storage.getlist('FRAMA_Diff_list')
    IndicatorBid = gc.FRAMA.DiffUp
    IndicatorAsk = gc.FRAMA.DiffDown
  Graphl_list = [
      storage.getlist('FRAMA_Short_list'), storage.getlist('FRAMA_Long_list')]
  Graphn_list = ['Short', 'Long']


class MACD:
  if gc.MACD.IndicatorStrategy == 'CD':
    BidAskList = True
    TradeReverse = True
    IndicatorList = storage.getlist('MACD_ind_list')
    IndicatorBid = storage.getlist('MACD_Signal_list')
    IndicatorAsk = storage.getlist('MACD_Signal_list')
  elif gc.MACD.IndicatorStrategy == 'Diff':
    TradeReverse = True
    IndicatorList = storage.getlist('MACD_ind_list')
    IndicatorBid = gc.MACD.DiffUp
    IndicatorAsk = gc.MACD.DiffDown
  Graphl_list = [
      storage.getlist('MACD_Signal_list'), storage.getlist('MACD_ind_list')]
  Graphn_list = ['Signal', 'MACD']


class DMACD:
  if gc.DMACD.IndicatorStrategy == 'CD':
    BidAskList = True
    TradeReverse = True
    IndicatorList = storage.getlist('DMACD_ind_list')
    IndicatorBid = storage.getlist('DMACD_Signal_list')
    IndicatorAsk = storage.getlist('DMACD_Signal_list')
  elif gc.DMACD.IndicatorStrategy == 'Diff':
    TradeReverse = True
    IndicatorList = storage.getlist('MACD_ind_list')
    IndicatorBid = gc.DMACD.DiffUp
    IndicatorAsk = gc.DMACD.DiffDown
  Graphl_list = [
      storage.getlist('DMACD_Signal_list'), storage.getlist('DMACD_ind_list')]
  Graphn_list = ['Signal', 'DMACD']


class SMA:
  if gc.SMA.IndicatorStrategy == 'CD':
    BidAskList = True
    IndicatorList = storage.getlist('SMA_Long_list')
    IndicatorBid = storage.getlist('SMA_Short_list')
    IndicatorAsk = storage.getlist('SMA_Short_list')
  elif gc.SMA.IndicatorStrategy == 'Diff':
    TradeReverse = True
    IndicatorList = storage.getlist('SMA_Diff_list')
    IndicatorBid = gc.SMA.DiffUp
    IndicatorAsk = gc.SMA.DiffDown
  Graphl_list = [
      storage.getlist('SMA_Short_list'), storage.getlist('SMA_Long_list')]
  Graphn_list = ['Short', 'Long']


class KDJ:
  if gc.KDJ.IndicatorStrategy == 'CD':
    BidAskList = True
    TradeReverse = True
    IndicatorList = storage.getlist('KDJ_FullK_list')
    IndicatorBid = storage.getlist('KDJ_FullD_list')
    IndicatorAsk = storage.getlist('KDJ_FullD_list')
  elif gc.KDJ.IndicatorStrategy == 'Diff':
    IndicatorList = storage.getlist('KDJ_J_list')
    IndicatorAsk = gc.KDJ.Ask
    IndicatorBid = gc.KDJ.Bid
  Graphl_list = [storage.getlist('KDJ_FullK_list'), storage.getlist(
      'KDJ_FullD_list'), storage.getlist('KDJ_J_list')]
  Graphn_list = ['K', 'D', 'J']


class Aroon:
  IndicatorList = storage.getlist('Aroon_ind_list')
  if gc.Aroon.IndicatorStrategy == 'CD':
    TradeReverse = True
    IndicatorBid = 0
    IndicatorAsk = 0
  elif gc.Aroon.IndicatorStrategy == 'Diff':
    IndicatorBid = gc.Aroon.Bid
    IndicatorAsk = gc.Aroon.Ask
  Graphl_list = [storage.getlist('Aroon_ind_list')]
  Graphn_list = ['Aroon']


class Ichimoku:
  if gc.Ichimoku.IndicatorStrategy == 'Strong':
    IndicatorList = storage.getlist('Ichimoku_Strong_list')
  elif gc.Ichimoku.IndicatorStrategy == 'Weak':
    IndicatorList = ind.Ichimoku.Weak_list
  IndicatorBid = 0
  IndicatorAsk = 0
  Graphl_list = [storage.getlist('Ichimoku_KijunSen_list'), storage.getlist('Ichimoku_TenkanSenSen_list'), storage.getlist(
      'Ichimoku_SenkouSpanA_list'), storage.getlist('Ichimoku_SenkouSpanB_list')]
  Graphn_list = ['KijunSen', 'TenkanSen', 'SenkouSpanA', 'SenkouSpanB']


class RSI:
  IndicatorList = storage.getlist('RSI_ind_list')
  IndicatorAsk = gc.RSI.Ask
  IndicatorBid = gc.RSI.Bid
  Graphl_list = [storage.getlist('RSI_ind_list')]
  Graphn_list = ['RSI']


class FastStochRSIK:
  IndicatorList = storage.getlist('FastStochRSIK_ind_list')
  IndicatorAsk = gc.FastStochRSIK.Ask
  IndicatorBid = gc.FastStochRSIK.Bid
  Graphl_list = [storage.getlist('FastStochRSIK_ind_list')]
  Graphn_list = ['FastStochRSIK']


class FastStochRSID:
  IndicatorList = storage.getlist('FastStochRSID_ind_list')
  IndicatorAsk = gc.FastStochRSID.Ask
  IndicatorBid = gc.FastStochRSID.Bid
  Graphl_list = [storage.getlist('FastStochRSID_ind_list')]
  Graphn_list = ['FastStochRSID']


class FullStochRSID:
  Graphl_list = [storage.getlist('FullStochRSID_ind_list')]
  Graphn_list = ['FullStochRSID']
  if gc.FullStochRSID.IndicatorStrategy == 'Diff':
    IndicatorList = storage.getlist('FullStochRSID_ind_list')
    IndicatorAsk = gc.FullStochRSID.Ask
    IndicatorBid = gc.FullStochRSID.Bid
  elif gc.FullStochRSID.IndicatorStrategy == 'CD':
    BidAskList = True
    IndicatorList = storage.getlist('FullStochRSID_ind_list')
    IndicatorBid = storage.getlist('FastStochRSID_ind_list')
    IndicatorAsk = storage.getlist('FastStochRSID_ind_list')
    Graphl_list.append(storage.getlist('FastStochRSID_ind_list'))
    Graphn_list.append('FastStochRSID')


class FastStochK:
  IndicatorList = storage.getlist('FastStochK_ind_list')
  IndicatorAsk = gc.FastStochK.Ask
  IndicatorBid = gc.FastStochK.Bid
  Graphl_list = [storage.getlist('FastStochK_ind_list')]
  Graphn_list = ['FastStochK']


class FastStochD:
  IndicatorList = storage.getlist('FastStochD_ind_list')
  IndicatorAsk = gc.FastStochD.Ask
  IndicatorBid = gc.FastStochD.Bid
  Graphl_list = [storage.getlist('FastStochD_ind_list')]
  Graphn_list = ['FastStochD']


class FullStochD:
  IndicatorList = storage.getlist('FullStochD_ind_list')
  IndicatorAsk = gc.FullStochD.Ask
  IndicatorBid = gc.FullStochD.Bid
  Graphl_list = [storage.getlist('FullStochD_ind_list')]
  Graphn_list = ['FullStochD']


class SROC:
  IndicatorList = storage.getlist('SROC_ind_list')
  IndicatorBid = 0
  IndicatorAsk = 0
  Graphl_list = [storage.getlist('SROC_ind_list')]
  Graphn_list = ['SROC']
