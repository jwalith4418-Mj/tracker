"""Append today's per-target totals from a wheelgap scan to the history file (one entry per day).

    python scripts/update_history.py data/coverage.json data/history.json

The full scan is replaced each night; the history keeps only the small summaries, so the
site can draw coverage over time without the repo growing by a full scan every day.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def update(coverage_path: Path, history_path: Path) -> dict:
    scan = json.loads(coverage_path.read_text(encoding="utf-8"))
    entry = {
        "date": scan["generated"][:10],
        "wheelgap": scan["wheelgap"],
        "packages": len(scan["packages"]),
        "summary": scan["summary"],
    }
    history = json.loads(history_path.read_text(encoding="utf-8")) if history_path.exists() else []
    history = [h for h in history if h["date"] != entry["date"]] + [entry]
    history.sort(key=lambda h: h["date"])
    history_path.write_text(json.dumps(history, separators=(",", ":")) + "\n", encoding="utf-8")
    return entry


if __name__ == "__main__":
    coverage, history = (Path(p) for p in sys.argv[1:3])
    entry = update(coverage, history)
    print(f"history: {entry['date']}, {entry['packages']} packages, {len(entry['summary'])} targets")
