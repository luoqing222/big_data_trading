"""unit test for the class yahoo_option_web_page_crawler.py. """
import unittest
import datetime
import sys
import os
import shutil
sys.path.append(os.getcwd())
from crawler import yahoo_option_web_page_crawler

class TestYahooOptionWebPageCrawlerUnittest(unittest.TestCase):
    """class to run the unit test """
    def test_make_folder_name(self):
        '''
        unit test to test the function make_folder_name
        '''
        symbol_list = ["FB"]
        running_time = datetime.datetime(2012, 2, 23, 0, 0)
        temp_folder = "C:/dev/temp"
        mycrawler = yahoo_option_web_page_crawler.YahooOptionWebPageCrawler(symbol_list)
        for symbol in symbol_list:
            webpage_path = mycrawler.make_folder_name(temp_folder, symbol, running_time)
            self.assertEqual(webpage_path, "C:/dev/temp/02232012/FB")
            self.assertTrue(os.path.exists(webpage_path))
            shutil.rmtree(webpage_path)
            self.assertFalse(os.path.exists(webpage_path))

    def test_get_option_web_page_link(self):
        '''
        unit test to test the function of getting the option link
        '''
        symbol = "FB"
        option_link = yahoo_option_web_page_crawler.YahooOptionWebPageCrawler.\
        get_option_webpage_link(symbol)
        self.assertEqual(option_link, "http://finance.yahoo.com/quote/FB/options?p=FB")

if __name__ == '__main__':
    unittest.main()
