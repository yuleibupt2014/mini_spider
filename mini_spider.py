#!/usr/bin/python
#coding:gbk


import argparse
import spider



if "__main__" == __name__:
    argflag=argparse.readargs()
    if argflag=='IsOK':
        url_list_file,output_directory,max_depth,crawl_interval,crawl_timeout, target_url, thread_count=argparse.readconfigfile()
        print url_list_file,output_directory,max_depth,crawl_interval,crawl_timeout, target_url, thread_count
    elif argflag==None:
        print '请输入命令行参数'

