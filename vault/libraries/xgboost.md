---
node_type: library
name: xgboost
domain: ml_scoring
status: candidate
installed: false
toggled_on: null
toggled_off: null
observations_generated: 0
stack_items_committed: 0
stack_items_discarded: 0
replaced_by: null
notes: "Gradient boosting. Strong baseline for non-linear scoring relationships."
---

# xgboost

## What it teaches
Non-linear feature interactions the linear scoring model misses. When switched on,
teaches whether the bubble score should be additive (as currently specified) or
whether certain combinations of metrics interact multiplicatively — e.g. whether
high EV/Sales AND high AIExposure together produce a score much higher than
either alone.

## Toggle history
<!-- Auto-populated by vault_watcher.py -->

## Links
[[scikit-learn]] [[lightgbm]]
