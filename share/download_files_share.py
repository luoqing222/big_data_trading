import configparser

class DownloadFilesShare(object):
    """description of class"""    
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    
    def get_temp_eod_data_location(self, running_time):
        """description of the function """
        """function to get the eod data location"""
        temp_folder_name = self.config.get("csv", "temp_folder")
        return temp_folder_name+"/"+running_time.strftime("%m%d%Y")+"/EOD"
   
 
    def get_temp_google_page_location(self, running_time):
        """description of the function """
        """function to get the eod data location"""
        temp_folder_name = self.config.get("csv", "temp_folder")
        return temp_folder_name+"/"+running_time.strftime("%m%d%Y")+"/GoogleFinance"
    
    def get_temp_yahoo_option_page_location(self, running_time):
        """description of the function """
        """function to get the eod data location"""
        temp_folder_name = self.config.get("csv", "temp_folder")
        return temp_folder_name+"/"+running_time.strftime("%m%d%Y")+"/YahooOption"
    
   
    


        

