import time

import genconfig as gc

# Want to add support for a new exchange? Check docs/Contributing.md

if gc.API.Exchange == 'okcoin':
  import okcoin_api

  if gc.API.Currency == 'usd':
    urlpre = 'https://www.okcoin.com/'
  else:
    urlpre = 'https://www.okcoin.cn/'

  Market = okcoin_api.MarketData()
  if gc.Trader.Enabled:
    TradeAPI = okcoin_api.TradeAPI(
        gc.API.partner, gc.API.secret_key)

  def GetFree(security):
    if security == 'currency':
      time.sleep(gc.API.APIWait)
      Free = TradeAPI.get_info()['info']['funds']['free']\
          [gc.API.Currency]
    elif security == 'asset':
      time.sleep(gc.API.APIWait)
      Free = TradeAPI.get_info()['info']['funds']['free']\
          [gc.API.Asset]
    return Free

  def GetFrozen(security):
    if security == 'currency':
      time.sleep(gc.API.APIWait)
      Frozen = TradeAPI.get_info()['info']['funds']['freezed'][
          gc.API.Currency]
    elif security == 'asset':
      time.sleep(gc.API.APIWait)
      Frozen = TradeAPI.get_info()['info']['funds']['freezed'][
          gc.API.Asset]
    return Frozen

  def GetTradeAmount(security):
    if security == 'currency':
      Amount = (gc.Trader.TradeVolume / 100) * \
          float(GetFree('currency'))
    elif security == 'asset':
      Amount = (gc.Trader.TradeVolume / 100) * \
          float(GetFree('asset'))
    return Amount

  def GetMarketPrice(order):
    if order == 'bid':
      Price = Market.ticker(gc.API.TradePair).bid
    elif order == 'ask':
      Price = Market.ticker(gc.API.TradePair).ask
    return Price

  def OrderExist():
    # NOTE: occasionally OKCoin has a bug that reports FrozenCurrency
    # as up to 0.0009 across accounts.
    if float(GetFrozen('asset')) > 0 or float(GetFrozen('currency')) > 0.003:
      return True
    else:
      return False

  def CancelLastOrderIfExist():
    if OrderExist():
      print(
          'We have a stale trade from last candle! Cancelling so we may move on')
      try:
        LastOrderID = TradeAPI.get_order()['orders'][0]['orders_id']
        time.sleep(gc.API.APIWait)
        try:
          TradeAPI.cancel_order(
              LastOrderID, symbol=gc.API.TradePair)
          time.sleep(gc.API.APIWait)
        except Exception:
          print(
              "Order cancel failed! Did you manually remove the order?")
      except IndexError:
        print('Order just completed, can no longer cancel')

  def Trade(order, rate, amount, pair):
    TradeAPI.trade(order, rate, amount, pair)
