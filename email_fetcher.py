import time
from email_fetcher import create_runtime_db, fetch_emails
from generate_responses import generate_all_responses
from gmail_utils import gmail_authenticate
import threading
import streamlit.cli as stcli
import sys
import os

CHECK_INTERVAL = 30  # seconds

def continuous_loop(service):
    while True:
        print("\n=== Fetching New Emails ===")
        fetch_emails(service)  # fetch new emails
        print("=== Generating AI Replies ===")
        generate_all_responses()  # generate AI replies for new emails
        print(f"⏱ Waiting {CHECK_INTERVAL} seconds before next check...")
        time.sleep(CHECK_INTERVAL)

def main():
    print("🔹 Authenticating OpenAI key & Gmail...")
    service = gmail_authenticate()
    print("✅ Gmail authentication complete.")

    print("🗑️ Removing old runtime database...")
    create_runtime_db()  # creates a fresh runtime database
    print("✅ Fresh runtime database created.")

    # Fetch emails immediately on startup
    fetch_emails(service)
    generate_all_responses()

    # Start continuous fetch in a separate thread
    t = threading.Thread(target=continuous_loop, args=(service,), daemon=True)
    t.start()

    print("\n🚀 Launching Streamlit Dashboard...")
    # Launch dashboard in a separate process
    os.system("streamlit run dashboard.py")

if __name__ == "__main__":
    main()
