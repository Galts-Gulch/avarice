import http.client
import logging
import os
import urllib
from logging import handlers

import genconfig as gc


class Wrapper:

  def Run():
    if gc.Notifier.TextFile.Simulator:
      TextFile.Simulator()
    if gc.Notifier.TextFile.Trader:
      TextFile.Trader()
    if gc.Simulator.Verbose:
      Printer.Simulator()
    if gc.Trader.Verbose:
      Printer.Trader()
    if gc.Notifier.Pushover.Simulator:
      Pushover.Simulator()
    if gc.Notifier.Pushover.Trader:
      Pushover.Trader()
    if gc.Notifier.SMTP.Simulator:
      SMTP.Simulator()
    if gc.Notifier.SMTP.Trader:
      SMTP.Trader()


class PrintHandler(logging.Handler):

  def __init__(self):
    logging.Handler.__init__(self)

  def emit(self, record):
    print(record.name.upper() + ':', record.message)


class PushoverHandler(logging.Handler):

  def __init__(self):
    logging.Handler.__init__(self)

  def emit(self, record):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
                 urllib.parse.urlencode({
                     "token": gc.Notifier.Pushover.AppToken,
                     "user": gc.Notifier.Pushover.UserKey,
                     "message": record.name.upper() + ': ' + record.message,
                 }), {"Content-type": "application/x-www-form-urlencoded"})
    conn.getresponse()


class Printer:

  def Simulator():
    logger = logging.getLogger('simulator')
    logger.setLevel(logging.DEBUG)
    simprinthandler = PrintHandler()
    simprinthandler.setLevel(logging.DEBUG)
    logger.addHandler(simprinthandler)

  def Trader():
    logger = logging.getLogger('trader')
    logger.setLevel(logging.DEBUG)
    tradeprinthandler = PrintHandler()
    tradeprinthandler.setLevel(logging.DEBUG)
    logger.addHandler(tradeprinthandler)


class TextFile:

  def Simulator():
    os.makedirs(gc.Notifier.TextFile.Path, exist_ok=True)
    logger = logging.getLogger('simulator')
    logger.setLevel(logging.DEBUG)
    simhandler = handlers.TimedRotatingFileHandler(
        gc.Notifier.TextFile.Path + '/' + gc.Notifier.TextFile.SimName,
        when='h', interval=gc.Notifier.TextFile.RolloverTime)
    simhandler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    simhandler.setFormatter(formatter)
    logger.addHandler(simhandler)

  def Trader():
    os.makedirs(gc.Notifier.TextFile.Path, exist_ok=True)
    logger = logging.getLogger('trader')
    logger.setLevel(logging.DEBUG)
    tradehandler = handlers.TimedRotatingFileHandler(
        gc.Notifier.TextFile.Path + '/' + gc.Notifier.TextFile.TradeName,
        when='h', interval=gc.Notifier.TextFile.RolloverTime)
    tradehandler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    tradehandler.setFormatter(formatter)
    logger.addHandler(tradehandler)


class Pushover:

  def Simulator():
    logger = logging.getLogger('simulator')
    logger.setLevel(logging.DEBUG)
    simpushoverhandler = PushoverHandler()
    simpushoverhandler.setLevel(logging.DEBUG)
    logger.addHandler(simpushoverhandler)

  def Trader():
    logger = logging.getLogger('trader')
    logger.setLevel(logging.DEBUG)
    tradepushoverhandler = PushoverHandler()
    tradepushoverhandler.setLevel(logging.DEBUG)
    logger.addHandler(tradepushoverhandler)


class SMTP:

  def Simulator():
    logger = logging.getLogger('simulator')
    logger.setLevel(logging.DEBUG)
    simsmtphandler = handlers.SMTPHandler(
        gc.Notifier.SMTP.Host, gc.Notifier.SMTP.From, gc.Notifier.SMTP.To,
        'Avarice ' + 'Simulator')
    simsmtphandler.setLevel(logging.DEBUG)
    logger.addHandler(simsmtphandler)

  def Trader():
    logger = logging.getLogger('trader')
    logger.setLevel(logging.DEBUG)
    tradersmtphandler = handlers.SMTPHandler(
        gc.Notifier.SMTP.Host, gc.Notifier.SMTP.From, gc.Notifier.SMTP.To,
        'Avarice ' + 'Trader')
    tradersmtphandler.setLevel(logging.DEBUG)
    logger.addHandler(tradersmtphandler)
