# -*- coding: utf-8 -*-

import pandas as pd
from hdfs import InsecureClient


client_hdfs= InsecureClient('http://10.1.43.149:50070')
with client_hdfs.read('/user/coinone8.csv', encoding = 'utf-8') as reader:
    df = pd.read_csv(reader,index_col=0)
    print(df)
    Data_refined_non_dropna=pd.read_csv("data/data_refined_non_raw.csv",sep=",")