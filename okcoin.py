# OKCoin api
# https://www.okcoin.com/t-1000097.html
# https://www.okcoin.com/t-1000052.html

import urllib.request, urllib.parse, urllib.error
import hashlib
import simplejson
from time import time

class TickerObject(object):

    def __init__(self,data):
        self.bid = float(data['ticker']['buy'])
        self.ask = float(data['ticker']['sell'])
        self.high = float(data['ticker']['high'])
        self.low = float(data['ticker']['low'])
        self.last = float(data['ticker']['last'])
        self.volume = float(data['ticker']['vol'])

class DepthObject(object):

    def __init__(self,data):
        self.asks = {}
        for l in data['asks']:
            self.asks[l[0]] = l[1]
        self.bids = {}
        for l in data['bids']:
            self.bids[l[0]] = l[1]   
    
class MarketData(object):

    def get_json(self, url):
        response = urllib.request.urlopen(url)
        data = simplejson.load(response)
        return(data)
        
    def ticker(self, symbol='btc_cny'):
        btc_ticker_url = 'https://www.okcoin.com/api/ticker.do?symbol=btc_cny'
        ltc_ticker_url = 'https://www.okcoin.com/api/ticker.do?symbol=ltc_cny'
        if( symbol == 'btc_cny' ):
            data = self.get_json(btc_ticker_url)
            return( TickerObject(data) )
        if( symbol == 'ltc_cny' ):
            data = self.get_json(ltc_ticker_url)
            return( TickerObject(data) )
        if( symbol == 'ltc_btc' ):
            btc_data = self.get_json(btc_ticker_url)
            ltc_data = self.get_json(ltc_ticker_url)
            ltc_btc_bid = round( float(ltc_data['ticker']['buy']) / float(btc_data['ticker']['sell']), 8 )
            ltc_btc_ask = round( float(ltc_data['ticker']['sell']) / float(btc_data['ticker']['buy']), 8 )
            data = { 'ticker' : {"sell" : ltc_btc_ask, "buy" : ltc_btc_bid} }
            return( TickerObject(data) )
        else:
            print(('Unrecognized symbol: ' + symbol))

    def get_depth(self, symbol='btc_cny'):
        btc_depth_url = 'https://www.okcoin.com/api/depth.do?symbol=btc_cny'
        ltc_depth_url = 'https://www.okcoin.com/api/depth.do?symbol=ltc_cny'
        if( symbol == 'btc_cny' ):
            data = self.get_json(btc_depth_url)
            return( DepthObject(data) )
        if( symbol == 'ltc_cny' ):
            data = self.get_json(ltc_depth_url)
            return( DepthObject(data) )
        else:
            print(('Unrecognized symbol: ' + symbol))

    def get_history(self, symbol='btc_cny', since=None):
        str_since = ('&since=' + str(since)) if isinstance(since,int) else ''
        history_url = 'https://www.okcoin.com/api/trades.do?symbol='
        if( symbol == 'btc_cny' or symbol == 'ltc_cny'):
            return( self.get_json(history_url + symbol + str_since) )
        else:
            print(('Unrecognized symbol: ' + symbol))

    def get_closingtrades(self, n, N, symbol='btc_cny'):
        clstrades = [None] * N
    
        timemark = int( time() )
        i = 0
        passtrade = self.get_history(symbol=symbol)
        oldesttid = passtrade[0]['tid']

        for j in range(0, N):
            #print 'timemark =', timemark ####debug
            #print ' j =', j ####debug
            while True:
                i -= 1

                if i < -len(passtrade):
                    passtrade = self.get_history(symbol=symbol, since = oldesttid - int( len(passtrade)*1.9 ) );
                    newotid = passtrade[0]['tid']
                    while oldesttid > passtrade[-1]['tid']:
                        passtrade = self.get_history(symbol=symbol, since = newotid +2 )
                        newotid = passtrade[0]['tid']
                    oldesttid = newotid
                    i = -1
                #print ' i =', i ####debug

                if timemark - passtrade[i]['date'] > 0 and timemark - passtrade[i]['date'] <= n:
                    clstrades[j] = passtrade[i]
                    timemark -= n
                    break
                elif timemark - passtrade[i]['date'] > n:
                    i += 1
                    timemark -= n
                    break

        return clstrades

class TradeAPI(object):
    
    def __init__(self, partner, secret):
        
        self.partner = partner
        self.secret = secret

        # partner is integer, secret is string

    def _post(self, params, url):
        
        # params does not include the signed part, we add that
        
        sign_string = ''
        
        for pos,key in enumerate(sorted(params.keys())):
            sign_string += key + '=' + str(params[key])
            if( pos != len(params) - 1 ):
                sign_string += '&'
                
        sign_string += self.secret
        m = hashlib.md5()
        m.update(sign_string.encode('utf-8'))
        signed = m.hexdigest().upper()

        params['sign'] = signed

        data = urllib.parse.urlencode(params)
        binary_data = data.encode('utf-8')
        req = urllib.request.Request(url, binary_data)
        response = urllib.request.urlopen(req)
        result = simplejson.load(response)

        success = result['result']
        if( not success ):
            print(('Error: ' + str(result['errorCode'])))
            print(( self.error_code_meaning(result['errorCode']) ))
            return(result)
        else:
            return(result)

    def get_info(self):
        params = {'partner' : self.partner}
        user_info_url = 'https://www.okcoin.com/api/userinfo.do'
        return(self._post(params, user_info_url))

    def trade(self, trade_type, rate, amount, symbol='btc_cny'):
        params = { 'partner' : self.partner,
                   'symbol' : symbol,
                   'type' : trade_type,
                   'rate' : rate,
                   'amount' : amount }
        trade_url = 'https://www.okcoin.com/api/trade.do'
        return(self._post(params, trade_url))

    def cancel_order(self, order_id, symbol):
        params = { 'partner' : self.partner,
                   'order_id' : order_id,
                   'symbol' : symbol }
        cancel_order_url = 'https://www.okcoin.com/api/cancelorder.do'
        return(self._post(params, cancel_order_url))

    def get_order(self, order_id, symbol):
        params = { 'partner' : self.partner,
                   'order_id' : order_id,
                   'symbol' : symbol }
        get_order_url = 'https://www.okcoin.com/api/getorder.do'
        return(self._post(params, get_order_url))

    def error_code_meaning(self, error_code):
        codes = { 10000 : 'Required parameter can not be null',
                  10001 : 'Requests are too frequent',
                  10002 : 'System Error',
                  10003 : 'Restricted list request, please try again later',
                  10004 : 'IP restriction',
                  10005 : 'Key does not exist',
                  10006 : 'User does not exist',
                  10007 : 'Signatures do not match',
                  10008 : 'Illegal parameter',
                  10009 : 'Order does not exist',
                  10010 : 'Insufficient balance',
                  10011 : 'Order is less than minimum trade amount',
                  10012 : 'Unsupported symbol (not btc_cny or ltc_cny)',
                  10013 : 'This interface only accepts https requests' }
        return( codes[error_code] )
