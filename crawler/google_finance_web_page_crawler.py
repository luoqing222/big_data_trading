"""This module define the yahoo option web page crawler."""
import os
from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import datetime
import platform

class GoogleFinanceWebPageCrawler(object):
    """class to crawl the option pages at yahoo.com """
    def __init__(self, driver_location, **kwargs):
        self.driver_location = driver_location
        super().__init__(**kwargs)

    @staticmethod
    def make_folder_name(folder_name,running_time):
        '''
        function to create the directory that save the webpage crawler
        :return: folder name
        '''
        directory = folder_name+"/"+running_time.strftime("%m%d%Y")+"/GoogleFinance"
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    @staticmethod
    def get_webpage_link():
        '''
        function to create the link to the web page that contains option
        :return: link to the web crawl_option_webpage(self, symbol_list, folder_name,running_time):
        '''
        #link = "http://finance.yahoo.com/quote/" + symbol + "/options?p="+symbol
        link = "http://www.google.com/finance"
        return link

    def crawl_single_date(self, folder_name,running_time,driver):
        driver.get(self.get_webpage_link())
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source,'html.parser')
        directory=self.make_folder_name(folder_name,running_time)
        link=self.get_webpage_link()
        driver.get(link)
        time.sleep(2)
        filename=directory+"/"+running_time.strftime("%Y%m%d")+".html"
        with open(filename, 'wb') as f:
            f.write(driver.page_source.encode('utf-8'))

    def crawl_google_webpage(self,folder_name,running_time):
        print("begin to crawl google finance page... ")
        if platform.system() == "Windows":
            try:
                driver = webdriver.Chrome(executable_path=self.driver_location)  # or add to your PATH
                self.crawl_single_date(folder_name, running_time,driver)
                driver.quit()
            except Exception as e:
                print(str(e))
                pass

        if platform.system() == "Linux":
            try:
                display = Display(visible=0, size=(800, 600))
                display.start()
                driver = webdriver.Chrome()
                self.crawl_single_date(folder_name, running_time,driver)
                driver.quit()
                display.stop()
            except Exception as e:
                print(str(e))
                pass