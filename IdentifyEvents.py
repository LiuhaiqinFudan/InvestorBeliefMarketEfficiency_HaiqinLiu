# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 21:23:21 2021

get degrading event from wind 

@author: Haiqin
"""
import os 
os.chdir(r"D:\Course2021Autumn\MachineLearningFintech\project")

from WindPy import *
w.start()

import pandas as pd 
pd.read_csv("allComments.csv")

# 不太方便，得明早修复，所以还是先用excel