import os
import csv
import json
from collections import defaultdict
from dateutil import parser

def run_analysis(csv_path="activities.csv", memberlist_path="memberlist.csv", output_report="data_analysis_report.json"):
    # Locate files
    if not os.path.exists(csv_path):
        for alt in ["activities.csv", "../activities.csv", "YEAR2026/activities.csv", "../YEAR2026/activities.csv"]:
            if os.path.exists(alt):
                csv_path = alt
                break

    if not os.path.exists(memberlist_path):
        for alt in ["memberlist.csv", "../memberlist.csv", "YEAR2026/memberlist.csv", "../YEAR2026/memberlist.csv"]:
            if os.path.exists(alt):
                memberlist_path = alt
                break

    with open(csv_path, "r", encoding="utf-8") as f:
        activities = list(csv.DictReader(f))

    club_members = {}
    if os.path.exists(memberlist_path):
        with open(memberlist_path, "r", encoding="utf-8") as f:
            club_members = {r["athlete_id"]: r["athlete_name"] for r in csv.DictReader(f)}

    print(f"============================================================")
    print(f" STRAVA CLUB 2026 DATA ANALYSIS SUITE")
    print(f" Dataset: {os.path.abspath(csv_path)} ({len(activities)} activities)")
    print(f" Club Members: {len(club_members)} registered athletes")
    print(f"============================================================\n")

    # 1. First Athlete In-Depth Diagnosis
    first_aid = activities[0]["athlete_id"] if activities else None
    first_acts = [r for r in activities if r["athlete_id"] == first_aid]
    first_name = first_acts[0]["athlete_name"] if first_acts else "Unknown"

    first_total_pts = sum(float(r.get("points", 0) or 0) for r in first_acts)
    first_total_dist = sum(float(r.get("distance_km", 0) or 0) for r in first_acts)
    first_total_dur = sum(float(r.get("duration_minutes", 0) or 0) for r in first_acts)

    print(f"--- 1. FIRST ATHLETE DIAGNOSIS: {first_name} (ID: {first_aid}) ---")
    print(f"Raw Stats: {len(first_acts)} activities | {first_total_dist:.2f} km | {first_total_dur/60:.1f} hrs | {first_total_pts:.1f} pts")

    # Known true owner overrides discovered from Strava DOM / feed inspection
    TRUE_OWNERS = {
        "20041069989": ("178279476", "Muni Asheesh Potta"),
        "19957207427": ("178279476", "Muni Asheesh Potta"),
        "19662532293": ("123461241", "Srinivas K R"),
        "19628232467": ("181332418", "pritam Panigrahy"),
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
        "19923787876": ("181332418", "pritam Panigrahy"),
        "19184023245": ("158271875", "Atul Soni")
    }

    first_misattributed = []
    first_timer_glitches = []
    first_historical_prs = []

    for r in first_acts:
        aid = r["activity_id"]
        pts = float(r.get("points", 0) or 0)
        dur = float(r.get("duration_minutes", 0) or 0)
        dist = float(r.get("distance_km", 0) or 0)
        stype = r.get("activity_type", "")
        raw_dt = r.get("datetime_utc", "")

        # Check misattribution
        if aid in TRUE_OWNERS and TRUE_OWNERS[aid][0] != first_aid:
            first_misattributed.append({
                "activity_id": aid,
                "type": stype,
                "date": raw_dt,
                "points": pts,
                "true_owner": TRUE_OWNERS[aid][1],
                "true_owner_id": TRUE_OWNERS[aid][0]
            })

        # Check timer glitch
        if stype.lower() == "swim" and dur > 300:
            first_timer_glitches.append({
                "activity_id": aid,
                "type": stype,
                "date": raw_dt,
                "duration_minutes": dur,
                "duration_hours": round(dur / 60.0, 1),
                "points": pts,
                "reason": "Watch timer left running for 35+ hours; points inflated by duration multiplier."
            })

        # Check date (outside Aug & Sep 2026)
        try:
            clean_dt = raw_dt.replace(" on ", " ")
            dt_obj = parser.parse(clean_dt)
            if dt_obj.year == 2026 and dt_obj.month not in [8, 9]:
                first_historical_prs.append({
                    "activity_id": aid,
                    "type": stype,
                    "date": raw_dt,
                    "distance_km": dist,
                    "points": pts
                })
        except Exception:
            pass

    print(f"\n[A] Group Activity Misattributions in Athlete #1 ({len(first_misattributed)} activities):")
    for item in first_misattributed:
        print(f"    - Act {item['activity_id']} ({item['type']}, {item['points']} pts): Truly belongs to '{item['true_owner']}' ({item['true_owner_id']})")

    print(f"\n[B] Sensor / Timer Glitches ({len(first_timer_glitches)} activities):")
    for item in first_timer_glitches:
        print(f"    - Act {item['activity_id']} ({item['type']}): Duration {item['duration_hours']} hrs ({item['duration_minutes']} mins) -> {item['points']} pts ({item['reason']})")

    print(f"\n[C] Out-of-Competition Historical PRs ({len(first_historical_prs)} activities):")
    for item in first_historical_prs:
        print(f"    - Act {item['activity_id']} ({item['type']}, {item['date']}): {item['distance_km']} km -> {item['points']} pts")

    total_distorted_pts = (
        sum(x["points"] for x in first_misattributed)
        + sum(x["points"] for x in first_timer_glitches)
        + sum(x["points"] for x in first_historical_prs)
    )
    print(f"\n>> Total Artificial / Distorted Points on Athlete #1: {total_distorted_pts:.1f} pts!")
    print(f">> Adjusted True Competition Points: ~{first_total_pts - total_distorted_pts:.1f} pts\n")

    # 2. Activity ID Uniqueness Audit
    print("--- 2. ACTIVITY ID UNIQUENESS & DEDUPLICATION AUDIT ---")
    act_counts = defaultdict(list)
    for r in activities:
        act_counts[r["activity_id"]].append(r)

    duplicate_ids = {k: v for k, v in act_counts.items() if len(v) > 1}
    print(f"Total Unique Activity IDs: {len(act_counts)} of {len(activities)} rows.")
    if duplicate_ids:
        print(f"[!] Warning: {len(duplicate_ids)} duplicate activity IDs detected!")
        for did, items in duplicate_ids.items():
            print(f"    Act {did} repeated {len(items)} times across athletes: {[x['athlete_name'] for x in items]}")
    else:
        print("[+] PASS: All activity IDs are currently unique.")

    # 3. Cross-Athlete Group Activity Leakage Audit
    print("\n--- 3. CROSS-ATHLETE GROUP ACTIVITY LEAKAGE AUDIT ---")
    all_misattributed = []
    for r in activities:
        aid = r["activity_id"]
        if aid in TRUE_OWNERS:
            true_aid, true_name = TRUE_OWNERS[aid]
            if true_aid != r["athlete_id"]:
                all_misattributed.append({
                    "activity_id": aid,
                    "current_athlete": r["athlete_name"],
                    "current_athlete_id": r["athlete_id"],
                    "true_athlete": true_name,
                    "true_athlete_id": true_aid,
                    "is_club_member": true_aid in club_members,
                    "points": float(r.get("points", 0) or 0),
                    "type": r.get("activity_type", "")
                })

    print(f"Total Group Misattributions Detected across Dataset: {len(all_misattributed)}")
    for m in all_misattributed:
        status = "Club Member" if m["is_club_member"] else "NON-CLUB External Friend"
        print(f"  * Act {m['activity_id']} ({m['type']}, {m['points']} pts): Assigned to '{m['current_athlete']}' -> TRUE: '{m['true_athlete']}' [{status}]")

    # 4. Outliers & Anomaly Detection
    print("\n--- 4. STATISTICAL OUTLIER DETECTION ---")
    outliers = []
    for r in activities:
        pts = float(r.get("points", 0) or 0)
        dist = float(r.get("distance_km", 0) or 0)
        dur = float(r.get("duration_minutes", 0) or 0)
        stype = r.get("activity_type", "").lower()

        reasons = []
        if pts > 4000:
            reasons.append(f"Points ({pts}) > 4,000")
        if dur > 600:
            reasons.append(f"Duration ({dur} mins / {dur/60:.1f} hrs) > 10 hours")
        if stype == "swim" and dur > 120:
            reasons.append(f"Swim duration ({dur} mins) > 2 hours")
        if dist > 100:
            reasons.append(f"Distance ({dist} km) > 100 km")

        if reasons:
            outliers.append({
                "activity_id": r["activity_id"],
                "athlete_name": r["athlete_name"],
                "activity_type": r["activity_type"],
                "distance_km": dist,
                "duration_minutes": dur,
                "points": pts,
                "date": r["datetime_utc"],
                "reasons": reasons
            })

    print(f"Total Statistical Outliers Found: {len(outliers)}")
    for o in outliers:
        print(f"  * Act {o['activity_id']} ({o['athlete_name']}, {o['activity_type']}): {', '.join(o['reasons'])}")

    # 5. Competition Period Distribution
    print("\n--- 5. TEMPORAL DISTRIBUTION (MONTHLY) ---")
    month_counts = defaultdict(int)
    for r in activities:
        raw_dt = r["datetime_utc"].replace(" on ", " ")
        try:
            dt = parser.parse(raw_dt)
            month_counts[f"{dt.year}-{dt.month:02d}"] += 1
        except Exception:
            month_counts["Unknown"] += 1

    for ym, cnt in sorted(month_counts.items()):
        period = "Competition Window" if ym in ["2026-08", "2026-09"] else "Out-of-Window PR Widget"
        print(f"  {ym}: {cnt:3d} activities [{period}]")

    # Generate JSON report
    report = {
        "dataset_summary": {
            "total_activities": len(activities),
            "unique_athletes": len(set(r["athlete_id"] for r in activities)),
            "first_athlete": {
                "id": first_aid,
                "name": first_name,
                "raw_activities": len(first_acts),
                "raw_points": round(first_total_pts, 1),
                "misattributed_activities": len(first_misattributed),
                "timer_glitches": len(first_timer_glitches),
                "historical_prs": len(first_historical_prs),
                "total_distorted_points": round(total_distorted_pts, 1)
            }
        },
        "misattributions": all_misattributed,
        "outliers": outliers,
        "monthly_distribution": dict(sorted(month_counts.items()))
    }

    with open(output_report, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"\n[+] Saved full diagnostic report -> {os.path.abspath(output_report)}\n")

    return report

if __name__ == "__main__":
    run_analysis()
