# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 19:28:52 2018

@author: user
"""

import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
import locale
import datetime

##Data_refined_non_dropna=pd.read_csv("data/data_refined_non_raw.csv",sep=",")
##Data_refined_non_dropna=Data_refined_non_dropna.dropna()



Data_refined_f=pd.read_csv("data/data_refined.csv", sep="," )
Data_refined_f['5min_0']=pd.to_datetime(Data_refined_f['5min_0'])

Data_refined_f['day_1']=pd.DataFrame(pd.Series(pd.to_datetime(Data_refined_f['5min_0'])).dt.floor('D'))
#Data_refined_f['day_2']=pd.DataFrame(pd.Series(pd.to_datetime(Data_refined_f['5min_0'])).dt.floor('D'))

Data_refined_f['K_price_Rtn']=np.log(Data_refined_f['K_price'])-np.log(Data_refined_f['K_price']).shift(1)

#plt.plot(Data_refined_f['K_price_Rtn'])
#Data_refined_f['K_price_Rtn'].hist(bins=50)


Data_refined_f['Adj_U_price_Rtn']=np.log(Data_refined_f['Adj_U_price'])-np.log(Data_refined_f['Adj_U_price']).shift(1)

Data_refined_f.fillna(method='bfill', inplace=True)

Day_Count=Data_refined_f['day_1'].groupby(Data_refined_f['day_1']).count()

Day_Count=pd.DataFrame(Day_Count)
Day_Count['Day_Count']=Day_Count.index
Day_Count.columns=["Day_Count","day_1"]

Data_refined_f=pd.merge(Data_refined_f,Day_Count, on="day_1")


Data_refined_f['K_price_Drift']=pd.DataFrame(Data_refined_f['K_price_Rtn'].mean()*Data_refined_f['Day_Count'])
Data_refined_f['K_price_Volatility']=pd.DataFrame(Data_refined_f['K_price_Rtn'].std()*np.sqrt(Data_refined_f['Day_Count']))

Data_refined_f['Adj_U_price_Drift']=pd.DataFrame(Data_refined_f['Adj_U_price_Rtn'].mean()*Data_refined_f['Day_Count'])
Data_refined_f['Adj_U_price_Volatility']=pd.DataFrame(Data_refined_f['Adj_U_price_Rtn'].std()*np.sqrt(Data_refined_f['Day_Count']))

## missing value 분석 : 17.05 월 부터 missing value 거의 없음 

temp_5min={}
temp_5min['5min']=pd.date_range('2014-01-07 19:05:00','2018-03-13 23:05:00',freq='5min')
temp_5min=pd.DataFrame(temp_5min)
Data_temp=pd.merge(Data_refined_f, temp_5min, left_on='5min_0', right_on='5min',how='right')
Data_refined_non_f=Data_temp
Data_refined_non_f['day']=pd.to_datetime(Data_refined_non['day'])

##del Data_refined_non['day_ts']

Data_refined_non_f['day_2']=pd.DataFrame(pd.Series(pd.to_datetime(Data_refined_non_f['5min'])).dt.floor('D'))

    
#Data_refined_non.index
#for i in range(0,439536):
#    if Data_refined_non.index[i]==i:
#        print(time.mktime(Data_refined_non['5min'].timetuple()))
        
#Data_refined_non_f['day_tms']=pd.DataFrame(time.mktime(Data_refined_non_f['day_1'].timetuple()))

#tmp_Day_Count
#tmp_Volatility
#tmp_drift

#tmp_Day_Count=Data_refined_non_dropna['Day_Count'].groupby(Data_refined_non_dropna['day_2']).mean()
#tmp_Day_Count=pd.DataFrame(tmp_Day_Count)
#tmp_Day_Count['day_2']=tmp_Day_Count.index
#tmp_Day_Count.columns=["Day_Count","day_2"]


#del tmp_K_price_Drift
tmp_K_price_Drift=Data_refined_f['K_price_Drift'].groupby(Data_refined_f['day_1']).mean()
tmp_K_price_Drift=pd.DataFrame(tmp_K_price_Drift)
tmp_K_price_Drift['day_1']=tmp_K_price_Drift.index
tmp_K_price_Drift.columns=["K_price_Drift","day_1"]

tmp_Adj_U_price_Drift=Data_refined_f['Adj_U_price_Drift'].groupby(Data_refined_f['day_1']).mean()
tmp_Adj_U_price_Drift=pd.DataFrame(tmp_Adj_U_price_Drift)
tmp_Adj_U_price_Drift['day_1']=tmp_Adj_U_price_Drift.index
tmp_Adj_U_price_Drift.columns=["Adj_U_price_Drift","day_1"]


#del tmp_Volatility
tmp_K_price_Volatility =Data_refined_f['K_price_Volatility'].groupby(Data_refined_f['day_1']).mean()
tmp_K_price_Volatility=pd.DataFrame(tmp_K_price_Volatility)
tmp_K_price_Volatility['day_1']=tmp_K_price_Volatility.index
tmp_K_price_Volatility.columns=["K_price_Volatility","day_1"]

#del tmp_Adj_U_price_Volatility
tmp_Adj_U_price_Volatility =Data_refined_f['Adj_U_price_Volatility'].groupby(Data_refined_f['day_1']).mean()
tmp_Adj_U_price_Volatility=pd.DataFrame(tmp_Adj_U_price_Volatility)
tmp_Adj_U_price_Volatility['day_1']=tmp_Adj_U_price_Volatility.index
tmp_Adj_U_price_Volatility.columns=["Adj_U_price_Volatility","day_1"]



#del tmp_firstPrice
tmp_k_first_Price=Data_refined_f[['K_price','day_1']].groupby(Data_refined_f['day_1']).head(1)
tmp_k_first_Price=pd.DataFrame(tmp_k_first_Price)

tmp_U_firstPrice=Data_refined_f[['Adj_U_price','day_1']].groupby(Data_refined_f['day_1']).head(1)
tmp_U_firstPrice=pd.DataFrame(tmp_U_firstPrice)

del K_priceInfo
K_priceInfo=tmp_K_price_Drift
K_priceInfo=pd.merge(K_priceInfo,tmp_k_first_Price, on="day_1")
K_priceInfo=pd.merge(K_priceInfo,tmp_K_price_Volatility, on="day_1")

del U_priceInfo
U_priceInfo=tmp_Adj_U_price_Drift
U_priceInfo=pd.merge(U_priceInfo,tmp_U_firstPrice, on="day_1")
U_priceInfo=pd.merge(U_priceInfo,tmp_Adj_U_price_Volatility, on="day_1")

Day_Count=Data_refined_f['day_1'].groupby(Data_refined_f['day_1']).count()
Day_Count=pd.DataFrame(Day_Count)
Day_Count['Day_Count']=Day_Count.index
Day_Count.columns=["Day_Count","day_1"]
K_priceInfo=pd.merge(K_priceInfo, Day_Count, on="day_1")


Day_Count=Data_refined_f['day_1'].groupby(Data_refined_f['day_1']).count()
Day_Count=pd.DataFrame(Day_Count)
Day_Count['Day_Count']=Day_Count.index
Day_Count.columns=["Day_Count","day_1"]
U_priceInfo=pd.merge(U_priceInfo, Day_Count, on="day_1")


##random=[]
##for i in range(0,1426):
##    price=[]
##    n=288-priceInfo['Day_Count']
##    drift=priceInfo['Drift']
##    vol=priceInfo['Volatility']
##    S0=priceInfo['K_price']
##    price=StockPrice(n,drift,vol,S0)
##    random.append(price)
##    
#priceTmp=priceInfo.ix[1]
#priceTmp['Drift']
#
#sample=[]
#for i in range(0,2):
#    priceTmp=priceInfo.ix[i]
#    n=288-int(priceTmp['Day_Count'])
#    drift=priceTmp['Drift']
#    vol=priceTmp['Volatility']
#    S0=priceTmp['K_price']
#    price=StockPrice(n,drift,vol,S0)
#    sample.append(price)
#    print(i)
#    print(price)
#    print(len(price))
#len(sample)    
#
#
#sampleK_price=[]
#for i in range(0,1428):
#    priceTmp=priceInfo.ix[i]
#    n=288-int(priceTmp['Day_Count'])
#    drift=priceTmp['Drift']
#    vol=priceTmp['Volatility']
#    S0=priceTmp['K_price']
#    price=StockPrice(n,drift,vol,S0)
#    sampleK_price.append(price)
#len(sampleK_price)
#
del sample_K_price
sample_K_price=[]
for i in range(0,1427):
    priceTmp=K_priceInfo.ix[i]
    n=288-int(priceTmp['Day_Count'])
    drift=priceTmp['K_price_Drift']
    vol=priceTmp['K_price_Volatility']
    S0=priceTmp['K_price']
    price=StockPrice(n,drift,vol,S0)
    sampleK_price.append(price)
len(sampleK_price)


del sample_U_price
sample_U_price=[]
for i in range(0,1427):
    priceTmp=U_priceInfo.ix[i]
    n=288-int(priceTmp['Day_Count'])
    drift=priceTmp['Adj_U_price_Drift']
    vol=priceTmp['Adj_U_price_Volatility']
    S0=priceTmp['Adj_U_price']
    price=StockPrice(n,drift,vol,S0)
    sample_U_price.append(price)
len(sample_U_price)

pd.DataFrame(sample_K_price).to_csv("data/sample_K_price.csv")
pd.DataFrame(sample_U_price).to_csv("data/sample_U_price.csv")
#
#
#
#    
#    
#Day_Count=Data_refined['day_1'].groupby(Data_refined['day_1']).count()
#Day_Count=pd.DataFrame(Day_Count)
#Day_Count['Day_Count']=Day_Count.index
#Day_Count.columns=["Day_Count","day_1"]
#
#
#    
#tmp_drift=Day_Count=Data_refined['Drift'].groupby(Data_refined['day_1'])
#    
##i=datetime.datetime.fromtimestamp(1389052800)
##print(i)
##pd.DataFrame(pd.Series(pd.to_datetime(i)).dt.floor('D'))
#
#
#
#
#
## 초기값 S0 에서 다음 GBM값 1개를 계산한다. drift, vol은 연간 단위
def GBM(drift, vol, S0=1):
    #mu = drift / 252             # daily drift rate
    #sigma = vol / np.sqrt(252) 	# daily volatlity 
    mu = drift
    sigma = vol
    
    
    # Monte Carlo simulation
    w = np.random.normal(0, 1, 1)[0]
    S = S0 * np.exp((mu - 0.5 * sigma**2) + sigma * w)
    return S

# n-기간 동안의 가상 주가를 생성한다
def StockPrice(n, drift, vol, S0):
    s = []
    for i in range(0, n):
        price = GBM(drift, vol, S0)
        s.append(GBM(drift, vol, S0))
        S0 = price
    return s
