# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
from function.crawling_for_mail  import crawling
from function.crawling_for_mail  import data_to_file, exchange_rate_to_file
from function.mail_func import mail, exchange
from function.get_memberlist import get_memberlist
import math
import datetime
import time

def bollingerband(x,y=100,sigma=5) :
    x=pd.DataFrame(x)
    mva=x.rolling(window=y).mean()
    mvstd=x.rolling(window=y).std()
    upper_bound=mva+sigma*mvstd
    lower_bound=mva-sigma*mvstd
    return list(upper_bound[0]), list(lower_bound[0])


def append_maxsize(x,y,z) :
    if len(x)<z :
        x.append(y)
    else :
        x.pop(0)
        x.append(y) 
    return x


def gener_percentFlag(x,y) :
    global percent_flag
    percent_flag={}
    percent_flag['Boll']=1
    for i in range(x,y+1) :
       a='p_%d' %i
       percent_flag[a]=1

def setup_percentFlag(x,y,z) :
    for i in range(x,y+1) :
        a='p_%d' %i
        percent_flag[a]=1
    b='p_%d' %z
    percent_flag[b]=0
    percent_flag['Boll']=0

       
def premium_int(x,y) : 
    z= max(math.floor(x*100),math.floor(y*100))
    return z 




# 초기 데이터 생성용 로직




j=0
premium=[]
for j in range(0,10) : 
    premium.append(crawling('bithumb','poloniex'))
    j+=1
upper_bound,lower_bound=bollingerband(premium,10,5)


print('##### 메일 보내는 로직 시작 #####')
# 메일 보내는 로직 (mail 함수 제목 주는거 고쳐야함)
i=0
j=0
m=0
gener_percentFlag(-10,10)
time_exchange_data={'timestamp':[],'exchange_rate':[]} 
start_time_m=datetime.datetime.now()
start_time_h=datetime.datetime.now()
while True :
    time.sleep(5)
    i+=1    
    premium=append_maxsize(premium,crawling('bithumb','poloniex'),1000)
    upper_bound,lower_bound=bollingerband(premium,10,5)
    
    if not lower_bound[-1] < crawling('bithumb','poloniex') < upper_bound[-1]:
        percent_flag['Boll']=1
                
    if not math.floor(premium[-2]*100)==math.floor(premium[-1]*100) :
        temp=premium_int(premium[-2],premium[-1])
        temp_premium='p_%d' %temp
       
        if percent_flag['Boll']==1 or percent_flag[temp_premium]==1  :
            #mail_address=get_memberlist(temp)
            mail_address=['jwy627wywy@naver.com']       
            mail('test',mail_address)           
        setup_percentFlag(-10,10,premium_int(premium[-2],premium[-1]))
        
    time_for_logic_m=datetime.datetime.now()-start_time_m
    if time_for_logic_m.total_seconds()>36 :   
        time_exchange_data['timestamp'].append(int(time.time()))
        time_exchange_data['exchange_rate'].append(exchange())
        
        try :
            data_to_file(m)
        except :
            time.sleep(10)
            data_to_file(m)
        m+=1
        start_time_m=datetime.datetime.now()
        
    time_for_logic_h=datetime.datetime.now()-start_time_h
    
    if time_for_logic_h.total_seconds()>36*12 :
        exchange_rate_to_file(time_exchange_data,j)
        time_exchange_data={'timestamp':[],'exchange_rate':[]} 
        start_time_h=datetime.datetime.now()
        j+=1
    
#    if i==2000 :
#        break


# bollinger band test plot
plt.plot(upper_bound)
plt.plot(premium)
plt.plot(lower_bound)    


#함수, 나중에 다른 폴더로 뺄 계획 
##############################################################################

#def bollingerband(x,y=100,sigma=5) :
#    x=pd.DataFrame(x)
#    mva=x.rolling(window=y).mean()
#    mvstd=x.rolling(window=y).std()
#    upper_bound=mva+sigma*mvstd
#    lower_bound=mva-sigma*mvstd
#    return list(upper_bound[0]), list(lower_bound[0])
#
#
#def append_maxsize(x,y,z) :
#    if len(x)<z :
#        x.append(y)
#    else :
#        x.pop(0)
#        x.append(y) 
#    return x
#
#
#def gener_percentFlag(x,y) :
#    global percent_flag
#    percent_flag={}
#    percent_flag['Boll']=1
#    for i in range(x,y+1) :
#       a='p_%d' %i
#       percent_flag[a]=1
#
#def setup_percentFlag(x,y,z) :
#    for i in range(x,y+1) :
#        a='p_%d' %i
#        percent_flag[a]=1
#    b='p_%d' %z
#    percent_flag[b]=0
#    percent_flag['Boll']=0
#
#       
#def premium_int(x,y) : 
#    z= max(math.floor(x*100),math.floor(y*100))
#    return z 
#
#        