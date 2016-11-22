from os import listdir
from os.path import isfile, join, getsize
import sys
import os
import datetime
sys.path.append(os.path.dirname(os.path.dirname((os.path.realpath(__file__)))))
from share import download_files_share

def check_folder(folder_name):
    onlyfiles =[join(folder_name, f) for f in listdir(folder_name) if isfile(join(folder_name, f))]
    onlyfolders = [f for f in listdir(folder_name) if not isfile(join(folder_name, f))]
    for folder in onlyfolders:
        onlyfiles = onlyfiles + check_folder(join(folder_name, folder))
    return onlyfiles
    

if __name__ == "__main__":
    #create the object
    shareUtils = download_files_share.DownloadFilesShare(os.path.dirname(os.path.dirname((os.path.realpath(__file__))))+"/setting.ini")

    #specify the running time
    #running_time=datetime.datetime.now()
    running_time = datetime.datetime(year=2016, month=11, day=21)

    folder_name = shareUtils.get_temp_yahoo_option_page_location(running_time)
    #folder_name = shareUtils.get_temp_eod_data_location(running_time)
    print(folder_name)
    
    thresh_hold = 400000
    files = check_folder(folder_name)
    total_file_size = [getsize(file) for file in files]
    non_zero_file_size = [getsize(file) for file in files if getsize(file)!=0]
    valide_file_size = [getsize(file) for file in files if getsize(file)> thresh_hold]
    print("total number of file is "+ str(len(total_file_size)))
    print("number of non zero file is "+ str(len(non_zero_file_size)))
    print("number of valid file is "+ str(len(valide_file_size)))

