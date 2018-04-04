# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 16:03:30 2018

@author: user
"""

import os
import subprocess

def savetofile(filename):
    os.chdir('/home/rabbit/hadoop2/')
    subprocess.call('./bin/hdfs dfs -ls /test', shell=True)
    file=filename
    subprocess.call('./bin/hdfs dfs -put /home/rabbit/data_anal/kps_ml/data/'+file+'.csv /user/hdfs/test', shell=True)

