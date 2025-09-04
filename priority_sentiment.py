# priority_sentiment.py
from transformers import pipeline

# Sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Keywords to determine urgency
URGENT_KEYWORDS = ["immediately", "urgent", "critical", "cannot access", "asap", "problem", "help"]

# priority_sentiment.py
def detect_priority_sentiment(subject, body):
    """Detects priority, sentiment, and extracts metadata info."""
    # Priority detection
    urgent_keywords = ["immediately", "urgent", "critical", "cannot access"]
    priority = "Urgent" if any(word in body.lower() for word in urgent_keywords) else "Normal"

    # Simple sentiment analysis
    positive_words = ["thanks", "thank you", "great", "good"]
    negative_words = ["problem", "issue", "angry", "frustrated", "bad"]
    sentiment = "Positive" if any(word in body.lower() for word in positive_words) else \
                "Negative" if any(word in body.lower() for word in negative_words) else "Neutral"

    # Extract metadata info
    info = {
        "keywords": [word for word in body.split() if len(word) > 5],
        "word_count": len(body.split())
    }

    return priority, sentiment, info

