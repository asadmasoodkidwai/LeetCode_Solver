"""Daily entry point: plan the day, wait a bit, submit, log.

Usage:
  python daily.py --dry-run              # print today's plan, submit nothing
  python daily.py --dry-run --seed 7     # preview a different random day
  python daily.py --check-login          # verify your cookies work
  python daily.py                        # the real run (use this in the scheduler)
  python daily.py --no-delay             # real run without random waits (testing)
"""
import argparse
import json
import random
import time
from datetime import date

import config as C
from logger import log_submission, seen_slugs
from planner import generate_day, print_plan, solution_path


def plan_file(day):
    return C.LOG_DIR / f"plan_{day.isoformat()}.json"


def load_or_create_plan(day):
    """The plan is saved so a rerun (or crash recovery) continues the same day's plan."""
    f = plan_file(day)
    if f.exists():
        return json.loads(f.read_text())
    plan = generate_day(seed=day.toordinal(), history=seen_slugs())
    C.LOG_DIR.mkdir(exist_ok=True)
    f.write_text(json.dumps(plan, indent=2))
    return plan


def save_plan(day, plan):
    plan_file(day).write_text(json.dumps(plan, indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--no-delay", action="store_true")
    ap.add_argument("--check-login", action="store_true")
    args = ap.parse_args()

    if args.check_login:
        from submitter import LeetCodeClient
        ok, name = LeetCodeClient().check_login()
        print(f"Logged in as {name}" if ok else "Not logged in: refresh your cookies.")
        return

    today = date.today()

    if args.dry_run:
        seed = args.seed if args.seed is not None else today.toordinal()
        plan = generate_day(seed=seed, history=seen_slugs())
        print_plan(plan, f"[dry run] LeetCode plan for {today} (seed {seed}):")
        return

    plan = load_or_create_plan(today)
    print_plan(plan, f"LeetCode plan for {today}:")
    pending = [p for p in plan if not p["done"]]
    if not pending:
        print("Nothing left to do today.")
        return

    from submitter import LeetCodeClient
    client = LeetCodeClient()
    ok, name = client.check_login()
    if not ok:
        raise SystemExit("Not logged in: refresh LEETCODE_SESSION / LEETCODE_CSRF.")
    print(f"Logged in as {name}")

    if not args.no_delay:
        wait = random.uniform(0, C.MAX_START_DELAY_MINUTES * 60)
        print(f"Waiting {wait / 60:.0f} min before starting...")
        time.sleep(wait)

    for i, item in enumerate(pending):
        path = solution_path(item["slug"], item["language"], item["level"])
        if not path.exists():
            print(f"skip {item['problem']}: missing {path.name}")
            item["done"] = True
            save_plan(today, plan)
            continue
        try:
            verdict = client.submit(item["slug"], item["language"], path.read_text())
        except Exception as e:                       # network/403/etc.: log and move on
            verdict = f"Error: {e}"
        print(f"{item['problem']} ({item['language']}, {item['level']}): {verdict}")
        log_submission(item, path, verdict)
        item["done"] = True
        save_plan(today, plan)
        if i < len(pending) - 1 and not args.no_delay:
            time.sleep(random.uniform(C.MIN_GAP_SECONDS, C.MAX_GAP_SECONDS))


if __name__ == "__main__":
    main()
