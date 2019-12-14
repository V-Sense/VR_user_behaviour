# coding: utf-8
# A script to download UCL TCD dataset for 360-degree video
# Any problem, you can please contact to Cagri Ozcinar, cagriozcinar@gmail.com
# More description related to our work, you can check our project page: https://v-sense.scss.tcd.ie/research/3dof/vr_user_behaviour_system_design/
# and publication: Rossi et al. "Do users behave similarly in VR? Investigation of the influence on the system design", ACM TOMM 2020
# importing required modules
from zipfile import ZipFile
# import requests
import wget
import os
import glob

# specifying the zip file name
file_name       = 'data_ucl_tcd.zip'
project_name    = 'data/'


def extract_process(name):
    # opening the zip file in READ mode
    with ZipFile(name, 'r') as zip:
        # printing all the contents of the zip file
        zip.printdir()
 
        # extracting all the files
        print('Extracting all the files now...')
        zip.extractall(project_name + '/')
        print('Done!')

if __name__ == '__main__':

    # download the zip file and extract it
    try:
        if(os.path.isfile(file_name)!=True):
            wget.download('http://v-sense.scss.tcd.ie/Datasets/' + file_name, file_name)
            extract_process(file_name)
    except:
        print("No file to be downloaded!")