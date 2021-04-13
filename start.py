"""
New's Search Engine

Created on Wes Jun 11, 2020

@author: Liwei Wang
"""
"""
New's Scrapy Crawler

Created on Wes Aug 8, 2018
Last Modified on June 22, 2020

@author: Liwei Wang
"""

import os
import multiprocessing
import threading


def p0():
    os.system("python Backend/get_data.py&")


def p1():
    os.system("python Backend/api.py&")


def p2():
    os.system("serve -s build&")

def p3():
    os.system("cd Backend/News_Crawler/News_Crawler && "
              "scrapy crawl News_Crawler&")


if __name__ == "__main__":
    # multiprocessing -- python start.py/ & !!!!!!!!!!!!!!

    pro0 = multiprocessing.Process(target=p0)
    pro1 = multiprocessing.Process(target=p1)
    pro2 = multiprocessing.Process(target=p2)
    pro3 = multiprocessing.Process(target=p3)
    pro0.start()
    pro1.start()
    pro2.start()
    pro3.start()

# pro1 = threading.Thread(target=p1)
# pro2 = threading.Thread(target=p2)
