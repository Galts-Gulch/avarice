import exchangelayer
import genconfig
import genutils
import loggerdb
import simulator
import strategies

SimCurrency = genconfig.Simulator.Currency
SimAsset = genconfig.Simulator.Asset


def SimPrint():
  Worth = (loggerdb.price_list[-1] * SimAsset) + SimCurrency
  print('[SIMULATOR] Asset:', SimAsset, genconfig.API.Asset, 'Currency:', SimCurrency,
        genconfig.API.Currency, 'Net Worth:', Worth, genconfig.API.Currency)


def SimulateFromStrategy():
  # Is external, otherwise on each function call we clear content
  for d in strategies.Trade_list:
    TradeCurrency = (
        d['TradeVolume'] / 100) * simulator.SimCurrency
    TradeAsset = (
        d['TradeVolume'] / 100) * simulator.SimAsset
    if d['Order'] == 'Buy':
      # Get fresh ask price
      MarketAskPrice = exchangelayer.GetMarketPrice('ask')
      BidTradeAmount = TradeCurrency / MarketAskPrice
      if BidTradeAmount > genconfig.API.AssetTradeMin:
        if len(str(BidTradeAmount).split('.')[1]) > 3:
          BidTradeAmount = round(BidTradeAmount, 3)
        simulator.SimAsset += BidTradeAmount
        simulator.SimCurrency -= BidTradeAmount * MarketAskPrice
        print('[SIMULATOR] BUYING', BidTradeAmount, genconfig.API.Asset, 'at',
              MarketAskPrice, genconfig.API.Currency)
        if not genconfig.Simulator.Verbose:
          SimPrint()
        if genconfig.TradeRecorder.Enabled:
          genutils.RecordTrades('BOUGHT', MarketAskPrice, BidTradeAmount)
      elif BidTradeAmount < genconfig.API.AssetTradeMin:
        print('[SIMULATOR] Wanted to BUY', BidTradeAmount, genconfig.API.Asset,
              'at', MarketAskPrice, 'but needed more', genconfig.API.Currency)
    elif d['Order'] == 'Sell':
      # Get fresh bid price
      MarketBidPrice = exchangelayer.GetMarketPrice('bid')
      if TradeAsset > genconfig.API.AssetTradeMin:
        if len(str(TradeAsset).split('.')[1]) > 3:
          TradeAsset = round(TradeAsset, 3)
        simulator.SimAsset -= TradeAsset
        simulator.SimCurrency += TradeAsset * MarketBidPrice
        print('[SIMULATOR] SELLING', TradeAsset, genconfig.API.Asset, 'at',
              MarketBidPrice, genconfig.API.Currency)
        if not genconfig.Simulator.Verbose:
          SimPrint()
        if genconfig.TradeRecorder.Enabled:
          genutils.RecordTrades('SOLD', MarketBidPrice, TradeAsset)
      elif TradeAsset < genconfig.API.AssetTradeMin:
        print('[SIMULATOR] Wanted to SELL', TradeAsset, genconfig.API.Asset, 'at',
              MarketBidPrice, 'but needed more', genconfig.API.Asset)
    if genconfig.Simulator.Verbose:
      SimPrint()
