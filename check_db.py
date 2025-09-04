import sqlite3

def init_db():
    """Create emails table if it doesn't exist"""
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            subject TEXT,
            body TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def view_emails():
    # Initialize database/table
    init_db()

    # Connect and fetch rows
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    c.execute("SELECT * FROM emails")
    rows = c.fetchall()

    print("\n--- All Emails in Database ---")
    if rows:
        for row in rows:
            print(row)
    else:
        print("No emails found in the database.")

    conn.close()

if __name__ == "__main__":
    view_emails()
