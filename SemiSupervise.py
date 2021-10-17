Logistic
# -*- coding: utf-8 -*-
"""
Created on Sep 28 19:56:04 2021

@author: Haiqin Liu
"""

# sklearn semi-supervision
# my comment: out; original one: inline

import numpy as np
from sklearn import svm
from sklearn.semi_supervised import LabelSpreading
import pandas as pd
from gensim.models import Word2Vec
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

batch_num = 10
model = Word2Vec.load('CBOWmodel.model')
X = model[model.wv.index2word]  # 词向量矩阵
X = PCA(n_components = 2).fit_transform(X)

nf = pd.read_csv('WordVecScore_CBOW.csv', encoding='gbk') 

con_y = np.array(nf['score'])    # 连续取值

hist, edge = np.histogram(con_y)
plt.plot(hist, 'g', label = 'labeled')


y = np.sign(con_y) + 1  # 0 1 2

batch_size = len(X)//batch_num  # 大约每30000条数据train一次

predictions_1 = np.array([0,0,0],dtype='float64')
predictions_3 = np.array([0,0,0],dtype='float64')
predictions_5 = np.array([0,0,0],dtype='float64')

svm_predict = np.array([0,0,0],dtype='float64')

for i in range(batch_num-1):
    X_batch = X[i*batch_size: (i+1)*batch_size]
    y_batch = y[i*batch_size: (i+1)*batch_size]
    indices = [i for i in range(len(y_batch))]
    np.random.shuffle(indices)
    
    train_size = int(len(X_batch)//3)  # train/test ~ 1:2
    train_x = X_batch[indices[:train_size]]
    train_y = y_batch[indices[:train_size]]
    
    indices = [i for i in range(len(train_y))]
    
    train_y_1 = train_y.copy()
    train_y_3 = train_y.copy()
    train_y_5 = train_y.copy()
    
    # 随机设置unlabel data
    np.random.shuffle(indices)
    train_y_1[indices[:int(.1*len(train_y))]] = -1    #10%
    
    np.random.shuffle(indices)
    train_y_3[indices[:int(.3*len(train_y))]] = -1    #30%
    
    np.random.shuffle(indices)
    train_y_5[indices[:int(.5*len(train_y))]] = -1    #50%
    
    print('finish shuffle')

# -------------------------------- training -----------------------------------
    rng = np.random.RandomState(42)

    ls_1 = LabelSpreading().fit(train_x, train_y_1)      
    res_ls_1 = ls_1.predict_proba(X_batch)
    predictions_1 = np.vstack((predictions_1,res_ls_1))
    print('finish ls 0.1')
    
    ls_3 = LabelSpreading().fit(train_x, train_y_3)
    res_ls_3 = ls_3.predict_proba(X_batch)
    predictions_3 = np.vstack((predictions_3,res_ls_3))
    print('finish ls 0.3')

    ls_5 = LabelSpreading().fit(train_x, train_y_5)
    res_ls_5 = ls_5.predict_proba(X_batch)
    predictions_5 = np.vstack((predictions_5,res_ls_5))
    print('finish ls predict 0.5')
    
    # ------------------------------ svm -------------------------------
    rbf_svc = svm.SVC(kernel='rbf', probability=True,
                      gamma=.5).fit(train_x, train_y)  # 无unlabel data
    res_svc = rbf_svc.predict_proba(X_batch)
    svm_predict = np.vstack((svm_predict, res_svc))  
    print('finish svm predict')
    
# 再做最后一个batch
X_batch = X[(i+1)*batch_size:,]
y_batch = y[(i+1)*batch_size:]
indices = [i for i in range(len(y_batch))]
np.random.shuffle(indices)

train_size = int(len(X_batch)//3) 
train_x = X_batch[indices[:train_size],:]
train_y = y_batch[indices[:train_size]]

indices = [i for i in range(len(train_y))]

train_y_1 = train_y.copy()
train_y_3 = train_y.copy()
train_y_5 = train_y.copy()

# 随机设置unlabel data
np.random.shuffle(indices)
train_y_1[indices[:int(.1*len(train_y))]] = -1  

np.random.shuffle(indices)
train_y_3[indices[:int(.3*len(train_y))]] = -1 

np.random.shuffle(indices)
train_y_5[indices[:int(.5*len(train_y))]] = -1 

print('finish shuffle')

rng = np.random.RandomState(i)  #伪随机种子

ls_1 = LabelSpreading().fit(train_x, train_y_1)      
res_ls_1 = ls_1.predict_proba(X_batch)
predictions_1 = np.vstack((predictions_1,res_ls_1))

ls_3 = LabelSpreading().fit(train_x, train_y_3)
res_ls_3 = ls_3.predict_proba(X_batch)
predictions_3 = np.vstack((predictions_3,res_ls_3))

ls_5 = LabelSpreading().fit(train_x, train_y_5)
res_ls_5 = ls_5.predict_proba(X_batch)
predictions_5 = np.vstack((predictions_5,res_ls_5))

print('finish ls predict')


rbf_svc = svm.SVC(kernel='rbf', probability = True, 
                  gamma=.5).fit(train_x, train_y)
res_svc = rbf_svc.predict_proba(X_batch)
svm_predict = np.vstack((svm_predict, res_svc))

print('finish svm predict')

i = 0
sett = ['b-', 'c-', 'm-', 'r--']
labels = ['ls(10%)', 'ls(30%)', 'ls(50%)', 'svm']
for prediction in (predictions_1, predictions_3, predictions_5, svm_predict):
    # 计算score的期望(前面返回的是属于三类的概率)
    prediction = np.dot(prediction[1:], np.array([-1, 0, 1]).T)
    prediction[np.where(np.isfinite(prediction)==0)[0]] = 0
    hist, bin_edges = np.histogram(np.around(prediction, 5))
    plt.plot(hist, sett[i], label=labels[i])
    nf[labels[i]] = prediction
    i += 1

plt.xlim(0,1)
plt.legend()
plt.show()  

nf.to_csv('semi_label_continuous.csv', index=False)

































