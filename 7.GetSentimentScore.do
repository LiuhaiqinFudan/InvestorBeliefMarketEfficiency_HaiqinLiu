**************************************************************
********************  取回CNN/LSTM预测结果  ******************
**************************************************************
clear all 
global root "D:\Course2021Autumn\MachineLearningFintech\project - copy"
cd "$root"

* 具体长度,替换逗号为中文,去掉空白评论否则读取错位等,打开文件看看判断一下
infile str3 tag str3 predict str200 remark using "chinese_sentiment-master\model\cnn\results\score\eval.preds.txt", clear 
duplicates drop remark, force   // 只需保留每条remark对应的情感打分
compress
save CleanData\predictions1, replace

infile str3 tag str3 predict str200 remark using "chinese_sentiment-master\model\cnn\results\score\train.preds.txt", clear 
duplicates drop remark, force   // 只需保留每条remark对应的情感打分
compress
append using CleanData\predictions1
duplicates drop remark, force 
save CleanData\predictions, replace 

drop if remark == "[图片]"

import excel using allComments.xlsx, firstrow clear 
duplicates drop 
merge m:1 remark using CleanData\predictions
keep if _merge == 3 
drop _merge 

replace time = time[_n-1] if time == ""
replace time = time[_n+1] if time == ""

gen blanc = strrpos(time, " ")
gen datestr = substr(time,1,blanc-1)
drop blanc 

gen     stkid = "000063.SZ" if symbol == "'000063"  // 中兴通讯
replace stkid = "601588.SH" if symbol == "'601588"  // 北辰实业 
replace stkid = "600585.SH" if symbol == "'600585"  // 海螺水泥 
drop symbol 

export excel using stockScore.xlsx, firstrow(variables) replace
* 然后在excel中调用价格行情等指标

import excel using stockScore-withwind.xlsx, firstrow clear 

* reduced form 
gen positive = (predict == "POS")
gen lnvol = log(volume)
est clear
eststo: reghdfe price pos, a(stkid datestr)
eststo: reghdfe lnvol pos, a(stkid datestr)
eststo: reghdfe turnover pos, a(stkid datestr)
eststo: reghdfe dispersion pos, a(stkid datestr)
esttab



