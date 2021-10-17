# -*- coding: utf-8 -*-
"""
Created on Sep 28 19:57:35 2021

@author: Haiqin Liu
"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.gaussian_process.kernels import RBF
from sklearn.gaussian_process import GaussianProcessClassifier 
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from gensim.models import Word2Vec
import pandas as pd

model = Word2Vec.load('CBOWmodel.model')
X = model[model.wv.index2word]  # 词向量矩阵
X = PCA(n_components = 2).fit_transform(X)[:10000]

nf = pd.read_csv('WordVecScore_CBOW.csv', encoding='gbk') 

con_y = np.array(nf['score'])[:10000]    # 连续取值
y = np.sign(con_y) + 1

C = 1.0
kernel = 1.0 * RBF([1.0, 1.0]) # for GPC
classifiers = {'L1 logistic': LogisticRegression(C=C, penalty='l1'),
                'L2 logistic (OvR)': LogisticRegression(C=C, penalty='l2'),
                'L2 logistic (Multinomial)': LogisticRegression(
                C=C, solver='lbfgs', multi_class='multinomial'),
                'GPC': GaussianProcessClassifier(kernel) 
                }
n_classifiers = len(classifiers)

plt.figure(figsize=(3 * 2, n_classifiers * 2))
plt.subplots_adjust(bottom=.2, top=.95)

xx = np.linspace(3, 9, 100)
yy = np.linspace(1, 5, 100).T
xx, yy = np.meshgrid(xx, yy)
Xfull = np.c_[xx.ravel(), yy.ravel()]

for index, (name, classifier) in enumerate(classifiers.items()):

    classifier.fit(X, y)
    
    y_pred = classifier.predict(X)
    classif_rate = np.mean(y_pred.ravel() == y.ravel()) * 100
    print("classif_rate for %s : %f " % (name, classif_rate))
    
    # View probabilities=
    probas = classifier.predict_proba(X)
    n_classes = np.unique(y_pred).size
    for k in range(n_classes):
        plt.subplot(n_classifiers, n_classes, index * n_classes + k + 1)
        plt.title("Class %d" % k)
        if k == 0:
            plt.ylabel(name)
        imshow_handle = plt.imshow(probas[:, k].reshape((100, 100)),
                                 extent=(3, 9, 1, 5), origin='lower')
        plt.xticks(())
        plt.yticks(())
        idx = (y_pred == k)
        if idx.any():
            plt.scatter(X[idx,0], X[idx,1], marker='.', c='k')
ax = plt.axes([0.15, 0.04, 0.7, 0.05])
plt.title("Probability")
plt.colorbar(imshow_handle, cax=ax, orientation='horizontal')
plt.show()














