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

def calculate_activity_points(activity_type: str, distance_km: float, duration_minutes: float, is_indoor: bool = False) -> float:
    t = str(activity_type).strip().lower()
    try:
        dist = float(distance_km or 0.0)
        dur = float(duration_minutes or 0.0)
    except Exception:
        dist, dur = 0.0, 0.0

    if t == "walk":
        return round(dist * 100, 2)
    elif t in ["run", "trail run"]:
        return round(dist * 120, 2)
    elif t in ["ride", "virtual ride", "ebike ride", "indoor ride"]:
        if dist > 0.0 and not is_indoor:
            return round(dist * 40, 2)
        else:
            # Indoor / Stationary ride duration-based points (10 pts/min, aligned with cardio workouts)
            return round(dur * 10, 2)
    else:
        # Default duration based multiplier (10 pts/min)
        return round(dur * 10, 2)

