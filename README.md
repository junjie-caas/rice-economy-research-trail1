# 水稻经济项目（Rice Economy Research）

本仓库提供一个简洁、可复现的水稻经济研究项目结构，便于后续开展数据清洗、描述统计、计量分析和结果输出。

## 项目目录结构

```text
data_raw/           # 原始数据（只读，不直接改）
data_clean/         # 清洗后的分析数据
do/                 # 脚本（清洗、分析、制图）
output/tables/      # 回归表、描述统计表等
output/figures/     # 图形结果
README.md           # 项目说明
replication_steps.md# 复现实验步骤
```

## 核心数据指标（建议字段）

- 排序
- 问卷序号
- 年份
- 调查年份
- 水稻类别（1=早籼稻；2=中籼稻；3=晚籼稻；4=粳稻）
- 省级编码
- 地市级编码
- 县级编码
- 农户id
- 填表日期
- 种植面积（亩）
- 流转面积（亩）
- 流转地租金（元/亩）
- 最大品种名称

## 推荐做法

1. 将原始问卷或行政数据放入 `data_raw/`。
2. 在 `do/` 中运行已提供的 `01_clean.py`、`02_analysis.py`、`03_figures.py` 脚本（可按需扩展）。
3. 将清洗后的主分析数据输出到 `data_clean/`。
4. 将表格与图形分别输出到 `output/tables/` 与 `output/figures/`。
5. 在 `replication_steps.md` 中记录可复现步骤与软件环境。


## 快速运行

```bash
python do/01_clean.py
python do/02_analysis.py
python do/03_figures.py
```
