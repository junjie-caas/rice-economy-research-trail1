#!/usr/bin/env python3
"""01_clean.py

从 data_raw/ 读取原始问卷数据，完成基础清洗后输出到 data_clean/。
当前版本提供一个可运行模板：
- 若不存在原始文件，则提示用户放置文件后再运行；
- 若存在原始文件，则执行列名标准化和关键字段完整性检查。
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data_raw" / "raw_survey.csv"
CLEAN_FILE = ROOT / "data_clean" / "survey_clean.csv"

REQUIRED_COLUMNS = [
    "排序",
    "问卷序号",
    "年份",
    "调查年份",
    "水稻类别",
    "省级编码",
    "地市级编码",
    "县级编码",
    "农户id",
    "填表日期",
    "种植面积（亩）",
    "流转面积（亩）",
    "流转地租金（元/亩）",
    "最大品种名称",
]


def main() -> None:
    if not RAW_FILE.exists():
        print(f"[01_clean] 未找到原始数据文件: {RAW_FILE}")
        print("[01_clean] 请将原始数据命名为 raw_survey.csv 并放入 data_raw/ 后重试。")
        return

    with RAW_FILE.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        input_columns = reader.fieldnames or []

        missing = [col for col in REQUIRED_COLUMNS if col not in input_columns]
        if missing:
            raise ValueError(f"原始数据缺少必要字段: {missing}")

        rows = list(reader)

    # 基础清洗：去掉两端空格
    cleaned_rows = []
    for row in rows:
        cleaned_row = {k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
        cleaned_rows.append(cleaned_row)

    CLEAN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with CLEAN_FILE.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=input_columns)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    print(f"[01_clean] 清洗完成，输出文件: {CLEAN_FILE}")
    print(f"[01_clean] 样本量: {len(cleaned_rows)}")


if __name__ == "__main__":
    main()
