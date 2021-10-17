# -*- coding: utf-8 -*-
"""
Created on Sep 28 19:52:51 2021

@author: Thetis
"""

import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from sklearn.cluster import KMeans
import random

# 加载用所有的remarks建立的corpus
model = Word2Vec.load('CBOWmodel.model')
#model = Word2Vec.load('sgmodel.model')
print('finish loading')

word_mat = model[model.wv.index2word]

n_clusters = 100
  
kmeans = KMeans(n_clusters=n_clusters, random_state=0)

indices = [i for i in range(len(word_mat))]
random.shuffle(indices)
kmeans.fit(word_mat[indices[:10000],:])
print('finish kmeans training')


def interact_console(index):
    "控制台交互"
    print("the center word in the cluster is:")
    print(model.wv.index2word[index])
    label = eval(input('label? '))
    assert label in {-1, 0, 1}, 'invalid label'
    return label


def group_score(group_index):
    "每个clustering group人工打分"
    center = kmeans.cluster_centers_[group_index]
    class_ = np.where(kmeans.predict(word_mat) == group_index)[0]
    group = word_mat[class_,:]
    
    # 计算向量欧氏距离
    distances = np.power(np.sum(np.power(group-center, 2), axis=1), 0.5)
    
    # 选取距离聚类中心最近词打印至控制台手动label
    closest = np.argmin(distances)
    center_score = interact_console(class_[closest])
    
    scores = []
    for i in class_:
        # 根据到手动label词的similarity打分
        scores.append(center_score*model.similarity(model.wv.index2word[i], 
                                       model.wv.index2word[closest]))
    return np.array(scores)


word_vec_score = [0 for i in range(len(model.wv.index2word))]
for index in range(n_clusters):
    nodes = np.where(kmeans.predict(word_mat) == index)[0]
    group_scores = group_score(index)
    for i in range(len(nodes)):
        word_vec_score[nodes[i]] = group_scores[i].sum()

model_score = zip(model.wv.index2word, word_vec_score)
pd.DataFrame(model_score, columns=['word', 'score']).to_csv(
        'WordVecScore_CBOW.csv',index=False)
