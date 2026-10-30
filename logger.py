"""CSV log of every submission, plus helpers that read it back."""
import csv
from datetime import datetime

from config import LOG_DIR, LOG_FILE

FIELDS = ["date", "time", "problem", "slug", "difficulty", "language", "level", "file", "verdict"]


def log_submission(item, path, verdict):
    LOG_DIR.mkdir(exist_ok=True)
    new_file = not LOG_FILE.exists()
    now = datetime.now()
    with LOG_FILE.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new_file:
            w.writeheader()
        w.writerow({
            "date": now.date().isoformat(),
            "time": now.strftime("%H:%M:%S"),
            "problem": item["problem"],
            "slug": item["slug"],
            "difficulty": item["difficulty"],
            "language": item["language"],
            "level": item["level"],
            "file": str(path),
            "verdict": verdict,
        })


def read_log():
    if not LOG_FILE.exists():
        return []
    with LOG_FILE.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def seen_slugs():
    """Slugs already submitted at some point; the planner prefers unseen ones."""
    return {row["slug"] for row in read_log()}
