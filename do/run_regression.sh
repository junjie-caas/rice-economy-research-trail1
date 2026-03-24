#!/usr/bin/env bash
set -euo pipefail

python do/01_clean.py
python do/04_regression.py

echo "[run_regression] 完成：已执行清洗与回归，并导出标准格式结果。"
