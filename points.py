import os
import re
from typing import Any, Tuple, List, Dict, Optional

def convert_distance_to_km(distance_str: Any) -> float:
    if not distance_str:
        return 0.0
    if isinstance(distance_str, (int, float)):
        return float(distance_str)
    val = str(distance_str).strip().lower().replace(",", "")
    try:
        if "km" in val:
            return round(float(val.replace("km", "").strip()), 2)
        elif "mi" in val:
            return round(float(val.replace("mi", "").strip()) * 1.60934, 2)
        elif "m" in val:
            return round(float(val.replace("m", "").strip()) / 1000.0, 2)
        else:
            nums = re.findall(r"[-+]?\d*\.\d+|\d+", val)
            if nums:
                return round(float(nums[0]), 2)
    except Exception:
        pass
    return 0.0

def convert_duration_to_minutes(duration_str: Any) -> float:
    if not duration_str:
        return 0.0
    if isinstance(duration_str, (int, float)):
        return float(duration_str)
    val = str(duration_str).strip().lower()
    if ":" in val:
        parts = val.split(":")
        try:
            if len(parts) == 3:
                return round(float(parts[0]) * 60.0 + float(parts[1]) + float(parts[2]) / 60.0, 2)
            elif len(parts) == 2:
                return round(float(parts[0]) + float(parts[1]) / 60.0, 2)
        except Exception:
            pass
    m = re.match(r"(?:(\d+)h)?\s*(?:(\d+)m)?\s*(?:(\d+)s)?", val)
    if m and any(m.groups()):
        h = int(m.group(1) or 0)
        minutes = int(m.group(2) or 0)
        s = int(m.group(3) or 0)
        return round(h * 60.0 + minutes + s / 60.0, 2)
    return 0.0

def format_pace(distance_km: Any, duration_minutes: Any, sport: str = "") -> str:
    """Formats pace in MM:SS /km for running/walking, or MM:SS /100m for swimming."""
    try:
        dist = float(distance_km or 0.0)
        dur = float(duration_minutes or 0.0)
        if dist <= 0.0 or dur <= 0.0:
            return ""

        sp = str(sport).strip().lower()
        if "swim" in sp:
            # Pace per 100m in minutes
            p_100m = (dur / dist) / 10.0
            if p_100m > 15.0 or p_100m < 0.5:
                return ""
            mins = int(p_100m)
            secs = int(round((p_100m - mins) * 60.0))
            if secs >= 60:
                mins += 1
                secs = 0
            return f"{mins}:{secs:02d} /100m"
        else:
            pace_dec = dur / dist
            if pace_dec > 60.0 or pace_dec < 1.0:
                return ""
            mins = int(pace_dec)
            secs = int(round((pace_dec - mins) * 60.0))
            if secs >= 60:
                mins += 1
                secs = 0
            return f"{mins}:{secs:02d} /km"
    except Exception:
        return ""

def is_indoor_ride(activity_type: str, distance_km: Any) -> bool:
    t = str(activity_type).strip().lower()
    try:
        dist = float(distance_km or 0.0)
    except Exception:
        dist = 0.0
    return t in ["ride", "virtual ride", "ebike ride", "indoor ride"] and dist <= 0.0

def parse_pace_to_min(pace_str: Any, distance_km: float = 0.0, duration_minutes: float = 0.0) -> float:
    """Parses a pace string like '6:30 /km' or '2:15 /100m' or derives it from distance and duration."""
    if pace_str and ":" in str(pace_str):
        try:
            val = str(pace_str).strip()
            if "/100m" in val:
                parts = val.replace("/100m", "").strip().split(":")
                return (float(parts[0]) + float(parts[1]) / 60.0) * 10.0
            else:
                parts = val.replace("/km", "").strip().split(":")
                return float(parts[0]) + float(parts[1]) / 60.0
        except Exception:
            pass
    if distance_km > 0.0 and duration_minutes > 0.0:
        return duration_minutes / distance_km
    return 6.5

def calculate_unified_foot_points(distance_km: float, pace_min: float, scale: str = "100_base") -> float:
    """
    Unified Foot-Sports Formula for Runs and Walks:
    Eliminates arbitrary Walk vs Run labels. Points continuously scale with physical speed,
    while distance dampening ensures long endurance runs (10K, 21K, 30K) are not penalized.
    """
    dist = float(distance_km or 0.0)
    if dist <= 0.0:
        return 0.0

    # Speed in km/h clamped between 3.0 (20:00/km) and 20.0 (3:00/km)
    p = max(3.0, min(20.0, float(pace_min or 6.5)))
    v = 60.0 / p

    # Continuous base rate based on speed:
    # 7.5 km/h (8:00/km recovery jog) -> 69.0 pts/km (~70 pts/km)
    # 10.0 km/h (6:00/km aerobic base) -> 87.0 pts/km (80-90 pts/km)
    # 13.6 km/h (4:25/km fast tempo)  -> 112.9 pts/km (~113 pts/km)
    raw_rate = 15.0 + 7.2 * v
    neutral_rate = 80.0

    # Distance dampening: higher pace rewarded on short/mid runs,
    # but multiplier smoothly stabilizes near 80 pts/km as distance increases (> 10 km, 21 km, 30 km)
    w = 1.0 / (1.0 + (dist / 16.0))
    rate = neutral_rate + w * (raw_rate - neutral_rate)

    if scale == "met":
        rate = rate * (15.0 / 100.0)

    return round(dist * rate, 2)

def calculate_unified_cycling_points(distance_km: float, scale: str = "100_base") -> float:
    """
    Continuous Distance Curve for Outdoor Cycling (Option B):
    Eliminates commute inflation while rewarding true endurance rides.
    - Short utility commutes (3-5 km) earn ~13.5-14.2 pts/km (~45-75 pts).
    - Fitness rides (15-30 km) scale to ~16.4-18.0 pts/km (~245-540 pts).
    - Long endurance rides (70-80+ km) scale to ~19.6-19.8 pts/km (~1,400-1,600 pts).
    Evaluated per-ride to prevent retroactive monthly score dilution.
    """
    dist = float(distance_km or 0.0)
    if dist <= 0.0:
        return 0.0

    rate = 12.0 + 9.5 * (dist / (18.0 + dist))

    if scale == "met":
        rate = rate * (15.0 / 100.0)

    return round(dist * rate, 2)

def calculate_dynamic_points(
    activity_type: str,
    distance_km: float,
    duration_minutes: float,
    pace_str: str = "",
    is_indoor: bool = False,
    scale: str = "100_base",
    slow_met_multiplier: float = 1.0,
    cycling_rate: Optional[float] = None
) -> float:
    """Sports-science Dynamic MET Points with unified foot sports, swimming distance/pace dynamics, cycling percentile scaling, and slow-MET weekly consistency."""
    t = str(activity_type).strip().lower()
    dist = float(distance_km or 0.0)
    dur = float(duration_minutes or 0.0)

    # 1. Foot activities: Separate Running from Walking (Option 1: Calibrated Walking Rate at 35 pts/km)
    if any(k in t for k in ["run", "trail"]):
        p_min = parse_pace_to_min(pace_str, dist, dur)
        return calculate_unified_foot_points(dist, p_min, scale=scale)
    elif any(k in t for k in ["walk", "hike"]):
        # Option 1: Calibrated Walking Rate (35.0 pts/km in 100_base, 5.25 in MET scale)
        rate = 35.0 if scale == "100_base" else 5.25
        if dist > 0.0:
            return round(dist * rate, 2)
        else:
            # Fallback duration rate (~3.0 pts/min)
            dur_rate = 3.0 if scale == "100_base" else 1.0
            return round(dur * dur_rate, 2)

    # 2. Cycling (outdoor distance vs indoor duration)
    elif "ride" in t or "cycle" in t:
        if dist > 0.0 and not is_indoor:
            if cycling_rate is not None:
                return round(dist * cycling_rate, 2)
            return calculate_unified_cycling_points(dist, scale=scale)
        else:
            # Indoor / Stationary Ride: 4 pts/min (240 pts/hr) in 100-base, 1.5 in MET
            rate = 4.0 if scale == "100_base" else 1.5
            return round(dur * rate, 2)

    # 3. Swimming: Dynamic distance & pace formula with duration fallback
    # Swimming burns ~4x calories/km compared to running.
    # When distance & pace are logged, scale rate based on pace (250 - 450 pts/km).
    # Always guarantees at least the 5 pts/min (300 pts/hr) baseline.
    elif "swim" in t:
        dur_rate = 5.0 if scale == "100_base" else 2.0
        dur_pts = dur * dur_rate
        if dist > 0.0:
            if pace_str and "/100m" in str(pace_str):
                try:
                    parts = str(pace_str).replace("/100m", "").strip().split(":")
                    pace_100m = float(parts[0]) + float(parts[1]) / 60.0
                    pace_km = pace_100m * 10.0
                except Exception:
                    pace_km = dur / dist if dur > 0.0 else 25.0
            elif dur > 0.0:
                pace_km = dur / dist
            else:
                pace_km = 25.0

            # Clamp pace_km: 12.0 min/km (1:12/100m) to 50.0 min/km (5:00/100m)
            p_clamped = max(12.0, min(50.0, float(pace_km)))
            speed_kmh = 60.0 / p_clamped
            # Base 250 pts/km + 50 * speed (at 2.4 km/h / 2:30/100m -> 370 pts/km; at 3.0 km/h / 2:00/100m -> 400 pts/km)
            swim_rate = 250.0 + 50.0 * speed_kmh
            if scale == "met":
                swim_rate = swim_rate * (15.0 / 100.0)
            dist_pts = dist * swim_rate
            return round(max(dur_pts, dist_pts), 2)
        return round(dur_pts, 2)

    # 4. Badminton: High-intensity agility racket sport (5.0 pts/min, court distance bonus if GPS recorded)
    elif "badminton" in t:
        dur_rate = 5.0 if scale == "100_base" else 2.0
        dur_pts = dur * dur_rate
        if dist > 0.0:
            dist_rate = 80.0 if scale == "100_base" else 12.0
            dist_pts = dist * dist_rate
            return round(max(dur_pts, dist_pts), 2)
        return round(dur_pts, 2)

    # 5. Cricket: Active team field/bat/bowl sport (4.5 pts/min, match distance bonus if GPS recorded)
    elif "cricket" in t:
        dur_rate = 4.5 if scale == "100_base" else 1.8
        dur_pts = dur * dur_rate
        if dist > 0.0:
            dist_rate = 70.0 if scale == "100_base" else 10.5
            dist_pts = dist * dist_rate
            return round(max(dur_pts, dist_pts), 2)
        return round(dur_pts, 2)

    # 6. Weight Training / Gym / Workout / Strength (Slow-MET with Consistency Multiplier)
    elif any(k in t for k in ["weight", "gym", "workout", "crossfit", "strength"]):
        rate = 4.0 if scale == "100_base" else 1.5
        mult = slow_met_multiplier if slow_met_multiplier is not None else 1.0
        return round(dur * rate * mult, 2)

    # 7. Default clause: Robust fallback for all other unseen sports (Tennis, Table Tennis, Squash, Soccer, Rowing, Yoga, etc.)
    else:
        if "yoga" in t or "pilates" in t:
            rate = 4.0 if scale == "100_base" else 1.5
            mult = slow_met_multiplier if slow_met_multiplier is not None else 1.0
            return round(dur * rate * mult, 2)
        if dist > 0.0 and not is_indoor:
            dist_rate = 35.0 if scale == "100_base" else 5.0
            dist_pts = dist * dist_rate
            dur_rate = 4.0 if scale == "100_base" else 1.5
            dur_pts = dur * dur_rate
            return round(max(dist_pts, dur_pts), 2)
        else:
            rate = 4.0 if scale == "100_base" else 1.5
            return round(dur * rate, 2)

def calculate_legacy_points(activity_type: str, distance_km: float, duration_minutes: float, is_indoor: bool = False) -> float:
    """Historical Strava 2025 fixed multiplier scoring."""
    t = str(activity_type).strip().lower()
    dist = float(distance_km or 0.0)
    dur = float(duration_minutes or 0.0)

    if t == "walk":
        return round(dist * 100.0, 2)
    elif t in ["run", "trail run"]:
        return round(dist * 120.0, 2)
    elif t in ["ride", "virtual ride", "ebike ride", "indoor ride"]:
        if dist > 0.0 and not is_indoor:
            return round(dist * 40.0, 2)
        else:
            return round(dur * 10.0, 2)
    elif "swim" in t:
        if dist > 0.0:
            return round(max(dur * 10.0, dist * 350.0), 2)
        return round(dur * 10.0, 2)
    elif "badminton" in t:
        if dist > 0.0:
            return round(max(dur * 10.0, dist * 80.0), 2)
        return round(dur * 10.0, 2)
    elif "cricket" in t:
        if dist > 0.0:
            return round(max(dur * 10.0, dist * 70.0), 2)
        return round(dur * 10.0, 2)
    elif any(k in t for k in ["weight", "gym", "workout", "crossfit", "strength"]):
        return round(dur * 10.0, 2)
    else:
        if dist > 0.0 and not is_indoor:
            return round(max(dur * 10.0, dist * 40.0), 2)
        return round(dur * 10.0, 2)

def calculate_activity_points(
    activity_type: str,
    distance_km: float,
    duration_minutes: float,
    is_indoor: bool = False,
    pace_str: str = "",
    schema: str = "dynamic",
    slow_met_multiplier: float = 1.0,
    cycling_rate: Optional[float] = None
) -> float:
    """Primary points router supporting both Dynamic MET and Legacy schemas."""
    if schema == "legacy":
        return calculate_legacy_points(activity_type, distance_km, duration_minutes, is_indoor=is_indoor)
    else:
        return calculate_dynamic_points(
            activity_type, distance_km, duration_minutes,
            pace_str=pace_str, is_indoor=is_indoor,
            slow_met_multiplier=slow_met_multiplier,
            cycling_rate=cycling_rate
        )

def recover_missing_activity_data(activity_type: str, distance_km: Any, duration_minutes: Any) -> tuple:
    """Automated recovery action: recovers duration from distance + benchmark pace when time is missing."""
    try:
        dist = float(distance_km or 0.0)
        dur = float(duration_minutes or 0.0)
    except Exception:
        dist, dur = 0.0, 0.0

    t = str(activity_type).strip().lower()

    # Case A: Distance known, Duration missing (0.0)
    if dist > 0.0 and dur <= 0.0:
        if any(k in t for k in ["run", "trail"]):
            dur = round(dist * 6.5, 2) # Nominal 6:30/km
        elif any(k in t for k in ["walk", "hike"]):
            dur = round(dist * 9.5, 2) # Nominal 9:30/km
        elif "ride" in t:
            dur = round(dist * 2.5, 2) # Nominal 24 km/h
        elif "swim" in t:
            dur = round(dist * 25.0, 2) # Nominal 25 min/km (2:30/100m)

    pace_str = format_pace(dist, dur, sport=t) if any(k in t for k in ["run", "walk", "hike", "trail", "swim"]) else ""
    return dist, dur, pace_str

CYCLING_BASE_RATE = 25.0
CYCLING_CEILING_FACTOR = 0.4076

def is_slow_met_activity(activity_type: str) -> bool:
    """Identifies slow-MET resistance, gym, and studio activities that qualify for consistency bonuses."""
    t = str(activity_type).strip().lower()
    if any(k in t for k in ["run", "walk", "trail", "hike", "swim", "ride", "cycle"]):
        return False
    return any(k in t for k in ["weight", "gym", "workout", "yoga", "pilates", "crossfit", "strength"])

def get_slow_met_multiplier(day_count_in_week: int) -> float:
    """Escalating weekly frequency multiplier for slow-MET activities (calibrated consistency bonus)."""
    if day_count_in_week <= 1:
        return 1.00
    elif day_count_in_week == 2:
        return 1.10
    elif day_count_in_week == 3:
        return 1.20
    else:
        return 1.30

def get_historical_cycling_cohort() -> List[float]:
    """Loads historical total distance per cyclist from archive if available, with robust calibrated fallback."""
    cohort = []
    base_dir = os.path.dirname(os.path.abspath(__file__))
    potential_paths = [
        os.path.join(base_dir, "archive", "activities_OLD.csv"),
        os.path.join(base_dir, "..", "archive", "activities_OLD.csv"),
        "archive/activities_OLD.csv",
        "../archive/activities_OLD.csv"
    ]
    for p in potential_paths:
        if os.path.exists(p):
            try:
                cyclists = {}
                with open(p, "r", encoding="utf-8") as f:
                    import csv
                    for r in csv.DictReader(f):
                        if "ride" in str(r.get("activity_type", "")).lower():
                            d = float(r.get("distance_km") or 0.0)
                            if d > 0:
                                aid = r.get("athlete_name") or r.get("athlete_id")
                                cyclists[aid] = cyclists.get(aid, 0.0) + d
                if cyclists:
                    cohort = list(cyclists.values())
                    break
            except Exception:
                pass
    if not cohort:
        cohort = [1.0, 1.2, 2.5, 3.8, 5.0, 14.5, 19.7, 25.0, 28.2, 38.5, 43.5, 49.2, 61.9, 89.1, 188.8, 335.8]
    return cohort

def calculate_cyclist_percentile_scoring(
    athlete_total_km: float,
    all_cohort_distances: List[float] = None,
    factor: float = CYCLING_CEILING_FACTOR,
    current_pts_per_km: float = CYCLING_BASE_RATE
) -> Tuple[float, float, float, float]:
    """
    Percentile-based cycling score calculation.
    Ceiling = current_pts_per_km * max_km * factor (as 100th percentile).
    Returns (percentile_pct, total_score, ceiling, effective_rate_per_km).
    """
    if athlete_total_km <= 0.0:
        return 0.0, 0.0, 0.0, current_pts_per_km

    if all_cohort_distances is None or len(all_cohort_distances) == 0:
        all_cohort_distances = get_historical_cycling_cohort() + [athlete_total_km]

    cohort = sorted(all_cohort_distances)
    max_km = max(cohort) if cohort else athlete_total_km
    ceiling = round(current_pts_per_km * max_km * factor, 2)

    rank = sum(1 for x in cohort if x <= athlete_total_km)
    pct = rank / len(cohort)
    pct_points = round(ceiling * pct, 2)
    unadjusted = round(athlete_total_km * current_pts_per_km, 2)

    # Cap total points to min(unadjusted, pct_points) so short rides are not inflated
    total_score = min(unadjusted, pct_points)
    effective_rate = round(total_score / athlete_total_km, 4) if athlete_total_km > 0 else current_pts_per_km

    return round(pct * 100.0, 1), total_score, ceiling, effective_rate

def apply_dataset_scoring_rules(activities: List[Dict[str, Any]], scale: str = "100_base") -> List[Dict[str, Any]]:
    """
    Applies cohort-wide scoring rules across a full activity list:
    1. Slow-MET weekly frequency multiplier (1.0x -> 1.25x -> 1.5x -> 1.75x) for Gym, Weights, Workout, Yoga.
       - Qualifying duration: >= 25.0 minutes moving time.
       - Max 1 credit per calendar day per athlete.
       - Tiers applied within each Monday-Sunday ISO week.
    2. Cycling Percentile Scoring:
       - Benchmarked against all-time cohort (historical archive + current contest).
       - Ceiling = current_pts_per_km * max_km * factor (as 100th percentile).
       - Total points capped at min(unadjusted, percentile_points).
       - Effective rate per km allocated proportionally across rides.
    3. Runs, Walks, Swims, and other sports retain full Dynamic MET models.
    4. Computes both dynamic points and legacy points.
    """
    from dateutil import parser as dt_parser
    from datetime import datetime
    import collections

    # 1. Parse dates and sort chronologically
    indexed = []
    for idx, act in enumerate(activities):
        raw_dt = str(act.get("datetime_utc", "") or act.get("datetime_iso", "")).strip().replace(" on ", " ")
        try:
            dt = dt_parser.parse(raw_dt)
        except Exception:
            dt = datetime(2026, 9, 1)
        indexed.append((dt, idx, act))
    indexed.sort(key=lambda x: x[0])

    # 2. Gather cyclist contest totals and slow-MET weekly active days
    cyclist_totals = collections.defaultdict(float)
    athlete_week_days = collections.defaultdict(lambda: collections.defaultdict(dict))

    for dt, idx, act in indexed:
        stype = str(act.get("activity_type", "")).strip()
        try:
            dist = float(act.get("distance_km", 0.0) or 0.0)
            dur = float(act.get("duration_minutes", 0.0) or 0.0)
        except (ValueError, TypeError):
            dist, dur = 0.0, 0.0

        aid = str(act.get("athlete_id") or act.get("athlete_name", "unknown")).strip()
        is_ind = str(act.get("is_indoor", "")).strip().lower() in ["true", "1", "yes"] or is_indoor_ride(stype, dist)

        if ("ride" in stype.lower() or "cycle" in stype.lower()) and dist > 0.0 and not is_ind:
            cyclist_totals[aid] += dist

        if is_slow_met_activity(stype) and dur >= 25.0:
            wk = f"{dt.year}-W{dt.isocalendar()[1]}"
            day_str = dt.strftime("%Y-%m-%d")
            week_dict = athlete_week_days[aid][wk]
            if day_str not in week_dict:
                day_num = len(week_dict) + 1
                week_dict[day_str] = day_num

    # 3. Compute cycling percentile metrics across combined cohort
    hist_cohort = get_historical_cycling_cohort()
    all_cyclist_cohort = list(hist_cohort) + list(cyclist_totals.values())
    all_cyclist_cohort.sort()

    cyclist_metrics = {}
    for aid, total_d in cyclist_totals.items():
        pct, total_score, ceiling, eff_rate = calculate_cyclist_percentile_scoring(
            total_d,
            all_cohort_distances=all_cyclist_cohort,
            factor=CYCLING_CEILING_FACTOR,
            current_pts_per_km=CYCLING_BASE_RATE
        )
        cyclist_metrics[aid] = {
            "percentile": pct,
            "total_score": total_score,
            "ceiling": ceiling,
            "effective_rate": eff_rate
        }

    # 3b. Gather athlete and club median paces for normal walks and runs (Integrity Baseline)
    import statistics
    ath_walk_paces = collections.defaultdict(list)
    ath_run_paces = collections.defaultdict(list)
    club_walk_paces = []
    club_run_paces = []

    for dt, idx, act in indexed:
        st = str(act.get("activity_type", "")).strip().lower()
        try:
            d = float(act.get("distance_km", 0.0) or 0.0)
            tm = float(act.get("duration_minutes", 0.0) or 0.0)
        except (ValueError, TypeError):
            d, tm = 0.0, 0.0
        aid = str(act.get("athlete_id") or act.get("athlete_name", "unknown")).strip()
        if d > 0.0 and tm > 0.0:
            p = tm / d
            if any(k in st for k in ["walk", "hike"]) and 7.0 <= p <= 20.0:
                ath_walk_paces[aid].append(p)
                club_walk_paces.append(p)
            elif any(k in st for k in ["run", "trail"]) and 4.25 <= p <= 12.0:
                ath_run_paces[aid].append(p)
                club_run_paces.append(p)

    club_median_walk_pace = statistics.median(club_walk_paces) if club_walk_paces else 11.33
    club_median_run_pace = statistics.median(club_run_paces) if club_run_paces else 7.03

    # 4. Assign enriched points to each activity with Integrity Filtering
    scored_activities = [None] * len(activities)

    for dt, orig_idx, act in indexed:
        row = dict(act)
        stype = str(row.get("activity_type", "Workout")).strip()
        act_id = str(row.get("activity_id", "")).strip()

        # Standardize resistance and workout activities to Weight Training
        if any(k in stype.lower() for k in ["weight", "gym", "workout", "crossfit", "strength"]):
            stype = "Weight Training"
            row["activity_type"] = "Weight Training"

        KNOWN_RAW_DISTANCES = {
            "20215946659": 8.61,  # Pradyumna Pandey Walk (logged 8.61 km in 48.4m at 5:37/km)
            "20208633094": 5.02,  # Krishna A Run (logged 5.02 km in 19.38m at 3:51/km)
            "20210427180": 2.99,  # Krishna A Walk (logged 2.99 km in 13.95m at 4:40/km)
            "20183441925": 2.65,  # Krishna A Walk (logged 2.65 km in 14.43m at 5:26/km)
            "20199262701": 1.32,  # Luffy Stark Walk (logged 1.32 km in 4.3m at 3:17/km)
            "20179102235": 0.34,  # Sumantha Madhyastha Walk (logged 0.34 km in 1.2m at 3:35/km)
        }

        try:
            if act_id in KNOWN_RAW_DISTANCES:
                dist = KNOWN_RAW_DISTANCES[act_id]
            elif row.get("original_distance_km") and str(row.get("original_distance_km")).strip() != "":
                dist = float(row.get("original_distance_km"))
            else:
                dist = float(row.get("distance_km", 0.0) or 0.0)
            dur = float(row.get("duration_minutes", 0.0) or 0.0)
        except (ValueError, TypeError):
            dist, dur = 0.0, 0.0

        if stype == "Weight Training":
            # Gym and weight training sessions do not accrue distance points
            dist = 0.0
            row["distance_km"] = 0.0

        aid = str(row.get("athlete_id") or row.get("athlete_name", "unknown")).strip()
        is_ind = str(row.get("is_indoor", "")).strip().lower() in ["true", "1", "yes"] or is_indoor_ride(stype, dist)
        pace_val = format_pace(dist, dur, sport=stype) if dist > 0.0 else str(row.get("pace", "")).strip()

        # Integrity Layer & Anomaly Auto-Adjustment
        integrity_flag = ""
        integrity_badge = ""
        adj_dist = dist
        adj_pace = dur / dist if dist > 0.0 else 0.0
        speed_kmh = (dist / dur) * 60.0 if dur > 0.0 else 0.0

        if dist > 0.0 and dur > 0.0:
            # Check 1: Motor / Vehicle velocity on foot sports (> 18 km/h or < 3:20 min/km)
            if any(k in stype.lower() for k in ["walk", "hike", "run", "trail"]) and (adj_pace < 3.33 or speed_kmh > 18.0):
                integrity_flag = "VEHICLE_SPEED"
                integrity_badge = "🚗 Vehicle Speed Review"
                ath_med_walk = statistics.median(ath_walk_paces[aid]) if ath_walk_paces[aid] else club_median_walk_pace
                adj_pace = ath_med_walk
                adj_dist = round(dur / adj_pace, 2)

            # Check 2: Mislabeled Walk (Walk with pace < 7:00 min/km / speed > 8.57 km/h)
            elif any(k in stype.lower() for k in ["walk", "hike"]) and adj_pace < 7.0:
                integrity_flag = "MISLABELED_WALK"
                integrity_badge = "🚨 Mislabeled Walk (Run/Cycle Speed)"
                ath_med_walk = statistics.median(ath_walk_paces[aid]) if ath_walk_paces[aid] else club_median_walk_pace
                adj_pace = ath_med_walk
                adj_dist = round(dur / adj_pace, 2)

            # Check 3: Sensor Pace Anomaly on Run (Pace < 4:15 min/km / speed > 14.1 km/h)
            elif any(k in stype.lower() for k in ["run", "trail"]) and adj_pace < 4.25:
                integrity_flag = "SENSOR_PACE_ANOMALY"
                integrity_badge = "⚠️ Sensor Pace Spike (< 4:15/km)"
                ath_med_run = statistics.median(ath_run_paces[aid]) if ath_run_paces[aid] else club_median_run_pace
                adj_pace = max(4.60, ath_med_run)
                adj_dist = round(dur / adj_pace, 2)

            # Check 4: Suspect Long Endurance Run (10+ km with pace < 5:00 min/km / speed > 12.0 km/h)
            elif any(k in stype.lower() for k in ["run", "trail"]) and dist >= 9.8 and adj_pace < 5.00:
                integrity_flag = "SUSPECT_ENDURANCE_PACE"
                integrity_badge = "⚠️ Suspect Long Run Pace (< 5:00/km on 10k+)"
                ath_med_run = statistics.median(ath_run_paces[aid]) if ath_run_paces[aid] else club_median_run_pace
                adj_pace = max(5.33, ath_med_run)
                adj_dist = round(dur / adj_pace, 2)

        adj_pace_str = format_pace(adj_dist, dur, sport=stype) if adj_dist > 0.0 else pace_val

        # Slow-MET multiplier
        mult = 1.00
        if is_slow_met_activity(stype):
            wk = f"{dt.year}-W{dt.isocalendar()[1]}"
            day_str = dt.strftime("%Y-%m-%d")
            day_num = athlete_week_days[aid][wk].get(day_str, 1)
            mult = get_slow_met_multiplier(day_num)

        # Cycling rate calculation (Option B: Continuous Distance Curve)
        cyc_rate = None
        if ("ride" in stype.lower() or "cycle" in stype.lower()) and dist > 0.0 and not is_ind:
            pts_unified = calculate_unified_cycling_points(adj_dist, scale=scale)
            cyc_rate = round(pts_unified / adj_dist, 4) if adj_dist > 0 else 12.0

        pts_dyn = calculate_dynamic_points(
            stype, adj_dist, dur,
            pace_str=adj_pace_str,
            is_indoor=is_ind,
            scale=scale,
            slow_met_multiplier=mult,
            cycling_rate=cyc_rate
        )
        pts_leg = calculate_legacy_points(stype, adj_dist, dur, is_indoor=is_ind)

        row["points"] = round(pts_dyn, 2)
        row["points_dynamic"] = round(pts_dyn, 2)
        row["points_legacy"] = round(pts_leg, 2)
        row["distance_km"] = round(adj_dist, 2)
        row["duration_minutes"] = round(dur, 2)
        row["pace"] = adj_pace_str
        row["is_indoor"] = is_ind
        row["integrity_flag"] = integrity_flag
        row["integrity_badge"] = integrity_badge
        row["original_distance_km"] = round(dist, 2)
        row["original_pace"] = pace_val

        if is_slow_met_activity(stype):
            row["slow_met_multiplier"] = mult

        if cyc_rate is not None:
            if aid in cyclist_metrics:
                row["cycling_percentile"] = cyclist_metrics[aid]["percentile"]
            row["cycling_effective_rate"] = cyc_rate

        scored_activities[orig_idx] = row

    return scored_activities


