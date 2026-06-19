"""
database.py
Handles all SQLite operations for the attendance system.
Creates the database and table if they don't exist.
"""

import sqlite3
from datetime import date, datetime


DB_NAME = "attendance.db"


def init_db():
    """
    Creates the attendance table if it doesn't already exist.
    Run this once when the app starts.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT NOT NULL,
            date      TEXT NOT NULL,
            time      TEXT NOT NULL,
            UNIQUE(name, date)   -- prevents duplicate entries for same person on same day
        )
    """)
    conn.commit()
    conn.close()


def mark_present(name: str):
    """
    Inserts an attendance record for today.
    If the person was already marked today, it does nothing (IGNORE).
    Returns True if a new record was inserted, False if already present.
    """
    today = str(date.today())                          # e.g. "2025-06-10"
    now   = datetime.now().strftime("%H:%M:%S")        # e.g. "09:32:15"

    conn   = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO attendance (name, date, time)
        VALUES (?, ?, ?)
    """, (name, today, now))

    inserted = cursor.rowcount == 1    # 1 = new row, 0 = already existed
    conn.commit()
    conn.close()
    return inserted


def get_today_records():
    """
    Returns a list of (name, time) tuples for today's attendance.
    """
    today  = str(date.today())
    conn   = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, time FROM attendance
        WHERE date = ?
        ORDER BY time ASC
    """, (today,))
    records = cursor.fetchall()
    conn.close()
    return records


def get_all_records():
    """
    Returns every record in the database as a list of dicts.
    Used by the export and dashboard features.
    """
    conn   = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, date, time FROM attendance ORDER BY date DESC, time ASC")
    rows    = cursor.fetchall()
    conn.close()
    return [{"Name": r[0], "Date": r[1], "Time": r[2]} for r in rows]