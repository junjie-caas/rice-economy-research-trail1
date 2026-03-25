# 复现步骤（Replication Steps）

## 1. 准备环境

- 根目录：`D:\#AGENT\rice-economy-trial1`
- 克隆仓库
- 安装分析所需软件（例如 Python/R/Stata）
- 确认目录结构完整

## 2. 放置原始数据

- 将原始数据文件放入 `data_raw/`
- 原始数据保持不变，不在原文件上做覆盖修改

## 3. 数据清洗

- 运行 `python do/01_clean.py`
- 输出清洗数据到 `data_clean/survey_clean.csv`

## 3.1 品种字段标准化

- 运行 `python do/01_clean_ricevariety.py --input data_raw/survey_raw.csv --output data_clean/survey_ricevariety_clean.csv`
- 产出 `ricevariety_std`（标准品种）、`rice_type_group`（类别分组）、`ricevariety_multi_flag`（多品种混填标记）

## 4. 实证分析

- 运行 `python do/02_analysis.py`
- 输出统计表到 `output/tables/summary_by_rice_type.csv`

## 5. 绘图与可视化

- 运行 `python do/03_figures.py`
- 输出图片到 `output/figures/avg_area_by_rice_type.svg`


## 6. 回归分析：`area` 对 `rent` 的面板影响（Stata）

- 将源数据放置为 `D:\#AGENT\rice-economy-trial1\data_clean\rent_raw.dta`（包含 `id year area rent`）
- 运行 `stata -b do do/04_panel_area_rent.do`
- 脚本会执行：
  - pooled OLS：`reg rent area i.year, vce(cluster id)`
  - 固定效应：`xtreg rent area i.year, fe vce(cluster id)`
  - 随机效应：`xtreg rent area i.year, re vce(cluster id)`
  - Hausman 检验：比较 FE 与 RE
  - 地区控制：自动选择 `county_id` / `city_id` / `province_id` 中可用变量并加入回归
- 输出日志：`output/tables/panel_area_rent.log`
- 输出 esttab 表：`output/tables/panel_area_rent_esttab.csv`、`output/tables/panel_area_rent_esttab.rtf`
- 输出 outreg2 Word 表：`output/tables/panel_area_rent_outreg2.doc`
- 输出回归样本：`data_clean/rent_panel_used.dta`

## 7. 归档与检查

- 核对表格和图形是否可由脚本一键再生
- 记录软件版本与随机种子（如适用）

## 8. 本项目建议使用的数据字段

| 字段名 | 说明 |
|---|---|
| 排序 | 记录顺序编号 |
| 问卷序号 | 问卷唯一序号 |
| 年份 | 生产年份/统计年份 |
| 调查年份 | 进行调查的年份 |
| 水稻类别 | 1=早籼稻；2=中籼稻；3=晚籼稻；4=粳稻 |
| 省级编码 | 省级行政区代码 |
| 地市级编码 | 地市行政区代码 |
| 县级编码 | 县级行政区代码 |
| 农户id | 农户唯一标识 |
| 填表日期 | 问卷填报日期 |
| 种植面积（亩） | 水稻种植面积 |
| 流转面积（亩） | 土地流转面积 |
| 流转地租金（元/亩） | 土地流转租金水平 |
| 最大品种名称 | 种植面积最大的品种 |
