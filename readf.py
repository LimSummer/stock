#encoding:utf
from log import logging
import re
file_object = open('stocks.txt')
try:
    pattern = re.compile(r'\(\d+\)')
    dic = {}
    for line in file_object:
        slist = line.split(' ')
        for i in range(len(slist)):
            #logging.info(slist[i])
            l = slist[i]
            #logging.info(l)
            match = pattern.search(l)
            #logging.info(match)
            if match:
                g = match.group()
                g = g.strip('()')
                firstchar = g[0]
                if dic.has_key(firstchar):
                    dic[firstchar].append(g)
                else:
                    dic[firstchar] = [g]
                logging.info(g)
            #logging.info(slist[i])
        
    logging.info(dic.keys())
    for key in dic:
        if key == '0':
            szfile = open('sz.txt','w')
            try:
                for l in dic[key]:
                    szfile.write(l + '\n')
            finally:
                szfile.close()
        elif key == '6':
            shfile = open('sh.txt','w')
            try:
                for l in dic[key]:
                    shfile.write(l + '\n')
            finally:
                shfile.close()
finally:
    file_object.close()