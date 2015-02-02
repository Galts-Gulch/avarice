import genconfig
import hidconfig

n = 'None'
b = 'Buy'
s = 'Sell'
Trade_dict = {'Order': 'None', 'TradeVolume': None}
LocalTrade_list = []
VolatilityTrade_list = []
IndependentTrade_dict = {}


def Default():
  # Clear prior to loop
  CombinedTrade_list = []
  for i in genconfig.Trader.TradeIndicators:
    # Combined
    if isinstance(i, list):
      for l in i:
        Trade_dict['TradeVolume'] = genconfig.Trader.TradeVolume
        hidind = getattr(hidconfig, l)
        if hasattr(hidind, 'VolatilityIndicator'):
          FilterList = hidind.IndicatorList
          LocalThreshold = hidind.Threshold
        elif hasattr(hidind, 'BidAskList'):
          if len(hidind.IndicatorBid) >= 1:
            LocalBid = hidind.IndicatorBid[-1]
            LocalAsk = hidind.IndicatorAsk[-1]
          FilterList = hidind.IndicatorBid
        else:
          LocalBid = hidind.IndicatorBid
          LocalAsk = hidind.IndicatorAsk
          FilterList = hidind.IndicatorList
        # Wait until we have enough data to trade off
        if len(FilterList) >= genconfig.Trader.TradeDelay:
          if hasattr(hidind, 'VolatilityIndicator'):
            if hidind.IndicatorList[-1] > LocalThreshold:
              VolatilityTrade_list.append(True)
            else:
              VolatilityTrade_list.append(False)
          elif hasattr(hidind, 'TradeReverse'):
            if hidind.IndicatorList[-1] > LocalBid:
              CombinedTrade_list.append(b)
            elif hidind.IndicatorList[-1] < LocalAsk:
              CombinedTrade_list.append(s)
            else:
              CombinedTrade_list.append(n)
          else:
            if hidind.IndicatorList[-1] < LocalBid:
              CombinedTrade_list.append(b)
            elif hidind.IndicatorList[-1] > LocalAsk:
              CombinedTrade_list.append(s)
            else:
              CombinedTrade_list.append(n)

      # Check if we have data for all Combined TradeIndicators, then check that
      # signals are the same.
      if VolatilityTrade_list:
        combined_num = len(i) - 1
      else:
        combined_num = len(i)
      if len(CombinedTrade_list) == combined_num:
        if all(x == CombinedTrade_list[0] for x in CombinedTrade_list):
          LocalTrade_list.append(CombinedTrade_list[0])
        else:
          LocalTrade_list.append(n)
      else:
        LocalTrade_list.append(n)
      if genconfig.Trader.SingleTrade and len(LocalTrade_list) > 1:
        if LocalTrade_list[-1] == LocalTrade_list[-2]:
          if genconfig.Trader.TradePersist:
            if len(LocalTrade_list) > 2 and not LocalTrade_list[-2] \
                    == LocalTrade_list[-3]:
              if VolatilityTrade_list:
                if VolatilityTrade_list[-1]:
                  Trade_dict['Order'] = LocalTrade_list[-1]
                else:
                  Trade_dict['Order'] = n
              else:
                Trade_dict['Order'] = LocalTrade_list[-1]
            else:
              Trade_dict['Order'] = n
          else:
            Trade_dict['Order'] = n
        else:
          if genconfig.Trader.TradePersist:
            Trade_dict['Order'] = n
          else:
            if VolatilityTrade_list:
              if VolatilityTrade_list[-1]:
                Trade_dict['Order'] = LocalTrade_list[-1]
              else:
                Trade_dict['Order'] = n
            else:
              Trade_dict['Order'] = LocalTrade_list[-1]
      else:
        if genconfig.Trader.TradePersist:
          if len(LocalTrade_list) > 2 and LocalTrade_list[-1] == \
                  LocalTrade_list[-2] and not LocalTrade_list[-2] == \
                  LocalTrade_list[-3]:
            if VolatilityTrade_list:
              if VolatilityTrade_list[-1]:
                Trade_dict['Order'] = LocalTrade_list[-1]
              else:
                Trade_dict['Order'] = n
            else:
              Trade_dict['Order'] = LocalTrade_list[-1]
          else:
            Trade_dict['Order'] = n
        else:
          if VolatilityTrade_list:
            if VolatilityTrade_list[-1]:
              Trade_dict['Order'] = LocalTrade_list[-1]
            else:
              Trade_dict['Order'] = n
          else:
            Trade_dict['Order'] = LocalTrade_list[-1]
    # Independent
    else:
      hidind = getattr(hidconfig, i)
      genind = getattr(genconfig, i).Trader
      Trade_dict['TradeVolume'] = genind.TradeVolume
      # Create new key/dict value for this indicator if key doesn't exist
      if i not in IndependentTrade_dict:
        IndependentTrade_dict[i] = {'Signals': []}
      it_signals = IndependentTrade_dict[i]['Signals']
      if hasattr(hidind, 'BidAskList'):
        if hidind.IndicatorBid:
          LocalBid = hidind.IndicatorBid[-1]
          LocalAsk = hidind.IndicatorAsk[-1]
        FilterList = hidind.IndicatorBid
      else:
        LocalBid = hidind.IndicatorBid
        LocalAsk = hidind.IndicatorAsk
        FilterList = hidind.IndicatorList
      # Wait until we have enough data to trade off
      if len(FilterList) >= genind.TradeDelay:
        if hasattr(hidind, 'TradeReverse'):
          if hidind.IndicatorList[-1] > LocalBid:
            it_signals.append(b)
          elif hidind.IndicatorList[-1] < LocalAsk:
            it_signals.append(s)
          else:
            it_signals.append(n)
        else:
          if hidind.IndicatorList[-1] < LocalBid:
            it_signals.append(b)
          elif hidind.IndicatorList[-1] > LocalAsk:
            it_signals.append(s)
          else:
            it_signals.append(n)
        if genind.SingleTrade and len(it_signals) > 1:
          if it_signals[-1] == it_signals[-2]:
            if genind.TradePersist:
              if len(it_signals) > 2 and not it_signals[-2] == it_signals[-3]:
                Trade_dict['Order'] = it_signals[-1]
              else:
                Trade_dict['Order'] = n
            else:
              Trade_dict['Order'] = n
          else:
            if genind.TradePersist:
              Trade_dict['Order'] = n
            else:
              Trade_dict['Order'] = it_signals[-1]
        else:
          if genind.TradePersist:
            if len(it_signals) > 2 and it_signals[-1] == \
                    it_signals[-2] and not it_signals[-2] == \
                    it_signals[-3]:
              Trade_dict['Order'] = it_signals[-1]
            else:
              Trade_dict['Order'] = n
          else:
            Trade_dict['Order'] = it_signals[-1]
