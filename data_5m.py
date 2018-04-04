# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

# 데이터 정제 작업 
#18.03.26 현재 : data 결측값 문제  2014-01-07 19:08 ~ 2018-03-13 23:05:00

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
import locale
import datetime
from function.data_purify import time_generation

# Read data
Ex_Data=pd.read_csv("data/exchange_rate.csv", sep=",",header=None )
K_Data=pd.read_csv("data/.korbitKRW.csv", sep="," , header=None)  
U_Data=pd.read_csv("data/.krakenUSD.csv", sep="," , header=None) 

K_Data=pd.DataFrame(K_Data)
U_Data=pd.DataFrame(U_Data)

#timestamp 그래프 -> 최근으로 올수록 거래량이 많아지면서 
plt.plot(K_Data[0])
plt.plot(U_Data[0])

# Exchange rate refinement
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
Adjusted_K_Count=K_Data[2].groupby(K_Data['date']).count()

Adjusted_U_Price=U_Data[1].groupby(U_Data['date']).mean()
Adjusted_U_Volume=U_Data[2].groupby(U_Data['date']).sum()
Adjusted_U_Count=U_Data[2].groupby(U_Data['date']).count()


#plt.plot(Adjusted_K_Price)
#plt.plot(Adjusted_U_Price)
#plt.plot(Adjusted_K_Volume)
#plt.plot(Adjusted_U_Volume)

Adjusted_K_Price=pd.DataFrame(Adjusted_K_Price)
Adjusted_K_Volume=pd.DataFrame(Adjusted_K_Volume)
Adjusted_K_Count=pd.DataFrame(Adjusted_K_Count)
Adjusted_U_Price=pd.DataFrame(Adjusted_U_Price)
Adjusted_U_Volume=pd.DataFrame(Adjusted_U_Volume)
Adjusted_U_Count=pd.DataFrame(Adjusted_U_Count)

Adjusted_K_Price['time']=Adjusted_K_Price.index
Adjusted_K_Volume['time']=Adjusted_K_Volume.index
Adjusted_K_Count['time']=Adjusted_K_Count.index
Adjusted_U_Price['time']=Adjusted_U_Price.index
Adjusted_U_Volume['time']=Adjusted_U_Volume.index
Adjusted_U_Count['time']=Adjusted_U_Count.index

Adjusted_K_Price.columns=["K_price","time"]
Adjusted_K_Volume.columns=["K_volume","time"]
Adjusted_K_Count.columns=["K_count","time"]
Adjusted_U_Price.columns=["U_price","time"]
Adjusted_U_Volume.columns=["U_volume","time"]
Adjusted_U_Count.columns=["U_count","time"]

Data_K=pd.merge(Adjusted_K_Price,Adjusted_K_Volume, on="time")
Data_K=pd.merge(Data_K,Adjusted_K_Count, on="time")
Data_U=pd.merge(Adjusted_U_Price,Adjusted_U_Volume, on="time")
Data_U=pd.merge(Data_U,Adjusted_U_Count, on="time")

Data_K['5min_0']=pd.DataFrame(list(map(lambda x:time_generation(x,0),Data_K['time'])))
#Data_K['5min_1']=pd.DataFrame(list(map(lambda x:time_generation(x,1),Data_K['time'])))
#Data_K['5min_2']=pd.DataFrame(list(map(lambda x:time_generation(x,2),Data_K['time'])))
#Data_K['5min_3']=pd.DataFrame(list(map(lambda x:time_generation(x,3),Data_K['time'])))
#Data_K['5min_4']=pd.DataFrame(list(map(lambda x:time_generation(x,4),Data_K['time'])))

Data_U['5min_0']=pd.DataFrame(list(map(lambda x:time_generation(x,0),Data_U['time'])))
#Data_U['5min_1']=pd.DataFrame(list(map(lambda x:time_generation(x,1),Data_U['time'])))
#Data_U['5min_2']=pd.DataFrame(list(map(lambda x:time_generation(x,2),Data_U['time'])))
#Data_U['5min_3']=pd.DataFrame(list(map(lambda x:time_generation(x,3),Data_U['time'])))
#Data_U['5min_4']=pd.DataFrame(list(map(lambda x:time_generation(x,4),Data_U['time'])))

# %5==0 일때 row : 164068
Adjusted_K_Price_5_0=Data_K['K_price'].groupby(Data_K['5min_0']).mean()
Adjusted_K_Volume_5_0=Data_K['K_volume'].groupby(Data_K['5min_0']).sum()
Adjusted_K_Count_5_0=Data_K['K_count'].groupby(Data_K['5min_0']).sum()

Adjusted_U_Price_5_0=Data_U['U_price'].groupby(Data_U['5min_0']).mean()
Adjusted_U_Volume_5_0=Data_U['U_volume'].groupby(Data_U['5min_0']).sum()
Adjusted_U_Count_5_0=Data_U['U_count'].groupby(Data_U['5min_0']).sum()

Adjusted_K_Price_5_0=pd.DataFrame(Adjusted_K_Price_5_0)
Adjusted_K_Volume_5_0=pd.DataFrame(Adjusted_K_Volume_5_0)
Adjusted_K_Count_5_0=pd.DataFrame(Adjusted_K_Count_5_0)
Adjusted_U_Price_5_0=pd.DataFrame(Adjusted_U_Price_5_0)
Adjusted_U_Volume_5_0=pd.DataFrame(Adjusted_U_Volume_5_0)
Adjusted_U_Count_5_0=pd.DataFrame(Adjusted_U_Count_5_0)

Adjusted_K_Price_5_0['5min_0']=Adjusted_K_Price_5_0.index
Adjusted_K_Volume_5_0['5min_0']=Adjusted_K_Volume_5_0.index
Adjusted_K_Count_5_0['5min_0']=Adjusted_K_Count_5_0.index
Adjusted_U_Price_5_0['5min_0']=Adjusted_U_Price_5_0.index
Adjusted_U_Volume_5_0['5min_0']=Adjusted_U_Volume_5_0.index
Adjusted_U_Count_5_0['5min_0']=Adjusted_U_Count_5_0.index

Adjusted_K_Price_5_0.columns=["K_price","5min_0"]
Adjusted_K_Volume_5_0.columns=["K_volume","5min_0"]
Adjusted_K_Count_5_0.columns=["K_count","5min_0"]
Adjusted_U_Price_5_0.columns=["U_price","5min_0"]
Adjusted_U_Volume_5_0.columns=["U_volume","5min_0"]
Adjusted_U_Count_5_0.columns=["U_count","5min_0"]

Data_K_5_0=pd.merge(Adjusted_K_Price_5_0,Adjusted_K_Volume_5_0, on="5min_0")
Data_K_5_0=pd.merge(Data_K_5_0,Adjusted_K_Count_5_0, on="5min_0")
Data_U_5_0=pd.merge(Adjusted_U_Price_5_0,Adjusted_U_Volume_5_0, on="5min_0")
Data_U_5_0=pd.merge(Data_U_5_0,Adjusted_U_Count_5_0, on="5min_0")

Data=pd.merge(Data_K_5_0,Data_U_5_0, on='5min_0')


Data['day']=pd.DataFrame(pd.Series(Data['5min_0']).dt.round('D'))

# data 탐색용 Data_explor 생성
Data_explor=Data
Data_explor.index=Data_explor['day']
Data_explor.loc['2014-01-08']




Data_final=pd.merge(Data, Ex_Data, left_on='day', right_on='day')
Data_final['Adj_U_price']=pd.to_numeric(Data_final['U_price'])*pd.to_numeric(Data_final['Ex_rate'])

Data_final['premium']=((Data_final['K_price']-Data_final['Adj_U_price'])/Data_final['Adj_U_price'])*100
Data_final.to_csv("data/data_refined.csv")

# 환율차트
#plt.plot(Data_final['day'],Data_final['Ex_rate'])

# 조정된 미국가격 차트
#plt.plot(Data_final['day'],Data_final['Adj_U_price'])

# 한국가격 차트
#plt.plot(Data_final['day'],Data_final['K_price'])


#코프 차트
#plt.plot(Data_final['day'],Data_final['premium'])

#####################################################################################


# EDA : Exploratory Data Analysis

Data_final.describe()

# count 값의 분포 확인
Data_final['K_count'].hist(bins=30)
Data_final['U_count'].hist(bins=30)


plt.hist(Data_final['premium'])
plt.axvline(Data_final['premium'].mean(),color='red')
plt.show()

Data_final['premium'].plot(kind='box')

# Data final explor data 생성
Data_final_explor=Data_final
Data_final_explor.index=Data_final_explor['day']
# 프리미엄 차트가 right-skewed 되어있음. 
# 최근으로 올수록 거래량이 많아 최근 데이터일수록 count 수가 많은 현상 보정 필요

Data_final.corr()
# corr 결과 가격과 프리미엄간의 양의 상관관계가 돋보임. 특히 환율과 음의 상관관계가 있는것도 재밌음.


# missing value 분석 : 17.05 월 부터 missing value 거의 없음 
temp_5min={}
temp_5min['5min']=pd.date_range('2014-01-07 18:20:00','2018-03-13 23:05:00',freq='5min')
temp_5min=pd.DataFrame(temp_5min)
Data_temp=pd.merge(Data_final, temp_5min, left_on='5min_0', right_on='5min',how='right')
missing_data=Data_temp.loc[164068:]
missing_data=missing_data[['5min','premium']]
missing_data['day']=pd.DataFrame(pd.Series(missing_data['5min']).dt.round('D'))
missing_data=missing_data.groupby('day').count()
del missing_data['premium']
plt.plot(missing_data.loc['2018-01-08':'2018-03-11'])

missing_data.loc['2018-01-08':'2018-03-11']
missing_data['date']=missing_data.index
for i in range(len(missing_data)-1) :
    print(missing_data['5min'][i])
#    if missing_data['5min'].loc(i)>=200 :
  #      print(missing_data[i]['5min']>=200 )

max(missing_data.loc['2018-01-08':'2018-03-11'])

# data 탐색용 코드 
temp=missing_data.loc['2014-01-08':'2014-03-15']
plt.plot(temp['5min'])
Data_explor.loc['2017-04-08']
Data_final_explor.loc['2017-07-08']




