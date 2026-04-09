# Scoring Model: MAD-Robust Composite Score

## Purpose

Every asset in the universe receives a **bubble score** S_i ∈ [0, 100]. Higher score = higher conviction that the asset is overvalued. The score determines index weight via:

```
w_i,t = S_i,t / Σ_j S_j,t
```

---

## Score Formula

### Step 1 — MAD-Robust Z-Score (per signal)

```
Z(x_i) = (x_i − median(x)) / (1.4826 × MAD(x))
```

Using MAD (Median Absolute Deviation) instead of standard deviation makes the score robust to outliers — critical in bubble detection where tail observations carry meaning.

### Step 2 — Composite Score

```
S_i = 100 × σ(
    0.25 × Z(EV/Sales)
  + 0.20 × Z(P/FCF)
  + 0.15 × AIExposure
  + 0.10 × Z(ShortInterest)
  + 0.10 × Z(DaysToCover)
  − 0.10 × BorrowPenalty
  + 0.10 × IVSkew
)
```

Where:
- `σ()` = logistic function, maps to (0, 1), scaled to (0, 100)
- `BorrowPenalty = min(BorrowFee / 0.20, 1)`
- `AIExposure ∈ [0, 1]`
- `IVSkew = IV_25Δput − IV_25Δcall` (in vol points)

---

## Prior-Implied Index (PII)

```
PII_t = PII_{t-1} × (1 + Σ_i w_{i,t-1} × r_{i,t})
```

Initialized at 100. Rises when bubbly assets rise. Strategy earns alpha when bubble deflates:

```
α_t = NAV_t − PII_t
```

---

## Example Instantiation (AI Bubble Short)

| Asset | Bucket | Score | Weight | δ_i | κ_i | Note |
|-------|--------|-------|--------|-----|-----|------|
| NVDA | Semis | 120 | 0.240 | 3 | −0.000254 | Dominant, tight threshold |
| AMD | Semis | 80 | 0.160 | 13 | −0.000051 | High corr, looser |
| SMCI | Semis | 45 | 0.090 | 2 | +0.000344 | Idiosyncratic vol, tightest |
| MSFT | Hyper | 60 | 0.120 | 3 | −0.000233 | QQQ-correlated |
| GOOGL | Hyper | 55 | 0.110 | 4 | −0.000166 | Moderate |
| PLTR | Sw AI | 70 | 0.140 | 5 | +0.000148 | Idiosyncratic |
| ARKK | ETF | 40 | 0.080 | 3 | +0.000213 | Amplifier |
| QQQ | Bench | 30 | 0.060 | ∞ | −0.000001 | Variance-neutral anchor |

> These are one user's priors operationalized. Any user derives their own scores using the same formula.
