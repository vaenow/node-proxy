# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import httplib
import threading
import sys
import socket

################
# http://m.66ip.cn/mo.php?sxb=&tqsl=100&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=
################

socket.setdefaulttimeout(7)

reload(sys)
sys.setdefaultencoding('utf-8')

inFile = open('ip66-list.txt')
outFile = open('ip66-verified.txt', 'w')

lock = threading.Lock()
    
def verifyProxyList():
    '''
    验证代理的有效性
    '''
    requestHeader = {
        'User-Agent': 'okhttp/3.6.0',
        'version': '1.1.6.1',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Cookie': '5MVv=x5Nbz347Mbic01ycV1M6z12939Mb810az6y0kbO4+dh7s3x1'
    }
    myurl = 'http://hots:port/path'

    while True:
        ll = inFile.readline().strip()
        if len(ll) == 0: break
        line = ll.strip().split(':')
        ip      = line[0]
        port    = line[1]
        
        try:
            conn = httplib.HTTPConnection(ip, port, timeout=7.0)
            conn.request(method = "GET", url = myurl, headers = requestHeader )
            res = conn.getresponse()
            data = res.read()

            # print data
            if "username" not in data:
                raise Exception("invalid proxy")

            # print "[%s:%s] => " % (ip, port) + data

            print ip + ":" + port
            outFile.write(ll + "\n")
            formattedHttpFile.write(ip + ":" + port + ",")
        except:
            a = ""
            # print "---Failure: " + ip + ":" + port
        
    
if __name__ == '__main__':

    print u"\n验证代理的有效性："
    
    all_thread = []
    for i in range(30):
        t = threading.Thread(target=verifyProxyList)
        all_thread.append(t)
        t.start()
        
    for t in all_thread:
        t.join()
    
    inFile.close()
    outFile.close()
    print "All Done."

