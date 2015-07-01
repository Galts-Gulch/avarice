from storage import config

# This file is not to be edited
#
# BidAskList is used to determine if Bid and Ask are lists.
# BidAskReverse is used to determine if Bid and Ask trades
# should be reversed (useful for diff trend trading)

# TODO: add more expanded aliases and further make config.ini more readable.
IndicatorAlias_dict = {'Fast Stochastic RSI %K': 'FastStochRSIK',
                       'Fast Stochastic RSI %D': 'FastStochRSID',
                       'Full Stochastic RSI %D': 'FullStochRSID',
                       'Fast Stochastic %K': 'FastStochK',
                       'Fast Stochastic %D': 'FastStochD',
                       'Full Stochastic %D': 'FullStochD',
                       'Standard Deviation': 'StdDev',
                       'Bollinger Bands': 'BollBands',
                       'Bollinger Bandwidth': 'BollBandwidth',
                       'Average True Range': 'ATR',
                       'Chandelier Exit': 'ChandExit',
                       'Directional Movement Index': 'DMI',
                       'Simple Rate of Change': 'SROC',
                       'Exponential Movement Average': 'EMA',
                       'Simple Movement Average': 'SMA',
                       'Fractal Adaptive Movement Average': 'FRAMA'}

IndicatorAlias2_dict = dict(
    zip(IndicatorAlias_dict.values(), IndicatorAlias_dict.keys()))


class EMA:
  if config.gc['Indicators']['EMA']['Indicator Strategy'] == 'CD':
    BidAskList = True
    IndicatorList = 'EMA_Long_list'
    IndicatorBid = 'EMA_Short_list'
    IndicatorAsk = 'EMA_Short_list'
  elif config.gc['Indicators']['EMA']['Indicator Strategy'] == 'Diff':
    TradeReverse = True
    IndicatorList = 'EMA_Diff_list'
    IndicatorBid = config.gc['Indicators']['EMA']['Diff Up']
    IndicatorAsk = config.gc['Indicators']['EMA']['Diff Down']
  Graphl_list = [
      'EMA_Short_list', 'EMA_Long_list']
  Graphn_list = ['Short', 'Long']


class DEMA:
  if config.gc['Indicators']['DEMA']['Indicator Strategy'] == 'CD':
    BidAskList = True
    IndicatorList = 'DEMA_Long_list'
    IndicatorBid = 'DEMA_Short_list'
    IndicatorAsk = 'DEMA_Short_list'
  elif config.gc['Indicators']['DEMA']['Indicator Strategy'] == 'Diff':
    TradeReverse = True
    IndicatorList = 'DEMA_Diff_list'
    IndicatorBid = config.gc['Indicators']['DEMA']['Diff Up']
    IndicatorAsk = config.gc['Indicators']['DEMA']['Diff Down']
  Graphl_list = [
      'DEMA_Short_list', 'DEMA_Long_list']
  Graphn_list = ['Short', 'Long']


class EMAwbic:
  IndicatorList = 'EMAwbic_ind_list'
  IndicatorBid = config.gc['Indicators']['EMAwbic']['Bid']
  IndicatorAsk = config.gc['Indicators']['EMAwbic']['Ask']
  Graphl_list = ['EMAwbic_ind_list']
  Graphn_list = ['Price : EMA percent delta']


class FRAMA:
  if config.gc['Indicators']['FRAMA']['Indicator Strategy'] == 'CD':
    BidAskList = True
    IndicatorList = 'FRAMA_Long_list'
    IndicatorBid = 'FRAMA_Short_list'
    IndicatorAsk = 'FRAMA_Short_list'
  elif config.gc['Indicators']['FRAMA']['Indicator Strategy'] == 'Diff':
    TradeReverse = True
    IndicatorList = 'FRAMA_Diff_list'
    IndicatorBid = config.gc['Indicators']['FRAMA']['Diff Up']
    IndicatorAsk = config.gc['Indicators']['FRAMA']['Diff Down']
  Graphl_list = [
      'FRAMA_Short_list', 'FRAMA_Long_list']
  Graphn_list = ['Short', 'Long']


class MACD:
  if config.gc['Indicators']['MACD']['Indicator Strategy'] == 'CD':
    BidAskList = True
    TradeReverse = True
    IndicatorList = 'MACD_ind_list'
    IndicatorBid = 'MACD_Signal_list'
    IndicatorAsk = 'MACD_Signal_list'
  elif config.gc['Indicators']['MACD']['Indicator Strategy'] == 'Diff':
    TradeReverse = True
    IndicatorList = 'MACD_ind_list'
    IndicatorBid = config.gc['Indicators']['MACD']['Diff Up']
    IndicatorAsk = config.gc['Indicators']['MACD']['Diff Down']
  Graphl_list = [
      'MACD_Signal_list', 'MACD_ind_list']
  Graphn_list = ['Signal', 'MACD']


class DMACD:
  if config.gc['Indicators']['DMACD']['Indicator Strategy'] == 'CD':
    BidAskList = True
    TradeReverse = True
    IndicatorList = 'DMACD_ind_list'
    IndicatorBid = 'DMACD_Signal_list'
    IndicatorAsk = 'DMACD_Signal_list'
  elif config.gc['Indicators']['DMACD']['Indicator Strategy'] == 'Diff':
    TradeReverse = True
    IndicatorList = 'DMACD_ind_list'
    IndicatorBid = config.gc['Indicators']['DMACD']['Diff Up']
    IndicatorAsk = config.gc['Indicators']['DMACD']['Diff Down']
  Graphl_list = [
      'DMACD_Signal_list', 'DMACD_ind_list']
  Graphn_list = ['Signal', 'DMACD']


class SMA:
  if config.gc['Indicators']['SMA']['Indicator Strategy'] == 'CD':
    BidAskList = True
    IndicatorList = 'SMA_Long_list'
    IndicatorBid = 'SMA_Short_list'
    IndicatorAsk = 'SMA_Short_list'
  elif config.gc['Indicators']['SMA']['Indicator Strategy'] == 'Diff':
    TradeReverse = True
    IndicatorList = 'SMA_Diff_list'
    IndicatorBid = config.gc['Indicators']['SMA']['Diff Up']
    IndicatorAsk = config.gc['Indicators']['SMA']['Diff Down']
  Graphl_list = [
      'SMA_Short_list', 'SMA_Long_list']
  Graphn_list = ['Short', 'Long']


class KDJ:
  if config.gc['Indicators']['KDJ']['Indicator Strategy'] == 'CD':
    BidAskList = True
    TradeReverse = True
    IndicatorList = 'KDJ_FullK_list'
    IndicatorBid = 'KDJ_FullD_list'
    IndicatorAsk = 'KDJ_FullD_list'
  elif config.gc['Indicators']['KDJ']['Indicator Strategy'] == 'Diff':
    IndicatorList = 'KDJ_J_list'
    IndicatorAsk = config.gc['Indicators']['KDJ']['Ask']
    IndicatorBid = config.gc['Indicators']['KDJ']['Bid']
  Graphl_list = ['KDJ_FullK_list',
                 'KDJ_FullD_list', 'KDJ_J_list']
  Graphn_list = ['K', 'D', 'J']


class Aroon:
  IndicatorList = 'Aroon_ind_list'
  if config.gc['Indicators']['Aroon']['Indicator Strategy'] == 'CD':
    TradeReverse = True
    IndicatorBid = 0
    IndicatorAsk = 0
  elif config.gc['Indicators']['Aroon']['Indicator Strategy'] == 'Diff':
    IndicatorBid = config.gc['Indicators']['Aroon']['Bid']
    IndicatorAsk = config.gc['Indicators']['Aroon']['Ask']
  Graphl_list = ['Aroon_ind_list']
  Graphn_list = ['Aroon']


class Ichimoku:
  if config.gc['Indicators']['Ichimoku']['Indicator Strategy'] == 'Strong':
    IndicatorList = 'Ichimoku_Strong_list'
  elif config.gc['Indicators']['Ichimoku']['Indicator Strategy'] == 'Optimized':
    IndicatorList = 'Ichimoku_Optimized_list'
  elif config.gc['Indicators']['Ichimoku']['Indicator Strategy'] == 'Weak':
    IndicatorList = 'Ichimoku_Weak_list'
  elif config.gc['Indicators']['Ichimoku']['Indicator Strategy'] == 'CloudOnly':
    IndicatorList = 'Ichimoku_CloudOnly_list'
  IndicatorBid = 0
  IndicatorAsk = 0
  Graphl_list = ['Ichimoku_KijunSen_list', 'Ichimoku_TenkanSenSen_list',
                 'Ichimoku_SenkouSpanA_list', 'Ichimoku_SenkouSpanB_list']
  Graphn_list = ['KijunSen', 'TenkanSen', 'SenkouSpanA', 'SenkouSpanB']


class RSI:
  IndicatorList = 'RSI_ind_list'
  IndicatorAsk = config.gc['Indicators']['RSI']['Ask']
  IndicatorBid = config.gc['Indicators']['RSI']['Bid']
  Graphl_list = ['RSI_ind_list']
  Graphn_list = ['RSI']


class FastStochRSIK:
  IndicatorList = 'FastStochRSIK_ind_list'
  IndicatorAsk = config.gc['Indicators']['Fast Stochastic RSI %K']['Ask']
  IndicatorBid = config.gc['Indicators']['Fast Stochastic RSI %K']['Bid']
  Graphl_list = ['FastStochRSIK_ind_list']
  Graphn_list = ['FastStochRSIK']


class FastStochRSID:
  IndicatorList = 'FastStochRSID_ind_list'
  IndicatorAsk = config.gc['Indicators']['Fast Stochastic RSI %D']['Ask']
  IndicatorBid = config.gc['Indicators']['Fast Stochastic RSI %D']['Bid']
  Graphl_list = ['FastStochRSID_ind_list']
  Graphn_list = ['FastStochRSID']


class FullStochRSID:
  Graphl_list = ['FullStochRSID_ind_list']
  Graphn_list = ['FullStochRSID']
  if config.gc['Indicators']['Full Stochastic RSI %D']['Indicator Strategy'] == 'Diff':
    IndicatorList = 'FullStochRSID_ind_list'
    IndicatorAsk = config.gc['Indicators']['Full Stochastic RSI %D']['Ask']
    IndicatorBid = config.gc['Indicators']['Full Stochastic RSI %D']['Bid']
  elif config.gc['Indicators']['Full Stochastic RSI %D']['Indicator Strategy'] == 'CD':
    BidAskList = True
    IndicatorList = 'FullStochRSID_ind_list'
    IndicatorBid = 'FastStochRSID_ind_list'
    IndicatorAsk = 'FastStochRSID_ind_list'
    Graphl_list.append('FastStochRSID_ind_list')
    Graphn_list.append('FastStochRSID')


class FastStochK:
  IndicatorList = 'FastStochK_ind_list'
  IndicatorAsk = config.gc['Indicators']['Fast Stochastic %K']['Ask']
  IndicatorBid = config.gc['Indicators']['Fast Stochastic %K']['Bid']
  Graphl_list = ['FastStochK_ind_list']
  Graphn_list = ['FastStochK']


class FastStochD:
  IndicatorList = 'FastStochD_ind_list'
  IndicatorAsk = config.gc['Indicators']['Fast Stochastic %D']['Ask']
  IndicatorBid = config.gc['Indicators']['Fast Stochastic %D']['Bid']
  Graphl_list = ['FastStochD_ind_list']
  Graphn_list = ['FastStochD']


class FullStochD:
  IndicatorList = 'FullStochD_ind_list'
  IndicatorAsk = config.gc['Indicators']['Full Stochastic %D']['Ask']
  IndicatorBid = config.gc['Indicators']['Full Stochastic %D']['Bid']
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
  Threshold = config.gc['Indicators']['Standard Deviation']['Threshold']
  Graphl_list = ['StdDev.ind_list']
  Graphn_list = ['Standard Deviation']


class BollBandwidth:
  VolatilityIndicator = True
  IndicatorList = 'BollBandwidth_ind_list'
  Threshold = config.gc['Indicators']['Bollinger Bandwidth']['Threshold']
  Graphl_list = ['BollBandwidth_ind_list']
  Graphn_list = ['Bollinger Bandwidth']


class ATR:
  VolatilityIndicator = True
  IndicatorList = 'ATR_ind_list'
  Threshold = config.gc['Indicators']['Average True Range']['Threshold']
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
  if config.gc['Indicators']['Directional Movement Index']['Indicator Strategy'] == 'DI':
    IndicatorList = 'DMI_DMISignal_list'
    IndicatorBid = 0
    IndicatorAsk = 0
    Graphl_list = [
        'DMI_PosDI_list', 'DMI_NegDI_list']
    Graphn_list = ['+DI', '-DI']
  elif config.gc['Indicators']['Directional Movement Index']['Indicator Strategy'] == 'Full':
    IndicatorList = 'DMI_FullDMISignal_list'
    IndicatorBid = 0
    IndicatorAsk = 0
    Graphl_list = [
        'DMI_PosDI_list', 'DMI_NegDI_list']
    Graphn_list = ['+DI', '-DI']
  else:
    VolatilityIndicator = True
    IndicatorList = 'DMI_ind_list'
    Threshold = config.gc['Indicators'][
        'Directional Movement Index']['Threshold']
    Graphl_list = ['DMI_ind_list']
    Graphn_list = ['ADX']
