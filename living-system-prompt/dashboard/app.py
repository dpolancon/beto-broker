"""
Living System Prompt — Streamlit Dashboard
==========================================
Surface 2: Where observation happens.

Run: streamlit run dashboard/app.py
Reads from: /vault/system/pii-index.json, /vault/system/stack.json
Credentials: loaded from .env (never from vault)
"""

import streamlit as st
import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

VAULT_ROOT = Path(__file__).parent.parent / "vault"
STACK_PATH = VAULT_ROOT / "system" / "stack.json"
PII_PATH   = VAULT_ROOT / "system" / "pii-index.json"

st.set_page_config(
    page_title="Living System",
    page_icon="📊",
    layout="wide",
)

# --- Header ---
st.title("Living System — Financial Market Observatory")
st.caption("Surface 2: Observation | Human-steered | AI-mediated | v1.0")

# --- Stack reminder badge ---
with open(STACK_PATH) as f:
    stack = json.load(f)

stack_size = stack.get("stack_size", 0)
if stack_size > 0:
    st.warning(f"📥 Stack: **{stack_size}** item(s) awaiting your review.", icon="⚠️")
else:
    st.success("Stack: 0 items pending. All clear.", icon="✅")

st.divider()

# --- PII and NAV curves (placeholder until IBKR connected) ---
col1, col2, col3 = st.columns(3)

with open(PII_PATH) as f:
    pii = json.load(f)

col1.metric("NAV (normalized)", f"${pii['nav_level']:.2f}", help="Strategy performance. $100 base.")
col2.metric("PII Level", f"${pii['current_level']:.2f}", help="Prior-Implied Index. $100 base.")
col3.metric("Alpha (α)", f"${pii['alpha']:.2f}", help="NAV − PII. Positive = outperforming your own bubble index.")

st.divider()

# --- Universe (placeholder) ---
st.subheader("Universe")
st.info("Add asset nodes to `/vault/my-priors/` and deploy your universe to populate this panel.")

st.divider()

# --- Stack review panel ---
st.subheader("Stack Review")

if stack_size == 0:
    st.write("No pending suggestions. The system is observing.")
else:
    for item in stack["stack"]:
        with st.expander(f"[{item['type']}] {item.get('asset', '')} — {item['timestamp']}"):
            st.json(item)
            col_a, col_b, col_c = st.columns(3)
            col_a.button("✅ Commit", key=f"commit_{item['id']}")
            col_b.button("❌ Discard", key=f"discard_{item['id']}")
            col_c.button("✏️ Annotate", key=f"annotate_{item['id']}")

st.divider()
st.caption("Credentials loaded from `.env` only. No PII in vault. Reproducible Prompt v1.0")
