"""
score_engine.py — Living System Prompt
========================================
Computes MAD-robust bubble scores S_i and PII weights w_i
for all active asset nodes in the vault.

Usage:
    python scripts/score_engine.py
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path

VAULT_ROOT = Path(__file__).parent.parent / "vault"
PII_PATH   = VAULT_ROOT / "system" / "pii-index.json"


def z_robust(series: pd.Series) -> pd.Series:
    """MAD-robust z-score."""
    med = series.median()
    mad = (series - med).abs().median()
    scale = 1.4826 * mad if mad > 0 else 1.0
    return (series - med) / scale


def compute_scores(df: pd.DataFrame) -> pd.Series:
    """
    Compute bubble scores S_i in [0, 100].

    Required columns:
        EVSales, PFCF, AIExposure [0..1], ShortInterest,
        DaysToCover, BorrowFee [0..1 annual], IVSkew
    """
    borrow_penalty = np.clip(df["BorrowFee"] / 0.20, 0, 1)

    raw = (
        0.25 * z_robust(df["EVSales"]) +
        0.20 * z_robust(df["PFCF"]) +
        0.15 * df["AIExposure"] +
        0.10 * z_robust(df["ShortInterest"]) +
        0.10 * z_robust(df["DaysToCover"]) -
        0.10 * borrow_penalty +
        0.10 * df["IVSkew"]
    )
    return 100.0 * (1.0 / (1.0 + np.exp(-raw)))


def compute_weights(scores: pd.Series) -> pd.Series:
    """Normalize scores to PII weights."""
    total = scores.sum()
    if total == 0:
        return pd.Series(0.0, index=scores.index)
    return scores / total


def size_debit_trade(nav: float, max_loss_pct: float, debit_per_contract: float) -> int:
    """Max contracts for a debit spread given max loss per idea."""
    max_loss = nav * max_loss_pct
    return max(0, int(max_loss // debit_per_contract))


def borrow_carry_cost(notional: float, borrow_annual: float, days: int) -> float:
    """Estimated borrow carry cost over `days` days."""
    return notional * borrow_annual * (days / 360.0)


if __name__ == "__main__":
    # Example universe (replace with live data from yfinance/IBKR)
    universe = pd.DataFrame({
        "EVSales":       [18, 10, 6, 8, 7, 15, 5, 4],
        "PFCF":          [120, 55, 25, 35, 30, 90, 20, 18],
        "AIExposure":    [0.6, 0.3, 0.1, 0.4, 0.35, 0.7, 0.3, 0.25],
        "ShortInterest": [0.08, 0.03, 0.02, 0.02, 0.02, 0.06, 0.04, 0.01],
        "DaysToCover":   [7, 2, 1, 2, 1, 5, 3, 1],
        "BorrowFee":     [0.12, 0.03, 0.01, 0.02, 0.02, 0.08, 0.03, 0.005],
        "IVSkew":        [0.06, 0.03, 0.01, 0.02, 0.02, 0.05, 0.04, 0.01],
    }, index=["NVDA", "AMD", "SMCI", "MSFT", "GOOGL", "PLTR", "ARKK", "QQQ"])

    universe["Score"]  = compute_scores(universe)
    universe["Weight"] = compute_weights(universe["Score"])

    print(universe[["Score", "Weight"]].sort_values("Score", ascending=False).round(4))
