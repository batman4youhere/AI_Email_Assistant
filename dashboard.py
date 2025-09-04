import streamlit as st
import pandas as pd
import os
import sqlite3
from email_tasks import get_all_emails, update_ai_reply

DB_FILE = "runtime_emails.db"
STOP_FILE = "stop_flag.txt"

st.set_page_config(page_title="AI Email Assistant", layout="wide")
st.title("📧 AI Email Assistant Dashboard")

# --- Load emails from DB ---
def load_emails():
    if not os.path.exists(DB_FILE):
        return pd.DataFrame(columns=["id", "sender", "subject", "body", "priority", "sentiment", "info", "ai_reply"])
    
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM emails", conn)
    conn.close()
    return df

emails_df = load_emails()

# ✅ Handle empty case
if emails_df.empty:
    st.info("No emails found yet. Please wait while the system fetches emails...")
    st.stop()

# ✅ Ensure ai_reply column always exists
if "ai_reply" not in emails_df.columns:
    emails_df["ai_reply"] = ""

# --- Dashboard sections ---
st.subheader("📨 Latest Emails")
st.dataframe(emails_df, width="stretch")

st.subheader("📊 Insights")
st.write("Priority distribution:")
st.bar_chart(emails_df["priority"].value_counts())

st.write("Sentiment distribution:")
st.bar_chart(emails_df["sentiment"].value_counts())

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    selected_priority = st.selectbox(
        "Filter by Priority", ["All"] + sorted(emails_df["priority"].dropna().unique().tolist())
    )
    selected_sentiment = st.selectbox(
        "Filter by Sentiment", ["All"] + sorted(emails_df["sentiment"].dropna().unique().tolist())
    )

# Apply filters
filtered_df = emails_df.copy()
if selected_priority != "All":
    filtered_df = filtered_df[filtered_df["priority"] == selected_priority]
if selected_sentiment != "All":
    filtered_df = filtered_df[filtered_df["sentiment"] == selected_sentiment]

# Display emails in a table
st.subheader("📩 Emails")
st.dataframe(filtered_df[["id", "sender", "subject", "priority", "sentiment", "ai_reply"]], width="stretch")

# Edit replies section
st.subheader("✏️ Edit AI Replies")
for idx, row in filtered_df.iterrows():
    with st.expander(f"📨 {row['subject']} - from {row['sender']}"):
        st.markdown(f"**Sender:** {row['sender']}")
        st.markdown(f"**Subject:** {row['subject']}")
        st.markdown(f"**Body:** {row['body']}")
        st.markdown("---")

        new_reply = st.text_area("AI Suggested Reply", row.get("ai_reply", ""), key=f"reply_{row['id']}")
        if st.button("💾 Save Reply", key=f"save_{row['id']}"):
            update_ai_reply(row["id"], new_reply)
            st.success("✅ Reply saved!")

# --- One single Stop button (graceful shutdown) ---
st.sidebar.markdown("---")
if st.sidebar.button("🛑 Stop Application"):
    with open(STOP_FILE, "w") as f:
        f.write("stop")  # create stop flag
    st.success("🛑 Application stop requested. Backend will shut down shortly.")
    st.stop()
