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
from crawler import yahoo_option_web_page_crawler

def get_us_stock_list(host, user, passwd, db):
    symbol_list=[]
    conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("SELECT symbol from eodequity where transaction_date= (select max(transaction_date) from eodequity) order by symbol")
    for r in cur:
        symbol_list.append(r[0])
    cur.close()
    conn.close()
    return symbol_list 

if __name__ == "__main__":

    start_time=time.time()
    #read config file
    config_file_name = "setting.ini"
    config_file_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    
    config = configparser.ConfigParser()
    config.read(config_file_folder+"/"+config_file_name)

    host = config.get("database", "host")
    user = config.get("database", "user")
    database = config.get("database","database")
    password = config.get("database","passwd")

    #step 1: get all the stock list in the exchange
    symbol_list=get_us_stock_list(host, user, password, database)

    #step 2: filter those symbol's that is not stock but preferred stock or mutual fund
    symbol_list = [symbol for symbol in symbol_list if "-" not in symbol and "." not in symbol]

    #read  the input parameter from the commandline
    parser=argparse.ArgumentParser()
    parser.add_argument("--index", help="symbol with index for every 100 stock")
    args = parser.parse_args()

    #symbol_list = ["FB", "IBM", "A", "AA"]
    
    temp_folder_name = config.get("csv", "temp_folder")
    #driver_location = config.get("driver", "Phantomjs")
    driver_location = config.get("driver", "chrome_driver")
    
    data_collector = yahoo_option_web_page_crawler.YahooOptionWebPageCrawler(symbol_list, driver_location)
    running_time=datetime.datetime.now()
    
    if args.initial:
        data_collector.crawl_option_webpage_partial(symbol_list,temp_folder_name,running_time, args.index)
    else:
        data_collector.crawl_option_webpage_multiple_times(symbol_list,temp_folder_name,running_time)

    print("--- %s seconds ---" % (time.time() - start_time))

