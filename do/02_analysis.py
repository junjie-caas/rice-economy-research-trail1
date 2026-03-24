#!/usr/bin/env python3
"""02_analysis.py

读取清洗后的数据并输出一个基础描述统计表（按水稻类别分组）。
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLEAN_FILE = ROOT / "data_clean" / "survey_clean.csv"
TABLE_FILE = ROOT / "output" / "tables" / "summary_by_rice_type.csv"

RICE_TYPE_LABELS = {
    "1": "早籼稻",
    "2": "中籼稻",
    "3": "晚籼稻",
    "4": "粳稻",
}


def to_float(v: str) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def main() -> None:
    if not CLEAN_FILE.exists():
        print(f"[02_analysis] 未找到清洗数据: {CLEAN_FILE}")
        print("[02_analysis] 请先运行 do/01_clean.py")
        return

    group = defaultdict(lambda: {"n": 0, "area": 0.0, "rent": 0.0})

    with CLEAN_FILE.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rice_type = str(row.get("水稻类别", "")).strip()
            group[rice_type]["n"] += 1
            group[rice_type]["area"] += to_float(row.get("种植面积（亩）", "0"))
            group[rice_type]["rent"] += to_float(row.get("流转地租金（元/亩）", "0"))

    TABLE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with TABLE_FILE.open("w", encoding="utf-8", newline="") as f:
        fieldnames = ["水稻类别编码", "水稻类别", "样本数", "平均种植面积（亩）", "平均流转地租金（元/亩）"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for rice_type in sorted(group.keys()):
            n = group[rice_type]["n"]
            avg_area = group[rice_type]["area"] / n if n else 0.0
            avg_rent = group[rice_type]["rent"] / n if n else 0.0
            writer.writerow(
                {
                    "水稻类别编码": rice_type,
                    "水稻类别": RICE_TYPE_LABELS.get(rice_type, "未知"),
                    "样本数": n,
                    "平均种植面积（亩）": round(avg_area, 2),
                    "平均流转地租金（元/亩）": round(avg_rent, 2),
                }
            )

    print(f"[02_analysis] 描述统计已输出: {TABLE_FILE}")


if __name__ == "__main__":
    main()
