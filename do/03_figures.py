#!/usr/bin/env python3
"""03_figures.py

基于统计表生成一个轻量 SVG 柱状图（不依赖第三方库）。
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE_FILE = ROOT / "output" / "tables" / "summary_by_rice_type.csv"
FIG_FILE = ROOT / "output" / "figures" / "avg_area_by_rice_type.svg"


def main() -> None:
    if not TABLE_FILE.exists():
        print(f"[03_figures] 未找到统计表: {TABLE_FILE}")
        print("[03_figures] 请先运行 do/02_analysis.py")
        return

    data = []
    with TABLE_FILE.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            label = row.get("水稻类别", "未知")
            value = float(row.get("平均种植面积（亩）", "0") or 0)
            data.append((label, value))

    if not data:
        print("[03_figures] 统计表为空，未生成图形。")
        return

    width = 720
    height = 420
    margin = 50
    plot_width = width - 2 * margin
    plot_height = height - 2 * margin
    max_value = max(v for _, v in data) or 1.0
    bar_width = plot_width // max(len(data), 1) - 20

    rects = []
    labels = []
    for i, (label, value) in enumerate(data):
        x = margin + i * (bar_width + 20) + 10
        bar_h = int((value / max_value) * (plot_height - 30))
        y = height - margin - bar_h
        rects.append(f'<rect x="{x}" y="{y}" width="{bar_width}" height="{bar_h}" fill="#4e79a7" />')
        labels.append(f'<text x="{x + bar_width / 2}" y="{height - margin + 20}" text-anchor="middle" font-size="12">{label}</text>')
        labels.append(f'<text x="{x + bar_width / 2}" y="{y - 8}" text-anchor="middle" font-size="11">{value:.2f}</text>')

    svg = f"""<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{width}\" height=\"{height}\"> 
  <rect width=\"100%\" height=\"100%\" fill=\"white\" />
  <text x=\"{width/2}\" y=\"30\" text-anchor=\"middle\" font-size=\"18\">各水稻类别平均种植面积（亩）</text>
  <line x1=\"{margin}\" y1=\"{height-margin}\" x2=\"{width-margin}\" y2=\"{height-margin}\" stroke=\"black\" />
  <line x1=\"{margin}\" y1=\"{margin}\" x2=\"{margin}\" y2=\"{height-margin}\" stroke=\"black\" />
  {''.join(rects)}
  {''.join(labels)}
</svg>
"""

    FIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    FIG_FILE.write_text(svg, encoding="utf-8")
    print(f"[03_figures] 图形已输出: {FIG_FILE}")


if __name__ == "__main__":
    main()
