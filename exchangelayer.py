import asyncio
import json
import time

import avarice
import genconfig as gc

# Want to add support for a new exchange? Check docs/Contributing.md

if gc.API.Exchange == 'okcoin':
  from okcoin.WebSocketAPI import OKCoinWSPublic

  okwspub = OKCoinWSPublic(gc.API.TradePair, gc.API.Verbose)

  # Runs forever
  AdditionalAsync = [okwspub.initialize()]

  if gc.Trader.Enabled:
    from okcoin.WebSocketAPI import OKCoinWSPrivate
    okwspriv = OKCoinWSPrivate(
        gc.API.TradePair, gc.API.Verbose, gc.API.apikey, gc.API.secretkey)

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
          okwspriv.userinfo())[-1]['data']['info']['funds']['free'][gc.API.Currency]
    elif security == 'asset':
      Free = json.loads(
          okwspriv.userinfo())[-1]['data']['info']['funds']['free'][gc.API.Asset]
    return float(Free)

  def GetFrozen(security):
    if security == 'currency':
      Frozen = json.loads(
          okwspriv.userinfo())[-1]['data']['info']['funds']['freezed'][gc.API.Currency]
    elif security == 'asset':
      Frozen = json.loads(
          okwspriv.userinfo())[-1]['data']['info']['funds']['freezed'][gc.API.Asset]
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
