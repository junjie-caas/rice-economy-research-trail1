*******************************************************
* 04_regression.do
* 目的：用 Stata 回归分析“规模（种植面积）对流转地租金的影响”
* 模型：reg 流转地租金（元/亩） c.种植面积（亩）, robust
*******************************************************

version 16.0
clear all
set more off

* 项目根目录：当前 do 文件在 do/ 下，故上一级为项目根目录
cd "`c(pwd)'"
local root = subinstr("`c(pwd)'", "/do", "", .)

* 读取清洗数据
import delimited using "`root'/data_clean/survey_clean.csv", clear stringcols(_all) encoding(utf8)

* 将关键变量转为数值
capture confirm numeric variable 种植面积（亩）
if _rc {
    destring 种植面积（亩）, replace force
}

capture confirm numeric variable 流转地租金（元/亩）
if _rc {
    destring 流转地租金（元/亩）, replace force
}

* 删除缺失
drop if missing(种植面积（亩）) | missing(流转地租金（元/亩）)

* 基准回归（稳健标准误）
reg 流转地租金（元/亩） c.种植面积（亩）, vce(robust)

* 导出 Stata 标准回归表（CSV）
matrix b = e(b)
matrix V = e(V)
scalar beta = b[1,1]
scalar alpha = _b[_cons]
scalar se_beta = _se[种植面积（亩）]
scalar se_alpha = _se[_cons]
scalar t_beta = _b[种植面积（亩）] / _se[种植面积（亩）]
scalar t_alpha = _b[_cons] / _se[_cons]
scalar p_beta = 2*ttail(e(df_r),abs(t_beta))
scalar p_alpha = 2*ttail(e(df_r),abs(t_alpha))

clear
set obs 2
gen str32 term = ""
gen coef = .
gen std_err = .
gen t_stat = .
gen p_value = .
gen n_obs = .
gen r2 = .

replace term = "Intercept" in 1
replace coef = alpha in 1
replace std_err = se_alpha in 1
replace t_stat = t_alpha in 1
replace p_value = p_alpha in 1
replace n_obs = e(N) in 1
replace r2 = e(r2) in 1

replace term = "种植面积（亩）" in 2
replace coef = beta in 2
replace std_err = se_beta in 2
replace t_stat = t_beta in 2
replace p_value = p_beta in 2
replace n_obs = e(N) in 2
replace r2 = e(r2) in 2

export delimited using "`root'/output/tables/reg_scale_on_rent_stata.csv", replace

display "[Stata] 回归结果已输出: output/tables/reg_scale_on_rent_stata.csv"
