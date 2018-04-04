# -*- coding: utf-8 -*-
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from pandas.plotting import scatter_matrix
import datetime

data=pd.read_csv("data/data_refined.csv")
data=data[['K_price','K_volume','K_count','U_price','Adj_U_price','U_volume','U_count','Ex_rate','premium']]

#plt.plot(data['premium'])
#data.corr()
#data['premium'].hist()
#scatter_matrix(data[['premium','K_price']], figsize=(10,8), diagonal='kde', color='brown', marker='o', s=2.5)
#plt.show()












#def seasonality (x) :
#    if 8<pd.to_datetime(x).hour<24 :
#        return 1
#    else :
#        return 0
#    





