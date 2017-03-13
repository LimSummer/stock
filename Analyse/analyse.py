#encoding:utf
import sqlite3,sys,os,time
sys.path.append("..")
import traceback
from log import logging
db = "stocka_f.db"
def func_filter1(stocklist):
    for stock in stocklist:
        pass

def analyse(stocklist, func):
    filteredlist = func(stocklist)

query1 = 'select STOCK_ID,STOCK_NAME,DATE,PRICE,CHANGE,CHANGE_PERCENTAGE,DEAL_CNT,DEAL_PRICE from STOCK_RECORD ORDER BY DATE DESC'
query2 = 'select STOCK_ID,STOCK_NAME,SUM(CHANGE) AS TOTALCHANGE from STOCK_RECORD GROUP BY STOCK_ID ORDER BY TOTALCHANGE DESC'
query3 = "select STOCK_ID,STOCK_NAME,PRICE_YESTODAY from STOCK_RECORD where DATE='2017-03-01'"
def getdata(sql):
    dbfile = os.path.join(os.path.dirname(os.getcwd()),db)
    conn = sqlite3.connect(dbfile)
    valuelist = []
    try:
        cursor = conn.execute(sql)
        for row in cursor:
            valuelist.append(row)
    except Exception,e:
        logging.error(traceback.format_exc())
    finally:
        conn.close()
    return valuelist

if __name__ == "__main__":
    changelist = getdata(query2)
    
    mchangelist = [x for x in changelist if x[2] > 0]
    logging.info("data count = %i",len(mchangelist) )
    time.sleep(2)
    
    ylist = getdata(query3)
    dc = {}
    for r in mchangelist:
        dc[r[0]] = [r[0],r[1],r[2]]
    for r in ylist:
        if dc.has_key(r[0]):
            y = float(r[2])
            x = float(dc[r[0]][2])
            p = x / y * 100 if y != 0 else 0
            dc[r[0]].append(r[2])
            dc[r[0]].append(p)
    def compare1(x,y):
        if x[4] <= y[4]:
            return 1
        else:
            return -1
    li =sorted(dc.values(),cmp=compare1)
    logging.info("=======================")
    for l in li:
        logging.info("%s,%s,%s,%s,%s", l[0],l[1],l[2],l[3],round(l[4],2))
    #print dc.values()[0:2]
'''
if __name__ == "__main__":
    datas = getdata(query1)
    dic = {}
    dataDic = {}
    for row in datas:
        stockid = row[0]
        if not dic.has_key(stockid):
            dic[stockid] = 0
        if not dataDic.has_key(stockid):
            dataDic[stockid] = []
        dataDic[stockid].append(row)
        v = float(row[5])
        if v < 0:
            dic[stockid] = dic[stockid] + 1
    #print dic
    for key in dic:
        cnt = int(dic[key])
        if cnt == 4:
            for data in dataDic[key]:
                logging.info("\t%s\t%s\t%s\t%s\t%s\t%s\t%s",data[0],data[1],data[2],data[3],data[4],data[5],data[6])
            #logging.info(key)
            '''

