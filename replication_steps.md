# 复现步骤（Replication Steps）

## 1. 准备环境

- 克隆仓库
- 安装分析所需软件（例如 Python/R/Stata）
- 确认目录结构完整

## 2. 放置原始数据

- 将原始数据文件放入 `data_raw/`
- 原始数据保持不变，不在原文件上做覆盖修改

## 3. 数据清洗

- 运行 `python do/01_clean.py`
- 输出清洗数据到 `data_clean/survey_clean.csv`

## 4. 实证分析

- 运行 `python do/02_analysis.py`
- 输出统计表到 `output/tables/summary_by_rice_type.csv`

## 5. 绘图与可视化

- 运行 `python do/03_figures.py`
- 输出图片到 `output/figures/avg_area_by_rice_type.svg`


## 6. 回归分析：规模对流转租金的影响

- 运行 `python do/04_regression.py` 或 `bash do/run_regression.sh`
- 输出回归结果到 `output/tables/reg_scale_on_rent.csv`
- 输出标准格式结果到 `output/tables/reg_scale_on_rent_standard.csv`
- 输出 Markdown 回归表到 `output/tables/reg_scale_on_rent.md`
- 输出回归摘要到 `output/tables/reg_scale_on_rent.txt`

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
