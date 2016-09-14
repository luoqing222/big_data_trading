import os
import pymysql
import time
import configparser
import datetime
from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup
from concurrent import futures

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

def crawl_single_symbol(symbol, folder_name, running_time, driver):
    page_link = "http://finance.yahoo.com/quote/" + symbol + "/options?p="+symbol
    driver.get(page_link)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    directory = folder_name+"/"+running_time.strftime("%m%d%Y")+"/"+symbol
    for select_menu in soup.findAll("select"):
        if len(select_menu['data-reactid']) != 0:
            for options in select_menu.findAll("option"):
                link = page_link + "?date=" + options['value']
                driver.get(link)
                time.sleep(2)
                expire_date = options.string.strip()
                expire_date = datetime.datetime.strptime(expire_date, "%B %d, %Y")
                filename = directory + "/" + expire_date.strftime("%Y%m%d") + ".html"
                with open(filename, 'wb') as f:
                    f.write(driver.page_source.encode('utf-8'))


def crawl_option_webpage(symbol_list, running_time, folder_name):
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Chrome()
    failed_stock=set()
    while len(symbol_list) != 0:
        symbol = symbol_list.pop(0)
        print("downloading web page for " + symbol + " under linux")
        try:
            crawl_single_symbol(symbol, folder_name, running_time, driver)
        except Exception as e:
            failed_stock.add(symbol)
            print(str(e))
            pass
    try:
        driver.quit()
        display.stop()
    except Exception as e:
        print(str(e))
        pass

    return failed_stock

def when_done(r):
    print('Got:', r.result())

def crawl_option_webpage_all(symbol_list, running_time, folder_name):
    all_failed_stock = set()
    with futures.ProcessPoolExecutor() as pool:
        for index in range(0,3):
            new_symbol_list = symbol_list[index * 100: (index + 1) * 100]
            future_result=pool.submit(crawl_option_webpage, new_symbol_list, running_time, folder_name)
            future_result.add_done_callback(when_done)


if __name__ == "__main__":
    start_time = time.time()
    # read config file
    config_file_name = "setting.ini"
    config_file_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    config = configparser.ConfigParser()
    config.read(config_file_folder + "/" + config_file_name)
    host = config.get("database", "host")
    user = config.get("database", "user")
    database = config.get("database", "database")
    password = config.get("database", "passwd")

    # step 1: get all the stock list in the exchange
    symbol_list = get_us_stock_list(host, user, password, database)

    # step 2: filter those symbol's that is not stock but preferred stock or mutual fund
    symbol_list = [symbol for symbol in symbol_list if "-" not in symbol and "." not in symbol]

    #step 3. make the folder for the
    temp_folder_name = config.get("csv", "temp_folder")
    running_time = datetime.datetime.now()
    for symbol in symbol_list:
        directory = temp_folder_name + "/test/" + running_time.strftime("%m%d%Y") + "/" + symbol
        if not os.path.exists(directory):
            os.makedirs(directory)

    #step 4. begin to crawl the option page concurrently
    #driver_location = config.get("driver", "chrome_driver")
    crawl_option_webpage_all(symbol_list, running_time, temp_folder_name)

    print("--- %s seconds ---" % (time.time() - start_time))


