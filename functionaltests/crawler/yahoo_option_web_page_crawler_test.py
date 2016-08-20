"""functional test to crawl yahoo option web page """
import datetime
import sys
import os
import shutil
import pymysql
import argparse
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from crawler import yahoo_option_web_page_crawler

def get_Us_stock_list():
    symbol_list=[]
    conn = pymysql.connect(host='192.168.1.11', user='root', passwd='0307linsanlinqi)#)&', db='trading_data')
    cur = conn.cursor()
    cur.execute("SELECT symbol from eodequity where transaction_date= (select max(transaction_date) from eodequity)")
    for r in cur:
        symbol_list.append(r[0])
    cur.close()
    conn.close()
    return symbol_list 

if __name__ == "__main__":
    
    start_time=time.time()

    #read  the input parameter from the commandline
    parser=argparse.ArgumentParser()
    parser.add_argument("--initial", help="symbol with initial")
    args = parser.parse_args()
    
    #step 1: get all the stock list in the exchange
    symbol_list=get_Us_stock_list()

    #step 2: filter those symbol's that is not stock but preferred stock or mutual fund
    symbol_list = [symbol for symbol in symbol_list if "-" not in symbol and "." not in symbol]

    symbol_list = ["FB", "IBM", "A", "AA"]
    
    data_collector = yahoo_option_web_page_crawler.YahooOptionWebPageCrawler(symbol_list)
    folder_name="C:/dev/temp"
    running_time=datetime.datetime.now()
    
    if args.initial:
        data_collector.crawl_option_webpage_partial(symbol_list,folder_name,running_time, args.initial)
    else:
        data_collector.crawl_option_webpage(symbol_list,folder_name,running_time)

    print("--- %s seconds ---" % (time.time() - start_time))
