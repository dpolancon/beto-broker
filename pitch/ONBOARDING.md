# 7-Step Onboarding Flow

Minimalist. Each step has one clear action and one clear output.

---

### Step 1 — Open the Vault
**Action:** Clone the repo locally. Open `/vault` in Obsidian. Open the repo root in VS Code.

**Output:** Three surfaces live simultaneously for the first time.

---

### Step 2 — Connect to GitHub
**Action:**
```bash
git remote add origin [YOUR_REPO_URL]
git push -u origin main
```
**Output:** Vault is versioned and backed up.

---

### Step 3 — Deploy Your Prior to the Central Node
**Action:** Edit `/vault/my-priors/central-node.md`. Write your thesis. This is the seed of the knowledge graph.

> Suggestion: Start with one central node. Study the example in `/vault/examples/ai-bubble-short/` first.

**Output:** The knowledge graph has a center of gravity.

---

### Step 4 — Build Your Universe
**Action:** For each asset, copy `/vault/system/templates/asset-node.md`. Fill in the YAML frontmatter. Save.

**Output:** The PII has a universe. Weights are auto-computed on first dashboard load.

---

### Step 5 — Configure Your Library Registry
**Action:** Open `/vault/libraries/`. Toggle libraries to `active` or `inactive`. Run:
```bash
pip install -r requirements.txt
```
**Output:** The system knows which lenses are live.

---

### Step 6 — Enter Credentials (Post-Prompt)
**Action:** Copy `.env.example` to `.env`. Fill in:
```
IBKR_GATEWAY_URL=https://localhost:5000
IBKR_ACCOUNT_ID=[YOUR_ACCOUNT_ID]
NAV_BASE_USD=[YOUR_ACTUAL_NAV]
```
> These values are used only at runtime. Never committed to git. Never stored in the vault.

**Output:** System connects to IBKR and normalizes performance to your actual NAV.

---

### Step 7 — Launch the Dashboard
**Action:**
```bash
streamlit run living-system-prompt/dashboard/app.py
```
**Output:** Three curves appear (NAV $100, PII, self-referential). Stack badge shows 0. The system is live.
