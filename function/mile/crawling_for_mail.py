# -*- coding: utf-8 -*-
import urllib.request as req
import json 
import pandas as pd
import time
from bs4 import BeautifulSoup
from function.mail_func import exchange, premiumFunc, mail

  
def crawling(x='bithumb',y='poloniex') :
    url={'bithumb':"https://api.bithumb.com/public/ticker/BTC",
         'coinone':"https://api.coinone.co.kr/ticker/?currency=btc&format=json",
         'poloniex':"https://poloniex.com/public?command=returnTicker",
         'kraken':"https://api.kraken.com/0/public/Ticker?pair=XBTUSD",
         'bitfinex':"https://api.bitfinex.com/v1/pubticker/btcusd"
         }
    global err_code
    
    
    if (x=='bithumb' or x=='coinone') and (y=='poloniex' or y=='kraken' or y=='bitfinex') :
        crawling_url_K =url[x]
        crawling_url_U =url[y]
        
        #try
        
        data_K=json.loads((req.urlopen(crawling_url_K).read()).decode('utf-8'))
        data_U=json.loads((req.urlopen(crawling_url_U).read()).decode('utf-8'))
        
        
        err_code=0        
        if x=='bithumb' :
            
            if data_K['status']=='0000' :
                k_price=data_K['data']['closing_price']
            else :
                err_code=1
                print('bithumb error')
                data_K=json.loads((req.urlopen(url['coinone']).read()).decode('utf-8'))
                if data_K['result']=='success' :
                    k_price=data_K['last']
                else :
                    err_code=12
                    print('coinone error')
                
        if x=='coinone' :
            
            if data_K['result']=='success' :
                 k_price=data_K['last']
            else :
                err_code=2
                print('coinone error')
                data_K=json.loads((req.urlopen(url['bithumb']).read()).decode('utf-8'))          
                if data_K['status']=='0000' :
                    k_price=data_K['data']['closing_price']
                else :
                    err_code=11
                    print('bithumb error')

        if y =='poloniex' :
            
            try :
                u_price=data_U['USDT_BTC']['last']
            except:
                print('poloniex error')
                err_code=3
                data_U=json.loads((req.urlopen(url['bitfinex']).read()).decode('utf-8'))
                u_price=data_U['last_price']
                
        if y =='kraken' :
            
            if data_U['error'] ==[] :
                u_price=data_U['result']['XXBTZUSD']['c'][0] 
            else :
                err_code=4
                print('kraken error')
                data_U=json.loads((req.urlopen(url['poloniex']).read()).decode('utf-8'))
                u_price=data_U['USDT_BTC']['last']
                
        if y=='bitfinex' :
            try :   
                u_price=data_U['last_price']
            except :
                print('bitfinex error')
                err_code=5
                data_U=json.loads((req.urlopen(url['poloniex']).read()).decode('utf-8'))
                u_price=data_U['USDT_BTC']['last']
                      
    else :
        print('parameter error')
        err_code='pameter error'
            
    premium=premiumFunc(k_price,u_price)
    print(
        "krw:", k_price,
        "usd:", u_price,
        "premium:", premium
        )    
    return premium




# coinone, kraken data 파일로 떨구는 함수 (한시간 마다 떨구면 될듯 )
def data_to_file(i) : 
    now_timestamp=str(time.time()).replace(".","")+'00'
    before_hour_timestamp=str(int(now_timestamp)-3600000000000)
    url_coinone = 'https://api.coinone.co.kr/trades/?currency=btc&period=hour&format=json'
    url_kraken = 'https://api.kraken.com/0/public/Trades?pair=XBTUSD&since='+before_hour_timestamp # since 값을 한시간씩 옮기면 될듯.
 
    
    res_coinone=req.urlopen(url_coinone).read()
    data_coinone=json.loads(res_coinone.decode('utf-8'))
    data_coinone=pd.DataFrame(data_coinone['completeOrders'])
    data_coinone=data_coinone[['timestamp','price','qty']]
    json_to_file(data_coinone,'coinone',i)
      
    
    res_kraken=req.urlopen(url_kraken).read()
    data_kraken=json.loads(res_kraken.decode('utf-8'))
    data_kraken=pd.DataFrame(data_kraken['result']['XXBTZUSD'])
    data_kraken=data_kraken[[2,0,1]]
    data_kraken.columns=['timestamp','price','qty']
    json_to_file(data_kraken,'kraken',i)


def exchange_rate_to_file(exchange_data,i):
    i=str(i)
    exchange_rate=pd.DataFrame(exchange_data)
    exchange_rate.to_csv('data/exchange_rate_'+i+'.csv') 
    
def json_to_file(data,coinone,i):
    i=str(i)
    data=pd.DataFrame(data)
    data.to_csv('data/'+coinone+i+'.csv') 







     
    
#def crawling() :
#    url_bithumb="https://api.bithumb.com/public/ticker/ALL"
#    url_coinone="https://api.coinone.co.kr/ticker/?currency=all&format=json"
#    url_poloniex="https://poloniex.com/public?command=returnTicker"
#    url_exchange_rate="http://info.finance.naver.com/marketindex/?tabSel=exchange#tab_section"
#    url=[url_bithumb, url_coinone, url_poloniex, url_exchange_rate]
#    web_data={}
#    err=0
#    z=0
#    e=0
#    while True :
#        try :        
#            for i,j in enumerate(url) :
#                res=req.urlopen(j)
#                data=json.load(res)
#                if i==0 :
#                    if data['status']=='0000' :
#                        web_data['bithumb']=data['data']
#                    else :
#                        err=10
#                if i==1 : 
#                    if data['errorCode']=='0' :
#                        web_data['coinone']=data
#                    else :
#                        err=11
#                if i==2 : 
#                    #poloniex status 값
#                    web_data['poloniex'] =data
#                if i==3 :
#                    b=exchange()
#                    
#        
#            time.sleep(10)
#        except :
#            pass
#        premium=premiumFunc(web_data['bithumb']['BTC']['sell_price'],web_data['poloniex']['USDT_BTC']['last'])
#        print(
#            "bithumb:", web_data['bithumb']['BTC']['sell_price'],
#            "coinone:",web_data['coinone']['btc']['last'],
#            "poloniex:",web_data['poloniex']['USDT_BTC']['last'],
#            "premium:", premium)
#        
#        return premium
##        if z==0 :
##            if premium > 0.03 :
##                mail('more than 3%')
##                z+=1
##        if e==0 : 
##            if premium < 0.02 :
##                mail('less than 2%')
##                e+=1
#        
            
