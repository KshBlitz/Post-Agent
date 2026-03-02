import requests
import feedparser
import json
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

BOT_TOKEN = "8596891202:AAG00Iue-MzUHxQSYu9KwwFiHhBzDinvqUM"
CHAT_ID = "7632007425"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

RSS_URL = "https://feeds.feedburner.com/TheHackersNews"

# -----------------------------
# Step 1: Fetch RSS
# -----------------------------
def fetch_rss():
    feed = feedparser.parse(RSS_URL)
    articles = []

    for entry in feed.entries[:5]:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published
        })

    return articles

# -----------------------------
# Step 2: Store JSON
# -----------------------------
def store_articles(articles):
    with open("data/today_feed.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=4)

# -----------------------------
# Step 3: Send Options
# -----------------------------
def send_options(articles):
    message = "📰 Daily News Options:\n\n"
    for i, article in enumerate(articles[:3], start=1):
        message += f"{i}️⃣ {article['title']}\n\n"

    message += "Reply with 1, 2, or 3."

    requests.post(f"{BASE_URL}/sendMessage", data={
        "chat_id": CHAT_ID,
        "text": message
    })

# -----------------------------
# Step 4: Get Latest Reply
# -----------------------------
def get_latest_reply():
    response = requests.get(f"{BASE_URL}/getUpdates")
    data = response.json()

    if not data["result"]:
        return None

    latest_update = data["result"][-1]

    if "message" in latest_update and "text" in latest_update["message"]:
        return latest_update["message"]["text"]

    return None

# -----------------------------
# Step 5: Fetch Full Article
# -----------------------------
def fetch_full_article(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")

    paragraphs = soup.find_all("p")
    article_text = "\n".join([p.get_text() for p in paragraphs])

    return article_text[:1000]  # limit for test

# -----------------------------
# MAIN FLOW
# -----------------------------
if __name__ == "__main__":
    print("Fetching RSS...")
    articles = fetch_rss()

    print("Storing JSON...")
    store_articles(articles)

    print("Sending options to Telegram...")
    send_options(articles)

    print("Waiting 15 seconds for reply...")
    time.sleep(15)

    reply = get_latest_reply()

    if reply in ["1", "2", "3"]:
        choice = int(reply)
        selected_article = articles[choice - 1]

        print(f"Selected: {selected_article['title']}")

        print("Fetching full article...")
        content = fetch_full_article(selected_article["link"])

        print("Sending dummy final content...")
        requests.post(f"{BASE_URL}/sendMessage", data={
            "chat_id": CHAT_ID,
            "text": f"📄 Dummy LinkedIn Post Preview:\n\n{content[:500]}"
        })

        print("Done.")
    else:
        print("No valid reply detected.")