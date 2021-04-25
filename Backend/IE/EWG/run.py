import os
import multiprocessing
import threading
from scrapy import cmdline


if __name__ == "__main__":
    os.system("cd EWG Scrapy/hw1")
    cmdline.execute("scrapy crawl EWG".split())
