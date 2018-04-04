# -*- coding: utf-8 -*-
import urllib.request as req
import smtplib
from bs4 import BeautifulSoup


def exchange():
    url="http://info.finance.naver.com/marketindex/?tabSel=exchange#tab_section"
    res=req.urlopen(url).read()
    soup=BeautifulSoup(res,'html.parser')
    soup=soup.find_all("span")
    j=0
    for a in soup :
        j+=1
        if j==3:
            b=a.string
    b=float(b.replace(",",""))
    return b
    
def premiumFunc(a,b) :
    a=float(a)
    b=float(b)
    c=(a-b*exchange())/(b*exchange())
    return c


# Specifying the from and to addresses

def mail(x,y):
    username = 'koreanpremium' #without @gmail.com only write Google Id.
    password = 'koreanadmin'
    fromaddr = 'koreanpremium@gmail.com'
    msg =x
    
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    
    for i in y :
        toaddrs  = i
        server.sendmail(fromaddr, toaddrs, msg)
   
    server.quit()





#def mail(x, toaddrs):
#    fromaddr = 'koreanpremium@gmail.com'
#
## Writing the message (this message will appear in the email)
#
#    msg =x
#
## Gmail Login
#
#    username = 'koreanpremium' #without @gmail.com only write Google Id.
#    password = 'koreanadmin'
#
## Sending the mail
#
#    server = smtplib.SMTP('smtp.gmail.com:587')
#    server.starttls()
#    server.login(username,password)
#    set(map(lambda to:server.sendmail(fromaddr,to,msg),toaddrs))
#    server.quit()


#Data_K['5min_0']=pd.DataFrame(list(map(lambda x:time_generation(x,0),Data_K['time'])))
    
    
#def mail(x):
#    fromaddr = 'koreanpremium@gmail.com'
#    toaddrs  = 'jwy627@naver.com'
#
## Writing the message (this message will appear in the email)
#
#    msg =x
#
## Gmail Login
#
#    username = 'koreanpremium' #without @gmail.com only write Google Id.
#    password = 'koreanadmin'
#
## Sending the mail
#
#    server = smtplib.SMTP('smtp.gmail.com:587')
#    server.starttls()
#    server.login(username,password)
#    server.sendmail(fromaddr, toaddrs, msg)
#    server.quit()