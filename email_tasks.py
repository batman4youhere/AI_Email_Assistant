import os
import time
import sqlite3
import pandas as pd
from gmail_utils import fetch_last_n_emails
from priority_sentiment import detect_priority_sentiment
from gmail_utils import gmail_authenticate
DB_FILE = "runtime_emails.db"

STOP_FILE = "stop_flag.txt"
RECHECK_INTERVAL = 30



def init_db():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print("🗑️ Old database removed.")

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id TEXT PRIMARY KEY,
            sender TEXT,
            subject TEXT,
            body TEXT,
            priority TEXT,
            sentiment TEXT,
            info TEXT,
            ai_reply TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Fresh runtime database created.")

def get_all_emails():
    """Fetch all emails from the database as a Pandas DataFrame."""
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM emails", conn)
    conn.close()
    return df

DB_FILE = "runtime_emails.db"

def create_runtime_db():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print("🗑️ Old database removed.")

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # ✅ Add ai_reply column from the start
    c.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id TEXT PRIMARY KEY,
            sender TEXT,
            subject TEXT,
            body TEXT,
            priority TEXT,
            sentiment TEXT,
            info TEXT,
            ai_reply TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Fresh runtime database created.")

def save_email_to_db(email):
    """Save a single email to the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
    '''INSERT OR IGNORE INTO emails 
       (id, sender, subject, body, priority, sentiment, info, ai_reply)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
    (
        email['id'],
        email['sender'],
        email['subject'],
        email['body'],
        email.get('priority'),
        email.get('sentiment'),
        str(email.get('info')),   # store as string if dict
        email.get('ai_reply')     # 👈 matches the new column
    )
)

    conn.commit()
    conn.close()


def fetch_emails(service, fetch_count=50):
    """Fetch last N emails from Gmail and store them in DB."""
    print(f"=== Fetching the last {fetch_count} emails ===")
    emails = fetch_last_n_emails(service, fetch_count)

    for email in emails:
        priority, sentiment, info = detect_priority_sentiment(
            email["subject"], email["body"]
        )
        email["priority"] = priority
        email["sentiment"] = sentiment
        email["info"] = info
        email["reply"] = None

        save_email_to_db(email)

    print(f"✅ {len(emails)} emails fetched and stored.")


def generate_replies():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # ✅ look for emails that don’t yet have an ai_reply
    c.execute("SELECT id, subject, body FROM emails WHERE ai_reply IS NULL")
    emails = c.fetchall()

    if not emails:
        print("No new emails to generate replies for.")
        conn.close()
        return

    for email_id, subject, body in emails:
        # Here you call your OpenAI function
        reply = f"AI-generated reply for subject: {subject}"  # placeholder

        c.execute("UPDATE emails SET ai_reply = ? WHERE id = ?", (reply, email_id))
        conn.commit()
        print(f"✅ Reply generated for email {email_id}")

    conn.close()

import sqlite3

DB_FILE = "runtime_emails.db"

def update_ai_reply(email_id, reply_text):
    """Update AI reply text for a given email ID."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE emails SET reply = ? WHERE id = ?", (reply_text, email_id))
    conn.commit()
    conn.close()
    return True
def main():
    service = gmail_authenticate()

    # Reset DB
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    print("🗑️ Old database removed.")

    init_db()  # 🔹 Create schema before inserting
    print("✅ Fresh runtime database created.")

    while True:
        if os.path.exists(STOP_FILE):
            print("🛑 Stop flag detected. Shutting down gracefully...")
            os.remove(STOP_FILE)
            break

        print("=== Fetching the last 50 emails ===")
        fetch_emails(service, fetch_count=50)
        generate_replies()

        print("⏳ Waiting before next cycle...")
        time.sleep(RECHECK_INTERVAL)