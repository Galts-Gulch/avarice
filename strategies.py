import genconfig
import hidconfig
import indicators
import strategies

Trade = 'stub'
def Generic():
    # Support for convergence/divergence style trading
    if hidconfig.BidAskList:
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
                strategies.Trade = 'Buy'
            elif hidconfig.IndicatorList[-1] < LocalAsk:
                strategies.Trade = 'Sell'
        else:
            if hidconfig.IndicatorList[-1] < LocalBid:
                strategies.Trade = 'Buy'
            elif hidconfig.IndicatorList[-1] > LocalAsk:
                strategies.Trade = 'Sell'
