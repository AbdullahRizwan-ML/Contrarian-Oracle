"""Track LLM token usage across analysis runs."""
from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime
from typing import Dict


class TokenTracker:
    """Track token usage per analysis run."""

    def __init__(self, log_file: str = "data/token_usage.json"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.current_run: Dict = {}

    def start_run(self, ticker: str) -> None:
        """Start tracking a new analysis run."""
        self.current_run = {
            "ticker": ticker,
            "timestamp": datetime.now().isoformat(),
            "agents": {},
            "total_tokens": 0
        }

    def log_agent(self, agent_name: str, tokens: int) -> None:
        """Log tokens used by an agent."""
        self.current_run["agents"][agent_name] = tokens
        self.current_run["total_tokens"] += tokens

    def end_run(self) -> None:
        """Save the completed run."""
        if not self.log_file.exists():
            data = {"runs": []}
        else:
            with open(self.log_file, "r") as f:
                data = json.load(f)

        data["runs"].append(self.current_run)

        # Keep only last 100 runs
        data["runs"] = data["runs"][-100:]

        with open(self.log_file, "w") as f:
            json.dump(data, f, indent=2)

    def get_summary(self) -> Dict:
        """Get token usage summary."""
        if not self.log_file.exists():
            return {"total_runs": 0, "avg_tokens": 0, "total_tokens": 0}

        with open(self.log_file, "r") as f:
            data = json.load(f)

        runs = data.get("runs", [])
        if not runs:
            return {"total_runs": 0, "avg_tokens": 0, "total_tokens": 0}

        total_tokens = sum(r.get("total_tokens", 0) for r in runs)
        return {
            "total_runs": len(runs),
            "avg_tokens": total_tokens // len(runs),
            "total_tokens": total_tokens,
            "last_run": runs[-1] if runs else None
        }


# Global tracker
token_tracker = TokenTracker()
