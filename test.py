#coding:gbk
__author__ = 'yuleibupt2014'

import threading
import time

# ��Ʒ
product = None
# ��������
con = threading.Condition()

# �����߷���
def produce():
    global product

    if con.acquire():
        while True:
            if product is None:
                print 'produce...'
                product = 'anything'

                # ֪ͨ�����ߣ���Ʒ�Ѿ�����
                con.notify()

            # �ȴ�֪ͨ
            con.wait()
            time.sleep(2)

# �����߷���
def consume():
    global product

    if con.acquire():
        while True:
            if product is not None:
                print 'consume...'
                product = None

                # ֪ͨ�����ߣ���Ʒ�Ѿ�û��
                con.notify()

            # �ȴ�֪ͨ
            con.wait()
            time.sleep(2)

t1 = threading.Thread(target=produce)
t2 = threading.Thread(target=consume)
t2.start()
t1.start()



