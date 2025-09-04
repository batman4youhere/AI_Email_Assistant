import sqlite3
import openai
from config_loader import load_config
from config_loader import get_openai_key
import openai

openai.api_key = get_openai_key()


config = load_config()
openai.api_key = config.get("openai_api_key")


DB_FILE = "emails.db"
openai.api_key = get_openai_key()

def generate_reply(subject, body, priority, sentiment, info):
    """Generate AI reply using OpenAI GPT"""
    prompt = f"""
You are a helpful customer support assistant.
Email Subject: {subject}
Email Body: {body}
Priority: {priority}
Sentiment: {sentiment}
Additional Info: {info}

Write a professional and empathetic reply addressing the customer's needs.
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250
    )
    return response['choices'][0]['message']['content']

def generate_all_responses():
    """Generate replies for all emails that do not have a reply yet"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Select emails where AI reply is NULL
    c.execute("SELECT id, subject, body, priority, sentiment, info FROM emails WHERE ai_reply IS NULL")
    emails_to_reply = c.fetchall()

    if not emails_to_reply:
        print("No new emails to generate replies for.")
        conn.close()
        return

    for email in emails_to_reply:
        id_, subject, body, priority, sentiment, info = email
        reply = generate_reply(subject, body, priority, sentiment, info)
        
        # Update AI reply in DB
        c.execute("UPDATE emails SET ai_reply = ? WHERE id = ?", (reply, id_))
    
    conn.commit()
    conn.close()
    print(f"✅ Generated AI replies for {len(emails_to_reply)} new email(s).")
