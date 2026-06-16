import random

def make_lotto():
    numbers = sorted(random.sample(range(1, 46), 6))
    return "🎟️ 이번 로또 번호는 " + ", ".join(map(str, numbers))
