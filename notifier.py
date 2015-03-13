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
