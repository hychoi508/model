# -*- coding: utf-8 -*-
import math
import pandas as pd

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

        
