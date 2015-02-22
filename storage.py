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
        db[ln] = temp
      db.close()

  def getlist(ln):
    db = shelve.open(indicators.indshelve, writeback=True)
    if ln not in db:
      temp = []
    else:
      temp = db[ln]
    db.close
    return temp
