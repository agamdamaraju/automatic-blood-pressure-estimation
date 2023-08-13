"""
File: download_mimic_iii_records.py
Author: Agam Damaraju
E-Mail: agamdamaraju@hotmail.com
Date created: 19/2/2023
Date last modified: 10/5/2023
"""

from os.path import expanduser, join, isdir
from os import mkdir
from sys import argv
from itertools import compress
import datetime
import argparse

import wfdb
import numpy as np
import heartpy as hp
import h5py, time, threading

def download_mimic_iii_records(RecordFiles, OutputPath):
    count = 0 
    with open(RecordFiles, 'r') as f:
        RecordFiles = f.read()
        RecordFiles = RecordFiles.split("\n")
    for file in RecordFiles:
        if count <= 2:
            # download record
            print(file)
            record = wfdb.rdrecord(file.split('/')[1], pn_dir='mimic3wdb/1.0/' + file.split('_')[0])
            print(f'{datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}: Processing record {file}')
            # check, if ABP and PLETH are present in the record. If not, continue with next record
            if 'PLETH' in record.sig_name:
                pleth_idx = record.sig_name.index('PLETH')
                ppg = record.p_signal[:,pleth_idx]
                fs = record.fs
            else:
                continue
        
            if 'ABP' in record.sig_name:
                abp_idx = record.sig_name.index('ABP')
                abp = record.p_signal[:,abp_idx]
            else:
                continue

            # save ABP and PPG signals as well as detected peaks in a .h5 file
            SubjectName = file.split('/')[1]
            SubjectName = SubjectName.split('_')[0]
            SubjectFolder = join(join(OutputPath, SubjectName))
            if not isdir(SubjectFolder):
                mkdir(SubjectFolder)
        
            with h5py.File(join(SubjectFolder, file.split('/')[1] + ".h5"),'w') as f:
                signals = np.concatenate((abp[:,np.newaxis],ppg[:,np.newaxis]), axis=1)
                f.create_dataset('val', signals.shape, data=signals)
            count += 1
        else:
            print("Sleeping for 1/6th minute...")
            time.sleep(10)
    
    print('script finished')
    

if __name__ == '__main__':
    
    # Create a destination dir as "Dataset_raw" either manually or using os.mkdir 
    download_mimic_iii_records('MIMIC-III_ppg_dataset_records.txt', "./Dataset_raw")
    