# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 15:53:17 2018

@author: user
"""
#pip install PyMySQL
import pymysql

def get_memberlist(predict_percent) :
    
    predict_percent=str(predict_percent)
    # MySQL Connection 연결
    conn = pymysql.connect(host='10.1.43.149', user='rabbit', password='rabbit',db='kps', charset='utf8')
     
    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()
     
    # SQL문 실행
    sql = "select address from contact where member_no in (select member_no from alarm where percent="+predict_percent+" and type=1) and type=1 and certification=1"
    curs.execute(sql)
    
    # 데이타 Fetch
    rows = curs.fetchall()
    rows=list(rows)
    memberlist=[]
    
    for i,j in enumerate(rows):
        memberlist.append(rows[i][0])
       
    # Connection 닫기
    conn.close()
    return memberlist

#get_memberlist(3.0)
