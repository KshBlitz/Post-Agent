import requests
import time

BOT_TOKEN = "8596891202:AAG00Iue-MzUHxQSYu9KwwFiHhBzDinvqUM"
CHAT_ID = "7632007425"

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ---- Engine 1 Simulation: Send Options ----
def send_options():
    message = """
📰 Daily News Options:

1️⃣ Article One (Fake Summary)
2️⃣ Article Two (Fake Summary)
3️⃣ Article Three (Fake Summary)

Reply with 1, 2, or 3.
"""
    requests.post(f"{BASE_URL}/sendMessage", data={
        "chat_id": CHAT_ID,
        "text": message
    })

# ---- Engine 2 Simulation: Read Latest Reply ----
def get_latest_reply():
    response = requests.get(f"{BASE_URL}/getUpdates")
    data = response.json()

    if not data["result"]:
        return None

    # Get latest message only
    latest_update = data["result"][-1]

    if "message" in latest_update and "text" in latest_update["message"]:
        return latest_update["message"]["text"]

    return None


if __name__ == "__main__":
    print("Sending options to Telegram...")
    send_options()

    print("Waiting for reply...")
    time.sleep(10)  # Give you time to reply

    reply = get_latest_reply()

    if reply in ["1", "2", "3"]:
        print(f"✅ You selected option {reply}")
    else:
        print("❌ No valid selection detected.")