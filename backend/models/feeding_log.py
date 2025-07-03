from datetime import datetime

class FeedingLog:
    """
    Represents a feeding log entry for a pet.
    """

    def __init__(self, pet_id: int, start_date: str, num_days: int,
                 feed_once=False, feed_twice=False, feed_thrice=False, notes=""):
        self.pet_id = pet_id
        self.start_date = start_date  # Format: YYYY-MM-DD
        self.num_days = num_days
        self.feed_once = feed_once
        self.feed_twice = feed_twice
        self.feed_thrice = feed_thrice
        self.notes = notes

    def to_dict(self):
        return {
            "pet_id": self.pet_id,
            "start_date": self.start_date,
            "num_days": self.num_days,
            "feed_once": int(self.feed_once),
            "feed_twice": int(self.feed_twice),
            "feed_thrice": int(self.feed_thrice),
            "notes": self.notes
        }

    def __str__(self):
        feeds = []
        if self.feed_once: feeds.append("Once")
        if self.feed_twice: feeds.append("Twice")
        if self.feed_thrice: feeds.append("Thrice")
        feeding_plan = ", ".join(feeds) if feeds else "No feeding"
        return f"{self.start_date} — Pet #{self.pet_id} for {self.num_days} day(s), Feeding: {feeding_plan}"
