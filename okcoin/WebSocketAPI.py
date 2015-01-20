import asyncio
import hashlib

import websockets
from websocket import create_connection


class OKCoinWSPublic:

  Ticker = None
  TickerFirstRun = True

  def __init__(self, pair):
    self.pair = pair

  @asyncio.coroutine
  def initialize(self):
    while True:
      if OKCoinWSPublic.TickerFirstRun or not ws.open:
        OKCoinWSPublic.TickerFirstRun = False
        if self.pair == 'btc_cny':
          sockpair = 'btccny'
          url = "wss://real.okcoin.cn:10440/websocket/okcoinapi"
        elif self.pair == 'btc_usd':
          sockpair = 'btcusd'
          url = "wss://real.okcoin.com:10440/websocket/okcoinapi"
        print('Connecting to Public OKCoin WebSocket...')
        ws = yield from websockets.connect(url)
        # Ticker
        yield from ws.send("{'event':'addChannel','channel':'ok_" + sockpair + "_ticker'}")
      OKCoinWSPublic.Ticker = yield from ws.recv()


class OKCoinWSPrivate:

  def __init__(self, pair, api_key='', secret=''):
    self.pair = pair
    self.api_key = api_key
    self.secret = secret
    if self.pair == 'btc_cny':
      self.url = "wss://real.okcoin.cn:10440/websocket/okcoinapi"
    elif self.pair == 'btc_usd':
      self.url = "wss://real.okcoin.com:10440/websocket/okcoinapi"
    print('Connecting to Private OKCoin WebSocket...')
    self.ws = create_connection(self.url)

  def buildMySign(self, params, secretKey):
    sign = ''
    for key in sorted(params.keys()):
      sign += key + '=' + str(params[key]) + '&'
    data = sign + 'secret_key=' + secretKey
    return hashlib.md5(data.encode("utf8")).hexdigest().upper()

  def userinfo(self):
    params = {'api_key': self.api_key}
    sign = self.buildMySign(params, self.secret)
    self.ws.send("{'event':'addChannel', 'channel':'ok_spot" + self.pair[-3:] + "_userinfo',\
                 'parameters':{ 'api_key':'" + self.api_key + "', 'sign':'" + sign + "'} }")
    info = self.ws.recv()
    return info

  def cancelorder(self, order_id):
    params = {'api_key': self.api_key,
              'symbol': self.pair, 'order_id': order_id}
    sign = self.buildMySign(params, self.secret)
    self.ws.send("{'event':'addChannel', 'channel':'ok_spot" + self.pair[-3:]
                 + "cny_cancel_order', 'parameters':{ 'api_key':'" + self.api_key + "',\
                 'sign':'" + sign + "', 'symbol':'" + self.pair
                 + "', 'order_id':'" + order_id + "'} }")

  def trade(self, order, rate, amount):
    params = {'api_key': self.api_key, 'symbol': self.pair,
              'type': order, 'price': rate, 'amount': amount}
    sign = self.buildMySign(params, self.secret)
    self.ws.send("{'event':'addChannel','channel':'ok_spot" + self.pair[-3:]
                 + "_trade','parameters':{'api_key':'" + self.api_key
                 + "','sign':'" + sign + "','symbol':'" + self.pair
                 + "','type':'" + order + "','price':'"
                 + str(rate) + "','amount':'" + str(amount) + "'}}")
    # Don't muck the userinfo with a successful trade message
    self.ws.recv()

  # Subscribes to channel, updates on new trade. Not currently in use, a
  # better place would be in an asyncio.coroutine if ever needed.
  def realtrades(self):
    params = {'api_key': self.api_key}
    sign = self.buildMySign(params, self.secret)
    self.ws.send("{'event':'addChannel','channel':'okspot_" + self.pair[-3:]
                 + "_cancel_order','parameters':{'api_key':'"
                 + self.api_key + "','sign':'" + sign + "', 'symbol':'"
                 + self.pair + "', 'order_id':'-1'} }")
    trades = self.ws.recv()
    return trades
