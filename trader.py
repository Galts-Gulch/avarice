import exchangelayer as el
import genconfig as gc
import genutils as gu
import strategies as st
import trader as trd

LastOrder = 'N'
OrderPrice = 0
MarketAskPrice = 0
MarketBidPrice = 0

def GetTradeAmount(order):
    if order == 'buy':
        ta = gu.RoundIfGreaterThan((el.GetTradeAmount('currency')\
                / MarketAskPrice), 3)
    elif order == 'sell':
        ta = gu.RoundIfGreaterThan(el.GetTradeTradeAmount('asset'), 3)
    else:
        ta = 0
    return ta

def SetMarketPrice(order):
    if order == 'buy':
        trd.MarketAskPrice = el.GetMarketPrice('ask')
    elif order == 'sell':
        trd.MarketBidPrice = el.GetMarketPrice('bid')

def TradeFromStrategy():
    # Wait until we have enough data to trade off
    if len(st.Trade_list) >= gc.Trader.TradeDelay:
        if st.Trade_list[-1] == 'Buy':
            el.CancelLastOrderIfExist()
            # Get fresh ask price
            SetMarketPrice('buy')
            TradeAmount = GetTradeAmount('buy')
            if TradeAmount > gc.API.AssetTradeMin:
                el.Trade('buy', trd.MarketAskPrice, TradeAmount,\
                        gc.API.TradePair)
                print('BUYING', TradeAmount, gc.API.Asset, 'at',\
                        trd.MarketAskPrice, gc.API.Currency)
                if gc.Trader.Enabled:
                    gu.RecordTrades('BOUGHT', trd.MarketAskPrice, TradeAmount)
                # KISS method...
                trd.OrderPrice = trd.MarketAskPrice
                trd.LastOrder = 'buy'
            elif TradeAmount < gc.API.AssetTradeMin:
                print('Wanted to BUY', TradeAmount, gc.API.Asset,\
                        'at', trd.MarketAskPrice, 'but needed more', gc.API.Currency)
        elif st.Trade_list[-1] == 'Sell':
            el.CancelLastOrderIfExist()
            TradeAmount = GetTradeAmount('sell')
            # Get fresh bid price
            SetMarketPrice('sell')
            if TradeAmount > gc.API.AssetTradeMin:
                el.Trade('sell', trd.MarketBidPrice, TradeAmount, gc.API.TradePair)
                print('SELLING', TradeAmount, gc.API.Asset, 'at',\
                        trd.MarketBidPrice, gc.API.Currency)
                if gc.Trader.Enabled:
                    gu.RecordTrades('SOLD', trd.MarketBidPrice, TradeAmount)
                # KISS method...
                trd.OrderPrice = trd.MarketBidPrice
                trd.LastOrder = 'sell'
            elif TradeAmount < gc.API.AssetTradeMin:
                print('Wanted to SELL', TradeAmount, gc.API.Asset, 'at',\
                        trd.MarketBidPrice, 'but needed more', gc.API.Asset)

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
                el.Trade(LastOrder, CurrPrice, GetTradeAmount(LastOrder),\
                        gc.API.TradePair)
                print('Re-', LastOrder.upper(), 'at ', CurrPrice)
