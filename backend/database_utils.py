# database_utils.py
import sqlite3

DB_FILE = "runtime.db"

def create_runtime_db():
    """Creates a fresh runtime database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS emails')
    c.execute('''
        CREATE TABLE emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            subject TEXT,
            body TEXT,
            priority TEXT,
            sentiment TEXT,
            info TEXT,
            reply TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_email_to_db(sender, subject, body, priority, sentiment, info):
    """Saves a single email record to the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO emails (sender, subject, body, priority, sentiment, info)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (sender, subject, body, priority, sentiment, str(info)))
    conn.commit()
    conn.close()
