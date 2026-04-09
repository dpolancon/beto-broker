"""
rebalance_engine.py — Living System Prompt
===========================================
Checks each active asset node against its asset-specific δ threshold.
When a score move exceeds δ_i, pushes a rebalance suggestion to the stack.
Updates pii-index.json with new weights after user approval (via stack_manager).

Usage:
    python scripts/rebalance_engine.py

Triggered by:
    - vault_watcher.py on asset node save (score change detected)
    - Scheduled run (e.g. daily via VS Code task)
    - Manual run from terminal
"""

import json
import numpy as np
from pathlib import Path
from datetime import datetime

VAULT_ROOT  = Path(__file__).parent.parent / "vault"
PII_PATH    = VAULT_ROOT / "system" / "pii-index.json"
STACK_PATH  = VAULT_ROOT / "system" / "stack.json"
ASSETS_PATH = VAULT_ROOT / "examples" / "ai-bubble-short" / "assets"
MY_ASSETS   = VAULT_ROOT / "my-priors"


# ── Helpers ──────────────────────────────────────────────────────────────────

def load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)

def save_json(path: Path, data: dict):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)


def load_active_assets(assets_dir: Path) -> dict:
    """
    Read all .json companion files in an assets directory.
    Returns {ticker: frontmatter_dict} for status==active assets.
    vault_watcher.py keeps .json files in sync with .md frontmatter.
    """
    assets = {}
    for p in assets_dir.glob("*.json"):
        data = load_json(p)
        if data.get("status") == "active" and data.get("node_type") == "asset":
            ticker = data.get("asset", p.stem)
            assets[ticker] = data
    return assets


def compute_weights(assets: dict) -> dict:
    """
    w_i = S_i / Σ_j S_j
    Returns {ticker: weight}
    """
    total = sum(a.get("score", 0) for a in assets.values())
    if total == 0:
        return {t: 0.0 for t in assets}
    return {t: round(a.get("score", 0) / total, 6) for t, a in assets.items()}


def compute_delta_index_variance(
    asset: str,
    delta_score: float,
    assets: dict,
    sigma_total: float = 500.0
) -> float:
    """
    ΔVar ≈ κ_i × δ_i
    κ_i stored in asset node frontmatter.
    Returns estimated change in index variance.
    """
    kappa = assets[asset].get("kappa", 0.0)
    return round(abs(kappa * delta_score), 8)


# ── Core rebalance check ──────────────────────────────────────────────────────

def check_rebalance(assets: dict, pii: dict) -> list:
    """
    Compare current scores vs last recorded scores in pii-index.json.
    Returns list of assets that exceed their δ threshold.
    """
    triggers = []
    recorded = pii.get("assets", {})

    for ticker, data in assets.items():
        current_score  = data.get("score", 0)
        previous_score = recorded.get(ticker, {}).get("score", current_score)
        delta          = abs(current_score - previous_score)
        threshold      = data.get("delta_threshold", 5)

        if delta >= threshold:
            triggers.append({
                "asset":         ticker,
                "score_before":  previous_score,
                "score_after":   current_score,
                "delta_score":   round(current_score - previous_score, 4),
                "threshold":     threshold,
            })

    return triggers


def push_rebalance_to_stack(trigger: dict, assets: dict, new_weights: dict, library_source: str = "rebalance_engine"):
    """Push a rebalance suggestion to vault/system/stack.json."""
    import uuid
    stack = load_json(STACK_PATH)

    delta_var = compute_delta_index_variance(
        trigger["asset"],
        abs(trigger["delta_score"]),
        assets
    )

    item_id = f"obs-{datetime.now().strftime('%Y-%m-%d')}-{str(uuid.uuid4())[:6]}"
    item = {
        "id":                    item_id,
        "timestamp":             datetime.now().isoformat(),
        "type":                  "score_update",
        "asset":                 trigger["asset"],
        "score_before":          trigger["score_before"],
        "score_after":           trigger["score_after"],
        "delta_score":           trigger["delta_score"],
        "delta_weight":          round(
            new_weights.get(trigger["asset"], 0) -
            assets[trigger["asset"]].get("weight", 0), 6
        ),
        "delta_index_variance":  delta_var,
        "exceeds_threshold":     True,
        "threshold":             trigger["threshold"],
        "library_source":        library_source,
        "rebalance_recommended": True,
        "awaiting_user_approval": True,
        "user_note":             None,
    }

    stack["stack"].append(item)
    stack["stack_size"] = len(stack["stack"])
    stack["last_updated"] = datetime.now().isoformat()
    save_json(STACK_PATH, stack)

    print(f"[rebalance] pushed to stack: {trigger['asset']} "
          f"Δscore={trigger['delta_score']:+.2f} "
          f"ΔVar={delta_var:.8f} "
          f"(threshold={trigger['threshold']})")

    if stack["stack_size"] >= 50:
        print(f"[rebalance] ⚠️  Stack has {stack['stack_size']} items — consider a review session.")


def update_pii_weights(assets: dict, new_weights: dict):
    """
    Write updated scores and weights to pii-index.json assets field.
    Called AFTER user commits a rebalance from the stack — not before.
    """
    pii = load_json(PII_PATH)
    pii["universe"] = list(assets.keys())
    pii["assets"] = {
        ticker: {
            "score":            data.get("score", 0),
            "weight":           new_weights.get(ticker, 0),
            "delta_threshold":  data.get("delta_threshold", 5),
            "kappa":            data.get("kappa", 0.0),
            "mcv":              data.get("mcv", 0.0),
            "sigma_annualized": data.get("sigma_annualized", 0.0),
            "last_score_update": datetime.now().isoformat(),
            "status":           data.get("status", "active"),
        }
        for ticker, data in assets.items()
    }
    pii["last_rebalance"] = datetime.now().isoformat()
    pii["rebalance_count"] = pii.get("rebalance_count", 0) + 1
    pii["initialized"] = True
    if pii.get("init_date") is None:
        pii["init_date"] = datetime.now().strftime("%Y-%m-%d")
    save_json(PII_PATH, pii)
    print(f"[rebalance] pii-index.json updated — {len(assets)} assets, "
          f"rebalance #{pii['rebalance_count']}")


# ── Entry point ───────────────────────────────────────────────────────────────

def run(assets_dir: Path = ASSETS_PATH, dry_run: bool = False):
    print(f"[rebalance] scanning: {assets_dir}")
    assets = load_active_assets(assets_dir)

    if not assets:
        print("[rebalance] no active asset nodes found. Add assets to the vault first.")
        return

    pii = load_json(PII_PATH)
    new_weights = compute_weights(assets)
    triggers = check_rebalance(assets, pii)

    if not triggers:
        print(f"[rebalance] no thresholds exceeded across {len(assets)} assets. No action.")
        return

    print(f"[rebalance] {len(triggers)} threshold(s) exceeded:")
    for t in triggers:
        print(f"  {t['asset']}: score {t['score_before']} → {t['score_after']} "
              f"(δ={abs(t['delta_score']):.2f}, threshold={t['threshold']})")

    if not dry_run:
        for trigger in triggers:
            push_rebalance_to_stack(trigger, assets, new_weights)
        print(f"[rebalance] {len(triggers)} item(s) pushed to stack. "
              f"Awaiting user review in dashboard.")
    else:
        print("[rebalance] dry_run=True — stack not modified.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Rebalance engine for Living System Prompt")
    parser.add_argument("--dry-run", action="store_true", help="Check thresholds without writing to stack")
    parser.add_argument("--assets-dir", type=str, default=str(ASSETS_PATH),
                        help="Path to assets directory (default: examples/ai-bubble-short/assets)")
    args = parser.parse_args()
    run(assets_dir=Path(args.assets_dir), dry_run=args.dry_run)
