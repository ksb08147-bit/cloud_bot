from mastodon import Mastodon
from lotto import make_lotto
import json
import time
import re
import os
import random

mastodon = Mastodon(
    access_token=os.environ["MASTODON_TOKEN"],
    api_base_url="https://planet.moe"
)

with open("replies.json", "r", encoding="utf-8") as f:
    replies = json.load(f)

def clean_text(text):
    return re.sub("<.*?>", "", text)

# ⭐ 핵심: 마지막으로 처리한 notification id 저장
LAST_ID_FILE = "last_notif.txt"

def load_last_id():
    if os.path.exists(LAST_ID_FILE):
        with open(LAST_ID_FILE, "r") as f:
            return int(f.read().strip())
    return 0

def save_last_id(nid):
    with open(LAST_ID_FILE, "w") as f:
        f.write(str(nid))

def check_mentions():
    since_id = load_last_id()

    while True:
        try:
            notifications = mastodon.notifications(
                since_id=since_id
                )

            # 최신 → 오래된 순이라 뒤집어 처리
            notifications = list(reversed(notifications))

            for n in notifications:
                if n["type"] != "mention":
                    continue

                nid = int(n["id"])

                # 이미 처리한 건 스킵
                if since_id and nid <= since_id:
                    continue

                status = n["status"]
                sid = status["id"]
                text = clean_text(status["content"])

                replied = False

                if "로또번호" in text:
                    reply = make_lotto()

                    mastodon.status_post(
                        status=reply,
                        in_reply_to_id=sid
                    )

                    print(f"💬 답장 (로또번호): {reply}")
                    replied = True

                else:
                    print("TEXT RECEIVED:", text)
                    for key in replies:
                        print("CHECK:", key)
                        
                        if key in text:
                            print("MATCH:", key, replies[key])
                            reply = random.choice(replies[key])

                            mastodon.status_post(
                                status=reply,
                                in_reply_to_id=sid
                            )

                            print(f"💬 답장 ({key}): {reply}")
                            replied = True
                            break

                if not replied:
                    mastodon.status_post(
                        status="...",
                        in_reply_to_id=sid
                    )

                # ⭐ 마지막 처리 ID 갱신
                since_id = nid
                save_last_id(nid)

        except Exception as e:
            print("❌ 멘션 오류:", e)

        time.sleep(10)


if __name__ == "__main__":
    check_mentions()
