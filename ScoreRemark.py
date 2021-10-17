# -*- coding: utf-8 -*-
"""
Created on Sep 28 19:54:11 2021

@author: Haiqin Liu
"""
from jiebacut import clean_cut
import pandas as pd
import os
import numpy as np


vec_score = pd.read_csv('semi_compact.csv', encoding='gbk')
                                      # sg

methods = vec_score.columns[2:]  # 除第一列为word, 第二列为labeled score
print('finish VecScore loading')

def avg_score(header, remark):
    '根据每种分类方法计算加权分数'
    weighted_score = 0
    total_score = 0
    words = clean_cut(remark)
    
    for word in words:
        try:
            score = vec_score[header].loc[
                np.where(np.array(vec_score['word']) == word)[0][0]]
        except:
            score = 0           
        
        total_score += abs(score) 
        weighted_score += score * abs(score)
   
    if total_score != 0:
        weighted_score /= total_score  # 以该词自身的score为权重
    else:
        weighted_score = 0
        # 此情况只有当该条评论jieba cut后啥也不剩了才出现
    return weighted_score


for corpus in os.listdir('OutPuts'):
    corpusname = corpus[:-4] 
    remarks = pd.read_csv('OutPuts\\'+corpus, encoding = 'gbk')[:100]
    
    scores = np.array([0,0,0,0])
    for remark in remarks['remark']:
        sentence_score = []
        for method in methods:   # 第一行是分类方法名
            method_score = avg_score(method, remark)
            sentence_score.append(method_score)
           
        scores = np.vstack((scores, sentence_score))
    
    
    pd.DataFrame(scores[1:],columns=['ls 10%','ls 30%',"ls 50%", 
                'svm']).to_csv(corpusname+' semi-supervise result.csv', index=False)
    print('Done')
     
    
    
    
    
    
    
    