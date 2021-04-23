import os
import multiprocessing
import threading
import time
from scrapy import cmdline


def p1():
    os.system("scrapy crawl EWG")


if __name__ == "__main__":
    cmdline.execute("scrapy crawl EWG".split())
