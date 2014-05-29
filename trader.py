import time

import genconfig
import indicators
import loggerdb
import okcoin

def TradeFromIndicator():
    TradeAPI = okcoin.TradeAPI(genconfig.partner, genconfig.secret_key)
    Market = okcoin.MarketData()
    FreeAsset = TradeAPI.get_info()['info']['funds']['free']\
            [genconfig.Asset]
    # Fucking api restrictions!
    time.sleep(1)
    FreeCurrency = TradeAPI.get_info()['info']['funds']['free']\
            [genconfig.Currency]
    time.sleep(1)
    TradeAsset = (genconfig.TradeVolume / 100) * float(FreeAsset)
    TradeCurrency = (genconfig.TradeVolume /100) * float(FreeCurrency)

    #OKCoin minimum asset trade values
    if genconfig.TradePair == 'btc_cny':
        AssetTradeMin = 0.01
    elif genconfig.TradePair == 'ltc_cny':
        AssetTradeMin = 0.1

    # Due to external calling, we can't use concat or getattr here
    if genconfig.Indicator == 'RSI':
        IndicatorList = indicators.RSI_list
        IndicatorAsk = genconfig.RSIAsk
        IndicatorBid = genconfig.RSIBid
    elif genconfig.Indicator == 'StochRSI':
        IndicatorList = indicators.StochRSI_list
        IndicatorAsk = genconfig.StochRSIAsk
        IndicatorBid = genconfig.StochRSIBid

    # Wait until we have enough data to trade off
    if len(IndicatorList) >= genconfig.TradeDelay:
        if IndicatorList[-1] <= IndicatorBid:
            time.sleep(1)
            # Get fresh ask price
            MarketAskPrice = Market.ticker(genconfig.TradePair).ask
            BidTradeAmount = TradeCurrency / MarketAskPrice
            if BidTradeAmount > AssetTradeMin:
                if len(str(BidTradeAmount).split('.')[1]) > 3:
                    BidTradeAmount = round(BidTradeAmount, 3)
                time.sleep(1)
                TradeAPI.trade('buy',MarketAskPrice,BidTradeAmount,genconfig.TradePair)
                print('BUYING', BidTradeAmount, genconfig.Asset, 'at',\
                        MarketAskPrice, genconfig.Currency)
            elif BidTradeAmount < 0.01:
                print('Wanted to BUY', BidTradeAmount, genconfig.Asset,\
                        'at', MarketAskPrice, 'but needed more', genconfig.Currency)
        elif IndicatorList[-1] >= IndicatorAsk:
            time.sleep(1)
            # Get fresh bid price
            MarketBidPrice = Market.ticker(genconfig.TradePair).bid
            if TradeAsset > 0.01:
                if len(str(TradeAsset).split('.')[1]) > 3:
                    TradeAsset = round(TradeAsset, 3)
                time.sleep(1)
                TradeAPI.trade('sell',MarketBidPrice,TradeAsset,genconfig.TradePair)
                print('SELLING', TradeAsset, genconfig.Asset, 'at',\
                        MarketBidPrice, genconfig.Currency)
            elif TradeAsset < AssetTradeMin:
                print('Wanted to SELL', TradeAsset, genconfig.Asset, 'at',\
                        MarketBidPrice, 'but needed more', genconfig.Asset)
