********************************************************************************
**************** Annotate the data using down rating Events  *******************
********************************************************************************
clear all 
global root = "D:\Course2021Autumn\MachineLearningFintech\project"
cd "$root"

global trainratio = 0.4  // 40% as insample trained

import excel using "CleanData\allComments-wind.xlsx", firstrow clear 
* this is the output of CleanRemarks.do, and daily market data retrieved from wind

gen microtime = clock(time, "MDYhm")
format microtime %tc

sort stkid microtime 

gen     ratingGrade = 1 if rating == "AAA"
replace ratingGrade = 2 if rating == "AA+"
replace ratingGrade = 3 if rating == "AA-"
replace ratingGrade = 4 if rating == "A+"
replace ratingGrade = 5 if rating == "A"
replace ratingGrade = 6 if rating == "A-"
replace ratingGrade = 7 if rating == "BBB+"
replace ratingGrade = 8 if rating == "BB+"
replace ratingGrade = 9 if rating == "BB"
replace ratingGrade = 10 if rating == "BB-"
replace ratingGrade = 11 if rating == "B"
replace ratingGrade = 12 if rating == "CCC"
replace ratingGrade = 13 if rating == "CC"
replace ratingGrade = 14 if rating == "C"
replace ratingGrade = 15  if rating == "0"  // not rated: 视为信用资质最差，无法发债融资

gen ddate = dofc(microtime)
format ddate %td

bys stkid (microtime): gen badnews  = (ratingGrade >  ratingGrade[_n-1]) if _n > 1 & ratingGrade != .
replace badnews = 1 if dofc(microtime) >= 22159  & substr(stkid, 6,2) == "HK"   // 2020/9/1三道红线以来房企处于政策紧周期；目前样本港交所上市样本仅有国企

bys stkid (microtime): gen goodnews = (ratingGrade <= ratingGrade[_n-1]) if _n > 1 & ratingGrade[_n-1] != .
 // if keep the previous rating, take as good news (like 展望稳定)
 
save CleanData\allComments-wind, replace 
*use CleanData\allComments-wind, replace 

keep remark goodnews badnews 
duplicates drop 
save CleanData\allComments, replace 

keep if goodnews == 1            // only labeled 
gen selectrand = runiform()      // randomized split
sort selectrand 
keep if _n <= int(_N*$trainratio )  // traint:test = 4:6
keep remark 
duplicates drop 
local obs = _N 
forval k = 1/`obs'{
outsheet using "$root\chinese_sentiment-master\data\stock_comment\raw_data\pos\pos.`k'.txt" if _n == `k', replace nonames noquote
}

use CleanData\allComments, replace 
keep if badnews == 1   
gen selectrand = runiform() 
sort selectrand 
keep if _n <= int(_N*$trainratio )  
keep remark 
duplicates drop 
local obs = _N 
forval k = 1/`obs'{
qui outsheet using "$root\chinese_sentiment-master\data\stock_comment\raw_data\neg\neg.`k'.txt" if _n == `k', replace nonames noquote
}


use CleanData\allComments, replace 
keep if goodnews == . & badnews == .
gen selectrand = runiform() 
sort selectrand 
keep if _n <= int(_N*$trainratio )  
keep remark 
duplicates drop 
local obs = _N 
forval k = 1/`obs'{
qui outsheet using "$root\chinese_sentiment-master\data\stock_comment\raw_data\unlabeled\unlabeled.`k'.txt" if _n == `k', replace nonames noquote
}


* stkid date title view comment score


export excel using stockEvent-out.xlsx, firstrow(variables) replace
save stockEvent-out, replace
* then add fundamental variables from wind 

* then get the sentiment score for each comments 
import excel using allComments.xlsx, firstrow clear 
* stkid date title view comment score, minute level high frequency 
merge m:1 stkid date using stockEvent-out
keep if _merge == 3 
drop _merge 
save commentMerged, replace

*replace date = r(mean)+2 if ID - 4*int(ID/4)==2
*replace date = r(mean)+1 if ID - 4*int(ID/4)==1
*replace date = r(mean)+3 if ID - 4*int(ID/4)==3
