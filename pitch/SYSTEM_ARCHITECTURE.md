# System Architecture

## The Three Surfaces

| Surface | Tool | Function | Tempo |
|---------|------|----------|-------|
| Surface 1: The Vault | Obsidian + VS Code | Where thinking happens | Slow, deliberate, permanent |
| Surface 2: The Dashboard | Streamlit | Where observation happens | Fast, ambient, real-time |
| Surface 3: The Terminal | VS Code integrated terminal | Where execution happens | Precise, intentional |

All three surfaces share **one local repository** as the single source of truth. Synced to GitHub. No cloud dependency for core function.

---

## Repository Structure

```
beto-broker/
├── COMPUTER.md                        ← Perplexity Computer reads this first
├── pitch/                             ← Contest submission (this folder)
├── living-system-prompt/
│   ├── PROMPT.md                      ← Full reproducible prompt
│   ├── vault/
│   │   ├── system/                    ← Engine nodes, stack.json, templates
│   │   ├── examples/ai-bubble-short/  ← Worked example with research priors
│   │   ├── my-priors/                 ← User's own central node
│   │   └── libraries/                ← Library registry nodes
│   ├── dashboard/
│   │   └── app.py                     ← Streamlit dashboard
│   ├── scripts/
│   │   ├── rebalance_engine.py        ← Score → weight → rebalance loop
│   │   └── watcher.py                 ← .md ↔ .json sync
│   └── data/                          ← Lightweight .csv and .json only
├── original_research_bigshort/        ← 3 seed research reports
├── .env.example                       ← Credential template (no real values)
├── requirements.txt
└── README.md
```

---

## Data Flow

```
Market Data (yfinance / IBKR)
        ↓
  Score Engine (rebalance_engine.py)
        ↓
  Stack (stack.json) ← awaiting human approval
        ↓  [user commits]
  Vault Node (.md + .json pair)
        ↓
  Dashboard (Streamlit)
        ↓
  NAV_t, PII_t, α_t displayed as equity curves
```

---

## Perplexity Computer Integration

Perplexity Computer reads `COMPUTER.md` at the start of every session. That file contains:
- Current repo state summary
- Build status table
- Next steps queue
- Session resume instructions

This makes every Computer session **stateful and reproducible** — the AI knows exactly where the user left off.
