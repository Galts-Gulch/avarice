from ast import literal_eval
from configobj import ConfigObj
from multiprocessing import Process

import avarice


class Runner(object):

  def __init__(self, target=avarice.RunAll):
    self.target = target
    self._proc = None

  def run(self):
    self._proc = Process(target=self.target)
    self._proc.start()

  def stop(self):
    self._proc.terminate()
    self._proc = None


class Configurables(object):

  def __init__(self):
    self.config = ConfigObj("config.ini", list_values=False)
    self.config.filename = "config.ini"
    # TODO: Better format dictionaries. Read from xml to make it less ugly?
    self.traderoptions = [
        'Trade Volume', 'Single Trade', 'Trade Persist', 'Trade Delay']
    self.indicator_dict = {'Simple Movement Average': {'Options': ['Verbose', 'Indicator Strategy',
                                                                   'Candle Size Multiplier',
                                                                   'Short Period', 'Long Period',
                                                                   'Diff Down', 'Diff Up'], 'Trader': True},
                           'Exponential Movement Average': {'Options': ['Verbose', 'Indicator Strategy',
                                                                        'Candle Size Multiplier',
                                                                        'Short Period', 'Long Period',
                                                                        'Diff Down', 'Diff Up'], 'Trader': True},
                           'Double Exponential Movement Average': {'Options': ['Verbose', 'Indicator Strategy',
                                                                               'Candle Size Multiplier',
                                                                               'Diff Down', 'Diff Up'],
                                                                   'Trader': True},
                           'EMAwbic': {'Options': ['Verbose', 'Candle Size Multiplier',
                                                   'Period', 'Bid', 'Ask'], 'Trader': True},
                           'Fractal Adaptive Movement Average': {'Options': ['Verbose',
                                                                             'Indicator Strategey',
                                                                             'Candle Size Multiplier',
                                                                             'Short Period', 'Long Period',
                                                                             'Alpha Constant', 'Diff Down',
                                                                             'Diff Up'], 'Trader': True},
                           'MACD': {'Options': ['Verbose', 'Indicator Strategy', 'Candle Size Multiplier',
                                                'Short period', 'Signal Period', 'Diff Down', 'Diff Up'],
                                    'Trader': True},
                           'DMACD': {'Options': ['Verbose', 'Indicator Strategy', 'Candle Size Multiplier',
                                                 'Signal Period', 'Diff Down', 'Diff Up'], 'Trader': True},
                           'RSI': {'Options': ['Verbose', 'Candle Size Multiplier', 'Period', 'Ask', 'Bid'],
                                   'Trader': True},
                           'Fast Stochastic RSI %K': {'Options': ['Verbose', 'Period', 'Ask', 'Bid'],
                                                      'Trader': True},
                           'Fast Stochastic RSI %D': {'Options': ['Verbose', 'Period', 'Ask', 'Bid'],
                                                      'Trader': True},
                           'Full Stochastic RSI %D': {'Options': ['Verbose', 'Period', 'Ask', 'Bid'],
                                                      'Trader': True},
                           'Fast Stochastic %K': {'Options': ['Verbose', 'Candle Size Multiplier' 'Period',
                                                              'Ask', 'Bid'], 'Trader': True},
                           'Fast Stochastic %D': {'Options': ['Verbose', 'Period', 'Ask', 'Bid'],
                                                  'Trader': True},
                           'Full Stochastic %D': {'Options': ['Verbose', 'Period', 'Ask', 'Bid'],
                                                  'Trader': True},
                           'KDJ': {'Options': ['Verbose', 'Indicator Strategy', 'Candle Size Multiplier',
                                               'Fast K Period', 'Full K Period', 'Full D Period', 'Ask',
                                               'Bid'], 'Trader': True},
                           'Aroon': {'Options': ['Verbose', 'Indicator Strategy', 'Candle Size Multiplier',
                                                 'Period', 'Ask', 'Bid'], 'Trader': True},
                           'Ichimoku': {'Options': ['Verbose', 'Indicator Strategy', 'Candle Size Multiplier',
                                                    'Tenkan-Sen Period', 'Senkou Span Period', 'Kijun-Sen Period',
                                                    'Chikou Span Period'], 'Trader': True,
                                        'Overrides': {'Indicator Strategy': {
                                            'Description': "See <a href='http://galts-gulch.github.io/avarice/indicators/#ichimoku-ichimoku-cloud'>documentation</a> for info on supported strategies.",
                                            'MenuOptions': ['Optimized', 'Strong', 'Weak', 'CloudOnly'],
                                            'Type': 'ComboBox'}}},
                           'Standard Deviation': {'Options': ['Verbose', 'Candle Size Multiplier',
                                                              'Volatility Threshold Over', 'Period', 'Threshold'],
                                                  'Volatility': True},
                           'Bollinger Bands': {'Options': ['Verbose', 'Candle Size Multiplier', 'Period'], 'Full': False},
                           'Bollinger Bandwidth': {'Options': ['Verbose', 'Volatility Threshold Over', 'Threshold'],
                                                   'Volatility': True},
                           'Average True Range': {'Options': ['Verbose', 'Volatility Threshold Over',
                                                              'Candle Size Multiplier', 'Period', 'Threshold'],
                                                  'Volatility': True},
                           'Chandelier Exit': {'Options': ['Verbose', 'Candle Size Multiplier', 'Period',
                                                           'Multiplier'], 'Trader': True},
                           'Directional Movement Index': {'Options': ['Verbose', 'Indicator Strategy',
                                                                      'Volatility Threshold Over', 'Threshold'],
                                                          'Trader': True, 'Overrides': {'Indicator Strategy': {
                                                              'Description': "'Full' uses ADX threshold, and +DI -DI crossovers to determine signal. 'DI' uses +DI -DI crossovers to determine signal. 'Volatility' only uses ADX threshold as volatility indicator (must be combined)",
                                                              'MenuOptions': ['Full', 'DI', 'Volatility'], 'Type': 'ComboBox'}}},
                           'Simple Rate of Change': {'Options': ['Verbose', 'Candle Size Multiplier', 'Period'],
                                                     'Trader': True}}
    self.indicatoroptions = {'Verbose': {'Type': 'checkbox', 'Description': 'Should we print additional information about the indicator on each candle?'},
                             'Candle Size Multiplier':
                             {'Description': 'Used for aggregation. E.g. set to 3 if on 5 min candles and 15min indicator period is desired.',
                              'Type': 'SpinButton'},
                             'Indicator Strategy': {'Description': 'Convergence/Divergence trades on short/long convergence/divergence. Difference trades on the difference between short/long.',
                                                    'MenuOptions': ['Convergence/Divergence', 'Diff'],
                                                    'Type': 'ComboBox'},
                             'Tenkan-Sen Period': {'Type': 'SpinButton'},
                             'Senkou Span Period': {'Type': 'SpinButton',
                                                    'Description': 'Default is 2 * Kijun-Sen Period'},
                             'Kijun-Sen Period': {'Type': 'SpinButton'},
                             'Chikou Span Period': {'Type': 'SpinButton',
                                                    'Description': 'Default is the same as Kijun-Sen Period'},
                             'Trade Volume': {'Type': 'SpinButton', 'SpinButtonFloat': True,
                                              'Description': 'Percentage of available asset and currency evaluated on each trade. 50 is 50%. Only used on an independent indicator. It is recommended to set this to a low value if SingleTrade is disabled.'},
                             'Single Trade': {'Type': 'checkbox',
                                              'Description': 'Should we only do a single sell or buy? This still uses Trade Volume percent on each trade. This is useful for MA style strategies, whereas oscillator or diff style should be set to False (to often continue selling if above threshold, or buying below).'},
                             'Trade Persist': {'Type': 'checkbox',
                                               'Description': 'Waits for a signal to persist two candles.'},
                             'Trade Delay': {'Type': 'SpinButton', 'Description': 'Number of candles with indicator info before trading.'},
                             'Short Period': {'Type': 'SpinButton'},
                             'Long Period': {'Type': 'SpinButton'},
                             'Period': {'Type': 'SpinButton'},
                             'Alpha Constant': {'Type': 'SpinButton', 'SpinButtonFloat': True},
                             'Signal Period': {'Type': 'SpinButton'},
                             'Fast K Period': {'Type': 'SpinButton'},
                             'Full K Period': {'Type': 'SpinButton'},
                             'Full D Period': {'Type': 'SpinButton'},
                             'Multiplier': {'Type': 'SpinButton'},
                             'Volatility Threshold Over': {'Type': 'checkbox',
                                                           'Description': 'This is default enabled and runs if the volatility indicator is above threshold. This may be set to False to reverse the behavior.'},
                             'Bid': {'Type': 'SpinButton', 'Description': 'Buy when less than Bid'},
                             'Ask': {'Type': 'SpinButton', 'Description': 'Sell when greater than Ask'},
                             'Diff Up': {'Type': 'SpinButton', 'SpinButtonFloat': True, 'Description': 'Wait to pass this threshold before trend is determined.'},
                             'Diff Down': {'Type': 'SpinButton', 'SpinButtonFloat': True, 'Description': 'Wait to pass this threshold before trend is dtermined.'},
                             'Threshold': {'Type': 'SpinButton', 'SpinButtonFloat': True, 'Description': 'Threshold to limit trades for volatility indicators.'}}

  def get_indicator_structure(self, indicator):
    """Gets full indicator configuration structure in dict form.
    Uses booleans to describe if indicator may be combined, independent, or both.
    """
    ind = self.indicator_dict[indicator]
    indopts = ind['Options'][::]

    # Add trader defaults if applicable.
    try:
      if ind['Trader']:
        for i in self.traderoptions:
          indopts.append(i)
    except KeyError:
      pass
    # Create new dict
    fullind = {'Options': {}}
    # Fill out Options
    for i in indopts:
      fullind['Options'][i] = self.indicatoroptions[i]
    # Override default keys.
    try:
      for i in ind['Overrides']:
        fullind['Options'][i] = ind['Overrides'][i]
    except KeyError:
      pass
    # Add defaults for options. XXX: Must happen after overriding defaults.
    for i in indopts:
      if i in self.traderoptions:
        fullind['Options'][i]['Default'] = self.config[
            'Indicators'][indicator]['Trader'][i]
      else:
        fullind['Options'][i]['Default'] = self.config[
            'Indicators'][indicator][i]
    # Add Volatility boolean
    try:
      fullind['Volatility'] = ind['Volatility']
    except KeyError:
      fullind['Volatility'] = False
    # Add Full boolean (only in use on Bollinger Bandwidth)
    try:
      fullind['Full'] = ind['Full']
    except KeyError:
      fullind['Full'] = True

    return fullind

  def write_indicator_structure(self, indicator, option, value):
    """Writes a string option to a string indicator"""
    if option in self.traderoptions:
      self.config['Indicators'][indicator]['Trader'][option] = value
    else:
      self.config['Indicators'][indicator][option] = value
    config.write()
