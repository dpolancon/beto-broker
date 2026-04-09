# A Living System for Financial Market Self-Discovery

> **Reproducible Prompt v1.0** | No PII | April 2026  
> All personal account data requested post-prompt via `.env` gateways.  
> This file is the versioned specification of the system. Track changes with `git log PROMPT.md`.

---

## Frontmatter

```yaml
version: "1.0"
date: "2026-04-08"
author: "[post-prompt]"
scenario: "[A | B | C — post-prompt]"
central_node: "[post-prompt]"
jurisdiction: "[post-prompt]"
nav_base_usd: "[post-prompt]"
```

---

## PART I — System Philosophy

### 1.1 What this system is

An AI-mediated, human-steered supervised learning simulation that learns about financial markets starting from explicit research priors. It is not a black box — every observation, every signal, every library toggle is recorded in a human-readable knowledge graph. The human is always sovereign: the system suggests, the user decides.

### 1.2 The three surfaces

| Surface | Tool | Mode | Speed |
|---|---|---|---|
| The Vault | Obsidian + VS Code | Where thinking happens | Slow, deliberate, permanent |
| The Live Dashboard | Streamlit (local browser) | Where observation happens | Fast, ambient, real-time |
| The Terminal | VS Code integrated terminal | Where execution happens | Precise, intentional |

All three share one local repository as the single source of truth. Synced to GitHub by user choice. No cloud dependency for core function.

### 1.3 The self-discovery principle

Knowledge is created through observation. The system starts with priors (the central node), observes markets in real time, generates suggestions, and stacks them for human review. The user decides what becomes permanent knowledge in the vault. Every library toggled, every rebalance approved, every node added is a recorded step in the user's intellectual trajectory through the system.

### 1.4 The dual-core capability

The system starts with **one central node** — one prior, one thesis. A second core can be activated by explicit user design, with a human-calibrated dominance weight between the two.

> **Rule of thumb**: Start with one central node to learn the system. The multiverse comes later, by design. This is a suggestion — not a constraint. The user is always sovereign.

---

## PART II — Repository Architecture

### 2.1 Directory structure

```
/living-system-prompt
├── /vault
│   ├── /system
│   │   ├── stack.json                  ← pending suggestions buffer
│   │   ├── pii-index.json              ← Prior-Implied Index state
│   │   └── /templates
│   │       ├── asset-node.md
│   │       ├── observation-node.md
│   │       └── library-node.md
│   ├── /examples
│   │   └── /ai-bubble-short            ← worked example: research priors
│   │       ├── central-node.md
│   │       ├── /assets
│   │       └── /observations
│   ├── /my-priors                      ← user's own central node (empty at init)
│   │   └── central-node.md
│   └── /libraries                      ← library registry
│       ├── py_vollib.md
│       ├── QuantLib.md
│       ├── vectorbt.md
│       ├── backtrader.md
│       ├── ib_insync.md
│       ├── tws-api-official.md
│       ├── yfinance.md
│       ├── openbb.md
│       ├── websockets.md
│       ├── confluent-kafka.md
│       ├── scikit-learn.md
│       ├── xgboost.md
│       ├── lightgbm.md
│       ├── streamlit.md
│       ├── dash.md
│       └── /ai-assistants
│           ├── github-copilot.md
│           ├── cursor.md
│           └── continue.md
├── /dashboard
│   └── app.py                          ← Streamlit entry point
├── /scripts
│   ├── vault_watcher.py                ← md ↔ json sync
│   ├── score_engine.py                 ← PII and scoring
│   ├── stack_manager.py                ← stack read/write/remind
│   └── rebalance_engine.py             ← delta threshold checks
├── /data                               ← heavyweight data, outside vault
│   └── .gitkeep
├── /tests
│   └── .gitkeep
├── .env.example
├── .gitignore
├── requirements.txt
├── PROMPT.md                           ← this file
└── README.md
```

### 2.2 File type rules

The vault stores **only**: `.md` `.json` `.csv` `.txt`

No binaries, no databases, no `.pkl`, no `.parquet` inside `/vault`.  
Heavy data (historical OHLCV, option chains) lives in `/data` outside the vault.

### 2.3 GitHub sync

```bash
git init
git remote add origin [YOUR_REPO_URL]   # post-prompt
git push -u origin main
git tag v1.0
```

`.gitignore` excludes `.env` and `*_PRIVATE*`. The vault is fully public-safe by design.

### 2.4 VS Code recommended extensions

- Python, Pylance
- GitLens
- Markdown All in One
- YAML
- Obsidian for VS Code (or open `/vault` in the Obsidian app directly)
- AI assistant: GitHub Copilot / Cursor / Continue (user choice — record in library registry)

---

## PART III — Vault Node Schema

Three node types. Each is a `.md` file (human-readable in Obsidian) with YAML frontmatter and a companion `.json` (machine-readable). The watcher script `/scripts/vault_watcher.py` keeps them in sync on save.

### 3.1 Asset node (`/vault/system/templates/asset-node.md`)

```yaml
---
node_type: asset
asset: "[TICKER]"
bucket: "[semiconductors | hyperscalers | software_ai | etf | benchmark]"
score: 0
weight: 0.000
delta_threshold: 5
kappa: 0.000000
mcv: 0.0000
sigma_annualized: 0.00
last_rebalance: "[YYYY-MM-DD]"
rebalance_trigger: "[score_update | node_added | node_removed | manual]"
status: "[active | inactive | removed]"
notes: ""
---

# [TICKER]

## Prior
[Why this asset is in the universe. What your research says about it.]

## Observations
<!-- Auto-populated by system from stack commits. Date-stamped. -->

## Links
[[central-node]] [[scoring-model]] [[rebalance-log]] [[pii-index]]
```

### 3.2 Observation node (`/vault/system/templates/observation-node.md`)

```yaml
---
node_type: observation
date: "[YYYY-MM-DD HH:MM]"
trigger: "[score_update | borrow_spike | iv_skew_shift | macro_event | manual]"
assets_affected: []
delta_weight: 0.0000
delta_index_variance: 0.000000
library_source: ""
stack_id: ""
stack_state: "[pending | committed | discarded]"
user_note: ""
---

# Observation — [DATE]

## What the system detected
[Auto-populated from stack item on commit.]

## User annotation
[Written by user before or after committing.]

## Links
<!-- Link to affected asset nodes -->
```

### 3.3 Library node (`/vault/system/templates/library-node.md`)

```yaml
---
node_type: library
name: ""
domain: "[options_pricing | backtesting | ibkr_connectivity | market_data | streaming | ml_scoring | visualization | ai_assistant]"
status: "[active | inactive | candidate]"
installed: false
toggled_on: null
toggled_off: null
observations_generated: 0
stack_items_committed: 0
stack_items_discarded: 0
replaced_by: null
notes: ""
---

# [Library Name]

## What it teaches
[What becomes visible through this lens that wasn't visible before.]

## Toggle history
<!-- Auto-populated by vault_watcher.py -->

## Links
<!-- Link to observations generated while this library was active -->
```

---

## PART IV — Library Registry

> **Rule**: Toggling a library off never deletes its node or observation history. The vault retains the full intellectual trajectory.

### Options Pricing & Greeks

| Library | Default | Substitutes | What it teaches |
|---|---|---|---|
| `py_vollib` | **active** | QuantLib, mibian | Fast BSM greeks. Limited smile modeling. |
| `QuantLib` | candidate | py_vollib | Full vol surface, smile modeling, term structure. |
| `mibian` | candidate | py_vollib | Lightweight BSM alternative. |

### Backtesting

| Library | Default | Substitutes | What it teaches |
|---|---|---|---|
| `vectorbt` | **active** | backtrader | Vectorized, fast parallel backtest. |
| `backtrader` | inactive | vectorbt | Event-driven, more realistic fill modeling. |
| `quantstrat` (R) | candidate | vectorbt | Signal-based, institutional-style. |

### IBKR Connectivity

| Library | Default | Substitutes | What it teaches |
|---|---|---|---|
| `ib_insync` | **active** | TWS API official | Async wrapper, simpler state management. |
| `TWS API official` | candidate | ib_insync | Raw official client, maximum control. |

### Market Data

| Library | Default | Substitutes | What it teaches |
|---|---|---|---|
| `yfinance` | **active** | openbb, pandas_datareader | Fast, free, 1m bars. |
| `openbb` | candidate | yfinance | Multi-source, extensible, community-driven. |
| `pandas_datareader` | inactive | yfinance | Legacy but stable alternative. |

### Streaming

| Library | Default | Substitutes | What it teaches |
|---|---|---|---|
| `websockets` | **active** | confluent-kafka | Lightweight async streaming. |
| `confluent-kafka` | candidate | websockets | Production-grade, Kafka backbone. |

### ML / Scoring

| Library | Default | Substitutes | What it teaches |
|---|---|---|---|
| `scikit-learn` | **active** | xgboost, lightgbm | Baseline models, interpretable. |
| `xgboost` | candidate | scikit-learn | Gradient boosting, strong baseline. |
| `lightgbm` | candidate | scikit-learn | Fast training on large datasets. |

### Visualization

| Library | Default | Substitutes | What it teaches |
|---|---|---|---|
| `streamlit` | **active** | dash | Fastest path to live local dashboard. |
| `plotly` | **active** (within streamlit) | matplotlib | Interactive charts, hover data. |
| `dash` | candidate | streamlit | More control, production-grade layout. |

### AI Coding Assistant

| Tool | Default | Substitutes | What it teaches |
|---|---|---|---|
| `GitHub Copilot` | candidate | Cursor, Continue | IDE-integrated, broad language support. |
| `Cursor` | candidate | Copilot | Repo-aware, strong context window. |
| `Continue` | candidate | Copilot | Open source, local model support. |

---

## PART V — The $100 Normalized Unit and Prior-Implied Index

### 5.1 The $100 unit

All performance is expressed as a return on a normalized $100 unit. Actual account size, NAV, and position sizes are never stored in the vault. They are entered post-prompt via `.env` and used only at runtime.

```
NAV_0 = $100.00  (vault opening day)
NAV_t = NAV_{t-1} × (1 + r_strategy_t)
```

Any user can replicate the simulation with their own capital: x% return on the $100 unit = x% return on their actual base.

### 5.2 The Prior-Implied Index (PII)

A score-weighted performance index built entirely from the asset universe in the vault. Initialized at 100 on the same day as the $100 unit.

**Index level:**

```
PII_t = PII_{t-1} × (1 + Σ_i  w_{i,t-1} × r_{i,t})
```

**Weights:**

```
w_{i,t} = S_{i,t} / Σ_j S_{j,t}
```

Weights sum to 1 by construction. Higher score = more weight = more "bubbly" conviction.

**Alpha:**

```
α_t = NAV_t − PII_t
```

When the bubble deflates and the strategy pays off, α_t > 0.

### 5.3 Score formula (MAD-robust)

**Robust z-score:**

```
Z(x_i) = (x_i − median(x)) / (1.4826 × MAD(x))
```

**Score (logistic mapping to [0, 100]):**

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

σ(x) = 1 / (1 + exp(−x))

BorrowPenalty = min(BorrowFee / 0.20, 1)
AIExposure    ∈ [0, 1]
IVSkew        = IV_25Δput − IV_25Δcall  (vol points)
```

### 5.4 Asset-specific δ thresholds

Each asset has a rebalance threshold `δ_i` calibrated so that a `δ_i`-point score move produces **equal index variance impact** across all assets. Derived from the variance sensitivity coefficient `κ_i`:

```
κ_i = (2/Σ) × [ (1 − w_i) × MCV_i − w_i × Σ_{j≠i} MCV_j ]

MCV_i = Σ_j w_j × Cov(r_i, r_j)

δ_i* = ΔVar* / |κ_i|      (then rescaled to practical integer points)
```

> ⚠️ **EXAMPLE INSTANTIATION** — The table below is one user's priors operationalized.  
> Replace entirely with your own universe, scores, and derived thresholds.

| Asset | Bucket | S_i (example) | w_i | δ_i | κ_i | Note |
|---|---|---:|---:|---:|---:|---|
| NVDA | Semis | 120 | 0.240 | 3 | −0.000254 | Dominant, tight threshold |
| AMD | Semis | 80 | 0.160 | 13 | −0.000051 | High corr, looser |
| SMCI | Semis | 45 | 0.090 | 2 | +0.000344 | Idiosyncratic vol, tightest |
| MSFT | Hyperscaler | 60 | 0.120 | 3 | −0.000233 | QQQ-correlated |
| GOOGL | Hyperscaler | 55 | 0.110 | 4 | −0.000166 | Moderate |
| PLTR | Software AI | 70 | 0.140 | 5 | +0.000148 | Idiosyncratic |
| ARKK | ETF | 40 | 0.080 | 3 | +0.000213 | Amplifier |
| QQQ | Benchmark | 30 | 0.060 | ∞ | −0.000001 | Variance-neutral anchor |

### 5.5 Dashboard benchmark display

Three curves rendered simultaneously on the same chart:

1. `NAV_t` — strategy performance ($100 base)
2. `PII_t` — prior-implied index ($100 base)
3. Self-referential cumulative return — strategy vs its own starting point

QQQ and regime-conditional benchmarks available as user-activated features (second-core candidates), not defaults.

---

## PART VI — The Stack Mechanism

### 6.1 What the stack is

`/vault/system/stack.json` — a temporary buffer holding all system-generated suggestions pending human review. The system **never** writes permanently to the vault without user approval.

### 6.2 Stack file format

```json
{
  "stack": [
    {
      "id": "obs-YYYY-MM-DD-001",
      "timestamp": "YYYY-MM-DDTHH:MM:SS",
      "type": "score_update",
      "asset": "[TICKER]",
      "score_before": 0,
      "score_after": 0,
      "delta_score": 0,
      "delta_weight": 0.0000,
      "delta_index_variance": 0.000000,
      "exceeds_threshold": false,
      "threshold": 0,
      "library_source": "",
      "rebalance_recommended": false,
      "awaiting_user_approval": true,
      "user_note": null
    }
  ],
  "stack_size": 0,
  "last_updated": "YYYY-MM-DDTHH:MM:SS"
}
```

### 6.3 User actions on each stack item

| Action | Effect |
|---|---|
| **Commit** | Writes observation node to vault permanently. Updates asset node. Logs to rebalance-log. |
| **Discard** | Removes from stack. Logs as discarded in library node stats. No vault write. |
| **Annotate** | Adds `user_note` before committing. |

### 6.4 Stack reminder rule

Dashboard shows persistent badge: **"Stack: N items awaiting review."**  
When stack exceeds 50 items, system suggests (not forces) a review session.

---

## PART VII — Onboarding Flow

Seven steps. One action per step. One output per step.

### Step 1 — Open the vault
**Action:** Clone the repo locally. Open `/vault` in Obsidian. Open repo root in VS Code.  
**Output:** Three surfaces live simultaneously for the first time.

### Step 2 — Connect to GitHub *(optional but recommended)*
**Action:** `git remote add origin [YOUR_REPO_URL]` → `git push -u origin main` → `git tag v1.0`  
**Output:** Vault is versioned and backed up.

### Step 3 — Deploy your prior to the central node
**Action:** Edit `/vault/my-priors/central-node.md`. Write your thesis. This seeds the knowledge graph.  
**Suggestion:** Study the example in `/vault/examples/ai-bubble-short/` first.  
**Output:** The knowledge graph has a center of gravity.

### Step 4 — Build your universe
**Action:** For each asset, copy `/vault/system/templates/asset-node.md`. Fill in YAML frontmatter. Save.  
**Output:** The PII has a universe. Weights are auto-computed on first dashboard load.

### Step 5 — Configure your library registry
**Action:** Open `/vault/libraries/`. Set `status: active` or `status: inactive` in each node's frontmatter. Run `pip install -r requirements.txt`.  
**Output:** The system knows which lenses are live.

### Step 6 — Enter credentials *(POST-PROMPT)*
**Action:** Copy `.env.example` → `.env`. Fill in:
```
IBKR_GATEWAY_URL=https://localhost:5000
IBKR_ACCOUNT_ID=[YOUR_ACCOUNT_ID]
NAV_BASE_USD=[YOUR_ACTUAL_NAV]
PAPER_TRADING=true
BASE_CURRENCY=USD
JURISDICTION=[CL | US | EU | UK]
SCENARIO=[A | B | C]
```
`.env` is git-ignored. Never committed. Never in the vault.  
**Output:** System can connect to IBKR and normalize to your actual NAV.

### Step 7 — Launch the dashboard
**Action:** `streamlit run dashboard/app.py`  
**Output:** Three curves appear. Stack badge shows 0. The system is live.

---

## PART VIII — Worked Example: AI Bubble Short

> ⚠️ **EXAMPLE INSTANTIATION** — One user's priors operationalized.  
> Not prescriptive. Replace entirely with your own central node and universe.  
> Source files: `/vault/examples/ai-bubble-short/`

### 8.1 The central node

**Thesis:** A structured short against the AI bubble using options with capped maximum loss. Instruments: debit put spreads (primary), long puts (crash layer). Preferred over naked shorts due to margin and squeeze risk.

**Scenario A defaults:**

| Parameter | Value |
|---|---|
| NAV base | $100k (normalized to $100 unit) |
| Max loss per idea | 0.75% NAV |
| Sleeve budget | 6% NAV ($6,000) |
| Kill-switch | 50% sleeve drawdown ($3,000) |
| Jurisdiction | Chile (CMF) / US markets via IBKR |
| Horizon | 8–16 weeks per position |

### 8.2 Operational risk thresholds (example)

| Signal | Threshold | Automatic response |
|---|---|---|
| Sleeve drawdown | 30–50% of budget | Reduce 50% exposure, pause 48h |
| Borrow fee | >10% annual | Migrate short stock → puts/spreads |
| Margin cushion | <1.2× required | Reduce sold legs |
| IV crush post-event | −30% IV | Take gains on spreads |
| Gap up vs thesis | +10% day / +20% overnight | Kill-switch on direct shorts |

### 8.3 Operational flow

```
Data ingestion
(1m bars + option chain + borrow fee + short interest)
        ↓
Score + Signals
(S_i, triggers: technical / fundamental / macro)
        ↓
Risk engine
(max loss per idea/sleeve, VaR proxy, bucket limits)
        ↓
Pre-trade checks
(liquidity, spreads, OI, margin, projected borrow)
        ↓
Order builder
(multileg spreads, limit orders, idempotency keys)
        ↓
Order router
(IBKR Client Portal REST API → https://localhost:5000)
        ↓
Execution + fills + reconciliation
        ↓
Monitoring
(PnL, margin ratio, borrow fee, IV, short interest, DTC)
        ↓
Automatic responses
(reduce, hedge, roll, kill-switch)
        ↓
[back to Risk engine]
```

---

## PART IX — Post-Prompt Input Gateways

> All fields below are entered **after** reading this prompt.  
> None are stored in the vault. All live in `.env` only.

### Gateway 1 — IBKR credentials
```
IBKR_GATEWAY_URL=https://localhost:5000
IBKR_ACCOUNT_ID=
PAPER_TRADING=true
```

### Gateway 2 — Capital normalization
```
NAV_BASE_USD=
BASE_CURRENCY=USD
```

### Gateway 3 — Jurisdiction
```
JURISDICTION=          # CL | US | EU | UK
BROKER_TYPE=retail     # retail | professional
```

### Gateway 4 — Prior deployment
```
CENTRAL_NODE_PATH=vault/my-priors/central-node.md
UNIVERSE_TICKERS=      # comma-separated, e.g. NVDA,AMD,SMCI,MSFT
SCENARIO=A             # A | B | C
```

### Gateway 5 — Library preferences
```
ACTIVE_LIBRARIES=py_vollib,vectorbt,ib_insync,yfinance,websockets,scikit-learn,streamlit,plotly
```

---

## PART X — Design Principles

1. **The human is always sovereign.** The system suggests. The user decides.
2. **Priors are explicit.** No hidden assumptions. Every weight, threshold, and formula is documented in the vault.
3. **Self-discovery is operational.** Every library toggle, every rebalance, every committed observation is a recorded step in the user's learning trajectory.
4. **Privacy by design.** No PII in the vault. No PII on GitHub. Credentials enter only at runtime via `.env`.
5. **Lightweight by design.** Vault files are `.md`, `.json`, `.csv`, `.txt` only. The system runs on a laptop.
6. **The example is not the system.** The AI bubble short thesis is one instantiation. The system is agnostic.
7. **One central node to start.** Not a constraint — a suggestion grounded in the system's own learning theory.
8. **The stack is the conscience.** Nothing becomes permanent knowledge without human approval.
9. **Libraries are lenses.** Switching libraries is switching epistemology. The vault records the trajectory.
10. **The $100 unit is the universal language.** Any user, any capital, any thesis can be expressed and compared in the same normalized unit.

---

## Changelog

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-08 | Initial release. Full system specification. |

---

*Reproducible Prompt v1.0 | No PII | April 2026*
