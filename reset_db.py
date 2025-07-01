import os
import sqlite3

DB_DIR = "chemical_research_agent/data"
DB_PATH = os.path.join(DB_DIR, "chemicals.db")

def reset_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("🗑️ Old database deleted.")
    else:
        print("ℹ️ No existing database found.")

    os.makedirs(DB_DIR, exist_ok=True)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chemicals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    input_name TEXT,
                    matched_name TEXT,
                    cas TEXT,
                    cid TEXT,
                    image_url TEXT,
                    searched_at TIMESTAMP
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_searched_at ON chemicals(searched_at DESC)")
            conn.commit()
        print("✅ New database created successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to reset database: {e}")

if __name__ == "__main__":
    reset_database()
