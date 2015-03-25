import datetime
import math
import os.path
import sqlite3
import time

import avarice
import exchangelayer as el
import genconfig
import genutils
import loggerdb

sqlite_file = genconfig.Database.Path + '/MarketHistory_' + genconfig.API.TradePair \
    + str(genconfig.Candles.Size) + 'm.sqlite'
table_name = 'MarketHistory'
candle_type = 'INTEGER'
column0 = 'Candle'
column1 = 'Bid'
column2 = 'Ask'
column3 = 'Price'
column4 = 'Time'
column5 = 'Date'
column6 = 'DateTime'
AccessErr = 'Avarice needs full access to ' + sqlite_file

ThreadWait = 0
CandleSizeSeconds = genconfig.Candles.Size * 60


def ExtractUsefulLists():
  '''Extracts useful lists from MarketHistory table.
  The lists are useful for loggerdb and externally.
  Returns: NULL since it handles multiple lists which are
  externally accessible'''
  # Connect
  conn = sqlite3.connect(sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES)
  db = conn.cursor()

  # Clear since we otherwise re-populate on top
  loggerdb.candle_list = []
  loggerdb.time_list = []
  loggerdb.datetime_list = []
  loggerdb.price_list = []
  # Create table with Candle column
  db.execute('CREATE TABLE IF NOT EXISTS {tn} ({nf} {ft} PRIMARY KEY AUTOINCREMENT)'
             .format(tn=table_name, nf=column0, ft=candle_type))

  db.execute("SELECT * from '{tn}'".format(tn=table_name))
  # extract column names
  column_names = [d[0] for d in db.description]
  for row in db:
    # build dict
    info = dict(zip(column_names, row))
    try:
      # Build ordered Candle list
      loggerdb.candle_list.append(str(info[column0]))
      # Build ordered Time list
      loggerdb.time_list.append(info[column4])
      # Build ordered DateTime list
      loggerdb.datetime_list.append(info[column6])
      # Build ordered Price list
      loggerdb.price_list.append(info[column3])
    except KeyError:
      print('An update changed database structure.\n \
                    Deleting and starting over')
      try:
        try:
          db.execute(
              "DROP TABLE IF EXISTS '{tn}'".format(tn=table_name))
          conn.commit()
        except sqlite3.OperationalError:
          os.remove(sqlite_file)
          db.execute(
              "DROP TABLE IF EXISTS '{tn}'".format(tn=table_name))
      except OSError:
        print(AccessErr)
  conn.close()


def ConfigureDatabase():
  ''' Achieves the following:
  - Check for database path, otherwise create.
  - Create table with 4 columns:
      Candle: auto incrementing for easy hack since genconfig.Candles.Size
              may vary depending on configuration, but operations stay
              the same.
      Price:  Only last trade of asset in currency...that's it!
      Date: YYYY-MM-DD
      Time: HH-MM-SS
      DateTime: YY-MM-DD HH-MM-SS
  '''

  os.makedirs(genconfig.Database.Path, exist_ok=True)

  conn = sqlite3.connect(sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES)
  db = conn.cursor()

  ExtractUsefulLists()

  # If table exists, check if the last candle is older than our current
  # genconfig.Candles.Size
  # NOTE: the following exceptions are meant to handle the possibility
  # of interrupting at the wrong time, and leaving a hung sqlite task
  if loggerdb.datetime_list:
    Now = datetime.datetime.now()
    LastCandle = loggerdb.datetime_list[-1]
    CandleDelta = Now - LastCandle
    DeltaSeconds = CandleDelta.total_seconds()
    if not DeltaSeconds <= CandleSizeSeconds:
      DropMarketHistoryTable = True
    else:
      loggerdb.ThreadWait = CandleSizeSeconds - DeltaSeconds
      DropMarketHistoryTable = False
  else:
    DropMarketHistoryTable = True

  if DropMarketHistoryTable:
    try:
      db.execute("DROP TABLE IF EXISTS '{tn}'".format(tn=table_name))
    except sqlite3.OperationalError:
      print('Database locked. Deleting database.\n \
                    In the future, check for hung processes and kill them')
      try:
        os.remove(sqlite_file)
        db.execute("DROP TABLE IF EXISTS '{tn}'".format(tn=table_name))
      except OSError:
        print(AccessErr)

    # NOTE: following column creation should be kept separate for candles.
    # This is all committed together however.

    # Create table with Candle column
    db.execute('CREATE TABLE IF NOT EXISTS {tn} ({nf} {ft} PRIMARY KEY AUTOINCREMENT)'
               .format(tn=table_name, nf=column0, ft=candle_type))

    # Add Price columns
    db.execute("ALTER TABLE {tn} ADD COLUMN '{cn}'"
               .format(tn=table_name, cn=column1))
    db.execute("ALTER TABLE {tn} ADD COLUMN '{cn}'"
               .format(tn=table_name, cn=column2))
    db.execute("ALTER TABLE {tn} ADD COLUMN '{cn}'"
               .format(tn=table_name, cn=column3))

    # Add Time column
    db.execute("ALTER TABLE {tn} ADD COLUMN '{cn}'"
               .format(tn=table_name, cn=column4))

    # Add Date column
    db.execute("ALTER TABLE {tn} ADD COLUMN '{cn}'"
               .format(tn=table_name, cn=column5))

    # Add DateTime column
    db.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' timestamp"
               .format(tn=table_name, cn=column6))

    conn.commit()
  else:
    print("Database is recent enough; resuming")
  conn.close()


def PopulateRow():
  '''Populate Candle, Price, Time, and Date columns'''

  # Connect/insert new row for new Candle
  conn = sqlite3.connect(sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES)
  db = conn.cursor()

  # Date and Time
  CurrDate = time.strftime("%Y/%m/%d")
  CurrTime = time.strftime("%H:%M:%S")
  CurrDateTime = datetime.datetime.now()

  # Insert fresh candle
  db.execute("INSERT INTO MarketHistory(Bid, Ask, Price, Time, Date, DateTime)\
                  VALUES(?,?,?,?,?,?)", (el.GetMarketPrice('bid'),
                                         el.GetMarketPrice('ask'),
                                         el.GetMarketPrice('last'),
                                         CurrTime, CurrDate, CurrDateTime))

  # Delete old rows
  if not genconfig.Database.StoreAll:
    for i in ['Candle', 'Bid', 'Ask', 'Price', 'Time', 'Date', 'DateTime']:
      db.execute("DELETE FROM {tn} where {cn} not in\
                (select {cn} from {tn} order by {cn} desc limit {lim})"
                 .format(tn=table_name, cn=i, lim=avarice.MaxCandleDepends))

  # Get nice info for verbosity
  db.execute("SELECT max(Candle) FROM '{tn}'".format(tn=table_name))
  LastCandle = db.fetchone()[0]
  if genconfig.Candles.Verbose:
    print("Candle:", LastCandle, "|", "Price:", el.GetMarketPrice('last'),
          genconfig.API.Currency, "|", "Time:", CurrTime, "|", "Date:",
          CurrDate)

  # Commit/close
  conn.commit()
  conn.close()
