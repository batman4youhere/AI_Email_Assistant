# 📧 AI-Powered Email Assistant

---

## Overview 
The AI-Powered Email Assistant is a tool designed to automate the handling of support emails. It:
- Fetches and filters support-related emails.
- Categorizes emails by sentiment and priority.
- Generates context-aware AI responses using OpenAI GPT.
- Displays emails and AI replies on a user-friendly Streamlit dashboard.
- Supports continuous monitoring and auto-updates.

---

## Features

### Email Retrieval & Filtering
- Fetch emails via Gmail API (OAuth 2.0)
- Filter emails containing keywords: `Support`, `Query`, `Request`, `Help`
- Extract sender, subject, body, date/time

### Categorization & Prioritization
- Sentiment Analysis: Positive / Neutral / Negative
- Priority Detection: Urgent / Not urgent
- Urgent emails appear at the top using a priority queue

### AI Response Generation
- Generates professional, context-aware replies
- Prioritizes urgent emails
- Uses RAG + Prompt Engineering for accurate responses

### Dashboard
- Built with Streamlit
- Shows emails, extracted info, AI responses, and analytics
- Interactive graphs for email trends and statuses

---
## 🚀 Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/batman4youhere/ai-email-assistant.git
cd ai-email-assistant
````

### 3. Install dependencies

```bash
pip install -r requirements.txt
```
### 4. Prerequisites
- Python 3.9+
- Google Cloud `credentials.json`
- OpenAI API key

### 5. Setup Gmail API

* Go to [Google Cloud Console](https://console.cloud.google.com/)
* Enable Gmail API
* Download `credentials.json` and place it in `backend Folder`
* On first run, it will create `token.json` 
* OpenAI API key using https://platform.openai.com/ or gemeni and Enter it after runnig code when its asked

### 6. Run the AI-Powered Email Assistant

cd backend
python run_all.py

## 🛑 Stopping the System

* Use the **Stop Application** button inside the dashboard.
* Or press `Ctrl+C` in terminal.

---
