# run_all.py
import time
import subprocess
from email_fetcher import create_runtime_db, fetch_emails
from generate_responses import generate_all_responses
from gmail_utils import gmail_authenticate

def main():
    print("🔹 Authenticating OpenAI key & Gmail...")
    service = gmail_authenticate()
    print("✅ Gmail authentication complete.")

    # Remove old database & create fresh runtime DB
    create_runtime_db()
    print("🗑️ Old database removed, ✅ Fresh runtime database created.\n")

    # Ask user recheck interval
    try:
        interval = int(input("Enter email recheck interval in seconds (default 30): ") or 30)
    except ValueError:
        interval = 30
    print(f"⏱ Rechecking emails every {interval} seconds...\n")

    # Launch Streamlit dashboard once
    try:
        subprocess.Popen(["streamlit", "run", "dashboard.py"])
        print("🚀 Streamlit dashboard launched!\n")
    except Exception as e:
        print(f"⚠️ Error launching dashboard: {e}")

    # Continuous loop
    while True:
        print("=== Fetching New Emails ===")
        try:
            fetch_emails(service, limit=50)
            print("✅ Emails fetched.")
        except Exception as e:
            print(f"⚠️ Error fetching emails: {e}")

        print("=== Generating AI Replies ===")
        try:
            generate_all_responses()
            print("✅ AI replies generated.\n")
        except Exception as e:
            print(f"⚠️ Error generating replies: {e}")

        print(f"Waiting {interval} seconds before checking again...\n")
        time.sleep(interval)

if __name__ == "__main__":
    main()
