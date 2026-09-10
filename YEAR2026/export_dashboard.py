import os
import sys
import csv
import json
import shutil
import datetime
from typing import List, Dict, Any
from dateutil import parser

# Ensure points.py is importable
from points import (
    calculate_dynamic_points,
    calculate_legacy_points,
    format_pace,
    is_indoor_ride
)

def generate_dashboard_json(csv_path: str = "activities.csv", output_paths: List[str] = None):
    if not os.path.exists(csv_path):
        for alt in ["activities.csv", "../activities.csv", "YEAR2026/activities.csv", "../YEAR2026/activities.csv"]:
            if os.path.exists(alt):
                csv_path = alt
                break

    if not os.path.exists(csv_path):
        print(f"[-] CSV file not found: {csv_path}")
        return None

    if output_paths is None:
        output_paths = [
            "dashboard_data.json",
            "../dashboard_data.json",
            "YEAR2026/dashboard_data.json",
            "../YEAR2026/dashboard_data.json",
            "web/dashboard_data.json",
            "../web/dashboard_data.json",
            "export/dashboard_data.json",
            "../export/dashboard_data.json"
        ]

    activities: List[Dict[str, Any]] = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            act_type = str(r.get("activity_type", "Workout")).strip()
            try:
                dist = float(r.get("distance_km", 0.0) or 0.0)
                dur = float(r.get("duration_minutes", 0.0) or 0.0)
            except ValueError:
                dist, dur = 0.0, 0.0

            raw_dt = str(r.get("datetime_utc", "")).strip()
            iso_dt = ""
            display_dt = raw_dt
            if raw_dt:
                try:
                    clean = raw_dt.replace(" on ", " ")
                    dt = parser.parse(clean)
                    iso_dt = dt.isoformat()
                    display_dt = dt.strftime("%b %d, %Y %I:%M %p") if (dt.hour or dt.minute) else dt.strftime("%b %d, %Y")
                except Exception:
                    iso_dt = raw_dt

            is_ind = str(r.get("is_indoor", "")).strip().lower() in ["true", "1", "yes"] or is_indoor_ride(act_type, dist)
            pace_val = str(r.get("pace", "")).strip()
            if not pace_val and any(k in act_type.lower() for k in ["run", "walk", "hike", "trail"]):
                pace_val = format_pace(dist, dur)

            # Compute points under both schemas
            pts_dyn = calculate_dynamic_points(act_type, dist, dur, pace_str=pace_val, is_indoor=is_ind)
            pts_leg = calculate_legacy_points(act_type, dist, dur, is_indoor=is_ind)

            activities.append({
                "activity_id": str(r.get("activity_id", "")),
                "athlete_id": str(r.get("athlete_id", "")),
                "athlete_name": str(r.get("athlete_name", "Unknown Athlete")),
                "activity_type": act_type,
                "datetime_utc": raw_dt,
                "datetime_iso": iso_dt,
                "datetime_display": display_dt,
                "distance_km": round(dist, 2),
                "duration_minutes": round(dur, 2),
                "points": round(pts_dyn, 2), # Default active points (Dynamic MET)
                "points_dynamic": round(pts_dyn, 2),
                "points_legacy": round(pts_leg, 2),
                "pace": pace_val,
                "is_indoor": is_ind,
                "activity_url": str(r.get("activity_url", ""))
            })

    # Group by athlete
    athletes_map: Dict[str, Dict[str, Any]] = {}
    for act in activities:
        aid = act["athlete_id"]
        aname = act["athlete_name"]
        if aid not in athletes_map:
            athletes_map[aid] = {
                "athlete_id": aid,
                "athlete_name": aname,
                "total_activities": 0,
                "activity_types": set(),
                "total_distance_km": 0.0,
                "total_duration_minutes": 0.0,
                "total_points_dynamic": 0.0,
                "total_points_legacy": 0.0
            }
        a = athletes_map[aid]
        a["total_activities"] += 1
        a["activity_types"].add(act["activity_type"])
        a["total_distance_km"] += act["distance_km"]
        a["total_duration_minutes"] += act["duration_minutes"]
        a["total_points_dynamic"] += act["points_dynamic"]
        a["total_points_legacy"] += act["points_legacy"]

    # Calculate Legacy ranks mapping
    sorted_legacy = sorted(athletes_map.values(), key=lambda x: x["total_points_legacy"], reverse=True)
    legacy_ranks = {a["athlete_id"]: rank for rank, a in enumerate(sorted_legacy, 1)}

    leaderboard = []
    for aid, a in athletes_map.items():
        leaderboard.append({
            "athlete_id": aid,
            "athlete_name": a["athlete_name"],
            "total_activities": a["total_activities"],
            "unique_types": len(a["activity_types"]),
            "total_distance_km": round(a["total_distance_km"], 2),
            "total_duration_minutes": round(a["total_duration_minutes"], 2),
            "total_points": round(a["total_points_dynamic"], 2), # Default active
            "total_points_dynamic": round(a["total_points_dynamic"], 2),
            "total_points_legacy": round(a["total_points_legacy"], 2),
            "rank_legacy": legacy_ranks.get(aid, 1)
        })

    # Sort leaderboard by Dynamic Points descending
    leaderboard.sort(key=lambda x: x["total_points_dynamic"], reverse=True)

    max_dist = max([a["total_distance_km"] for a in leaderboard] + [1.0])
    max_dur = max([a["total_duration_minutes"] for a in leaderboard] + [1.0])
    max_pts_dyn = max([a["total_points_dynamic"] for a in leaderboard] + [1.0])
    max_pts_leg = max([a["total_points_legacy"] for a in leaderboard] + [1.0])
    max_cnt = max([a["total_activities"] for a in leaderboard] + [1])
    max_div = max([a["unique_types"] for a in leaderboard] + [1])

    dashboard_athletes = []
    for rank, ath in enumerate(leaderboard, 1):
        ath_copy = dict(ath)
        ath_copy["rank"] = rank # Default dynamic rank
        ath_copy["rank_dynamic"] = rank
        ath_copy["radar_metrics"] = {
            "distance": round((ath["total_distance_km"] / max_dist) * 100, 1),
            "duration": round((ath["total_duration_minutes"] / max_dur) * 100, 1),
            "points": round((ath["total_points_dynamic"] / max_pts_dyn) * 100, 1),
            "frequency": round((ath["total_activities"] / max_cnt) * 100, 1),
            "diversity": round((ath["unique_types"] / max_div) * 100, 1)
        }
        ath_copy["radar_metrics_dynamic"] = dict(ath_copy["radar_metrics"])
        ath_copy["radar_metrics_legacy"] = {
            "distance": round((ath["total_distance_km"] / max_dist) * 100, 1),
            "duration": round((ath["total_duration_minutes"] / max_dur) * 100, 1),
            "points": round((ath["total_points_legacy"] / max_pts_leg) * 100, 1),
            "frequency": round((ath["total_activities"] / max_cnt) * 100, 1),
            "diversity": round((ath["unique_types"] / max_div) * 100, 1)
        }
        dashboard_athletes.append(ath_copy)

    # Sport breakdown
    sports: Dict[str, Dict[str, Any]] = {}
    for act in activities:
        st = act["activity_type"]
        if st not in sports:
            sports[st] = {
                "activity_type": st,
                "count": 0,
                "total_distance_km": 0.0,
                "total_duration_minutes": 0.0,
                "total_points": 0.0,
                "total_points_dynamic": 0.0,
                "total_points_legacy": 0.0
            }
        sp = sports[st]
        sp["count"] += 1
        sp["total_distance_km"] += act["distance_km"]
        sp["total_duration_minutes"] += act["duration_minutes"]
        sp["total_points_dynamic"] += act["points_dynamic"]
        sp["total_points_legacy"] += act["points_legacy"]
        sp["total_points"] = sp["total_points_dynamic"]

    sport_list = list(sports.values())
    for sp in sport_list:
        sp["total_distance_km"] = round(sp["total_distance_km"], 2)
        sp["total_duration_minutes"] = round(sp["total_duration_minutes"], 2)
        sp["total_points"] = round(sp["total_points"], 2)
        sp["total_points_dynamic"] = round(sp["total_points_dynamic"], 2)
        sp["total_points_legacy"] = round(sp["total_points_legacy"], 2)
    sport_list.sort(key=lambda x: x["count"], reverse=True)

    summary = {
        "total_athletes": len(dashboard_athletes),
        "total_activities": len(activities),
        "total_distance_km": round(sum(a["total_distance_km"] for a in dashboard_athletes), 2),
        "total_duration_hours": round(sum(a["total_duration_minutes"] for a in dashboard_athletes) / 60.0, 1),
        "total_points": round(sum(a["total_points_dynamic"] for a in dashboard_athletes), 2),
        "total_points_dynamic": round(sum(a["total_points_dynamic"] for a in dashboard_athletes), 2),
        "total_points_legacy": round(sum(a["total_points_legacy"] for a in dashboard_athletes), 2),
        "last_updated": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    payload = {
        "summary": summary,
        "athletes": dashboard_athletes,
        "sport_breakdown": sport_list,
        "activities": activities
    }

    # Save to all dashboard_data.json destinations
    for p in output_paths:
        try:
            parent_dir = os.path.dirname(os.path.abspath(p))
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
            print(f"[+] Exported dashboard data -> {os.path.abspath(p)}")
        except Exception as e:
            print(f"[-] Warning: Failed to write {p}: {e}")

    # Write enriched CSV with dual schemas
    csv_headers = [
        "activity_id", "athlete_id", "athlete_name", "activity_type",
        "datetime_utc", "distance_km", "duration_minutes",
        "points", "points_dynamic", "points_legacy",
        "pace", "is_indoor", "activity_url"
    ]

    csv_destinations = [
        "activities.csv",
        "../activities.csv",
        "YEAR2026/activities.csv",
        "../YEAR2026/activities.csv",
        "web/activities.csv",
        "../web/activities.csv",
        "export/activities.csv",
        "../export/activities.csv"
    ]

    for dest in csv_destinations:
        try:
            dest_abs = os.path.abspath(dest)
            parent = os.path.dirname(dest_abs)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(dest_abs, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=csv_headers)
                writer.writeheader()
                for act in activities:
                    writer.writerow({
                        "activity_id": act["activity_id"],
                        "athlete_id": act["athlete_id"],
                        "athlete_name": act["athlete_name"],
                        "activity_type": act["activity_type"],
                        "datetime_utc": act["datetime_utc"],
                        "distance_km": act["distance_km"],
                        "duration_minutes": act["duration_minutes"],
                        "points": act["points"],
                        "points_dynamic": act["points_dynamic"],
                        "points_legacy": act["points_legacy"],
                        "pace": act["pace"],
                        "is_indoor": act["is_indoor"],
                        "activity_url": act["activity_url"]
                    })
            print(f"[+] Exported synced CSV -> {dest_abs}")
        except Exception as e:
            pass

    return payload

if __name__ == "__main__":
    generate_dashboard_json()
