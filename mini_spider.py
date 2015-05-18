#!/usr/bin/python
#coding:gbk


import argparse
import spider
import Queue


if "__main__" == __name__:
    argflag=argparse.readargs()
    if argflag=='IsOK':
        url_list_file,output_directory,max_depth,crawl_interval,crawl_timeout, target_url, thread_count=argparse.readconfigfile()
        print url_list_file,output_directory,max_depth,crawl_interval,crawl_timeout, target_url, thread_count
    elif argflag==None:
        print '请输入命令行参数'

    queueUrl = Queue.Queue()
    queueHtml = Queue.Queue()
    queueUrl.put([0,'http://www.sina.com'])

    t = spider.WorkerGetHtml(queueUrl, queueHtml)
    t.setDaemon(True)
    t.start()

    t1 = spider.WorkerParserHtml(queueHtml, queueUrl)
    t1.setDaemon(True)
    t1.start()

    queueUrl.join()
    queueHtml.join()