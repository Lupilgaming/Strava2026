import re
from typing import Any

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

def format_pace(distance_km: Any, duration_minutes: Any) -> str:
    """Formats pace in MM:SS /km for running and walking activities."""
    try:
        dist = float(distance_km or 0.0)
        dur = float(duration_minutes or 0.0)
        if dist <= 0.0 or dur <= 0.0:
            return ""
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
    """Parses a pace string like '6:30 /km' or derives it from distance and duration."""
    if pace_str and ":" in str(pace_str):
        try:
            parts = str(pace_str).replace("/km", "").strip().split(":")
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
    # 12 km/h (5:00/km) -> 114 pts/km
    # 10 km/h (6:00/km) -> 100 pts/km (standard run baseline)
    # 7.5 km/h (8:00/km) -> 82.5 pts/km (easy jog / power walk)
    # 6.0 km/h (10:00/km) -> 72.0 pts/km (brisk walk)
    # 4.5 km/h (13:20/km) -> 61.5 pts/km (casual walk)
    raw_rate = 30.0 + 7.0 * v
    neutral_rate = 85.0

    # Distance dampening: higher pace rewarded on short/mid runs,
    # but multiplier smoothly stabilizes near 1.0 as distance increases (> 10 km, 21 km, 30 km)
    w = 1.0 / (1.0 + (dist / 12.0))
    rate = neutral_rate + w * (raw_rate - neutral_rate)

    if scale == "met":
        rate = rate * (15.0 / 100.0)

    return round(dist * rate, 2)

def calculate_dynamic_points(
    activity_type: str,
    distance_km: float,
    duration_minutes: float,
    pace_str: str = "",
    is_indoor: bool = False,
    scale: str = "100_base"
) -> float:
    """Sports-science Dynamic MET Points with unified foot sports and equitable cardio ratios."""
    t = str(activity_type).strip().lower()
    dist = float(distance_km or 0.0)
    dur = float(duration_minutes or 0.0)

    # 1. Foot activities: Runs, Walks, Hikes seamlessly unified by pace & distance
    if any(k in t for k in ["run", "walk", "hike"]):
        p_min = parse_pace_to_min(pace_str, dist, dur)
        return calculate_unified_foot_points(dist, p_min, scale=scale)

    # 2. Cycling
    elif "ride" in t:
        if dist > 0.0 and not is_indoor:
            rate = 25.0 if scale == "100_base" else 4.0
            return round(dist * rate, 2)
        else:
            # Indoor / Stationary Ride: 4 pts/min (240 pts/hr) in 100-base, 1.5 in MET
            rate = 4.0 if scale == "100_base" else 1.5
            return round(dur * rate, 2)

    # 3. Swimming: 5 pts/min (300 pts/hr) in 100-base, 2.0 in MET
    elif "swim" in t:
        rate = 5.0 if scale == "100_base" else 2.0
        return round(dur * rate, 2)

    # 4. Weight Training / Gym / Workout: 4 pts/min (240 pts/hr) in 100-base, 1.5 in MET
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
    else:
        return round(dur * 10.0, 2)

def calculate_activity_points(
    activity_type: str,
    distance_km: float,
    duration_minutes: float,
    is_indoor: bool = False,
    pace_str: str = "",
    schema: str = "dynamic"
) -> float:
    """Primary points router supporting both Dynamic MET and Legacy schemas."""
    if schema == "legacy":
        return calculate_legacy_points(activity_type, distance_km, duration_minutes, is_indoor=is_indoor)
    else:
        return calculate_dynamic_points(activity_type, distance_km, duration_minutes, pace_str=pace_str, is_indoor=is_indoor)

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
            dur = round((dist / 1000.0) * 25.0, 2) # 25 min/km

    pace_str = format_pace(dist, dur) if any(k in t for k in ["run", "walk", "hike", "trail"]) else ""
    return dist, dur, pace_str


