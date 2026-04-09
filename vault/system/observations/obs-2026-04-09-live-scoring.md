---
node_type: observation
date: "2026-04-09 03:25"
trigger: score_update
assets_affected: [AMD, ARKK, GOOGL, MSFT, NVDA, PLTR, QQQ, SMCI]
delta_weight: 0.0
delta_index_variance: 0.0
library_source: "score_engine.py + yfinance"
stack_id: "live-scoring-2026-04-09"
stack_state: committed
user_note: "First live scoring run. All inputs from yfinance. BorrowFee proxied from short_pct. IVSkew from options chain."
---

# Observation — 2026-04-09 03:25: First Live Scoring Run

## What the system detected

Live scores computed for all 8 assets using yfinance.
Formula: MAD-robust z-scores + logistic mapping to [0, 100].
BorrowFee: proxied as `short_pct × 0.5` (replace with IBKR live feed post .env setup).
IVSkew: from nearest-expiry options chain (put IV median − call IV median).

### Scores and weights

| Asset  |  Score |   Weight | EV/Sales |    P/FCF | AIExp | ShortPct |  DTC | IVSkew |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| AMD    |  52.05 | 0.102312 | 10.722476042023999 | 82.39399616472978 | 0.70 | 0.0199 |  0.97 | -0.2187 |
| ARKK   |  51.49 | 0.101211 |    None |     None | 0.40 |   None |  None | 0.0469 |
| GOOGL  |  50.58 | 0.099422 | 9.38042534236775 | 100.78193338581255 | 0.50 | 0.0137 |  2.64 | -0.2778 |
| MSFT   |  35.76 | 0.070291 | 9.210751788893125 | 51.86669126477872 | 0.55 | 0.0108 |   2.5 | -0.1494 |
| NVDA   |  88.76 | 0.174470 | 20.249658834232058 | 76.13161824030328 | 0.95 | 0.0098 |  1.28 | -0.1484 |
| PLTR   | 100.00 | 0.196564 | 73.69216775224643 | 266.9897107124458 | 0.80 |  0.024 |   1.0 | -0.0156 |
| QQQ    |  51.36 | 0.100955 |    None |     None | 0.35 |   None |  None | 0.0686 |
| SMCI   |  78.74 | 0.154775 | 0.5401834835330668 | 135.6132836490143 | 0.65 | 0.19700001 |  3.61 | 0.5937 |

Weight Σ = 1.000000

### Key observations

- **Highest score**: PLTR (100.00) — consistent with prior thesis weighting
- **ETF handling**: ARKK and QQQ fundamentals filled with cross-sectional median of single names
- **Borrow fee**: proxied — replace with IBKR Client Portal live feed for accuracy
- **IVSkew**: live from options chain — reflects current put/call skew at time of run

## User annotation

First live scoring run. Scores should be reviewed against prior example values
in pii-index.json to assess how the live universe compares to the seeded priors.
SMCI short interest notably high (0.197) — warrants monitoring.

## Links

[[AMD]] [[ARKK]] [[GOOGL]] [[MSFT]] [[NVDA]] [[PLTR]] [[QQQ]] [[SMCI]] [[pii-index]] [[yfinance]] [[score_engine]] [[rebalance_engine]]
