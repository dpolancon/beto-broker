---
node_type: observation
date: "2026-04-08 23:19"
trigger: manual
assets_affected: [NVDA, AMD, SMCI, MSFT, GOOGL, PLTR, ARKK, QQQ]
delta_weight: 0.0
delta_index_variance: 0.0
library_source: "rebalance_engine.py v1.0.1"
stack_id: "dry-run-validation"
stack_state: committed
user_note: "First system validation. Dry-run only. No stack writes. No live data."
---

# Observation — 2026-04-08: Dry-Run Validation

## What the system detected

Full engine validation run against the 8-asset example universe.
Mode: `--dry-run` (no stack writes, no vault mutations).

### Phase 1 — Cold start
Engine loaded 8 active assets from `vault/examples/ai-bubble-short/assets/`.
`pii-index.json` contained no prior scores.
Result: no thresholds exceeded. Clean cold-start confirmed.

### Phase 2 — Weight computation

| Asset | Score | Weight | Cumulative |
|---|---:|---:|---:|
| NVDA | 120 | 0.2400 | 0.2400 |
| AMD | 80 | 0.1600 | 0.4000 |
| SMCI | 45 | 0.0900 | 0.4900 |
| MSFT | 60 | 0.1200 | 0.6100 |
| GOOGL | 55 | 0.1100 | 0.7200 |
| PLTR | 70 | 0.1400 | 0.8600 |
| ARKK | 40 | 0.0800 | 0.9400 |
| QQQ | 30 | 0.0600 | 1.0000 |
| **TOTAL** | **500** | **1.0000** | — |

Weight sum = 1.0000 exactly. Formula `w_i = S_i / Σ S_j` verified.

### Phase 3 — δ_i threshold logic

**Below-threshold shocks (should not trigger):**
- NVDA+2 (δ=3), AMD+5 (δ=13), SMCI+1 (δ=2), QQQ+10 (δ=999)
- Result: ✓ PASS — zero triggers fired

**At-threshold shocks (should trigger):**
- NVDA+3, SMCI+2, MSFT+3, PLTR+5
- Result: ✓ PASS — all 4 triggered, zero false positives

### Phase 4 — QQQ variance-neutral anchor

50-point shock on QQQ (δ=999) → no trigger.
Result: ✓ PASS — benchmark anchor exempt as designed.

### Phase 5 — ΔVar equalization

| Asset | δ_i | kappa_abs | ΔVar = kappa × δ |
|---|---:|---:|---:|
| NVDA | 3 | 0.000254 | 0.000762 |
| AMD | 13 | 0.000051 | 0.000663 |
| SMCI | 2 | 0.000344 | 0.000688 |
| MSFT | 3 | 0.000233 | 0.000699 |
| GOOGL | 4 | 0.000166 | 0.000664 |
| PLTR | 5 | 0.000148 | 0.000740 |
| ARKK | 3 | 0.000213 | 0.000639 |

ΔVar range: 0.000639 – 0.000762. Spread: 0.000123 across 7 assets.
Equalization derivation holds in practice. ✓ PASS

## User annotation

All 5 validation phases passed. Engine is consistent with:
- PROMPT.md Part V formula (MAD-robust scores, weight normalization)
- PROMPT.md Part V.4 (asset-specific δ thresholds derived from κ_i)
- PROMPT.md Part VI (stack schema, dry-run flag, no unauthorized vault writes)

System cleared for live scoring data ingestion.
Next step: wire score_engine.py to yfinance for live S_i computation.

## Links

[[pii-index]] [[central-node]] [[NVDA]] [[AMD]] [[SMCI]] [[MSFT]] [[GOOGL]] [[PLTR]] [[ARKK]] [[QQQ]]
[[yfinance]] [[rebalance_engine]]
