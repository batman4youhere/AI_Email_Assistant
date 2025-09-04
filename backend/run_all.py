import time
import subprocess
import os
from gmail_utils import gmail_authenticate
from email_tasks import init_db, fetch_emails, generate_replies
import signal

# Config
DB_FILE = "runtime_emails.db"
STOP_FILE = "stop_flag.txt"
RECHECK_INTERVAL = 30  # seconds


dashboard_process = None  # <-- track dashboard process

def launch_dashboard():
    """Launch Streamlit dashboard in a subprocess."""
    try:
        subprocess.Popen(
            ["python", "-m", "streamlit", "run", "dashboard.py"]
        )
        print("✅ Streamlit dashboard launched.")
    except FileNotFoundError:
        print("⚠️ Streamlit not found. Install it with: pip install streamlit")

def stop_dashboard():
    """Stop Streamlit dashboard if running."""
    global dashboard_process
    if dashboard_process and dashboard_process.poll() is None:
        dashboard_process.terminate()
        print("🛑 Streamlit dashboard stopped.")


def main():
    print("Device set to use cpu")

    # Initialize database
    init_db()

    # Authenticate Gmail
    service = gmail_authenticate()
    # ✅ Launch Streamlit dashboard
    launch_dashboard()
    # First fetch + generate
    print("=== Fetching the last 50 emails ===")
    fetch_emails(service, fetch_count=50)
    generate_replies()

    # Loop for continuous checking
    while True:
        # Check for stop flag
        if os.path.exists(STOP_FILE):
            print("🛑 Stop flag detected. Shutting down gracefully...")
            os.remove(STOP_FILE)  # cleanup
            break

        print("🔄 Rechecking for new emails...")
        fetch_emails(service, fetch_count=50)
        generate_replies()

        print(f"⏳ Waiting {RECHECK_INTERVAL} seconds before next cycle...")
        time.sleep(RECHECK_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("🛑 Stopped by user (Ctrl+C)")
