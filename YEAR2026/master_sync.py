import os
import sys
import re
import csv
import json
import time
import shutil
import datetime
import subprocess
import argparse
from typing import List, Dict, Set, Any
from bs4 import BeautifulSoup
import requests
from dateutil import parser as dt_parser

# Setup paths and environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Import module functions
from points import (
    calculate_dynamic_points,
    calculate_legacy_points,
    format_pace,
    is_indoor_ride
)
from fetch_memberlist import fetch_club_members
from fetch_single_user import (
    load_session,
    discover_activity_ids,
    parse_activity_page,
    resolve_athlete_name,
    append_activity_to_csv,
    log_activity_status,
    load_config
)
from filter_and_clean_data import clean_and_filter_activities
from export_dashboard import generate_dashboard_json

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

LOG_FILE = "daily_sync.log"

def log(msg: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(formatted)
    try:
        with open(os.path.join(BASE_DIR, LOG_FILE), "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass

def check_if_activity_deleted(session: requests.Session, activity_id: str) -> bool:
    """
    Checks whether an activity has been deleted on Strava.
    Returns True if deleted or 404, False if active.
    """
    url = f"https://www.strava.com/activities/{activity_id}"
    try:
        resp = session.get(url, timeout=12)
        if resp.status_code == 404:
            return True
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            title = soup.find("title").text if soup.find("title") else ""
            
            # Deleted activities show generic title or "Page Not Found"
            if "Running, Cycling & Hiking App" in title or "Page Not Found" in title:
                script = soup.find("script", id="__NEXT_DATA__")
                if script and script.string:
                    try:
                        data = json.loads(script.string)
                        if not data.get("props", {}).get("pageProps", {}).get("activity"):
                            return True
                    except Exception:
                        return True
                else:
                    return True
            return False
        return False
    except Exception:
        return False

def run_pipeline(
    skip_scrape: bool = False,
    no_push: bool = False,
    limit: int = None,
    force_reconcile: bool = False
):
    start_time = time.time()
    log("=" * 72)
    log("       CONNECTIVITY SPORTS DAY 2026 - MASTER SYNC PIPELINE       ")
    log("=" * 72)
    log(f"Working Directory: {BASE_DIR}")
    log(f"Mode: {'SKIP-SCRAPE' if skip_scrape else 'FULL SYNC'} | Git Push: {not no_push}")

    # =========================================================================
    # STEP 1: Refresh Memberlist
    # =========================================================================
    log("\n[STEP 1/7] Refreshing Club Member List from Strava...")
    members_csv = "memberlist.csv"
    if not skip_scrape:
        try:
            fetch_club_members(club_id="1649493", max_pages=8, min_delay=1.5, out_csv=members_csv)
            log("[+] Member list refreshed successfully from Strava.")
        except Exception as e:
            log(f"[!] Warning: Memberlist fetch notice ({e}). Continuing with existing members.")

    club_members: Dict[str, str] = {}
    if os.path.exists(members_csv):
        with open(members_csv, "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                aid = str(r.get("athlete_id", "")).strip()
                aname = str(r.get("athlete_name", "")).strip()
                if aid:
                    club_members[aid] = aname
    log(f"[+] Loaded {len(club_members)} registered club athlete(s).")

    # =========================================================================
    # STEP 2: Scrape Latest Activities & Discover New Ones
    # =========================================================================
    log("\n[STEP 2/7] Scraping Active Club Activities for August & September 2026...")
    session = load_session()
    activities_csv = "activities.csv"
    activity_log_csv = "activity_log.csv"

    # Load existing activity IDs
    existing_activities: Dict[str, Dict[str, Any]] = {}
    if os.path.exists(activities_csv):
        with open(activities_csv, "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                act_id = str(r.get("activity_id", "")).strip()
                if act_id:
                    existing_activities[act_id] = r

    log(f"[*] Currently tracking {len(existing_activities)} activities in {activities_csv}.")

    discovered_active_by_athlete: Dict[str, Set[str]] = {}
    new_activities_added = 0

    if not skip_scrape:
        athlete_list = list(club_members.items())
        if limit and limit > 0:
            athlete_list = athlete_list[:limit]

        for idx, (aid, aname) in enumerate(athlete_list, 1):
            log(f" -> [{idx}/{len(athlete_list)}] Discovering activities for {aname} (ID: {aid})...")
            try:
                # Discover active activities for current & previous months (Aug & Sep 2026)
                act_ids = discover_activity_ids(session, aid, months_back=2)
                discovered_active_by_athlete[aid] = set(act_ids)
                log(f"    Discovered {len(act_ids)} activity link(s) on Strava.")

                # Process any newly found activities
                for act_id in act_ids:
                    if act_id not in existing_activities:
                        act_url = f"https://www.strava.com/activities/{act_id}"
                        try:
                            resp = session.get(act_url, timeout=12)
                            if resp.status_code == 200:
                                rec = parse_activity_page(resp.text, act_id, aid, aname, act_url)
                                
                                # Verify 2026 date
                                dt_str = rec.get("datetime_utc", "")
                                m_prev = re.search(r"\b(202[0-5]|201\d)\b", dt_str)
                                if m_prev:
                                    log_activity_status(activity_log_csv, act_id, act_url, aid, aname, "SKIPPED", f"Historical year {m_prev.group(1)}")
                                    continue

                                append_activity_to_csv(activities_csv, rec)
                                existing_activities[act_id] = rec
                                new_activities_added += 1
                                log_activity_status(activity_log_csv, act_id, act_url, aid, aname, "SUCCESS")
                                log(f"    [+] New Activity logged: {rec.get('activity_type')} {rec.get('distance_km')}km ({rec.get('points')} pts)")
                            else:
                                log_activity_status(activity_log_csv, act_id, act_url, aid, aname, "FAILURE", f"HTTP {resp.status_code}")
                        except Exception as ex:
                            log_activity_status(activity_log_csv, act_id, act_url, aid, aname, "FAILURE", str(ex))
                        time.sleep(0.4)
            except Exception as e:
                log(f"    [!] Error discovering activities for athlete {aid}: {e}")
            time.sleep(1.5)

        log(f"[+] Scraping complete: {new_activities_added} new activities added.")
    else:
        log("[*] Skipping scraping as requested (--skip-scrape).")

    # =========================================================================
    # STEP 3: Reconcile and Purge Deleted Entries
    # =========================================================================
    log("\n[STEP 3/7] Reconciling Deleted Entries & Active Auditing...")
    purged_deleted = 0
    purged_non_member = 0
    retained_activities: List[Dict[str, Any]] = []

    for act_id, record in existing_activities.items():
        aid = str(record.get("athlete_id", "")).strip()
        
        # Check A: Exclude non-club members
        if aid not in club_members:
            log(f"    [-] Removing activity {act_id}: Athlete {aid} ({record.get('athlete_name')}) is no longer in club.")
            log_activity_status(activity_log_csv, act_id, record.get("activity_url", ""), aid, record.get("athlete_name", ""), "PURGED_NON_MEMBER")
            purged_non_member += 1
            continue

        # Check B: Verify if activity was deleted on Strava
        # If athlete was scanned in this run and the activity is no longer in their active list:
        if (aid in discovered_active_by_athlete and act_id not in discovered_active_by_athlete[aid]) or force_reconcile:
            log(f"    [*] Auditing potentially deleted activity {act_id} for {record.get('athlete_name')}...")
            if check_if_activity_deleted(session, act_id):
                log(f"    [!] DELETED ACTIVITY DETECTED: {act_id} ({record.get('activity_type')} - {record.get('distance_km')}km). Purging from dataset.")
                log_activity_status(activity_log_csv, act_id, record.get("activity_url", ""), aid, record.get("athlete_name", ""), "PURGED_DELETED")
                purged_deleted += 1
                continue

        retained_activities.append(record)

    log(f"[+] Deletion Reconciliation Complete:")
    log(f"    - Purged deleted activities: {purged_deleted}")
    log(f"    - Purged non-member activities: {purged_non_member}")
    log(f"    - Active activities retained: {len(retained_activities)}")

    # Write back reconciled dataset to activities.csv
    headers = [
        "activity_id", "athlete_id", "athlete_name", "activity_type",
        "datetime_utc", "distance_km", "duration_minutes", "points",
        "pace", "is_indoor", "activity_url"
    ]
    with open(activities_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for r in retained_activities:
            writer.writerow({k: r.get(k, "") for k in headers})

    # =========================================================================
    # STEP 4: Apply Anti-Cheat & Data Integrity Filters
    # =========================================================================
    log("\n[STEP 4/7] Applying Anti-Cheat & Data Integrity Safeguards...")
    clean_and_filter_activities(
        input_csv=activities_csv,
        output_csv=activities_csv,
        memberlist_csv=members_csv,
        competition_only=True
    )

    # =========================================================================
    # STEP 5: Export Dashboard Data & Dual-Schema Points
    # =========================================================================
    log("\n[STEP 5/7] Computing Dual-Schema Standings (Dynamic MET & Legacy 2025)...")
    dashboard_payload = generate_dashboard_json(csv_path=activities_csv)

    if dashboard_payload and "summary" in dashboard_payload:
        s = dashboard_payload["summary"]
        log(f"[+] Summary Standings:")
        log(f"    - Total Active Athletes: {s.get('total_athletes')}")
        log(f"    - Total Valid Activities: {s.get('total_activities')}")
        log(f"    - Total Distance: {s.get('total_distance_km')} km")
        log(f"    - Total Duration: {s.get('total_duration_hours')} hrs")
        log(f"    - Total Dynamic MET Points: {s.get('total_points_dynamic'):,} pts")
        log(f"    - Total Legacy 2025 Points: {s.get('total_points_legacy'):,} pts")

    # =========================================================================
    # STEP 6: Build Web Dashboard HTML
    # =========================================================================
    log("\n[STEP 6/7] Building Web Dashboard HTML & Synchronizing Targets...")
    try:
        # Run generate_html.py
        gen_script = os.path.join(BASE_DIR, "generate_html.py")
        if os.path.exists(gen_script):
            subprocess.run([sys.executable, gen_script], check=True, cwd=BASE_DIR)
            log("[+] index.html successfully rebuilt with embedded fallback data and schema toggles.")
    except Exception as e:
        log(f"[!] Error building index.html: {e}")

    # Synchronize all auxiliary directories
    for target in ["YEAR2026", "web", "export"]:
        target_dir = os.path.join(BASE_DIR, target)
        os.makedirs(target_dir, exist_ok=True)
        for fname in ["activities.csv", "dashboard_data.json", "index.html", "arena.html", "ANTI_CHEAT_AND_DATA_INTEGRITY.md"]:
            src = os.path.join(BASE_DIR, fname)
            dst = os.path.join(target_dir, fname)
            if os.path.exists(src):
                shutil.copy2(src, dst)
    log("[+] Target directories (YEAR2026, web, export) fully synchronized.")

    # =========================================================================
    # STEP 7: Commit & Push to GitHub Pages
    # =========================================================================
    log("\n[STEP 7/7] Committing & Pushing Updates to GitHub Pages...")
    if not no_push:
        try:
            # Check for git modifications
            status_res = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True, cwd=BASE_DIR, check=True
            )
            changes = status_res.stdout.strip()
            if changes:
                log(f"[*] Detected changes to repository:\n{changes}")
                # Stage files
                files_to_stage = [
                    "activities.csv",
                    "dashboard_data.json",
                    "index.html",
                    "arena.html",
                    "ANTI_CHEAT_AND_DATA_INTEGRITY.md",
                    "status.html",
                    "activity_log.csv",
                    "memberlist.csv",
                    "generate_html.py",
                    "generate_arena.py",
                    "export_dashboard.py",
                    "points.py",
                    "master_sync.py",
                    "YEAR2026",
                    "web",
                    "export"
                ]
                subprocess.run(["git", "add"] + files_to_stage, cwd=BASE_DIR, check=True)
                
                # Commit
                ts_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                total_acts = dashboard_payload.get("summary", {}).get("total_activities", len(retained_activities)) if dashboard_payload else len(retained_activities)
                commit_msg = f"Auto-sync Strava club data: {ts_str} ({total_acts} acts, {new_activities_added} new, {purged_deleted} purged)"
                subprocess.run(["git", "commit", "-m", commit_msg], cwd=BASE_DIR, check=True)
                log(f"[+] Committed: '{commit_msg}'")

                # Push
                subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR, check=True)
                log("[+] Successfully pushed to GitHub Pages! Live at https://lupilgaming.github.io/Strava2026/")
            else:
                log("[*] No data changes detected. Repository is already up to date.")
        except subprocess.CalledProcessError as err:
            log(f"[!] Git operation error: {err}")
        except Exception as e:
            log(f"[!] Warning: Git push encountered issue: {e}")
    else:
        log("[*] Git push skipped (--no-push flag active).")

    elapsed = round(time.time() - start_time, 1)
    log("=" * 72)
    log(f" PIPELINE COMPLETED SUCCESSFULLY IN {elapsed}s")
    log("=" * 72 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Master sync pipeline for Strava 2026 Club Leaderboard")
    parser.add_argument("--skip-scrape", action="store_true", help="Skip scraping new data from Strava and reprocess local data")
    parser.add_argument("--no-push", action="store_true", help="Skip git commit and push")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of athletes to sync")
    parser.add_argument("--force-reconcile", action="store_true", help="Force deletion audit check on all activities")
    args = parser.parse_args()

    run_pipeline(
        skip_scrape=args.skip_scrape,
        no_push=args.no_push,
        limit=args.limit,
        force_reconcile=args.force_reconcile
    )
