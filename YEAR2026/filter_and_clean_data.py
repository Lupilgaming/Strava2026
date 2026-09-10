import os
import sys
import csv
import json
import shutil
import argparse
from collections import defaultdict
from dateutil import parser as dt_parser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from points import calculate_activity_points, format_pace, is_indoor_ride

def clean_and_filter_activities(
    input_csv="activities.csv",
    output_csv="activities.csv",
    memberlist_csv="memberlist.csv",
    competition_only=True
):
    # Locate paths
    if not os.path.exists(input_csv):
        for alt in ["activities.csv", "../activities.csv", "YEAR2026/activities.csv", "../YEAR2026/activities.csv"]:
            if os.path.exists(alt):
                input_csv = alt
                break

    if not os.path.exists(memberlist_csv):
        for alt in ["memberlist.csv", "../memberlist.csv", "YEAR2026/memberlist.csv", "../YEAR2026/memberlist.csv"]:
            if os.path.exists(alt):
                memberlist_csv = alt
                break

    print("============================================================")
    print(" STRAVA 2026 DATA FILTER & SANITIZATION PIPELINE")
    print(f" Input: {os.path.abspath(input_csv)}")
    print(f" Memberlist: {os.path.abspath(memberlist_csv)}")
    print(f" Competition Window Only: {competition_only} (Aug & Sep 2026)")
    print("============================================================\n")

    # Load club members
    club_members = {}
    if os.path.exists(memberlist_csv):
        with open(memberlist_csv, "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                aid = str(r["athlete_id"]).strip()
                aname = str(r["athlete_name"]).strip()
                club_members[aid] = aname

    # Verified true owner mappings from Strava activity DOM inspection
    TRUE_OWNERS = {
        "20041069989": ("178279476", "Muni Asheesh Potta"),
        "19957207427": ("178279476", "Muni Asheesh Potta"),
        "19662532293": ("123461241", "Srinivas K R"),
        "19628232467": ("181332418", "pritam Panigrahy"), # external non-club
        "19628253900": ("180079292", "aadhar sharma"),
        "17057440050": ("178453532", "Divyansh Singh"),
        "18845057178": ("178453532", "Divyansh Singh"),
        "17030281673": ("178453532", "Divyansh Singh"),
        "16930171186": ("178453532", "Divyansh Singh"),
        "20103416049": ("178453532", "Divyansh Singh"),
        "20103404501": ("178453532", "Divyansh Singh"),
        "20103393824": ("178453532", "Divyansh Singh"),
        "19917167043": ("178453532", "Divyansh Singh"),
        "19720008251": ("178453532", "Divyansh Singh"),
        "19923785855": ("178279476", "Muni Asheesh Potta"),
        "20041095636": ("50127060", "Prateek Giri"),
        "19923787876": ("181332418", "pritam Panigrahy"), # external non-club
        "19184023245": ("158271875", "Atul Soni")        # external non-club
    }

    with open(input_csv, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    print(f"[*] Total input activities: {len(reader)}")

    # 1. Deduplication by activity_id & Owner Correction
    seen_activity_ids = set()
    cleaned_activities = []
    excluded_non_club = []
    corrected_ownership = 0
    fixed_timer_glitches = 0
    filtered_out_of_window = 0

    for row in reader:
        act_id = str(row.get("activity_id", "")).strip()
        if not act_id:
            continue

        # Strict uniqueness: ensure data has unique activity IDs only
        if act_id in seen_activity_ids:
            print(f"[-] Dropping duplicate activity ID {act_id}")
            continue
        seen_activity_ids.add(act_id)

        # 2. Re-attribute to True Owner
        if act_id in TRUE_OWNERS:
            true_aid, true_name = TRUE_OWNERS[act_id]
            # If external non-club friend, exclude from club competition
            if true_aid not in club_members:
                excluded_non_club.append({
                    "activity_id": act_id,
                    "athlete": true_name,
                    "reason": "External friend (not in club memberlist)"
                })
                continue

            # Re-attribute to true club member
            if row["athlete_id"] != true_aid:
                corrected_ownership += 1
                row["athlete_id"] = true_aid
                row["athlete_name"] = club_members.get(true_aid, true_name)

        # 3. Fix sensor / watch-timer outliers and restore missing durations
        # Activity 20035504028: 2,025m swim left running for 35 hours
        if act_id == "20035504028":
            # Normal swim duration for 2,025m (~2.03 km) is ~50.6 minutes
            row["distance_km"] = "2.03"
            row["duration_minutes"] = "50.6"
            fixed_timer_glitches += 1
        elif act_id == "20103393824":  # Walk 7.00 km (1:06:00 duration)
            row["distance_km"] = "7.00"
            row["duration_minutes"] = "66.0"
            fixed_timer_glitches += 1
        elif act_id == "20103404501":  # Weight Training 5x5 split (1:10:00 duration)
            row["distance_km"] = "0.0"
            row["duration_minutes"] = "70.0"
            fixed_timer_glitches += 1
        elif act_id == "20103416049":  # Workout Morning shift (47:00 duration)
            row["distance_km"] = "0.0"
            row["duration_minutes"] = "47.0"
            fixed_timer_glitches += 1
        elif act_id == "19917167043":  # Run 5.00 km (32:00 duration)
            row["distance_km"] = "5.00"
            row["duration_minutes"] = "32.0"
            fixed_timer_glitches += 1
        elif act_id == "20088869641":  # Run 3.00 km (24:00 duration)
            row["distance_km"] = "3.00"
            row["duration_minutes"] = "24.0"
            fixed_timer_glitches += 1
        elif act_id == "19593209953":  # Run 3.10 km (26:33 duration)
            row["distance_km"] = "3.10"
            row["duration_minutes"] = "26.55"
            fixed_timer_glitches += 1

        # 4. Filter by Competition Period (August & September 2026)
        raw_dt = row.get("datetime_utc", "")
        clean_dt = raw_dt.replace(" on ", " ")
        try:
            dt = dt_parser.parse(clean_dt)
            if competition_only:
                if dt.year != 2026 or dt.month not in [8, 9]:
                    filtered_out_of_window += 1
                    continue
            else:
                if dt.year != 2026:
                    filtered_out_of_window += 1
                    continue
        except Exception:
            pass

        # 5. Recalculate Points accurately, detect indoor rides, and calculate pace
        stype = row.get("activity_type", "Workout")
        try:
            dist = float(row.get("distance_km", 0.0) or 0.0)
            dur = float(row.get("duration_minutes", 0.0) or 0.0)
        except ValueError:
            dist, dur = 0.0, 0.0

        indoor_flag = is_indoor_ride(stype, dist)
        pace_str = ""
        if stype.lower() in ["run", "trail run", "walk", "hike"]:
            pace_str = format_pace(dist, dur)

        calc_pts = calculate_activity_points(stype, dist, dur, is_indoor=indoor_flag)

        row["points"] = str(round(calc_pts, 2))
        row["distance_km"] = str(round(dist, 2))
        row["duration_minutes"] = str(round(dur, 2))
        row["pace"] = pace_str
        row["is_indoor"] = "true" if indoor_flag else "false"

        cleaned_activities.append(row)

    print(f"\n[+] Sanitization Summary:")
    print(f"    - Unique activities retained: {len(cleaned_activities)}")
    print(f"    - Group activity ownerships corrected: {corrected_ownership}")
    print(f"    - External non-club activities excluded: {len(excluded_non_club)}")
    print(f"    - Watch timer outliers corrected: {fixed_timer_glitches}")
    print(f"    - Out-of-competition activities filtered: {filtered_out_of_window}")

    # Output to CSV destinations
    headers = [
        "activity_id", "athlete_id", "athlete_name", "activity_type",
        "datetime_utc", "distance_km", "duration_minutes", "points",
        "pace", "is_indoor", "activity_url"
    ]


    dest_paths = [
        "activities.csv",
        "../activities.csv",
        "YEAR2026/activities.csv",
        "../YEAR2026/activities.csv",
        "web/activities.csv",
        "../web/activities.csv",
        "export/activities.csv",
        "../export/activities.csv"
    ]

    for p in dest_paths:
        try:
            p_abs = os.path.abspath(p)
            os.makedirs(os.path.dirname(p_abs), exist_ok=True)
            with open(p_abs, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                for r in cleaned_activities:
                    writer.writerow({k: r.get(k, "") for k in headers})
            print(f"[+] Saved cleaned activities CSV -> {p_abs}")
        except Exception:
            pass

    return cleaned_activities

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter and clean Strava activities dataset")
    parser.add_argument("--all-year", action="store_true", help="Keep all 2026 activities instead of Aug-Sep only")
    args = parser.parse_args()

    clean_and_filter_activities(competition_only=not args.all_year)
