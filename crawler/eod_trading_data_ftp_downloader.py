import os
from ftplib import FTP 
import datetime
import re

class EodDataFtpDownloader:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
    
    def download_daily_data(self, temp_folder, running_time):
        '''
        function to download trading data from ftp.eoddata.com
        :return:
        '''
        
        des_folder = temp_folder+"/"+ running_time.strftime('%m%d%Y')+"/EOD"
        if not os.path.exists(des_folder):
            os.makedirs(des_folder)

        ftp = FTP(host=self.host, user=self.username, passwd=self.password)
        files = ftp.nlst()
        file_pattern = re.compile('[a-zA-Z]+_\d{8}.txt\Z')
        for f in files:
            if file_pattern.match(f):
                file_date = f.replace('.txt', "")
                file_date = re.sub('[a-zA-Z]+_', '', file_date)
                if file_date ==running_time.strftime('%Y%m%d'):
                    des_file_name = des_folder + "/" + f
                    print("downloading " + f + " to " + des_folder)
                    ftp.retrbinary('RETR ' + f, open(des_file_name, 'wb').write)

        ftp.close()

    def run(self, temp_folder, running_time):
        self.download_daily_data(temp_folder, running_time)


