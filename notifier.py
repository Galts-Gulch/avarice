import logging
from logging import handlers
import os

import genconfig as gc


class Wrapper:

  def Run():
    if gc.Notifier.TextFile.SimulatorRecord:
      TextFile.Simulator()
    if gc.Notifier.TextFile.TradeRecord:
      TextFile.Trader()
    if gc.Simulator.Verbose:
      Printer.Simulator()
    if gc.Trader.Verbose:
      Printer.Trader()


class PrintMsgHandler(logging.Handler):

  def __init__(self):
    logging.Handler.__init__(self)

  def emit(self, record):
    print(record.name.upper() + ':', record.message)


class Printer:

  def Simulator():
    logger = logging.getLogger('simulator')
    logger.setLevel(logging.DEBUG)
    simprinthandler = PrintMsgHandler()
    simprinthandler.setLevel(logging.DEBUG)
    logger.addHandler(simprinthandler)

  def Trader():
    logger = logging.getLogger('trader')
    logger.setLevel(logging.DEBUG)
    tradeprinthandler = PrintMsgHandler()
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
