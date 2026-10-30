"""Builds a random plan for one day."""
import random
from pathlib import Path

import config as C
from problems import PROBLEMS


def weighted_pick(weights, rng):
    return rng.choices(list(weights), weights=list(weights.values()), k=1)[0]


def solution_path(slug, language, level):
    prefix, ext = C.LANG_EXT[language]
    return C.SOLUTIONS_DIR / slug / f"{prefix}_{C.LEVEL_KEY[level]}.{ext}"


def has_solution(slug, language, level):
    return solution_path(slug, language, level).exists()


def _candidates(difficulty, language, level, used):
    out = [p for p in PROBLEMS if p[2] == difficulty and p[1] not in used]
    if C.REQUIRE_SOLUTION_FILES:
        out = [p for p in out if has_solution(p[1], language, level)]
    return out


def _resolve(difficulty, language, level, used):
    """Find candidates for the rolled combo; relax level, then language, if empty."""
    levels = [level] + [l for l in C.LEVEL_WEIGHTS[difficulty] if l != level]
    langs = [language] + [l for l in C.LANGUAGE_WEIGHTS if l != language]
    for lang in langs:
        for lv in levels:
            cands = _candidates(difficulty, lang, lv, used)
            if cands:
                return lang, lv, cands
    return None


def generate_day(seed=None, history=None):
    rng = random.Random(seed)
    history = history or set()
    budget = rng.randint(0, C.MAX_BUDGET)
    plan, used = [], set()
    attempts = 0

    while len(plan) < C.MAX_PROBLEMS and budget >= C.COST["Easy"] and attempts < 60:
        attempts += 1
        difficulty = weighted_pick(C.DIFFICULTY_WEIGHTS, rng)
        if C.COST[difficulty] > budget:
            difficulty = "Easy"          # can't afford it, fall back to the cheapest
        language = weighted_pick(C.LANGUAGE_WEIGHTS, rng)
        level = weighted_pick(C.LEVEL_WEIGHTS[difficulty], rng)

        resolved = _resolve(difficulty, language, level, used)
        if not resolved:
            continue
        language, level, cands = resolved

        unseen = [p for p in cands if p[1] not in history]
        title, slug, diff, topic = rng.choice(unseen or cands)
        used.add(slug)
        budget -= C.COST[diff]
        plan.append({
            "problem": title, "slug": slug, "difficulty": diff, "topic": topic,
            "language": language, "level": level, "done": False,
        })
    return plan


def print_plan(plan, header=""):
    if header:
        print(header)
    if not plan:
        print("  Rest day. No problems today.")
    for i, p in enumerate(plan, 1):
        flag = "x" if p.get("done") else " "
        print(f"  [{flag}] {i}. {p['problem']} [{p['difficulty']}, {p['topic']}] "
              f"-> {p['language']}, {p['level']}")
