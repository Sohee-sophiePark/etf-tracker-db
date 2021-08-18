
--DROP TABLE stock;
CREATE TABLE IF NOT EXISTS stock (
    id SERIAL PRIMARY KEY, --automatic increment
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    exchange TEXT NOT NULL,
    is_etf BOOLEAN NOT NULL
);

--DROP TABLE etf_holding;
CREATE TABLE IF NOT EXISTS etf_holding (
    etf_id INTEGER NOT NULL, --FK
    holding_id INTEGER NOT NULL, --FK
    dt DATE NOT NULL,
    shares NUMERIC, --fractional share (etf) / nullable for no holding
    weight NUMERIC,
    PRIMARY KEY (etf_id, holding_id, dt), -- unique combination of / etf_id, holding_id, dt /               
    CONSTRAINT fk_etf FOREIGN KEY (etf_id) REFERENCES stock (id) ON DELETE CASCADE,
    CONSTRAINT fk_holding FOREIGN KEY (holding_id) REFERENCES stock (id) ON DELETE CASCADE
);

--DROP TABLE stock_price;
CREATE TABLE IF NOT EXISTS stock_price (
    stock_id INTEGER NOT NULL, --FK
    dt TIMESTAMP, --accuracy
    open NUMERIC NOT NULL, -- not null for completed bar 
    high NUMERIC NOT NULL,
    low NUMERIC NOT NULL,
    close NUMERIC NOT NULL,
    volume NUMERIC NOT NULL,
    PRIMARY KEY (stock_id, dt),
    CONSTRAINT fk_stock FOREIGN KEY (stock_id) REFERENCES stock (id) ON DELETE CASCADE
);


CREATE INDEX ON stock_price (stock_id, dt DESC);

-- create_hypertable:  partitioned by time as using the values in 'time' column
SELECT create_hypertable('stock_price', 'dt');