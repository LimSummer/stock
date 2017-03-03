#encoding:utf
from log import logging
import os
class StockA:
    def __init__(self,filelist):
        self.dic_stock = {}
        shlist = []
        szlist = []
        for f in filelist:
            file_ob = open(f)
            ll = []
            try:
                for l in file_ob:
                    ll.append(l)
                fn = os.path.basename(f)
                self.dic_stock[fn[0:fn.index('.')]] = ll
            finally:
                file_ob.close()

if __name__ == "__main__":
    filelist = ['s_sh.txt','s_sz.txt']
    stock = StockA(filelist)
    for key in stock.dic_stock:
        print key
