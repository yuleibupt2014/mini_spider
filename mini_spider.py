#!/usr/bin/python
#coding:gbk
__author__ = 'yuleibupt2014'

import argparse
import spider
import Queue
import os,sys
import md5
##############以下是默认参数配置##############################
url_list_file= 'C:\Users\yuleibupt2014\Desktop\mini_spider\urls'    #种子文件路径
output_directory='C:\Users\yuleibupt2014\Desktop\mini_spider\output' #抓取结果存储目录
max_depth= 10                       #最大抓取深度(种子为0级)
crawl_interval= 1                  #抓取间隔. 单位: 秒
crawl_timeout= 1                   #抓取超时. 单位: 秒
target_url='.*.(gif|png|jpg|bmp)$ '#需要存储的目标网页URL pattern(正则表达式)
thread_count= 8                    # 抓取线程数
############################################################

def main():

    global url_list_file,output_directory,max_depth,crawl_interval,crawl_timeout, target_url, thread_count
    argflag=argparse.readargs()
    if argflag=='IsOK':
        url_list_file,output_directory,max_depth,crawl_interval,crawl_timeout, target_url, thread_count=argparse.readconfigfile()
#        print url_list_file,output_directory,max_depth,crawl_interval,crawl_timeout, target_url, thread_count
    elif argflag==None:
        print "请输入命令行参数"
#        print url_list_file,output_directory,max_depth,crawl_interval,crawl_timeout, target_url, thread_count

    queueUrl = Queue.Queue()
    dict_url = {}

    urlfile=open(str(url_list_file),'r')       #打开种子文件
    for website in urlfile.readlines():   #读取种子文件信息
        queueUrl.put([0,website])

    # outputfileses = os.listdir(output_directory)    #计算已经存在的html文件hash值
    # for htmlfilename in outputfileses:
    #     srcfilename = os.path.splitext(htmlfilename)[0][1:]
    #     htmlname="http://"+srcfilename
    #     print htmlname
    #     url_hash = md5.new(str(htmlname)).hexdigest()
    #     dict_url[url_hash] = str(htmlname)
    print dict_url

    for i in range(thread_count):
        t = spider.WorkerGetHtml(queueUrl,dict_url,max_depth)
        t.setDaemon(True)
        t.start()
    queueUrl.join()
    print len(dict_url)

if __name__=='__main__':
    main()