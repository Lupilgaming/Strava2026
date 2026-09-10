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

def calculate_activity_points(activity_type: str, distance_km: float, duration_minutes: float) -> float:
    t = str(activity_type).strip().lower()
    if t == "walk":
        return round(distance_km * 100, 2)
    elif t in ["run", "trail run"]:
        return round(distance_km * 120, 2)
    elif t in ["ride", "virtual ride", "ebike ride"]:
        return round(distance_km * 40, 2)
    else:
        return round(duration_minutes * 10, 2)
