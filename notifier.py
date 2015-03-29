import http.client
import logging
import os
import urllib
from logging import handlers

import genconfig as gc


class Wrapper:

  def Run():
    TextFile.Simulator()
    TextFile.Trader()
    if gc.Simulator.Verbose:
      Printer.Simulator()
    if gc.Trader.Verbose:
      Printer.Trader()
    if gc.Notifier.Pushover.Simulator:
      Pushover.Simulator()
    if gc.Notifier.Pushover.Trader:
      Pushover.Trader()
    if gc.Notifier.TlsSMTP.Simulator:
      TlsSMTP.Simulator()
    if gc.Notifier.TlsSMTP.Trader:
      TlsSMTP.Trader()
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


class TlsSMTPHandler(logging.handlers.SMTPHandler):

  def emit(self, record):
    import smtplib
    try:
      from email.utils import formatdate
    except ImportError:
      formatdate = self.date_time
    port = self.mailport
    if not port:
      port = smtplib.SMTP_PORT
    smtp = smtplib.SMTP(self.mailhost, port)
    msg = self.format(record)
    msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
          self.fromaddr,
          self.toaddrs,
          self.getSubject(record),
          formatdate(), msg)
    if self.username:
      smtp.ehlo()
      smtp.starttls()
      smtp.ehlo()
      smtp.login(self.username, self.password)
    smtp.sendmail(self.fromaddr, self.toaddrs, msg)
    smtp.quit()


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
        when='h', interval=gc.Notifier.TextFile.RolloverTime,
        backupCount=gc.Notifier.TextFile.BackupCount)
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
        when='h', interval=gc.Notifier.TextFile.RolloverTime,
        backupCount=gc.Notifier.TextFile.BackupCount)
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


class TlsSMTP:

  def Simulator():
    logger = logging.getLogger('simulator')
    logger.setLevel(logging.DEBUG)
    simgm = TlsSMTPHandler((gc.Notifier.TlsSMTP.Host, gc.Notifier.TlsSMTP.Port),
                           gc.Notifier.TlsSMTP.To, [gc.Notifier.TlsSMTP.To],
                           'Avarice Simulator', (gc.Notifier.TlsSMTP.Username,
                                                 gc.Notifier.TlsSMTP.Password))
    simgm.setLevel(logging.DEBUG)
    logger.addHandler(simgm)

  def Trader():
    logger = logging.getLogger('trader')
    logger.setLevel(logging.DEBUG)
    tradergm = TlsSMTPHandler((gc.Notifier.TlsSMTP.Host, gc.Notifier.TlsSMTP.Port),
                              gc.Notifier.TlsSMTP.To, [gc.Notifier.TlsSMTP.To],
                              'Avarice Trader', (gc.Notifier.TlsSMTP.Username,
                                                 gc.Notifier.TlsSMTP.Password))
    tradergm.setLevel(logging.DEBUG)
    logger.addHandler(tradergm)


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
