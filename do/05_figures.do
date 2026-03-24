*******************************************************
* 05_figures.do
* 目的：用 Stata 绘制“种植面积与流转地租金关系图”
*******************************************************

version 16.0
clear all
set more off

cd "`c(pwd)'"
local root = subinstr("`c(pwd)'", "/do", "", .)

import delimited using "`root'/data_clean/survey_clean.csv", clear stringcols(_all) encoding(utf8)

capture confirm numeric variable 种植面积（亩）
if _rc {
    destring 种植面积（亩）, replace force
}

capture confirm numeric variable 流转地租金（元/亩）
if _rc {
    destring 流转地租金（元/亩）, replace force
}

drop if missing(种植面积（亩）) | missing(流转地租金（元/亩）)

* 散点 + 拟合线
twoway \
    (scatter 流转地租金（元/亩） 种植面积（亩）, msize(vsmall) mcolor(navy%45)) \
    (lfit 流转地租金（元/亩） 种植面积（亩）, lcolor(maroon) lwidth(medthick)), \
    title("规模与流转租金关系") \
    ytitle("流转地租金（元/亩）") \
    xtitle("种植面积（亩）") \
    legend(order(1 "样本点" 2 "线性拟合"))

graph export "`root'/output/figures/rent_vs_scale_stata.png", replace width(1600)

display "[Stata] 图形已输出: output/figures/rent_vs_scale_stata.png"
