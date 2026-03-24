#!/usr/bin/env python3
"""04_regression.py

回归分析：规模（种植面积）对流转地租金的影响。
模型：rent_i = alpha + beta * scale_i + e_i

导出结果：
1) reg_scale_on_rent.csv         - 简明结果
2) reg_scale_on_rent_standard.csv- 标准回归结果格式
3) reg_scale_on_rent.md          - Markdown 表格
4) reg_scale_on_rent.txt         - 文本摘要
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLEAN_FILE = ROOT / "data_clean" / "survey_clean.csv"
OUT_CSV = ROOT / "output" / "tables" / "reg_scale_on_rent.csv"
OUT_STANDARD_CSV = ROOT / "output" / "tables" / "reg_scale_on_rent_standard.csv"
OUT_MD = ROOT / "output" / "tables" / "reg_scale_on_rent.md"
OUT_TXT = ROOT / "output" / "tables" / "reg_scale_on_rent.txt"


def to_float(v: str) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return math.nan


def norm_cdf(x: float) -> float:
    """标准正态分布 CDF（用于大样本近似 p 值）。"""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def stars(p: float) -> str:
    if p < 0.01:
        return "***"
    if p < 0.05:
        return "**"
    if p < 0.1:
        return "*"
    return ""


def ols_with_intercept(x: list[float], y: list[float]) -> dict[str, float]:
    n = len(x)
    if n < 3:
        raise ValueError("有效样本量不足（至少需要 3 条）")

    x_bar = sum(x) / n
    y_bar = sum(y) / n

    sxx = sum((xi - x_bar) ** 2 for xi in x)
    if sxx == 0:
        raise ValueError("自变量（种植面积）无变异，无法回归")

    sxy = sum((xi - x_bar) * (yi - y_bar) for xi, yi in zip(x, y))
    beta = sxy / sxx
    alpha = y_bar - beta * x_bar

    y_hat = [alpha + beta * xi for xi in x]
    resid = [yi - yhi for yi, yhi in zip(y, y_hat)]

    sse = sum(ei**2 for ei in resid)
    tss = sum((yi - y_bar) ** 2 for yi in y)
    r2 = 1 - sse / tss if tss != 0 else 0.0

    sigma2 = sse / (n - 2)
    se_beta = math.sqrt(sigma2 / sxx)
    se_alpha = math.sqrt(sigma2 * (1 / n + (x_bar**2) / sxx))

    t_beta = beta / se_beta if se_beta > 0 else math.nan
    t_alpha = alpha / se_alpha if se_alpha > 0 else math.nan

    # 正态近似双侧 p 值
    p_beta = 2 * (1 - norm_cdf(abs(t_beta))) if not math.isnan(t_beta) else math.nan
    p_alpha = 2 * (1 - norm_cdf(abs(t_alpha))) if not math.isnan(t_alpha) else math.nan

    z = 1.96  # 95% CI 近似
    ci_alpha_l, ci_alpha_u = alpha - z * se_alpha, alpha + z * se_alpha
    ci_beta_l, ci_beta_u = beta - z * se_beta, beta + z * se_beta

    return {
        "n": n,
        "alpha": alpha,
        "beta": beta,
        "se_alpha": se_alpha,
        "se_beta": se_beta,
        "t_alpha": t_alpha,
        "t_beta": t_beta,
        "p_alpha": p_alpha,
        "p_beta": p_beta,
        "ci_alpha_l": ci_alpha_l,
        "ci_alpha_u": ci_alpha_u,
        "ci_beta_l": ci_beta_l,
        "ci_beta_u": ci_beta_u,
        "r2": r2,
    }


def write_outputs(result: dict[str, float]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        fieldnames = ["模型", "样本量N", "截距alpha", "规模系数beta", "SE(alpha)", "SE(beta)", "t(alpha)", "t(beta)", "R2"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(
            {
                "模型": "rent = alpha + beta * scale",
                "样本量N": int(result["n"]),
                "截距alpha": round(result["alpha"], 6),
                "规模系数beta": round(result["beta"], 6),
                "SE(alpha)": round(result["se_alpha"], 6),
                "SE(beta)": round(result["se_beta"], 6),
                "t(alpha)": round(result["t_alpha"], 6),
                "t(beta)": round(result["t_beta"], 6),
                "R2": round(result["r2"], 6),
            }
        )

    with OUT_STANDARD_CSV.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "model",
            "term",
            "coef",
            "std_err",
            "t_stat",
            "p_value",
            "ci_95_lower",
            "ci_95_upper",
            "signif",
            "n_obs",
            "r2",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        writer.writerow(
            {
                "model": "rent_on_scale_ols",
                "term": "Intercept",
                "coef": f"{result['alpha']:.6f}",
                "std_err": f"{result['se_alpha']:.6f}",
                "t_stat": f"{result['t_alpha']:.6f}",
                "p_value": f"{result['p_alpha']:.6f}",
                "ci_95_lower": f"{result['ci_alpha_l']:.6f}",
                "ci_95_upper": f"{result['ci_alpha_u']:.6f}",
                "signif": stars(result["p_alpha"]),
                "n_obs": int(result["n"]),
                "r2": f"{result['r2']:.6f}",
            }
        )
        writer.writerow(
            {
                "model": "rent_on_scale_ols",
                "term": "种植面积（亩）",
                "coef": f"{result['beta']:.6f}",
                "std_err": f"{result['se_beta']:.6f}",
                "t_stat": f"{result['t_beta']:.6f}",
                "p_value": f"{result['p_beta']:.6f}",
                "ci_95_lower": f"{result['ci_beta_l']:.6f}",
                "ci_95_upper": f"{result['ci_beta_u']:.6f}",
                "signif": stars(result["p_beta"]),
                "n_obs": int(result["n"]),
                "r2": f"{result['r2']:.6f}",
            }
        )

    md = (
        "| term | coef | std_err | t_stat | p_value | ci_95_lower | ci_95_upper | signif |\n"
        "|---|---:|---:|---:|---:|---:|---:|:---:|\n"
        f"| Intercept | {result['alpha']:.6f} | {result['se_alpha']:.6f} | {result['t_alpha']:.6f} | {result['p_alpha']:.6f} | {result['ci_alpha_l']:.6f} | {result['ci_alpha_u']:.6f} | {stars(result['p_alpha'])} |\n"
        f"| 种植面积（亩） | {result['beta']:.6f} | {result['se_beta']:.6f} | {result['t_beta']:.6f} | {result['p_beta']:.6f} | {result['ci_beta_l']:.6f} | {result['ci_beta_u']:.6f} | {stars(result['p_beta'])} |\n\n"
        f"- N = {int(result['n'])}\n"
        f"- R2 = {result['r2']:.6f}\n"
    )
    OUT_MD.write_text(md, encoding="utf-8")

    summary = (
        "回归模型: rent = alpha + beta * scale\n"
        f"N = {int(result['n'])}\n"
        f"alpha = {result['alpha']:.6f} (SE={result['se_alpha']:.6f}, t={result['t_alpha']:.6f}, p={result['p_alpha']:.6f})\n"
        f"beta  = {result['beta']:.6f} (SE={result['se_beta']:.6f}, t={result['t_beta']:.6f}, p={result['p_beta']:.6f})\n"
        f"95% CI(beta) = [{result['ci_beta_l']:.6f}, {result['ci_beta_u']:.6f}]\n"
        f"R2 = {result['r2']:.6f}\n"
        "注：p 值与置信区间基于正态近似。\n"
    )
    OUT_TXT.write_text(summary, encoding="utf-8")


def main() -> None:
    if not CLEAN_FILE.exists():
        print(f"[04_regression] 未找到清洗数据: {CLEAN_FILE}")
        print("[04_regression] 请先运行 do/01_clean.py")
        return

    x, y = [], []
    with CLEAN_FILE.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            scale = to_float(row.get("种植面积（亩）", ""))
            rent = to_float(row.get("流转地租金（元/亩）", ""))
            if math.isnan(scale) or math.isnan(rent):
                continue
            x.append(scale)
            y.append(rent)

    if not x:
        print("[04_regression] 没有可用样本（种植面积/租金字段缺失或不可解析）。")
        return

    result = ols_with_intercept(x, y)
    write_outputs(result)

    print(f"[04_regression] 回归结果已输出: {OUT_CSV}")
    print(f"[04_regression] 标准格式结果已输出: {OUT_STANDARD_CSV}")
    print(f"[04_regression] Markdown 表格已输出: {OUT_MD}")
    print(f"[04_regression] 回归摘要已输出: {OUT_TXT}")


if __name__ == "__main__":
    main()
