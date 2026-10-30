"""Shows which (problem, language, level) solution files exist.

  python check_solutions.py            # full grid
  python check_solutions.py --missing  # only list what's missing
"""
import argparse

import config as C
from planner import has_solution
from problems import PROBLEMS


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--missing", action="store_true")
    args = ap.parse_args()

    combos = [(lang, lvl) for lang in C.LANGUAGE_WEIGHTS for lvl in C.LEVEL_KEY]
    total = have = 0
    print(f"{'problem':48} " + " ".join(f"{('cpp' if l == 'C++' else 'py')}-{C.LEVEL_KEY[v][:3]}" for l, v in combos))
    for title, slug, diff, _ in PROBLEMS:
        marks = [has_solution(slug, l, v) for l, v in combos]
        total += len(marks)
        have += sum(marks)
        if args.missing and all(marks):
            continue
        cells = " ".join(f"{'  ok ' if m else '  .  ':7}" for m in marks)
        print(f"{title[:40]:40} {diff:7} {cells}")
    print(f"\n{have}/{total} solution files present ({100 * have // total}%).")


if __name__ == "__main__":
    main()
