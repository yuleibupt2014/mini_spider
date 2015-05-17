#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'yuleibupt2014'

import urllib2
import StringIO
import gzip

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