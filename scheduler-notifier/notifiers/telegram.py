import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def notify(message):
    requests.get(URL, params={'chat_id': CHAT_ID, 'text': message})
