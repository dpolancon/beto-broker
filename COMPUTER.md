# COMPUTER.md — Shared Memory for Computer Sessions

> Read this first. It tells Computer exactly where things are and how to continue.

## Repo structure

```
beto-broker/
├── COMPUTER.md                              ← you are here
├── pitch/                                   ← contest submission + pitch video assets
│   ├── README.md                            ← one-sentence thesis, folder map
│   ├── THESIS.md                            ← full differentiated thesis (2-page)
│   ├── SYSTEM_ARCHITECTURE.md              ← 3-surface architecture + data flow
│   ├── SCORING_MODEL.md                    ← MAD-robust formula + PII + δ table
│   ├── ONBOARDING.md                       ← 7-step reproducible onboarding flow
│   └── DESIGN_PRINCIPLES.md               ← 10 design principles
├── living-system-prompt/                   ← the system (vault, dashboard, scripts)
│   ├── PROMPT.md                           ← full reproducible specification v1.0
│   ├── vault/
│   │   ├── system/
│   │   │   ├── stack.json                  ← pending suggestions buffer
│   │   │   ├── pii-index.json             ← PII state (live, 8 assets)
│   │   │   ├── observations/              ← committed vault observation nodes
│   │   │   └── templates/                 ← asset, observation, library node templates
│   │   ├── examples/ai-bubble-short/      ← worked example (8 assets, central node)
│   │   ├── my-priors/central-node.md      ← user's own thesis (empty — awaiting input)
│   │   └── libraries/                     ← 17 library nodes across all domains
│   ├── dashboard/app.py                   ← Streamlit entry point
│   ├── scripts/
│   │   ├── score_engine.py               ← live yfinance scoring (414 lines) ✓
│   │   ├── rebalance_engine.py           ← δ threshold checks + stack push ✓
│   │   ├── stack_manager.py             ← stack read/write/commit/discard ✓
│   │   └── vault_watcher.py             ← .md ↔ .json sync on save ✓
│   └── data/                             ← heavy data (outside vault)
└── original_research_bigshort/            ← 3 seed research reports (priors)
```

## What this repo is

A living, versioned system for financial market self-discovery, built as a
Perplexity Computer contest submission. Full spec: `living-system-prompt/PROMPT.md`.

The `pitch/` folder is the contest submission surface — 6 markdown files
covering thesis, architecture, scoring model, onboarding, and design principles.

## Current version

- **Prompt version**: 1.0.1
- **Latest commit**: daae026 (living-system-prompt repo) / initial (beto-broker)
- **Validation state**: live — first live scoring run completed ✓
- **Date**: 2026-04-08
- **Owner**: dpolancon

> ⚠️ NOTE FOR COMPUTER: The `living-system-prompt` GitHub repo is ahead of
> `beto-broker`. All engine files (score_engine.py, rebalance_engine.py,
> all 17 library nodes, all 8 asset nodes, observation nodes) exist in the
> living-system-prompt local workspace. Sync is pending. When working on
> engine files, prefer the local workspace at:
> /home/user/workspace/living-system-prompt/

## Pitch folder — purpose and status

| File | Purpose | Status |
|---|---|---|
| `pitch/README.md` | Contest entry point, one-sentence thesis | Complete |
| `pitch/THESIS.md` | Full 2-page differentiated thesis | Complete |
| `pitch/SYSTEM_ARCHITECTURE.md` | 3-surface + data flow diagram | Complete |
| `pitch/SCORING_MODEL.md` | MAD-robust formula, PII, δ table | Complete |
| `pitch/ONBOARDING.md` | 7-step onboarding flow | Complete |
| `pitch/DESIGN_PRINCIPLES.md` | 10 design principles table | Complete |

**Live results available for pitch**: First live scoring run (2026-04-09 03:25 UTC):
- PLTR: 100.00 | NVDA: 88.76 | SMCI: 78.74 | AMD: 52.05 | ARKK: 51.49 | QQQ: 51.36 | GOOGL: 50.58 | MSFT: 35.76
- SMCI IVSkew = +0.594 (only asset with positive put skew — market pricing downside)
- Weight Σ = 1.000000 exact

## How Computer should work with this repo

### Reading order for any session
1. `COMPUTER.md` (this file) — repo state and context
2. `living-system-prompt/PROMPT.md` — full system specification
3. `pitch/README.md` — contest context if pitch-related task
4. `living-system-prompt/vault/system/stack.json` — pending suggestions
5. `living-system-prompt/vault/system/pii-index.json` — live scores and weights

### Writing rules
1. Never write PII to any vault file. Credentials in `.env` only (git-ignored).
2. Never overwrite `PROMPT.md` without incrementing version + changelog entry.
3. Always commit with a meaningful message.
4. Tag PROMPT.md changes: `v1.1`, `v1.2` etc.
5. Stack writes → `vault/system/stack.json` only.
6. New observations → `vault/system/observations/obs-YYYY-MM-DD-<name>.md`.
7. Pitch edits → `pitch/` folder only. Never mix pitch and system files.

## Build state

| Component | Path | Status |
|---|---|---|
| System specification | `living-system-prompt/PROMPT.md` | v1.0 complete |
| Pitch folder | `pitch/` | 6 files — complete |
| Original research | `original_research_bigshort/` | 3 reports |
| All 8 example asset nodes | `living-system-prompt/vault/examples/ai-bubble-short/assets/` | Complete (.md + .json) |
| Library registry | `living-system-prompt/vault/libraries/` | 17 nodes |
| Score engine | `living-system-prompt/scripts/score_engine.py` | Live yfinance ✓ |
| Rebalance engine | `living-system-prompt/scripts/rebalance_engine.py` | Dry-run validated ✓ |
| Stack manager | `living-system-prompt/scripts/stack_manager.py` | Complete ✓ |
| Vault watcher | `living-system-prompt/scripts/vault_watcher.py` | Complete ✓ |
| Dashboard | `living-system-prompt/dashboard/app.py` | Scaffold — no live panels yet |
| PII index | `living-system-prompt/vault/system/pii-index.json` | Live — 8 assets scored ✓ |
| Observations | `living-system-prompt/vault/system/observations/` | 2 nodes (dry-run + live) ✓ |
| User prior | `living-system-prompt/vault/my-priors/central-node.md` | Empty — awaiting user |

## What needs to be built next

### System
- [ ] Build dashboard live panels: PII chart, scoring table, options greeks, risk monitor
- [ ] Build `scripts/ibkr_client.py` — IBKR Client Portal REST wrapper
- [ ] Wire `rebalance_engine.py` into `vault_watcher.py` trigger loop
- [ ] Replace BorrowFee proxy with IBKR live feed (post `.env`)
- [ ] Deploy user's own central node in `vault/my-priors/central-node.md`

### Pitch
- [ ] Add live scoring results table to `pitch/SCORING_MODEL.md`
- [ ] Sync `beto-broker` repo with all engine files from `living-system-prompt`

## Validation log

| Date | Component | Result |
|---|---|---|
| 2026-04-08 | rebalance_engine.py — 5-phase dry-run | ✓ All passed |
| 2026-04-08 | pii-index.json — weight computation | ✓ Σ=1.0000 exact |
| 2026-04-08 | δ_i threshold logic | ✓ Zero false positives |
| 2026-04-08 | ΔVar equalization — 7 assets | ✓ Spread 0.000123 |
| 2026-04-09 | score_engine.py — first live yfinance run | ✓ 8 assets scored |

## How to resume in a new Computer session

Paste this into the chat:

```
I'm working on the beto-broker repo at github.com/dpolancon/beto-broker.
Read COMPUTER.md first, then living-system-prompt/PROMPT.md.
Here is what I need today: [YOUR TASK]
```

---

*This file is maintained by Computer. Last updated: 2026-04-09 — pitch folder integrated, live scoring run documented.*
