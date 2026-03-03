# src/platform10/memory/memory_manager.py

"""
Persistent Memory Manager (SQLite Backend)

Provides:
- Episodic memory storage (decision history)
- Semantic knowledge storage
- Durable storage across restarts
"""

import sqlite3
import json
from typing import Any, Dict, List


class MemoryManager:
    """
    Unified persistent memory interface for Platform10 agents.
    """

    def __init__(self, db_path: str = "platform10_memory.db"):
        self.db_path = db_path
        self._initialize_database()

    # --------------------------------------------------
    # Database Setup
    # --------------------------------------------------

    def _initialize_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Episodic Memory Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS episodic_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            data TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Semantic Memory Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS semantic_memory (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)

        conn.commit()
        conn.close()

    # --------------------------------------------------
    # Episodic Memory
    # --------------------------------------------------

    def store_decision(self, event_type: str, payload: Dict[str, Any]) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO episodic_memory (event_type, data)
        VALUES (?, ?)
        """, (event_type, json.dumps(payload)))

        conn.commit()
        conn.close()

    def recall_recent(self, limit: int = 5) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT event_type, data, timestamp
        FROM episodic_memory
        ORDER BY timestamp DESC
        LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "event_type": row[0],
                "data": json.loads(row[1]),
                "timestamp": row[2],
            }
            for row in rows
        ]

    def recall_by_type(self, event_type: str) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT data, timestamp
        FROM episodic_memory
        WHERE event_type = ?
        ORDER BY timestamp DESC
        """, (event_type,))

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "data": json.loads(row[0]),
                "timestamp": row[1],
            }
            for row in rows
        ]

    # --------------------------------------------------
    # Semantic Memory
    # --------------------------------------------------

    def learn_pattern(self, key: str, value: Any):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT OR REPLACE INTO semantic_memory (key, value)
        VALUES (?, ?)
        """, (key, json.dumps(value)))

        conn.commit()
        conn.close()

    def recall_knowledge(self, key: str) -> Any:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT value FROM semantic_memory WHERE key = ?
        """, (key,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return json.loads(row[0])
        return None

    def knowledge_summary(self) -> Dict[str, Any]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT key, value FROM semantic_memory")
        rows = cursor.fetchall()
        conn.close()

        return {row[0]: json.loads(row[1]) for row in rows}