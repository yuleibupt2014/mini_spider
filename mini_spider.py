#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'yuleibupt2014'

import argparse
import spider
import Queue
import os,sys
import md5
import time
import logging
####################################################################
url_list_file= 'C:\Users\yuleibupt2014\Desktop\mini_spider\urls'    #种子文件路径
output_directory='C:\Users\yuleibupt2014\Desktop\mini_spider\output' #抓取结果存储目录
max_depth= 2                       #最大抓取深度(种子为0级)
crawl_interval= 1                  #抓取间隔. 单位: 秒
crawl_timeout= 20                   #抓取超时. 单位: 秒
target_url='.*'#需要存储的目标网页URL pattern(正则表达式)
thread_count= 10                    # 抓取线程数
############################################################
def main():

    global url_list_file,output_directory,max_depth,crawl_interval,crawl_timeout, target_url, thread_count
    argflag=argparse.readargs()
    if argflag=='IsOK':
        url_list_file,output_directory,max_depth,crawl_interval,crawl_timeout, target_url, thread_count=argparse.readconfigfile()
        print u'按照配置文件参数开始运行：'
    elif argflag==None:
        print u'按照默认参数开始运行：'

    queueUrl = Queue.Queue()
    dict_downloaded = {}

    urlfile=open(str(url_list_file),'r')       #读种子文件
    for website in urlfile.readlines():
        queueUrl.put([0,website,md5.new(website).hexdigest])

    # outputfileses = os.listdir(output_directory)    #
    # for htmlfilename in outputfileses:
    #     srcfilename = os.path.splitext(htmlfilename)[0][1:]
    #     htmlname="http://"+srcfilename
    #     print htmlname
    #     url_hash = md5.new(str(htmlname)).hexdigest()
    #     dict_downloaded[url_hash] = str(htmlname)
    #print dict_downloaded
    threads = []

    for i in range(thread_count):
        t = spider.WorkerGetHtml(queueUrl,dict_downloaded,max_depth,crawl_timeout,None,"utf-8")
        t.setDaemon(True)
        threads.append(t)
        t.start()
    thread_log = spider.PrintLog(queueUrl, dict_downloaded,max_depth)
    thread_log.setDaemon(True)
    thread_log.start()
    threads.append(thread_log)

    while 1:       #当深度已达到时则杀死线程
         alive = False
         for i in range(thread_count):
             alive = (alive or threads[i].isAlive())
         if not alive:
             break
    print '\n'
    print "^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^"
    print u'''抓取任务完成！！！          总共下载Html数量: {0}          退出系统时间 Time: {1}'''.format(len(dict_downloaded), time.strftime( '%Y-%m-%d %X', time.localtime() ))
    print "^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^ ^_^"
    logging.debug(u"总共下载Html数量:{0}     退出系统时间 Time: {1}".format(len(dict_downloaded), time.strftime("%Y-%m-%d %X", time.localtime() )))

if __name__=='__main__':
    main()