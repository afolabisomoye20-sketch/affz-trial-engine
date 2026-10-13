"""
Performance logging and learning loop for Affz Trial Engine.
Tracks which variations perform well so the system can improve recommendations.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict
from models.data_models import Variation


PERF_FILE = Path("/workspace/artifacts/affz_trial_engine/data/performance.json")


def log_performance(variation_id: str, views: int, retention: float = 0.0,
                    follows: int = 0, graduated: bool = False, notes: str = ""):
    """Log performance metrics for a variation."""
    data = load_performance()
    data[variation_id] = {
        "views": views,
        "retention": retention,
        "follows": follows,
        "graduated": graduated,
        "notes": notes,
        "logged_at": datetime.utcnow().isoformat(),
    }
    save_performance(data)
    return data[variation_id]


def load_performance() -> Dict:
    if PERF_FILE.exists():
        with open(PERF_FILE) as f:
            return json.load(f)
    return {}


def save_performance(data: Dict):
    PERF_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PERF_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_top_performers(min_views: int = 1000, limit: int = 10) -> List[dict]:
    """Return the best performing variations."""
    data = load_performance()
    scored = []
    for vid, metrics in data.items():
        score = metrics.get("views", 0) * 0.5 + metrics.get("follows", 0) * 100 + (1000 if metrics.get("graduated") else 0)
        if metrics.get("views", 0) >= min_views:
            scored.append({"id": vid, "score": score, **metrics})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:limit]


def get_winning_patterns() -> Dict:
    """Analyze logged performance to find patterns (simple version)."""
    data = load_performance()
    if not data:
        return {"message": "No performance data yet. Log results after posting Trial Reels."}

    # Placeholder analysis — expand later with full variation data
    total = len(data)
    graduated = sum(1 for m in data.values() if m.get("graduated"))
    avg_views = sum(m.get("views", 0) for m in data.values()) / max(total, 1)

    return {
        "total_logged": total,
        "graduated_count": graduated,
        "avg_views": round(avg_views, 0),
        "recommendation": "Continue testing transform_years and photobooth_max. Log more results to improve this."
    }
