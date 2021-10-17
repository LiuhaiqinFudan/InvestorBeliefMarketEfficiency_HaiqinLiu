# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 22:41:58 2019

Clean the comments, remove stopwords

@author: Haiqin Liu
"""
import jieba
import json
import re

def clean_text(text):
    '除去除中英文外的字符及多余空格'
    rule = re.compile(u'[^a-zA-Z\u4e00-\u9fa5]')
    text = rule.sub(' ', text)
    re.sub(r'\s+', '', text)
    return text

def clean_cut(sentence):
    # 载入json手写的stopwords, 来源http://www.baiduguide.com/baidu-stopwords/
    f = open('stopwords.txt', 'r')
    stopwords = json.load(f).split(',')
    f.close()
    
    cuts = []
    sentence = clean_text(sentence)
    for seg in jieba.cut(sentence):
        if seg not in stopwords and seg != " ":
            cuts.append(seg.replace(' ', ''))
    return cuts
