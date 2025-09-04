import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes: Read + Send
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly",
          "https://www.googleapis.com/auth/gmail.send"]

TOKEN_FILE = "token.pickle"
CREDENTIALS_FILE = "credentials.json"
def gmail_authenticate():
    """Authenticate the user with Gmail API and return a service object."""
    creds = None

    # Load saved credentials
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    # Refresh or request login if no valid creds
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError("⚠️ Gmail credentials.json not found!")
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save new credentials
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    # Build Gmail API service
    service = build("gmail", "v1", credentials=creds)
    return service

def get_gmail_service():
    """Authenticate and return Gmail API service."""
    creds = None
    token_path = "token.pickle"

    # Load existing token if available
    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)

    # If no valid credentials, go through login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    # Build Gmail API service
    service = build("gmail", "v1", credentials=creds)
    return service


def fetch_last_n_emails(service, n=50):
    """Fetch last N emails from Gmail inbox."""
    results = service.users().messages().list(
        userId="me", maxResults=n, labelIds=["INBOX"]
    ).execute()
    messages = results.get("messages", [])

    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        headers = msg_data["payload"]["headers"]

        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "")
        snippet = msg_data.get("snippet", "")

        emails.append({
            "id": msg["id"],
            "sender": sender,
            "subject": subject,
            "body": snippet
        })

    return emails
