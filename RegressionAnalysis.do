********************************************************************************
********************* Merge with the A share stock basic info ******************
*********************     And conduct regression analysis     ******************
********************************************************************************
clear all 
cd "D:\Course2021Autumn\MachineLearningFintech\project"

import excel using "RawData\scorePrice.xlsx", firstrow clear 

* stkid stkname sentiment_score_guba sentiment_score_wsj price turnover volume 