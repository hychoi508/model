# -*- coding: utf-8 -*-
# 데이터 정제 작업 
#18.03.26 현재 : data 결측값 문제  2014-01-07 19:08 ~ 2018-03-13 23:05:00

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
import locale
import datetime

Ex_Data=pd.read_csv("exchange_rate.csv", sep=",",header=None )
K_Data=pd.read_csv("data/.korbitKRW.csv", sep="," , header=None)  
U_Data=pd.read_csv("data/.krakenUSD.csv", sep="," , header=None) 

K_Data=pd.DataFrame(K_Data)
U_Data=pd.DataFrame(U_Data)

Ex_Data=pd.DataFrame(Ex_Data)
Ex_Data.columns=['day','Ex_rate']
Ex_Data.fillna(method='ffill', inplace=True)
Ex_Data.fillna(method='bfill', inplace=True)

Ex_Data['day']=pd.to_datetime(Ex_Data['day'])
Ex_Data['day']=pd.DataFrame(pd.Series(Ex_Data['day']).dt.ceil('D'))


K_Data['date']=pd.to_datetime(K_Data[0],unit='s')
K_Data['date']=pd.Series(K_Data['date']).dt.ceil('min')
U_Data['date']=pd.to_datetime(U_Data[0],unit='s')
U_Data['date']=pd.Series(U_Data['date']).dt.ceil('min')

Adjusted_K_Price=K_Data[1].groupby(K_Data['date']).mean()
Adjusted_K_Volume=K_Data[2].groupby(K_Data['date']).sum()
Adjusted_U_Price=U_Data[1].groupby(U_Data['date']).mean()
Adjusted_U_Volume=U_Data[2].groupby(U_Data['date']).sum()

#plt.plot(Adjusted_K_Price)
#plt.plot(Adjusted_U_Price)
#plt.plot(Adjusted_K_Volume)
#plt.plot(Adjusted_U_Volume)

Adjusted_K_Price=pd.DataFrame(Adjusted_K_Price)
Adjusted_K_Volume=pd.DataFrame(Adjusted_K_Volume)
Adjusted_U_Price=pd.DataFrame(Adjusted_U_Price)
Adjusted_U_Volume=pd.DataFrame(Adjusted_U_Volume)

Adjusted_K_Price['time']=Adjusted_K_Price.index
Adjusted_K_Volume['time']=Adjusted_K_Volume.index
Adjusted_U_Price['time']=Adjusted_U_Price.index
Adjusted_U_Volume['time']=Adjusted_U_Volume.index

Adjusted_K_Price.columns=["K_price","time"]
Adjusted_K_Volume.columns=["K_volume","time"]
Adjusted_U_Price.columns=["U_price","time"]
Adjusted_U_Volume.columns=["U_volume","time"]

Data_K=pd.merge(Adjusted_K_Price,Adjusted_K_Volume, on="time")
Data_U=pd.merge(Adjusted_U_Price,Adjusted_U_Volume, on="time")

#Data_K['5min_0']=pd.DataFrame(list(map(lambda x:time_generation(x,0),Data_K['time'])))
#Data_K['5min_1']=pd.DataFrame(list(map(lambda x:time_generation(x,1),Data_K['time'])))
#Data_K['5min_2']=pd.DataFrame(list(map(lambda x:time_generation(x,2),Data_K['time'])))
#Data_K['5min_3']=pd.DataFrame(list(map(lambda x:time_generation(x,3),Data_K['time'])))
#Data_K['5min_4']=pd.DataFrame(list(map(lambda x:time_generation(x,4),Data_K['time'])))
#
#Data_U['5min_0']=pd.DataFrame(list(map(lambda x:time_generation(x,0),Data_U['time'])))
#Data_U['5min_1']=pd.DataFrame(list(map(lambda x:time_generation(x,1),Data_U['time'])))
#Data_U['5min_2']=pd.DataFrame(list(map(lambda x:time_generation(x,2),Data_U['time'])))
#Data_U['5min_3']=pd.DataFrame(list(map(lambda x:time_generation(x,3),Data_U['time'])))
#Data_U['5min_4']=pd.DataFrame(list(map(lambda x:time_generation(x,4),Data_U['time'])))

#
#Data=pd.merge(Data_K,Data_U, on='5min_0')






Data=pd.merge(Data_K,Data_U, on="time")
Data['day']=pd.DataFrame(pd.Series(Data['time']).dt.ceil('D'))

Data_final=pd.merge(Data, Ex_Data, left_on='day', right_on='day')
Data_final['Adj_U_price']=pd.to_numeric(Data_final['U_price'])*pd.to_numeric(Data_final['Ex_rate'])

#plt.plot(Data_final['day'],Data_final['Ex_rate'])
#plt.plot(Data_final['day'],Data_final['Adj_U_price'])
#plt.plot(Data_final['day'],Data_final['K_price'])

Data_final['premium']=((Data_final['K_price']-Data_final['Adj_U_price'])/Data_final['Adj_U_price'])*100
temp_1min={}
temp_1min['1min']=pd.date_range('2014-01-07 19:08:00','2018-03-13 23:05:00',freq='1min')
temp_1min=pd.DataFrame(temp_1min)
Data_temp=pd.merge(Data_final, temp_1min, left_on='time', right_on='1min',how='right')
Data_temp=Data_temp.sort_values(by=['1min'])
#plt.plot(Data_final['day'],Data_final['premium'])


#####################################################################################
# EDA : Exploratory Data Analysis

Data_final.describe()
(n,bins, patched)=plt.hist(Data_final['premium'])
plt.axvline(Data_final['premium'].mean(),color='red')
plt.show()
Data_final['premium'].plot(kind='box')
# 프리미엄 차트가 right-skewed 되어있음. 
# 최근으로 올수록 거래량이 많아 최근 데이터일수록 count 수가 많은 현상 보정 필요
np.corrcoef(Data_final[['K_volume','premium']])
Data_final.corr()



def time_generation(x,i) :
    if x.minute%5==i%5 :
        return x
    if x.minute%5==(i+1)%5 :
        x=x-datetime.timedelta(minutes=1)
        return x
    if x.minute%5==(i+2)%5 :
        x=x-datetime.timedelta(minutes=2)
        return x
    if x.minute%5==(i+3)%5 :
        x=x-datetime.timedelta(minutes=3)
        return x
    if x.minute%5==(i+4)%5 :
        x=x-datetime.timedelta(minutes=4)
        return x