import asyncio
import logging
import time

import exchangelayer as el
import genconfig as gc
import genutils as gu
import strategies as st
import trader as trd

FreshOrder = False
LastOrder = {}

logger = logging.getLogger('trader')


def GetTradeAmount(order, volume):
  if order == 'buy':
    ta = gu.RoundIfGreaterThan(
        ((volume / 100) * el.GetFree('currency') / el.GetMarketPrice('ask')), 3)
  elif order == 'sell':
    ta = gu.RoundIfGreaterThan((volume / 100) * el.GetFree('asset'), 3)
  else:
    ta = 0
  return ta


@asyncio.coroutine
def TradeWrapper():
  while True:
    if trd.LastOrder:
      if trd.FreshOrder:
        # New order, so just make a standard trade.
        el.Trade(trd.LastOrder['order'], trd.LastOrder[
                 'price'], trd.LastOrder['amount'])
        trd.FreshOrder = False
      elif el.OrderExist():
        el.CancelLastOrderIfExist()
        if trd.LastOrder['order'] == 'sell':
          CurrPrice = el.GetMarketPrice('bid')
        if trd.LastOrder['order'] == 'buy':
          CurrPrice = el.GetMarketPrice('ask')
        Prices = [CurrPrice, trd.LastOrder['price']]
        PriceDelta = max(Prices) - min(Prices)
        TradeAmount = GetTradeAmount(
            trd.LastOrder['order'], trd.LastOrder['tradevolume'])
        if PriceDelta <= (gc.Trader.ReIssueSlippage / 100) * trd.LastOrder['price']:
          if TradeAmount > gc.API.AssetTradeMin:
            el.Trade(trd.LastOrder['order'], CurrPrice, TradeAmount)
            logger.debug(
                'Re %s at %s', trd.LastOrder['order'].upper(), str(CurrPrice))
          else:
            logger.debug('Order Mostly Filled; Leftover Too Small')
            trd.LastOrder = {}
      else:
        # Not a new order, and no existing orders. Stop loop.
        logger.debug('Order Successful')
        trd.LastOrder = {}
    yield from asyncio.sleep(gc.Trader.ReIssueDelay)


def TradeFromStrategy():
  if st.Trade_dict['Order'] == 'Buy':
    trd.FreshOrder = True
    TradeAmount = GetTradeAmount('buy', st.Trade_dict['TradeVolume'])
    if TradeAmount > gc.API.AssetTradeMin:
      logger.debug('BUYING %s %s at %s %s', str(TradeAmount), gc.API.Asset, str(
          el.GetMarketPrice('ask')), gc.API.Currency)
      trd.LastOrder = {
          'order': 'buy', 'price': el.GetMarketPrice('ask'),
          'amount': TradeAmount, 'tradevolume': st.Trade_dict['TradeVolume']}
    else:
      logger.debug('Wanted to BUY %s %s at %s but needed more %s', str(
          TradeAmount), gc.API.Asset, str(el.GetMarketPrice('bid')), gc.API.Currency)
  elif st.Trade_dict['Order'] == 'Sell':
    trd.FreshOrder = True
    TradeAmount = GetTradeAmount('sell', st.Trade_dict['TradeVolume'])
    if TradeAmount > gc.API.AssetTradeMin:
      logger.debug('SELLING %s %s at %s %s', str(TradeAmount), gc.API.Asset, str(
          el.GetMarketPrice('bid')), gc.API.Currency)
      trd.LastOrder = {
          'order': 'sell', 'price': el.GetMarketPrice('bid'),
          'amount': TradeAmount, 'tradevolume': st.Trade_dict['TradeVolume']}
    else:
      logger.debug('Wanted to SELL %s %s at %s but needed more %s', str(
          TradeAmount), gc.API.Asset, str(el.GetMarketPrice('bid')), gc.API.Asset)
