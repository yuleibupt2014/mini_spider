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

class WorkerGetHtml(threading.Thread):
    def __init__(self, queueUrl,dict_downloaded,deep):
        threading.Thread.__init__(self)
        self.queueUrl = queueUrl
        self.dict_downloaded = dict_downloaded
        self.deep     = deep

    def run(self):
        while True:
            url = self.queueUrl.get()
            try:
                response = urllib2.urlopen(url[1], timeout=20)
                global htmlcount
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
                if url[0] < self.deep:
                    soup = BeautifulSoup.BeautifulSoup(html)
                    for link in soup.findAll('a',attrs={'href': re.compile("^http://")}):
                        href = link.get('href')
                        url_hash = md5.new(url[1]).hexdigest()
                        if not self.dict_downloaded.has_key(url_hash):
                            self.queueUrl.put([url[0]+1, href])

                os.chdir(mini_spider.output_directory)  #转换目录到output下
                urlnetloc=urlparse.urlparse(url[1])
                hostname=urlnetloc.netloc
                pathname=urlnetloc.path
                splitstring='/'
                addstring='~'
                path=str(addstring.join(pathname.split(splitstring)))
                desname=hostname+path+".html"

                fp = open(desname,"w+")
                fp.write(html)
                fp.close()

                logging.debug("{0} downloaded {1}".format(self.getName(), url[1].encode("utf8")))

                self.dict_downloaded[url_hash] = url[1]

            self.queueUrl.task_done() #queueUrl.task_done()，每次从queue中get一个数据之后，当处理好相关问题，最后调用该方法，以提示q.join()是否停止阻塞，让线程向前执行或者退出；
                                             #queueUrl.join()，阻塞，直到queue中的数据均被删除或者处理。为队列中的每一项都调用一次。

#打印日志：当前已下载HTML数量、queue（URL）数量以及他们的总和
class PrintLog(threading.Thread):
    def __init__(self, queue_url, dict_downloaded):
        threading.Thread.__init__(self)
        self.queue_url = queue_url
        self.dict_downloaded = dict_downloaded

    def run(self):
        while True:
            time.sleep(1)
            queue = self.queue_url.qsize()
            downloaded = len(self.dict_downloaded)
            print "queue:{0} downloaded:{1}".format(queue, downloaded)

def save_html(data):
    fp = open("a.html","w+")
    fp.write(data)

def print_html(data):
    print data


