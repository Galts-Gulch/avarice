import time
import exchangelayer as el
import genconfig as gc
import genutils as gu
import strategies as st
import trader as trd

LastOrder = 'N'
OrderPrice = 0
TradeAmount = 0
def TradeFromStrategy():
    # Wait until we have enough data to trade off
    if len(st.Trade_list) >= gc.Trader.TradeDelay:
        if st.Trade_list[-1] == 'Buy':
            el.CancelLastOrderIfExist()
            # Get fresh ask price
            MarketAskPrice = el.GetMarketPrice('ask')
            trd.TradeAmount = gu.RoundIfGreaterThan((\
                    el.GetTradeAmount('currency') / MarketAskPrice) , 3)
            if TradeAmount > gc.API.AssetTradeMin:
                el.Trade('buy', MarketAskPrice, TradeAmount,\
                        gc.API.TradePair)
                print('BUYING', TradeAmount, gc.API.Asset, 'at',\
                        MarketAskPrice, gc.API.Currency)
                if gc.Trader.Enabled:
                    gu.RecordTrades('BOUGHT', MarketAskPrice, TradeAmount)
                # KISS method...
                trd.OrderPrice = MarketAskPrice
                trd.LastOrder = 'buy'
            elif TradeAmount < gc.API.AssetTradeMin:
                print('Wanted to BUY', TradeAmount, gc.API.Asset,\
                        'at', MarketAskPrice, 'but needed more', gc.API.Currency)
        elif st.Trade_list[-1] == 'Sell':
            el.CancelLastOrderIfExist()
            trd.TradeAmount = gu.RoundIfGreaterThan(\
                    el.GetTradeAmount('asset'), 3)
            MarketBidPrice = el.GetMarketPrice('bid')
            if TradeAmount > gc.API.AssetTradeMin:
                el.Trade('sell',MarketBidPrice, TradeAmount, gc.API.TradePair)
                print('SELLING', TradeAmount, gc.API.Asset, 'at',\
                        MarketBidPrice, gc.API.Currency)
                if gc.Trader.Enabled:
                    gu.RecordTrades('SOLD', MarketBidPrice, TradeAmount)
                # KISS method...
                trd.OrderPrice = MarketBidPrice
                trd.LastOrder = 'sell'
            elif TradeAmount < gc.API.AssetTradeMin:
                print('Wanted to SELL', TradeAmount, gc.API.Asset, 'at',\
                        MarketBidPrice, 'but needed more', gc.API.Asset)

def ReIssueTrade():
    if el.OrderExist():
        el.CancelLastOrderIfExist()
        if LastOrder == 'sell':
            CurrPrice = el.GetMarketPrice('bid')
        if LastOrder == 'buy':
            CurrPrice = el.GetMarketPrice('ask')
        Prices = [CurrPrice, OrderPrice]
        PriceDelta = max(Prices) / min(Prices)
        if not PriceDelta == 1.0:
            if PriceDelta <= (gc.Trader.ReIssueSlippage / 100) + 1:
                el.Trade(Lastorder, CurrPrice, TradeAmount, gc.API.TradePair)
                print('Re-', LastOrder.upper(), 'at ', CurrPrice)
