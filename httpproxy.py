# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import httplib
import threading
import sys
import socket

socket.setdefaulttimeout(180)

reload(sys)
sys.setdefaultencoding('utf-8')

inFile = open('proxy.txt')
outFile = open('verified.txt', 'w')
formattedHttpFile = open('formattedHttp.txt', 'w')
formattedHttpsFile = open('formattedHttps.txt', 'w')

lock = threading.Lock()

def getProxyList(targeturl="http://www.xicidaili.com/nn/"):
    countNum = 0
    proxyFile = open('proxy.txt' , 'a')
    
    useragent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
    requestHeader = {'User-Agent': useragent}
    
    
    for page in range(1, 5):
        try:
            url = targeturl + str(page)

            # # proxy
            # proxy = urllib2.ProxyHandler({'http': 'http://111.121.193.214:3128'})
            # opener = urllib2.build_opener(proxy)
            # urllib2.install_opener(opener)
            print url
            # html_doc = opener.open(url)

            #print url
            request = urllib2.Request(url, headers=requestHeader)
            html_doc = urllib2.urlopen(request).read()

            soup = BeautifulSoup(html_doc, "html.parser")
            #print soup
            trs = soup.find('table', id='ip_list').find_all('tr')

            for tr in trs[1:]:
                tds = tr.find_all('td')
                #国家
                if tds[0].find('img') is None :
                    nation = '未知'
                    locate = '未知'
                else:
                    nation =   tds[0].find('img')['alt'].strip()
                    locate =   tds[3].text.strip()
                # print nation
                # print locate
                # print tds
                ip      =   tds[1].text.strip()
                port    =   tds[2].text.strip()
                anony   =   tds[4].text.strip()
                protocol=   tds[5].text.strip()
                speed   =   tds[6].find('div')['title'].strip()
                time    =   tds[7].text.strip()
                
                if protocol == 'HTTP': 
                    proxyFile.write('%s|%s|%s|%s|%s|%s|%s|%s\n' % (nation, ip, port, locate, anony, protocol,speed, time) )
                    #print '%s=%s:%s' % (protocol, ip, port)
                    countNum += 1
        except:
            print "network err"
    
    proxyFile.close()
    return countNum
    
def verifyProxyList():
    '''
    验证代理的有效性
    '''
    requestHeader = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
    myurl = 'http://www.baidu.com/'

    while True:
        lock.acquire()
        ll = inFile.readline().strip()
        lock.release()
        if len(ll) == 0: break
        line = ll.strip().split('|')
        protocol= line[5]
        ip      = line[1]
        port    = line[2]
        
        try:
            conn = httplib.HTTPConnection(ip, port, timeout=5.0)
            conn.request(method = 'GET', url = myurl, headers = requestHeader )
            res = conn.getresponse()
            data = res.read()

            print data
            if u"百度一下" not in data:
                raise Exception('invalid proxy')

            # print "[%s:%s] => " % (ip, port) + data
    
            lock.acquire()
            print "+++Success: " + ip + ":" + port
            outFile.write(ll + "\n")
            if protocol == 'HTTP':
                formattedHttpFile.write(ip + ":" + port + ",")
            elif protocol == 'HTTPS':
                formattedHttpsFile.write(ip + ":" + port + ",")
            lock.release()
        except:
             a = ""
            # print "---Failure: " + ip + ":" + port
        
    
if __name__ == '__main__':
    tmp = open('proxy.txt' , 'w')
    tmp.write("")
    tmp.close()

    proxynum = getProxyList("http://www.xicidaili.com/nn/")
    print u"国内高匿：" + str(proxynum)
    proxynum = getProxyList("http://www.xicidaili.com/nt/")
    print u"国内透明：" + str(proxynum)
    proxynum = getProxyList("http://www.xicidaili.com/wn/")
    print u"国外高匿：" + str(proxynum)
    proxynum = getProxyList("http://www.xicidaili.com/wt/")
    print u"国外透明：" + str(proxynum)

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

