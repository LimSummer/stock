#encoding:utf
import urllib,urllib2
import re,time,sqlite3
from log import logging
if __name__ == "__main__":
    sh_object = open('sh.txt')
    shlist = []
    szlist = []
    try:
        for line in sh_object:
            shlist.append(line)
    finally:
        sh_object.close()
    sz_object = open('sz.txt')
    try:
        for line in sz_object:
            szlist.append(line)
    finally:
        sz_object.close()
    
    logging.info('shlist=%d', len(shlist))
    dic2 = {}
    dic2['s_sh'] = shlist
    dic2['s_sz'] = szlist
    dicEncode = {'s_sh':'GB2312','s_sz':'GBK'}
    for key in dic2:
        datalist = []
        tempList = []
        for l1 in dic2[key]:
            tempList.append(l1)
            if(len(tempList) == 20):
                try:
                    tstr = ""
                    for t in tempList:
                        if tstr == "":
                            tstr = key + t.strip()
                        else:
                            tstr = tstr + "," + key + t.strip()
                    #logging.info(tstr)
                    url = "http://qt.gtimg.cn/q=" + tstr
                    response = urllib2.urlopen(url) 
                    html = response.read()
                    lines = html.strip().split(";")
                    lines.remove("")

                    #time.sleep(100)
                    logging.info(len(lines))
                    for line in lines:
                        lv = line.strip().split("=")[1].replace('"','').split('~')
                        datalist.append(lv)
                    #logging.info(tempList)
                except Exception,e:
                    logging.error(e)
                tempList = []
        if(len(tempList) > 0):
            try:
                tstr = ""
                for t in tempList:
                    if tstr == "":
                        tstr = "s_sh" + t.strip()
                    else:
                        tstr = tstr + "," + "s_sh" + t.strip()
                url = "http://qt.gtimg.cn/q=" + tstr
                response = urllib2.urlopen(url) 
                html = response.read()
                lines = html.split("\r\n")
                for lv in lines:
                    lv = html.split("=")[1].replace('"','').split('~')
                    datalist.append(lv)
                    #logging.info(lv[1])
            except:
                logging.error('crawl error')
            tempList = []
        conn = sqlite3.connect('stocka.db')
        cursor = conn.cursor()
        valueList = []
        insertsql = "INSERT INTO STOCK_VALUE (STOCK_ID,STOCK_NAME,DATE,PRICE,CHANGE,CHANGE_PERCENTAGE,DEAL_CNT,DEAL_PRICE) VALUES (?,?,strftime('%Y-%m-%d',date('now')),?,?,?,?,?)"
        #print datalist
        print datalist[0][1]
        for data in datalist:
            valueList.append((data[2],data[1].decode(dicEncode[key]),float(data[3]),float(data[4]),float(data[5]),float(data[6]),float(data[7])))
        cursor.executemany(insertsql,valueList)
        conn.commit()
        conn.close()
