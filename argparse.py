#!/usr/bin/python
#coding:gbk
__author__ = 'yuleibupt2014'

#import argparse
import ConfigParser
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
#读取配置文件
def readconfigfile():
    config=ConfigParser.ConfigParser()
    with open("spider.conf","r") as cfgfile:
        config.readfp(cfgfile)
        url_list_file=config.get("spider","url_list_file")
        output_directory = config.get("spider", "output_directory")  #抓取结果存储目录
        max_depth = config.getint("spider", "max_depth")      #最大抓取深度(种子为0级)
        crawl_interval = config.getint("spider", "crawl_interval")     #抓取间隔. 单位: 秒
        crawl_timeout = config.getint("spider", "crawl_timeout")    #抓取超时. 单位: 秒
        target_url = config.get("spider", "target_url")        #需要存储的目标网页URL pattern(正则表达式)
        thread_count = config.getint("spider", 'thread_count')    #抓取线程数
    return url_list_file,output_directory,max_depth,crawl_interval,crawl_timeout, target_url, thread_count
#读命令行参数
def readargs():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvc:")
        for opt,arg in opts:
                if opt in ("-h", "--help"):
                    print_help()
                    return "IsFalse"
                elif opt in ("-v", "--version"):
                    print_version()
                    return "IsFalse"
                elif opt=="-c":
                    if arg=='spider.conf':
                        print '读取配置文件成功'
                        return "IsOK"
                    else:
                        print '请输入"-c spider.conf"作为读取配置文件命令'
                        return "IsFalse"
                else:
                    print  "输入格式错误，请重新输入，更多详情请输入'python mini_spider.py -h'"
                    return "IsFalse"
    except getopt.GetoptError:
        print "输入格式错误，请重新输入，更多详情请输入'python mini_spider.py -h'"
        return "IsFalse"


#parser = argparse.ArgumentParser()
#parser.add_argument("-c", dest="spider.conf", default="spider.conf", help="-C 配置文件名")

#parser.add_argument("-v", type=int, dest="deep", default=1, help="")
#args = parser.parse_args()

#html = get_html(args.url)
#save_html(html)