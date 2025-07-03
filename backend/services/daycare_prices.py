# File: backend/services/daycare_prices.py

def compute_total_fee(num_days: int, feed_once=False, feed_twice=False, feed_thrice=False) -> int:
    if feed_once:
        feed_cost = 85
    elif feed_twice:
        feed_cost = 170
    elif feed_thrice:
        feed_cost = 255
    else:
        feed_cost = 0
    return num_days * (350 + feed_cost)