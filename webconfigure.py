import ast
from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import TextField, BooleanField, SelectField, SubmitField, FormField
from configobj import ConfigObj
config = ConfigObj("config.ini", list_values=False)
config.filename = "config.ini"


class API(Form):
  verbose = BooleanField('Verbose',
                         description='Print API re-connections',
                         default=ast.literal_eval(
                             config['API']['Verbose']))
  exchange = SelectField(
      'Exchange', default='okcoin', choices=[('okcoin', 'okcoin')])
  tradepair = SelectField('Trade Pair', default=config['API']['Trade Pair'],
                          choices=[('btc_cny', 'btc_cny'), ('ltc_cny', 'ltc_cny'),
                                   ('btc_usd', 'btc_usd'), ('ltc_usd', 'ltc_usd')])
  apikey = TextField('API Key', description='Only used when live trading',
                     default=config['API']['API Key'])
  secretkey = TextField('Secret Key', description='Only used when live trading',
                        default=config['API']['Secret Key'])
  trademin = TextField('Asset Trade Minimum',
                       description='0.01 for BTC and 0.1 for LTC. This may be set higher',
                       default=config['API']['Asset Trade Minimum'])
  api_submit = SubmitField('Save')


class Candles(Form):
  verbose = BooleanField('Verbose',
                         description='Print API re-connections',
                         default=ast.literal_eval(
                             config['Candles']['Verbose']))
  size = TextField(
      'Size', description='In minutes', default=config['Candles']['Size'])
  candles_submit = SubmitField('Save')


# TODO: cleanup long strings
class Trader(Form):
  enabled = BooleanField('Enabled',
                         description='Should we live trade with real money?' +
                         ' This always sells/buys at market bid/ask.',
                         default=ast.literal_eval(config['Trader']['Enabled']))
  verbose = BooleanField('Verbose',
                         description='Print on every trade',
                         default=ast.literal_eval(config['Trader']['Verbose']))
  tradeindicators = TextField('Trade Indicators',
                              description='See http://http://galts-gulch.github.io/avarice/configuring/#trader',
                              default=config['Trader']['Trade Indicators'])
  verboseindicators = TextField('Verbose Indicators',
                                description='Indicators which should be verbose each candle.',
                                default=config['Trader']['Verbose Indicators'])
  advancedstrategy = TextField('Advanced Strategy',
                               description='This is an advanced option with no'
                               + ' other available option stock. This may be '
                               +
                                 'changed to the function name of a custom written '
                               + 'strategy in strategies.py.',
                               default=config['Trader']['Advanced Strategy'])
  tradevolume = TextField('Trade Volume', description='Percentage of available asset and currency evaluated on each trade. 50 is 50%. Only used on combined indicators. It is recommended to set this to a low value if SingleTrade is disabled.',
                          default=config['Trader']['Trade Volume'])
  singletrade = TextField('Single Trade', description='Should we only do a single consecutive sell or buy? This still uses TradeVolume percent on each trade. This is useful for MA style strategies, whereas oscillator or diff style should be set to False (to often continue selling if above threshold, or buying below).',
                          default=config['Trader']['Single Trade'])
  tradepersist = TextField('Trade Persist', description='Waits for a signal to persist two candles.',
                           default=config['Trader']['Trade Persist'])
  tradedelay = TextField('Trade Delay', description='How many candles with indicator info before allowing trades?',
                         default=config['Trader']['Trade Delay'])
  reissueslippage = TextField('ReIssue Slippage', description='What delta (as a percentage) of order price should we continue trying to get an order through for?',
                              default=config['Trader']['ReIssue Slippage'])
  reissuedelay = TextField('ReIssue Delay', description='How many seconds should we wait for an order to succeed before attempting to re-order? This also affects the order delay',
                           default=config['Trader']['ReIssue Delay'])
  trader_submit = SubmitField('Save')


class Simulator(Form):
  verbose = BooleanField(
      'Verbose', default=ast.literal_eval(config['Simulator']['Verbose']))
  asset = TextField('Asset', description='Number of BTC or LTC to start the simulation with.',
                    default=config['Simulator']['Asset'])
  currency = TextField('Currency', description='Number of CNY or USD to start the simulation with.',
                       default=config['Simulator']['Currency'])
  simulator_submit = SubmitField('Save')


class TextFile(Form):
  rollover = TextField('Rollover Time', description=' Time in hours to switch to a new log file.',
                       default=config['Notifier']['Text File']['Rollover Time'])
  backup = TextField('Backup Count', description='Number of log files to keep. 0 to keep all.',
                     default=config['Notifier']['Text File']['Backup Count'])
  path1 = TextField('Path', description='Relative path to simulator and trader text file directory.',
                    default=config['Notifier']['Text File']['Path'])
  tfilename = TextField('Trader File Name', description='Filename for trader log file.',
                        default=config['Notifier']['Text File']['Trader File Name'])
  sfilename = TextField('Simulator File Name', description='Filename for simulator log file.',
                        default=config['Notifier']['Text File']['Simulator File Name'])
  textfile_submit = SubmitField('Save')


class Pushover(Form):
  simulator = BooleanField('Simulator', description='Enable for simulator actions.',
                           default=ast.literal_eval(config['Notifier']['Pushover']['Simulator']))
  trader = BooleanField('Trader', description='Enable for trader actions.',
                        default=ast.literal_eval(config['Notifier']['Pushover']['Trader']))
  app = TextField('App Token', description='The Pushover Application Token to be used.',
                  default=config['Notifier']['Pushover']['App Token'])
  user = TextField('User Key', description='Your Pushover User Key found on the Pushover dashboard.',
                   default=config['Notifier']['Pushover']['User Key'])
  pushover_submit = SubmitField('Save')


class SMTP(Form):
  simulator = BooleanField('Simulator', description='Enable for simulator actions.',
                           default=ast.literal_eval(config['Notifier']['SMTP']['Simulator']))
  trader = BooleanField('Trader', description='Enable for trader actions.',
                        default=ast.literal_eval(config['Notifier']['SMTP']['Trader']))
  host = TextField('Host', description='SMTP host to be used.',
                   default=config['Notifier']['SMTP']['Host'])
  From = TextField('From', description='SMTP account to send from.',
                   default=config['Notifier']['SMTP']['From'])
  to = TextField('To', description='Email address to send to.',
                 default=config['Notifier']['SMTP']['To'])
  smtp_submit = SubmitField('Save')


class TLSSMTP(Form):
  simulator = BooleanField('Simulator', description='Enable for simulator actions.',
                           default=ast.literal_eval(config['Notifier']['TLS SMTP']['Simulator']))
  trader = BooleanField('Trader', description='Enable for trader actions.',
                        default=ast.literal_eval(config['Notifier']['TLS SMTP']['Trader']))
  host = TextField('Host', description='TLS SMTP host to be used. smtp.gmail.com by default for GMail.',
                   default=config['Notifier']['TLS SMTP']['Host'])
  port = TextField('Port', description='TLS SMTP port to be used. 587 by default for GMail.',
                   default=config['Notifier']['TLS SMTP']['Port'])
  user = TextField('Username', description='For GMail creating a new account is recommended. You will need to login to your new GMail account and enable access for less secure apps.',
                   default=config['Notifier']['TLS SMTP']['Username'])
  passw = TextField('Password', description='Your TLS SMTP account password.',
                    default=config['Notifier']['TLS SMTP']['Password'])
  to = TextField('To', description='Email address to send to.',
                 default=config['Notifier']['TLS SMTP']['To'])
  tlssmtp_submit = SubmitField('Save')


class Database(Form):
  store = BooleanField(
      'Store All', default=ast.literal_eval(config['Database']['Store All']))
  debug = BooleanField(
      'Debug', default=ast.literal_eval(config['Database']['Debug']))
  path2 = TextField('Path', description='Relative path to database directory',
                    default=config['Database']['Path'])
  database_submit = SubmitField('Save')


class Grapher(Form):
  enabled = BooleanField('Enabled', description='Record graphs. Requires pygal and lxml',
                         default=ast.literal_eval(config['Grapher']['Enabled']))
  stime = BooleanField('Show Time Instead of Candles', default=ast.literal_eval(
      config['Grapher']['Show Time']))
  path3 = TextField('Path', description='Relative path to chart directory.',
                    default=config['Grapher']['Path'])
  theme = SelectField('Theme', default='DarkSolarized', choices=[
      ('DarkSolarized', 'Dark Solarized'),
      ('LightSolarized', 'Light Solarized'), ('Light', 'Light'),
      ('Clean', 'Clean'), ('Red Blue', 'Red Blue'),
      ('DarkColorized', 'Dark Colorized'),
      ('LightColorized', 'Light Colorized'),
      ('Turquoise', 'Turquoise'), ('LightGreen', 'Light Green'),
      ('DarkGreen', 'Dark Green'), ('DarkGreenBlue', 'Dark Green Blue'),
      ('Blue', 'Blue')])
  look = TextField('Max Lookback', description='Max candles to show on x-axis',
                   default=config['Grapher']['Max Lookback'])
  grapher_submit = SubmitField('Save')


class SMA(Form):
  indstr1 = SelectField('Indicator Strategy',
                        default=config['Indicators'][
                            'Simple Movement Average']['Indicator Strategy'],
                        choices=[
                            ('CD', 'Convergence/Divergence'), ('Diff', 'Difference')],
                        description='Convergence/Divergence trades on short/long convergence/divergence. Difference trades on the difference between short/long.')
  sp1 = TextField(
      'Short Period', default=config['Indicators']['Simple Movement Average']['Short Period'])
  lp1 = TextField(
      'Long Period', default=config['Indicators']['Simple Movement Average']['Long Period'])
  dd1 = TextField('Diff Down', default=config['Indicators']['Simple Movement Average']['Diff Down'],
                  description='Only used on "Diff" Indicator Strategy')
  du1 = TextField('Diff Up', default=config['Indicators']['Simple Movement Average']['Diff Up'],
                  description='Only used on "Diff" Indicator Strategy')
  tv1 = TextField('Trade Volume', description='Percentage of available asset and currency evaluated on each trade. 50 is 50%. Only used on an independent indicator. It is recommended to set this to a low value if SingleTrade is disabled.',
                  default=config['Indicators']['Simple Movement Average']['Trader']['Trade Volume'])
  st1 = BooleanField('Single Trade', description='Should we only do a single consecutive sell or buy? Only used on an independent indicator. This still uses TradeVolume percent on each trade. This is useful for MA style strategies, whereas oscillator or diff style should be set to False (to often continue selling if above threshold, or buying below).',
                     default=ast.literal_eval(config['Indicators']['Simple Movement Average']['Trader']['Single Trade']))
  tp1 = BooleanField('Trade Persist', description='Waits for a signal to persist two candles. Only used on an independent indicator.',
                     default=ast.literal_eval(config['Indicators']['Simple Movement Average']['Trader']['Trade Persist']))
  td1 = TextField('Trade Delay', description='Number of candles with indicator info before trading. Must be greater than 0. Only used on an independent indicator.',
                  default=config['Indicators']['Simple Movement Average']['Trader']['Trade Delay'])
  sma_submit = SubmitField('Save')


class EMA(Form):
  indstr2 = SelectField('Indicator Strategy',
                        default=config['Indicators'][
                            'Exponential Movement Average']['Indicator Strategy'],
                        choices=[
                            ('CD', 'Convergence/Divergence'), ('Diff', 'Difference')],
                        description='Convergence/Divergence trades on short/long convergence/divergence. Difference trades on the difference between short/long.')
  sp2 = TextField(
      'Short Period', default=config['Indicators']['Exponential Movement Average']['Short Period'])
  lp2 = TextField(
      'Long Period', default=config['Indicators']['Exponential Movement Average']['Long Period'])
  dd2 = TextField('Diff Down', default=config['Indicators']['Exponential Movement Average']['Diff Down'],
                  description='Only used on "Diff" Indicator Strategy')
  du2 = TextField('Diff Up', default=config['Indicators']['Exponential Movement Average']['Diff Up'],
                  description='Only used on "Diff" Indicator Strategy')
  tv2 = TextField('Trade Volume', description='Percentage of available asset and currency evaluated on each trade. 50 is 50%. Only used on an independent indicator. It is recommended to set this to a low value if SingleTrade is disabled.',
                  default=config['Indicators']['Exponential Movement Average']['Trader']['Trade Volume'])
  st2 = BooleanField('Single Trade', description='Should we only do a single consecutive sell or buy? Only used on an independent indicator. This still uses TradeVolume percent on each trade. This is useful for MA style strategies, whereas oscillator or diff style should be set to False (to often continue selling if above threshold, or buying below).',
                     default=ast.literal_eval(config['Indicators']['Exponential Movement Average']['Trader']['Single Trade']))
  tp2 = BooleanField('Trade Persist', description='Waits for a signal to persist two candles. Only used on an independent indicator.',
                     default=ast.literal_eval(config['Indicators']['Exponential Movement Average']['Trader']['Trade Persist']))
  td2 = TextField('Trade Delay', description='Number of candles with indicator info before trading. Must be greater than 0. Only used on an independent indicator.',
                  default=config['Indicators']['Exponential Movement Average']['Trader']['Trade Delay'])
  ema_submit = SubmitField('Save')


class DEMA(Form):
  indstr3 = SelectField('Indicator Strategy',
                        default=config['Indicators'][
                            'Double Exponential Movement Average']['Indicator Strategy'],
                        choices=[
                            ('CD', 'Convergence/Divergence'), ('Diff', 'Difference')],
                        description='Convergence/Divergence trades on short/long convergence/divergence. Difference trades on the difference between short/long.')

  dd3 = TextField('Diff Down', default=config['Indicators']['Double Exponential Movement Average']['Diff Down'],
                  description='Only used on "Diff" Indicator Strategy')
  du3 = TextField('Diff Up', default=config['Indicators']['Double Exponential Movement Average']['Diff Up'],
                  description='Only used on "Diff" Indicator Strategy')
  tv3 = TextField('Trade Volume', description='Percentage of available asset and currency evaluated on each trade. 50 is 50%. Only used on an independent indicator. It is recommended to set this to a low value if SingleTrade is disabled.',
                  default=config['Indicators']['Double Exponential Movement Average']['Trader']['Trade Volume'])
  st3 = BooleanField('Single Trade', description='Should we only do a single consecutive sell or buy? Only used on an independent indicator. This still uses TradeVolume percent on each trade. This is useful for MA style strategies, whereas oscillator or diff style should be set to False (to often continue selling if above threshold, or buying below).',
                     default=ast.literal_eval(config['Indicators']['Double Exponential Movement Average']['Trader']['Single Trade']))
  tp3 = BooleanField('Trade Persist', description='Waits for a signal to persist two candles. Only used on an independent indicator.',
                     default=ast.literal_eval(config['Indicators']['Double Exponential Movement Average']['Trader']['Trade Persist']))
  td3 = TextField('Trade Delay', description='Number of candles with indicator info before trading. Must be greater than 0. Only used on an independent indicator.',
                  default=config['Indicators']['Double Exponential Movement Average']['Trader']['Trade Delay'])
  dema_submit = SubmitField('Save')


class EMAwbic(Form):
  period1 = TextField(
      'Period', default=config['Indicators']['EMAwbic']['Period'])
  bid1 = TextField('Bid', default=config['Indicators']['EMAwbic']['Bid'],
                   description='Buy when price is < Bid % of EMA')
  ask1 = TextField('Ask', default=config['Indicators']['EMAwbic']['Ask'],
                   description='Sell when price is > Ask % of EMA')
  tv4 = TextField('Trade Volume', description='Percentage of available asset and currency evaluated on each trade. 50 is 50%. Only used on an independent indicator. It is recommended to set this to a low value if SingleTrade is disabled.',
                  default=config['Indicators']['EMAwbic']['Trader']['Trade Volume'])
  st4 = BooleanField('Single Trade', description='Should we only do a single consecutive sell or buy? Only used on an independent indicator. This still uses TradeVolume percent on each trade. This is useful for MA style strategies, whereas oscillator or diff style should be set to False (to often continue selling if above threshold, or buying below).',
                     default=ast.literal_eval(config['Indicators']['EMAwbic']['Trader']['Single Trade']))
  tp4 = BooleanField('Trade Persist', description='Waits for a signal to persist two candles. Only used on an independent indicator.',
                     default=ast.literal_eval(config['Indicators']['EMAwbic']['Trader']['Trade Persist']))
  td4 = TextField('Trade Delay', description='Number of candles with indicator info before trading. Must be greater than 0. Only used on an independent indicator.',
                  default=config['Indicators']['EMAwbic']['Trader']['Trade Delay'])
  emawbic_submit = SubmitField('Save')


class FRAMA(Form):
  indstr5 = SelectField('Indicator Strategy',
                        default=config['Indicators'][
                            'Fractal Adaptive Movement Average']['Indicator Strategy'],
                        choices=[
                            ('CD', 'Convergence/Divergence'), ('Diff', 'Difference')],
                        description='Convergence/Divergence trades on short/long convergence/divergence. Difference trades on the difference between short/long.')
  sp5 = TextField(
      'Short Period', default=config['Indicators']['Fractal Adaptive Movement Average']['Short Period'])
  lp5 = TextField(
      'Long Period', default=config['Indicators']['Fractal Adaptive Movement Average']['Long Period'])
  ac = TextField(
      'Alpha Constant', default=config['Indicators']['Fractal Adaptive Movement Average']['Alpha Constant'])
  dd5 = TextField('Diff Down', default=config['Indicators']['Fractal Adaptive Movement Average']['Diff Down'],
                  description='Only used on "Diff" Indicator Strategy')
  du5 = TextField('Diff Up', default=config['Indicators']['Fractal Adaptive Movement Average']['Diff Up'],
                  description='Only used on "Diff" Indicator Strategy')
  tv5 = TextField('Trade Volume', description='Percentage of available asset and currency evaluated on each trade. 50 is 50%. Only used on an independent indicator. It is recommended to set this to a low value if SingleTrade is disabled.',
                  default=config['Indicators']['Fractal Adaptive Movement Average']['Trader']['Trade Volume'])
  st5 = BooleanField('Single Trade', description='Should we only do a single consecutive sell or buy? Only used on an independent indicator. This still uses TradeVolume percent on each trade. This is useful for MA style strategies, whereas oscillator or diff style should be set to False (to often continue selling if above threshold, or buying below).',
                     default=ast.literal_eval(config['Indicators']['Fractal Adaptive Movement Average']['Trader']['Single Trade']))
  tp5 = BooleanField('Trade Persist', description='Waits for a signal to persist two candles. Only used on an independent indicator.',
                     default=ast.literal_eval(config['Indicators']['Fractal Adaptive Movement Average']['Trader']['Trade Persist']))
  td5 = TextField('Trade Delay', description='Number of candles with indicator info before trading. Must be greater than 0. Only used on an independent indicator.',
                  default=config['Indicators']['Fractal Adaptive Movement Average']['Trader']['Trade Delay'])
  frama_submit = SubmitField('Save')


class MACD(Form):
  indstr6 = SelectField('Indicator Strategy',
                        default=config['Indicators'][
                            'MACD']['Indicator Strategy'],
                        choices=[
                            ('CD', 'Convergence/Divergence'), ('Diff', 'Difference')],
                        description='Convergence/Divergence trades on MACD/signal convergence/divergence. Difference trades on the difference between MACD and signal.')
  sp6 = TextField(
      'Short Period', default=config['Indicators']['MACD']['Short Period'])
  lp6 = TextField(
      'Long Period', default=config['Indicators']['MACD']['Long Period'])
  sig1 = TextField(
      'Signal Period', default=config['Indicators']['MACD']['Signal Period'])
  dd6 = TextField('Diff Down', default=config['Indicators']['MACD']['Diff Down'],
                  description='Only used on "Diff" Indicator Strategy')
  du6 = TextField('Diff Up', default=config['Indicators']['MACD']['Diff Up'],
                  description='Only used on "Diff" Indicator Strategy')
  tv6 = TextField('Trade Volume', description='Percentage of available asset and currency evaluated on each trade. 50 is 50%. Only used on an independent indicator. It is recommended to set this to a low value if SingleTrade is disabled.',
                  default=config['Indicators']['MACD']['Trader']['Trade Volume'])
  st6 = BooleanField('Single Trade', description='Should we only do a single consecutive sell or buy? Only used on an independent indicator. This still uses TradeVolume percent on each trade. This is useful for MA style strategies, whereas oscillator or diff style should be set to False (to often continue selling if above threshold, or buying below).',
                     default=ast.literal_eval(config['Indicators']['MACD']['Trader']['Single Trade']))
  tp6 = BooleanField('Trade Persist', description='Waits for a signal to persist two candles. Only used on an independent indicator.',
                     default=ast.literal_eval(config['Indicators']['MACD']['Trader']['Trade Persist']))
  td6 = TextField('Trade Delay', description='Number of candles with indicator info before trading. Must be greater than 0. Only used on an independent indicator.',
                  default=config['Indicators']['MACD']['Trader']['Trade Delay'])
  macd_submit = SubmitField('Save')


class DMACD(Form):
  indstr7 = SelectField('Indicator Strategy',
                        default=config['Indicators'][
                            'DMACD']['Indicator Strategy'],
                        choices=[
                            ('CD', 'Convergence/Divergence'), ('Diff', 'Difference')],
                        description='Convergence/Divergence trades on MACD/signal convergence/divergence. Difference trades on the difference between MACD and signal.')
  sig2 = TextField(
      'Signal Period', default=config['Indicators']['DMACD']['Signal Period'])
  dd7 = TextField('Diff Down', default=config['Indicators']['DMACD']['Diff Down'],
                  description='Only used on "Diff" Indicator Strategy')
  du7 = TextField('Diff Up', default=config['Indicators']['DMACD']['Diff Up'],
                  description='Only used on "Diff" Indicator Strategy')
  tv7 = TextField('Trade Volume', description='Percentage of available asset and currency evaluated on each trade. 50 is 50%. Only used on an independent indicator. It is recommended to set this to a low value if SingleTrade is disabled.',
                  default=config['Indicators']['DMACD']['Trader']['Trade Volume'])
  st7 = BooleanField('Single Trade', description='Should we only do a single consecutive sell or buy? Only used on an independent indicator. This still uses TradeVolume percent on each trade. This is useful for MA style strategies, whereas oscillator or diff style should be set to False (to often continue selling if above threshold, or buying below).',
                     default=ast.literal_eval(config['Indicators']['DMACD']['Trader']['Single Trade']))
  tp7 = BooleanField('Trade Persist', description='Waits for a signal to persist two candles. Only used on an independent indicator.',
                     default=ast.literal_eval(config['Indicators']['DMACD']['Trader']['Trade Persist']))
  td7 = TextField('Trade Delay', description='Number of candles with indicator info before trading. Must be greater than 0. Only used on an independent indicator.',
                  default=config['Indicators']['DMACD']['Trader']['Trade Delay'])
  dmacd_submit = SubmitField('Save')


class RSI(Form):
  period2 = TextField('Period', default=config['Indicators']['RSI']['Period'])
  bid2 = TextField('Bid', default=config['Indicators']['RSI']['Bid'],
                   description='Buy when RSI is < Bid')
  ask2 = TextField('Ask', default=config['Indicators']['RSI']['Ask'],
                   description='Sell when RSI is > Ask')
  tv8 = TextField('Trade Volume', description='Percentage of available asset and currency evaluated on each trade. 50 is 50%. Only used on an independent indicator. It is recommended to set this to a low value if SingleTrade is disabled.',
                  default=config['Indicators']['RSI']['Trader']['Trade Volume'])
  st8 = BooleanField('Single Trade', description='Should we only do a single consecutive sell or buy? Only used on an independent indicator. This still uses TradeVolume percent on each trade. This is useful for MA style strategies, whereas oscillator or diff style should be set to False (to often continue selling if above threshold, or buying below).',
                     default=ast.literal_eval(config['Indicators']['RSI']['Trader']['Single Trade']))
  tp8 = BooleanField('Trade Persist', description='Waits for a signal to persist two candles. Only used on an independent indicator.',
                     default=ast.literal_eval(config['Indicators']['RSI']['Trader']['Trade Persist']))
  td8 = TextField('Trade Delay', description='Number of candles with indicator info before trading. Must be greater than 0. Only used on an independent indicator.',
                  default=config['Indicators']['RSI']['Trader']['Trade Delay'])
  rsi_submit = SubmitField('Save')


class FastStochRSIK(Form):
  period3 = TextField(
      'Period', default=config['Indicators']['Fast Stochastic RSI %K']['Period'])
  bid3 = TextField('Bid', default=config['Indicators']['Fast Stochastic RSI %K']['Bid'],
                   description='Buy when Fast Stochastic RSI %K is < Bid')
  ask3 = TextField('Ask', default=config['Indicators']['Fast Stochastic RSI %K']['Ask'],
                   description='Sell when Fast Stochastic RSI %K is > Ask')
  tv9 = TextField('Trade Volume', description='Percentage of available asset and currency evaluated on each trade. 50 is 50%. Only used on an independent indicator. It is recommended to set this to a low value if SingleTrade is disabled.',
                  default=config['Indicators']['Fast Stochastic RSI %K']['Trader']['Trade Volume'])
  st9 = BooleanField('Single Trade', description='Should we only do a single consecutive sell or buy? Only used on an independent indicator. This still uses TradeVolume percent on each trade. This is useful for MA style strategies, whereas oscillator or diff style should be set to False (to often continue selling if above threshold, or buying below).',
                     default=ast.literal_eval(config['Indicators']['Fast Stochastic RSI %K']['Trader']['Single Trade']))
  tp9 = BooleanField('Trade Persist', description='Waits for a signal to persist two candles. Only used on an independent indicator.',
                     default=ast.literal_eval(config['Indicators']['Fast Stochastic RSI %K']['Trader']['Trade Persist']))
  td9 = TextField('Trade Delay', description='Number of candles with indicator info before trading. Must be greater than 0. Only used on an independent indicator.',
                  default=config['Indicators']['Fast Stochastic RSI %K']['Trader']['Trade Delay'])
  faststochrsik_submit = SubmitField('Save')


class FastStochRSID(Form):
  period4 = TextField(
      'Period', default=config['Indicators']['Fast Stochastic RSI %D']['Period'])
  bid4 = TextField('Bid', default=config['Indicators']['Fast Stochastic RSI %D']['Bid'],
                   description='Buy when Fast Stochastic RSI %D is < Bid')
  ask4 = TextField('Ask', default=config['Indicators']['Fast Stochastic RSI %D']['Ask'],
                   description='Sell when Fast Stochastic RSI %D is > Ask')
  tv10 = TextField('Trade Volume', description='Percentage of available asset and currency evaluated on each trade. 50 is 50%. Only used on an independent indicator. It is recommended to set this to a low value if SingleTrade is disabled.',
                   default=config['Indicators']['Fast Stochastic RSI %D']['Trader']['Trade Volume'])
  st10 = BooleanField('Single Trade', description='Should we only do a single consecutive sell or buy? Only used on an independent indicator. This still uses TradeVolume percent on each trade. This is useful for MA style strategies, whereas oscillator or diff style should be set to False (to often continue selling if above threshold, or buying below).',
                      default=ast.literal_eval(config['Indicators']['Fast Stochastic RSI %D']['Trader']['Single Trade']))
  tp10 = BooleanField('Trade Persist', description='Waits for a signal to persist two candles. Only used on an independent indicator.',
                      default=ast.literal_eval(config['Indicators']['Fast Stochastic RSI %D']['Trader']['Trade Persist']))
  td10 = TextField('Trade Delay', description='Number of candles with indicator info before trading. Must be greater than 0. Only used on an independent indicator.',
                   default=config['Indicators']['Fast Stochastic RSI %D']['Trader']['Trade Delay'])
  faststochrsid_submit = SubmitField('Save')


class FullStochRSID(Form):
  period5 = TextField(
      'Period', default=config['Indicators']['Full Stochastic RSI %D']['Period'])
  bid5 = TextField('Bid', default=config['Indicators']['Full Stochastic RSI %D']['Bid'],
                   description='Buy when Full Stochastic RSI %D is < Bid')
  ask5 = TextField('Ask', default=config['Indicators']['Full Stochastic RSI %D']['Ask'],
                   description='Sell when Full Stochastic RSI %D is > Ask')
  tv11 = TextField('Trade Volume', description='Percentage of available asset and currency evaluated on each trade. 50 is 50%. Only used on an independent indicator. It is recommended to set this to a low value if SingleTrade is disabled.',
                   default=config['Indicators']['Full Stochastic RSI %D']['Trader']['Trade Volume'])
  st11 = BooleanField('Single Trade', description='Should we only do a single consecutive sell or buy? Only used on an independent indicator. This still uses TradeVolume percent on each trade. This is useful for MA style strategies, whereas oscillator or diff style should be set to False (to often continue selling if above threshold, or buying below).',
                      default=ast.literal_eval(config['Indicators']['Full Stochastic RSI %D']['Trader']['Single Trade']))
  tp11 = BooleanField('Trade Persist', description='Waits for a signal to persist two candles. Only used on an independent indicator.',
                      default=ast.literal_eval(config['Indicators']['Full Stochastic RSI %D']['Trader']['Trade Persist']))
  td11 = TextField('Trade Delay', description='Number of candles with indicator info before trading. Must be greater than 0. Only used on an independent indicator.',
                   default=config['Indicators']['Full Stochastic RSI %D']['Trader']['Trade Delay'])
  fullstochrsid_submit = SubmitField('Save')


class FastStochK(Form):
  period6 = TextField(
      'Period', default=config['Indicators']['Fast Stochastic %K']['Period'])
  bid6 = TextField('Bid', default=config['Indicators']['Fast Stochastic %K']['Bid'],
                   description='Buy when Fast Stochastic %K is < Bid')
  ask6 = TextField('Ask', default=config['Indicators']['Fast Stochastic %K']['Ask'],
                   description='Sell when Fast Stochastic %K is > Ask')
  tv12 = TextField('Trade Volume', description='Percentage of available asset and currency evaluated on each trade. 50 is 50%. Only used on an independent indicator. It is recommended to set this to a low value if SingleTrade is disabled.',
                   default=config['Indicators']['Fast Stochastic %K']['Trader']['Trade Volume'])
  st12 = BooleanField('Single Trade', description='Should we only do a single consecutive sell or buy? Only used on an independent indicator. This still uses TradeVolume percent on each trade. This is useful for MA style strategies, whereas oscillator or diff style should be set to False (to often continue selling if above threshold, or buying below).',
                      default=ast.literal_eval(config['Indicators']['Fast Stochastic %K']['Trader']['Single Trade']))
  tp12 = BooleanField('Trade Persist', description='Waits for a signal to persist two candles. Only used on an independent indicator.',
                      default=ast.literal_eval(config['Indicators']['Fast Stochastic %K']['Trader']['Trade Persist']))
  td12 = TextField('Trade Delay', description='Number of candles with indicator info before trading. Must be greater than 0. Only used on an independent indicator.',
                   default=config['Indicators']['Fast Stochastic %K']['Trader']['Trade Delay'])
  faststochk_submit = SubmitField('Save')


class FastStochD(Form):
  period7 = TextField(
      'Period', default=config['Indicators']['Fast Stochastic %D']['Period'])
  bid7 = TextField('Bid', default=config['Indicators']['Fast Stochastic %D']['Bid'],
                   description='Buy when Fast Stochastic %D is < Bid')
  ask7 = TextField('Ask', default=config['Indicators']['Fast Stochastic %D']['Ask'],
                   description='Sell when Fast Stochastic %D is > Ask')
  tv13 = TextField('Trade Volume', description='Percentage of available asset and currency evaluated on each trade. 50 is 50%. Only used on an independent indicator. It is recommended to set this to a low value if SingleTrade is disabled.',
                   default=config['Indicators']['Fast Stochastic %D']['Trader']['Trade Volume'])
  st13 = BooleanField('Single Trade', description='Should we only do a single consecutive sell or buy? Only used on an independent indicator. This still uses TradeVolume percent on each trade. This is useful for MA style strategies, whereas oscillator or diff style should be set to False (to often continue selling if above threshold, or buying below).',
                      default=ast.literal_eval(config['Indicators']['Fast Stochastic %D']['Trader']['Single Trade']))
  tp13 = BooleanField('Trade Persist', description='Waits for a signal to persist two candles. Only used on an independent indicator.',
                      default=ast.literal_eval(config['Indicators']['Fast Stochastic %D']['Trader']['Trade Persist']))
  td13 = TextField('Trade Delay', description='Number of candles with indicator info before trading. Must be greater than 0. Only used on an independent indicator.',
                   default=config['Indicators']['Fast Stochastic %D']['Trader']['Trade Delay'])
  faststochd_submit = SubmitField('Save')


class FullStochD(Form):
  period8 = TextField(
      'Period', default=config['Indicators']['Full Stochastic %D']['Period'])
  bid8 = TextField('Bid', default=config['Indicators']['Full Stochastic %D']['Bid'],
                   description='Buy when Full Stochastic %D is < Bid')
  ask8 = TextField('Ask', default=config['Indicators']['Full Stochastic %D']['Ask'],
                   description='Sell when Full Stochastic %D is > Ask')
  tv14 = TextField('Trade Volume', description='Percentage of available asset and currency evaluated on each trade. 50 is 50%. Only used on an independent indicator. It is recommended to set this to a low value if SingleTrade is disabled.',
                   default=config['Indicators']['Full Stochastic %D']['Trader']['Trade Volume'])
  st14 = BooleanField('Single Trade', description='Should we only do a single consecutive sell or buy? Only used on an independent indicator. This still uses TradeVolume percent on each trade. This is useful for MA style strategies, whereas oscillator or diff style should be set to False (to often continue selling if above threshold, or buying below).',
                      default=ast.literal_eval(config['Indicators']['Full Stochastic %D']['Trader']['Single Trade']))
  tp14 = BooleanField('Trade Persist', description='Waits for a signal to persist two candles. Only used on an independent indicator.',
                      default=ast.literal_eval(config['Indicators']['Full Stochastic %D']['Trader']['Trade Persist']))
  td14 = TextField('Trade Delay', description='Number of candles with indicator info before trading. Must be greater than 0. Only used on an independent indicator.',
                   default=config['Indicators']['Full Stochastic %D']['Trader']['Trade Delay'])
  fullstochd_submit = SubmitField('Save')


class KDJ(Form):
  indstr9 = SelectField('Indicator Strategy',
                        default=config['Indicators'][
                            'KDJ']['Indicator Strategy'],
                        choices=[
                            ('CD', 'Convergence/Divergence'), ('Diff', 'Difference')],
                        description='Convergence/Divergence trades on K/D convergence/divergence. Difference trades on the difference between J and Bid/Ask.')
  fastkperiod = TextField(
      'Fast K Period', default=config['Indicators']['KDJ']['Fast K Period'])
  fullkperiod = TextField(
      'Full K Period', default=config['Indicators']['KDJ']['Full K Period'])
  fulldperiod = TextField(
      'Full D Period', default=config['Indicators']['KDJ']['Full D Period'])
  bid9 = TextField('Bid', default=config['Indicators']['KDJ']['Bid'],
                   description='Only used on "Diff" (off J)')
  ask9 = TextField('Ask', default=config['Indicators']['KDJ']['Ask'],
                   description='Only used on "Diff" (off J)')
  tv15 = TextField('Trade Volume', description='Percentage of available asset and currency evaluated on each trade. 50 is 50%. Only used on an independent indicator. It is recommended to set this to a low value if SingleTrade is disabled.',
                   default=config['Indicators']['KDJ']['Trader']['Trade Volume'])
  st15 = BooleanField('Single Trade', description='Should we only do a single consecutive sell or buy? Only used on an independent indicator. This still uses TradeVolume percent on each trade. This is useful for MA style strategies, whereas oscillator or diff style should be set to False (to often continue selling if above threshold, or buying below).',
                      default=ast.literal_eval(config['Indicators']['KDJ']['Trader']['Single Trade']))
  tp15 = BooleanField('Trade Persist', description='Waits for a signal to persist two candles. Only used on an independent indicator.',
                      default=ast.literal_eval(config['Indicators']['KDJ']['Trader']['Trade Persist']))
  td15 = TextField('Trade Delay', description='Number of candles with indicator info before trading. Must be greater than 0. Only used on an independent indicator.',
                   default=config['Indicators']['KDJ']['Trader']['Trade Delay'])
  kdj_submit = SubmitField('Save')


class Ichimoku(Form):
  indstr10 = SelectField('Indicator Strategy', description='Check http://galts-gulch.github.io/avarice/indicators/#ichimoku-ichimoku-cloud for info on supported strategies.',
                         default=config['Indicators'][
                             'Ichimoku']['Indicator Strategy'],
                         choices=[('Strong', 'Strong'), ('Optimized', 'Optimized'),
                                  ('Weak', 'Weak'), ('CloudOnly', 'Cloud Only')])
  tsperiod = TextField(
      'Tenkan-Sen Period', default=config['Indicators']['Ichimoku']['Tenkan-Sen Period'])
  ssperiod = TextField('Senkou Span Period', default=config['Indicators']['Ichimoku']['Senkou Span Period'],
                       description='Default is 2 * Kijun-Sen Period')
  ksperiod = TextField(
      'Kijun-Sen Period', default=config['Indicators']['Ichimoku']['Kijun-Sen Period'])
  csperiod = TextField('Chikou Span Period', default=config['Indicators']['Ichimoku']['Chikou Span Period'],
                       description='Default is the same as Kijun-Sen Period')
  tv16 = TextField('Trade Volume', description='Percentage of available asset and currency evaluated on each trade. 50 is 50%. Only used on an independent indicator. It is recommended to set this to a low value if SingleTrade is disabled.',
                   default=config['Indicators']['Ichimoku']['Trader']['Trade Volume'])
  st16 = BooleanField('Single Trade', description='Should we only do a single consecutive sell or buy? Only used on an independent indicator. This still uses TradeVolume percent on each trade. This is useful for MA style strategies, whereas oscillator or diff style should be set to False (to often continue selling if above threshold, or buying below).',
                      default=ast.literal_eval(config['Indicators']['Ichimoku']['Trader']['Single Trade']))
  tp16 = BooleanField('Trade Persist', description='Waits for a signal to persist two candles. Only used on an independent indicator.',
                      default=ast.literal_eval(config['Indicators']['Ichimoku']['Trader']['Trade Persist']))
  td16 = TextField('Trade Delay', description='Number of candles with indicator info before trading. Must be greater than 0. Only used on an independent indicator.',
                   default=config['Indicators']['Ichimoku']['Trader']['Trade Delay'])
  ichimoku_submit = SubmitField('Save')


class StdDev(Form):
  period9 = TextField(
      'Period', default=config['Indicators']['Standard Deviation']['Period'])
  vto1 = BooleanField('Volatility Threshold Over', description='Support signals when indicator is above threshold',
                      default=ast.literal_eval(config['Indicators']['Standard Deviation']['Volatility Threshold Over']))
  thresh1 = TextField('Threshold',
                      default=config['Indicators']['Standard Deviation']['Threshold'])
  stddev_submit = SubmitField('Save')


class BollBands(Form):
  period10 = TextField(
      'Period', default=config['Indicators']['Bollinger Bands']['Period'])
  bollbands_submit = SubmitField('Save')


class BollingerBandwidth(Form):
  vto2 = BooleanField('Volatility Threshold Over', description='Support signals when indicator is above threshold',
                      default=ast.literal_eval(config['Indicators']['Bollinger Bandwidth']['Volatility Threshold Over']))
  thresh2 = TextField('Threshold',
                      default=config['Indicators']['Bollinger Bandwidth']['Threshold'])
  bollingerbandwidth_submit = SubmitField('Save')


class ATR(Form):
  period11 = TextField(
      'Period', default=config['Indicators']['Average True Range']['Period'])
  vto3 = BooleanField('Volatility Threshold Over', description='Support signals when indicator is above threshold',
                      default=ast.literal_eval(config['Indicators']['Average True Range']['Volatility Threshold Over']))
  thresh3 = TextField('Threshold',
                      default=config['Indicators']['Average True Range']['Threshold'])
  atr_submit = SubmitField('Save')


class ChandExit(Form):
  period12 = TextField(
      'Period', default=config['Indicators']['Chandelier Exit']['Period'])
  mult = TextField('Multiplier',
                   default=config['Indicators']['Chandelier Exit']['Multiplier'])
  tv17 = TextField('Trade Volume', description='Percentage of available asset and currency evaluated on each trade. 50 is 50%. Only used on an independent indicator. It is recommended to set this to a low value if SingleTrade is disabled.',
                   default=config['Indicators']['Chandelier Exit']['Trader']['Trade Volume'])
  st17 = BooleanField('Single Trade', description='Should we only do a single consecutive sell or buy? Only used on an independent indicator. This still uses TradeVolume percent on each trade. This is useful for MA style strategies, whereas oscillator or diff style should be set to False (to often continue selling if above threshold, or buying below).',
                      default=ast.literal_eval(config['Indicators']['Chandelier Exit']['Trader']['Single Trade']))
  tp17 = BooleanField('Trade Persist', description='Waits for a signal to persist two candles. Only used on an independent indicator.',
                      default=ast.literal_eval(config['Indicators']['Chandelier Exit']['Trader']['Trade Persist']))
  td17 = TextField('Trade Delay', description='Number of candles with indicator info before trading. Must be greater than 0. Only used on an independent indicator.',
                   default=config['Indicators']['Chandelier Exit']['Trader']['Trade Delay'])
  chandexit_submit = SubmitField('Save')


class DMI(Form):
  indstr11 = SelectField('Indicator Strategy', default=config['Indicators'][
                       'Directional Movement Index']['Indicator Strategy'],
                       choices=[('Volatility', 'Volatility'), ('Full', 'Full')],
                       description='Volatility uses ADX as a volatility indicator (only functional when combined with a non-volatility indicator). Full uses Threshold and +DI/-DI crossovers.')
  vto4 = BooleanField('Volatility Threshold Over', description='Support signals when indicator is above threshold',
                      default=ast.literal_eval(config['Indicators']['Directional Movement Index']['Volatility Threshold Over']))
  thresh4 = TextField('Threshold',
                      default=config['Indicators']['Directional Movement Index']['Threshold'])
  tv18 = TextField('Trade Volume', description='Percentage of available asset and currency evaluated on each trade. 50 is 50%. Only used on an independent indicator. It is recommended to set this to a low value if SingleTrade is disabled.',
                   default=config['Indicators']['Directional Movement Index']['Trader']['Trade Volume'])
  st18 = BooleanField('Single Trade', description='Should we only do a single consecutive sell or buy? Only used on an independent indicator. This still uses TradeVolume percent on each trade. This is useful for MA style strategies, whereas oscillator or diff style should be set to False (to often continue selling if above threshold, or buying below).',
                      default=ast.literal_eval(config['Indicators']['Directional Movement Index']['Trader']['Single Trade']))
  tp18 = BooleanField('Trade Persist', description='Waits for a signal to persist two candles. Only used on an independent indicator.',
                      default=ast.literal_eval(config['Indicators']['Directional Movement Index']['Trader']['Trade Persist']))
  td18 = TextField('Trade Delay', description='Number of candles with indicator info before trading. Must be greater than 0. Only used on an independent indicator.',
                   default=config['Indicators']['Directional Movement Index']['Trader']['Trade Delay'])
  dmi_submit = SubmitField('Save')


class SROC(Form):
  period13 = TextField(
      'Period', default=config['Indicators']['Simple Rate of Change']['Period'])
  tv19 = TextField('Trade Volume', description='Percentage of available asset and currency evaluated on each trade. 50 is 50%. Only used on an independent indicator. It is recommended to set this to a low value if SingleTrade is disabled.',
                   default=config['Indicators']['Simple Rate of Change']['Trader']['Trade Volume'])
  st19 = BooleanField('Single Trade', description='Should we only do a single consecutive sell or buy? Only used on an independent indicator. This still uses TradeVolume percent on each trade. This is useful for MA style strategies, whereas oscillator or diff style should be set to False (to often continue selling if above threshold, or buying below).',
                      default=ast.literal_eval(config['Indicators']['Simple Rate of Change']['Trader']['Single Trade']))
  tp19 = BooleanField('Trade Persist', description='Waits for a signal to persist two candles. Only used on an independent indicator.',
                      default=ast.literal_eval(config['Indicators']['Simple Rate of Change']['Trader']['Trade Persist']))
  td19 = TextField('Trade Delay', description='Number of candles with indicator info before trading. Must be greater than 0. Only used on an independent indicator.',
                   default=config['Indicators']['Simple Rate of Change']['Trader']['Trade Delay'])
  sroc_submit = SubmitField('Save')


def create_app():
  app = Flask(__name__)
  Bootstrap(app)

  app.config['SECRET_KEY'] = 'devkey'

  @app.route('/', methods=('GET', 'POST'))
  def index():
    return render_template('configuration.html')

  @app.route('/configuration_api', methods=('GET', 'POST'))
  def configuration_api():
    form1 = API()
    if form1.validate_on_submit():
      config['API']['Verbose'] = form1.verbose.data
      config['API']['Exchange'] = form1.exchange.data
      config['API']['Trade Pair'] = form1.tradepair.data
      config['API']['API Key'] = form1.apikey.data
      config['API']['Secret Key'] = form1.secretkey.data
      config['API']['Asset Trade Minimum'] = form1.trademin.data
      config.write()
    return render_template('configuration_api.html', form=form1)

  @app.route('/configuration_candles', methods=('GET', 'POST'))
  def configuration_candles():
    form2 = Candles()
    if form2.validate_on_submit():
      config['Candles']['Verbose'] = form2.verbose.data
      config['Candles']['Size'] = form2.size.data
      config.write()
    return render_template('configuration_candles.html', form=form2)

  @app.route('/configuration_trader', methods=('GET', 'POST'))
  def configuration_trader():
    form3 = Trader()
    if form3.validate_on_submit():
      config['Trader']['Enabled'] = form3.enabled.data
      config['Trader']['Verbose'] = form3.verbose.data
      config['Trader']['Trade Indicators'] = form3.tradeindicators.data
      config['Trader']['Verbose Indicators'] = form3.verboseindicators.data
      config['Trader']['Advanced Strategy'] = form3.advancedstrategy.data
      config['Trader']['Trade Volume'] = form3.tradevolume.data
      config['Trader']['Single Trade'] = form3.singletrade.data
      config['Trader']['Trade Persist'] = form3.tradepersist.data
      config['Trader']['Trade Delay'] = form3.tradedelay.data
      config['Trader']['ReIssue Slippage'] = form3.reissueslippage.data
      config['Trader']['ReIssue Delay'] = form3.reissuedelay.data
      config.write()
    return render_template('configuration_trader.html', form=form3)

  @app.route('/configuration_simulator', methods=('GET', 'POST'))
  def configuration_simulator():
    form4 = Simulator()
    if form4.validate_on_submit():
      config['Simulator']['Verbose'] = form4.verbose.data
      config['Simulator']['Asset'] = form4.asset.data
      config['Simulator']['Currency'] = form4.currency.data
      config.write()
    return render_template('configuration_simulator.html', form=form4)

  @app.route('/configuration_notifier', methods=('GET', 'POST'))
  def configuration_textfile():
    form5 = TextFile()
    if form5.textfile_submit.data:
      config['Notifier']['Text File']['Rollover Time'] = form5.rollover.data
      config['Notifier']['Text File']['Backup Count'] = form5.backup.data
      config['Notifier']['Text File']['Path'] = form5.path1.data
      config['Notifier']['Text File'][
          'Trader File Name'] = form5.tfilename.data
      config['Notifier']['Text File'][
          'Simulator File Name'] = form5.sfilename.data
      config.write()
    return render_template('configuration_textfile.html', form=form5)

  @app.route('/configuration_pushover', methods=('GET', 'POST'))
  def configuration_pushover():
    form6 = Pushover()
    if form6.pushover_submit.data:
      config['Notifier']['Pushover']['Simulator'] = form6.simulator.data
      config['Notifier']['Pushover']['Trader'] = form6.trader.data
      config['Notifier']['Pushover']['App Token'] = form6.app.data
      config['Notifier']['Pushover']['User Key'] = form6.user.data
      config.write()
    return render_template('configuration_pushover.html', form=form6)

  @app.route('/configuration_smtp', methods=('GET', 'POST'))
  def configuration_smtp():
    form7 = SMTP()
    if form7.smtp_submit.data:
      config['Notifier']['SMTP']['Simulator'] = form7.simulator.data
      config['Notifier']['SMTP']['Trader'] = form7.trader.data
      config['Notifier']['SMTP']['Host'] = form7.host.data
      config['Notifier']['SMTP']['From'] = form7.From.data
      config['Notifier']['SMTP']['To'] = form7.to.data
      config.write()
    return render_template('configuration_smtp.html', form=form7)

  @app.route('/configuration_tlssmtp', methods=('GET', 'POST'))
  def configuration_tlssmtp():
    form8 = TLSSMTP()
    if form8.tlssmtp_submit.data:
      config['Notifier']['TLS SMTP']['Simulator'] = form8.simulator.data
      config['Notifier']['TLS SMTP']['Trader'] = form8.trader.data
      config['Notifier']['TLS SMTP']['Host'] = form8.host.data
      config['Notifier']['TLS SMTP']['Port'] = form8.port.data
      config['Notifier']['TLS SMTP']['Username'] = form8.user.data
      config['Notifier']['TLS SMTP']['Password'] = form8.passw.data
      config['Notifier']['TLS SMTP']['To'] = form8.to.data
      config.write()
    return render_template('configuration_tlssmtp.html', form=form8)

  @app.route('/configuration_database', methods=('GET', 'POST'))
  def configuration_database():
    form9 = Database()
    if form9.validate_on_submit():
      config['Database']['Store All'] = form9.store.data
      config['Database']['Debug'] = form9.debug.data
      config['Database']['Path'] = form9.path2.data
      config.write()
    return render_template('configuration_database.html', form=form9)

  @app.route('/configuration_grapher', methods=('GET', 'POST'))
  def configuration_grapher():
    form10 = Grapher()
    if form10.validate_on_submit():
      config['Grapher']['Enabled'] = form10.enabled.data
      config['Grapher']['Show Time'] = form10.stime.data
      config['Grapher']['Path'] = form10.path3.data
      config['Grapher']['Theme'] = form10.theme.data
      config['Grapher']['Max Lookback'] = form10.look.data
      config.write()
    return render_template('configuration_grapher.html', form=form10)

  @app.route('/configuration_sma', methods=('GET', 'POST'))
  def configuration_sma():
    form11 = SMA()
    if form11.validate_on_submit():
      config['Indicators']['SMA']['Indicator Strategy'] = form11.indstr1.data
      config['Indicators']['SMA']['Short Period'] = form11.sp1.data
      config['Indicators']['SMA']['Long Period'] = form11.lp1.data
      config['Indicators']['SMA']['Diff Down'] = form11.dd1.data
      config['Indicators']['SMA']['Diff Up'] = form11.du1.data
      config['Indicators']['SMA']['Trader']['Trade Volume'] = form11.tv1.data
      config['Indicators']['SMA']['Trader']['Single Trade'] = form11.st1.data
      config['Indicators']['SMA']['Trader']['Trade Persist'] = form11.tp1.data
      config['Indicators']['SMA']['Trader']['Trade Delay'] = form11.td1.data
      config.write()
    return render_template('configuration_sma.html', form=form11)

  @app.route('/configuration_ema', methods=('GET', 'POST'))
  def configuration_ema():
    form12 = EMA()
    if form12.validate_on_submit():
      config['Indicators']['EMA']['Indicator Strategy'] = form12.indstr2.data
      config['Indicators']['EMA']['Short Period'] = form12.sp2.data
      config['Indicators']['EMA']['Long Period'] = form12.lp2.data
      config['Indicators']['EMA']['Diff Down'] = form12.dd2.data
      config['Indicators']['EMA']['Diff Up'] = form12.du2.data
      config['Indicators']['EMA']['Trader']['Trade Volume'] = form12.tv2.data
      config['Indicators']['EMA']['Trader']['Single Trade'] = form12.st2.data
      config['Indicators']['EMA']['Trader']['Trade Persist'] = form12.tp2.data
      config['Indicators']['EMA']['Trader']['Trade Delay'] = form12.td2.data
      config.write()
    return render_template('configuration_ema.html', form=form12)

  @app.route('/configuration_dema', methods=('GET', 'POST'))
  def configuration_dema():
    form13 = DEMA()
    if form13.validate_on_submit():
      config['Indicators']['DEMA']['Indicator Strategy'] = form13.indstr3.data
      config['Indicators']['DEMA']['Diff Down'] = form13.dd3.data
      config['Indicators']['DEMA']['Diff Up'] = form13.du3.data
      config['Indicators']['DEMA']['Trader']['Trade Volume'] = form13.tv3.data
      config['Indicators']['DEMA']['Trader']['Single Trade'] = form13.st3.data
      config['Indicators']['DEMA']['Trader']['Trade Persist'] = form13.tp3.data
      config['Indicators']['DEMA']['Trader']['Trade Delay'] = form13.td3.data
      config.write()
    return render_template('configuration_dema.html', form=form13)

  @app.route('/configuration_emawbic', methods=('GET', 'POST'))
  def configuration_emawbic():
    form14 = EMAwbic()
    if form14.validate_on_submit():
      config['Indicators']['EMAwbic']['Period'] = form14.period1.data
      config['Indicators']['EMAwbic']['Bid'] = form14.bid1.data
      config['Indicators']['EMAwbic']['Ask'] = form14.ask1.data
      config['Indicators']['EMAwbic']['Trader'][
          'Trade Volume'] = form14.tv4.data
      config['Indicators']['EMAwbic']['Trader'][
          'Single Trade'] = form14.st4.data
      config['Indicators']['EMAwbic']['Trader'][
          'Trade Persist'] = form14.tp4.data
      config['Indicators']['EMAwbic']['Trader'][
          'Trade Delay'] = form14.td4.data
      config.write()
    return render_template('configuration_emawbic.html', form=form14)

  @app.route('/configuration_frama', methods=('GET', 'POST'))
  def configuration_frama():
    form15 = FRAMA()
    if form15.validate_on_submit():
      config['Indicators']['FRAMA']['Indicator Strategy'] = form15.indstr5.data
      config['Indicators']['FRAMA']['Short Period'] = form15.sp5.data
      config['Indicators']['FRAMA']['Long Period'] = form15.lp5.data
      config['Indicators']['FRAMA']['Alpha Constant'] = form15.ac.data
      config['Indicators']['FRAMA']['Diff Down'] = form15.dd5.data
      config['Indicators']['FRAMA']['Diff Up'] = form15.du5.data
      config['Indicators']['FRAMA']['Trader']['Trade Volume'] = form15.tv5.data
      config['Indicators']['FRAMA']['Trader']['Single Trade'] = form15.st5.data
      config['Indicators']['FRAMA']['Trader'][
          'Trade Persist'] = form15.tp5.data
      config['Indicators']['FRAMA']['Trader']['Trade Delay'] = form15.td5.data
      config.write()
    return render_template('configuration_frama.html', form=form15)

  @app.route('/configuration_macd', methods=('GET', 'POST'))
  def configuration_macd():
    form16 = MACD()
    if form16.validate_on_submit():
      config['Indicators']['MACD']['Indicator Strategy'] = form16.indstr6.data
      config['Indicators']['MACD']['Short Period'] = form16.sp6.data
      config['Indicators']['MACD']['Long Period'] = form16.lp6.data
      config['Indicators']['MACD']['Signal Period'] = form16.sig1.data
      config['Indicators']['MACD']['Diff Down'] = form16.dd6.data
      config['Indicators']['MACD']['Diff Up'] = form16.du6.data
      config['Indicators']['MACD']['Trader']['Trade Volume'] = form16.tv6.data
      config['Indicators']['MACD']['Trader']['Single Trade'] = form16.st6.data
      config['Indicators']['MACD']['Trader']['Trade Persist'] = form16.tp6.data
      config['Indicators']['MACD']['Trader']['Trade Delay'] = form16.td6.data
      config.write()
    return render_template('configuration_macd.html', form=form16)

  @app.route('/configuration_dmacd', methods=('GET', 'POST'))
  def configuration_dmacd():
    form17 = DMACD()
    if form17.validate_on_submit():
      config['Indicators']['DMACD']['Indicator Strategy'] = form17.indstr7.data
      config['Indicators']['DMACD']['Signal Period'] = form17.sig2.data
      config['Indicators']['DMACD']['Diff Down'] = form17.dd7.data
      config['Indicators']['DMACD']['Diff Up'] = form17.du7.data
      config['Indicators']['DMACD']['Trader']['Trade Volume'] = form17.tv7.data
      config['Indicators']['DMACD']['Trader']['Single Trade'] = form17.st7.data
      config['Indicators']['DMACD']['Trader'][
          'Trade Persist'] = form17.tp7.data
      config['Indicators']['DMACD']['Trader']['Trade Delay'] = form17.td7.data
      config.write()
    return render_template('configuration_dmacd.html', form=form17)

  @app.route('/configuration_rsi', methods=('GET', 'POST'))
  def configuration_rsi():
    form18 = RSI()
    if form18.validate_on_submit():
      config['Indicators']['RSI']['Period'] = form18.period2.data
      config['Indicators']['RSI']['Ask'] = form18.ask2.data
      config['Indicators']['RSI']['Bid'] = form18.bid2.data
      config['Indicators']['RSI']['Trader']['Trade Volume'] = form18.tv8.data
      config['Indicators']['RSI']['Trader']['Single Trade'] = form18.st8.data
      config['Indicators']['RSI']['Trader']['Trade Persist'] = form18.tp8.data
      config['Indicators']['RSI']['Trader']['Trade Delay'] = form18.td8.data
      config.write()
    return render_template('configuration_rsi.html', form=form18)

  @app.route('/configuration_faststochrsik', methods=('GET', 'POST'))
  def configuration_faststochrsik():
    form19 = FastStochRSIK()
    if form19.validate_on_submit():
      config['Indicators']['Fast Stochastic RSI %K'][
          'Period'] = form19.period3.data
      config['Indicators']['Fast Stochastic RSI %K']['Ask'] = form19.ask3.data
      config['Indicators']['Fast Stochastic RSI %K']['Bid'] = form19.bid3.data
      config['Indicators']['Fast Stochastic RSI %K'][
          'Trader']['Trade Volume'] = form19.tv9.data
      config['Indicators']['Fast Stochastic RSI %K'][
          'Trader']['Single Trade'] = form19.st9.data
      config['Indicators']['Fast Stochastic RSI %K'][
          'Trader']['Trade Persist'] = form19.tp9.data
      config['Indicators']['Fast Stochastic RSI %K'][
          'Trader']['Trade Delay'] = form19.td9.data
      config.write()
    return render_template('configuration_faststochrsik.html', form=form19)

  @app.route('/configuration_faststochrsid', methods=('GET', 'POST'))
  def configuration_faststochrsid():
    form20 = FastStochRSID()
    if form20.validate_on_submit():
      config['Indicators']['Fast Stochastic RSI %D'][
          'Period'] = form20.period4.data
      config['Indicators']['Fast Stochastic RSI %D']['Ask'] = form20.ask4.data
      config['Indicators']['Fast Stochastic RSI %D']['Bid'] = form20.bid4.data
      config['Indicators']['Fast Stochastic RSI %D'][
          'Trader']['Trade Volume'] = form20.tv10.data
      config['Indicators']['Fast Stochastic RSI %D'][
          'Trader']['Single Trade'] = form20.st10.data
      config['Indicators']['Fast Stochastic RSI %D'][
          'Trader']['Trade Persist'] = form20.tp10.data
      config['Indicators']['Fast Stochastic RSI %D'][
          'Trader']['Trade Delay'] = form20.td10.data
      config.write()
    return render_template('configuration_faststochrsid.html', form=form20)

  @app.route('/configuration_fullstochrsid', methods=('GET', 'POST'))
  def configuration_fullstochrsid():
    form21 = FullStochRSID()
    if form21.validate_on_submit():
      config['Indicators']['Full Stochastic RSI %D'][
          'Period'] = form21.period5.data
      config['Indicators']['Full Stochastic RSI %D']['Ask'] = form21.ask5.data
      config['Indicators']['Full Stochastic RSI %D']['Bid'] = form21.bid5.data
      config['Indicators']['Full Stochastic RSI %D'][
          'Trader']['Trade Volume'] = form21.tv11.data
      config['Indicators']['Full Stochastic RSI %D'][
          'Trader']['Single Trade'] = form21.st11.data
      config['Indicators']['Full Stochastic RSI %D'][
          'Trader']['Trade Persist'] = form21.tp11.data
      config['Indicators']['Full Stochastic RSI %D'][
          'Trader']['Trade Delay'] = form21.td11.data
      config.write()
    return render_template('configuration_fullstochrsid.html', form=form21)

  @app.route('/configuration_faststochk', methods=('GET', 'POST'))
  def configuration_faststochk():
    form22 = FastStochK()
    if form22.validate_on_submit():
      config['Indicators']['Fast Stochastic %K'][
          'Period'] = form22.period6.data
      config['Indicators']['Fast Stochastic %K']['Ask'] = form22.ask6.data
      config['Indicators']['Fast Stochastic %K']['Bid'] = form22.bid6.data
      config['Indicators']['Fast Stochastic %K'][
          'Trader']['Trade Volume'] = form22.tv12.data
      config['Indicators']['Fast Stochastic %K'][
          'Trader']['Single Trade'] = form22.st12.data
      config['Indicators']['Fast Stochastic %K'][
          'Trader']['Trade Persist'] = form22.tp12.data
      config['Indicators']['Fast Stochastic %K'][
          'Trader']['Trade Delay'] = form22.td12.data
      config.write()
    return render_template('configuration_faststochk.html', form=form22)

  @app.route('/configuration_faststochd', methods=('GET', 'POST'))
  def configuration_faststochd():
    form23 = FastStochD()
    if form23.validate_on_submit():
      config['Indicators']['Fast Stochastic %D'][
          'Period'] = form23.period7.data
      config['Indicators']['Fast Stochastic %D']['Ask'] = form23.ask7.data
      config['Indicators']['Fast Stochastic %D']['Bid'] = form23.bid7.data
      config['Indicators']['Fast Stochastic %D'][
          'Trader']['Trade Volume'] = form23.tv13.data
      config['Indicators']['Fast Stochastic %D'][
          'Trader']['Single Trade'] = form23.st13.data
      config['Indicators']['Fast Stochastic %D'][
          'Trader']['Trade Persist'] = form23.tp13.data
      config['Indicators']['Fast Stochastic %D'][
          'Trader']['Trade Delay'] = form23.td13.data
      config.write()
    return render_template('configuration_faststochd.html', form=form23)

  @app.route('/configuration_fullstochd', methods=('GET', 'POST'))
  def configuration_fullstochd():
    form24 = FullStochD()
    if form24.validate_on_submit():
      config['Indicators']['Full Stochastic %D'][
          'Period'] = form24.period8.data
      config['Indicators']['Full Stochastic %D']['Ask'] = form24.ask8.data
      config['Indicators']['Full Stochastic %D']['Bid'] = form24.bid8.data
      config['Indicators']['Full Stochastic %D'][
          'Trader']['Trade Volume'] = form24.tv14.data
      config['Indicators']['Full Stochastic %D'][
          'Trader']['Single Trade'] = form24.st14.data
      config['Indicators']['Full Stochastic %D'][
          'Trader']['Trade Persist'] = form24.tp14.data
      config['Indicators']['Full Stochastic %D'][
          'Trader']['Trade Delay'] = form24.td14.data
      config.write()
    return render_template('configuration_fullstochd.html', form=form24)

  @app.route('/configuration_kdj', methods=('GET', 'POST'))
  def configuration_kdj():
    form25 = KDJ()
    if form25.validate_on_submit():
      config['Indicators']['KDJ']['Indicator Strategy'] = form25.indstr9.data
      config['Indicators']['KDJ']['Fast K Period'] = form25.fastkperiod.data
      config['Indicators']['KDJ']['Full K Period'] = form25.fullkperiod.data
      config['Indicators']['KDJ']['Full D Period'] = form25.fulldperiod.data
      config['Indicators']['KDJ']['Trader']['Trade Volume'] = form25.tv15.data
      config['Indicators']['KDJ']['Trader']['Single Trade'] = form25.st15.data
      config['Indicators']['KDJ']['Trader']['Trade Persist'] = form25.tp15.data
      config['Indicators']['KDJ']['Trader']['Trade Delay'] = form25.td15.data
      config.write()
    return render_template('configuration_kdj.html', form=form25)

  @app.route('/configuration_ichimoku', methods=('GET', 'POST'))
  def configuration_ichimoku():
    form26 = Ichimoku()
    if form26.validate_on_submit():
      config['Indicators']['Ichimoku'][
          'Indicator Strategy'] = form26.indstr10.data
      config['Indicators']['Ichimoku'][
          'Tenkan-Sen Period'] = form26.tsperiod.data
      config['Indicators']['Ichimoku'][
          'Senkou Span Period'] = form26.ssperiod.data
      config['Indicators']['Ichimoku'][
          'Kijun-Sen Period'] = form26.ksperiod.data
      config['Indicators']['Ichimoku'][
          'Chikou Span Period'] = form26.csperiod.data
      config['Indicators']['Ichimoku']['Trader'][
          'Trade Volume'] = form26.tv16.data
      config['Indicators']['Ichimoku']['Trader'][
          'Single Trade'] = form26.st16.data
      config['Indicators']['Ichimoku']['Trader'][
          'Trade Persist'] = form26.tp16.data
      config['Indicators']['Ichimoku']['Trader'][
          'Trade Delay'] = form26.td16.data
      config.write()
    return render_template('configuration_ichimoku.html', form=form26)

  @app.route('/configuration_stddev', methods=('GET', 'POST'))
  def configuration_stddev():
    form27 = StdDev()
    if form27.validate_on_submit():
      config['Indicators']['Standard Deviation'][
          'Volatility Threshold Over'] = form27.vto1.data
      config['Indicators']['Standard Deviation'][
          'Period'] = form27.period9.data
      config['Indicators']['Standard Deviation'][
          'Threshold'] = form27.thresh1.data
      config.write()
    return render_template('configuration_stddev.html', form=form27)

  @app.route('/configuration_bollbands', methods=('GET', 'POST'))
  def configuration_bollbands():
    form28 = BollBands()
    if form28.validate_on_submit():
      config['Indicators']['Bollinger Bands']['Period'] = form28.period10.data
      config.write()
    return render_template('configuration_bollbands.html', form=form28)

  @app.route('/configuration_bollingerbandwidth', methods=('GET', 'POST'))
  def configuration_bollingerbandwidth():
    form29 = BollingerBandwidth()
    if form29.validate_on_submit():
      config['Indicators']['Bollinger Bandwidth'][
          'Volatility Threshold Over'] = form29.vto2.data
      config['Indicators']['Bollinger Bandwidth'][
          'Threshold'] = form29.thresh2.data
      config.write()
    return render_template('configuration_bollingerbandwidth.html', form=form29)

  @app.route('/configuration_atr', methods=('GET', 'POST'))
  def configuration_atr():
    form30 = ATR()
    if form30.validate_on_submit():
      config['Indicators']['Average True Range'][
          'Period'] = form30.period11.data
      config['Indicators']['Average True Range'][
          'Volatility Threshold Over'] = form30.vto3.data
      config['Indicators']['Average True Range'][
          'Threshold'] = form30.thresh3.data
      config.write()
    return render_template('configuration_atr.html', form=form30)

  @app.route('/configuration_chandexit', methods=('GET', 'POST'))
  def configuration_chandexit():
    form31 = ChandExit()
    if form31.validate_on_submit():
      config['Indicators']['Chandelier Exit']['Period'] = form31.period12.data
      config['Indicators']['Chandelier Exit']['Multiplier'] = form31.mult.data
      config['Indicators']['Chandelier Exit'][
          'Trader']['Trade Volume'] = form31.tv17.data
      config['Indicators']['Chandelier Exit'][
          'Trader']['Single Trade'] = form31.st17.data
      config['Indicators']['Chandelier Exit'][
          'Trader']['Trade Persist'] = form31.tp17.data
      config['Indicators']['Chandelier Exit'][
          'Trader']['Trade Delay'] = form31.td17.data
      config.write()
    return render_template('configuration_chandexit.html', form=form31)

  @app.route('/configuration_dmi', methods=('GET', 'POST'))
  def configuration_dmi():
    form32 = DMI()
    if form32.validate_on_submit():
      config['Indicators']['Directional Movement Index'][
          'Indicator Strategy'] = form32.indstr11.data
      config['Indicators']['Directional Movement Index'][
          'Volatility Threshold Over'] = form32.vto4.data
      config['Indicators']['Directional Movement Index'][
          'Threshold'] = form32.thresh4.data
      config['Indicators']['Directional Movement Index'][
          'Trader']['Trade Volume'] = form32.tv18.data
      config['Indicators']['Directional Movement Index'][
          'Trader']['Single Trade'] = form32.st18.data
      config['Indicators']['Directional Movement Index'][
          'Trader']['Trade Persist'] = form32.tp18.data
      config['Indicators']['Directional Movement Index'][
          'Trader']['Trade Delay'] = form32.td18.data
      config.write()
    return render_template('configuration_dmi.html', form=form32)

  @app.route('/configuration_sroc', methods=('GET', 'POST'))
  def configuration_sroc():
    form33 = SROC()
    if form33.validate_on_submit():
      config['Indicators']['Simple Rate of Change'][
          'Period'] = form33.period13.data
      config['Indicators']['Simple Rate of Change'][
          'Trader']['Trade Volume'] = form33.tv19.data
      config['Indicators']['Simple Rate of Change'][
          'Trader']['Single Trade'] = form33.st19.data
      config['Indicators']['Simple Rate of Change'][
          'Trader']['Trade Persist'] = form33.tp19.data
      config['Indicators']['Simple Rate of Change'][
          'Trader']['Trade Delay'] = form33.td19.data
      config.write()
    return render_template('configuration_sroc.html', form=form33)

  return app

if __name__ == '__main__':
  create_app().run(debug=True)
