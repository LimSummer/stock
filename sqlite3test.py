import sqlite3

"""
conn = sqlite3.connect('stocka2.db')
print "Opended database successfully"
conn.execute('''CREATE TABLE STOCK_VALUE
       (
       STOCK_ID          VARCHAR(32)    NOT NULL,
       STOCK_NAME        VARCHAR(32)      NOT NULL,
       DATE         date,
       PRICE        DOUBLE,
       CHANGE       DOUBLE,
       CHANGE_PERCENTAGE    DOUBLE,
       DEAL_CNT     DOUBLE,
       DEAL_PRICE   DOUBLE,
       primary key (STOCK_ID,DATE));''')
conn.commit()
conn.close()
print "Table created successfully";
"""
#conn = sqlite3.connect('stocka_f.db')
conn = sqlite3.connect('stock_record_rt.db')
createsql = '''
        CREATE TABLE STOCK_RECORD (
        STOCK_ID    VARCHAR(32) NOT NULL,
        STOCK_NAME  VARCHAR(32) NOT NULL,
        DATE date,
        PRICE_YESTODAY DOUBLE,
        PRICE_START DOUBLE,
        PRICE_CURRENT   DOUBLE,
        CHANGE  DOUBLE,
        CHANGE_PERCENTAGE DOUBLE,
        TURNOVER    DOUBLE,
        HIGH    DOUBLE,
        LOW DOUBLE,
        DEAL_CNT DOUBLE,
        DEAL_PRICE   DOUBLE,
        TOTALPRICE_FREE DOUBLE,
        TOTALPRICE DOUBLE,
        primary key (STOCK_ID,DATE)
    );
'''
print createsql
conn.execute(createsql)
conn.commit()
conn.close()