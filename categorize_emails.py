from transformers import pipeline

# Load sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    if not text:
        return "Neutral"
    result = sentiment_analyzer(text)[0]
    return result['label']  # Returns POSITIVE, NEGATIVE, NEUTRAL
