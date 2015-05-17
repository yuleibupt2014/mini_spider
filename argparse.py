#!/usr/bin/python
#coding:gbk
__author__ = 'yuleibupt2014'

#import argparse
import ConfigParser
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
#��ȡ�����ļ�
def readconfigfile():
    config=ConfigParser.ConfigParser()
    with open("spider.conf","r") as cfgfile:
        config.readfp(cfgfile)
        url_list_file=config.get("spider","url_list_file")
        output_directory = config.get("spider", "output_directory")  #ץȡ����洢Ŀ¼
        max_depth = config.getint("spider", "max_depth")      #���ץȡ���(����Ϊ0��)
        crawl_interval = config.getint("spider", "crawl_interval")     #ץȡ���. ��λ: ��
        crawl_timeout = config.getint("spider", "crawl_timeout")    #ץȡ��ʱ. ��λ: ��
        target_url = config.get("spider", "target_url")        #��Ҫ�洢��Ŀ����ҳURL pattern(������ʽ)
        thread_count = config.getint("spider", 'thread_count')    #ץȡ�߳���
    return url_list_file,output_directory,max_depth,crawl_interval,crawl_timeout, target_url, thread_count
#�������в���
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
                        print '��ȡ�����ļ��ɹ�'
                        return "IsOK"
                    else:
                        print '������"-c spider.conf"��Ϊ��ȡ�����ļ�����'
                        return "IsFalse"
                else:
                    print  "�����ʽ�������������룬��������������'python mini_spider.py -h'"
                    return "IsFalse"
    except getopt.GetoptError:
        print "�����ʽ�������������룬��������������'python mini_spider.py -h'"
        return "IsFalse"


#parser = argparse.ArgumentParser()
#parser.add_argument("-c", dest="spider.conf", default="spider.conf", help="-C �����ļ���")

#parser.add_argument("-v", type=int, dest="deep", default=1, help="")
#args = parser.parse_args()

#html = get_html(args.url)
#save_html(html)