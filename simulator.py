import logging

import exchangelayer
import genconfig
import genutils
import loggerdb
import simulator
import strategies

SimCurrency = genconfig.Simulator.Currency
SimAsset = genconfig.Simulator.Asset

logger = logging.getLogger('simulator')


def SimLog():
  Worth = (loggerdb.price_list[-1] * SimAsset) + SimCurrency
  logger.debug('Asset: %s %s, Currency: %s %s, Net Worth: %s %s', str(SimAsset),
               genconfig.API.Asset, str(SimCurrency), genconfig.API.Currency,
               str(Worth), genconfig.API.Currency)


def SimulateFromStrategy():
  # Is external, otherwise on each function call we clear content
  TradeCurrency = (
      strategies.Trade_dict['TradeVolume'] / 100) * simulator.SimCurrency
  TradeAsset = (
      strategies.Trade_dict['TradeVolume'] / 100) * simulator.SimAsset
  if strategies.Trade_dict['Order'] == 'Buy':
    # Get fresh ask price
    MarketAskPrice = exchangelayer.GetMarketPrice('ask')
    BidTradeAmount = TradeCurrency / MarketAskPrice
    if BidTradeAmount > genconfig.API.AssetTradeMin:
      if len(str(BidTradeAmount).split('.')[1]) > 3:
        BidTradeAmount = round(BidTradeAmount, 3)
      simulator.SimAsset += BidTradeAmount
      simulator.SimCurrency -= BidTradeAmount * MarketAskPrice
      logger.debug('BUYING %s %s at %s %s', str(BidTradeAmount), genconfig.API.Asset,
                   str(MarketAskPrice), genconfig.API.Currency)
      SimLog()
    elif BidTradeAmount < genconfig.API.AssetTradeMin:
      logger.debug('Wanted to BUY %s %s at %s but needed more %s', str(BidTradeAmount),
                   genconfig.API.Asset, str(MarketAskPrice), genconfig.API.Currency)
  elif strategies.Trade_dict['Order'] == 'Sell':
    # Get fresh bid price
    MarketBidPrice = exchangelayer.GetMarketPrice('bid')
    if TradeAsset > genconfig.API.AssetTradeMin:
      if len(str(TradeAsset).split('.')[1]) > 3:
        TradeAsset = round(TradeAsset, 3)
      simulator.SimAsset -= TradeAsset
      simulator.SimCurrency += TradeAsset * MarketBidPrice
      logger.debug('SELLING %s %s at %s %s', str(TradeAsset), genconfig.API.Asset,
                   str(MarketBidPrice), genconfig.API.Currency)
      SimLog()
    elif TradeAsset < genconfig.API.AssetTradeMin:
      logger.debug('Wanted to SELL %s %s at %s but needed more %s', str(TradeAsset),
                   genconfig.API.Asset, str(MarketBidPrice), genconfig.API.Asset)
