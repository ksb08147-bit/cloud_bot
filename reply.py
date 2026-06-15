from mastodon import Mastodon
import json
import time
import re
import os
from dotenv import load_dotenv
load_dotenv("/root/cloud_bot/.env")

# =====================
# Mastodon 설정
# =====================
mastodon = Mastodon(
    access_token=os.getenv("MASTODON_TOKEN"),
    api_base_url="https://planet.moe"
)

# =====================
# replies.json 로드
# =====================
with open("replies.json", "r", encoding="utf-8") as f:
    replies = json.load(f)

# =====================
# HTML 제거
# =====================
def clean_text(text):
    return re.sub("<.*?>", "", text)

# =====================
# 멘션 처리 루프
# =====================
def check_mentions():
    seen = set()

    while True:
        try:
            notifications = mastodon.notifications()

            for n in notifications:
                if n["type"] != "mention":
                    continue

                status = n["status"]
                sid = status["id"]
                text = clean_text(status["content"])

                if sid in seen:
                    continue
                seen.add(sid)

                replied = False

                for key in replies:
                    if key in text:
                        reply = replies[key][0]  # 첫 번째 고정 or random으로 바꿔도 됨

                        mastodon.status_post(
                            status=reply,
                            in_reply_to_id=sid
                        )

                        print(f"💬 답장 ({key}): {reply}")
                        replied = True
                        break

                if not replied:
                    fallback = "..."
                    mastodon.status_post(
                        status=fallback,
                        in_reply_to_id=sid
                    )
                    print("💬 기본 답장")

        except Exception as e:
            print("❌ 멘션 오류:", e)

        time.sleep(10)


# =====================
# 실행
# =====================
if __name__ == "__main__":
    check_mentions()
