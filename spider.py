#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

__author__ = 'yuleibupt2014'
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

    def __init__(self, queueUrl,dict_url,deep):
        threading.Thread.__init__(self)
        self.queueUrl = queueUrl
        self.dict_url = dict_url
        self.deep     = deep

    def run(self):
        while True:
            url = self.queueUrl.get()
            url_hash = md5.new(url[1]).hexdigest()
            if not self.dict_url.has_key(url_hash):
                self.dict_url[url_hash] = url[1]
                try:
                    print "[toget] %s %s" % (url[0], url[1])
                    response = urllib2.urlopen(url[1], timeout=5)
                    global htmlcount
                    htmlcount=htmlcount+1
                    if response.info().get('Content-Encoding') == 'gzip':
                        buf = StringIO.StringIO(response.read())
                        f = gzip.GzipFile(fileobj=buf)
                        html = f.read()
                    else:
                        html = response.read()

                    os.chdir(mini_spider.output_directory)  #转换目录到output下
                    print "dangqianmulu:",os.getcwd()

                    urlnetloc=urlparse.urlparse(url[1])    #改文件名
                    deslink=urlnetloc.netloc+urlnetloc.path

                    splitstring='/'
                    addstring='~'

                    desname=str(addstring.join(deslink.split(splitstring)) )+".html"
                    print "desname:",desname

                    fp = open(desname,"w+")
                    fp.write(html)
                    fp.close()
                    print "haswritetimes:",str(htmlcount)

                    logging.debug("{0} downloaded {1}".format(self.getName(), url[1].encode("utf8")))
                    fp.close()
                    print "%s [well down!hasdown] %s %s" % (self.getName(),url[0], url[1])
                except:
                    logging.error("Unexpected error:", sys.exc_info()[0])
                else:
                    if url[0] < self.deep:
                        soup = BeautifulSoup.BeautifulSoup(html)
                        for link in soup.findAll('a',attrs={'href': re.compile("^http://")}):
                            href = link.get('href')
                            self.queueUrl.put([url[0]+1, href])
#                            logging.debug("{0} add href {1} to queue".format(self.getName(), href.encode("utf8")))

                self.queueUrl.task_done() #queueUrl.task_done()，每次从queue中get一个数据之后，当处理好相关问题，最后调用该方法，以提示q.join()是否停止阻塞，让线程向前执行或者退出；
                                             #queueUrl.join()，阻塞，直到queue中的数据均被删除或者处理。为队列中的每一项都调用一次。


def save_html(data):
    fp = open("a.html","w+")
    fp.write(data)

def print_html(data):
    print data



