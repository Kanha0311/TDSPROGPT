


### 📂 Directory structure

#### `/scraper/scrape_discourse.py`


import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = 'https://discourse.onlinedegree.iitm.ac.in'

def scrape_topic(topic_id):
    url = f"{BASE_URL}/t/{topic_id}.json"
    resp = requests.get(url)
    if resp.status_code != 200:
        return None
    data = resp.json()
    posts = []
    for post in data.get("post_stream", {}).get("posts", []):
        posts.append({
            "username": post["username"],
            "created_at": post["created_at"],
            "content": post["cooked"]
        })
    return posts

def scrape_multiple_topics(topic_ids):
    all_posts = []
    for tid in topic_ids:
        posts = scrape_topic(tid)
        if posts:
            all_posts.extend(posts)
            time.sleep(1)
    return all_posts

if __name__ == "__main__":
    topic_ids = [12345, 12346, 12347]  # Replace with actual topic IDs
    posts = scrape_multiple_topics(topic_ids)

    with open("../data/discourse_posts.json", "w") as f:
        json.dump(posts, f, indent=2)
