@echo off
cd /d "C:\Users\ds-ga\Documents\automations\strava club download"
"C:\Users\ds-ga\Documents\automations\strava club download\.venv\Scripts\python.exe" "C:\Users\ds-ga\Documents\automations\strava club download\master_sync.py" >> "C:\Users\ds-ga\Documents\automations\strava club download\daily_sync.log" 2>&1
