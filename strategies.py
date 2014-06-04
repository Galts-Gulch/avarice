import genconfig
import hidconfig
import indicators
import strategies

Trade = 'stub'
def Generic():
    # Support for convergence/divergence style trading
    if hidconfig.BidAskList:
        # Wait until we have enough data to trade off
        print(hidconfig.IndicatorBid)
        if len(hidconfig.IndicatorBid) >= genconfig.TradeDelay:
            if hidconfig.IndicatorList[-1] < hidconfig.IndicatorBid[-1]:
                strategies.Trade = 'Buy'
            elif hidconfig.IndicatorList[-1] > hidconfig.IndicatorAsk[-1]:
                strategies.Trade = 'Sell'
    else:
        # Wait until we have enough data to trade off
        if len(hidconfig.IndicatorList) >= genconfig.TradeDelay:
            if hidconfig.IndicatorList[-1] < hidconfig.IndicatorBid[-1]:
                strategies.Trade = 'Buy'
            elif hidconfig.IndicatorList[-1] > hidconfig.IndicatorAsk[-1]:
                strategies.Trade = 'Sell'
