import shelve
import genconfig


class indicators:

  def writelist(ln, key):
    if not key == None:
      db = shelve.open(
          genconfig.Database.Path + '/' + 'indicators.shelf', writeback=True)
      if ln not in db:
        db[ln] = [key]
      else:
        temp = db[ln]
        temp.append(key)
        db[ln] = temp
      db.close()

  def getlist(ln):
    db = shelve.open(
        genconfig.Database.Path + '/' + 'indicators.shelf', writeback=True)
    if ln not in db:
      temp = []
    else:
      temp = db[ln]
    db.close
    return temp
