import asyncio

import websockets


class OKCoinWS:

  Ticker = None
  TickerFirstRun = True

  def __init__(self, url):
    self.url = url

  @asyncio.coroutine
  def initialize(self, pair):
    while True:
      if OKCoinWS.TickerFirstRun:
        OKCoinWS.TickerFirstRun = False
        print('Connecting to OKCoin WebSocket...')
        ws = yield from websockets.connect(self.url)
        if pair == 'btc_cny':
          sockpair = 'btccny'
        elif pair == 'btc_usd':
          sockpair = 'btcusd'
        yield from ws.send("{'event':'addChannel','channel':'ok_" + sockpair + "_ticker'}")
        yield from ws.send("{'event':'addChannel','channel':'ok_" + sockpair + "_ticker'}")
      OKCoinWS.Ticker = yield from ws.recv()
