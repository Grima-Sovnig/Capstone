
import paramiko as pm

import numpy as np
import pandas as pd
import pyodbc
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import itertools
import pysftp
import glob
import warnings

print("Beginning First Look Nissan File Uploads to USAI SFTP.")

reload_needed = ''
while reload_needed not in ["YES","NO"]:
    ###reload_needed = input("Do you want to overwrite current month reports on SFTP? (Yes/No) ")
    reload_needed = input("Are you re-uploading current reports to SFTP? (Yes/No) ")
    reload_needed = reload_needed.upper()

warnings.filterwarnings('ignore')
from Python_Cnopts_Ciphers import cnopts


cinfo = {
    'host':'HOST_NAME',
    'username':'USER_NAME',
    'password':r'PASSWORD',
    'cnopts':cnopts,
    'default_path' : 'NissanDataHub'
}

##New FTP Server - First Look Folder
prev_path = 'FirstLook\\Previous'
curr_path = 'FirstLook\\Current'
local_path = 'W:\\NIS4083 Nissan Market Flash Report\\Scripts\\Process InfinitiNissan\\1. FirstLook\\Outputs\\Nissan'
curr_dir = r'W:\NIS4083 Nissan Market Flash Report\Scripts\Process InfinitiNissan\1. FirstLook\Outputs\Nissan'
YYYYMM = (datetime.now() - relativedelta(months=1)).strftime("%Y%m")

# The all encompassing WITH statement ensure closure of cnxn
# with pysftp.Connection(log="./logs/pysftp.log", **cinfo) as cnxn:

os.chdir(r'W:\NIS4098 Nissan SRS Data Feed and Support\Python Scripts\SFTP Uploads')
# dir(os)
# Use this code for interactive mode
cnxn = pysftp.Connection(log="./logs/pysftp.log", **cinfo)


files_to_load = {}
files_not_found = 0

def build_folder_dict(folder, file_list, dict_to_append,files_not_found):
    os.chdir(folder)

    for file in file_list:
        found_files = glob.glob(file)
        if len(found_files) == 0:
            print("[WARNING] Could not find {}".format(file))
            files_not_found = files_not_found + 1
            continue
        else:
            print("[INFO] {} files found".format(len(found_files)))

        for file_to_add in found_files:
            dict_to_append[file_to_add] = os.path.join(folder, file_to_add)
            print("[INFO] {} added to list".format(file_to_add))
    return dict_to_append, files_not_found

folder = r'W:\NIS4083 Nissan Market Flash Report\Scripts\Process InfinitiNissan\1. FirstLook\Outputs\Nissan'
files = ['URBNSC_NMAP_FIRSTLOOK_DHS_NRADD_*.zip', 'URBNSC_FIRSTLOOK_DHS_*.zip', 'URBNSC_DHS_PMAMS_DLR_CNT_FIRSTLOOK_*.zip']
files_to_load, files_not_found = build_folder_dict(folder, files, files_to_load, files_not_found)

folder = r'W:\NIS4098 Nissan SRS Data Feed and Support\Files\Pedigree Report'
files = ['Pedigree Report - {YYYYMM} 1st Look.xlsx'.format(YYYYMM = YYYYMM)]
files_to_load, files_not_found = build_folder_dict(folder, files, files_to_load, files_not_found)

folder = r'W:\NIS4098 Nissan SRS Data Feed and Support\Files\KPI File\Delivered - {YYYYMM}'.format(YYYYMM = YYYYMM)
files = ['KPI_DHS_FIRST_????????.txt']
files_to_load, files_not_found = build_folder_dict(folder, files, files_to_load, files_not_found)

folder = r'W:\NIS4098 Nissan SRS Data Feed and Support\Files\Winner Loser File\Delivered - {YYYYMM}'.format(YYYYMM = YYYYMM)
files = ['DHS Report - {YYYYMM} 1st Look - Full Report.xlsx'.format(YYYYMM = YYYYMM)]
files_to_load, files_not_found = build_folder_dict(folder, files, files_to_load, files_not_found)

folder = r'W:\NIS4083 Nissan Market Flash Report\Scripts\Process InfinitiNissan\1. FirstLook\Outputs\Infiniti'
files = ['URBNSC_NMAP_FIRSTLOOK_DHS_NRADD_INF_*.zip']
files_to_load, files_not_found = build_folder_dict(folder, files, files_to_load, files_not_found)

folder = r'W:\NIS4018 Nissan-Infiniti MAS\M-PMA List\{YYYYMM}\Cleo'.format(YYYYMM=YYYYMM)
files = ['NissanDlrList.txt', 'InfinitiDlrList.txt']
files_to_load, files_not_found = build_folder_dict(folder, files, files_to_load, files_not_found)

# folder = r'W:\NIS4083 Nissan Market Flash Report\Scripts\Process InfinitiNissan\1. FirstLook\Outputs\Nissan'
# files = ['URBNSC_NMAP_FIRSTLOOK_DHS_PMAMS_*.zip']
# files_to_load, files_not_found = build_folder_dict(folder, files, files_to_load, files_not_found)

###files_not_found = 3
continue_upload = ''
if files_not_found > 0:
    while continue_upload not in ["YES","NO"]:
        continue_upload = input("There were " + str(files_not_found) + " files not found. Do you want to continue with uploading? (Yes/No) ")
        continue_upload = continue_upload.upper()

# this code is NOT being executed when files_not_found is equal to 0 (aka normal upload cicumstances)
# necessary edit: set the if statment below equal to if yes OR if the continue_upload sting variable is still blank...

# if continue_upload == 'YES': ### OLD CODE

if continue_upload == 'YES' or continue_upload == '':
    os.chdir(r'W:\NIS4098 Nissan SRS Data Feed and Support\Python Scripts\SFTP Uploads')
    with pysftp.Connection(**cinfo) as cnxn:
        if reload_needed == 'NO':
            ## cnxn.chdir('FirstLook/Previous')
            files = cnxn.listdir(prev_path)
            for file in files:
                cnxn.remove(os.path.join(prev_path, file).replace("\\","/"))
                print('[INFO] Removed {}'.format(file))

            ## cnxn.chdir('FirstLook/Current')
            files = cnxn.listdir(curr_path)
            for file in files:
                cnxn.rename(os.path.join(curr_path, file).replace("\\","/"), os.path.join(prev_path, file).replace("\\","/"))
                print('[INFO] migrated {}'.format(file))

        ## cnxn.chdir('FirstLook/Current')
        files = cnxn.listdir(curr_path)
        for file in files:
            cnxn.remove(os.path.join(curr_path, file).replace("\\","/"))
            print('[INFO] removed {}'.format(file))

        for file in files_to_load:
            print('[INFO] Tranferring {a}...'.format(a=file))
            try:
                ## with pysftp.Connection(**cinfo) as cnxn:
                cnxn.put(os.path.join(files_to_load[file]).replace("\\","/"), os.path.join(curr_path, file).replace("\\","/"))
            except Exception as e:
                print('[ERROR] Tranfer of {a} could not be completed. /n {e}'.format(a=file, e = e))
            else:
                print('[INFO] Tranfer of {a} is complete'.format(a=file))

    print('USAI FirstLook file upload complete.')

else:
    print('USAI FirstLook file upload cancelled.')

cnxn.close()
