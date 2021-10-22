# -*- coding: utf-8 -*-
"""
Created on Sep 28 15:51:59 2021
Scrape Stock Forum Remark Data from Eastmoney Website
@author: Haiqin Liu
"""

import requests
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd
import os 
import time

os.chdir(r"D:\Course2021Autumn\MachineLearningFintech\project")
df = pd.read_excel(r'RawData\SampleSelected-A股+中概股+港交所.xlsx')

def get_time(url,head):
    # 打开详情页面获取发帖时间
    try:
        q = requests.get(url,headers=head)
        soup = BeautifulSoup(q.text,'html.parser')
        ptime = soup.find('div',{'class':'zwfbtime'}).get_text()
        ptime = re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',ptime)[0]
        return ptime
    except:
        return ''
                    
def get_urls(fw, url, head):
    baseurl = 'http://guba.eastmoney.com/'
    q = requests.get(url,headers=head)
    soup = BeautifulSoup(q.text,'html.parser')
    urllist = soup.findAll('div',{'class':'articleh'})
    for i in urllist:
        if i.find('a') != None:
            try:
                detailurl = i.find('a').attrs['href'].replace('/','')  #超链接
                title = i.find('a').attrs['title']                     #完整标题
                yuedu = i.find('span',{'class':'l1 a1'}).get_text()    #阅读量
                pinlun = i.find('span', {'class': 'l2 a2'}).get_text() #评论量
                ptime = get_time(baseurl+detailurl,head)               #时间
                fw.writerow([title,yuedu,pinlun,ptime])
            except:
                print("error!")
            
head ={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
       'Accept-Encoding':'gzip,deflate',
       'Accept-Language':'zh-CN,zh;q=0.9',
       'Cache-Control':'max-age=0',
       'Connection':'keep-alive',
       'Cookie':'st_pvi=87732908203428;st_si=12536249509085;qgqp_b_id=9777e9c5e51986508024bda7f12e6544;_adsame_fullscreen_16884=1',
       'Host':'guba.eastmoney.com',
       'Referer':'http://guba.eastmoney.com/list,600596,f_1.html',
       'Upgrade-Insecure-Requests':'1',
       'User-Agent':'Mozilla/5.0(WindowsNT6.1;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/65.0.3325.181Safari/537.36'}
 
for i in range(len(df.gubaSymbol)):  # 已经在Selected sample excel中改成guba链接识别的格式(如3333.HK对应hk03333,url=http://guba.eastmoney.com/list,hk03333.html)
    
    stkid = str(df.证券代码[i])
    stock = str(df.gubaSymbol[i])
    pagen = int(df.pagenum[i])
    page = (1, pagen)
    
    time_start = time.time()
    
    f = open('RawData\\'+stkid+'.csv', 'a', newline='')
    w = csv.writer(f)
    w.writerow(['remark', 'reading', 'comment','time'])

    #循环所有页数 
    for i in range(*page):
        
        print(stock + " page" + str(i))  # 有时会出现页面异常,重复读取股吧总站新闻;后续对原始数据进行清晰
        get_urls(w,'http://guba.eastmoney.com/list,'+stock+'_'+str(i)+'.html',head)
    
    f.close()   
    time_end = time.time()
    print("time cost: ", time_end-time_start, "s")

## output: RawData, 个股的csv





