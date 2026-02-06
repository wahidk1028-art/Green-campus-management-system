import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("waste_log.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS waste_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            waste_type TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_waste(class_name):
    conn = sqlite3.connect("waste_log.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO waste_log (timestamp, waste_type) VALUES (?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), class_name)
    )
    conn.commit()
    conn.close()
