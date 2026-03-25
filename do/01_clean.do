*******************************************************
* File: do/01_clean.do
* Purpose: 清洗原始问卷数据并生成分析样本
*******************************************************

version 16.0
clear all
set more off

*------------------------------------------------------
* 0) 项目路径
*------------------------------------------------------
local root `"`c(pwd)'"'
local raw_xlsx  `"`root'/data_raw/survey_raw.xlsx"'
local out_dta   `"`root'/data_clean/survey_clean.dta"'
local out_csv   `"`root'/data_clean/survey_clean.csv"'

capture mkdir `"`root'/data_clean"'
capture mkdir `"`root'/output"'
capture mkdir `"`root'/output/tables"'
capture mkdir `"`root'/output/figures"'

*------------------------------------------------------
* 1) 从 Excel 读取：默认第1行为中文标签，第2行为变量名
*------------------------------------------------------
capture confirm file `"`raw_xlsx'"'
if _rc {
    di as error "未找到原始数据文件: `raw_xlsx'"
    exit 601
}

import excel using `"`raw_xlsx'"', sheet("Sheet1") allstring clear

*------------------------------------------------------
* 2) 变量名标准化：取第2行作为变量名、第1行作为变量标签
*------------------------------------------------------
ds
local oldvars `r(varlist)'
local usednames

foreach v of local oldvars {
    quietly levelsof `v' in 1, local(vlabel)
    quietly levelsof `v' in 2, local(vname_raw)

    local vname = lower(strtoname("`vname_raw'"))

    if `"`vname'"' == "" {
        local vname = "`v'"
    }

    local base "`vname'"
    local i = 1
    while strpos(" `usednames' ", " `vname' ") > 0 {
        local vname = "`base'_`i'"
        local ++i
    }

    local usednames `usednames' `vname'

    rename `v' `vname'
    label variable `vname' `"`vlabel'"'
}

*------------------------------------------------------
* 检查变量名标准化
ds var1
if r(varlist) != "" {
    di as error "变量名未标准化，请先运行变量名标准化部分！"
    exit 602
}
*------------------------------------------------------

* 删除前两行（标签行+变量名行）
drop in 1/2

*------------------------------------------------------
* 3) 基础清洗
*------------------------------------------------------
* 先标准化字符串取值：按评审意见将“无”编码为0
quietly foreach v of varlist _all {
    capture confirm string variable `v'
    if !_rc replace `v' = "0" if trim(`v') == "无"
}

* 将全表可转数值字段转为数值型；忽略空格和千分位逗号
destring _all, replace ignore(" ,")

* 统一常见缺失值编码（字符串残留时）
foreach miss in "NA" "N/A" "." "-" "--" "未知" {
    quietly foreach v of varlist _all {
        capture confirm string variable `v'
        if !_rc replace `v' = "" if trim(upper(`v')) == trim(upper("`miss'"))
    }
}

*------------------------------------------------------
* 4) 派生变量（若基础字段存在则生成）
*------------------------------------------------------
capture confirm variable year
if !_rc {
    gen byte post_2018 = year >= 2018 if !missing(year)
    label var post_2018 "是否2018年及以后"
}

capture confirm variable rice_type
if !_rc {
    label define rice_lbl 1 "早籼稻" 2 "中籼稻" 3 "晚籼稻" 4 "粳稻", replace
    capture label values rice_type rice_lbl
}

*------------------------------------------------------
* 5) 保存清洗数据
*------------------------------------------------------
order _all
compress

save `"`out_dta'"', replace
export delimited using `"`out_csv'"', replace

di as result "数据清洗完成。"
di as result "DTA: `out_dta'"
di as result "CSV: `out_csv'"
