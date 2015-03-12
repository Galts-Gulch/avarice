import logging
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
    simhandler = logging.FileHandler(
        gc.Notifier.TextFile.Path + '/' + gc.Notifier.TextFile.SimName)
    simhandler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    simhandler.setFormatter(formatter)
    logger.addHandler(simhandler)

  def Trader():
    os.makedirs(gc.Notifier.TextFile.Path, exist_ok=True)
    logger = logging.getLogger('trader')
    logger.setLevel(logging.DEBUG)
    tradehandler = logging.FileHandler(
        gc.Notifier.TextFile.Path + '/' + gc.Notifier.TextFile.TradeName)
    tradehandler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    tradehandler.setFormatter(formatter)
    logger.addHandler(tradehandler)
