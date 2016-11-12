from os import listdir
from os.path import isfile, join, getsize

def check_folder(folder_name):
    onlyfiles =[join(folder_name, f) for f in listdir(folder_name) if isfile(join(folder_name, f))]
    onlyfolders = [f for f in listdir(folder_name) if not isfile(join(folder_name, f))]
    for folder in onlyfolders:
        onlyfiles = onlyfiles + check_folder(join(folder_name, folder))
    return onlyfiles
    

if __name__ == "__main__":
    #specify the running time
    #running_time=datetime.datetime.now()
    #running_time = datetime.datetime(year=2016, month=10, day=21)

    #specify the log file and log file clocation
    #log_file_name = "daily_run_"+running_time.strftime('%Y%m%d')+".log"
    
    folder_name = "C:\\Users\\luoq\\dev\\data"
    files = check_folder(folder_name)
    file_size = [getsize(file) for file in files if getsize(file)!=0]
    print(file_size)    

