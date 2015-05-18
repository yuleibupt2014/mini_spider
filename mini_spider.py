#!/usr/bin/python
#coding:gbk
__author__ = 'yuleibupt2014'

import argparse
import spider
import Queue
import os,sys
import md5
##############������Ĭ�ϲ�������##############################
url_list_file= 'C:\Users\yuleibupt2014\Desktop\mini_spider\urls'    #�����ļ�·��
output_directory='C:\Users\yuleibupt2014\Desktop\mini_spider\output' #ץȡ����洢Ŀ¼
max_depth= 10                       #���ץȡ���(����Ϊ0��)
crawl_interval= 1                  #ץȡ���. ��λ: ��
crawl_timeout= 1                   #ץȡ��ʱ. ��λ: ��
target_url='.*.(gif|png|jpg|bmp)$ '#��Ҫ�洢��Ŀ����ҳURL pattern(������ʽ)
thread_count= 8                    # ץȡ�߳���
############################################################

def main():

    global url_list_file,output_directory,max_depth,crawl_interval,crawl_timeout, target_url, thread_count
    argflag=argparse.readargs()
    if argflag=='IsOK':
        url_list_file,output_directory,max_depth,crawl_interval,crawl_timeout, target_url, thread_count=argparse.readconfigfile()
#        print url_list_file,output_directory,max_depth,crawl_interval,crawl_timeout, target_url, thread_count
    elif argflag==None:
        print "�����������в���"
#        print url_list_file,output_directory,max_depth,crawl_interval,crawl_timeout, target_url, thread_count

    queueUrl = Queue.Queue()
    dict_url = {}

    urlfile=open(str(url_list_file),'r')       #�������ļ�
    for website in urlfile.readlines():   #��ȡ�����ļ���Ϣ
        queueUrl.put([0,website])

    # outputfileses = os.listdir(output_directory)    #�����Ѿ����ڵ�html�ļ�hashֵ
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