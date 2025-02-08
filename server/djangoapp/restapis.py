import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv("backend_url", default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    "sentiment_analyzer_url", default="http://localhost:5050/"
)


def get_request(endpoint, **kwargs):
    """Send a GET request to the backend."""
    params = "&".join(f"{key}={value}" for key, value in kwargs.items())
    request_url = f"{backend_url}{endpoint}?{params}"
    print(f"GET from {request_url}")

    try:
        response = requests.get(request_url)
        return response.json()
    except requests.RequestException as err:
        print(f"Network exception occurred: {err}")
        return None


def analyze_review_sentiments(text):
    """Analyze sentiment of a review text."""
    request_url = f"{sentiment_analyzer_url}analyze/{text}"

    try:
        response = requests.get(request_url)
        return response.json()
    except requests.RequestException as err:
        print(f"Network exception occurred: {err}")
        return None


def post_review(data_dict):
    """Send a POST request to insert a review."""
    request_url = f"{backend_url}/insert_review"

    try:
        response = requests.post(request_url, json=data_dict)
        return response.json()
    except requests.RequestException as err:
        print(f"Network exception occurred: {err}")
        return None
