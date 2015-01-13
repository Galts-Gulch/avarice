import hashlib

import requests
import simplejson

import exchangelayer as el


class TickerObject(object):

  def __init__(self, data):
    self.bid = float(data['ticker']['buy'])
    self.ask = float(data['ticker']['sell'])
    if('high' in data):
      self.high = float(data['ticker']['high'])
      self.low = float(data['ticker']['low'])
      self.last = float(data['ticker']['last'])
      self.volume = float(data['ticker']['volume'])


class DepthObject(object):

  def __init__(self, data):
    self.asks = {}
    for l in data['asks']:
      self.asks[l[0]] = l[1]
    self.bids = {}
    for l in data['bids']:
      self.bids[l[0]] = l[1]


class MarketData(object):

  def __init__(self):
    self.http = requests.Session()

  def get_json(self, url, params):
    r = self.http.get(url, params=params)
    data = simplejson.loads(r.content)
    return(data)

  def ticker(self, symbol):
    params = {'symbol': symbol}
    ticker_url = el.urlpre + '/api/ticker.do'
    if symbol == 'btc_usd' or symbol == 'ltc_usd':
      params['ok'] = 1
    data = self.get_json(ticker_url, params)
    return(TickerObject(data))

  def get_depth(self, symbol):
    params = {'symbol': symbol}
    depth_url = el.urlpre + 'api/depth.do'
    if symbol == 'btc_usd' or symbol == 'ltc_usd':
      params['ok'] = 1
    data = self.get_json(depth_url, params)
    return(DepthObject(data))

  def get_history(self, symbol):
    params = {'symbol': symbol}
    if symbol == 'btc_usd' or symbol == 'ltc_usd':
      params['ok'] = 1
    history_url = el.urlpre + 'api/trades.do'
    return(self.get_json(history_url, params))

  def future_ticker(self, symbol, contract):
    params = {'symbol': symbol,
              'contractType': contract}
    url = el.urlpre + 'api/future_ticker.do'
    return self.get_json(url, params)


class TradeAPI(MarketData):

  def __init__(self, partner, secret):
    MarketData.__init__(self)
    self.partner = partner
    self.secret = secret

    # partner is integer, secret is string

  def _post(self, params, url):

    # params does not include the signed part, we add that

    sign_string = ''

    for pos, key in enumerate(sorted(params.keys())):
      sign_string += key + '=' + str(params[key])
      if(pos != len(params) - 1):
        sign_string += '&'

    sign_string += self.secret
    m = hashlib.md5()
    m.update(sign_string.encode('utf-8'))
    signed = m.hexdigest().upper()

    params['sign'] = signed

    req = self.http.post(url, params=params)
    result = simplejson.loads(req.content)

    success = result['result']
    if(not success):
      print('Error: ' + str(result['errorCode']))
      print(self.error_code_meaning(result['errorCode']))
      return(result)
    else:
      return(result)

  def get_info(self):
    params = {'partner': self.partner}
    user_info_url = el.urlpre + 'api/userinfo.do'
    return(self._post(params, user_info_url))

  def trade(self, symbol, trade_type, rate, amount):
    params = {'partner': self.partner,
              'symbol': symbol,
              'type': trade_type,
              'rate': rate,
              'amount': amount}
    trade_url = el.urlpre + 'api/trade.do'
    return(self._post(params, trade_url))

  def cancel_order(self, order_id, symbol):
    params = {'partner': self.partner,
              'order_id': order_id,
              'symbol': symbol}
    cancel_order_url = el.urlpre + 'api/cancelorder.do'
    return(self._post(params, cancel_order_url))

  def get_order(self, order_id, symbol):
    params = {'partner': self.partner,
              'order_id': order_id,
              'symbol': symbol}
    get_order_url = el.urlpre + 'api/getorder.do'
    return(self._post(params, get_order_url))

  def error_code_meaning(self, error_code):
    codes = {10000: 'Required parameter can not be null',
             10001: 'Requests are too frequent',
             10002: 'System Error',
             10003: 'Restricted list request, please try again later',
             10004: 'IP restriction',
             10005: 'Key does not exist',
             10006: 'User does not exist',
             10007: 'Signatures do not match',
             10008: 'Illegal parameter',
             10009: 'Order does not exist',
             10010: 'Insufficient balance',
             10011: 'Order is less than minimum trade amount',
             10012: 'Unsupported symbol (not btc_cny or ltc_cny)',
             10013: 'This interface only accepts https requests'}
    return(codes[error_code])

  def get_future_info(self):
    params = {'partner': self.partner}
    user_info_url = el.urlpre + 'api/future_userinfo.do'
    return(self._post(params, user_info_url))

  def get_future_holdings(self, symbol):
    params = {'partner': self.partner,
              'symbol': symbol}
    holdings_url = el.urlpre + 'api/future_position.do'
    return(self._post(params, holdings_url))

  def future_trade(self, symbol, contract, price, amount, type):
    params = {'partner': self.partner,
              'symbol': symbol,
              'contractType': contract,
              'price': price,
              'amount': amount,
              'type': type,
              'matchPrice': 0}
    url = el.urlpre + 'api/future_trade.do'
    return(self._post(params, url))
