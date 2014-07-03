import time
import exchangelayer
import genconfig
import genutils
import hidconfig
import loggerdb
import strategies

def TradeFromIndicator():
    # Wait until we have enough data to trade off
    if len(hidconfig.IndicatorList) >= genconfig.Trader.TradeDelay:
        if strategies.Trade_list[-1] == 'Buy':
            exchangelayer.CancelLastOrderIfExist()
            # Get fresh ask price
            MarketAskPrice = exchangelayer.GetMarketPrice('ask')
            BidTradeAmount = genutils.RoundIfGreaterThan((\
                    exchangelayer.GetTradeAmount('currency') / MarketAskPrice) , 3)
            if BidTradeAmount > genconfig.API.AssetTradeMin:
                exchangelayer.Trade('buy', MarketAskPrice, BidTradeAmount,\
                        genconfig.API.TradePair)
                print('BUYING', BidTradeAmount, genconfig.API.Asset, 'at',\
                        MarketAskPrice, genconfig.API.Currency)
                if genconfig.TradeRecorder.Enabled:
                    genutils.RecordTrades('BOUGHT', MarketAskPrice, BidTradeAmount)
            elif BidTradeAmount < genconfig.API.AssetTradeMin:
                print('Wanted to BUY', BidTradeAmount, genconfig.API.Asset,\
                        'at', MarketAskPrice, 'but needed more', genconfig.API.Currency)
        elif strategies.Trade_list[-1] == 'Sell':
            exchangelayer.CancelLastOrderIfExist()
            TradeAsset = genutils.RoundIfGreaterThan(\
                    exchangelayer.GetTradeAmount('asset'), 3)
            MarketBidPrice = exchangelayer.GetMarketPrice('bid')
            if TradeAsset > genconfig.API.AssetTradeMin:
                exchangelayer.Trade('sell',MarketBidPrice,TradeAsset,\
                        genconfig.API.TradePair)
                print('SELLING', TradeAsset, genconfig.API.Asset, 'at',\
                        MarketBidPrice, genconfig.API.Currency)
                if genconfig.TradeRecorder.Enabled:
                    genutils.RecordTrades('SOLD', MarketBidPrice, TradeAsset)
            elif TradeAsset < genconfig.API.AssetTradeMin:
                print('Wanted to SELL', TradeAsset, genconfig.API.Asset, 'at',\
                        MarketBidPrice, 'but needed more', genconfig.API.Asset)
