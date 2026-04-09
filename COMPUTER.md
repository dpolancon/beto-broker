# COMPUTER.md — Shared Memory for Computer Sessions

> This file is the entry point for any Computer (Perplexity) session working on this repo.
> Read this first. It tells Computer exactly where things are and how to continue the work.

---

## What this repo is

A living, versioned system for financial market self-discovery.
Full specification: `PROMPT.md` — read it before making any changes.

## Current version

- **Prompt version**: 1.0
- **Tagged**: `v1.0`
- **Date**: 2026-04-08
- **Owner**: dpolancon

## How Computer should work with this repo

### Reading
- `PROMPT.md` — the full system specification. Version-controlled. Read before any task.
- `vault/system/stack.json` — current pending suggestions. Check state before writing.
- `vault/system/pii-index.json` — PII index state (scores, weights, alpha).
- `vault/my-priors/central-node.md` — the user's active central node and thesis.
- `vault/libraries/*.md` — which libraries are active/inactive/candidate.

### Writing rules
1. **Never write PII** to any file in `vault/`. Credentials live in `.env` only (git-ignored).
2. **Never overwrite `PROMPT.md`** without incrementing the version in frontmatter and adding a changelog entry.
3. **Always commit with a meaningful message** describing what changed and why.
4. **Tag versions** when `PROMPT.md` changes: `v1.1`, `v1.2`, etc.
5. **Stack writes go to `vault/system/stack.json`** only — never directly to vault nodes.

### Branching convention
- `master` — stable, tagged releases only
- `develop` — active work in progress
- `feature/<name>` — new components (e.g. `feature/dashboard-pii-chart`)

## What has been built so far

| Component | Path | Status |
|---|---|---|
| System specification | `PROMPT.md` | v1.0 complete |
| Vault skeleton | `vault/` | Initialized |
| Worked example | `vault/examples/ai-bubble-short/` | Partial — NVDA node only |
| User prior | `vault/my-priors/central-node.md` | Empty — awaiting user input |
| Library registry | `vault/libraries/` | 3 nodes (py_vollib, yfinance, ib_insync) |
| Dashboard | `dashboard/app.py` | Scaffold only — no live data yet |
| Score engine | `scripts/score_engine.py` | Formula complete, needs live data wiring |
| Stack manager | `scripts/stack_manager.py` | Complete |
| Vault watcher | `scripts/vault_watcher.py` | Complete |

## What needs to be built next

- [ ] Wire `score_engine.py` to live yfinance data
- [ ] Wire `dashboard/app.py` to IBKR Client Portal API (post `.env` credentials)
- [ ] Add remaining example asset nodes (AMD, SMCI, MSFT, GOOGL, PLTR, ARKK, QQQ)
- [ ] Add remaining library nodes (vectorbt, websockets, scikit-learn, streamlit, etc.)
- [ ] Build `scripts/rebalance_engine.py` — δ threshold checks + PII update
- [ ] Build `dashboard/` panels: PII chart, scoring table, options greeks, risk monitor
- [ ] Write `scripts/ibkr_client.py` — IBKR Client Portal REST wrapper

## How to resume in a new Computer session

Paste this into the chat:

```
I'm working on the living-system-prompt repo at github.com/dpolancon/living-system-prompt.
Read COMPUTER.md first, then PROMPT.md. Here is what I need today: [YOUR TASK]
```

Computer will clone the repo, read the context, and continue exactly where we left off.

---

*This file is maintained by Computer. Update it after any significant session.*
