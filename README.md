# beto-broker

> A human-steered, AI-mediated supervised learning simulation for financial markets.  
> Reproducible. Lightweight. No PII in the repo.

---

## Repo layout

```
beto-broker/
│
├── PROMPT.md                          ← Full reproducible specification (v1.0)
├── COMPUTER.md                        ← Session memory — what the system knows so far
├── README.md                          ← You are here
├── requirements.txt                   ← Python dependencies
├── .env.example                       ← Credential template (never committed)
│
├── scripts/                           ← Engine layer
│   ├── score_engine.py                ← Live bubble scoring via yfinance + IV skew (414 lines)
│   ├── rebalance_engine.py            ← δ_i threshold checks, stack push, PII update (226 lines)
│   ├── stack_manager.py               ← Write buffer — human approval before vault commit
│   └── vault_watcher.py               ← Syncs .md frontmatter → .json on file save
│
├── vault/                             ← Knowledge graph (Obsidian-compatible)
│   ├── examples/
│   │   └── ai-bubble-short/
│   │       ├── central-node.md        ← Example thesis: AI bubble short
│   │       └── assets/                ← 8 scored assets (.md + .json each)
│   │           ├── NVDA.*             ←  Score 88.76 | weight 17.45%
│   │           ├── AMD.*              ←  Score 52.05 | weight 10.23%
│   │           ├── SMCI.*             ←  Score 78.74 | weight 15.48%
│   │           ├── MSFT.*             ←  Score 35.76 | weight  7.03%
│   │           ├── GOOGL.*            ←  Score 50.58 | weight  9.94%
│   │           ├── PLTR.*             ←  Score 100.0 | weight 19.66%  ← ceiling
│   │           ├── ARKK.*             ←  Score 51.49 | weight 10.12%  ← ETF
│   │           └── QQQ.*              ←  Score 51.36 | weight 10.10%  ← benchmark
│   │
│   ├── libraries/                     ← Epistemic lenses (toggle on/off)
│   │   ├── py_vollib.md               Options pricing
│   │   ├── QuantLib.md                Derivatives analytics
│   │   ├── mibian.md                  Black-Scholes utilities
│   │   ├── vectorbt.md                Backtesting
│   │   ├── backtrader.md              Strategy framework
│   │   ├── ib_insync.md               IBKR async wrapper
│   │   ├── tws-api-official.md        IBKR TWS official API
│   │   ├── yfinance.md                Market data (live)
│   │   ├── openbb.md                  Financial data platform
│   │   ├── pandas_datareader.md       Data ingestion
│   │   ├── websockets.md              Real-time feeds
│   │   ├── confluent-kafka.md         Event streaming
│   │   ├── scikit-learn.md            ML baseline
│   │   ├── xgboost.md                 Gradient boosting
│   │   ├── lightgbm.md                Fast gradient boosting
│   │   ├── streamlit.md               Dashboard (primary)
│   │   ├── dash.md                    Dashboard (alternative)
│   │   └── ai-assistants/
│   │       ├── github-copilot.md
│   │       ├── cursor.md
│   │       └── continue.md
│   │
│   ├── my-priors/
│   │   └── central-node.md            ← YOUR thesis goes here (empty template)
│   │
│   └── system/
│       ├── pii-index.json             ← Live PII index — 8 assets, validation_state: live
│       ├── stack.json                 ← Write buffer (human approval required)
│       ├── observations/
│       │   ├── obs-2026-04-08-dry-run-validation.md   ← First validation run
│       │   └── obs-2026-04-09-live-scoring.md         ← First live yfinance scores
│       └── templates/
│           ├── asset-node.md
│           ├── observation-node.md
│           └── library-node.md
│
├── pitch/                             ← Judge reading material
│   ├── README.md                      ← Start here — reading order + 60-sec pitch
│   ├── THESIS.md                      ← The AI bubble short thesis
│   ├── SCORING_MODEL.md               ← MAD-robust bubble score formula + live results
│   ├── SYSTEM_ARCHITECTURE.md         ← Three surfaces, vault graph, engine layer
│   ├── DESIGN_PRINCIPLES.md           ← 10 principles — human sovereign to $100 unit
│   └── ONBOARDING.md                  ← How to run this yourself in 10 minutes
│
├── original_research_bigshort/        ← Source research (3 reports + strategy note)
│   ├── deep-research-report_BigShort_v1.md
│   ├── deep-research-report_BigShort_v2.md
│   ├── deep-research-report_BigShort_v3.md
│   └── deep-research-report-Short-Run-Strategy.md
│
└── dashboard/
    └── app.py                         ← Streamlit scaffold (live panels in progress)
```

---

## What this is

A local system that:
- Learns from explicit research **priors** seeded in an Obsidian-compatible vault
- Observes financial markets in real time via IBKR Client Portal API and yfinance
- Normalizes all performance to a **$100 unit** for reproducibility and privacy
- Builds a **Prior-Implied Index (PII)** from your asset universe weighted by bubble scores
- Records every observation, library toggle, and rebalance in a **human-readable knowledge graph**
- Never writes to the vault without **explicit user approval** (the stack mechanism)

## Quick start

```bash
# 1. Clone
git clone https://github.com/dpolancon/beto-broker
cd beto-broker

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure credentials (post-prompt — no PII in repo)
cp .env.example .env
# Edit .env with your IBKR account, NAV, jurisdiction

# 4. Open vault in Obsidian
# Point Obsidian at: /vault

# 5. Deploy your prior
# Edit: vault/my-priors/central-node.md

# 6. Score live
python scripts/score_engine.py

# 7. Launch dashboard
streamlit run dashboard/app.py
```

## Three surfaces

| Surface | Tool | Purpose |
|---|---|---|
| Vault | Obsidian + VS Code | Knowledge graph — thinking |
| Dashboard | Streamlit (localhost) | Real-time observation |
| Terminal | VS Code terminal | Execution and git |

## For judges

Start with `pitch/README.md` — it has the reading order and the 60-second pitch.  
The full specification is in `PROMPT.md` (628 lines, versioned with git).

```bash
git log PROMPT.md        # track how the system evolves
git diff v1.0 PROMPT.md  # see what changed since first release
```

## Version history

| Tag | Date | Description |
|---|---|---|
| v1.0 | 2026-04-08 | Initial release — full vault architecture, scoring model, library registry |
| v1.0.1 | 2026-04-09 | Live yfinance scoring, 8 assets, 2 observation nodes, rebalance engine |

---

*No PII in this repo. All credentials in `.env` (git-ignored).*
