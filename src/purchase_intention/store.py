from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


class PredictionStore:
    def __init__(self, path: str | Path = "data/purchase_intention.db"):
        self.path = Path(path); self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as connection:
            connection.execute("CREATE TABLE IF NOT EXISTS predictions (id INTEGER PRIMARY KEY, created_at TEXT, input_json TEXT, result_json TEXT)")

    def record(self, values: dict, result: dict) -> None:
        with sqlite3.connect(self.path) as connection:
            connection.execute("INSERT INTO predictions(created_at,input_json,result_json) VALUES(?,?,?)", (datetime.now(timezone.utc).isoformat(), json.dumps(values), json.dumps(result)))