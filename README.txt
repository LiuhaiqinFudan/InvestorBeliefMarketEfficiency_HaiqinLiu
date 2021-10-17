:scrap.py: 爬取东方财富股市论坛

:stopwords.py --> stopwords.txt
结巴分词中需去掉的stopwords

:jiebacut.py
结巴分词处理的模块

:Model.py  --> CBOWmodel.model/sgmodel.model
用所有的数据建立Word2Vec model

:VecScore.py --> WordVecScore.csv
KMeans聚类后手动为聚类中心点打分，并以similarity计算分数

:ScoreRemark.py --> stock result.csv (见以result命名的文件夹)
为每个样本打分

:SemiSupervise.py --> semi-label-continuous.csv
半监督学习返回词向量打分（连续概率输出）

:LinearModel.py
使用LogisticRegression为词向量打分

:AllClass.py
使用9种分类器的robustness check

:BaiduNlp.py
百度AI开发平台

股票代码与文件对应序号及数据量:
2   000651 169505
20 000338 152448
3   000723 96729
4   600352 155750
5   000725 601412
6   000927 80881
7   000858 195761
8   600875 150228
9   600519 290855
1   000681 48466
10 600150 143139
12 000735 428160
13 002565 82823
14 002118 106958
15 000159 83801
16 600030 554682
17 600218 84067
18 000862 60770
19 300176 240372
20 000338 152448
11 002450 190856