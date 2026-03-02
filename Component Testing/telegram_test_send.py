import requests

BOT_TOKEN = "8596891202:AAG00Iue-MzUHxQSYu9KwwFiHhBzDinvqUM"
CHAT_ID = "7632007425"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": "🚀 Test message from AI News Engine"
}

response = requests.post(url, data=payload)

print(response.json())