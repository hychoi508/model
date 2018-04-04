# -*- coding: utf-8 -*-
import datetime
import time
import pandas as pd
from pandas.tseries.offsets import Hour, Minute


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
    
def timeProduction(x,y) :
    a={'time_production':[]}
    timestamp_start=time.mktime(datetime.datetime.strptime(x,"%Y-%m-%d %H:%M:%S").timetuple())
    timestamp_end=time.mktime(datetime.datetime.strptime(y,"%Y-%m-%d %H:%M:%S").timetuple())
    for i in range(int(timestamp_start),(int(timestamp_end)+60),60) :
        i=datetime.datetime.fromtimestamp(i).strftime("%Y-%m-%d %H:%M:%S")
        a['time_production'].append(i)
    return pd.DataFrame(a)

#b=timeProduction("2014-01-07 19:08:00","2018-03-13 23:05:00")
#b.head(10)
#b.tail(10)
#
#pd.date_range('2014-01-07 19:08:00','2018-03-13 23:05:00',freq='5min')
#pd.date_range('2014-01-07 19:09:00','2018-03-13 23:05:00',freq='5min')
#pd.date_range('2014-01-07 19:10:00','2018-03-13 23:05:00',freq='5min')
#pd.date_range('2014-01-07 19:11:00','2018-03-13 23:05:00',freq='5min')
#pd.date_range('2014-01-07 19:12:00','2018-03-13 23:05:00',freq='5min')
#
#
#
#
#now=datetime.datetime.now()
#now=now.strftime('%Y-%m-%d %H:%M')
#now=pd.datetime(now)
#now.minute

