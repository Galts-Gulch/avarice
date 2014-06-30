import exchangelayer
import genconfig
import genutils
import loggerdb
import simulator
import strategies

SimCurrency = genconfig.SimulatorCurrency
SimAsset = genconfig.SimulatorAsset

def SimulateFromIndicator():
    # Is external, otherwise on each function call we clear content
    TradeCurrency = (genconfig.TradeVolume / 100) * simulator.SimCurrency
    TradeAsset = (genconfig.TradeVolume / 100) * simulator.SimAsset
    if strategies.Trade_list[-1] == 'Buy':
        # Get fresh ask price
        MarketAskPrice = exchangelayer.GetMarketPrice('ask')
        BidTradeAmount = TradeCurrency / MarketAskPrice
        if BidTradeAmount > genconfig.AssetTradeMin:
            if len(str(BidTradeAmount).split('.')[1]) > 3:
                BidTradeAmount = round(BidTradeAmount, 3)
            simulator.SimAsset += BidTradeAmount
            simulator.SimCurrency -= BidTradeAmount * MarketAskPrice
            print('[SIMULATOR] BUYING', BidTradeAmount, genconfig.Asset, 'at',\
                    MarketAskPrice, genconfig.Currency)
            if genconfig.RecordTrades:
                genutils.RecordTrades('BOUGHT', MarketAskPrice, BidTradeAmount)
        elif BidTradeAmount < genconfig.AssetTradeMin:
            print('[SIMULATOR] Wanted to BUY', BidTradeAmount, genconfig.Asset,\
                    'at', MarketAskPrice, 'but needed more', genconfig.Currency)
    elif strategies.Trade_list[-1] == 'Sell':
        # Get fresh bid price
        MarketBidPrice = exchangelayer.GetMarketPrice('bid')
        if TradeAsset > genconfig.AssetTradeMin:
            if len(str(TradeAsset).split('.')[1]) > 3:
                TradeAsset = round(TradeAsset, 3)
            simulator.SimAsset -= TradeAsset
            simulator.SimCurrency += TradeAsset * MarketBidPrice
            print('[SIMULATOR] SELLING', TradeAsset, genconfig.Asset, 'at',\
                    MarketBidPrice, genconfig.Currency)
            if genconfig.RecordTrades:
                genutils.RecordTrades('SOLD', MarketBidPrice, TradeAsset)
        elif TradeAsset < genconfig.AssetTradeMin:
            print('[SIMULATOR] Wanted to SELL', TradeAsset, genconfig.Asset, 'at',\
                    MarketBidPrice, 'but needed more', genconfig.Asset)

    Worth = (loggerdb.price_list[-1] * SimAsset) + SimCurrency
    print('[SIMULATOR] Asset:', SimAsset, genconfig.Asset, 'Currency:', SimCurrency,\
            genconfig.Currency, 'Net Worth:', Worth, genconfig.Currency)
