# LeetCode Daily Planner

Plans a random 0-5 LeetCode problems per day and (optionally) submits matching solution
files from your own `solutions/` folder to a LeetCode account.

## How the randomness works
- **Effort budget:** each day rolls a budget of 0-8. Easy costs 1, Medium 2, Hard 4, so harder
  problems use the budget up faster. Capped at 5 problems; a budget of 0 is a rest day.
- **Difficulty:** weighted for a 3rd-semester DSA student (mostly Easy, some Medium, rare Hard).
- **Language:** 60% C++, 40% Python.
- **Code level:** brute force / standard / optimal & clean, weighted by difficulty
  (Easy leans optimal, Hard leans brute force).
- The plan is seeded by the date and saved to `logs/plan_YYYY-MM-DD.json`, so reruns and
  crash recovery continue the same day's plan instead of re-rolling it.
- Problems you haven't submitted before are preferred over repeats.

All weights live in `config.py`.

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env        # then fill in the two cookie values
```
Get the cookies from your browser (DevTools > Application > Cookies > leetcode.com) while
logged into the account: `LEETCODE_SESSION` and `csrftoken` (put the latter in `LEETCODE_CSRF`).
Treat them like a password. They expire every few weeks.

## Commands
```bash
python daily.py --dry-run             # preview today's plan, submit nothing
python daily.py --dry-run --seed 7    # preview a different random day
python daily.py --check-login         # test your cookies
python daily.py                       # real run (waits randomly, submits, logs)
python daily.py --no-delay            # real run without waits (testing)
python check_solutions.py             # grid of which solution files exist
python check_solutions.py --missing   # only problems with gaps
```

## Solutions folder
```
solutions/<slug>/{cpp,python}_{brute,standard,optimal}.{cpp,py}
```
Five sample problems are included (30 files). With `REQUIRE_SOLUTION_FILES = True` the planner
only picks combos that have a file, so fill the folder gradually and the pool grows with it.
Files are submitted as-is; C++ files need `class Solution` as on LeetCode, and Python files
can use `List` etc. since LeetCode preloads `typing`.

Add problems by appending a row to `problems.py` and creating its folder.

## Scheduling
- Linux/macOS: see `schedule/crontab.example`
- Windows: edit the path in `schedule/windows_task.bat` and run it once

The scheduler fires at a fixed time; `daily.py` then waits a random 0-180 minutes, and
2-25 minutes between submissions (`config.py`).

## Log
Every submission is appended to `logs/submissions.csv`
(date, time, problem, slug, difficulty, language, level, file, verdict).

## Caveats
- LeetCode has no official submission API. These are the website's own endpoints and can change
  or be blocked (403s usually mean refresh cookies or Cloudflare filtering).
- Automated submissions violate LeetCode's Terms of Service. Accounts can be flagged or banned;
  only use an account you can afford to lose.
- Brute-force files may fail or time out on harder problems. That shows up as a failed verdict
  in the log, same as a real attempt.
