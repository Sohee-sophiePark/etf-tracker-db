from json import decoder
from psaw import PushshiftAPI
import psycopg2
import psycopg2.extras
import datetime
import os
from time import monotonic
import csv
import config

from requests.models import DecodeError, encode_multipart_formdata


# db setup
conn = psycopg2.connect(host=config.DB_HOST, 
                        database=config.DB_NAME,
                        user=config.DB_USER,
                        password=config.DB_PASS)

# dict-like cursor for accessing to attributes of records 
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cursor.execute("""
               SELECT * FROM stock
               """)
rows = cursor.fetchall()
stocks = {}
for row in rows:
    stocks['$'+row['symbol']] = row['id']  

# for (key, value) in stocks.items():
#     print(f"{key}, {value}")
#     # print(f"${row.symbol}")
    

# get PushshiftAPI instance
api = PushshiftAPI()

# get current date (year / month / day) for timestamp
curr_date = datetime.date.today()
year = curr_date.year
mon = curr_date.month
day = curr_date.day
# print(f"year: {year}, month: {mon}, day: {day}")

start_epoch = int(datetime.datetime(year, mon, day).timestamp())
# print(start_epoch)

submissions = list(api.search_submissions(after=start_epoch,
                                          subreddit='wallstreetbets',
                                          filter=['url', 'author', 'title', 'subreddit'],
                                          limit=10),)


with open('web.txt', 'w', encoding='utf-8', newline='') as fout:
    for submission in submissions:
        # print(submission.title.split())
        
        writer = csv.writer(fout)
        writer.writerow([submission.created_utc])
        writer.writerow([submission.title])
        writer.writerow([submission.url])
        
        words = submission.title.split()
        cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))
        
        if len(cashtags) > 0:
            # print(f"cashtag: {cashtags}")
            # print(submission.title)
            
            for cashtag in cashtags:
                submitted_time = datetime.datetime.fromtimestamp(submission.created_utc).isoformat()
                
                
                # print("test here: ")
                # print(f"submitted time: {submitted_time}")
                # print(f"stocks[cashtag]: {stocks[cashtag]}")
                # print("submission title: "+submission.title)
                # print("submission url: "+submission.url)
                # print("test ends")
                try:
                    cursor.execute("""
                                   INSERT INTO mention (dt, stock_id, message, source, url)
                                   VALUES (%s, %s, %s, 'wallstreetbets', %s )
                                   """, (submitted_time, stocks[cashtag], str(submission.title), str(submission.url)))
                except Exception as e:
                    print(e)
                    conn.rollback()
            
            conn.commit()
            

        

        
        
        
        
    

    
    

