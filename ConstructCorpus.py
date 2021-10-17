# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 20:34:58 2021

Merge Stock Forum data to get High Frequency Panel and construct Corpus 

@author: Haiqin
"""
import os 
os.chdir(r"D:\Course2021Autumn\MachineLearningFintech\project")

import csv 

corpus = []

for f in os.listdir("RawData"):
    try:
        csv_reader = csv.reader(open(".\\RawData\\"+f))
        for line in csv_reader:
            line.append("'"+f[:-4])
            corpus.append(line)
    except UnicodeDecodeError:
        try: 
            csv_reader = csv.reader(open(".\\RawData\\",encoding = "utf8"))
            for line in csv_reader:
                line.append(f[:-4])
                corpus.append(line)
        except:
            print("not readable: ", f)
            pass


with open('allComments.csv',"w", newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    spamwriter.writerows(corpus)
    # 1st column: title; 2nd: views; 3rd: comments; 4th: stock code
    



