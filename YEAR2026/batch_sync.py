import os
import sys
import csv
import time
from tqdm import tqdm
from fetch_single_user import fetch_single_user

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def run_batch(limit: int = None, start_from: int = 1, delay: float = 2.0):
    members_file = "memberlist.csv"
    if not os.path.exists(members_file):
        print(f"[-] '{members_file}' not found.")
        return

    athletes = []
    with open(members_file, "r", encoding="utf-8", errors="replace") as f:
        for r in csv.DictReader(f):
            aid = str(r.get("athlete_id", "")).strip()
            name = str(r.get("athlete_name", "")).strip()
            if aid:
                athletes.append({"id": aid, "name": name})

    total_in_club = len(athletes)
    if start_from > 1:
        athletes = athletes[start_from - 1:]

    if limit and limit > 0:
        athletes = athletes[:limit]

    print(f"\n[*] Starting Batch Sync for {len(athletes)} athlete(s) (starting from #{start_from} of {total_in_club})...")
    total_added = 0

    with tqdm(athletes, desc="Syncing Athletes", unit="athlete") as pbar:
        for idx, ath in enumerate(pbar, start_from):
            aid = ath["id"]
            aname = ath["name"]
            safe_display = aname.encode("ascii", "replace").decode("ascii")[:15]
            pbar.set_postfix({"current": safe_display})

            try:
                added = fetch_single_user(aid, months_back=2)
                total_added += added
            except Exception as e:
                pbar.write(f"[!] Error on athlete {aid}: {e}")

            if idx < total_in_club and delay > 0:
                time.sleep(delay)

    print(f"\n[+] Batch complete: {total_added} new activities added across {len(athletes)} athletes.\n")
    try:
        from export_dashboard import generate_dashboard_json
        generate_dashboard_json()
        print("[+] Dashboard data refreshed for GitHub Pages.")
    except Exception as e:
        print(f"[-] Dashboard export error: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Batch sync Strava club athletes")
    parser.add_argument("limit", nargs="?", type=int, default=None, help="Limit number of athletes to sync")
    parser.add_argument("--start-from", type=int, default=1, help="Athlete index to start from (1-based, default: 1)")
    args = parser.parse_args()

    run_batch(limit=args.limit, start_from=args.start_from)
