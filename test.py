#coding:gbk
__author__ = 'yuleibupt2014'


import argparse
import ConfigParser
import urllib2
from StringIO import StringIO
import gzip

import getopt,sys

def print_help():
    print "请按照以下格式输入参数行命令:"
    print "python mini_spider.py -c spider.conf [-h] [-v]"
    print "PS:(1)其中'-c spider.conf'表示从spider.conf文件中读取配置信息"
    print "   (2)其中'-h'表示阅读帮助"
    print "   (3)其中'-c'表示显示当前版本号"
def print_version():
    print '当前python版本号为"2.7.9"'
    print '当前spider版本号为"1.0"'

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
        print "输入格式错误，请重新输入，更多详情请输入'python mini_spider.py -h'"
        exit