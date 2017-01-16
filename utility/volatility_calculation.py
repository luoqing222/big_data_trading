from os import listdir
from os.path import isfile, join, getsize
import sys
import os
import datetime
import pymysql
import configparser
import pandas as pd

if __name__ == "__main__":
    config_file_name = "setting.ini"
    config_file_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    config = configparser.ConfigParser()
    config.read(config_file_folder+"/"+config_file_name)

    remote_host = config.get("database", "host")
    user = config.get("database", "user")
    password = config.get("database", "passwd")
    database = config.get("database", "database")
    conn = pymysql.connect(host=remote_host,db=database, user=user, passwd=password)
    df = pd.read_sql("SELECT * from historicalprice where symbol='spy'", conn)
    df.to_csv("D:\\temp\\temp.csv")
    conn.close()

    
