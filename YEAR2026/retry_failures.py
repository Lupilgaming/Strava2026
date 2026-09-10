import os
import sys
import csv
import time
import requests
from tqdm import tqdm
from fetch_single_user import (
    load_session, parse_activity_page, append_activity_to_csv,
    log_activity_status, CSV_FIELDNAMES, LOG_FIELDNAMES
)

def retry_failed_activities(log_csv: str = "activity_log.csv", activities_csv: str = "activities.csv"):
    if not os.path.exists(log_csv):
        print(f"[!] Log file '{log_csv}' not found. No failed activities to retry.")
        return

    # Read existing activities to avoid duplication
    existing_act_ids = set()
    if os.path.exists(activities_csv):
        with open(activities_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                aid = r.get("activity_id")
                if aid:
                    existing_act_ids.add(str(aid).strip())

    # Find failures
    failed_rows = []
    with open(log_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r.get("status") == "FAILURE":
                act_id = str(r.get("activity_id", "")).strip()
                if act_id and act_id not in existing_act_ids:
                    failed_rows.append(r)

    if not failed_rows:
        print(f"[OK] No failed activities found in '{log_csv}'!")
        return

    print(f"\n[*] Found {len(failed_rows)} failed activities to retry from '{log_csv}'")
    session = load_session()
    resolved_count = 0

    with tqdm(failed_rows, desc="Retrying Failures", unit="act") as pbar:
        for r in pbar:
            act_id = r["activity_id"]
            act_url = r["activity_url"]
            athlete_id = r.get("athlete_id", "")
            athlete_name = r.get("athlete_name", "")

            try:
                resp = session.get(act_url, timeout=15, allow_redirects=True)
                if "register" in resp.url or "login" in resp.url:
                    pbar.set_postfix({"resolved": resolved_count, "err": "auth"})
                    continue

                if resp.status_code == 200:
                    data = parse_activity_page(resp.text, act_id, athlete_id, athlete_name, act_url)
                    append_activity_to_csv(activities_csv, data)
                    existing_act_ids.add(act_id)
                    resolved_count += 1
                    log_activity_status(log_csv, act_id, act_url, athlete_id, athlete_name, "SUCCESS", "Resolved on Retry")
                    pbar.set_postfix({"resolved": resolved_count, "pts": data["points"]})
                elif resp.status_code == 429:
                    pbar.write("[!] Rate limited (429). Waiting 15s...")
                    time.sleep(15)
                else:
                    pbar.set_postfix({"resolved": resolved_count, "err": f"HTTP {resp.status_code}"})
            except Exception as e:
                pbar.set_postfix({"resolved": resolved_count, "err": str(e)[:15]})

            time.sleep(1.0)

    print(f"\n[OK] Retry complete: {resolved_count} out of {len(failed_rows)} activities resolved and added to '{activities_csv}'\n")

if __name__ == "__main__":
    retry_failed_activities()
