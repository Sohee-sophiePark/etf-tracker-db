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

# converted into dict format for cursor
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor) 

api = tradeapi.REST(config.KEY_ID,
                    config.SECRET_KEY,
                    base_url=config.API_URL)

assets = api.list_assets()
for asset in assets:
    print(f"Stock Inserted {asset.name} {asset.symbol}")
    cursor.execute(
        """
        INSERT INTO stock (name, symbol, exchange, is_etf)
        VALUES (%s, %s, %s, false)
        """
    , (asset.name, asset.symbol, asset.exchange))    
    
connection.commit()