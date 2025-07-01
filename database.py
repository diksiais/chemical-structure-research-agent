import sqlite3
import os
from datetime import datetime, timezone

DB_PATH = "chemical_research_agent/data/chemicals.db"

def initialize_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chemicals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_name TEXT,
                matched_name TEXT,
                cid TEXT,
                image_url TEXT,
                searched_at TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_searched_at ON chemicals(searched_at DESC)
        """)
        conn.commit()

def save_chemical(input_name, matched_name, cid, image_url):
    initialize_db()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO chemicals (input_name, matched_name, cid, image_url, searched_at)
                VALUES (?, ?, ?, ?, ?)
            """, (input_name, matched_name, cid, image_url, datetime.now(timezone.utc)))
            conn.commit()
    except Exception as e:
        print(f"[ERROR] Failed to save chemical: {e}")

def load_history(limit=10):
    if not os.path.exists(DB_PATH):
        return []
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT input_name, cid, searched_at FROM chemicals
                ORDER BY searched_at DESC
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"[ERROR] Failed to load history: {e}")
        return []

def clear_history():
    if not os.path.exists(DB_PATH):
        return
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM chemicals")
            conn.commit()
    except Exception as e:
        print(f"[ERROR] Failed to clear history: {e}")
