# AI-Powered Email Assistant

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

## Installation
First create credintials using 
Google Cloud console
https://console.cloud.google.com
then copy them to backend Folder 

then create 
- OpenAI API key using https://platform.openai.com/ or gemeni

### Prerequisites
- Python 3.9+
- Google Cloud `credentials.json`
- OpenAI API key

### Install Dependencies
```bash
pip install -r requirements.txt

### RUN
--python run_all.py
