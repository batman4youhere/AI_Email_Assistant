# AI Email Assistant

## Setup

1. Install dependencies:
pip install -r requirements.txt

markdown
Copy code

2. Place `credentials.json` in backend/ (Gmail API credentials)

3. Set OpenAI API key:
setx OPENAI_API_KEY "your_api_key_here"

markdown
Copy code

## Usage

1. Fetch and process emails:
python email_fetcher.py

markdown
Copy code

2. Generate AI replies:
python generate_responses.py

markdown
Copy code

3. Run dashboard:
python -m streamlit run dashboard.py

diff
Copy code

- Edit AI replies in the dashboard  
- Send emails directly using Gmail API  
- View analytics charts