import datetime
import logging
import time

import exchangelayer
import loggerdb
import simulator
import strategies
from storage import config, trades

SimCurrency = float(config.gc['Simulator']['Currency'])
SimAsset = float(config.gc['Simulator']['Asset'])
TP = config.gc['API']['Trade Pair']
Worth = None

logger = logging.getLogger('simulator')


def SimLog():
  simulator.Worth = (loggerdb.price_list[-1] * SimAsset) + SimCurrency
  logger.debug('Asset: %s %s, Currency: %s %s, Net Worth: %s %s', str(SimAsset),
               TP[:3], str(SimCurrency), TP[-3:], str(simulator.Worth), TP[-3:])


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
    if BidTradeAmount > float(config.gc['API']['Asset Trade Minimum']):
      if len(str(BidTradeAmount).split('.')[1]) > 3:
        BidTradeAmount = round(BidTradeAmount, 3)
      simulator.SimAsset += BidTradeAmount
      simulator.SimCurrency -= BidTradeAmount * MarketAskPrice
      logger.debug('BUYING %s %s at %s %s', str(BidTradeAmount), TP[:3],
                   str(MarketAskPrice), TP[-3:])
      SimLog()
      # Tuple structure is (Order, Trade Amount, Price, Current Worth)
      trades.writelist('simulator', 'orders', ('Buy',
                                               BidTradeAmount,
                                               loggerdb.price_list[-1],
                                               simulator.Worth))
    elif BidTradeAmount < float(config.gc['API']['Asset Trade Minimum']):
      logger.debug('Wanted to BUY %s %s at %s but needed more %s', str(BidTradeAmount),
                   TP[:3], str(MarketAskPrice), TP[-3:])
  elif strategies.Trade_dict['Order'] == 'Sell':
    # Get fresh bid price
    MarketBidPrice = exchangelayer.GetMarketPrice('bid')
    if TradeAsset > float(config.gc['API']['Asset Trade Minimum']):
      if len(str(TradeAsset).split('.')[1]) > 3:
        TradeAsset = round(TradeAsset, 3)
      simulator.SimAsset -= TradeAsset
      simulator.SimCurrency += TradeAsset * MarketBidPrice
      logger.debug('SELLING %s %s at %s %s', str(TradeAsset), TP[:3],
                   str(MarketBidPrice), TP[-3:])
      SimLog()
      # Tuple structure is (Order, Trade Amount, Price, Current Worth)
      trades.writelist('simulator', 'orders', ('Sell',
                                               TradeAsset,
                                               loggerdb.price_list[-1],
                                               simulator.Worth))
    elif TradeAsset < float(config.gc['API']['Asset Trade Minimum']):
      logger.debug('Wanted to SELL %s %s at %s but needed more %s', str(TradeAsset),
                   TP[:3], str(MarketBidPrice), TP[:3])
