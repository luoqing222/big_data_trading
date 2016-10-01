"""functional test to crawl yahoo option web page """
import datetime
import sys
import os
import shutil
import pymysql
import argparse
import time
import configparser
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from crawler import google_finance_web_page_crawler

if __name__ == "__main__":

    start_time=time.time()
    #read config file
    config_file_name = "setting.ini"
    config_file_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    config = configparser.ConfigParser()
    config.read(config_file_folder+"/"+config_file_name)

    temp_folder_name = config.get("csv", "temp_folder")
    driver_location = config.get("driver", "chrome_driver")

    data_collector = google_finance_web_page_crawler.GoogleFinanceWebPageCrawler(driver_location)
    running_time=datetime.datetime.now()

    data_collector.crawl_google_webpage(temp_folder_name, running_time)

    print("--- %s seconds ---" % (time.time() - start_time))

