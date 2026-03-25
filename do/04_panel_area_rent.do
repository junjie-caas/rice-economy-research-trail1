clear all
set more off

* 根目录
global ROOT "D:\#AGENT\rice-economy-trial1"
cd "$ROOT"

* 面板回归：rent 对 area
* 用法（命令行）：
* stata -b do do/04_panel_area_rent.do
*
* 期望输入：$ROOT\data_clean\rent_raw.dta
* 核心变量：id year area rent

capture log close
cap mkdir output
cap mkdir output/tables
cap mkdir data_clean
log using "$ROOT\output\tables\panel_area_rent.log", replace text

* 若未安装 esttab/outreg2，自动尝试安装
capture which esttab
if _rc ssc install estout, replace
capture which outreg2
if _rc ssc install outreg2, replace

use "$ROOT\data_clean\rent_raw.dta", clear

* 地区控制变量：按 county_id > city_id > province_id 优先级自动选择
local region_var ""
foreach v in county_id city_id province_id {
    capture confirm variable `v'
    if !_rc {
        local region_var "`v'"
        continue, break
    }
}

if "`region_var'" != "" {
    di as txt "[INFO] 使用地区控制变量: `region_var'"
    local region_fe "i.`region_var'"
}
else {
    di as txt "[INFO] 未找到地区变量（province_id/city_id/county_id），回归不含地区控制。"
    local region_fe ""
}

* 仅保留核心变量并处理缺失
local keepvars "id year area rent"
if "`region_var'" != "" local keepvars "`keepvars' `region_var'"
keep `keepvars'
drop if missing(id) | missing(year) | missing(area) | missing(rent)
if "`region_var'" != "" drop if missing(`region_var')

* 检查并设置面板
isid id year, sort
xtset id year

* 描述统计
summarize rent area

* 1) pooled OLS（聚类稳健标准误）
reg rent area i.year `region_fe', vce(cluster id)
estimates store pooled

* 2) 个体固定效应 + 年份固定效应
xtreg rent area i.year `region_fe', fe vce(cluster id)
estimates store fe

* 3) 随机效应 + 年份效应（用于对照）
xtreg rent area i.year `region_fe', re vce(cluster id)
estimates store re

* Hausman 检验（FE vs RE，检验系统方差设定）
quietly xtreg rent area i.year `region_fe', fe
estimates store fe_h
quietly xtreg rent area i.year `region_fe', re
estimates store re_h
hausman fe_h re_h, sigmamore

* 屏幕展示对比表
estimates table pooled fe re, b(%9.4f) se(%9.4f) stats(N r2 r2_w, labels("N" "R2" "R2_within")) star(.1 .05 .01)

* 导出 esttab（CSV + Word/RTF）
capture noisily esttab pooled fe re using "$ROOT\output\tables\panel_area_rent_esttab.csv", ///
    replace se star(* 0.10 ** 0.05 *** 0.01) ///
    stats(N r2 r2_w, labels("N" "R2" "R2_within")) nonotes

capture noisily esttab pooled fe re using "$ROOT\output\tables\panel_area_rent_esttab.rtf", ///
    replace se star(* 0.10 ** 0.05 *** 0.01) ///
    stats(N r2 r2_w, labels("N" "R2" "R2_within")) nonotes

* 导出 outreg2（Word）
reg rent area i.year `region_fe', vce(cluster id)
outreg2 using "$ROOT\output\tables\panel_area_rent_outreg2.doc", replace word ctitle("Pooled OLS")

xtreg rent area i.year `region_fe', fe vce(cluster id)
outreg2 using "$ROOT\output\tables\panel_area_rent_outreg2.doc", append word ctitle("FE")

xtreg rent area i.year `region_fe', re vce(cluster id)
outreg2 using "$ROOT\output\tables\panel_area_rent_outreg2.doc", append word ctitle("RE")

* 保存回归样本（便于复核）
save "$ROOT\data_clean\rent_panel_used.dta", replace

log close
