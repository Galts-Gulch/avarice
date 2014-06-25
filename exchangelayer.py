import time

import genconfig

# Want to add support for a new exchange? Check docs/Contributing.md

if genconfig.Exchange == 'okcoin':
    import okcoin_api

    Market = okcoin_api.MarketData()
    if not genconfig.SimulatorTrading:
        TradeAPI = okcoin_api.TradeAPI(genconfig.partner, genconfig.secret_key)

    def GetFree(security):
        if security == 'currency':
            time.sleep(genconfig.APIWait)
            Free = TradeAPI.get_info()['info']['funds']['free']\
                    [genconfig.Currency]
        elif security == 'asset':
            time.sleep(genconfig.APIWait)
            Free = TradeAPI.get_info()['info']['funds']['free']\
                    [genconfig.Asset]
        return Free

    def GetFrozen(security):
        if security == 'currency':
            time.sleep(genconfig.APIWait)
            Frozen = TradeAPI.get_info()['info']['funds']['freezed'][genconfig.Currency]
        elif security == 'asset':
            time.sleep(genconfig.APIWait)
            Frozen = TradeAPI.get_info()['info']['funds']['freezed'][genconfig.Asset]
        return Frozen

    def GetTradeAmount(security):
        if security == 'currency':
            Amount = (genconfig.TradeVolume / 100) * float(GetFree('currency'))
        elif security == 'asset':
            Amount = (genconfig.TradeVolume / 100) * float(GetFree('asset'))
        return Amount

    def GetMarketPrice(order):
        if order == 'bid':
            Price = Market.ticker(genconfig.TradePair).bid
        elif order == 'ask':
            Price = Market.ticker(genconfig.TradePair).ask
        return Price

    def CancelLastOrderIfExist():
        # NOTE: occasionally OKCoin has a bug that reports FrozenCurrency
        # as up to 0.0009 across accounts.
        if float(GetFrozen('asset')) > 0 or float(GetFrozen('currency')) > 0.0009:
            print('We have a stale trade from last candle! Cancelling so we may move on')
            try:
                LastOrderID = TradeAPI.get_order()['orders'][0]['orders_id']
                time.sleep(genconfig.APIWait)
                try:
                    TradeAPI.cancel_order(LastOrderID, symbol=genconfig.TradePair)
                    time.sleep(genconfig.APIWait)
                except Exception:
                    print("Order cancel failed! Did you manually remove the order?")
            except IndexError:
                print('Order just completed, can no longer cancel')

    def Trade(order, rate, amount, pair):
        TradeAPI.trade(order, rate, amount, pair)
