from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Summarize multi-seed redocking reproducibility results.")
    p.add_argument("csv", type=Path)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.csv)

    mean_score = df["best_vina_score_kcal_mol"].mean()
    mean_rmsd = df["top_pose_rmsd_A"].mean()
    success = (df["top_pose_rmsd_A"] <= 2.0).sum()

    print(f"Runs: {len(df)}")
    print(f"Mean best Vina score: {mean_score:.3f} kcal/mol")
    print(f"Mean top-pose RMSD: {mean_rmsd:.3f} Å")
    print(f"Top-pose RMSD <= 2 Å: {success}/{len(df)}")


if __name__ == "__main__":
    main()
