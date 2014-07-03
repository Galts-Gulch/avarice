import genconfig
import hidconfig
import indicators
import strategies

Trade_list = ['None']
LocalTrade_list = []
n = 'None'
b = 'Buy'
s = 'Sell'

def Generic():
    # Clear prior to loop
    ITrade_list = []
    for i in genconfig.TradeIndicators:
        hidind = getattr(hidconfig, i)
        if hasattr(hidind, 'BidAskList'):
            if len(hidind.IndicatorBid) >= 1:
                LocalBid = hidind.IndicatorBid[-1]
                LocalAsk = hidind.IndicatorAsk[-1]
            FilterList = hidind.IndicatorBid
        else:
            LocalBid = hidind.IndicatorBid
            LocalAsk = hidind.IndicatorAsk
            FilterList = hidind.IndicatorList

        # Wait until we have enough data to trade off
        if len(FilterList) >= genconfig.Trader.TradeDelay:
            if hasattr(hidind, 'TradeReverse'):
                if hidind.IndicatorList[-1] > LocalBid:
                    ITrade_list.append(b)
                elif hidind.IndicatorList[-1] < LocalAsk:
                    ITrade_list.append(s)
                else:
                    ITrade_list.append(n)
            else:
                if hidind.IndicatorList[-1] < LocalBid:
                    ITrade_list.append(b)
                elif hidind.IndicatorList[-1] > LocalAsk:
                    ITrade_list.append(s)
                else:
                    ITrade_list.append(n)

    # Check if we have data for all TradeIndicators, then check that signals
    # are the same.
    if len(ITrade_list) == len(genconfig.TradeIndicators):
        if all(x == ITrade_list[0] for x in ITrade_list):
            LocalTrade_list.append(ITrade_list[0])
        else:
            LocalTrade_list.append(n)
    else:
        LocalTrade_list.append(n)

    if genconfig.Trader.SingleTrade and len(LocalTrade_list) > 1:
        if LocalTrade_list[-1] == LocalTrade_list[-2]:
            if genconfig.Trader.TradePersist:
                if len(LocalTrade_list) > 2 and not LocalTrade_list[-2] \
                        == LocalTrade_list[-3]:
                    Trade_list.append(LocalTrade_list[-1])
                else:
                    Trade_list.append('None')
            else:
                Trade_list.append('None')
        else:
            if genconfig.Trader.TradePersist:
                Trade_list.append('None')
            else:
                Trade_list.append(LocalTrade_list[-1])
    else:
        if genconfig.Trader.TradePersist:
            if len(LocalTrade_list) > 2 and LocalTrade_list[-1] == \
                    LocalTrade_list[-2] and not LocalTrade_list[-2] == \
                    LocalTrade_list[-3]:
                Trade_list.append(LocalTrade_list[-1])
            else:
                Trade_list.append('None')
        else:
            Trade_list.append(LocalTrade_list[-1])
