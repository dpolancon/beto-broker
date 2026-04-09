# Thesis: A Living System for Financial Market Self-Discovery

**Version 1.0 · April 2026 · No PII**

---

## The Core Claim

Perplexity Computer can serve as the reasoning engine of a reproducible, human-steered financial research system — one that starts from explicit priors, observes markets in real time, and turns every observation into a permanent, auditable node in a knowledge graph.

The system does not predict markets. It helps the user **organize, test, and refine a thesis** through structured observation. Every element is configurable, auditable, and recorded.

---

## Why It Is Differentiated

### 1. Priors are explicit, not hidden
Most AI financial tools embed assumptions invisibly. Here, every weight, threshold, and formula lives in the vault as a human-readable `.md` file with YAML frontmatter. There is nothing the system knows that the user cannot see and edit.

### 2. The human is always sovereign
The system generates suggestions. The user decides what becomes permanent knowledge. The **stack mechanism** (`/vault/system/stack.json`) is the buffer between machine observation and human approval — nothing is committed without an explicit user action.

### 3. It is truly reproducible
Any user can clone the repo, fill in their own priors, run `pip install -r requirements.txt`, and launch `streamlit run dashboard/app.py`. The normalized **$100 unit** means results are comparable regardless of actual capital size.

### 4. Perplexity Computer is the native reasoning layer
The system is designed around `COMPUTER.md` — a session-resumption file that lets Perplexity Computer read the full repo state and continue building from any session. Computer is not a tool used occasionally; it is the **primary agent** that reads, suggests, scores, and writes to the stack.

### 5. The Prior-Implied Index (PII) is novel
The PII is a score-weighted performance index built from the user's own asset universe. It tracks the "bubble" the user believes exists, weighted by conviction. Alpha is simply:

```
α_t = NAV_t − PII_t
```

The user earns alpha when their thesis is correct and the bubble deflates.

---

## The Worked Example: AI Bubble Short

The system ships with one instantiated example — a structured short against the AI bubble using options with capped maximum loss, seeded by three original research reports. This example is:
- **Not prescriptive** — any user replaces it entirely with their own thesis
- **Fully documented** — every score, weight, and threshold is derived from the formula
- **Risk-bounded** — max loss per idea: 0.75% NAV; sleeve budget: 6% NAV; kill-switch: 50% sleeve drawdown

---

## What Judges Can Verify

- Clone the repo: `git clone https://github.com/dpolancon/beto-broker.git`
- Read `COMPUTER.md` to see how Perplexity Computer resumes any session
- Read `living-system-prompt/PROMPT.md` for the full system specification
- Run the scoring engine: `python living-system-prompt/scripts/rebalance_engine.py --dry-run`
- Launch the dashboard: `streamlit run living-system-prompt/dashboard/app.py`
