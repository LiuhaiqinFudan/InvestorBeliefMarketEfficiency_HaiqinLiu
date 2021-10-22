************************************************************************
*********** train CNN/LSTM 之前先对所有remarks数据进行清洗 *************
************************************************************************
clear all 
global root = "D:\Course2021Autumn\MachineLearningFintech\project"
cd "$root"

import excel using CleanData\allComments.xlsx, firstrow clear 
duplicates drop 
drop if time == "time"  // 重复写入的表头
replace time = time[_n-1] if time == ""   // 尽量保证第一条time不要漏爬;这种填充存在一定问题(如两股交界处),但按照爬取顺序,1-2条问题不大

gen blankpos = strrpos(time, " ")
gen datestr = substr(time, 1, blankpos - 1)
drop blankpos
drop if remark == ""
drop if remark == "[图片]"
drop if ustrregexm(remark, "^[0-9]+$")  // 仅包含数字

gen unit = strpos(reading, "万")
replace reading = subinstr(reading,"万","",.)
destring reading, force replace  
replace reading = reading * 1e4 if unit 
drop unit 
destring, replace

gen slash1 = strpos(datestr, "/")
gen slash2 = strrpos(datestr, "/")
gen year = substr(datestr, slash2+1, .)
gen month = substr(datestr, 1, slash1-1)
gen day = substr(datestr, slash1+1, slash2-slash1-1)
drop slash* 
gen date = year + "/" + month + "/" + day 
drop year month day datestr 
replace date = subinstr(date, " ", "", .)

export excel using CleanData\allComments-cleaned.xlsx, firstrow(variables) replace
* 然后wind提取公式，保存无公式版本到allComments-wind.xlsx