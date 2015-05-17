#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'yuleibupt2014'

import urllib2
import StringIO
import gzip
import BeautifulSoup
import re
import threading

class WorkerGetHtml(threading.Thread):
    def __init__(self, queueUrl, queueHtml):
        threading.Thread.__init__(self)
        self.queueUrl = queueUrl
        self.queueHtml = queueHtml

    def run(self):
        while True:
            url = self.queueUrl.get()
            print "[get] %s %s" % (url[0], url[1])
            response = urllib2.urlopen(url[1], timeout=5)

            if response.info().get('Content-Encoding') == 'gzip':
                buf = StringIO(response.read())
                f = gzip.GzipFile(fileobj=buf)
                html = f.read()
            else:
                html = response.read()

            self.queueHtml.put([url[0], html])
            self.queueUrl.task_done()

class WorkerParserHtml(threading.Thread):
    def __init__(self, queueHtml, queueUrl):
        threading.Thread.__init__(self)
        self.queueHtml = queueHtml
        self.queueUrl = queueUrl

    def run(self):
        while True:
            html = self.queueHtml.get()
            deep = html[0] + 1
            soup = BeautifulSoup.BeautifulSoup(html[1])
            count = 0
            for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
                href = link.get('href')
                count = count + 1
                self.queueUrl.put([deep, href])
                print "[href] %s %s" % (deep, href)
            print count
            self.queueHtml.task_done()


def save_html(data):
    fp = open("a.html","w+")
    fp.write(data)

def print_html(data):
    print data


