import time
import exchangelayer
import genconfig
import genutils
import hidconfig
import loggerdb
import strategies

def TradeFromIndicator():
    # Wait until we have enough data to trade off
    if len(hidconfig.IndicatorList) >= genconfig.TradeDelay:
        if strategies.Trade_list[-1] == 'Buy':
            exchangelayer.CancelLastOrderIfExist()
            # Get fresh ask price
            MarketAskPrice = exchangelayer.GetMarketPrice('ask')
            BidTradeAmount = genutils.RoundIfGreaterThan((\
                    exchangelayer.GetTradeAmount('currency') / MarketAskPrice) , 3)
            if BidTradeAmount > genconfig.AssetTradeMin:
                exchangelayer.Trade('buy', MarketAskPrice, BidTradeAmount,\
                        genconfig.TradePair)
                print('BUYING', BidTradeAmount, genconfig.Asset, 'at',\
                        MarketAskPrice, genconfig.Currency)
                if genconfig.RecordTrades:
                    genutils.RecordTrades('BOUGHT', MarketAskPrice, BidTradeAmount)
            elif BidTradeAmount < genconfig.AssetTradeMin:
                print('Wanted to BUY', BidTradeAmount, genconfig.Asset,\
                        'at', MarketAskPrice, 'but needed more', genconfig.Currency)
        elif strategies.Trade_list[-1] == 'Sell':
            exchangelayer.CancelLastOrderIfExist()
            TradeAsset = genutils.RoundIfGreaterThan(\
                    exchangelayer.GetTradeAmount('asset'), 3)
            MarketBidPrice = exchangelayer.GetMarketPrice('bid')
            if TradeAsset > genconfig.AssetTradeMin:
                exchangelayer.Trade('sell',MarketBidPrice,TradeAsset,\
                        genconfig.TradePair)
                print('SELLING', TradeAsset, genconfig.Asset, 'at',\
                        MarketBidPrice, genconfig.Currency)
                if genconfig.RecordTrades:
                    genutils.RecordTrades('SOLD', MarketBidPrice, TradeAsset)
            elif TradeAsset < genconfig.AssetTradeMin:
                print('Wanted to SELL', TradeAsset, genconfig.Asset, 'at',\
                        MarketBidPrice, 'but needed more', genconfig.Asset)
