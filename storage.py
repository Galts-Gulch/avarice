import avarice
import shelve
import genconfig


class indicators:

  indshelve = genconfig.Database.Path + '/' + genconfig.API.TradePair + str(
      genconfig.Candles.Size) + 'indicators.shelve'

  def writelist(ln, key):
    if not key == None:
      db = shelve.open(indicators.indshelve, writeback=True)
      if ln not in db:
        db[ln] = [key]
      else:
        temp = db[ln]
        temp.append(key)
        if genconfig.Database.StoreAll:
          db[ln] = temp
        else:
          db[ln] = temp[-avarice.MaxCandleDepends:]
      db.close()

  def getlist(ln):
    db = shelve.open(indicators.indshelve, writeback=True)
    if ln not in db:
      temp = []
    else:
      try:
        temp = db[ln]
      except EOFError:
        try:
          temp = db[ln]
        except EOFError:
          temp = []
    db.close
    return temp
