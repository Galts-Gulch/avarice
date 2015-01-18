from threading import Timer

import exchangelayer as el
import genconfig as gc
import genutils as gu
import strategies as st
import trader as trd

LastOrder = {}


def GetTradeAmount(order):
  if order == 'buy':
    ta = gu.RoundIfGreaterThan(
        (el.GetTradeAmount('currency') / el.GetMarketPrice('ask')), 3)
  elif order == 'sell':
    ta = gu.RoundIfGreaterThan(el.GetTradeAmount('asset'), 3)
  else:
    ta = 0
  return ta


def SetMarketPrice(order):
  if order == 'buy':
    trd.MarketAskPrice = el.GetMarketPrice('ask')
  elif order == 'sell':
    trd.MarketBidPrice = el.GetMarketPrice('bid')


def Trade():
  while True:
    if el.OrderExist():
      el.CancelLastOrderIfExist()
      if LastOrder['order'] == 'sell':
        CurrPrice = el.GetMarketPrice('bid')
      if LastOrder['order'] == 'buy':
        CurrPrice = el.GetMarketPrice('ask')
      Prices = [CurrPrice, LastOrder['price']]
      PriceDelta = max(Prices) / min(Prices)
      if not PriceDelta == 1.0:
        if PriceDelta <= (gc.Trader.ReIssueSlippage / 100) + 1:
          TradeAmount = GetTradeAmount(LastOrder['order'])
          if TradeAmount > gc.API.AssetTradeMin:
            el.Trade(
                LastOrder['order'], CurrPrice, LastOrder['amount'])
            print('Re-', LastOrder['order'].upper(), 'at ', CurrPrice)
          else:
            print('Order Mostly Filled; Leftover Too Small')
            break
      else:
        el.Trade(LastOrder['order'], LastOrder['price'], LastOrder['amount'])
    else:
      el.Trade(LastOrder['order'], LastOrder['price'], LastOrder['amount'])
      print('Order Successful')
      break


def TradeWrapper(order, price, amt):
  trd.LastOrder = {'order': order, 'price': price, 'amount': amt}
  Timer(gc.Trader.ReIssueDelay, Trade).start()


def TradeFromStrategy():
  # Wait until we have enough data to trade off
  if len(st.Trade_list) >= gc.Trader.TradeDelay:
    if st.Trade_list[-1] == 'Buy':
      el.CancelLastOrderIfExist()
      TradeAmount = GetTradeAmount('buy')
      if TradeAmount > gc.API.AssetTradeMin:
        TradeWrapper('buy', el.GetMarketPrice('ask'), TradeAmount)
        print('BUYING', TradeAmount, gc.API.Asset, 'at',
              el.GetMarketPrice('ask'), gc.API.Currency)
        if gc.TradeRecorder.Enabled:
          gu.RecordTrades('BOUGHT', el.GetMarketPrice('ask'),
                          TradeAmount)
      else:
        print('Wanted to BUY', TradeAmount, gc.API.Asset,
              'at', el.GetMarketPrice('bid'), 'but needed more',
              gc.API.Currency)
    elif st.Trade_list[-1] == 'Sell':
      el.CancelLastOrderIfExist()
      TradeAmount = GetTradeAmount('sell')
      if TradeAmount > gc.API.AssetTradeMin:
        TradeWrapper('sell', el.GetMarketPrice('bid'), TradeAmount)
        print('SELLING', TradeAmount, gc.API.Asset,
              'at', el.GetMarketPrice('bid'), gc.API.Currency)
        if gc.TradeRecorder.Enabled:
          gu.RecordTrades('SOLD', el.GetMarketPrice('bid'), TradeAmount)
      else:
        print('Wanted to SELL', TradeAmount, gc.API.Asset, 'at',
              el.GetMarketPrice('bid'), 'but needed more', gc.API.Asset)
