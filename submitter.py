"""Sends solution files to LeetCode using your logged-in session cookies.

These are the unofficial endpoints the website itself uses; they can change without notice.
"""
import os
import time

import requests

from config import ROOT, LEETCODE_LANG

BASE = "https://leetcode.com"


def load_env():
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


class LeetCodeClient:
    def __init__(self):
        load_env()
        try:
            session, csrf = os.environ["LEETCODE_SESSION"], os.environ["LEETCODE_CSRF"]
        except KeyError:
            raise SystemExit("Missing LEETCODE_SESSION / LEETCODE_CSRF. See .env.example.")
        self.s = requests.Session()
        self.s.cookies.update({"LEETCODE_SESSION": session, "csrftoken": csrf})
        self.s.headers.update({
            "x-csrftoken": csrf,
            "Referer": BASE,
            "Origin": BASE,
            "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                           "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"),
        })
        self._qid = {}

    def _graphql(self, query, variables=None):
        r = self.s.post(f"{BASE}/graphql", json={"query": query, "variables": variables or {}})
        r.raise_for_status()
        return r.json()

    def check_login(self):
        data = self._graphql("{ userStatus { isSignedIn username } }")
        status = data.get("data", {}).get("userStatus", {})
        return status.get("isSignedIn", False), status.get("username")

    def question_id(self, slug):
        if slug not in self._qid:
            data = self._graphql(
                "query q($s:String!){question(titleSlug:$s){questionId}}", {"s": slug})
            self._qid[slug] = data["data"]["question"]["questionId"]
        return self._qid[slug]

    def submit(self, slug, language, code, retries=3):
        payload = {
            "lang": LEETCODE_LANG[language],
            "question_id": self.question_id(slug),
            "typed_code": code,
        }
        headers = {"Referer": f"{BASE}/problems/{slug}/"}
        for attempt in range(retries):
            r = self.s.post(f"{BASE}/problems/{slug}/submit/", json=payload, headers=headers)
            if r.status_code == 429:                 # rate limited: back off and retry
                time.sleep(60 * (attempt + 1))
                continue
            r.raise_for_status()
            return self._poll(r.json()["submission_id"])
        return "Rate limited"

    def _poll(self, sub_id):
        for _ in range(30):
            time.sleep(2)
            res = self.s.get(f"{BASE}/submissions/detail/{sub_id}/check/").json()
            if res.get("state") == "SUCCESS":
                return res.get("status_msg", "Unknown")
        return "Timed out"
