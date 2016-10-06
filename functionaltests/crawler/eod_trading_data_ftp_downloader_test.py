"""functional test to crawl yahoo option web page """
import datetime
import sys
import os
import shutil
import pymysql
import argparse
import time
import configparser
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from crawler import eod_trading_data_ftp_downloader

logger = logging.getLogger(__name__)

if __name__ == "__main__":

    start_time=time.time()
   
    #read config file
    config_file_name = "setting.ini"
    config_file_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    config = configparser.ConfigParser()
    config.read(config_file_folder+"/"+config_file_name)

    running_time=datetime.datetime.now()
    #running_time = datetime.datetime(year=2016, month=10, day=5)
    
    temp_folder_name = config.get("csv", "temp_folder")
    host = config.get("eod","host")
    username = config.get("eod", "user")
    password = config.get("eod", "passwd")
    
    #specify the log file information
    message_folder = config.get("message","messages_folder")
    if not os.path.exists(message_folder):
        os.makedirs(message_folder)

    log_file_name = "eod_ftp_download.log"
    log_file = message_folder + "/" + log_file_name
    
    logging.basicConfig(filename=log_file, level=logging.INFO, filemode="w")
    logger.info("start data collection process on " + running_time.strftime('%m_%d_%Y'))
    
    #begin the data collection process
    data_collector = eod_trading_data_ftp_downloader.EodDataFtpDownloader(host, username, password)
   
    data_collector.run(temp_folder_name, running_time)
    logger.info("eod trading data is successfully downloaded")

    print("--- %s seconds ---" % (time.time() - start_time))