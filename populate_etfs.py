import datetime
import os
import csv
import re
import config
import alpaca_trade_api as tradeapi
import psycopg2
import psycopg2.extras

# connection to timescale db
connection = psycopg2.connect(
    host=config.DB_HOST,
    database=config.DB_NAME,
    user=config.DB_USER,
    password=config.DB_PASS
    )

# row by row in dict 
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
cursor.execute("select * from stock where is_etf = TRUE")
etfs = cursor.fetchall()
 
wd = os.path.abspath(os.getcwd())
etf_dir = os.path.join(wd, "data\\etfs")
dates = os.listdir(etf_dir)
# print(dates)
for curr_date in dates:
    for etf in etfs:
        with open(f"{etf_dir}\\{curr_date}\\{etf['symbol']}.csv") as f:
            reader = csv.reader(f)
            next(reader) # no header
            for row in reader:
                symbol = row[1]
                ticker = row[3]
                shares = row[5]
                weight = row[7]
                if symbol and len(symbol) == 4:
                    # print(row)
                    cursor.execute("""
                                SELECT * FROM stock WHERE symbol = %s
                                """, (ticker, ))
                    stock = cursor.fetchone()
                    if stock:
                        cursor.execute("""
                                    INSERT INTO etf_holding (etf_id, holding_id, dt, shares, weight)
                                    VALUES (%s, %s, %s, %s, %s)
                                    """, (etf['id'], stock['id'], curr_date, shares, weight))
                        
connection.commit()

            
    