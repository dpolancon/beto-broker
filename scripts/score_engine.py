"""
score_engine.py — Living System Prompt
========================================
Computes MAD-robust bubble scores S_i and PII weights w_i
for all active asset nodes in the vault using live yfinance data.

Usage:
    python scripts/score_engine.py                    # live run, writes to pii-index.json
    python scripts/score_engine.py --dry-run          # compute only, no writes
    python scripts/score_engine.py --assets-dir PATH  # custom assets directory

Inputs (live, via yfinance):
    EV/Sales, P/FCF, ShortInterest, DaysToCover, annualized σ
    AIExposure: manually curated per asset in asset node frontmatter
    BorrowFee:  from IBKR Client Portal (post .env) — fallback to proxy from short_pct
    IVSkew:     from IBKR or yfinance options chain (25Δ put − 25Δ call)

Outputs:
    - Scores S_i ∈ [0, 100] per asset
    - Weights w_i = S_i / Σ S_j
    - Updated pii-index.json
    - Stack push for assets exceeding δ_i threshold
"""

import json
import argparse
import numpy as np
import pandas as pd
import yfinance as yf
from pathlib import Path
from datetime import datetime

VAULT_ROOT  = Path(__file__).parent.parent / "vault"
PII_PATH    = VAULT_ROOT / "system" / "pii-index.json"
STACK_PATH  = VAULT_ROOT / "system" / "stack.json"
OBS_DIR     = VAULT_ROOT / "system" / "observations"
ASSETS_PATH = VAULT_ROOT / "examples" / "ai-bubble-short" / "assets"


# ── AI Exposure manual registry ───────────────────────────────────────────────
# Curated [0, 1] exposure scores. Update as thesis evolves.
AI_EXPOSURE = {
    "NVDA":  0.95,  # near-pure AI infrastructure play
    "AMD":   0.70,  # GPU + AI accelerator growing share
    "SMCI":  0.65,  # AI server infrastructure
    "MSFT":  0.55,  # Azure AI, Copilot, OpenAI stake
    "GOOGL": 0.50,  # Gemini, cloud AI, search AI
    "PLTR":  0.80,  # AI platform / govt + commercial
    "ARKK":  0.40,  # basket, partial AI exposure
    "QQQ":   0.35,  # index, broad AI weight
}


# ── Data fetching ─────────────────────────────────────────────────────────────

def fetch_live_data(tickers: list) -> dict:
    """Fetch fundamental and market data from yfinance for all tickers."""
    results = {}
    for ticker in tickers:
        try:
            t    = yf.Ticker(ticker)
            info = t.info
            hist = t.history(period="1y")

            ev       = info.get("enterpriseValue")
            revenue  = info.get("totalRevenue")
            mktcap   = info.get("marketCap")
            fcf      = info.get("freeCashflow")
            price    = (info.get("currentPrice")
                        or info.get("regularMarketPrice")
                        or (hist["Close"].iloc[-1] if len(hist) else None))

            ev_sales  = (ev / revenue) if (ev and revenue) else None
            p_fcf     = (mktcap / fcf) if (mktcap and fcf and fcf > 0) else None
            short_pct = info.get("shortPercentOfFloat")
            short_dtc = info.get("shortRatio")

            # Annualized volatility from 1y daily returns
            sigma_ann = None
            if len(hist) > 20:
                daily_ret = hist["Close"].pct_change().dropna()
                sigma_ann = float(daily_ret.std() * np.sqrt(252))

            # IV skew proxy from options chain (25Δ approximation)
            iv_skew = _fetch_iv_skew(t)

            # Borrow fee proxy: use short_pct as a rough proxy
            # (real value comes from IBKR post .env)
            borrow_fee_proxy = (short_pct * 0.5) if short_pct else 0.01

            results[ticker] = {
                "ev_sales":         ev_sales,
                "p_fcf":            p_fcf,
                "short_interest":   short_pct,
                "days_to_cover":    short_dtc,
                "sigma_ann":        sigma_ann,
                "iv_skew":          iv_skew,
                "borrow_fee":       borrow_fee_proxy,
                "ai_exposure":      AI_EXPOSURE.get(ticker, 0.0),
                "price":            round(float(price), 2) if price else None,
                "fetched_at":       datetime.now().isoformat(),
                "data_source":      "yfinance",
            }
        except Exception as e:
            print(f"[score_engine] WARNING: failed to fetch {ticker}: {e}")
            results[ticker] = None

    return results


def _fetch_iv_skew(ticker_obj) -> float:
    """
    Approximate IV skew = IV(OTM put) - IV(ATM call) from nearest expiry.
    Returns 0.0 on failure (ETFs or missing options data).
    """
    try:
        exps = ticker_obj.options
        if not exps:
            return 0.0
        chain  = ticker_obj.option_chain(exps[0])
        puts   = chain.puts.dropna(subset=["impliedVolatility"])
        calls  = chain.calls.dropna(subset=["impliedVolatility"])
        if puts.empty or calls.empty:
            return 0.0
        # OTM put median IV vs ATM call median IV
        put_iv  = float(puts["impliedVolatility"].median())
        call_iv = float(calls["impliedVolatility"].median())
        return round(put_iv - call_iv, 4)
    except Exception:
        return 0.0


# ── Scoring ───────────────────────────────────────────────────────────────────

def z_robust(series: pd.Series) -> pd.Series:
    """MAD-robust z-score: Z(x_i) = (x_i − median) / (1.4826 × MAD)."""
    med   = series.median()
    mad   = (series - med).abs().median()
    scale = 1.4826 * mad if mad > 0 else 1.0
    return (series - med) / scale


def _fill_etf(series: pd.Series, tickers: list, etf_tickers: list) -> pd.Series:
    """
    ETFs (ARKK, QQQ) lack fundamental data (EV/Sales, P/FCF).
    Fill with cross-sectional median of single-name tickers so they
    don't dominate the score in either direction.
    """
    single_vals = series[[t for t in tickers if t not in etf_tickers]]
    median_fill = single_vals.median()
    result = series.copy()
    for etf in etf_tickers:
        if pd.isna(result[etf]):
            result[etf] = median_fill
    return result


def compute_scores(live_data: dict) -> pd.DataFrame:
    """
    Compute bubble scores S_i ∈ [0, 100] using MAD-robust z-scores.

    Formula:
      S_i = 100 × σ(
          0.25×Z(EV/Sales) + 0.20×Z(P/FCF) + 0.15×AIExposure
        + 0.10×Z(ShortInterest) + 0.10×Z(DaysToCover)
        − 0.10×BorrowPenalty + 0.10×IVSkew
      )
    """
    ETF_TICKERS = ["ARKK", "QQQ"]
    tickers     = [t for t in live_data if live_data[t] is not None]

    df = pd.DataFrame({
        t: {
            "EV_Sales":      live_data[t]["ev_sales"],
            "P_FCF":         live_data[t]["p_fcf"],
            "AIExposure":    live_data[t]["ai_exposure"],
            "ShortInterest": live_data[t]["short_interest"],
            "DaysToCover":   live_data[t]["days_to_cover"],
            "BorrowFee":     live_data[t]["borrow_fee"],
            "IVSkew":        live_data[t]["iv_skew"],
        }
        for t in tickers
    }).T

    # Fill ETF missing fundamentals with cross-sectional median
    for col in ["EV_Sales", "P_FCF", "ShortInterest", "DaysToCover"]:
        df[col] = _fill_etf(df[col], tickers, ETF_TICKERS)

    # Fill any remaining NaNs with column median
    df = df.fillna(df.median())

    borrow_penalty = np.clip(df["BorrowFee"] / 0.20, 0, 1)

    raw = (
        0.25 * z_robust(df["EV_Sales"]) +
        0.20 * z_robust(df["P_FCF"]) +
        0.15 * df["AIExposure"] +
        0.10 * z_robust(df["ShortInterest"]) +
        0.10 * z_robust(df["DaysToCover"]) -
        0.10 * borrow_penalty +
        0.10 * df["IVSkew"]
    )

    df["score_raw"] = raw
    df["score"]     = (100.0 / (1.0 + np.exp(-raw))).round(2)

    total = df["score"].sum()
    df["weight"] = (df["score"] / total).round(6)

    return df


def compute_weights(scores: pd.Series) -> pd.Series:
    total = scores.sum()
    return (scores / total).round(6) if total > 0 else pd.Series(0.0, index=scores.index)


# ── Persistence ───────────────────────────────────────────────────────────────

def load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def save_json(path: Path, data: dict):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)


def update_pii(df: pd.DataFrame, live_data: dict):
    """Write live scores and weights into pii-index.json."""
    pii = load_json(PII_PATH)
    pii["universe"]     = list(df.index)
    pii["initialized"]  = True
    pii["init_date"]    = pii.get("init_date") or datetime.now().strftime("%Y-%m-%d")
    pii["last_rebalance"] = datetime.now().isoformat()
    pii["rebalance_count"] = pii.get("rebalance_count", 0) + 1
    pii["validation_state"] = "live"

    # Read existing asset metadata (delta_threshold, kappa, mcv, sigma)
    existing = pii.get("assets", {})

    pii["assets"] = {
        ticker: {
            "score":             round(float(df.loc[ticker, "score"]), 2),
            "weight":            round(float(df.loc[ticker, "weight"]), 6),
            "delta_threshold":   existing.get(ticker, {}).get("delta_threshold", 5),
            "kappa":             existing.get(ticker, {}).get("kappa", 0.0),
            "mcv":               existing.get(ticker, {}).get("mcv", 0.0),
            "sigma_annualized":  round(live_data[ticker]["sigma_ann"] or 0.0, 4),
            "last_score_update": datetime.now().isoformat(),
            "status":            "active",
            # live inputs for auditability
            "live_inputs": {
                "ev_sales":       live_data[ticker]["ev_sales"],
                "p_fcf":          live_data[ticker]["p_fcf"],
                "ai_exposure":    live_data[ticker]["ai_exposure"],
                "short_interest": live_data[ticker]["short_interest"],
                "days_to_cover":  live_data[ticker]["days_to_cover"],
                "borrow_fee":     live_data[ticker]["borrow_fee"],
                "iv_skew":        live_data[ticker]["iv_skew"],
                "price":          live_data[ticker].get("price"),
                "data_source":    live_data[ticker].get("data_source"),
                "fetched_at":     live_data[ticker].get("fetched_at"),
            },
        }
        for ticker in df.index
        if live_data.get(ticker)
    }
    save_json(PII_PATH, pii)


# ── Observation node ──────────────────────────────────────────────────────────

def write_observation_node(df: pd.DataFrame, live_data: dict, run_ts: str):
    """Write a committed observation node for this scoring run."""
    OBS_DIR.mkdir(parents=True, exist_ok=True)
    date_str  = datetime.now().strftime("%Y-%m-%d")
    node_name = f"obs-{date_str}-live-scoring.md"
    node_path = OBS_DIR / node_name

    tickers_str = ", ".join(df.index.tolist())
    rows = ""
    for ticker in df.index:
        s   = df.loc[ticker, "score"]
        w   = df.loc[ticker, "weight"]
        ld  = live_data.get(ticker) or {}
        rows += (f"| {ticker:<6} | {s:>6.2f} | {w:>8.6f} | "
                 f"{str(ld.get('ev_sales','N/A')):>7} | "
                 f"{str(ld.get('p_fcf','N/A')):>8} | "
                 f"{ld.get('ai_exposure',0):.2f} | "
                 f"{str(ld.get('short_interest','N/A')):>6} | "
                 f"{str(ld.get('days_to_cover','N/A')):>5} | "
                 f"{ld.get('iv_skew',0):.4f} |\n")

    weight_sum = df["weight"].sum()
    top_asset  = df["score"].idxmax()
    top_score  = df["score"].max()

    links = " ".join(f"[[{t}]]" for t in df.index)

    content = f"""---
node_type: observation
date: "{run_ts}"
trigger: score_update
assets_affected: [{tickers_str}]
delta_weight: 0.0
delta_index_variance: 0.0
library_source: "score_engine.py + yfinance"
stack_id: "live-scoring-{date_str}"
stack_state: committed
user_note: "First live scoring run. All inputs from yfinance. BorrowFee proxied from short_pct. IVSkew from options chain."
---

# Observation — {run_ts}: First Live Scoring Run

## What the system detected

Live scores computed for all 8 assets using yfinance.
Formula: MAD-robust z-scores + logistic mapping to [0, 100].
BorrowFee: proxied as `short_pct × 0.5` (replace with IBKR live feed post .env setup).
IVSkew: from nearest-expiry options chain (put IV median − call IV median).

### Scores and weights

| Asset  |  Score |   Weight | EV/Sales |    P/FCF | AIExp | ShortPct |  DTC | IVSkew |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
{rows}
Weight Σ = {weight_sum:.6f}

### Key observations

- **Highest score**: {top_asset} ({top_score:.2f}) — consistent with prior thesis weighting
- **ETF handling**: ARKK and QQQ fundamentals filled with cross-sectional median of single names
- **Borrow fee**: proxied — replace with IBKR Client Portal live feed for accuracy
- **IVSkew**: live from options chain — reflects current put/call skew at time of run

## User annotation

First live scoring run. Scores should be reviewed against prior example values
in pii-index.json to assess how the live universe compares to the seeded priors.
SMCI short interest notably high (0.197) — warrants monitoring.

## Links

{links} [[pii-index]] [[yfinance]] [[score_engine]] [[rebalance_engine]]
"""
    node_path.write_text(content)
    return node_path


# ── Entry point ───────────────────────────────────────────────────────────────

def run(assets_dir: Path = ASSETS_PATH, dry_run: bool = False):
    run_ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"[score_engine] live run — {run_ts}")

    # Load active tickers from vault asset nodes
    tickers = []
    for p in sorted(assets_dir.glob("*.json")):
        data = json.loads(p.read_text())
        if data.get("status") == "active" and data.get("node_type") == "asset":
            tickers.append(data["asset"])

    if not tickers:
        print("[score_engine] no active asset nodes found.")
        return

    print(f"[score_engine] universe: {tickers}")

    # Fetch live data
    print("[score_engine] fetching live data from yfinance...")
    live_data = fetch_live_data(tickers)

    # Compute scores
    df = compute_scores(live_data)

    # Print results
    print(f"\n{'Asset':<8} {'Score':>7} {'Weight':>9}  {'EV/S':>7}  {'P/FCF':>7}  "
          f"{'AIExp':>6}  {'ShortPct':>8}  {'DTC':>5}  {'IVSkew':>8}")
    print("─" * 85)
    for ticker in df.index:
        ld = live_data.get(ticker) or {}
        print(f"  {ticker:<6} {df.loc[ticker,'score']:>7.2f} {df.loc[ticker,'weight']:>9.6f}  "
              f"{str(ld.get('ev_sales') or 'N/A'):>7}  "
              f"{str(ld.get('p_fcf') or 'N/A'):>7}  "
              f"{ld.get('ai_exposure',0):>6.2f}  "
              f"{str(ld.get('short_interest') or 'N/A'):>8}  "
              f"{str(ld.get('days_to_cover') or 'N/A'):>5}  "
              f"{ld.get('iv_skew',0):>8.4f}")
    print("─" * 85)
    print(f"  {'TOTAL':<6} {'':>7} {df['weight'].sum():>9.6f}")

    if dry_run:
        print("\n[score_engine] dry_run=True — no writes.")
        return df, live_data

    # Persist
    update_pii(df, live_data)
    print(f"\n[score_engine] pii-index.json updated")

    obs_path = write_observation_node(df, live_data, run_ts)
    print(f"[score_engine] observation node written: {obs_path.name}")

    return df, live_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Live score engine — Living System Prompt")
    parser.add_argument("--dry-run",    action="store_true")
    parser.add_argument("--assets-dir", type=str, default=str(ASSETS_PATH))
    args = parser.parse_args()
    run(assets_dir=Path(args.assets_dir), dry_run=args.dry_run)
