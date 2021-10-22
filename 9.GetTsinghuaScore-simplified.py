# --- encoding = utf-8 ----
# construct Tsinghua predictions

import os
import csv

# 1.存Tsinghua词库(有标签)的目录,获取正/负词库
os.chdir(r"D:\Course2021Autumn\MachineLearningFintech\project\sentiment_score-qinghualabel")
posset = []
negset = []
with open("tsinghua.positive.gb.txt") as f:
    for line in f:
        posset.append(line.replace("\n",""))
with open("tsinghua.negative.gb.txt") as f:
    for line in f:
        negset.append(line.replace("\n",""))
        
# 到保存jieba切词后的股吧评论文件夹,分别读取stuttered sentences
os.chdir(r"D:\Course2021Autumn\MachineLearningFintech\project\chinese_sentiment-master\data\stock_comment")  

## Evaluate set 
evaldata = []
with open("eval.words.txt", encoding="utf8") as inf:
    for line in inf.readlines():
        evaldata.append(line)

with open("evalsetcut.csv", encoding="gbk", mode="w+",newline='') as outf:
    csvwriter = csv.writer(outf)
    csvwriter.writerows(evaldata) # 然后打开保存为excel

evalclean = [d.replace("\n","") for d in evaldata]
evalscore = []
for word in evalclean:
    posnum = 0
    negnum = 0
    for d in word.split():
        if d in posset:
            posnum += 1
        if d in negset:
            negnum += 1
    try:
        score = posnum/len(word.split())
        evalscore.append([word, score])   # fraction of positive occurences
    except:
        evalscore.append([word, -1])  # -1 for words fail to be scored

with open("TsinghuaScoreEval.csv", "w+", encoding="gbk", newline='') as f:
    csvwriter = csv.writer(f)
    csvwriter.writerows(evalscore)
    
## Train Set
traindata = []
with open("train.words.txt", encoding="utf8") as inf:
    for line in inf.readlines():
        traindata.append(line)

with open("trainsetcut.csv", encoding="gbk", mode="w+", newline='') as outf:
    csvwriter = csv.writer(outf)
    csvwriter.writerows(traindata) # 然后打开保存为excel

trainclean = [d.replace("\n","") for d in traindata]
trainscore = []
for word in trainclean:
    posnum = 0
    negnum = 0
    for d in word.split():
        if d in posset:
            posnum += 1
        if d in negset:
            negnum += 1
    try:
        score = posnum/len(word.split())
        trainscore.append([word, score])   # fraction of positive occurences
    except:
        trainscore.append([word, -1])  # -1 for words fail to be scored

with open("TsinghuaScoretrain.csv", "w+", encoding="gbk",newline='') as f:
    csvwriter = csv.writer(f)
    csvwriter.writerows(trainscore)
    
    
## Unlabeled Set
unlabeldata = []
with open("unlabeled.words.txt", encoding="utf8") as inf:
    for line in inf.readlines():
        unlabeldata.append(line)

with open("unlabelsetcut.csv", encoding="gbk", mode="w+",newline='') as outf:
    csvwriter = csv.writer(outf)
    csvwriter.writerows(unlabeldata) # 然后打开保存为excel

unlabelclean = [d.replace("\n","") for d in unlabeldata]
unlabelscore = []
for word in unlabelclean:
    posnum = 0
    negnum = 0
    for d in word.split():
        if d in posset:
            posnum += 1
        if d in negset:
            negnum += 1
    try:
        score = posnum/len(word.split())
        unlabelscore.append([word, score])   # fraction of positive occurences
    except:
        unlabelscore.append([word, -1])  # -1 for words fail to be scored

with open("TsinghuaScoreunlabel.csv", "w+", encoding="gbk",newline='') as f:
    csvwriter = csv.writer(f)
    csvwriter.writerows(unlabelscore)
    

# 然后三个Tsingscore文件都打开，另存excel，到stata和原始comment文档merge
    
