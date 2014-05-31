import math
import os.path
import sqlite3
import time

import genconfig
import okcoin

sqlite_file = genconfig.DatabasePath
sqlite_file += '/MarketHistory_'
sqlite_file += genconfig.TradePair
sqlite_file += str(genconfig.CandleSize)
sqlite_file += 'm.sqlite'
table_name = 'MarketHistory'
candle_type = 'INTEGER'
column0 = 'Candle'
column1 = 'Price'
column2 = 'Time'
column3 = 'Date'

def ConfigureDatabase():
    ''' Acheives the following:
    - Check for database path, otherwise create.
    - Create table with 4 columns:
        Candle: auto incrementing for easy hack since genconfig.CandleSize
                may vary depending on configuration, but operations stay
                the same.
        Price:  Only last trade of asset in currency...that's it!
        Date: YYYY-MM-DD
        Time: HH-MM-SS
    - Looks something like this: | Candle | Price |     Date   |   Time   |
                                 |   1    | 3300  | 2014-03-28 | 13:03:03 |
    ''' 

    os.makedirs(genconfig.DatabasePath,exist_ok=True)

    conn = sqlite3.connect(sqlite_file)
    db = conn.cursor()

    # If table exists, drop it since we don't yet check candle times
    # NOTE: the following exceptions are meant to handle the possibility
    # of interrupting at the wrong time, and leaving a hung sqlite task
    try:
        db.execute("DROP TABLE IF EXISTS '{tn}'".format(tn=table_name))
    except sqlite3.OperationalError:
        print('Database locked. Deleting database.\n \
                In the future, check for hung processes and kill them')
        try:
            os.remove(sqlite_file)
            db.execute("DROP TABLE IF EXISTS '{tn}'".format(tn=table_name))
        except OSError:
            print('Do we have full access to', db_file)

    # NOTE: following column creation should be kept separate for candles.
    # This is all committed together however.

    # Create table with Candle column
    db.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY AUTOINCREMENT)'\
            .format(tn=table_name, nf=column0, ft=candle_type))

    # Add Price column
    db.execute("ALTER TABLE {tn} ADD COLUMN '{cn}'"\
            .format(tn=table_name, cn=column1))

    # Add Time column
    db.execute("ALTER TABLE {tn} ADD COLUMN '{cn}'"\
            .format(tn=table_name, cn=column2))

    # Add Date column
    db.execute("ALTER TABLE {tn} ADD COLUMN '{cn}'"\
            .format(tn=table_name, cn=column3))

    conn.commit()
    conn.close()

def PopulateRow():
    '''Populate Candle, Price, Time, and Date columns'''

    Market = okcoin.MarketData()

    # Due to high liquidity, no fees, and our usage, we will average
    # bid/ask values (which already have low delta)
    MarketAskPrice = Market.ticker(genconfig.TradePair).ask
    MarketBidPrice = Market.ticker(genconfig.TradePair).bid
    MarketPrices = [MarketAskPrice, MarketAskPrice]
    # We must use fsum for accurate floating point addition.
    # As of python 3.5, floating point division is more accurate
    # unlike python 2 (i.e 180.0/100.0 = 1).
    CurrPrice = math.fsum(MarketPrices) / 2

    # Date and Time
    # NOTE: Instead of using sqlite's date/time functionality, we use
    # python's for insert row simplicity to maintain autoincrementing
    # candle column
    CurrDate = time.strftime("%Y/%m/%d")
    CurrTime = time.strftime("%H:%M:%S")

    # Connect/insert new row for new Candle
    conn = sqlite3.connect(sqlite_file)
    db = conn.cursor()

    # Insert fresh candle
    db.execute("INSERT INTO MarketHistory(Price, Time, Date)\
                  VALUES(?,?,?)", (CurrPrice, CurrTime, CurrDate))

    # Get nice info for verbosity
    db.execute("SELECT max(Candle) FROM '{tn}'".format(tn=table_name))
    LastCandle = db.fetchone()[0]
    print("Candle:", LastCandle, "|", "Price:", CurrPrice,\
            genconfig.Currency, "|", "Time:", CurrTime, "|", "Date:",\
            CurrDate)

    # Commit/close
    conn.commit()
    conn.close()
