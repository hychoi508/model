# -*- coding: utf-8 -*-
import urllib.request as req
import json 
import pandas as pd
import time
from bs4 import BeautifulSoup
from function.mail_func import exchange, premiumFunc, mail

url_bithumb="https://api.bithumb.com/public/ticker/ALL"
url_coinone="https://api.coinone.co.kr/ticker/?currency=all&format=json"
url_poloniex="https://poloniex.com/public?command=returnTicker"
url_exchange_rate="http://info.finance.naver.com/marketindex/?tabSel=exchange#tab_section"
url=[url_bithumb, url_coinone, url_poloniex, url_exchange_rate]

web_data={}
err=0
z=0
e=0
while True :
    try :        
        for i,j in enumerate(url) :
            res=req.urlopen(j)
            data=json.load(res)
            if i==0 :
                if data['status']=='0000' :
                    web_data['bithumb']=data['data']
                else :
                    err=10
            if i==1 : 
                if data['errorCode']=='0' :
                    web_data['coinone']=data
                else :
                    err=11
            if i==2 : 
                #poloniex status 값
                web_data['poloniex'] =data
            if i==3 :
                b=exchange()
                
    
        time.sleep(10)
    except :
        pass
    premium=premiumFunc(web_data['bithumb']['BTC']['sell_price'],web_data['poloniex']['USDT_BTC']['last'])
    print(
        "bithumb:", web_data['bithumb']['BTC']['sell_price'],
        "coinone:",web_data['coinone']['btc']['last'],
        "poloniex:",web_data['poloniex']['USDT_BTC']['last'],
        "premium:", premium)
    if z==0 :
        if premium > 0.03 :
            mail('more than 3%')
            z+=1
    if e==0 : 
        if premium < 0.02 :
            mail('less than 2%')
            e+=1
    
            
