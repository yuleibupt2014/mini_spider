#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'yuleibupt2014'

import urllib2
import StringIO
import gzip
import BeautifulSoup
import re

def get_html(url):
    response = urllib2.urlopen(url, timeout=5)

    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        html = f.read()
    else:
        html = response.read()

    return html

def save_html(data):
    fp = open("a.html","w+")
    fp.write(data)

def print_html(data):
    print data

def get_link(html):   #得到HTML里面的所有网页链接
    new_link = []
    soup = BeautifulSoup.BeautifulSoup(html)
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        new_link.append(link.get('href'))
    return new_link

def print_link(link_array):     #打印出从HTML得到的所有网页链接
    for link in link_array:
        print link
    print len(link_array)

print_link(get_link(get_html("http://www.sina.com")))
