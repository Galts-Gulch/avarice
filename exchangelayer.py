import ast
import json

from storage import config

# Want to add support for a new exchange? Check docs/Contributing.md

# Ensure we have populated our config list
conf = config()

if config.gc['API']['Exchange'] == 'okcoin':
  from okcoin.WebSocketAPI import OKCoinWSPublic

  okwspub = OKCoinWSPublic(config.gc['API']['Trade Pair'], ast.literal_eval(
      config.gc['API']['Verbose']), int(config.gc['API']['Reconnect Wait']))

  # Runs forever
  AdditionalAsync = [okwspub.initialize()]

  if ast.literal_eval(config.gc['Trader']['Enabled']):
    from okcoin.WebSocketAPI import OKCoinWSPrivate
    okwspriv = OKCoinWSPrivate(config.gc['API']['Trade Pair'],
                               ast.literal_eval(config.gc['API']['Verbose']),
                               config.gc['API']['API Key'],
                               config.gc['API']['Secret Key'])

  def GetMarketPrice(pricetype):
    if OKCoinWSPublic.Ticker is not None:
      if pricetype == 'bid':
        Price = json.loads(str(OKCoinWSPublic.Ticker))[-1]['data']['buy']
      elif pricetype == 'ask':
        Price = json.loads(str(OKCoinWSPublic.Ticker))[-1]['data']['sell']
      elif pricetype == 'last':
        Price = json.loads(str(OKCoinWSPublic.Ticker))[-1]['data']['last']
      return float(Price)

  def GetFree(security):
    if security == 'currency':
      Free = json.loads(
          okwspriv.userinfo())[-1]['data']['info']['funds']['free'][config.gc[
              'API']['Trade Pair'][-3:]]
    elif security == 'asset':
      Free = json.loads(
          okwspriv.userinfo())[-1]['data']['info']['funds']['free'][config.gc[
              'API']['Trade Pair'][:3]]
    return float(Free)

  def GetFrozen(security):
    if security == 'currency':
      Frozen = json.loads(
          okwspriv.userinfo())[-1]['data']['info']['funds']['freezed'][config.gc[
              'API']['Trade Pair'][-3:]]
    elif security == 'asset':
      Frozen = json.loads(
          okwspriv.userinfo())[-1]['data']['info']['funds']['freezed'][config.gc[
              'API']['Trade Pair'][:3]]
    return float(Frozen)

  def OrderExist():
    # NOTE: occasionally OKCoin has a bug that reports FrozenCurrency
    # as up to 0.0009 across accounts.
    if GetFrozen('asset') > 0 or GetFrozen('currency') > 0.003:
      return True
    else:
      return False

  def Trade(order, rate, amount):
    okwspriv.trade(order, rate, amount)

  def CancelLastOrderIfExist():
    okwspriv.cancelorder(okwspriv.TradeOrderID)
