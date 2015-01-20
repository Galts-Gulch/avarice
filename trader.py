import time

import exchangelayer as el
import genconfig as gc
import genutils as gu
import strategies as st
import trader as trd

FreshOrder = False


def GetTradeAmount(order):
  if order == 'buy':
    ta = gu.RoundIfGreaterThan(
        (el.GetTradeAmount('currency') / el.GetMarketPrice('ask')), 3)
  elif order == 'sell':
    ta = gu.RoundIfGreaterThan(el.GetTradeAmount('asset'), 3)
  else:
    ta = 0
  return ta


def TradeWrapper(order, price, amt):
  while True:
    if trd.FreshOrder:
      # New order, so just make a standard trade.
      el.Trade(order, price, amt)
      trd.FreshOrder = False
    elif el.OrderExist():
      el.CancelLastOrderIfExist()
      if order == 'sell':
        CurrPrice = el.GetMarketPrice('bid')
      if order == 'buy':
        CurrPrice = el.GetMarketPrice('ask')
      Prices = [CurrPrice, price]
      PriceDelta = max(Prices) / min(Prices)
      TradeAmount = GetTradeAmount(order)
      if not PriceDelta == 1.0:
        if PriceDelta <= (gc.Trader.ReIssueSlippage / 100) + 1:
          if TradeAmount > gc.API.AssetTradeMin:
            el.Trade(order, CurrPrice, TradeAmount)
            print('Re-', order.upper(), 'at ', CurrPrice)
          else:
            print('Order Mostly Filled; Leftover Too Small')
            break
    else:
      # Not a new order, and no existing orders. Stop loop.
      print('Order Successful')
      break
    time.sleep(gc.Trader.ReIssueDelay)


def TradeFromStrategy():
  # Wait until we have enough data to trade off
  if len(st.Trade_list) >= gc.Trader.TradeDelay:
    if st.Trade_list[-1] == 'Buy':
      if el.OrderExist():
        el.CancelLastOrderIfExist()
      trd.FreshOrder = True
      TradeAmount = GetTradeAmount('buy')
      if TradeAmount > gc.API.AssetTradeMin:
        print('BUYING', TradeAmount, gc.API.Asset, 'at',
              el.GetMarketPrice('ask'), gc.API.Currency)
        TradeWrapper('buy', el.GetMarketPrice('ask'), TradeAmount)
        if gc.TradeRecorder.Enabled:
          gu.RecordTrades('BOUGHT', el.GetMarketPrice('ask'),
                          TradeAmount)
      else:
        print('Wanted to BUY', TradeAmount, gc.API.Asset,
              'at', el.GetMarketPrice('bid'), 'but needed more',
              gc.API.Currency)
    elif st.Trade_list[-1] == 'Sell':
      if el.OrderExist():
        el.CancelLastOrderIfExist()
      trd.FreshOrder = True
      TradeAmount = GetTradeAmount('sell')
      if TradeAmount > gc.API.AssetTradeMin:
        print('SELLING', TradeAmount, gc.API.Asset,
              'at', el.GetMarketPrice('bid'), gc.API.Currency)
        TradeWrapper('sell', el.GetMarketPrice('bid'), TradeAmount)
        if gc.TradeRecorder.Enabled:
          gu.RecordTrades('SOLD', el.GetMarketPrice('bid'), TradeAmount)
      else:
        print('Wanted to SELL', TradeAmount, gc.API.Asset, 'at',
              el.GetMarketPrice('bid'), 'but needed more', gc.API.Asset)
