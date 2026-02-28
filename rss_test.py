import feedparser

rss_url = "https://feeds.feedburner.com/TheHackersNews"

print("Fetching RSS feed...\n")

feed = feedparser.parse(rss_url)

if feed.bozo:
    print("Error reading feed.")
else:
    print("Latest Articles:\n")
    
    for i, entry in enumerate(feed.entries[:5], start=1):
        print(f"{i}. {entry.title}")
        print(f"   Link: {entry.link}")
        print(f"   Published: {entry.published}")
        print("-" * 60)