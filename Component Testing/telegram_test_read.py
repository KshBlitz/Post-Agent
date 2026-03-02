import requests

BOT_TOKEN = "8596891202:AAG00Iue-MzUHxQSYu9KwwFiHhBzDinvqUM"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

response = requests.get(url)
data = response.json()

print(data)