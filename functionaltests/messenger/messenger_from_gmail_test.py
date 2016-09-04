"""functional test to test the messenger from gmail """
import sys
import os
import shutil
import time
import configparser
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from messenger import messenger_from_gmail

if __name__ == "__main__":

    start_time=time.time()
    #read config file
    config_file_name = "setting.ini"
    config_file_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    
    config = configparser.ConfigParser()
    config.read(config_file_folder+"/"+config_file_name)
    
    email = config.get("gmail", "email")
    passwd = config.get("gmail","password")

    gmail_messenger = messenger_from_gmail.MessengerFromGmail(email, passwd)
    broadcast_list=["luoqing222@gmail.com"]

    with open("test.txt","w") as f:
        f.write("hello,world")

    client_email = ["luoqing222@gmail.com"]
    gmail_messenger.send_email("test.txt", client_email,config_file_folder)



    
