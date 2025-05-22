import argparse
import csv
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def _is_win(row: pd.Series, model: str) -> bool:
    if row["human_LLM"] == model and row["winner"] == "Human":
        return True
    if row["demon_LLM"] == model and row["winner"] == "Demon":
        return True
    return False

def _cost(row: pd.Series, role: str) -> int:
    return row["human_cost"] if role == "human" else row["demon_cost"]



def compute_metrics(
    df: pd.DataFrame,
    model: str,
    role: str,
    human_budget: int,
    demon_budget: int,
) -> Dict[str, float]:
    """Return five metrics for given (model, role) DataFrame."""
    n = len(df)
    if n == 0:
        return {
            "win_rate": 0.0,
            "correction_rate": 0.0,
            "correction_success_rate": 0.0,
            "improvement_slope": 0.0,
            "over_budget_ratio": 0.0,
        }

    # 1. Win rate
    win_rate = df.apply(lambda r: _is_win(r, model), axis=1).mean()

    # 2. Over-budget ratio
    budget = human_budget if role == "human" else demon_budget
    over_budget_ratio = df.apply(lambda r: _cost(r, role) > budget, axis=1).mean()

    # 3. Correction rate
    costs = df.apply(lambda r: _cost(r, role), axis=1).to_numpy()
    idx = np.arange(0 if role == "human" else 1, n, 2)
    corr = np.count_nonzero(np.diff(costs[idx]) != 0)
    turns = len(idx) - 1
    correction_rate = corr / turns if turns > 0 else 0.0

    # 4. Correction success
    success = 0
    for i in idx[:-1]:
        if costs[i + 2] != costs[i]:
            if not _is_win(df.iloc[i], model) and _is_win(df.iloc[i + 1], model):
                success += 1
    correction_success_rate = success / corr if corr > 0 else 0.0

    # 5. Improvement slope
    indicator = df.apply(lambda r: 1 if _is_win(r, model) else 0, axis=1).to_numpy()
    if n > 1:
        X = np.arange(n).reshape(-1, 1)
        slope = float(LinearRegression().fit(X, indicator).coef_[0])
    else:
        slope = 0.0

    return {
        "win_rate": win_rate,
        "correction_rate": correction_rate,
        "correction_success_rate": correction_success_rate,
        "improvement_slope": slope,
        "over_budget_ratio": over_budget_ratio,
    }

# -----------------------------------------------------------------------------  
# CSV discovery ---------------------------------------------------------------  

def collect_csvs(root: Path) -> List[Tuple[str, str, Path]]:

    items: List[Tuple[str, str, Path]] = []
    for role_dir in (root / "human_results", root / "demon_results"):
        if not role_dir.exists():
            continue
        role = "human" if "human" in role_dir.name else "demon"
        for tag in ("first", "second"):
            tag_dir = role_dir / tag
            if not tag_dir.is_dir():
                continue
            for csv_file in tag_dir.glob("*.csv"):
                stem = csv_file.stem
                if stem.endswith("_results"):
                    model_slug = stem[: -len("_results")]
                else:
                    model_slug = stem
                model = model_slug.replace("-", "/")
                items.append((model, role, csv_file))
    return items

# -----------------------------------------------------------------------------  
# main ------------------------------------------------------------------------  

def main() -> None:
    script_dir = Path(__file__).parent

    parser = argparse.ArgumentParser(description="Aggregate per-model metrics for one game.")
    parser.add_argument(
        "--results-root",
        type=Path,
        default=script_dir,
        help="Directory containing human_results/ and demon_results/ (default: script dir)",
    )
    parser.add_argument("--human-budget", type=int, default=20)
    parser.add_argument("--demon-budget", type=int, default=20)
    parser.add_argument(
        "--out-file",
        type=Path,
        default=script_dir / "model_metrics.csv",
        help="Output summary CSV path",
    )
    args = parser.parse_args()

    rows = []
    for model, role, csv_path in collect_csvs(args.results_root):
        df = pd.read_csv(csv_path)
        metrics = compute_metrics(df, model, role, 2000, 1500)
        metrics["model"] = model
        rows.append(metrics)

    if not rows:
        print("[WARN] No CSV files found under", args.results_root)
        sys.exit(0)

    # 不再按 role 分组，仅按 model 计算平均
    df_out = pd.DataFrame(rows).groupby("model", as_index=False).mean(numeric_only=True)
    df_out.to_csv(args.out_file, index=False, quoting=csv.QUOTE_NONNUMERIC)
    print(f"[✓] Metrics saved to {args.out_file}")

if __name__ == "__main__":
    main()