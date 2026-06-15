from mastodon import Mastodon
import random
import os
import time
mastodon = Mastodon(
    access_token=os.getenv("MASTODON_TOKEN"),
    api_base_url="https://planet.moe"
)

def post_random_message():
    with open("posts.txt", "r", encoding="utf-8") as f:
        posts = [line.strip() for line in f if line.strip()]

    last_post = ""

    if os.path.exists("last_post.txt"):
        with open("last_post.txt", "r", encoding="utf-8") as f:
            last_post = f.read().strip()

    available_posts = [p for p in posts if p != last_post]

    if not available_posts:
        available_posts = posts

    message = random.choice(available_posts)

    mastodon.status_post(message)

    with open("last_post.txt", "w", encoding="utf-8") as f:
        f.write(message)

    print(f"투고 완료: {message}")

while True:
    post_random_message()

    print("3시간 대기 중...")

    time.sleep(10800)
