---
node_type: library
name: lightgbm
domain: ml_scoring
status: candidate
installed: false
toggled_on: null
toggled_off: null
observations_generated: 0
stack_items_committed: 0
stack_items_discarded: 0
replaced_by: null
notes: "Fast gradient boosting. Better than xgboost on large feature sets."
---

# lightgbm

## What it teaches
Leaf-wise tree growth vs xgboost's level-wise — faster on large datasets
with many features. Useful when the scoring universe expands beyond 8 assets
or when macro features (yield curve slope, VIX term structure) are added
as additional scoring inputs.

## Toggle history
<!-- Auto-populated by vault_watcher.py -->

## Links
[[scikit-learn]] [[xgboost]]
