********************************************************************************
********************* Merge with the A share Rating/Events  ********************
********************************************************************************
clear all 
global root "D:\Course2021Autumn\MachineLearningFintech\project"
cd "$root"
global trainratio = 0.6  // 60% as insample trained

import excel using "allComments.xlsx", firstrow clear 
* this is the output of ConstructCorpus.py, it combines all the comments scraped from guba 


keep date stkid
duplicates drop 
export excel using "stockRating-out.xlsx", firstrow(variables) replace
* the fetch the latest market credit rating from wind 
* an upgrading(degrading) is identified as bad(good) news
import excel using "stockRating-in.xlsx", firstrow clear 

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
replace ratingGrade = 15 if rating == "0"  // not rated

bys stkid (date): gen badnews = (rating < rating[_n-1]) if _n > 1
bys stkid (date): gen goodnews = (rating >= rating[_n-1]) if _n > 1 
 // if keep the previous rating, take as good news


* stkid stkname sentiment_score_guba sentiment_score_wsj price turnover volume 
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

keep if goodnews  // only labeled 
gen selectrand = runiform() 
sort selectrand 
keep if _n <= int(_N*$trainratio )  // traint:test = 6:4
keep remark 
local obs = _N 
forval k = 1/`obs'{
preserve 
keep if _n == `k'
outsheet using "$root\chinese_sentiment-master\data\hotel_comment\raw_data\pos\pos.`k'.txt", replace nonames noquote
restore
}

use commentMerged, replace
keep if badnews  // only labeled 
gen selectrand = runiform() 
sort selectrand 
keep if _n <= int(_N*$trainratio )  // traint:test = 6:4
keep remark 
local obs = _N 
forval k = 1/`obs'{
preserve 
keep if _n == `k'
outsheet using "$root\chinese_sentiment-master\data\hotel_comment\raw_data\neg\neg.`k'.txt", replace nonames noquote
restore
}


* stkid date title view comment score


