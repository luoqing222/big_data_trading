"""This module define the yahoo option web page crawler."""
import os
from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import datetime
import platform

class YahooOptionWebPageCrawler(object):
    """class to crawl the option pages at yahoo.com """
    def __init__(self, symbol_list, driver_location, **kwargs):
        self.symbol_list = symbol_list
        self.driver_location = driver_location
        super().__init__(**kwargs)

    @staticmethod
    def make_folder_name(folder_name, symbol, running_time):
        '''
        function to create the directory that save the webpage crawler
        :return: folder name
        '''
        directory = folder_name+"/"+running_time.strftime("%m%d%Y")+"/YahooOption/"+symbol
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    @staticmethod
    def get_option_webpage_link(symbol):
        '''
        function to create the link to the web page that contains option
        :return: link to the web crawl_option_webpage(self, symbol_list, folder_name,running_time):
        '''
        link = "http://finance.yahoo.com/quote/" + symbol + "/options?p="+symbol
        return link

    def crawl_option_webpage_partial(self, symbol_list, folder_name,running_time, index):
        new_symbol_list=[]
        if index*100 <len(symbol_list):
            if (index+1)*100<len(symbol_list):
                new_symbol_list = symbol_list[index*100: (index+1)*100]
            else:
                new_symbol_list = symbol_list[index*100: -1]

        self.crawl_option_webpage_multiple_times(new_symbol_list, folder_name,running_time)

    def crawl_single_symbol(self, symbol, folder_name,running_time,driver):
        driver.get(self.get_option_webpage_link(symbol))
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source,'html.parser')
        directory=self.make_folder_name(folder_name,symbol,running_time)
        for select_menu in soup.findAll("select"):
            if len(select_menu['data-reactid']) != 0:
                for options in select_menu.findAll("option"):
                    link=self.get_option_webpage_link(symbol)+"?date="+options['value']
                    driver.get(link)
                    time.sleep(2)
                    expire_date=options.string.strip()
                    expire_date = datetime.datetime.strptime(expire_date, "%B %d, %Y")
                    filename=directory+"/"+expire_date.strftime("%Y%m%d")+".html"
                    with open(filename, 'wb') as f:
                        f.write(driver.page_source.encode('utf-8'))

    def crawl_option_webpage(self, symbol_list, folder_name,running_time):
        if symbol_list:
            print("number of stock is "+ str(len(symbol_list)))
        failed_stock=[]
        stock_list=symbol_list
        if platform.system() == "Windows":
            driver = webdriver.Chrome(executable_path=self.driver_location) # or add to your PATH
            while len(stock_list)!=0:
                symbol=stock_list.pop(0)
                print("downloading web page for "+symbol+" under windows")
                try:
                   self.crawl_single_symbol(symbol,folder_name, running_time,driver)
                except Exception as e:
                    failed_stock.append(symbol)
                    print(str(e))
                    pass
            try:
                driver.quit()
            except Exception as e:
                print(str(e))
                pass

        if platform.system() == "Linux":
            display =Display(visible = 0, size=(800,600))
            display.start()
            #print("driver location is "+self.driver_location)
            #chromedirver = self.driver_location
            #os.environ["webdriver.chrome.driver"] = chromedirver
            #driver = webdriver.Chrome(chromedirver)
            driver = webdriver.Chrome(executable_path=self.driver_location)
            while len(stock_list)!=0:
                symbol=stock_list.pop(0)
                print("downloading web page for "+symbol+" under linux")
                try:
                   self.crawl_single_symbol(symbol,folder_name, running_time,driver)
                except Exception as e:
                    failed_stock.append(symbol)
                    print(str(e))
                    pass
            try:
                driver.quit()
                display.stop()
            except Exception as e:
                print(str(e))
                pass

        return failed_stock

    def crawl_option_webpage_multiple_times(self, symbol_list, folder_name,running_time):
        stock_list=symbol_list
        for i in range(0, 2):
            stock_list=self.crawl_option_webpage(stock_list, folder_name,running_time)


        
 