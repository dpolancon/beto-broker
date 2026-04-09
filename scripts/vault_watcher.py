"""
vault_watcher.py — Living System Prompt
========================================
Watches /vault for .md file saves and syncs YAML frontmatter → companion .json.
Keeps the human-readable node and the machine-readable node in sync.

Run as a VS Code task or background process:
    python scripts/vault_watcher.py
"""

import json
import time
import re
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

VAULT_ROOT = Path(__file__).parent.parent / "vault"


def parse_frontmatter(md_path: Path) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    content = md_path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    import yaml
    try:
        return yaml.safe_load(match.group(1)) or {}
    except Exception:
        return {}


def sync_to_json(md_path: Path):
    """Write frontmatter of md_path to a companion .json file."""
    frontmatter = parse_frontmatter(md_path)
    if not frontmatter:
        return
    json_path = md_path.with_suffix(".json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(frontmatter, f, indent=2, default=str)
    print(f"[watcher] synced: {md_path.name} → {json_path.name}")


class VaultHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix == ".md":
            sync_to_json(path)

    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix == ".md":
            sync_to_json(path)


if __name__ == "__main__":
    print(f"[watcher] Watching vault: {VAULT_ROOT}")
    observer = Observer()
    observer.schedule(VaultHandler(), str(VAULT_ROOT), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
