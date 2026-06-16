import random

def make_lotto():
    numbers = sorted(random.sample(range(1, 46), 6))
    return "이번에는..." + ",".join(map(str, numbers)) + "번으로..어때?"
