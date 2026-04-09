# COMPUTER.md — Shared Memory for Computer Sessions

> Read this first. It tells Computer exactly where things are and how to continue.

## Repo structure

```
beto-broker/
├── living-system-prompt/   ← the system: vault, dashboard, scripts, PROMPT.md
└── original_research_bigshort/  ← the three research reports that seed the central node
```

## What this repo is

A living, versioned system for financial market self-discovery.
Full specification: `living-system-prompt/PROMPT.md` — read it before making any changes.

## Current version

- **Prompt version**: 1.0
- **Tagged**: initial commit
- **Date**: 2026-04-08
- **Owner**: dpolancon
- **Visibility**: public

## How Computer should work with this repo

### Reading
- `living-system-prompt/PROMPT.md` — full system spec. Read before any task.
- `living-system-prompt/vault/system/stack.json` — pending suggestions buffer.
- `living-system-prompt/vault/system/pii-index.json` — PII index state.
- `living-system-prompt/vault/my-priors/central-node.md` — user's active thesis.
- `living-system-prompt/vault/libraries/*.md` — library toggle states.
- `original_research_bigshort/` — the three research reports that seed the central node.

### Writing rules
1. Never write PII to any vault file. Credentials live in `.env` only (git-ignored).
2. Never overwrite `PROMPT.md` without incrementing the version and adding a changelog entry.
3. Always commit with a meaningful message describing what changed and why.
4. Tag versions when `PROMPT.md` changes: `v1.1`, `v1.2`, etc.
5. Stack writes go to `vault/system/stack.json` only — never directly to vault nodes.

## What has been built

| Component | Path | Status |
|---|---|---|
| System specification | `living-system-prompt/PROMPT.md` | v1.0 complete |
| Original research | `original_research_bigshort/` | 3 reports — seeds central node |
| Vault skeleton | `living-system-prompt/vault/` | Initialized |
| Worked example | `living-system-prompt/vault/examples/ai-bubble-short/` | NVDA node only |
| User prior | `living-system-prompt/vault/my-priors/central-node.md` | Empty — awaiting user |
| Library registry | `living-system-prompt/vault/libraries/` | 3 nodes (py_vollib, yfinance, ib_insync) |
| Dashboard | `living-system-prompt/dashboard/app.py` | Scaffold only |
| Score engine | `living-system-prompt/scripts/score_engine.py` | Formula complete, needs live data |
| Stack manager | `living-system-prompt/scripts/stack_manager.py` | Complete |
| Vault watcher | `living-system-prompt/scripts/vault_watcher.py` | Complete |

## What needs to be built next

- [ ] Wire score_engine.py to live yfinance data
- [ ] Wire dashboard to IBKR Client Portal API (post .env credentials)
- [ ] Add remaining example asset nodes (AMD, SMCI, MSFT, GOOGL, PLTR, ARKK, QQQ)
- [ ] Add remaining library nodes (vectorbt, websockets, scikit-learn, streamlit, etc.)
- [ ] Build rebalance_engine.py — delta threshold checks + PII update
- [ ] Build dashboard panels: PII chart, scoring table, options greeks, risk monitor
- [ ] Build scripts/ibkr_client.py — IBKR Client Portal REST wrapper

## How to resume in a new Computer session

Paste this into the chat:

```
I'm working on the beto-broker repo at github.com/dpolancon/beto-broker.
Read COMPUTER.md first, then living-system-prompt/PROMPT.md.
Here is what I need today: [YOUR TASK]
```

---

*This file is maintained by Computer. Updated after each session.*
