#encoding:utf
import sys,os,traceback
sys.path.append("..")
from log import logging
import urllib,urllib2,time,sqlite3,datetime
from StockA import StockA

dbfile = os.path.join(os.path.dirname(os.getcwd()),'stocka_f.db')
dicEncode = {'sh':'GB2312','sz':'GBK'}
def saveData(datalist,dec):
    try:
        valuelist = []
        insertSql = """
            INSERT INTO STOCK_RECORD (STOCK_ID,STOCK_NAME,DATE,PRICE_YESTODAY,PRICE_START,PRICE_CURRENT
            ,CHANGE,CHANGE_PERCENTAGE,TURNOVER,HIGH,LOW,DEAL_CNT,DEAL_PRICE,TOTALPRICE_FREE,TOTALPRICE)
             VALUES (?,?,strftime('%Y-%m-%d',datetime('now','localtime')),?,?,?,?,?,?,?,?,?,?,?,?)
            """
        for data in datalist:
            valuelist.append((data[2],data[1].decode(dicEncode[dec]),data[4],data[5],data[3],data[31],data[32],data[38],data[41],data[42],data[36],data[37],data[44],data[45]))
        
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
        cursor.executemany(insertSql, valuelist)
        conn.commit()
        conn.close()
    except Exception,e:
        logging.error(traceback.format_exc())
def crawlStock(stockidList,k):
    try:
        tstr = ""
        datalist = []
        for t in tempList:
            if tstr == "":
                tstr = k + t.strip()
            else:
                tstr = tstr + "," + k + t.strip()
        #logging.info(tstr)
        url = "http://qt.gtimg.cn/q=" + tstr
        #print url
        response = urllib2.urlopen(url) 
        html = response.read()
        #logging.info(html)
        lines = html.strip().split(";")
        lines.remove("")
        for line in lines:
            lv = line.strip().split("=")[1].replace('"','').split('~')
            datalist.append(lv)
        saveData(datalist,k)
    except Exception,e:
        logging.error(traceback.format_exc())
if __name__ == "__main__":
    filelist = []
    filelist.append(os.path.join(os.path.dirname(os.getcwd()),'sh.txt'))
    filelist.append(os.path.join(os.path.dirname(os.getcwd()),'sz.txt'))
    stock_all = StockA(filelist)
    now = datetime.datetime.now()
    endTime = datetime.datetime(now.year,now.month,now.day,16,0,0)
    #while now <= endTime:
        #logging.info(now)
    for key in stock_all.dic_stock:
        tempList = []
        print len(stock_all.dic_stock[key])
        
        for l1 in stock_all.dic_stock[key]:
            tempList.append(l1)
            if(len(tempList) == 50):
                crawlStock(tempList,key)
                tempList = []
        if (len(tempList) > 0):
            crawlStock(tempList,key)
            tempList = []
    logging.info("done.")