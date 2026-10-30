"""All tunable settings live here."""
from pathlib import Path

ROOT = Path(__file__).parent
SOLUTIONS_DIR = ROOT / "solutions"
LOG_DIR = ROOT / "logs"
LOG_FILE = LOG_DIR / "submissions.csv"

# ---- Daily randomness -------------------------------------------------------
MAX_PROBLEMS = 5            # hard cap per day
MAX_BUDGET = 8              # daily effort budget is randint(0, MAX_BUDGET); 0 = rest day
COST = {"Easy": 1, "Medium": 2, "Hard": 4}   # harder problems burn the budget faster

# Tuned for a 3rd-semester Data Structures student. Shift toward Medium over time.
DIFFICULTY_WEIGHTS = {"Easy": 55, "Medium": 40, "Hard": 5}
LANGUAGE_WEIGHTS = {"C++": 60, "Python": 40}
LEVEL_WEIGHTS = {
    "Easy":   {"Brute force": 20, "Standard": 40, "Optimal & clean": 40},
    "Medium": {"Brute force": 35, "Standard": 45, "Optimal & clean": 20},
    "Hard":   {"Brute force": 70, "Standard": 25, "Optimal & clean": 5},
}

# ---- File naming ------------------------------------------------------------
LEVEL_KEY = {"Brute force": "brute", "Standard": "standard", "Optimal & clean": "optimal"}
LANG_EXT = {"C++": ("cpp", "cpp"), "Python": ("python", "py")}   # (file prefix, extension)
LEETCODE_LANG = {"C++": "cpp", "Python": "python3"}              # LeetCode's lang codes

# If True, only pick (problem, language, level) combos that have a solution file,
# so no slot in the day is wasted on a missing file.
REQUIRE_SOLUTION_FILES = True

# ---- Timing -----------------------------------------------------------------
MIN_GAP_SECONDS = 120       # gap between submissions: 2 min ...
MAX_GAP_SECONDS = 1500      # ... to 25 min
MAX_START_DELAY_MINUTES = 180   # random wait before the first submission of the day
