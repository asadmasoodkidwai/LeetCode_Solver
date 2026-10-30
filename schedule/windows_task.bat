@echo off
REM Windows: run once (edit the path first) to create a daily 09:00 task.
REM daily.py then waits a random 0-180 min on its own.
schtasks /create /tn "LeetCodeDaily" /sc daily /st 09:00 /tr "cmd /c cd /d C:\path\to\leetcode_planner && python daily.py >> logs\task.log 2>&1"
