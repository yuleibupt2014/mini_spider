#coding:gbk
__author__ = 'yuleibupt2014'


import argparse
import ConfigParser
import urllib2
from StringIO import StringIO
import gzip

import getopt,sys

def print_help():
    print "�밴�����¸�ʽ�������������:"
    print "python mini_spider.py -c spider.conf [-h] [-v]"
    print "PS:(1)����'-c spider.conf'��ʾ��spider.conf�ļ��ж�ȡ������Ϣ"
    print "   (2)����'-h'��ʾ�Ķ�����"
    print "   (3)����'-c'��ʾ��ʾ��ǰ�汾��"
def print_version():
    print '��ǰpython�汾��Ϊ"2.7.9"'
    print '��ǰspider�汾��Ϊ"1.0"'

if "__main__" == __name__:
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvc:")
        for opt,arg in opts:
                if opt in ("-h", "--help"):
                    print_help()
                    sys.exit(1)
                elif opt in ("-v", "--version"):
                    print_version()
                    sys.exit(1)
                else:
                    print("%s  ==> %s" %(opt, arg))

    except getopt.GetoptError:
        print "�����ʽ�������������룬��������������'python mini_spider.py -h'"
        exit