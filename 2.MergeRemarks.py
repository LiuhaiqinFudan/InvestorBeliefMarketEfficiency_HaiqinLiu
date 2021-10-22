# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 20:34:58 2021

Merge Stock Forum data to get High Frequency Panel and construct Corpus 
Input: RawData\个股股吧评论数据(scraped)
OutPut: allComments.xlsx, 包括股票代码(文件名,手动修改),经过清理的评论

@author: Haiqin
"""
import os 
os.chdir(r"D:\Course2021Autumn\MachineLearningFintech\project")

import csv 

corpus = []

for f in os.listdir("RawData"):
    
    try:
        csv_reader = csv.reader(open(".\\RawData\\"+f))  # 默认编码,不确定是哪种
        for line in csv_reader:
            if line[1] == "":        # 漏爬评论样本剔除
                pass 
            else:
                line.append(f[:-4])  # 文件名改为股票代码
                corpus.append(line)
    except:
        try: 
            csv_reader = csv.reader(open(".\\RawData\\",encoding = "utf8"))
            for line in csv_reader:
                if line[1] == "":        # 漏爬评论样本剔除
                    pass 
                else:
                    line.append(f[:-4])  # 文件名改为股票代码
                    corpus.append(line)
        except:
            print("not readable: ", f)


with open('CleanData\\allComments.csv',"w", newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    spamwriter.writerows(corpus)
    # 1st column: title; 2nd: views; 3rd: comments; 4th: stock code
    # 然后拉wind公式(主体信用评级),保存为excel格式,去stata进一步定义NEGATIVE和POSITIVE及数据清洗
    # 然后生成样本丢进sentiment analysis Github里去train
    # 然后predict出来dummy为解释变量进行回归(需要merge m:1)



