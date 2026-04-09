# COMPUTER.md — Shared Memory for Computer Sessions

> Read this first. It tells Computer exactly where things are and how to continue.

## Repo structure

```
beto-broker/
├── COMPUTER.md                          ← you are here
├── living-system-prompt/                ← the system (vault, dashboard, scripts, PROMPT.md)
└── original_research_bigshort/          ← 3 research reports seeding the central node
```

## What this repo is

A living, versioned system for financial market self-discovery.
Full specification: `living-system-prompt/PROMPT.md` — read it before making any changes.

## Current version

- **Prompt version**: 1.0.1
- **Commit**: b78d090
- **Date**: 2026-04-08
- **Validation state**: dry-run-passed ✓
- **Owner**: dpolancon

## How Computer should work with this repo

### Reading
- `living-system-prompt/PROMPT.md` — full system spec. Read before any task.
- `living-system-prompt/vault/system/stack.json` — pending suggestions buffer.
- `living-system-prompt/vault/system/pii-index.json` — PII index state (initialized, 8 assets).
- `living-system-prompt/vault/system/observations/` — committed vault observations.
- `living-system-prompt/vault/my-priors/central-node.md` — user's active thesis (empty).
- `living-system-prompt/vault/libraries/*.md` — library toggle states.
- `original_research_bigshort/` — the three research reports seeding the central node.

### Writing rules
1. Never write PII to any vault file. Credentials live in `.env` only (git-ignored).
2. Never overwrite `PROMPT.md` without incrementing the version and adding a changelog entry.
3. Always commit with a meaningful message describing what changed and why.
4. Tag versions when `PROMPT.md` changes: `v1.1`, `v1.2`, etc.
5. Stack writes go to `vault/system/stack.json` only — never directly to vault nodes.
6. New committed observations go to `vault/system/observations/` as `obs-YYYY-MM-DD-<name>.md`.

## Build state

| Component | Path | Status |
|---|---|---|
| System specification | `living-system-prompt/PROMPT.md` | v1.0 complete |
| Original research | `original_research_bigshort/` | 3 reports — seeds central node |
| Vault skeleton | `living-system-prompt/vault/` | Complete |
| All 8 example asset nodes | `living-system-prompt/vault/examples/ai-bubble-short/assets/` | Complete (.md + .json) |
| User prior | `living-system-prompt/vault/my-priors/central-node.md` | Empty — awaiting user |
| Library registry | `living-system-prompt/vault/libraries/` | 17 nodes — all domains |
| Dashboard | `living-system-prompt/dashboard/app.py` | Scaffold — no live data yet |
| Score engine | `living-system-prompt/scripts/score_engine.py` | Formula complete, needs live data |
| Stack manager | `living-system-prompt/scripts/stack_manager.py` | Complete |
| Vault watcher | `living-system-prompt/scripts/vault_watcher.py` | Complete |
| Rebalance engine | `living-system-prompt/scripts/rebalance_engine.py` | Complete, dry-run validated ✓ |
| PII index | `living-system-prompt/vault/system/pii-index.json` | Initialized, 8 assets, validation_state: dry-run-passed |
| First observation node | `living-system-prompt/vault/system/observations/obs-2026-04-08-dry-run-validation.md` | Committed ✓ |

## What needs to be built next

- [ ] Wire score_engine.py to live yfinance data
- [ ] Wire dashboard to IBKR Client Portal API (post .env credentials)
- [ ] Build dashboard panels: PII chart, scoring table, options greeks, risk monitor
- [ ] Build scripts/ibkr_client.py — IBKR Client Portal REST wrapper
- [ ] Wire rebalance_engine.py into vault_watcher.py trigger loop
- [ ] Deploy user's own central node in vault/my-priors/central-node.md

## Validation log

| Date | Component | Result |
|---|---|---|
| 2026-04-08 | rebalance_engine.py — 5-phase dry-run | ✓ All passed |
| 2026-04-08 | pii-index.json — weight computation | ✓ Σ=1.0000 exact |
| 2026-04-08 | δ_i threshold logic — below/at threshold | ✓ Zero false positives |
| 2026-04-08 | ΔVar equalization — 7 assets | ✓ Spread 0.000123 |

## How to resume in a new Computer session

Paste this into the chat:

```
I'm working on the beto-broker repo at github.com/dpolancon/beto-broker.
Read COMPUTER.md first, then living-system-prompt/PROMPT.md.
Here is what I need today: [YOUR TASK]
```

---

*This file is maintained by Computer. Last updated: 2026-04-08 after dry-run validation.*
