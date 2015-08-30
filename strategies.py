import ast

import hidconfig
from storage import indicators as storage
from storage import config

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
  # Hack for single indicator configuration
  for i in ast.literal_eval(config.gc['Trader']['Trade Indicators']):
    # Combined
    if isinstance(i, list):
      for l in i:
        Trade_dict['TradeVolume'] = int(config.gc['Trader']['Trade Volume'])
        try:
          hidind = getattr(hidconfig, l)
        except AttributeError:
          try:
            hidind = getattr(hidconfig, hidconfig.IndicatorAlias_dict[l])
          except AttributeError:
            hidind = getattr(hidconfig, hidconfig.IndicatorAlias2_dict[l])
        if hasattr(hidind, 'VolatilityIndicator'):
          FilterList = storage.getlist(hidind.IndicatorList)
          LocalThreshold = float(hidind.Threshold)
        elif hasattr(hidind, 'BidAskList'):
          FilterList = storage.getlist(hidind.IndicatorBid)
          if storage.getlist(hidind.IndicatorBid):
            if FilterList:
              LocalBid = float(storage.getlist(hidind.IndicatorBid)[-1])
              LocalAsk = float(storage.getlist(hidind.IndicatorAsk)[-1])
        else:
          LocalBid = float(hidind.IndicatorBid)
          LocalAsk = float(hidind.IndicatorAsk)
          FilterList = storage.getlist(hidind.IndicatorList)
        IndList = storage.getlist(hidind.IndicatorList)
        # Wait until we have enough data to trade off
        if len(FilterList) >= int(config.gc['Trader']['Trade Delay']):
          if hasattr(hidind, 'VolatilityIndicator'):
            try:
              vola = config.gc['Indicators'][l]['Volatility Threshold Over']
            except KeyError:
              try:
                vola = config.gc['Indicators'][
                    hidconfig.IndicatorAlias_dict[l]]['Volatility Threshold Over']
              except KeyError:
                vola = config.gc['Indicators'][
                    hidconfig.IndicatorAlias2_dict[l]]['Volatility Threshold Over']
            if ast.literal_eval(vola):
              if IndList[-1] > LocalThreshold:
                VolatilityTrade_list.append(True)
              else:
                VolatilityTrade_list.append(False)
            else:
              if IndList[-1] < LocalThreshold:
                VolatilityTrade_list.append(True)
              else:
                VolatilityTrade_list.append(False)
          elif hasattr(hidind, 'TradeReverse'):
            if IndList[-1] > LocalBid:
              CombinedTrade_list.append(b)
            elif IndList[-1] < LocalAsk:
              CombinedTrade_list.append(s)
            else:
              CombinedTrade_list.append(n)
          else:
            if IndList[-1] < LocalBid:
              CombinedTrade_list.append(b)
            elif IndList[-1] > LocalAsk:
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

      # Make a clean signal list without "None" for SingleTrade use.
      CleanTrade_list = LocalTrade_list[:]
      while n in CleanTrade_list:
        CleanTrade_list.remove(n)

      if ast.literal_eval(config.gc['Trader']['Single Trade']) and len(LocalTrade_list) > 1:
        if LocalTrade_list[-1] == LocalTrade_list[-2]:
          if ast.literal_eval(config.gc['Trader']['Trade Persist']):
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
          if ast.literal_eval(config.gc['Trader']['Trade Persist']):
            Trade_dict['Order'] = n
          else:
            if VolatilityTrade_list:
              if VolatilityTrade_list[-1]:
                if CleanTrade_list:
                  Trade_dict['Order'] = CleanTrade_list[-1]
                else:
                  Trade_dict['Order'] = LocalTrade_list[-1]
              else:
                Trade_dict['Order'] = n
            else:
              if len(CleanTrade_list) > 1:
                if not CleanTrade_list[-1] == CleanTrade_list[-2]:
                  Trade_dict['Order'] = LocalTrade_list[-1]
                else:
                  Trade_dict['Order'] = n
              else:
                Trade_dict['Order'] = LocalTrade_list[-1]
      else:  # SingleTrade not enabled.
        if ast.literal_eval(config.gc['Trader']['Trade Persist']):
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
      try:
        hidind = getattr(hidconfig, i)
      except AttributeError:
        try:
          hidind = getattr(hidconfig, hidconfig.IndicatorAlias_dict[i])
        except AttributeError:
          hidind = getattr(hidconfig, hidconfig.IndicatorAlias2_dict[i])
      try:
        try:
          genind = config.gc['Indicators'][i]['Trader']
        except KeyError:
          try:
            genind = config.gc['Indicators'][
                hidconfig.IndicatorAlias_dict[i]]['Trader']
          except KeyError:
            genind = config.gc['Indicators'][
                hidconfig.IndicatorAlias2_dict[i]]['Trader']
      except AttributeError:
        print(
            'ERROR: Volatility indicator must be combined with a non volatility indicator.')
        print('See galts-gulch.io/avarice/configuring/#trader for more info.')
      Trade_dict['TradeVolume'] = int(genind['Trade Volume'])
      # Create new key/dict value for this indicator if key doesn't exist
      if i not in IndependentTrade_dict:
        IndependentTrade_dict[i] = {'Signals': []}
      it_signals = IndependentTrade_dict[i]['Signals']
      if hasattr(hidind, 'BidAskList'):
        FilterList = storage.getlist(hidind.IndicatorBid)
        if hidind.IndicatorBid:
          if FilterList:
            LocalBid = storage.getlist(hidind.IndicatorBid)[-1]
            LocalAsk = storage.getlist(hidind.IndicatorAsk)[-1]
      else:
        LocalBid = hidind.IndicatorBid
        LocalAsk = hidind.IndicatorAsk
        FilterList = storage.getlist(hidind.IndicatorList)
      IndList = storage.getlist(hidind.IndicatorList)
      # Wait until we have enough data to trade off
      if len(FilterList) >= int(genind['Trade Delay']):
        if hasattr(hidind, 'TradeReverse'):
          if IndList[-1] > LocalBid:
            it_signals.append(b)
          elif IndList[-1] < LocalAsk:
            it_signals.append(s)
          else:
            it_signals.append(n)
        else:
          if IndList[-1] < LocalBid:
            it_signals.append(b)
          elif IndList[-1] > LocalAsk:
            it_signals.append(s)
          else:
            it_signals.append(n)
        if ast.literal_eval(genind['Single Trade']) and len(it_signals) > 1:
          if it_signals[-1] == it_signals[-2]:
            if ast.literal_eval(genind['Trade Persist']):
              if len(it_signals) > 2 and not it_signals[-2] == it_signals[-3]:
                Trade_dict['Order'] = it_signals[-1]
              else:
                Trade_dict['Order'] = n
            else:
              Trade_dict['Order'] = n
          else:
            if ast.literal_eval(genind['Trade Persist']):
              Trade_dict['Order'] = n
            else:
              Trade_dict['Order'] = it_signals[-1]
        else:
          if ast.literal_eval(genind['Trade Persist']):
            if len(it_signals) > 2 and it_signals[-1] == \
                    it_signals[-2] and not it_signals[-2] == \
                    it_signals[-3]:
              Trade_dict['Order'] = it_signals[-1]
            else:
              Trade_dict['Order'] = n
          else:
            Trade_dict['Order'] = it_signals[-1]
