import asyncio
import hashlib
import json
import re
import ssl
import websocket
import websockets


class OKCoinWSPublic:

  Ticker = None

  def __init__(self, pair, verbose):
    self.pair = pair
    self.verbose = verbose

  @asyncio.coroutine
  def initialize(self):
    TickerFirstRun = True
    while True:
      if TickerFirstRun or not ws.open:
        TickerFirstRun = False
        sockpair = re.sub(r'[\W_]+', '', self.pair)
        if self.pair[-3:] == 'cny':
          url = "wss://real.okcoin.cn:10440/websocket/okcoinapi"
        elif self.pair[-3:] == 'usd':
          url = "wss://real.okcoin.com:10440/websocket/okcoinapi"
        if self.verbose:
          print('Connecting to Public OKCoin WebSocket...')
        try:
          ws = yield from websockets.connect(url)
          # Ticker
          yield from ws.send("{'event':'addChannel','channel':'ok_" + sockpair + "_ticker'}")
        except Exception:
          TickerFirstRun = True
      OKCoinWSPublic.Ticker = yield from ws.recv()


class OKCoinWSPrivate:
  TradeOrderID = None

  def __init__(self, pair, verbose, api_key='', secret=''):
    self.pair = pair
    self.verbose = verbose
    self.api_key = api_key
    self.secret = secret
    if self.pair[-3:] == 'cny':
      self.url = "wss://real.okcoin.cn:10440/websocket/okcoinapi"
    elif self.pair[-3:] == 'usd':
      self.url = "wss://real.okcoin.com:10440/websocket/okcoinapi"
    if self.verbose:
      print('Connecting to Private OKCoin WebSocket...')
    notconnected = True
    while notconnected:
      try:
        self.ws = websocket.create_connection(self.url)
        notconnected = False
      except Exception:
        pass

  def buildMySign(self, params, secretKey):
    sign = ''
    for key in sorted(params.keys()):
      sign += key + '=' + str(params[key]) + '&'
    data = sign + 'secret_key=' + secretKey
    return hashlib.md5(data.encode("utf8")).hexdigest().upper()

  def userinfo(self):
    params = {'api_key': self.api_key}
    sign = self.buildMySign(params, self.secret)
    try:
      self.ws.send("{'event':'addChannel', 'channel':'ok_spot" + self.pair[-3:] + "_userinfo',\
                   'parameters':{ 'api_key':'" + self.api_key + "', 'sign':'" + sign + "'} }")
      info = self.ws.recv()
    except (websocket._exceptions.WebSocketTimeoutException,
            websocket._exceptions.WebSocketConnectionClosedException, ssl.SSLError,
            ConnectionResetError):
      self.ws = websocket.create_connection(self.url)
      self.ws.send("{'event':'addChannel', 'channel':'ok_spot" + self.pair[-3:] + "_userinfo',\
                   'parameters':{ 'api_key':'" + self.api_key + "', 'sign':'" + sign + "'} }")
      info = self.ws.recv()
    return info

  def cancelorder(self, order_id):
    params = {'api_key': self.api_key,
              'symbol': self.pair, 'order_id': order_id}
    sign = self.buildMySign(params, self.secret)
    try:
      try:
        self.ws.send("{'event':'addChannel', 'channel':'ok_spot" + self.pair[-3:]
                     +
                     "_cancel_order', 'parameters':{ 'api_key':'" +
                     self.api_key
                     + "', 'sign':'" + sign + "', 'symbol':'" + self.pair
                     + "', 'order_id':'" + order_id + "'} }")
        # Don't muck up userinfo with executed order_id
        self.ws.recv()
      except (websocket._exceptions.WebSocketTimeoutException,
              websocket._exceptions.WebSocketConnectionClosedException, ssl.SSLError,
              ConnectionResetError):
        self.ws = websocket.create_connection(self.url)
        self.ws.send("{'event':'addChannel', 'channel':'ok_spot" + self.pair[-3:]
                     +
                     "_cancel_order', 'parameters':{ 'api_key':'" +
                     self.api_key
                     + "', 'sign':'" + sign + "', 'symbol':'" + self.pair
                     + "', 'order_id':'" + order_id + "'} }")
        # Don't muck up userinfo with executed order_id
        self.ws.recv()
    # If trading throws an error, we don't store an OrderID so there's no
    # order to cancel.
    except TypeError:
      pass

  def trade(self, order, rate, amount):
    params = {'api_key': self.api_key, 'symbol': self.pair,
              'type': order, 'price': rate, 'amount': amount}
    sign = self.buildMySign(params, self.secret)
    try:
      self.ws.send("{'event':'addChannel','channel':'ok_spot" + self.pair[-3:]
                   + "_trade','parameters':{'api_key':'" + self.api_key
                   + "','sign':'" + sign + "','symbol':'" + self.pair
                   + "','type':'" + order + "','price':'"
                   + str(rate) + "','amount':'" + str(amount) + "'}}")
    except (websocket._exceptions.WebSocketTimeoutException,
            websocket._exceptions.WebSocketConnectionClosedException, ssl.SSLError,
            ConnectionResetError):
      self.ws = websocket.create_connection(self.url)
      self.ws.send("{'event':'addChannel','channel':'ok_spot" + self.pair[-3:]
                   + "_trade','parameters':{'api_key':'" + self.api_key
                   + "','sign':'" + sign + "','symbol':'" + self.pair
                   + "','type':'" + order + "','price':'"
                   + str(rate) + "','amount':'" + str(amount) + "'}}")
    try:
      OKCoinWSPrivate.TradeOrderID = json.loads(
          self.ws.recv())[-1]['data']['order_id']
    except KeyError:
      pass  # Some error code instead (probably insufficient balance).

  # Subscribes to channel, updates on new trade. Not in use since we store
  # the order_id from trade
  def realtrades(self):
    params = {'api_key': self.api_key}
    sign = self.buildMySign(params, self.secret)
    self.ws.send("{'event':'addChannel','channel':'okspot_" + self.pair[-3:]
                 + "_cancel_order','parameters':{'api_key':'"
                 + self.api_key + "','sign':'" + sign + "', 'symbol':'"
                 + self.pair + "', 'order_id':'-1'} }")
    trades = self.ws.recv()
    return trades
