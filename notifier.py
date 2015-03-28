import ast
import http.client
import logging
import os
import urllib
from logging import handlers

from storage import config

if ast.literal_eval(config.gc['Notifier']['XMPP']['Simulator']) or ast.literal_eval(
        config.gc['Notifier']['XMPP']['Trader']):
  from xmpp_logging_handler import XMPPHandler


class Wrapper:

  def Run():
    TextFile.Simulator()
    TextFile.Trader()
    if ast.literal_eval(config.gc['Simulator']['Verbose']):
      Printer.Simulator()
    if ast.literal_eval(config.gc['Trader']['Verbose']):
      Printer.Trader()
    if ast.literal_eval(config.gc['Notifier']['Pushover']['Simulator']):
      Pushover.Simulator()
    if ast.literal_eval(config.gc['Notifier']['Pushover']['Trader']):
      Pushover.Trader()
    if ast.literal_eval(config.gc['Notifier']['TLS SMTP']['Simulator']):
      TlsSMTP.Simulator()
    if ast.literal_eval(config.gc['Notifier']['TLS SMTP']['Trader']):
      TlsSMTP.Trader()
    if ast.literal_eval(config.gc['Notifier']['SMTP']['Simulator']):
      SMTP.Simulator()
    if ast.literal_eval(config.gc['Notifier']['SMTP']['Trader']):
      SMTP.Trader()
    if ast.literal_eval(config.gc['Notifier']['XMPP']['Simulator']):
      XMPP.Simulator()
    if ast.literal_eval(config.gc['Notifier']['XMPP']['Trader']):
      XMPP.Trader()


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
                     "token": config.gc['Notifier']['Pushover']['App Token'],
                     "user": config.gc['Notifier']['Pushover']['User Key'],
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
    os.makedirs(config.gc['Notifier']['Text File']['Path'], exist_ok=True)
    logger = logging.getLogger('simulator')
    logger.setLevel(logging.DEBUG)
    simhandler = handlers.TimedRotatingFileHandler(
        config.gc['Notifier']['Text File']['Path'] + '/' +
        config.gc['Notifier']['Text File']['Simulator File Name'],
        when='h', interval=int(config.gc['Notifier']['Text File']['Rollover Time']),
        backupCount=int(config.gc['Notifier']['Text File']['Backup Count']))
    simhandler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    simhandler.setFormatter(formatter)
    logger.addHandler(simhandler)

  def Trader():
    os.makedirs(config.gc['Notifier']['Text File']['Path'], exist_ok=True)
    logger = logging.getLogger('trader')
    logger.setLevel(logging.DEBUG)
    tradehandler = handlers.TimedRotatingFileHandler(
        config.gc['Notifier']['Text File']['Path'] + '/' +
        config.gc['Notifier']['Text File']['Trader File Name'],
        when='h', interval=int(config.gc['Notifier']['Text File']['Rollover Time']),
        backupCount=int(config.gc['Notifier']['Text File']['Backup Count']))
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
    t = config.gc['Notifier']['TLS SMTP']
    simgm = TlsSMTPHandler((t['Host'], int(t['Port'])), t['To'], [t['To']],
                           'Avarice Simulator', (t['Username'], t['Password']))
    simgm.setLevel(logging.DEBUG)
    logger.addHandler(simgm)

  def Trader():
    logger = logging.getLogger('trader')
    logger.setLevel(logging.DEBUG)
    t = config.gc['Notifier']['TLS SMTP']
    tradergm = TlsSMTPHandler((t['Host'], int(t['Port'])), t['To'], [t['To']],
                              'Avarice Trader', (t['Username'], t['Password']))
    tradergm.setLevel(logging.DEBUG)
    logger.addHandler(tradergm)


class SMTP:

  def Simulator():
    logger = logging.getLogger('simulator')
    logger.setLevel(logging.DEBUG)
    s = config.gc['Notifier']['SMTP']
    simsmtphandler = handlers.SMTPHandler(s['Host'], s['From'], s['To'],
                                          'Avarice Simulator')
    simsmtphandler.setLevel(logging.DEBUG)
    logger.addHandler(simsmtphandler)

  def Trader():
    logger = logging.getLogger('trader')
    logger.setLevel(logging.DEBUG)
    s = config.gc['Notifier']['SMTP']
    tradersmtphandler = handlers.SMTPHandler(s['Host'], s['From'], s['To'],
                                          'Avarice Trader')
    tradersmtphandler.setLevel(logging.DEBUG)
    logger.addHandler(tradersmtphandler)


class XMPP:

  def Simulator():
    logger = logging.getLogger('simulator')
    logger.setLevel(logging.DEBUG)
    x = config.gc['Notifier']['XMPP']
    simxmpphandler = XMPPHandler(x['Username'], x['Password'], [x['Recipient']],
                                 x['Host'], x['Server'], int(x['Port']),
                                 x['Name'] + ' Simulator')
    simxmpphandler.setLevel(logging.DEBUG)
    logger.addHandler(simxmpphandler)

  def Trader():
    logger = logging.getLogger('trader')
    logger.setLevel(logging.DEBUG)
    x = config.gc['Notifier']['XMPP']
    traderxmpphandler = XMPPHandler(x['Username'], x['Password'], [x['Recipient']],
                                 x['Host'], x['Server'], int(x['Port']),
                                 x['Name'] + ' Trader')
    traderxmpphandler.setLevel(logging.DEBUG)
    logger.addHandler(traderxmpphandler)
