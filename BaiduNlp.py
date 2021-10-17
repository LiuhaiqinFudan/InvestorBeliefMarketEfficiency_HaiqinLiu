# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 23:35:38 2019

@author: Thetis
"""
from aip import AipNlp
import os
import pandas as pd
import csv

APP_ID = '16012696'
API_KEY = 'CGSpjBMuhZjYEGewoRmNBart'
SECRET_KEY = 'Wa3rfzaGi1BR0zfClGlzqoXthnvgGZR1'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

def get_sentiments(text, outfile):
    try:
        sitems = client.sentimentClassify(text)['items'][0]#情感分析
        positive = sitems['positive_prob']#积极概率
        confidence = sitems['confidence']#置信度
        sentiment = sitems['sentiment']#0表示消极，1表示中性，2表示积极
        #tagitems = client.commentTag(text, {'type': 9})  # 评论观点
        #propertys=tagitems['prop']#属性
        #adj=tagitems['adj']#描述词
        '''
        output='{}\t{}\t{}\n'.format(positive,confidence,sentiment)
        f=codecs.open(outfile,'a+','utf-8')
        f.write(output)
        f.close()
        '''
        f = open(outfile, 'a+',  newline='')
        writer = csv.writer(f, delimiter = ',')
        writer.writerow([positive,confidence,sentiment])
        f.close()
        print('Done')
    except Exception as e:
        print(e) 

if __name__ == "__main__":
    for corpus in os.listdir('result2'):
        corpusname = corpus[:-4]
        df = pd.read_csv('result2\\'+corpus, encoding='utf8')
        for remark in df.remark:
            get_sentiments(remark, corpusname+' baidu.csv')