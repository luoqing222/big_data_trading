import logging
import time
import configparser
import datetime
import os
from crawler import eod_1min_bar_data_crawler
from crawler import eod_trading_data_ftp_downloader
from crawler import google_finance_web_page_crawler

logger = logging.getLogger(__name__)

def download_raw_data(config, running_time):
    downloadEod1MinBarData(config, running_time)
    downloadEodTradingData(config, running_time)
    downloadGoogleFinanceData(config, running_time)

def downloadEod1MinBarData(config, running_time):
    '''
    function to download eod 1 min bar trading data from ftp.eoddata.com
    :return:
    '''
    logger.info("Downloading EOD Bar Data on " + running_time.strftime('%m_%d_%Y'))
    
    try:
        download_folder = config.get("driver", "download_folder")
        temp_folder_name = config.get("csv", "temp_folder")
        driver_location = config.get("driver", "chrome_driver")
        username = config.get("eod", "user")
        password = config.get("eod", "passwd")
    
        #begin the data collection process
        data_collector = eod_1min_bar_data_crawler.Eod1MinBarDataCollector(driver_location, username, password)
        data_collector.run(download_folder, temp_folder_name, running_time)
        #logger.info("eod 1 min bar data is successfully downloaded")
    except Exception as e:
        logger.warning("downloadEod1MinBarData: " + str(e)) 
        pass
    
def downloadEodTradingData(config, running_time):
    logger.info("Downloading EOD trading Data on " + running_time.strftime('%m_%d_%Y'))
    
    try:
        temp_folder_name = config.get("csv", "temp_folder")
        host = config.get("eod","host")
        username = config.get("eod", "user")
        password = config.get("eod", "passwd")
    #begin the data collection process
        data_collector = eod_trading_data_ftp_downloader.EodDataFtpDownloader(host, username, password)
        data_collector.run(temp_folder_name, running_time)
    except Exception as e:
        logger.warning("downloadEodTradingData: " + str(e)) 

def downloadGoogleFinanceData(config, running_time):
    logger.info("Downloading Google Finance Data on " + running_time.strftime('%m_%d_%Y'))

    try:
        temp_folder_name = config.get("csv", "temp_folder")
        driver_location = config.get("driver", "chrome_driver")
        data_collector = google_finance_web_page_crawler.GoogleFinanceWebPageCrawler(driver_location)
        data_collector.crawl_google_webpage(temp_folder_name, running_time)
    except Exception as e:
        logger.warning("downloadGoogleFinanceData: " + str(e))

if __name__ == "__main__":
    start_time=time.time()

    #get the configuration from setting.ini
    config_file_name = "setting.ini"
    config = configparser.ConfigParser()
    config.read(config_file_name)

    #specify the log file information
    message_folder = config.get("message","messages_folder")
    if not os.path.exists(message_folder):
        os.makedirs(message_folder)

    #specify the running time
    running_time=datetime.datetime.now()
    #running_time = datetime.datetime(year=2016, month=10, day=21)

    #specify the log file and log file clocation
    log_file_name = "daily_run_"+running_time.strftime('%Y%m%d')+".log"
    log_file = message_folder + "/" + log_file_name
    logging.basicConfig(filename=log_file, level=logging.INFO, filemode="w")
        
    #begin the data process
    download_raw_data(config, running_time)


    print("--- %s seconds ---" % (time.time() - start_time))


