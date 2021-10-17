# -*- coding: utf-8 -*-
"""
Created on Sep 28 19:49:34 2021

@author: Haiqin Liu
"""
import pandas as pd
from jiebacut import clean_cut
from gensim.models import Word2Vec
import os

li = []
for corpus in os.listdir('OutPuts'):
    remarks = pd.read_csv('OutPuts\\'+corpus, encoding = 'gbk')
    sentences = []
    for text in remarks.remark:
        try:
            sentences.append(clean_cut(text))
        except:
            pass
    li.extend(sentences)

#model = Word2Vec(li, sg=1, size=100, window=5, min_count=1, workers=4)
#model.save('sgmodel.model')

model = Word2Vec(li, sg=0, size=100, window=5, min_count=1, workers=4)
model.save('CBOWmodel.model')