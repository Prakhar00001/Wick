import aiosqlite
import json
from typing import List
from wick.core.models import EvaluationResult

class RunStore:
    def __init__(self, db_path: str = ".wick.db"):
        self.db_path = db_path

    async def initialize(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS runs (
                    run_id TEXT PRIMARY KEY,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    config_hash TEXT,
                    is_baseline BOOLEAN DEFAULT 0
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    run_id TEXT,
                    example_id TEXT,
                    success BOOLEAN,
                    scores_json TEXT,
                    target_output TEXT,
                    FOREIGN KEY(run_id) REFERENCES runs(run_id)
                )
            """)
            await db.commit()

    async def save_run(self, run_id: str, results: List[EvaluationResult]):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("INSERT INTO runs (run_id) VALUES (?)", (run_id,))
            
            rows = [
                (
                    run_id, 
                    res.example.id, 
                    res.success, 
                    json.dumps([s.model_dump() for s in res.scores]),
                    str(res.target_result.output)
                )
                for res in results
            ]
            
            await db.executemany(
                "INSERT INTO results (run_id, example_id, success, scores_json, target_output) VALUES (?, ?, ?, ?, ?)",
                rows
            )
            await db.commit()