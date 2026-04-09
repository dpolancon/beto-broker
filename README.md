# Living System Prompt

> A human-steered, AI-mediated supervised learning simulation for financial markets.  
> Reproducible. Lightweight. No PII in the repo.

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
git clone [YOUR_REPO_URL]
cd living-system-prompt

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure credentials (post-prompt)
cp .env.example .env
# Edit .env with your IBKR account, NAV, jurisdiction

# 4. Open vault in Obsidian
# Point Obsidian at: /living-system-prompt/vault

# 5. Deploy your prior
# Edit: vault/my-priors/central-node.md

# 6. Launch dashboard
streamlit run dashboard/app.py
```

## Three surfaces

| Surface | Tool | Purpose |
|---|---|---|
| Vault | Obsidian + VS Code | Knowledge graph — thinking |
| Dashboard | Streamlit (localhost) | Real-time observation |
| Terminal | VS Code terminal | Execution and git |

## Full specification

Read `PROMPT.md` — the complete reproducible specification, versioned with git.

```bash
git log PROMPT.md        # track how the system evolves
git diff v1.0 PROMPT.md  # see what changed since first release
```

## Version history

| Tag | Date | Description |
|---|---|---|
| v1.0 | 2026-04-08 | Initial release |

---

*No PII in this repo. All credentials in `.env` (git-ignored).*
