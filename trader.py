import time

import genconfig
import indicators
import loggerdb
import okcoin

def TradeFromIndicator():
    # Due to external calling and varying indicator types,
    # we can't use concat or getattr here
    if genconfig.Indicator == 'EMA':
        IndicatorList = indicators.EMALong_list
        IndicatorBid = genconfig.EMAShort_list
        IndicatorAsk = IndicatorBid
    elif genconfig.Indicator == 'RSI':
        IndicatorList = indicators.RSI_list
        IndicatorAsk = genconfig.RSIAsk
        IndicatorBid = genconfig.RSIBid
    elif genconfig.Indicator == 'FastStochRSIK':
        IndicatorList = indicators.FastStochRSIK_list
        IndicatorAsk = genconfig.FastStochRSIKAsk
        IndicatorBid = genconfig.FastStochRSIKBid
    elif genconfig.Indicator == 'FastStochRSID':
        IndicatorList = indicators.FastStochRSID_list
        IndicatorAsk = genconfig.FastStochRSIDAsk
        IndicatorBid = genconfig.FastStochRSIDBid
    elif genconfig.Indicator == 'FullStochRSID':
        IndicatorList = indicators.FullStochRSID_list
        IndicatorAsk = genconfig.FullStochRSIDAsk
        IndicatorBid = genconfig.FullStochRSIDBid
    elif genconfig.Indicator == 'FastStochK':
        IndicatorList = indicators.FastStochK_list
        IndicatorAsk = genconfig.FastStochKAsk
        IndicatorBid = genconfig.FastStochKBid
    elif genconfig.Indicator == 'FastStochD':
        IndicatorList = indicators.FastStochD_list
        IndicatorAsk = genconfig.FastStochDAsk
        IndicatorBid = genconfig.FastStochDBid
    elif genconfig.Indicator == 'FullStochD':
        IndicatorList = indicators.FullStochD_list
        IndicatorAsk = genconfig.FullStochDAsk
        IndicatorBid = genconfig.FullStochDBid

    # Wait until we have enough data to trade off
    if len(IndicatorList) >= genconfig.TradeDelay:
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
        TradeCurrency = (genconfig.TradeVolume /100) * float(FreeCurrency)
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

        #OKCoin minimum asset trade values
        if genconfig.TradePair == 'btc_cny':
            AssetTradeMin = 0.01
        elif genconfig.TradePair == 'ltc_cny':
            AssetTradeMin = 0.1

        if IndicatorList[-1] < IndicatorBid:
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
        elif IndicatorList[-1] > IndicatorAsk:
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
