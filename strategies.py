import genconfig
import hidconfig
import indicators
import strategies

Trade_list = ['None']
LocalTrade_list = []
def Generic():
    # Support for convergence/divergence style trading
    if hidconfig.BidAskList:
        if len(hidconfig.IndicatorBid) >= 1:
                LocalBid = hidconfig.IndicatorBid[-1]
                LocalAsk = hidconfig.IndicatorAsk[-1]
        FilterList = hidconfig.IndicatorBid
    else:
        LocalBid = hidconfig.IndicatorBid
        LocalAsk = hidconfig.IndicatorAsk
        FilterList = hidconfig.IndicatorList

    # Wait until we have enough data to trade off
    if len(FilterList) >= genconfig.TradeDelay:
        if hidconfig.TradeReverse:
            if hidconfig.IndicatorList[-1] > LocalBid:
                LocalTrade_list.append('Buy')
            elif hidconfig.IndicatorList[-1] < LocalAsk:
                LocalTrade_list.append('Sell')
            else:
                LocalTrade_list.append('None')
        else:
            if hidconfig.IndicatorList[-1] < LocalBid:
                LocalTrade_list.append('Buy')
            elif hidconfig.IndicatorList[-1] > LocalAsk:
                LocalTrade_list.append('Sell')
            else:
                LocalTrade_list.append('None')

        if genconfig.SingleTrade and len(LocalTrade_list) >= 2:
            if LocalTrade_list[-1] == LocalTrade_list[-2]:
                Trade_list.append('None')
            else:
                Trade_list.append(LocalTrade_list[-1])
        else:
            Trade_list.append(LocalTrade_list[-1])
