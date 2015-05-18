#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'yuleibupt2014'

import sys
import os
import urllib2
import StringIO
import gzip
import BeautifulSoup
import re
import threading
import logging
import urlparse
import mini_spider
import md5
import time
import chardet

htmlcount=0
LEVELS = {
        1:logging.CRITICAL,
        2:logging.ERROR,
        3:logging.WARNING,
        4:logging.INFO,
        5:logging.DEBUG
    }
level = LEVELS[5]
logging.basicConfig(filename='log',level=level)
currentdeep=0
class WorkerGetHtml(threading.Thread):
    def __init__(self, queueUrl,dict_downloaded,deep,crawl_timeout,key,encoding=None):
        threading.Thread.__init__(self)
        self.queueUrl = queueUrl
        self.dict_downloaded = dict_downloaded
        self.deep= deep
        self.key = key
        self.crawl_timeout=crawl_timeout
        self.encoding=encoding
    def run(self):
        while True:
            url = self.queueUrl.get()
            global currentdeep
            currentdeep=url[0]
            if currentdeep==self.deep:
                print self.getName(),"has quit"
                sys.exit(1)
            try:
                response = urllib2.urlopen(url[1], timeout=self.crawl_timeout)
                global htmlcount, charset
                htmlcount=htmlcount+1
                if response.info().get('Content-Encoding') == 'gzip':
                    buf = StringIO.StringIO(response.read())
                    f = gzip.GzipFile(fileobj=buf)
                    html = f.read()
                else:
                    html = response.read()
            except urllib2.URLError as e:
                logging.error("URLError:{0} {1}".format(url[1], e.reason))
            except urllib2.HTTPError as e:
                logging.error("HTTPError:{0} {1}".format(url[1], e.code))
            except Exception as e:
                logging.error("Unexpected:{0} {1}".format(url[1], str(e)))
            else:
                try:
                    if  self.key == None:
                        self.getLink(url, html)
                        self.saveHtml(url, html)
                    else:
                        if not self.encoding:
                            charset = chardet.detect(html)
                            print charset
                            self.encoding = charset['encoding']
                        match = re.search(re.compile(self.key), html.decode(self.encoding, "ignore"))
                        print match
                        if match:
                            print "match"
                            self.getLink(url, html)
                            self.saveHtml(url, html)
                        else:
                            logging.debug("{0} ignore {1} key not match".format(self.getName(), url[1].encode("utf8")))
                except UnicodeEncodeError as e:
                    logging.error("UnicodeEncodeError:{0} {1}".format(url[1], str(e)))
                except Exception as e:
                    logging.error("Unexpected:{0} {1}".format(url[1], str(e)))
            self.queueUrl.task_done() #queueUrl.task_done()，每次从queue中get一个数据之后，当处理好相关问题，最后调用该方法，以提示q.join()是否停止阻塞，让线程向前执行或者退出；
                                             #queueUrl.join()，阻塞，直到queue中的数据均被删除或者处理。为队列中的每一项都调用一次。
    def getLink(self,url,html):
        if url[0] < self.deep:
            soup = BeautifulSoup.BeautifulSoup(html)
            for link in soup.findAll('a',attrs={'href': re.compile("^http://")}):
                href = link.get('href')
                url_hash = md5.new(href).hexdigest()
                if not self.dict_downloaded.has_key(url_hash):
                    self.queueUrl.put([url[0]+1, href, url_hash])
    #               logging.debug("{0} add href {1} to queue".format(self.getName(), href.encode("utf8")))

    def saveHtml(self,url,html):
        os.chdir(mini_spider.output_directory)  #转换目录到output下

        urlnetloc=urlparse.urlparse(url[1])  #解析html名称
        hostname=urlnetloc.netloc
        pathname=urlnetloc.path
        splitstring='/'
        addstring='~'
        path=str(addstring.join(pathname.split(splitstring)))
        desname=hostname+path+".html"

        fp = open(desname,"w+")         #写入文件并保存
        fp.write(html)
        fp.close()
        self.dict_downloaded[url[2]] = url[1]   #存入hash值
        logging.debug("{0} downloaded {1}".format(self.getName(), url[1].encode("utf8")))

#打印日志：当前已下载HTML数量、queue（URL）数量
class PrintLog(threading.Thread):
    def __init__(self, queueUrl, dict_downloaded,max_depth):
        threading.Thread.__init__(self)
        self.queueUrl = queueUrl
        self.dict_downloaded = dict_downloaded
        self.max_depth = max_depth
    def run(self):
        while True:
            time.sleep(1)
            queue = self.queueUrl.qsize()
            downloaded = len(self.dict_downloaded)
            global currentdeep
            print "--------------------------------------------------"
            print u"当前深度:{0}".format(currentdeep)
            print u"待下载:{0}".format(queue)
            print u"已下载:{0}".format(downloaded)
            print "--------------------------------------------------"
            if currentdeep==self.max_depth:
                print "PrintLog has quit"
                sys.exit(1)

