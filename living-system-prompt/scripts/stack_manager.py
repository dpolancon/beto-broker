"""
stack_manager.py — Living System Prompt
========================================
Read, write, commit, and discard items from the vault stack.
The stack is the conscience: nothing enters the vault without user approval.

Usage:
    from scripts.stack_manager import push_to_stack, commit_item, discard_item
"""

import json
import uuid
from datetime import datetime
from pathlib import Path

VAULT_ROOT = Path(__file__).parent.parent / "vault"
STACK_PATH = VAULT_ROOT / "system" / "stack.json"


def _load_stack() -> dict:
    with open(STACK_PATH) as f:
        return json.load(f)


def _save_stack(stack: dict):
    stack["stack_size"] = len(stack["stack"])
    stack["last_updated"] = datetime.now().isoformat()
    with open(STACK_PATH, "w") as f:
        json.dump(stack, f, indent=2)


def push_to_stack(
    event_type: str,
    asset: str,
    score_before: float,
    score_after: float,
    delta_weight: float,
    delta_index_variance: float,
    threshold: int,
    library_source: str,
) -> str:
    """Push a new suggestion to the stack. Returns the item ID."""
    stack = _load_stack()
    item_id = f"obs-{datetime.now().strftime('%Y-%m-%d')}-{str(uuid.uuid4())[:6]}"
    item = {
        "id": item_id,
        "timestamp": datetime.now().isoformat(),
        "type": event_type,
        "asset": asset,
        "score_before": score_before,
        "score_after": score_after,
        "delta_score": round(score_after - score_before, 4),
        "delta_weight": round(delta_weight, 6),
        "delta_index_variance": round(delta_index_variance, 8),
        "exceeds_threshold": abs(score_after - score_before) >= threshold,
        "threshold": threshold,
        "library_source": library_source,
        "rebalance_recommended": abs(score_after - score_before) >= threshold,
        "awaiting_user_approval": True,
        "user_note": None,
    }
    stack["stack"].append(item)
    _save_stack(stack)
    print(f"[stack] pushed: {item_id} ({asset}, Δscore={item['delta_score']:.2f})")

    # Remind if stack is large
    if stack["stack_size"] >= stack.get("reminder_threshold", 50):
        print(f"[stack] ⚠️  {stack['stack_size']} items pending review. Consider a review session.")

    return item_id


def commit_item(item_id: str, user_note: str = "") -> dict:
    """Mark a stack item as committed (user approved). Returns the item."""
    stack = _load_stack()
    for item in stack["stack"]:
        if item["id"] == item_id:
            item["awaiting_user_approval"] = False
            item["stack_state"] = "committed"
            item["user_note"] = user_note
            _save_stack(stack)
            print(f"[stack] committed: {item_id}")
            return item
    raise ValueError(f"Item {item_id} not found in stack.")


def discard_item(item_id: str) -> dict:
    """Remove a stack item without writing to vault. Returns the discarded item."""
    stack = _load_stack()
    for i, item in enumerate(stack["stack"]):
        if item["id"] == item_id:
            discarded = stack["stack"].pop(i)
            discarded["stack_state"] = "discarded"
            _save_stack(stack)
            print(f"[stack] discarded: {item_id}")
            return discarded
    raise ValueError(f"Item {item_id} not found in stack.")


def get_stack_summary() -> dict:
    stack = _load_stack()
    return {
        "size": stack["stack_size"],
        "last_updated": stack["last_updated"],
        "items": [
            {"id": i["id"], "asset": i.get("asset"), "type": i["type"], "timestamp": i["timestamp"]}
            for i in stack["stack"]
        ],
    }
