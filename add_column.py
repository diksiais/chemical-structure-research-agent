import sqlite3

DB_PATH = "chemical_research_agent/data/chemicals.db"

def add_searched_at_column():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("ALTER TABLE chemicals ADD COLUMN searched_at TIMESTAMP")
            print("✅ Column 'searched_at' added successfully.")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
            print("ℹ️ Column 'searched_at' already exists.")
        else:
            print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    add_searched_at_column()
