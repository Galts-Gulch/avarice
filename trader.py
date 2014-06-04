import time

import genconfig
import hidconfig
import indicators
import loggerdb
import okcoin
import strategies

def TradeFromIndicator():

    # Wait until we have enough data to trade off
    if len(hidconfig.IndicatorList) >= genconfig.TradeDelay:
        TradeAPI = okcoin.TradeAPI(genconfig.partner, genconfig.secret_key)
        Market = okcoin.MarketData()
        FreeAsset = TradeAPI.get_info()['info']['funds']['free']\
                [genconfig.Asset]

        # Fucking api restrictions (why there are nasty sleeps in here)!
        time.sleep(1)
        FreeCurrency = TradeAPI.get_info()['info']['funds']['free']\
                [genconfig.Currency]
        time.sleep(1)
        TradeAsset = (genconfig.TradeVolume / 100) * float(FreeAsset)
        TradeCurrency = (genconfig.TradeVolume / 100) * float(FreeCurrency)
        time.sleep(1)
        FrozenAsset = TradeAPI.get_info()['info']['funds']['freezed'][genconfig.Asset]
        time.sleep(1)
        FrozenCurrency = TradeAPI.get_info()['info']['funds']['freezed'][genconfig.Currency]

        # Check for a trade from last candle. Cancel if one still exists.
        # NOTE: occasionally OKCoin has a bug that reports FrozenCurrency as 0.0001 across
        # accounts.
        if float(FrozenAsset) > 0 or float(FrozenCurrency) > 0.0001:
            print('We have a stale trade from last candle! Cancelling so we may move on')
            try:
                LastOrderID = TradeAPI.get_order()['orders'][0]['orders_id']
                time.sleep(1)
                try:
                    TradeAPI.cancel_order(LastOrderID, symbol=genconfig.TradePair)
                except:
                    print("Order cancel failed! Did you manually remove the order?")
            except IndexError:
                print('Order just completed, can no longer cancel')

        if strategies.Trade == 'Buy':
            time.sleep(1)
            # Get fresh ask price
            MarketAskPrice = Market.ticker(genconfig.TradePair).ask
            BidTradeAmount = TradeCurrency / MarketAskPrice
            if BidTradeAmount > hidconfig.AssetTradeMin:
                if len(str(BidTradeAmount).split('.')[1]) > 3:
                    BidTradeAmount = round(BidTradeAmount, 3)
                time.sleep(1)
                TradeAPI.trade('buy',MarketAskPrice,BidTradeAmount,genconfig.TradePair)
                print('BUYING', BidTradeAmount, genconfig.Asset, 'at',\
                        MarketAskPrice, genconfig.Currency)
            elif BidTradeAmount < 0.01:
                print('Wanted to BUY', BidTradeAmount, genconfig.Asset,\
                        'at', MarketAskPrice, 'but needed more', genconfig.Currency)
        elif strategies.Trade == 'Sell':
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
            elif TradeAsset < hidconfig.AssetTradeMin:
                print('Wanted to SELL', TradeAsset, genconfig.Asset, 'at',\
                        MarketBidPrice, 'but needed more', genconfig.Asset)
