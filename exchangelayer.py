import asyncio
import json
import time

import avarice
import genconfig as gc

# Want to add support for a new exchange? Check docs/Contributing.md

if gc.API.Exchange == 'okcoin':
  from okcoin.OkcoinSpotAPI import OKCoinSpot
  from okcoin.WebSocketAPI import OKCoinWS

  if gc.API.Currency == 'usd':
    okcoinSpot = OKCoinSpot('www.okcoin.com', gc.API.apikey, gc.API.secretkey)
    okws = OKCoinWS("wss://real.okcoin.com:10440/websocket/okcoinapi")
  else:
    okcoinSpot = OKCoinSpot('www.okcoin.cn', gc.API.apikey, gc.API.secretkey)
    okws = OKCoinWS("wss://real.okcoin.cn:10440/websocket/okcoinapi")

  AdditionalAsync = [okws.initialize(gc.API.TradePair)]

  def GetMarketPrice(order):
    # json.loads(self.ws.recv())[-1]['data']['sell']
    if OKCoinWS.Ticker is not None:
      if order == 'bid':
        Price = json.loads(str(OKCoinWS.Ticker))[-1]['data']['buy']
      elif order == 'ask':
        Price = json.loads(str(OKCoinWS.Ticker))[-1]['data']['sell']
      return float(Price)

  def GetFree(security):
    if security == 'currency':
      time.sleep(gc.API.APIWait)
      Free = json.loads(okcoinSpot.userinfo())['info'][
          'funds']['free'][gc.API.Currency]
    elif security == 'asset':
      time.sleep(gc.API.APIWait)
      Free = json.loads(okcoinSpot.userinfo())['info'][
          'funds']['free'][gc.API.Asset]
    return float(Free)

  def GetFrozen(security):
    if security == 'currency':
      time.sleep(gc.API.APIWait)
      Frozen = json.loads(okcoinSpot.userinfo())['info'][
          'funds']['freezed'][gc.API.Currency]
    elif security == 'asset':
      time.sleep(gc.API.APIWait)
      Frozen = json.loads(okcoinSpot.userinfo())['info'][
          'funds']['freezed'][gc.API.Asset]
    return float(Frozen)

  def GetTradeAmount(security):
    if security == 'currency':
      Amount = (gc.Trader.TradeVolume / 100) * GetFree('currency')
    elif security == 'asset':
      Amount = (gc.Trader.TradeVolume / 100) * GetFree('asset')
    return Amount

  def OrderExist():
    # NOTE: occasionally OKCoin has a bug that reports FrozenCurrency
    # as up to 0.0009 across accounts.
    if GetFrozen('asset') > 0 or GetFrozen('currency') > 0.003:
      return True
    else:
      return False

  def CancelLastOrderIfExist():
    if OrderExist():
      try:
        LastOrderID = json.loads(okcoinSpot.orderHistory(
            gc.API.TradePair, '0', '1', '2'))['orders'][0]['order_id']
        time.sleep(gc.API.APIWait)
        try:
          okcoinSpot.cancelOrder(gc.API.TradePair, LastOrderID)
          time.sleep(gc.API.APIWait)
        except Exception:
          print('Order cancel failed! Did you manually remove the order?')
      except IndexError:
        print('Order just completed, can no longer cancel')

  def Trade(order, rate, amount):
    okcoinSpot.trade(gc.API.TradePair, order, rate, amount)
