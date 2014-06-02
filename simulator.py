import genconfig
import indicators
import loggerdb
import okcoin
import simulator

SimCurrency = genconfig.SimulatorCurrency
SimAsset = genconfig.SimulatorAsset

def SimulateFromIndicator():
    # Is external, otherwise on each function call we clear content
    TradeCurrency = (genconfig.TradeVolume / 100) * simulator.SimCurrency
    TradeAsset = (genconfig.TradeVolume / 100) * simulator.SimAsset

    # Wait until we have enough data to simulate trades off
    if len(hidconfig.IndicatorList) >= genconfig.TradeDelay:
        Market = okcoin.MarketData()
        if hidconfig.IndicatorList[-1] < hidconfig.IndicatorBid:
            # Get fresh ask price
            MarketAskPrice = Market.ticker(genconfig.TradePair).ask
            BidTradeAmount = TradeCurrency / MarketAskPrice
            if BidTradeAmount > hidconfig.AssetTradeMin:
                if len(str(BidTradeAmount).split('.')[1]) > 3:
                    BidTradeAmount = round(BidTradeAmount, 3)
                simulator.SimAsset += BidTradeAmount
                simulator.SimCurrency -= BidTradeAmount * MarketAskPrice
                print('[SIMULATOR] BUYING', BidTradeAmount, genconfig.Asset, 'at',\
                        MarketAskPrice, genconfig.Currency)
            elif BidTradeAmount < 0.01:
                print('[SIMULATOR] Wanted to BUY', BidTradeAmount, genconfig.Asset,\
                        'at', MarketAskPrice, 'but needed more', genconfig.Currency)
        elif hidconfig.IndicatorList[-1] > hidconfig.IndicatorAsk:
            # Get fresh bid price
            MarketBidPrice = Market.ticker(genconfig.TradePair).bid
            if TradeAsset > 0.01:
                if len(str(TradeAsset).split('.')[1]) > 3:
                    TradeAsset = round(TradeAsset, 3)
                simulator.SimAsset -= TradeAsset
                simulator.SimCurrency += TradeAsset * MarketBidPrice
                print('[SIMULATOR] SELLING', TradeAsset, genconfig.Asset, 'at',\
                        MarketBidPrice, genconfig.Currency)
            elif TradeAsset < hidconfig.AssetTradeMin:
                print('[SIMULATOR] Wanted to SELL', TradeAsset, genconfig.Asset, 'at',\
                        MarketBidPrice, 'but needed more', genconfig.Asset)

        Worth = (indicators.price_list[-1] * SimAsset) + SimCurrency
        print('[SIMULATOR] Asset:', SimAsset, genconfig.Asset, 'Currency:', SimCurrency,\
                genconfig.Currency, 'Net Worth:', Worth, genconfig.Currency)
