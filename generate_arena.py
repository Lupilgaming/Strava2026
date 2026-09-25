import os
import json
import csv
import shutil
from datetime import datetime

ROOT_DIR = r"C:\Users\ds-ga\Documents\automations\strava club download"
YEAR_DIR = os.path.join(ROOT_DIR, "YEAR2026")
WEB_DIR = os.path.join(ROOT_DIR, "web")
EXPORT_DIR = os.path.join(ROOT_DIR, "export")

SQUAD_METAS = [
    {"id": 0, "name": "Red Phoenix", "color": "#ef4444", "bg": "rgba(239, 68, 68, 0.12)", "border": "rgba(239, 68, 68, 0.35)", "icon": "🔴"},
    {"id": 1, "name": "Blue Hydra", "color": "#3b82f6", "bg": "rgba(59, 130, 246, 0.12)", "border": "rgba(59, 130, 246, 0.35)", "icon": "🔵"},
    {"id": 2, "name": "Emerald Dragons", "color": "#10b981", "bg": "rgba(16, 185, 129, 0.12)", "border": "rgba(16, 185, 129, 0.35)", "icon": "🟢"},
    {"id": 3, "name": "Golden Gryphons", "color": "#f59e0b", "bg": "rgba(245, 158, 11, 0.12)", "border": "rgba(245, 158, 11, 0.35)", "icon": "🟡"},
    {"id": 4, "name": "Shadow Vipers", "color": "#a855f7", "bg": "rgba(168, 85, 247, 0.12)", "border": "rgba(168, 85, 247, 0.35)", "icon": "🟣"},
    {"id": 5, "name": "Solar Titans", "color": "#f97316", "bg": "rgba(249, 115, 22, 0.12)", "border": "rgba(249, 115, 22, 0.35)", "icon": "🟠"},
    {"id": 6, "name": "Silver Wolves", "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.12)", "border": "rgba(148, 163, 184, 0.35)", "icon": "⚪"},
    {"id": 7, "name": "Neon Cyber", "color": "#06b6d4", "bg": "rgba(6, 182, 212, 0.12)", "border": "rgba(6, 182, 212, 0.35)", "icon": "🔷"},
    {"id": 8, "name": "Thunder Hawks", "color": "#eab308", "bg": "rgba(234, 179, 8, 0.12)", "border": "rgba(234, 179, 8, 0.35)", "icon": "⚡"},
    {"id": 9, "name": "Magma Giants", "color": "#dc2626", "bg": "rgba(220, 38, 38, 0.12)", "border": "rgba(220, 38, 38, 0.35)", "icon": "🌋"},
    {"id": 10, "name": "Frost Phantoms", "color": "#38bdf8", "bg": "rgba(56, 189, 248, 0.12)", "border": "rgba(56, 189, 248, 0.35)", "icon": "❄️"},
    {"id": 11, "name": "Iron Rangers", "color": "#84cc16", "bg": "rgba(132, 204, 22, 0.12)", "border": "rgba(132, 204, 22, 0.35)", "icon": "🏹"},
    {"id": 12, "name": "Tidal Krakens", "color": "#2563eb", "bg": "rgba(37, 99, 235, 0.12)", "border": "rgba(37, 99, 235, 0.35)", "icon": "🌊"},
    {"id": 13, "name": "Forest Striders", "color": "#059669", "bg": "rgba(5, 150, 105, 0.12)", "border": "rgba(5, 150, 105, 0.35)", "icon": "🌲"},
    {"id": 14, "name": "Cosmic Nova", "color": "#ec4899", "bg": "rgba(236, 72, 153, 0.12)", "border": "rgba(236, 72, 153, 0.35)", "icon": "🌌"},
    {"id": 15, "name": "Aegis Knights", "color": "#64748b", "bg": "rgba(100, 116, 139, 0.12)", "border": "rgba(100, 116, 139, 0.35)", "icon": "🛡️"},
    {"id": 16, "name": "Vortex Storm", "color": "#8b5cf6", "bg": "rgba(139, 92, 246, 0.12)", "border": "rgba(139, 92, 246, 0.35)", "icon": "🌪️"},
    {"id": 17, "name": "Orbit Centurions", "color": "#d97706", "bg": "rgba(217, 119, 6, 0.12)", "border": "rgba(217, 119, 6, 0.35)", "icon": "🪐"},
    {"id": 18, "name": "Mystic Sorcerers", "color": "#c084fc", "bg": "rgba(192, 132, 252, 0.12)", "border": "rgba(192, 132, 252, 0.35)", "icon": "🔮"},
    {"id": 19, "name": "Apex Predators", "color": "#b91c1c", "bg": "rgba(185, 28, 28, 0.12)", "border": "rgba(185, 28, 28, 0.35)", "icon": "🦁"}
]

def precalculate_all_squads(activities, members):
    def aggregate_stats(act_list):
        stats = {}
        for m in members:
            stats[m] = {
                "name": m,
                "points": 0.0,
                "distance": 0.0,
                "activities": 0,
                "sports": {},
                "max_single_dist": 0.0,
                "max_single_dur": 0.0,
                "fastest_pace_val": 999.0,
                "fastest_pace_str": "N/A",
                "night_owl": 0,
                "dawn_patrol": 0
            }
        for act in act_list:
            name = act.get("athlete_name", "").strip()
            if not name:
                continue
            if name not in stats:
                stats[name] = {
                    "name": name,
                    "points": 0.0,
                    "distance": 0.0,
                    "activities": 0,
                    "sports": {},
                    "max_single_dist": 0.0,
                    "max_single_dur": 0.0,
                    "fastest_pace_val": 999.0,
                    "fastest_pace_str": "N/A",
                    "night_owl": 0,
                    "dawn_patrol": 0
                }
            st = stats[name]
            pts = float(act.get("points_dynamic") or act.get("points") or 0.0)
            dist = float(act.get("distance_km") or 0.0)
            dur = float(act.get("duration_minutes") or 0.0)
            st["points"] += pts
            st["distance"] += dist
            st["activities"] += 1
            sp = act.get("activity_type") or "Other"
            st["sports"][sp] = st["sports"].get(sp, 0) + 1
            if dist > st["max_single_dist"]:
                st["max_single_dist"] = dist
            if dur > st["max_single_dur"]:
                st["max_single_dur"] = dur

            iso = act.get("datetime_iso") or act.get("datetime_utc") or ""
            if iso:
                try:
                    d = datetime.fromisoformat(iso)
                    if d.hour >= 20:
                        st["night_owl"] += 1
                    elif d.hour < 7 or (d.hour == 7 and d.minute <= 30):
                        st["dawn_patrol"] += 1
                except Exception:
                    pass

            if "run" in sp.lower() and dist >= 2.5 and dur > 0:
                pace_dec = dur / dist
                if 2.5 < pace_dec < st["fastest_pace_val"]:
                    st["fastest_pace_val"] = pace_dec
                    st["fastest_pace_str"] = act.get("pace") or f"{int(pace_dec)}:{int((pace_dec%1)*60):02d} /km"

        # Classify
        for st in stats.values():
            sc = len(st["sports"])
            if sc >= 2:
                st["hero_class"] = "🧙‍♂️ Polymath"
                st["hero_color"] = "#38bdf8"
            elif st["fastest_pace_val"] < 5.4:
                st["hero_class"] = "⚡ Assassin"
                st["hero_color"] = "#a855f7"
            elif st["distance"] >= 25.0 or st["max_single_dist"] >= 10.0:
                st["hero_class"] = "🏹 Ranger"
                st["hero_color"] = "#22c55e"
            elif "Weight Training" in st["sports"] or "Workout" in st["sports"] or "Swim" in st["sports"] or st["max_single_dur"] >= 60.0:
                st["hero_class"] = "🏋️ Berserker"
                st["hero_color"] = "#ef4444"
            else:
                st["hero_class"] = "🛡️ Sentinel"
                st["hero_color"] = "#fbbf24"
        return stats

    def balance_k(k, stats_map):
        active = [m for m in members if stats_map[m]["points"] > 0]
        active.sort(key=lambda m: (stats_map[m]["points"], stats_map[m]["distance"]), reverse=True)
        inactive = [m for m in members if stats_map[m]["points"] == 0]
        inactive.sort(key=lambda m: m.lower())

        squads = [[] for _ in range(k)]
        squad_pts = [0.0 for _ in range(k)]

        for ath in active:
            min_sq = min(range(k), key=lambda i: squad_pts[i])
            squads[min_sq].append(ath)
            squad_pts[min_sq] += stats_map[ath]["points"]

        for _ in range(50):
            max_sq = max(range(k), key=lambda i: squad_pts[i])
            min_sq = min(range(k), key=lambda i: squad_pts[i])
            diff = squad_pts[max_sq] - squad_pts[min_sq]
            if diff <= 5:
                break
            best_swap = None
            best_diff = diff
            for a_i, ath_a in enumerate(squads[max_sq]):
                p_a = stats_map[ath_a]["points"]
                for b_i, ath_b in enumerate(squads[min_sq]):
                    p_b = stats_map[ath_b]["points"]
                    change = p_a - p_b
                    if change > 0:
                        new_diff = abs((squad_pts[max_sq] - change) - (squad_pts[min_sq] + change))
                        if new_diff < best_diff:
                            best_diff = new_diff
                            best_swap = (a_i, b_i, change)
            if best_swap and best_diff < diff - 2:
                a_i, b_i, change = best_swap
                squads[max_sq][a_i], squads[min_sq][b_i] = squads[min_sq][b_i], squads[max_sq][a_i]
                squad_pts[max_sq] -= change
                squad_pts[min_sq] += change
            else:
                break

        for ath in inactive:
            min_len_sq = min(range(k), key=lambda i: len(squads[i]))
            squads[min_len_sq].append(ath)

        return squads

    act_tourn = [a for a in activities if (a.get("datetime_iso") or "")[:10] >= "2026-09-14"]
    stats_tourn = aggregate_stats(act_tourn)
    stats_all = aggregate_stats(activities)

    precalc_dict = {
        "tournament": {},
        "all_time": {}
    }

    for k in range(2, 21):
        precalc_dict["tournament"][k] = balance_k(k, stats_tourn)
        precalc_dict["all_time"][k] = balance_k(k, stats_all)

    return precalc_dict

def build_arena(root_dir=None, year_dir=None, web_dir=None, export_dir=None):
    if root_dir is None:
        root_dir = ROOT_DIR
    if year_dir is None:
        year_dir = os.path.join(root_dir, "YEAR2026")
    if web_dir is None:
        web_dir = os.path.join(root_dir, "web")
    if export_dir is None:
        export_dir = os.path.join(root_dir, "export")

    json_path = os.path.join(root_dir, "dashboard_data.json")
    if not os.path.exists(json_path):
        json_path = os.path.join(year_dir, "dashboard_data.json")

    with open(json_path, "r", encoding="utf-8") as f:
        dashboard_data = json.load(f)

    # Load memberlist
    member_csv = os.path.join(root_dir, "memberlist.csv")
    if not os.path.exists(member_csv):
        member_csv = os.path.join(year_dir, "memberlist.csv")

    members = []
    if os.path.exists(member_csv):
        with open(member_csv, "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                m_name = r.get("athlete_name", "").strip()
                if m_name and m_name not in members:
                    members.append(m_name)

    if not members and dashboard_data.get("athletes"):
        members = [a["athlete_name"] for a in dashboard_data["athletes"]]

    # Precalculate squads for k=2..20
    precalculated = precalculate_all_squads(dashboard_data.get("activities", []), members)
    precalc_json_str = json.dumps(precalculated)

    json_str = json.dumps(dashboard_data, indent=2)

    # HTML Template begins
    arena_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  <title>The Arena • Strava 2026 Gamification Hub & Team Builder</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Outfit:wght@500;600;700;800;900&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {
      --bg-dark: #090d16;
      --card-bg: rgba(26, 35, 52, 0.75);
      --card-border: rgba(255, 255, 255, 0.08);
      --card-hover-border: rgba(252, 76, 2, 0.45);
      --strava-orange: #fc4c02;
      --strava-orange-light: #ff6a2b;
      --orange-glow: rgba(252, 76, 2, 0.4);
      --text-primary: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --gold: #fbbf24;
      --gold-glow: rgba(251, 191, 36, 0.35);
      --silver: #cbd5e1;
      --silver-glow: rgba(203, 213, 225, 0.25);
      --bronze: #d97706;
      --accent-blue: #38bdf8;
      --accent-green: #22c55e;
      --accent-purple: #a855f7;
      --fighter-red: #ef4444;
      --fighter-blue: #3b82f6;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    body {
      background-color: var(--bg-dark);
      background-image: 
        radial-gradient(at 0% 0%, rgba(252, 76, 2, 0.16) 0px, transparent 45%),
        radial-gradient(at 100% 100%, rgba(56, 189, 248, 0.12) 0px, transparent 45%),
        radial-gradient(at 50% 30%, rgba(168, 85, 247, 0.06) 0px, transparent 50%);
      color: var(--text-primary);
      min-height: 100vh;
      padding-bottom: 80px;
      overflow-x: hidden;
    }

    ::-webkit-scrollbar {
      width: 8px;
      height: 8px;
    }
    ::-webkit-scrollbar-track {
      background: #0b1120;
    }
    ::-webkit-scrollbar-thumb {
      background: #334155;
      border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: var(--strava-orange);
    }

    /* Navbar */
    .navbar {
      background: rgba(15, 23, 42, 0.88);
      backdrop-filter: blur(18px);
      -webkit-backdrop-filter: blur(18px);
      border-bottom: 1px solid var(--card-border);
      position: sticky;
      top: 0;
      z-index: 100;
      padding: 12px 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
      flex-wrap: wrap;
      gap: 12px;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 14px;
      text-decoration: none;
      color: var(--text-primary);
    }

    .brand-logo {
      width: 40px;
      height: 40px;
      background: linear-gradient(135deg, #a855f7, #ec4899);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 18px rgba(168, 85, 247, 0.5);
    }

    .brand-title {
      font-family: 'Outfit', sans-serif;
      font-size: 20px;
      font-weight: 800;
      letter-spacing: -0.5px;
      background: linear-gradient(90deg, #ffffff, #e2e8f0);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .brand-subtitle {
      font-size: 11px;
      color: var(--accent-purple);
      text-transform: uppercase;
      letter-spacing: 1px;
      font-weight: 700;
    }

    .nav-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .btn {
      padding: 8px 16px;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.2s ease;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 7px;
    }

    .btn-outline {
      background: rgba(30, 41, 59, 0.6);
      border-color: var(--card-border);
      color: var(--text-primary);
    }
    .btn-outline:hover {
      border-color: var(--strava-orange);
      color: var(--strava-orange);
      transform: translateY(-1px);
    }

    .btn-orange {
      background: linear-gradient(135deg, #fc4c02, #ff6a2b);
      color: #fff;
      box-shadow: 0 4px 14px var(--orange-glow);
    }
    .btn-orange:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px var(--orange-glow);
    }

    /* Container */
    .container {
      max-width: 1340px;
      margin: 0 auto;
      padding: 24px 20px;
    }

    /* Hero Banner */
    .arena-hero {
      background: linear-gradient(135deg, rgba(168, 85, 247, 0.15) 0%, rgba(252, 76, 2, 0.15) 50%, rgba(56, 189, 248, 0.1) 100%);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 24px;
      padding: 28px 32px;
      margin-bottom: 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 20px;
      position: relative;
      overflow: hidden;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.4);
    }

    .arena-hero::after {
      content: '⚡';
      position: absolute;
      right: -15px;
      bottom: -35px;
      font-size: 160px;
      opacity: 0.04;
      pointer-events: none;
      font-weight: 900;
    }

    .arena-hero-title {
      font-family: 'Outfit', sans-serif;
      font-size: 30px;
      font-weight: 900;
      color: #fff;
      margin-bottom: 6px;
      letter-spacing: -0.5px;
    }

    .arena-hero-sub {
      font-size: 13.5px;
      color: var(--text-muted);
      max-width: 680px;
      line-height: 1.6;
    }

    /* Date Filter Widget */
    .date-filter-bar {
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(12px);
      border: 1px solid var(--card-border);
      border-radius: 18px;
      padding: 14px 20px;
      margin-bottom: 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 14px;
      box-shadow: 0 4px 18px rgba(0,0,0,0.3);
    }

    .filter-left {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }

    .filter-label {
      font-size: 13px;
      font-weight: 700;
      color: var(--text-primary);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .preset-group {
      display: flex;
      background: rgba(30, 41, 59, 0.6);
      padding: 3px;
      border-radius: 10px;
      border: 1px solid var(--card-border);
      gap: 4px;
    }

    .preset-pill {
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 5px 12px;
      border-radius: 7px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }
    .preset-pill:hover {
      color: #fff;
    }
    .preset-pill.active {
      background: var(--strava-orange);
      color: #fff;
      box-shadow: 0 2px 8px var(--orange-glow);
    }

    .filter-right {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }

    .date-input-wrap {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      color: var(--text-muted);
    }

    .date-input {
      background: #0f172a;
      border: 1px solid var(--card-border);
      color: #fff;
      padding: 5px 10px;
      border-radius: 8px;
      font-size: 12px;
      outline: none;
      transition: border 0.2s;
    }
    .date-input:focus {
      border-color: var(--strava-orange);
    }

    .activity-count-badge {
      background: rgba(34, 197, 94, 0.15);
      border: 1px solid rgba(34, 197, 94, 0.35);
      color: var(--accent-green);
      font-size: 11.5px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 8px;
      white-space: nowrap;
    }

    /* Arena Navigation Tabs */
    .arena-nav-bar {
      display: flex;
      gap: 10px;
      overflow-x: auto;
      padding-bottom: 8px;
      margin-bottom: 28px;
      border-bottom: 1px solid var(--card-border);
    }

    .arena-nav-tab {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 10px 18px;
      font-size: 13px;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.25s ease;
      white-space: nowrap;
    }
    .arena-nav-tab:hover {
      color: #fff;
      border-color: rgba(255, 255, 255, 0.25);
      background: rgba(255, 255, 255, 0.05);
    }
    .arena-nav-tab.active {
      background: linear-gradient(135deg, rgba(252, 76, 2, 0.2), rgba(255, 106, 43, 0.15));
      border-color: var(--strava-orange);
      color: #fff;
      box-shadow: 0 0 16px var(--orange-glow);
    }

    /* Section Panels */
    .arena-panel {
      display: none;
      animation: fadeIn 0.3s ease;
    }
    .arena-panel.active {
      display: block;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Section Header */
    .section-header {
      margin-bottom: 22px;
    }
    .section-title {
      font-family: 'Outfit', sans-serif;
      font-size: 22px;
      font-weight: 800;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 6px;
    }
    .section-desc {
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.5;
    }

    /* =========================================================================
       TEAM BUILDER STYLES (Precalculated & Ultra-Lightweight)
       ========================================================================= */
    .tb-controls {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 18px 24px;
      margin-bottom: 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }

    .tb-group {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }

    .tb-squad-btn {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--card-border);
      color: var(--text-muted);
      padding: 7px 13px;
      border-radius: 10px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s;
    }
    .tb-squad-btn:hover {
      color: #fff;
      border-color: rgba(255, 255, 255, 0.3);
    }
    .tb-squad-btn.active {
      background: rgba(168, 85, 247, 0.2);
      border-color: var(--accent-purple);
      color: #fff;
      box-shadow: 0 0 12px rgba(168, 85, 247, 0.3);
    }

    .tb-select-dropdown {
      background: #0f172a;
      border: 1px solid var(--accent-purple);
      color: #fff;
      padding: 7px 12px;
      border-radius: 10px;
      font-size: 12.5px;
      font-weight: 700;
      outline: none;
      cursor: pointer;
    }

    /* Balance Meter Bar */
    .tb-balance-card {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 16px 20px;
      margin-bottom: 24px;
    }

    .tb-balance-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
      font-size: 12.5px;
      font-weight: 700;
      flex-wrap: wrap;
      gap: 8px;
    }

    .tb-balance-meter {
      height: 14px;
      border-radius: 8px;
      overflow: hidden;
      display: flex;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .tb-meter-segment {
      height: 100%;
      transition: width 0.3s ease;
      position: relative;
    }

    /* Squad Filter Toolbar */
    .tb-toolbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      flex-wrap: wrap;
      gap: 12px;
    }

    .tb-view-toggle {
      display: flex;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 3px;
      gap: 4px;
    }

    .tb-view-pill {
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 5px 12px;
      border-radius: 7px;
      font-size: 11.5px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s;
    }
    .tb-view-pill.active {
      background: #334155;
      color: #fff;
    }

    .tb-search-input {
      background: #0f172a;
      border: 1px solid var(--card-border);
      color: #fff;
      padding: 6px 12px;
      border-radius: 10px;
      font-size: 12px;
      outline: none;
      width: 200px;
      transition: border-color 0.2s;
    }
    .tb-search-input:focus {
      border-color: var(--strava-orange);
    }

    /* Squad Cards Grid */
    .tb-squad-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
      gap: 20px;
      margin-bottom: 30px;
    }

    .tb-squad-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 8px 24px rgba(0,0,0,0.3);
      transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .tb-squad-card:hover {
      border-color: rgba(255, 255, 255, 0.2);
    }

    .tb-squad-header {
      padding: 16px 18px;
      border-bottom: 1px solid var(--card-border);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .tb-squad-name {
      font-family: 'Outfit', sans-serif;
      font-size: 17px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .tb-squad-score {
      font-family: 'Outfit', sans-serif;
      font-size: 22px;
      font-weight: 900;
      letter-spacing: -0.5px;
    }

    .tb-squad-meta-bar {
      padding: 9px 18px;
      background: rgba(15, 23, 42, 0.4);
      display: flex;
      justify-content: space-between;
      font-size: 11.5px;
      color: var(--text-muted);
      border-bottom: 1px solid var(--card-border);
    }

    .tb-synergy-tray {
      padding: 10px 16px;
      background: rgba(255, 255, 255, 0.02);
      border-bottom: 1px solid var(--card-border);
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      min-height: 44px;
      align-items: center;
    }

    .tb-synergy-pill {
      font-size: 10.5px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 7px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      cursor: help;
      border: 1px solid transparent;
      transition: transform 0.15s;
    }
    .tb-synergy-pill:hover {
      transform: scale(1.05);
    }

    .tb-roster-list {
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      flex: 1;
      max-height: 440px;
      overflow-y: auto;
    }

    .tb-player-card {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 8px 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      transition: all 0.2s;
    }
    .tb-player-card:hover {
      background: rgba(30, 41, 59, 0.8);
      border-color: rgba(255, 255, 255, 0.2);
    }

    .tb-player-card.reserve {
      opacity: 0.75;
      background: rgba(15, 23, 42, 0.35);
      border-style: dashed;
    }

    .tb-player-info {
      display: flex;
      align-items: center;
      gap: 8px;
      min-width: 0;
    }

    .tb-player-avatar {
      width: 30px;
      height: 30px;
      border-radius: 9px;
      background: #1e293b;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      font-weight: 800;
      color: #cbd5e1;
      flex-shrink: 0;
    }

    .tb-player-name {
      font-size: 12.5px;
      font-weight: 700;
      color: #fff;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .tb-class-badge {
      font-size: 9.5px;
      font-weight: 800;
      padding: 1px 6px;
      border-radius: 5px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      display: inline-block;
      margin-top: 1px;
    }

    .tb-player-stats {
      text-align: right;
      flex-shrink: 0;
      white-space: nowrap;
    }

    .tb-player-pts-tag {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: rgba(251, 191, 36, 0.12);
      border: 1px solid rgba(251, 191, 36, 0.32);
      border-radius: 7px;
      padding: 2px 8px;
      font-family: 'Outfit', sans-serif;
      font-size: 13px;
      font-weight: 800;
      color: var(--gold);
      white-space: nowrap;
      box-shadow: 0 1px 4px rgba(0, 0, 0, 0.25);
    }

    .tb-player-pts-tag .pts-unit {
      font-family: 'Inter', sans-serif;
      font-size: 9.5px;
      font-weight: 700;
      color: rgba(251, 191, 36, 0.9);
      text-transform: uppercase;
      letter-spacing: 0.4px;
    }

    .tb-player-pts-tag.zero-pts {
      background: rgba(255, 255, 255, 0.04);
      border-color: rgba(255, 255, 255, 0.1);
      color: var(--text-dim);
      box-shadow: none;
    }

    .tb-player-pts-tag.zero-pts .pts-unit {
      color: var(--text-dim);
    }

    .tb-player-sub {
      font-size: 10px;
      color: var(--text-dim);
      white-space: nowrap;
      margin-top: 3px;
    }

    .tb-move-select {
      background: #0f172a;
      border: 1px solid var(--card-border);
      color: var(--text-muted);
      border-radius: 6px;
      font-size: 10.5px;
      padding: 2px 5px;
      outline: none;
      cursor: pointer;
    }
    .tb-move-select:hover {
      border-color: var(--strava-orange);
      color: #fff;
    }

    /* Class Directory Drawer */
    .tb-class-guide {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 22px;
      margin-bottom: 30px;
    }

    .tb-guide-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 14px;
      margin-top: 14px;
    }

    .tb-class-item {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 12px;
    }

    .tb-class-item-title {
      font-size: 13px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 6px;
      margin-bottom: 4px;
    }

    .tb-class-item-desc {
      font-size: 11.5px;
      color: var(--text-muted);
      line-height: 1.4;
    }

    /* =========================================================================
       OTHER TABS STYLES (Roulette, Momentum, Road Trip, Duel, Trophies)
       ========================================================================= */
    .trophy-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
      gap: 20px;
      margin-bottom: 40px;
    }

    .trophy-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 24px;
      position: relative;
      overflow: hidden;
      transition: all 0.3s ease;
    }
    .trophy-card:hover {
      transform: translateY(-4px);
      border-color: var(--card-hover-border);
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(252, 76, 2, 0.15);
    }

    .trophy-icon-box {
      width: 52px;
      height: 52px;
      border-radius: 16px;
      background: linear-gradient(135deg, rgba(252, 76, 2, 0.2), rgba(255, 106, 43, 0.1));
      border: 1px solid rgba(252, 76, 2, 0.3);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 26px;
      margin-bottom: 14px;
      box-shadow: 0 0 16px var(--orange-glow);
    }

    .trophy-title {
      font-family: 'Outfit', sans-serif;
      font-size: 18px;
      font-weight: 800;
      color: #fff;
      margin-bottom: 6px;
    }

    .trophy-desc {
      font-size: 12px;
      color: var(--text-dim);
      margin-bottom: 18px;
      line-height: 1.4;
    }

    .trophy-holder-box {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 12px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .trophy-holder-name {
      font-weight: 700;
      font-size: 13.5px;
      color: #fff;
    }

    .trophy-stat-pill {
      background: rgba(251, 191, 36, 0.12);
      border: 1px solid rgba(251, 191, 36, 0.3);
      color: var(--gold);
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 8px;
    }

    /* 1v1 Duel Arena */
    .duel-layout {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      margin-bottom: 30px;
    }

    .duel-selectors {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 24px;
      padding: 24px;
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      gap: 16px;
      margin-bottom: 24px;
    }

    .fighter-select-box {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .fighter-box-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }

    .fighter-score-pill {
      font-size: 12px;
      font-weight: 800;
      padding: 3px 10px;
      border-radius: 9999px;
      letter-spacing: 0.5px;
      white-space: nowrap;
    }
    .fighter-score-pill.red {
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid rgba(239, 68, 68, 0.35);
      color: #f87171;
    }
    .fighter-score-pill.blue {
      background: rgba(59, 130, 246, 0.15);
      border: 1px solid rgba(59, 130, 246, 0.35);
      color: #60a5fa;
    }

    .fighter-label {
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 1px;
      font-weight: 800;
    }
    .fighter-label.red { color: var(--fighter-red); }
    .fighter-label.blue { color: var(--fighter-blue); }

    .fighter-select {
      background: #0f172a;
      border: 1px solid var(--card-border);
      color: #fff;
      padding: 12px 16px;
      border-radius: 12px;
      font-size: 14px;
      font-weight: 600;
      outline: none;
      cursor: pointer;
      width: 100%;
      transition: border-color 0.2s;
    }
    .fighter-select:focus {
      border-color: var(--strava-orange);
    }

    .duel-vs-badge {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--fighter-red), var(--fighter-blue));
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Outfit', sans-serif;
      font-weight: 900;
      font-size: 15px;
      color: #fff;
      box-shadow: 0 0 20px rgba(0, 0, 0, 0.6);
      flex-shrink: 0;
    }

    .duel-chart-box {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 24px;
      padding: 28px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 380px;
    }

    .duel-stats-box {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 24px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .duel-stat-row {
      display: grid;
      grid-template-columns: 1fr 1.5fr 1fr;
      align-items: center;
      padding: 10px 14px;
      background: rgba(15, 23, 42, 0.5);
      border-radius: 10px;
      font-size: 13px;
    }

    .duel-val-left {
      font-weight: 800;
      color: var(--fighter-red);
      text-align: left;
    }
    .duel-stat-label {
      text-align: center;
      color: var(--text-muted);
      font-size: 11.5px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .duel-val-right {
      font-weight: 800;
      color: var(--fighter-blue);
      text-align: right;
    }

    .duel-verdict {
      background: linear-gradient(135deg, rgba(168, 85, 247, 0.15), rgba(252, 76, 2, 0.15));
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 16px;
      padding: 16px 20px;
      margin-top: 14px;
      text-align: center;
      font-size: 13.5px;
      font-weight: 600;
      color: #fff;
    }

    /* Virtual Road Trip */
    .journey-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 24px;
      padding: 32px;
      margin-bottom: 40px;
    }

    .journey-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      margin-bottom: 24px;
    }

    .journey-km-display {
      font-family: 'Outfit', sans-serif;
      font-size: 38px;
      font-weight: 900;
      background: linear-gradient(135deg, var(--strava-orange), var(--gold));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .progress-track {
      width: 100%;
      height: 18px;
      background: rgba(15, 23, 42, 0.8);
      border-radius: 10px;
      overflow: hidden;
      border: 1px solid var(--card-border);
      margin-bottom: 28px;
      position: relative;
    }

    .progress-fill {
      height: 100%;
      background: linear-gradient(90deg, #fc4c02, #ff6a2b, #fbbf24);
      border-radius: 10px;
      transition: width 1s ease-in-out;
      box-shadow: 0 0 20px rgba(252, 76, 2, 0.6);
    }

    .milestone-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(135px, 1fr));
      gap: 14px;
    }

    .milestone-card {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 14px;
      text-align: center;
      position: relative;
    }
    .milestone-card.unlocked {
      border-color: rgba(34, 197, 94, 0.4);
      background: rgba(34, 197, 94, 0.08);
    }
    .milestone-card.active-target {
      border-color: rgba(252, 76, 2, 0.45);
      background: rgba(252, 76, 2, 0.09);
      box-shadow: 0 0 20px var(--orange-glow);
    }

    .milestone-badge {
      font-size: 10px;
      font-weight: 800;
      padding: 2px 8px;
      border-radius: 8px;
      display: inline-block;
      margin-bottom: 8px;
      text-transform: uppercase;
    }
    .unlocked .milestone-badge { background: rgba(34, 197, 94, 0.2); color: var(--accent-green); }
    .active-target .milestone-badge { background: rgba(252, 76, 2, 0.25); color: var(--strava-orange); }
    .locked .milestone-badge { background: rgba(255, 255, 255, 0.08); color: var(--text-dim); }

    /* Momentum Section */
    .momentum-grid {
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 24px;
      margin-bottom: 40px;
    }

    .momentum-table-box {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 24px;
    }

    .streak-highlight-card {
      background: linear-gradient(135deg, rgba(252, 76, 2, 0.15), rgba(234, 179, 8, 0.1));
      border: 1px solid rgba(252, 76, 2, 0.3);
      border-radius: 20px;
      padding: 24px;
    }

    /* Workout Roulette */
    .roulette-box {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 24px;
      padding: 32px;
      text-align: center;
      max-width: 680px;
      margin: 0 auto 40px;
    }

    .roulette-card-display {
      background: rgba(15, 23, 42, 0.85);
      border: 2px dashed rgba(252, 76, 2, 0.4);
      border-radius: 20px;
      padding: 32px 24px;
      margin: 24px 0;
      transition: all 0.3s ease;
    }

    .roulette-icon {
      font-size: 56px;
      margin-bottom: 12px;
      display: inline-block;
    }

    .roulette-title {
      font-family: 'Outfit', sans-serif;
      font-size: 22px;
      font-weight: 800;
      color: #fff;
      margin-bottom: 8px;
    }

    .roulette-desc {
      font-size: 14px;
      color: var(--text-muted);
      max-width: 440px;
      margin: 0 auto 16px;
      line-height: 1.5;
    }

    .roulette-pts-tag {
      background: rgba(251, 191, 36, 0.15);
      border: 1px solid rgba(251, 191, 36, 0.4);
      color: var(--gold);
      font-weight: 800;
      font-size: 13px;
      padding: 6px 14px;
      border-radius: 12px;
      display: inline-block;
    }

    /* Toast Notification */
    #toastNotification {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid var(--accent-green);
      color: #fff;
      padding: 12px 20px;
      border-radius: 12px;
      font-size: 13px;
      font-weight: 600;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
      z-index: 1000;
      transform: translateY(100px);
      opacity: 0;
      transition: all 0.3s ease;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    #toastNotification.show {
      transform: translateY(0);
      opacity: 1;
    }

    /* =========================================================================
       7. META ANALYSIS & STRATEGY LAB STYLES
       ========================================================================= */
    .meta-hero-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
      margin-bottom: 32px;
    }
    .meta-hero-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 18px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      transition: all 0.3s ease;
      position: relative;
      overflow: hidden;
    }
    .meta-hero-card:hover {
      border-color: rgba(255, 255, 255, 0.22);
      transform: translateY(-2px);
      box-shadow: 0 10px 24px rgba(0,0,0,0.35);
    }
    .meta-hero-card::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0; height: 3px;
      background: var(--card-accent, var(--strava-orange));
    }
    .meta-hero-title {
      font-size: 13.5px;
      font-weight: 800;
      color: var(--text-primary);
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .meta-hero-rate {
      font-family: 'Outfit', sans-serif;
      font-size: 26px;
      font-weight: 900;
      color: #fff;
    }
    .meta-hero-subtitle {
      font-size: 11.5px;
      color: var(--text-muted);
      line-height: 1.45;
    }
    .meta-hero-tax {
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 8px;
      display: inline-block;
      margin-top: 4px;
      width: fit-content;
    }

    /* Subsections within Meta Lab */
    .meta-section {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 24px;
      padding: 28px;
      margin-bottom: 36px;
    }
    .meta-section-header {
      margin-bottom: 22px;
    }
    .meta-section-title {
      font-family: 'Outfit', sans-serif;
      font-size: 20px;
      font-weight: 800;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .meta-section-desc {
      font-size: 13.5px;
      color: var(--text-muted);
      margin-top: 6px;
      line-height: 1.5;
    }

    /* 3 Archetype Cards */
    .archetype-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
      gap: 20px;
      margin-top: 16px;
    }
    .archetype-card {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      transition: all 0.3s ease;
    }
    .archetype-card:hover {
      border-color: rgba(255, 255, 255, 0.25);
      transform: translateY(-3px);
      box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    }
    .archetype-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 800;
      padding: 5px 12px;
      border-radius: 20px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 14px;
      width: fit-content;
    }
    .archetype-title {
      font-family: 'Outfit', sans-serif;
      font-size: 19px;
      font-weight: 800;
      color: #fff;
      margin-bottom: 8px;
    }
    .archetype-desc {
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.5;
      margin-bottom: 18px;
    }
    .archetype-stats-box {
      background: rgba(0, 0, 0, 0.35);
      border-radius: 14px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-bottom: 16px;
    }
    .archetype-stat-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12.5px;
    }
    .archetype-stat-label {
      color: var(--text-muted);
    }
    .archetype-stat-val {
      font-weight: 700;
      color: #fff;
    }
    .archetype-health-box {
      border-top: 1px dashed rgba(255, 255, 255, 0.12);
      padding-top: 14px;
      font-size: 12px;
      line-height: 1.5;
    }

    /* 10K vs 2x5K Simulator */
    .duel-meta-box {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      margin-top: 20px;
    }
    .duel-meta-card {
      background: rgba(15, 23, 42, 0.75);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 24px;
      position: relative;
      transition: all 0.3s ease;
    }
    .duel-meta-card.winner {
      border-color: rgba(34, 197, 94, 0.5);
      background: linear-gradient(135deg, rgba(34, 197, 94, 0.08), rgba(15, 23, 42, 0.85));
    }
    .duel-meta-score {
      font-family: 'Outfit', sans-serif;
      font-size: 36px;
      font-weight: 900;
      color: #fff;
      margin: 10px 0;
    }
    .duel-control-panel {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--card-border);
      border-radius: 18px;
      padding: 20px 24px;
      margin-bottom: 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 20px;
    }
    .meta-slider-group {
      display: flex;
      flex-direction: column;
      gap: 8px;
      min-width: 260px;
      flex: 1;
    }
    .meta-slider-header {
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      font-weight: 700;
    }
    .meta-slider {
      -webkit-appearance: none;
      width: 100%;
      height: 8px;
      border-radius: 4px;
      background: #1e293b;
      outline: none;
    }
    .meta-slider::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      background: var(--strava-orange);
      cursor: pointer;
      box-shadow: 0 0 10px var(--orange-glow);
    }
    .meta-toggle-label {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 13px;
      font-weight: 600;
      color: #cbd5e1;
      cursor: pointer;
    }

    /* Sports Efficiency Table */
    .meta-table-wrap {
      overflow-x: auto;
      margin-top: 16px;
      border-radius: 16px;
      border: 1px solid var(--card-border);
    }
    .meta-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      text-align: left;
    }
    .meta-table th {
      background: rgba(15, 23, 42, 0.95);
      color: var(--text-muted);
      font-weight: 700;
      padding: 14px 18px;
      border-bottom: 1px solid var(--card-border);
      white-space: nowrap;
    }
    .meta-table td {
      padding: 14px 18px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      color: #e2e8f0;
    }
    .meta-table tr:hover td {
      background: rgba(255, 255, 255, 0.03);
    }

    /* Routine Simulator */
    .routine-grid {
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      gap: 24px;
      margin-top: 20px;
    }
    .routine-presets-bar {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 20px;
    }
    .routine-preset-pill {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 8px 14px;
      font-size: 12px;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .routine-preset-pill:hover {
      color: #fff;
      border-color: rgba(255, 255, 255, 0.3);
    }
    .routine-preset-pill.active {
      background: rgba(252, 76, 2, 0.2);
      border-color: var(--strava-orange);
      color: #fff;
      box-shadow: 0 0 12px var(--orange-glow);
    }
    .routine-sliders-box {
      display: flex;
      flex-direction: column;
      gap: 16px;
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--card-border);
      border-radius: 18px;
      padding: 20px;
    }
    .routine-slider-item {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .routine-slider-header {
      display: flex;
      justify-content: space-between;
      font-size: 12.5px;
      font-weight: 700;
    }
    .routine-gauge-card {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 18px;
    }
    .routine-meter-bar {
      height: 12px;
      background: #1e293b;
      border-radius: 6px;
      overflow: hidden;
      margin-top: 6px;
      display: flex;
    }
    .routine-meter-fill {
      height: 100%;
      transition: width 0.4s ease, background 0.4s ease;
    }

    /* Leader Metas Table */
    .lead-meta-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 8px;
      white-space: nowrap;
    }

    /* Responsive */
    @media (max-width: 900px) {
      .duel-layout { grid-template-columns: 1fr; }
      .momentum-grid { grid-template-columns: 1fr; }
      .duel-selectors { grid-template-columns: 1fr; }
      .duel-vs-badge { margin: 0 auto; }
      .date-filter-bar { flex-direction: column; align-items: stretch; }
      .filter-left, .filter-right { justify-content: space-between; }
      .duel-meta-box { grid-template-columns: 1fr; }
      .routine-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>

  <!-- Sticky Navbar -->
  <nav class="navbar">
    <a href="#" class="brand">
      <div class="brand-logo">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="#ffffff"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
      </div>
      <div>
        <div class="brand-title">The Connectivity Arena</div>
        <div class="brand-subtitle">Team Builder & Gamification Clubhouse</div>
      </div>
    </a>

    <div class="nav-actions">
      <a href="index.html" class="btn btn-orange" title="Return to Official Leaderboard">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
        Official Leaderboard
      </a>
    </div>
  </nav>

  <div class="container">

    <!-- Hero Banner -->
    <div class="arena-hero">
      <div>
        <div class="arena-hero-title">⚡ The Connectivity Arena</div>
        <div class="arena-hero-sub">
          The gamified clubhouse for Connectivity Sports Day 2026. Pre-balanced squads for up to 20 squads, RPG party synergies, workout roulette, momentum velocity, 1v1 duels, and algorithmic trophies.
        </div>
      </div>
      <div>
        <a href="index.html" class="btn btn-outline" style="font-size:12px; padding:7px 14px;">
          View Live Standings →
        </a>
      </div>
    </div>

    <!-- Reactive Date Filter Bar -->
    <div class="date-filter-bar">
      <div class="filter-left">
        <span class="filter-label">🗓️ Date Filter:</span>
        <div class="preset-group">
          <button id="presetTournament" class="preset-pill active" onclick="setDatePreset('tournament')">
            ⚡ Contest (Sep 14+)
          </button>
          <button id="presetAll" class="preset-pill" onclick="setDatePreset('all')">
            🌐 All-Time
          </button>
          <button id="preset7Days" class="preset-pill" onclick="setDatePreset('7days')">
            📅 Last 7 Days
          </button>
        </div>
      </div>
      <div class="filter-right">
        <div class="date-input-wrap">
          <span>From:</span>
          <input type="date" id="dateStart" class="date-input" value="2026-09-14" onchange="onCustomDateChange()">
        </div>
        <div class="date-input-wrap">
          <span>To:</span>
          <input type="date" id="dateEnd" class="date-input" value="" onchange="onCustomDateChange()">
        </div>
        <div id="activityCountBadge" class="activity-count-badge">Loading...</div>
      </div>
    </div>

    <!-- Arena Navigation Tabs -->
    <div class="arena-nav-bar">
      <button id="tabBtnDuel" class="arena-nav-tab active" onclick="switchArenaTab('tabDuel')">
        <span>🥊</span> 1v1 Duel Arena
      </button>
      <button id="tabBtnTeamBuilder" class="arena-nav-tab" onclick="switchArenaTab('tabTeamBuilder')">
        <span>👥</span> Team Builder
      </button>
      <button id="tabBtnTrophies" class="arena-nav-tab" onclick="switchArenaTab('tabTrophies')">
        <span>🏆</span> The Trophy Room
      </button>
      <button id="tabBtnMomentum" class="arena-nav-tab" onclick="switchArenaTab('tabMomentum')">
        <span>🔥</span> Momentum Tracker
      </button>
      <button id="tabBtnJourney" class="arena-nav-tab" onclick="switchArenaTab('tabJourney')">
        <span>🗺️</span> Virtual Road Trip
      </button>
      <button id="tabBtnRoulette" class="arena-nav-tab" onclick="switchArenaTab('tabRoulette')">
        <span>🎲</span> Workout Roulette
      </button>
      <button id="tabBtnMeta" class="arena-nav-tab" onclick="switchArenaTab('tabMeta')">
        <span>🔬</span> Meta Lab &amp; Strategy Analysis
      </button>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 1: 1v1 DUEL ARENA (Default Active) -->
    <!-- =================================================================== -->
    <div id="tabDuel" class="arena-panel active">
      <div class="section-header">
        <div class="section-title">
          <span>🥊</span> 1v1 Head-to-Head Athlete Duel Arena
        </div>
        <div class="section-desc">
          Select any two athletes to simulate an athletic tale-of-the-tape comparison across 6 core fitness dimensions.
        </div>
      </div>

      <div class="duel-selectors">
        <div class="fighter-select-box">
          <div class="fighter-box-header">
            <span class="fighter-label red">🔴 Red Corner</span>
            <span id="fighterRedScore" class="fighter-score-pill red">0 pts</span>
          </div>
          <select id="fighterRed" class="fighter-select" onchange="updateDuel()"></select>
        </div>

        <div class="duel-vs-badge">VS</div>

        <div class="fighter-select-box">
          <div class="fighter-box-header">
            <span class="fighter-label blue">🔵 Blue Corner</span>
            <span id="fighterBlueScore" class="fighter-score-pill blue">0 pts</span>
          </div>
          <select id="fighterBlue" class="fighter-select" onchange="updateDuel()"></select>
        </div>
      </div>

      <div class="duel-layout">
        <div class="duel-chart-box">
          <div style="font-size:12px; font-weight:700; color:var(--text-muted); margin-bottom:12px; text-transform:uppercase;">
            Athletic Profile Radar
          </div>
          <div style="width: 100%; max-width: 380px; height: 320px; position: relative;">
            <canvas id="duelRadarChart"></canvas>
          </div>
        </div>

        <div class="duel-stats-box">
          <div style="font-size:12px; font-weight:700; color:var(--text-muted); margin-bottom:6px; text-transform:uppercase;">
            Head-to-Head Stats Breakdown
          </div>

          <div id="duelStatsRows">
            <!-- Injected via JavaScript -->
          </div>

          <div class="duel-verdict" id="duelVerdict">
            Select two athletes above to generate duel comparison.
          </div>
        </div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 2: TEAM BUILDER (Precalculated & Instantaneous) -->
    <!-- =================================================================== -->
    <div id="tabTeamBuilder" class="arena-panel">
      <div class="section-header">
        <div class="section-title">
          <span>👥</span> Pre-Balanced Team Builder & RPG Synergies
        </div>
        <div class="section-desc">
          Instantly load mathematically pre-balanced squads (2 to 20 squads) with zero client calculation lag. Active scorers and registered candidates ({num_members} club members) are distributed evenly, with real-time party synergy buffs!
        </div>
      </div>

      <!-- Team Builder Controls -->
      <div class="tb-controls">
        <div class="tb-group">
          <span style="font-size:12.5px; font-weight:700; color:var(--text-muted);">Popular Squads:</span>
          <button id="squadBtn2" class="tb-squad-btn" onclick="setSquadCount(2)">2</button>
          <button id="squadBtn3" class="tb-squad-btn" onclick="setSquadCount(3)">3</button>
          <button id="squadBtn4" class="tb-squad-btn active" onclick="setSquadCount(4)">4</button>
          <button id="squadBtn6" class="tb-squad-btn" onclick="setSquadCount(6)">6</button>
          <button id="squadBtn8" class="tb-squad-btn" onclick="setSquadCount(8)">8</button>
          <button id="squadBtn10" class="tb-squad-btn" onclick="setSquadCount(10)">10</button>
          <button id="squadBtn15" class="tb-squad-btn" onclick="setSquadCount(15)">15</button>
          <button id="squadBtn20" class="tb-squad-btn" onclick="setSquadCount(20)" title="Recommended for 100+ candidates: ~5-6 per squad!">20 ⚡</button>

          <select id="squadSelectDropdown" class="tb-select-dropdown" onchange="setSquadCount(parseInt(this.value))">
            <!-- Populated 2..20 via JS -->
          </select>
        </div>

        <div class="tb-group">
          <button class="btn btn-orange" onclick="resetToPrecalculated()" title="Restore the optimal pre-calculated AI balance in 0ms">
            <span>⚡</span> Reset Pre-Balance
          </button>
          <button class="btn btn-outline" onclick="copyTeamRoster()" title="Copy clean roster text for Slack / WhatsApp">
            <span>📋</span> Copy Roster
          </button>
        </div>
      </div>

      <!-- Live Balance Meter -->
      <div class="tb-balance-card">
        <div class="tb-balance-header">
          <span id="tbBalanceTitle">⚖️ Squad Balance Meter</span>
          <span id="tbBalanceStatus" style="color:var(--accent-green);">Instant 0ms Pre-Calculated Balance</span>
        </div>
        <div id="tbBalanceMeter" class="tb-balance-meter">
          <!-- Injected via JS -->
        </div>
      </div>

      <!-- Squad View Options & Member Search -->
      <div class="tb-toolbar">
        <div class="tb-view-toggle">
          <button id="viewActiveOnly" class="tb-view-pill active" onclick="setViewMode('active')">
            Active Scorers (<span id="activeScorerCount">0</span>)
          </button>
          <button id="viewFullRoster" class="tb-view-pill" onclick="setViewMode('full')">
            Full Squad Roster (All {num_members} Candidates)
          </button>
        </div>

        <input type="text" id="memberSearch" class="tb-search-input" placeholder="🔍 Search member squad..." oninput="onSearchMember(this.value)">
      </div>

      <!-- Squad Columns Grid -->
      <div id="tbSquadGrid" class="tb-squad-grid">
        <!-- Injected via JS -->
      </div>

      <!-- RPG Hero Class & Synergies Explainer -->
      <div class="tb-class-guide">
        <div style="font-family:'Outfit',sans-serif; font-size:17px; font-weight:800; color:#fff; margin-bottom:4px;">
          🧙‍♂️ RPG Hero Classes & Team Synergies
        </div>
        <div style="font-size:12px; color:var(--text-muted); line-height:1.5;">
          Every athlete is classified based on pace, volume, and sport diversity. Combining different classes unlocks automatic team synergy buffs!
        </div>

        <div class="tb-guide-grid">
          <div class="tb-class-item">
            <div class="tb-class-item-title" style="color:#22c55e;">🏹 The Ranger</div>
            <div class="tb-class-item-desc">High-volume endurance specialist (&ge; 25 km distance or long continuous outings).</div>
          </div>
          <div class="tb-class-item">
            <div class="tb-class-item-title" style="color:#a855f7;">⚡ The Assassin</div>
            <div class="tb-class-item-desc">High-velocity speedster with blistering pace bursts (&lt; 5:30 /km pace).</div>
          </div>
          <div class="tb-class-item">
            <div class="tb-class-item-title" style="color:#fbbf24;">🛡️ The Sentinel</div>
            <div class="tb-class-item-desc">Unshakeable consistency anchor logging frequent daily streaks (&ge; 4 active sessions).</div>
          </div>
          <div class="tb-class-item">
            <div class="tb-class-item-title" style="color:#38bdf8;">🧙‍♂️ The Polymath</div>
            <div class="tb-class-item-desc">Hybrid multi-sport warrior active across 2+ distinct disciplines (Run, Ride, Walk, Workout).</div>
          </div>
          <div class="tb-class-item">
            <div class="tb-class-item-title" style="color:#ef4444;">🏋️ The Berserker</div>
            <div class="tb-class-item-desc">High-intensity crusher excelling in Weight Training, Workouts, Swimming, or 60+ min grinds.</div>
          </div>
        </div>

        <div style="margin-top:16px; padding-top:12px; border-top:1px solid var(--card-border); font-size:11.5px; color:var(--text-dim); display:flex; flex-wrap:wrap; gap:16px;">
          <span>✨ <strong>Tri-Sport Mastery (+8%):</strong> Squad covers Run, Walk, & Ride/Workout.</span>
          <span>🌙 <strong>24-Hour Watch (+5%):</strong> Squad features Dawn Patrol (&lt;7 AM) & Night Owl (&gt;8 PM).</span>
          <span>🛡️ <strong>Class Quintet (+10%):</strong> Squad includes 3+ distinct Hero Classes.</span>
          <span>⚡ <strong>Speed & Stamina (+6%):</strong> Squad pairs a Ranger with an Assassin.</span>
        </div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 3: THE TROPHY ROOM -->
    <!-- =================================================================== -->
    <div id="tabTrophies" class="arena-panel">
      <div class="section-header">
        <div class="section-title">
          <span>🏆</span> The Clubhouse Trophy Room
        </div>
        <div class="section-desc">
          Automated superlative badges awarded algorithmically across all Strava activities logged within the active date window.
        </div>
      </div>

      <div id="trophiesContainer" class="trophy-grid">
        <!-- Injected via JavaScript -->
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 4: MOMENTUM TRACKER -->
    <!-- =================================================================== -->
    <div id="tabMomentum" class="arena-panel">
      <div class="section-header">
        <div class="section-title">
          <span>🔥</span> Rolling Momentum & Activity Velocity
        </div>
        <div class="section-desc">
          Tracking which athletes are surging right now based on recent activity frequency within the active filter window.
        </div>
      </div>

      <div class="momentum-grid">
        <div class="momentum-table-box">
          <div style="font-family:'Outfit',sans-serif; font-size:16px; font-weight:800; color:#fff; margin-bottom:14px;">
            ⚡ Active Session Leaders
          </div>
          <div id="momentumList" style="display:flex; flex-direction:column; gap:8px;">
            <!-- Injected via JavaScript -->
          </div>
        </div>

        <div class="streak-highlight-card">
          <div style="font-size:12px; font-weight:800; text-transform:uppercase; color:var(--strava-orange); margin-bottom:6px;">
            Club Trend Insight
          </div>
          <div style="font-family:'Outfit',sans-serif; font-size:22px; font-weight:800; color:#fff; margin-bottom:10px;" id="streakTitle">
            Consistency Leads the Race
          </div>
          <div style="font-size:13px; color:var(--text-muted); line-height:1.6;" id="streakDesc">
            Athletes who log regular 3-5 km sessions 4+ times a week are currently outpacing single-effort marathoners in overall Dynamic MET points!
          </div>
        </div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 5: VIRTUAL ROAD TRIP -->
    <!-- =================================================================== -->
    <div id="tabJourney" class="arena-panel">
      <div class="section-header">
        <div class="section-title">
          <span>🗺️</span> The Great Indian Club Road Trip
        </div>
        <div class="section-desc">
          Every kilometer logged across all club members pulls us closer to our collective nationwide travel goal!
        </div>
      </div>

      <div class="journey-card">
        <div class="journey-header">
          <div>
            <div style="font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: var(--accent-blue); font-weight: 800;">
              Collective Club Journey
            </div>
            <div class="journey-km-display" id="journeyKmDisplay">0.0 km</div>
          </div>
          <div style="text-align: right;">
            <div style="font-size: 12px; color: var(--text-muted);">Current Leg Target:</div>
            <div style="font-size: 16px; font-weight: 800; color: #fff;" id="nextCityTarget">Loading...</div>
          </div>
        </div>

        <div class="progress-track">
          <div id="progressFill" class="progress-fill" style="width: 0%;"></div>
        </div>

        <div id="milestonesContainer" class="milestone-grid">
          <!-- Injected via JavaScript -->
        </div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 6: WORKOUT ROULETTE & DAILY ACTIVITY BOUNTY -->
    <!-- =================================================================== -->
    <div id="tabRoulette" class="arena-panel">
      <div class="section-header">
        <div class="section-title">
          <span>🎲</span> The Workout Roulette &amp; Daily Activity Bounty
        </div>
        <div class="section-desc">
          Every day features a boosted fitness quest with a +15% to +20% points multiplier bonus. Check today's active quest, see who claimed it, or spin the wheel for spontaneous fitness dares!
        </div>
      </div>

      <!-- Today's Featured Activity Bounty Box -->
      <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid var(--card-border); border-top: 3px solid var(--gold); border-radius: 20px; padding: 26px; margin-bottom: 28px; max-width: 820px; margin-left: auto; margin-right: auto; box-shadow: 0 10px 30px rgba(0,0,0,0.35);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 14px;">
          <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 34px;" id="bountyIcon">🏃‍♂️</span>
            <div>
              <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: var(--gold); font-weight: 800;">
                Today's Featured Activity Bounty • <span id="bountyDateDisplay">Loading Date...</span>
              </div>
              <div style="font-family: 'Outfit', sans-serif; font-size: 22px; font-weight: 800; color: #fff;" id="bountyTitle">
                Speedway Monday Tempo Run
              </div>
            </div>
          </div>
          <div style="background: rgba(251, 191, 36, 0.18); border: 1px solid rgba(251, 191, 36, 0.45); color: var(--gold); font-weight: 800; font-size: 13px; padding: 6px 14px; border-radius: 12px;" id="bountyMultiplierTag">
            ⚡ +15% Bonus Multiplier Active
          </div>
        </div>

        <div style="font-size: 13.5px; color: var(--text-muted); line-height: 1.5; margin-bottom: 18px;" id="bountyDesc">
          Log a continuous run of at least 4.0 km today to unlock a +15% dynamic points multiplier bonus.
        </div>

        <!-- Today's Bounty Claimers -->
        <div style="background: rgba(0,0,0,0.35); border: 1px solid rgba(255,255,255,0.06); border-radius: 14px; padding: 16px 18px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <div style="font-size: 12px; font-weight: 800; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px;">
              🎯 Today's Bounty Claimers (Athletes who completed today's quest):
            </div>
            <span id="bountyClaimCount" style="font-size:11px; font-weight:800; color:var(--accent-green); background:rgba(34,197,94,0.15); padding:2px 8px; border-radius:8px;">0 Claimed</span>
          </div>
          <div id="bountyClaimersList" style="display: flex; flex-wrap: wrap; gap: 8px; font-size: 12.5px;">
            <span style="color: var(--text-dim);">Scanning activities...</span>
          </div>
        </div>
      </div>

      <!-- Spontaneous Dare Spinner Box -->
      <div class="roulette-box">
        <div style="font-size: 13px; text-transform: uppercase; letter-spacing: 1px; color: var(--strava-orange); font-weight: 800;">
          Your Spontaneous Fitness Dare
        </div>

        <div class="roulette-card-display" id="rouletteDisplay">
          <div class="roulette-icon" id="dareIcon">🌅</div>
          <div class="roulette-title" id="dareTitle">The Sunrise 5k Cruise</div>
          <div class="roulette-desc" id="dareDesc">
            Log a brisk 5.0 km run or walk before 7:30 AM. Earn a dynamic pace bonus and secure the Dawn Patrol trophy lead.
          </div>
          <div class="roulette-pts-tag" id="darePts">Est. Reward: ~120 - 150 pts</div>
        </div>

        <button class="btn btn-orange" style="font-size: 15px; padding: 12px 28px;" onclick="spinRoulette()">
          🎲 Spin Dare
        </button>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 7: META ANALYSIS & STRATEGY LAB -->
    <!-- =================================================================== -->
    <div id="tabMeta" class="arena-panel">
      <div class="section-header">
        <div class="section-title">
          <span>🔬</span> The Strategic Meta Lab &amp; Physiological Health Analysis
        </div>
        <div class="section-desc">
          Empirical sports-science deep dive into Strava 2026 scoring mechanics, real club leader tactics, returns per unit consumption, and the hidden biological health cost of leaderboard dominance.
        </div>
      </div>

      <!-- Quick-Stat Benchmark Grid -->
      <div class="meta-hero-grid">
        <div class="meta-hero-card" style="--card-accent: #ef4444;">
          <div class="meta-hero-title">
            <span>🏃‍♂️</span> High-Velocity Land Engine (Running)
          </div>
          <div class="meta-hero-rate" id="metaHeroRunRate">11.47 <span style="font-size:14px; font-weight:600; color:var(--text-muted);">pts/min</span></div>
          <div class="meta-hero-subtitle">
            Avg Act: <strong>7.5 km in 52.3 min</strong> (~599 pts). Maximum time efficiency on land, scaling dynamically up to 113 pts/km at speed.
          </div>
          <div class="meta-hero-tax" style="background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3);">
            ⚠️ High Orthopedic Strain: 2.5-3.0x bodyweight impact shock
          </div>
        </div>

        <div class="meta-hero-card" style="--card-accent: #38bdf8;">
          <div class="meta-hero-title">
            <span>🏊‍♂️</span> The Hydro Supreme (Swimming)
          </div>
          <div class="meta-hero-rate" id="metaHeroSwimRate">14.43 <span style="font-size:14px; font-weight:600; color:var(--text-muted);">pts/min</span></div>
          <div class="meta-hero-subtitle">
            Avg Act: <strong>1.2 km in 31.4 min</strong> (~454 pts). Burns ~4x calories/km vs running. Highest points per minute in the club!
          </div>
          <div class="meta-hero-tax" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3);">
            💎 Zero Impact Shock: Restorative spinal decompression
          </div>
        </div>

        <div class="meta-hero-card" style="--card-accent: #f59e0b;">
          <div class="meta-hero-title">
            <span>🚴‍♂️</span> Endurance Scaling Curve (Cycling)
          </div>
          <div class="meta-hero-rate" id="metaHeroRideRate">19.76 <span style="font-size:14px; font-weight:600; color:var(--text-muted);">pts/km (peak)</span></div>
          <div class="meta-hero-subtitle">
            Option B curve: Short 5km rides earn ~14.1 pts/km, while epic 80km+ rides scale to 19.8 pts/km (+40% return rate).
          </div>
          <div class="meta-hero-tax" style="background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3);">
            🟢 Low Joint Impact: High duration time footprint required
          </div>
        </div>

        <div class="meta-hero-card" style="--card-accent: #10b981;">
          <div class="meta-hero-title">
            <span>🛡️</span> The Longevity Anchors (Gym &amp; Walk)
          </div>
          <div class="meta-hero-rate">4.0 - 5.2 <span style="font-size:14px; font-weight:600; color:var(--text-muted);">pts/min</span></div>
          <div class="meta-hero-subtitle">
            Gym hits 1.30x multiplier on Day 4+. Walking is flat 35 pts/km. Zero orthopedic breakdown; stimulates bone and muscle retention.
          </div>
          <div class="meta-hero-tax" style="background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3);">
            🌟 Restorative Longevity: Anabolic stimulation &amp; active recovery
          </div>
        </div>
      </div>

      <!-- SECTION 1: THE THREE STRATEGIC METAS -->
      <div class="meta-section">
        <div class="meta-section-header">
          <div class="meta-section-title">
            <span>⚔️</span> The 3 Archetypal Metas: Singular Heavy vs. 6-1 Iron vs. 3-Day Interleaved
          </div>
          <div class="meta-section-desc">
            How top athletes structure their week to reach 2,000 - 3,500 points, and the stark physiological contrast between burst shock and structured consistency.
          </div>
        </div>

        <div class="archetype-grid">
          <!-- Archetype A -->
          <div class="archetype-card" style="border-top: 3px solid #ef4444;">
            <div>
              <div class="archetype-badge" style="background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3);">
                ⚡ Archetype 1 • Singular Apex
              </div>
              <div class="archetype-title">The "Heavy Singularity" Meta</div>
              <div class="archetype-desc">
                Focuses on 1 to 3 massive, high-yield singular efforts per week (e.g. 15k-21k runs, 70-80k bike rides, or 120 min heavy sessions). Seen in club leaders <strong>Satyaprakash</strong> (81km epic ride), <strong>Krishna</strong> (21.5km peak run), and <strong>Muni Asheesh</strong> (15km run).
              </div>
              <div class="archetype-stats-box">
                <div class="archetype-stat-row">
                  <span class="archetype-stat-label">Weekly Yield:</span>
                  <span class="archetype-stat-val" style="color: var(--strava-orange);">2,200 - 3,500 pts</span>
                </div>
                <div class="archetype-stat-row">
                  <span class="archetype-stat-label">Burst per Session:</span>
                  <span class="archetype-stat-val" style="color: #fff;">750 - 1,877 pts/act</span>
                </div>
                <div class="archetype-stat-row">
                  <span class="archetype-stat-label">Time Commitment:</span>
                  <span class="archetype-stat-val">3.5 - 5.0 hours/wk</span>
                </div>
                <div class="archetype-stat-row">
                  <span class="archetype-stat-label">Acute Tissue Fatigue:</span>
                  <span class="archetype-stat-val" style="color: #ef4444;">Very High (48-72h recovery)</span>
                </div>
              </div>
            </div>
            <div class="archetype-health-box">
              <strong style="color:#f87171;">Hidden Health Cost:</strong> High peak ground shock (15,000+ continuous eccentric impacts), severe glycogen depletion, and delayed cartilage recovery. Repeated daily without rest causes rapid overuse injuries.
              <div style="margin-top: 8px; display: flex; justify-content: space-between; align-items: center;">
                <span style="color: var(--text-dim);">Sustainability:</span>
                <span style="font-weight: 800; color: #f59e0b;">6.5 / 10 (High Risk if unconditioned)</span>
              </div>
            </div>
          </div>

          <!-- Archetype B -->
          <div class="archetype-card" style="border-top: 3px solid #f59e0b;">
            <div>
              <div class="archetype-badge" style="background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3);">
                🔥 Archetype 2 • Iron Habit
              </div>
              <div class="archetype-title">The "Continuous 6-1" Meta</div>
              <div class="archetype-desc">
                6 consecutive days of structured, moderate exercise (45-55 mins) with exactly 1 mandatory, non-negotiable rest day. Maxes out the <strong>1.30x Slow-MET Consistency Multiplier</strong> on Days 4, 5, and 6. Exemplified by high-frequency athletes like <strong>Divyansh</strong> and <strong>Harsh</strong>.
              </div>
              <div class="archetype-stats-box">
                <div class="archetype-stat-row">
                  <span class="archetype-stat-label">Weekly Yield:</span>
                  <span class="archetype-stat-val" style="color: var(--strava-orange);">2,400 - 3,200 pts</span>
                </div>
                <div class="archetype-stat-row">
                  <span class="archetype-stat-label">Daily Average:</span>
                  <span class="archetype-stat-val" style="color: #fff;">400 - 520 pts/day</span>
                </div>
                <div class="archetype-stat-row">
                  <span class="archetype-stat-label">Time Commitment:</span>
                  <span class="archetype-stat-val">4.5 - 6.5 hours/wk</span>
                </div>
                <div class="archetype-stat-row">
                  <span class="archetype-stat-label">Rest Day Role:</span>
                  <span class="archetype-stat-val" style="color: #22c55e;">CNS &amp; Glycogen Supercompensation</span>
                </div>
              </div>
            </div>
            <div class="archetype-health-box">
              <strong style="color:#fbbf24;">Hidden Health Cost:</strong> High cumulative chronic fatigue. The 1 rest day is vital: without it, cortisol surges and sleep quality drops. With the rest day, tissues remodel smoothly and habit formation reaches peak discipline.
              <div style="margin-top: 8px; display: flex; justify-content: space-between; align-items: center;">
                <span style="color: var(--text-dim);">Sustainability:</span>
                <span style="font-weight: 800; color: #22c55e;">8.8 / 10 (Disciplined &amp; High-Yield)</span>
              </div>
            </div>
          </div>

          <!-- Archetype C -->
          <div class="archetype-card" style="border-top: 3px solid #10b981;">
            <div>
              <div class="archetype-badge" style="background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3);">
                ⚖️ Archetype 3 • Longevity Peak
              </div>
              <div class="archetype-title">The "Interleaved 3-Day Split" Meta</div>
              <div class="archetype-desc">
                3 intense loading days interleaved with active recovery or rest (e.g. Mon: 5k-7k Run, Wed: Heavy Gym/Weights, Fri: Swim or Tempo Run; Tue/Thu: Active Walk/Mobility; Sun: Full Rest). Perfect balance of cardiovascular conditioning and muscular hypertrophy.
              </div>
              <div class="archetype-stats-box">
                <div class="archetype-stat-row">
                  <span class="archetype-stat-label">Weekly Yield:</span>
                  <span class="archetype-stat-val" style="color: var(--strava-orange);">1,700 - 2,500 pts</span>
                </div>
                <div class="archetype-stat-row">
                  <span class="archetype-stat-label">Loading Days:</span>
                  <span class="archetype-stat-val" style="color: #fff;">3 hard + 3 active recovery</span>
                </div>
                <div class="archetype-stat-row">
                  <span class="archetype-stat-label">Time Commitment:</span>
                  <span class="archetype-stat-val">4.0 - 5.5 hours/wk</span>
                </div>
                <div class="archetype-stat-row">
                  <span class="archetype-stat-label">Injury Hazard:</span>
                  <span class="archetype-stat-val" style="color: #10b981;">Lowest in the Contest</span>
                </div>
              </div>
            </div>
            <div class="archetype-health-box">
              <strong style="color:#34d399;">Hidden Health Cost:</strong> <em>Health Positive!</em> Alternating running and weight training allows 48 hours for joint cartilage and tendons to remodel while preventing concurrent training interference (AMPK/mTOR clashes).
              <div style="margin-top: 8px; display: flex; justify-content: space-between; align-items: center;">
                <span style="color: var(--text-dim);">Sustainability:</span>
                <span style="font-weight: 800; color: #10b981;">9.6 / 10 (The Lifelong Health Meta)</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- SECTION 2: HEAD-TO-HEAD TACTICAL SIMULATOR: 10K VS TWO 5K RUNS -->
      <div class="meta-section">
        <div class="meta-section-header">
          <div class="meta-section-title">
            <span>⚡</span> Tactical Duel: Singular 10K Run vs. Two 5K Runs
          </div>
          <div class="meta-section-desc">
            Does splitting a 10K into two 5K bouts give more points under the Unified Foot Sports formula? What are the operational, cardiac, and orthopedic trade-offs?
          </div>
        </div>

        <!-- Simulator Control Bar -->
        <div class="duel-control-panel">
          <div class="meta-slider-group">
            <div class="meta-slider-header">
              <span>Target Total Distance:</span>
              <span id="distSliderDisplay" style="color: #38bdf8; font-family: monospace;">10.0 km (1x 10.0k vs 2x 5.0k)</span>
            </div>
            <input type="range" min="4.0" max="25.0" step="0.5" value="10.0" class="meta-slider" id="metaDistSlider" oninput="update10kVs5kSimulator()">
            <div style="display:flex; justify-content:space-between; font-size:11px; color:var(--text-dim);">
              <span>5.0 km</span>
              <span>10.0 km</span>
              <span>15.0 km</span>
              <span>21.1 km (Half)</span>
            </div>
          </div>

          <div class="meta-slider-group">
            <div class="meta-slider-header">
              <span>Benchmark Base Pace:</span>
              <span id="paceSliderDisplay" style="color: var(--strava-orange); font-family: monospace;">5:15 /km (11.4 km/h)</span>
            </div>
            <input type="range" min="4.25" max="7.5" step="0.05" value="5.25" class="meta-slider" id="metaPaceSlider" oninput="update10kVs5kSimulator()">
            <div style="display:flex; justify-content:space-between; font-size:11px; color:var(--text-dim);">
              <span>4:15 /km (Fast)</span>
              <span>5:30 /km (Aerobic)</span>
              <span>7:30 /km (Easy Jog)</span>
            </div>
          </div>

          <label class="meta-toggle-label">
            <input type="checkbox" id="splitAdvantageToggle" checked onchange="update10kVs5kSimulator()" style="accent-color: var(--strava-orange); width:18px; height:18px;">
            <span>Enable Split Pace Premium (Runners average ~20 sec/km faster on shorter split bouts)</span>
          </label>
        </div>

        <!-- Simulator Head-to-Head Cards -->
        <div class="duel-meta-box">
          <!-- Singular 10K Card -->
          <div class="duel-meta-card" id="card10k">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-weight:800; font-size:15px; color:#fff;">🏃‍♂️ Singular 10K Run</span>
              <span class="meta-badge" style="background:rgba(255,255,255,0.08); color:var(--text-muted);">1 Session</span>
            </div>
            <div class="duel-meta-score" id="ptsDisplay10k">902.5 <span style="font-size:16px; font-weight:600; color:var(--text-muted);">pts</span></div>
            <div style="font-size:12.5px; color:var(--text-dim); margin-bottom:16px;" id="paceDetail10k">Pace: 5:15 /km • Duration: 52.5 min</div>

            <div class="archetype-stats-box">
              <div class="archetype-stat-row">
                <span class="archetype-stat-label">Total Time Footprint:</span>
                <span class="archetype-stat-val" style="color:#22c55e;">~65 min (1 prep, 1 shower)</span>
              </div>
              <div class="archetype-stat-row">
                <span class="archetype-stat-label">Cardiac Drift:</span>
                <span class="archetype-stat-val" style="color:#ef4444;">High (+12-18 bpm late kms)</span>
              </div>
              <div class="archetype-stat-row">
                <span class="archetype-stat-label">Biomechanical Form:</span>
                <span class="archetype-stat-val" style="color:#f59e0b;">Fades in kms 7-10 (Pronation ↑)</span>
              </div>
              <div class="archetype-stat-row">
                <span class="archetype-stat-label">Logistical Friction:</span>
                <span class="archetype-stat-val" style="color:#22c55e;">Minimal (Single cycle)</span>
              </div>
            </div>

            <div style="font-size:12px; color:var(--text-muted); line-height:1.45; border-top:1px dashed rgba(255,255,255,0.1); padding-top:12px;">
              <strong>Strategic Value:</strong> Best for building mental grit, deep mitochondrial capillary density, and high time efficiency. Form breakdown in the final kilometers increases acute knee and plantar tendon strain.
            </div>
          </div>

          <!-- Two 5K Runs Card -->
          <div class="duel-meta-card" id="card2x5k">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-weight:800; font-size:15px; color:#fff;">🏃‍♂️🏃‍♂️ Two 5K Runs (Split "Doubles")</span>
              <span class="meta-badge" id="deltaBadge2x5k" style="background:rgba(34,197,94,0.18); color:#22c55e; border:1px solid rgba(34,197,94,0.35);">+41.8 pts advantage</span>
            </div>
            <div class="duel-meta-score" id="ptsDisplay2x5k">944.3 <span style="font-size:16px; font-weight:600; color:var(--text-muted);">pts</span></div>
            <div style="font-size:12.5px; color:var(--text-dim); margin-bottom:16px;" id="paceDetail2x5k">Each 5K: 4:55 /km • Duration: 24.6 min each (49.2m total)</div>

            <div class="archetype-stats-box">
              <div class="archetype-stat-row">
                <span class="archetype-stat-label">Total Time Footprint:</span>
                <span class="archetype-stat-val" style="color:#ef4444;">~105 min (+40m 2x prep &amp; shower)</span>
              </div>
              <div class="archetype-stat-row">
                <span class="archetype-stat-label">Cardiac Drift:</span>
                <span class="archetype-stat-val" style="color:#22c55e;">Minimal (Zone 3/4 baseline)</span>
              </div>
              <div class="archetype-stat-row">
                <span class="archetype-stat-label">Biomechanical Form:</span>
                <span class="archetype-stat-val" style="color:#22c55e;">Crisp Cadence &amp; Spring Maintained</span>
              </div>
              <div class="archetype-stat-row">
                <span class="archetype-stat-label">Logistical Friction:</span>
                <span class="archetype-stat-val" style="color:#ef4444;">Double (Two outfit changes)</span>
              </div>
            </div>

            <div style="font-size:12px; color:var(--text-muted); line-height:1.45; border-top:1px dashed rgba(255,255,255,0.1); padding-top:12px;">
              <strong>Strategic Value:</strong> Distance dampening allows shorter runs to capture higher speed rewards. Splitting prevents late-stage glycogen exhaustion and thermal stress, but requires double the daily overhead.
            </div>
          </div>
        </div>

        <!-- Coach Verdict Banner -->
        <div id="duelVerdictBox" style="margin-top:20px; padding:16px 20px; border-radius:14px; background:rgba(252,76,2,0.1); border:1px solid rgba(252,76,2,0.3); font-size:13px; line-height:1.5; color:#fff;">
          <strong>Coach's Tactical Verdict:</strong> Loading verdict...
        </div>
      </div>

      <!-- SECTION 3: SPORTS EFFICIENCY & HIDDEN HEALTH COST MATRIX -->
      <div class="meta-section">
        <div class="meta-section-header">
          <div class="meta-section-title">
            <span>📊</span> Activity Efficiency &amp; The Hidden Health Cost Factor (HCF)
          </div>
          <div class="meta-section-desc">
            Every sport has two prices: the time spent on the clock, and the physical wear-and-tear imposed on your body. Here is how all club activities stack up.
          </div>
        </div>

        <!-- Efficiency Table -->
        <div class="meta-table-wrap">
          <table class="meta-table">
            <thead>
              <tr>
                <th>Activity Type</th>
                <th>Points / Minute</th>
                <th>Points / KM</th>
                <th>Time to 1,000 Pts</th>
                <th>Hidden Health Cost Factor</th>
                <th>Longevity Score</th>
                <th>Strategic Arena Role</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>🏊‍♂️ Swimming</strong></td>
                <td><span style="color:#38bdf8; font-weight:800;">14.43 pts/min</span></td>
                <td>391.2 pts/km</td>
                <td>~69 min</td>
                <td><span style="color:#38bdf8; font-weight:700;">+25% Spinal Decompression</span></td>
                <td><strong style="color:#22c55e;">9.8 / 10</strong></td>
                <td>Supreme point density; zero joint wear. High pool access friction.</td>
              </tr>
              <tr>
                <td><strong>🏃‍♂️ Running</strong></td>
                <td><span style="color:#ef4444; font-weight:800;">11.47 pts/min</span></td>
                <td>79.5 pts/km</td>
                <td>~87 min</td>
                <td><span style="color:#f87171; font-weight:700;">-30% Orthopedic Impact Tax</span></td>
                <td><strong style="color:#f59e0b;">6.8 / 10</strong></td>
                <td>Primary leaderboard engine. High injury risk if done daily without gym.</td>
              </tr>
              <tr>
                <td><strong>🚴‍♂️ Outdoor Cycling</strong></td>
                <td><span style="color:#f59e0b; font-weight:800;">5.71 pts/min</span></td>
                <td>14.1 - 19.8 pts/km</td>
                <td>~175 min</td>
                <td><span style="color:#fbbf24; font-weight:700;">+15% Cardiovascular Base</span></td>
                <td><strong style="color:#22c55e;">8.9 / 10</strong></td>
                <td>Rewards big singular weekend rides. Low knee shock, high time demand.</td>
              </tr>
              <tr>
                <td><strong>🏋️ Weight Training</strong></td>
                <td><span style="color:#a855f7; font-weight:800;">4.00 - 5.20 pts/min</span></td>
                <td>N/A (Duration)</td>
                <td>~192 - 250 min</td>
                <td><span style="color:#c084fc; font-weight:700;">+30% Anabolic &amp; Bone Density</span></td>
                <td><strong style="color:#22c55e;">9.4 / 10</strong></td>
                <td>Consistency Multiplier scales to 1.30x on Day 4+. Builds armor for running.</td>
              </tr>
              <tr>
                <td><strong>🔥 Functional Workout</strong></td>
                <td><span style="color:#ec4899; font-weight:800;">4.51 pts/min</span></td>
                <td>N/A (Duration)</td>
                <td>~222 min</td>
                <td><span style="color:#f472b6; font-weight:700;">+15% Core &amp; Agility</span></td>
                <td><strong style="color:#22c55e;">8.7 / 10</strong></td>
                <td>High metabolic conditioning and calisthenics endurance.</td>
              </tr>
              <tr>
                <td><strong>🚶‍♂️ Walking / Hiking</strong></td>
                <td><span style="color:#10b981; font-weight:800;">3.10 pts/min</span></td>
                <td>35.0 pts/km</td>
                <td>~322 min (5.4 hrs)</td>
                <td><span style="color:#34d399; font-weight:700;">+35% Restorative Bonus</span></td>
                <td><strong style="color:#22c55e;">9.9 / 10</strong></td>
                <td><em>Health Positive!</em> Parasympathetic reset; huge opportunity cost.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- The 5K Daily + Gym Callout Box -->
        <div style="margin-top:24px; background:rgba(15,23,42,0.85); border:1px solid rgba(239,68,68,0.3); border-left:4px solid #ef4444; border-radius:16px; padding:20px 24px;">
          <div style="display:flex; align-items:center; gap:10px; font-weight:800; font-size:15px; color:#f87171; margin-bottom:8px;">
            <span>⚠️</span> The "5K Every Day + Daily Gym" Reality Check
          </div>
          <div style="font-size:13px; color:#cbd5e1; line-height:1.6;">
            Running 5k every single day generates <strong>~3,000 pts/week</strong>, but subjects lower extremity joints to <strong>35,000+ impact shocks per week</strong>. Combining daily running with daily heavy lifting triggers the biological <em>Concurrent Training Interference Effect (AMPK vs mTOR clash)</em>: heavy running blunts myofibrillar protein synthesis, while lifting on fatigued legs increases patellar tendinopathy risk exponentially.
            <br><br>
            <strong style="color:#34d399;">The Smart Meta Alternative:</strong> Replace 3 of those runs with <strong>active recovery walks</strong> (35 pts/km) and keep 3 dedicated running days. Walking provides the necessary non-glycolytic blood flow to clear metabolic waste, restores parasympathetic tone, and leaves tendons fresh for deep gym lifts!
          </div>
        </div>
      </div>

      <!-- SECTION 4: INTERACTIVE ROUTINE ARCHITECT & LONGEVITY CALCULATOR -->
      <div class="meta-section">
        <div class="meta-section-header">
          <div class="meta-section-title">
            <span>🛠️</span> Interactive Routine Architect &amp; Health Viability Simulator
          </div>
          <div class="meta-section-desc">
            Construct your weekly training schedule to balance Arena points, time investment, orthopedic stress, and long-term health sustainability.
          </div>
        </div>

        <!-- Presets Bar -->
        <div class="routine-presets-bar">
          <button class="routine-preset-pill active" id="presetBtnIron" onclick="applyRoutinePreset('iron')">🏋️ Iron 6-1 Hybrid (3 Run + 3 Gym + 1 Rest)</button>
          <button class="routine-preset-pill" id="presetBtnSplit" onclick="applyRoutinePreset('split')">⚖️ 3-Day Interleaved (2 Run + 2 Gym + 2 Walk)</button>
          <button class="routine-preset-pill" id="presetBtnDaily" onclick="applyRoutinePreset('daily')">🏃‍♂️ 5K Daily Grinder (7 Runs)</button>
          <button class="routine-preset-pill" id="presetBtnApex" onclick="applyRoutinePreset('apex')">⚡ Apex Singularity (1 Big Run + 1 Epic Ride + 1 Gym)</button>
          <button class="routine-preset-pill" id="presetBtnWalker" onclick="applyRoutinePreset('walker')">🚶‍♂️ The Walking Purist (7 Daily Walks)</button>
        </div>

        <!-- Mode Switcher -->
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:16px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:12px; font-weight:800; text-transform:uppercase; color:var(--text-muted); letter-spacing:0.5px;">Architect Mode:</span>
            <button class="routine-preset-pill active" id="modeBtnFreq" onclick="switchRoutineMode('freq')">📅 Frequency Mode (Days/Wk)</button>
            <button class="routine-preset-pill" id="modeBtnVolume" onclick="switchRoutineMode('volume')">⏱️ Hours &amp; KM Volume Mode</button>
          </div>
        </div>

        <div class="routine-grid">
          <!-- Left: Frequency Sliders Box -->
          <div class="routine-sliders-box" id="routineBoxFreq">
            <div class="routine-slider-item">
              <div class="routine-slider-header">
                <span>🏃‍♂️ Runs per Week (5.0 km @ 5:30/km):</span>
                <span id="sliderValRuns" style="color:var(--strava-orange); font-weight:800;">3 days</span>
              </div>
              <input type="range" min="0" max="7" step="1" value="3" class="meta-slider" id="sliderRuns" oninput="updateRoutineArchitect()">
            </div>

            <div class="routine-slider-item">
              <div class="routine-slider-header">
                <span>🏋️ Gym / Weights per Week (45 min sessions):</span>
                <span id="sliderValGym" style="color:#a855f7; font-weight:800;">3 days (1.20x Mult)</span>
              </div>
              <input type="range" min="0" max="7" step="1" value="3" class="meta-slider" id="sliderGym" oninput="updateRoutineArchitect()">
            </div>

            <div class="routine-slider-item">
              <div class="routine-slider-header">
                <span>🚶‍♂️ Walks per Week (5.0 km brisk stroll):</span>
                <span id="sliderValWalks" style="color:#10b981; font-weight:800;">0 days</span>
              </div>
              <input type="range" min="0" max="7" step="1" value="0" class="meta-slider" id="sliderWalks" oninput="updateRoutineArchitect()">
            </div>

            <div class="routine-slider-item">
              <div class="routine-slider-header">
                <span>🚴‍♂️ Cycling Rides per Week (20.0 km road ride):</span>
                <span id="sliderValRides" style="color:#f59e0b; font-weight:800;">0 days</span>
              </div>
              <input type="range" min="0" max="7" step="1" value="0" class="meta-slider" id="sliderRides" oninput="updateRoutineArchitect()">
            </div>

            <div class="routine-slider-item">
              <div class="routine-slider-header">
                <span>🏊‍♂️ Swims per Week (1.2 km pool session):</span>
                <span id="sliderValSwims" style="color:#38bdf8; font-weight:800;">0 days</span>
              </div>
              <input type="range" min="0" max="7" step="1" value="0" class="meta-slider" id="sliderSwims" oninput="updateRoutineArchitect()">
            </div>
          </div>

          <!-- Left: Volume & Distance Sliders Box (Initially Hidden) -->
          <div class="routine-sliders-box" id="routineBoxVolume" style="display:none;">
            <div class="routine-slider-item">
              <div class="routine-slider-header">
                <span>⏱️ Total Weekly Hours Budget:</span>
                <span id="sliderValVolBudget" style="color:#38bdf8; font-weight:800;">6.0 hours / week</span>
              </div>
              <input type="range" min="1.0" max="14.0" step="0.5" value="6.0" class="meta-slider" id="sliderVolBudget" oninput="updateRoutineArchitect()">
            </div>

            <div class="routine-slider-item">
              <div class="routine-slider-header">
                <span>🏃‍♂️ Weekly Running Distance:</span>
                <span id="sliderValVolRun" style="color:var(--strava-orange); font-weight:800;">15.0 km (~1.4 hrs)</span>
              </div>
              <input type="range" min="0" max="60" step="1" value="15" class="meta-slider" id="sliderVolRun" oninput="updateRoutineArchitect()">
            </div>

            <div class="routine-slider-item">
              <div class="routine-slider-header">
                <span>🏋️ Weekly Gym &amp; Resistance Time:</span>
                <span id="sliderValVolGym" style="color:#a855f7; font-weight:800;">2.5 hours</span>
              </div>
              <input type="range" min="0" max="8" step="0.5" value="2.5" class="meta-slider" id="sliderVolGym" oninput="updateRoutineArchitect()">
            </div>

            <div class="routine-slider-item">
              <div class="routine-slider-header">
                <span>🚶‍♂️ Weekly Walking Distance:</span>
                <span id="sliderValVolWalk" style="color:#10b981; font-weight:800;">10.0 km (~1.8 hrs)</span>
              </div>
              <input type="range" min="0" max="50" step="1" value="10" class="meta-slider" id="sliderVolWalk" oninput="updateRoutineArchitect()">
            </div>

            <div class="routine-slider-item">
              <div class="routine-slider-header">
                <span>🚴‍♂️ Weekly Cycling Distance:</span>
                <span id="sliderValVolRide" style="color:#f59e0b; font-weight:800;">20.0 km (~0.8 hrs)</span>
              </div>
              <input type="range" min="0" max="150" step="5" value="20" class="meta-slider" id="sliderVolRide" oninput="updateRoutineArchitect()">
            </div>

            <div class="routine-slider-item">
              <div class="routine-slider-header">
                <span>🏊‍♂️ Weekly Swimming Distance:</span>
                <span id="sliderValVolSwim" style="color:#38bdf8; font-weight:800;">1.0 km (~0.4 hrs)</span>
              </div>
              <input type="range" min="0" max="8" step="0.2" value="1.0" class="meta-slider" id="sliderVolSwim" oninput="updateRoutineArchitect()">
            </div>
          </div>

          <!-- Right: Diagnostic Output Gauge -->
          <div class="routine-gauge-card">
            <div>
              <div style="font-size:12px; text-transform:uppercase; letter-spacing:1px; color:var(--text-muted); font-weight:800;">
                Weekly Schedule Projection
              </div>
              <div style="display:flex; justify-content:space-between; align-items:baseline; margin-top:8px;">
                <div style="font-family:'Outfit', sans-serif; font-size:36px; font-weight:900; color:#fff;" id="routineTotalPts">
                  1,869 <span style="font-size:16px; font-weight:600; color:var(--text-muted);">pts / week</span>
                </div>
                <div style="font-size:13px; font-weight:700; color:var(--strava-orange);" id="routineTotalHours">
                  ~3.6 hours / wk
                </div>
              </div>
              <div style="font-size:12px; color:var(--text-dim);" id="routineVelocityDisplay">
                Points Velocity: 519 pts/hr of active movement
              </div>
            </div>

            <!-- Health & Stress Meters -->
            <div>
              <div style="display:flex; justify-content:space-between; font-size:12.5px; font-weight:700;">
                <span>Orthopedic Impact Load:</span>
                <span id="routineImpactLabel" style="color:#f59e0b;">Moderate Impact</span>
              </div>
              <div class="routine-meter-bar">
                <div class="routine-meter-fill" id="routineImpactFill" style="width:45%; background:#f59e0b;"></div>
              </div>

              <div style="display:flex; justify-content:space-between; font-size:12.5px; font-weight:700; margin-top:14px;">
                <span>Longevity &amp; Sustainability Score:</span>
                <span id="routineLongevityLabel" style="color:#22c55e;">88 / 100</span>
              </div>
              <div class="routine-meter-bar">
                <div class="routine-meter-fill" id="routineLongevityFill" style="width:88%; background:#22c55e;"></div>
              </div>
            </div>

            <!-- Coaching Diagnostic -->
            <div id="routineCoachAdvice" style="font-size:12.5px; line-height:1.5; color:#cbd5e1; background:rgba(0,0,0,0.3); border-radius:12px; padding:12px 16px;">
              Diagnostic evaluating...
            </div>
          </div>
        </div>
      </div>

      <!-- SECTION 5: REAL CLUB LEADER META BREAKDOWN -->
      <div class="meta-section">
        <div class="meta-section-header">
          <div class="meta-section-title">
            <span>🏆</span> Club Leader Strategy Breakdown
          </div>
          <div class="meta-section-desc">
            Algorithmic classification of current club athletes into their empirical meta-game strategies based on real activity logs.
          </div>
        </div>

        <div class="meta-table-wrap">
          <table class="meta-table" id="leaderMetasTable">
            <thead>
              <tr>
                <th>Rank &amp; Athlete</th>
                <th>Detected Meta Archetype</th>
                <th>Primary Sport</th>
                <th>Contest Points</th>
                <th>Peak Single Effort</th>
                <th>Points Velocity</th>
                <th>Health Sustainability</th>
              </tr>
            </thead>
            <tbody id="leaderMetasTbody">
              <tr><td colspan="7" style="text-align:center; color:var(--text-muted);">Loading leader metas...</td></tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>

  </div>

  <!-- Toast Element -->
  <div id="toastNotification">
    <span id="toastMsg">✅ Roster copied!</span>
  </div>

  <!-- Precalculated Squads for Instant Client-Side Zero-Latency Rendering -->
  <script id="precalculated-squads-data" type="application/json">
<!-- PRECALCULATED_SQUADS_PLACEHOLDER -->
  </script>

  <!-- Embedded fallback JSON data for seamless offline rendering -->
  <script id="fallback-data" type="application/json">
<!-- FALLBACK_DATA_PLACEHOLDER -->
  </script>

  <script>
    let globalData = null;
    let PRECALC_SQUADS = null;
    let duelRadarChartInstance = null;

    // Date Filter State (Default: Sep 14, 2026 onwards)
    window.currentDateStart = '2026-09-14';
    window.currentDateEnd = '';
    window.currentPreset = 'tournament';

    // Team Builder State
    let currentTeamCount = 4;
    let activeRosters = []; // array of member name arrays
    let viewMode = 'active'; // 'active' or 'full'
    let memberFilterQuery = '';

    const SQUAD_METAS = [
      {"id": 0, "name": "Red Phoenix", "color": "#ef4444", "bg": "rgba(239, 68, 68, 0.12)", "border": "rgba(239, 68, 68, 0.35)", "icon": "🔴"},
      {"id": 1, "name": "Blue Hydra", "color": "#3b82f6", "bg": "rgba(59, 130, 246, 0.12)", "border": "rgba(59, 130, 246, 0.35)", "icon": "🔵"},
      {"id": 2, "name": "Emerald Dragons", "color": "#10b981", "bg": "rgba(16, 185, 129, 0.12)", "border": "rgba(16, 185, 129, 0.35)", "icon": "🟢"},
      {"id": 3, "name": "Golden Gryphons", "color": "#f59e0b", "bg": "rgba(245, 158, 11, 0.12)", "border": "rgba(245, 158, 11, 0.35)", "icon": "🟡"},
      {"id": 4, "name": "Shadow Vipers", "color": "#a855f7", "bg": "rgba(168, 85, 247, 0.12)", "border": "rgba(168, 85, 247, 0.35)", "icon": "🟣"},
      {"id": 5, "name": "Solar Titans", "color": "#f97316", "bg": "rgba(249, 115, 22, 0.12)", "border": "rgba(249, 115, 22, 0.35)", "icon": "🟠"},
      {"id": 6, "name": "Silver Wolves", "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.12)", "border": "rgba(148, 163, 184, 0.35)", "icon": "⚪"},
      {"id": 7, "name": "Neon Cyber", "color": "#06b6d4", "bg": "rgba(6, 182, 212, 0.12)", "border": "rgba(6, 182, 212, 0.35)", "icon": "🔷"},
      {"id": 8, "name": "Thunder Hawks", "color": "#eab308", "bg": "rgba(234, 179, 8, 0.12)", "border": "rgba(234, 179, 8, 0.35)", "icon": "⚡"},
      {"id": 9, "name": "Magma Giants", "color": "#dc2626", "bg": "rgba(220, 38, 38, 0.12)", "border": "rgba(220, 38, 38, 0.35)", "icon": "🌋"},
      {"id": 10, "name": "Frost Phantoms", "color": "#38bdf8", "bg": "rgba(56, 189, 248, 0.12)", "border": "rgba(56, 189, 248, 0.35)", "icon": "❄️"},
      {"id": 11, "name": "Iron Rangers", "color": "#84cc16", "bg": "rgba(132, 204, 22, 0.12)", "border": "rgba(132, 204, 22, 0.35)", "icon": "🏹"},
      {"id": 12, "name": "Tidal Krakens", "color": "#2563eb", "bg": "rgba(37, 99, 235, 0.12)", "border": "rgba(37, 99, 235, 0.35)", "icon": "🌊"},
      {"id": 13, "name": "Forest Striders", "color": "#059669", "bg": "rgba(5, 150, 105, 0.12)", "border": "rgba(5, 150, 105, 0.35)", "icon": "🌲"},
      {"id": 14, "name": "Cosmic Nova", "color": "#ec4899", "bg": "rgba(236, 72, 153, 0.12)", "border": "rgba(236, 72, 153, 0.35)", "icon": "🌌"},
      {"id": 15, "name": "Aegis Knights", "color": "#64748b", "bg": "rgba(100, 116, 139, 0.12)", "border": "rgba(100, 116, 139, 0.35)", "icon": "🛡️"},
      {"id": 16, "name": "Vortex Storm", "color": "#8b5cf6", "bg": "rgba(139, 92, 246, 0.12)", "border": "rgba(139, 92, 246, 0.35)", "icon": "🌪️"},
      {"id": 17, "name": "Orbit Centurions", "color": "#d97706", "bg": "rgba(217, 119, 6, 0.12)", "border": "rgba(217, 119, 6, 0.35)", "icon": "🪐"},
      {"id": 18, "name": "Mystic Sorcerers", "color": "#c084fc", "bg": "rgba(192, 132, 252, 0.12)", "border": "rgba(192, 132, 252, 0.35)", "icon": "🔮"},
      {"id": 19, "name": "Apex Predators", "color": "#b91c1c", "bg": "rgba(185, 28, 28, 0.12)", "border": "rgba(185, 28, 28, 0.35)", "icon": "🦁"}
    ];

    const MILESTONES = [
      { city: "Bangalore", km: 0, icon: "🏁" },
      { city: "Mysore", km: 140, icon: "🏰" },
      { city: "Chennai", km: 350, icon: "🌊" },
      { city: "Goa", km: 560, icon: "🏖️" },
      { city: "Hyderabad", km: 880, icon: "💎" },
      { city: "Mumbai", km: 1400, icon: "🏙️" },
      { city: "Jaipur", km: 1950, icon: "🕌" },
      { city: "New Delhi", km: 2220, icon: "🏛️" }
    ];

    const DARES = [
      { icon: "🌅", title: "The Sunrise 5k Cruise", desc: "Log a continuous 5.0 km run or walk before 7:30 AM. Earn dynamic pace points and lead the Dawn Patrol trophy.", pts: "~110 - 145 pts" },
      { icon: "⚡", title: "Negative Split 4k", desc: "Run 4 km outdoor where your second 2 km is at least 15 sec/km faster than your first 2 km.", pts: "~120 - 160 pts" },
      { icon: "🚴", title: "Virtual Century Sprint", desc: "Complete 15.0+ km on an indoor smart trainer or outdoor cycling route maintaining steady cadence.", pts: "~95 - 130 pts" },
      { icon: "🔥", title: "Midday 30m Tabata Burn", desc: "Log 30 minutes of high-intensity functional workout or weight training during lunch hour.", pts: "~90 - 120 pts" },
      { icon: "🦉", title: "Night Hawk Recovery Stride", desc: "Log a 4.0 km walk or gentle jog after 8:30 PM under the stars to claim the Night Owl badge.", pts: "~80 - 100 pts" },
      { icon: "⛰️", title: "The Elevation Challenge", desc: "Find a route with at least 50m of elevation gain across your run or walk.", pts: "~130 - 170 pts" }
    ];

    function showToast(msg) {
      const t = document.getElementById('toastNotification');
      document.getElementById('toastMsg').innerText = msg;
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 3200);
    }

    function switchArenaTab(tabId) {
      document.querySelectorAll('.arena-panel').forEach(p => p.classList.remove('active'));
      document.querySelectorAll('.arena-nav-tab').forEach(b => b.classList.remove('active'));

      const activePanel = document.getElementById(tabId);
      if (activePanel) activePanel.classList.add('active');

      const btnMap = {
        'tabDuel': 'tabBtnDuel',
        'tabTeamBuilder': 'tabBtnTeamBuilder',
        'tabTrophies': 'tabBtnTrophies',
        'tabMomentum': 'tabBtnMomentum',
        'tabJourney': 'tabBtnJourney',
        'tabRoulette': 'tabBtnRoulette',
        'tabMeta': 'tabBtnMeta'
      };

      if (btnMap[tabId]) {
        const btn = document.getElementById(btnMap[tabId]);
        if (btn) btn.classList.add('active');
      }

      if (tabId === 'tabDuel') {
        setTimeout(() => updateDuel(), 50);
      } else if (tabId === 'tabTeamBuilder') {
        setTimeout(() => renderTeamBuilder(), 50);
      } else if (tabId === 'tabRoulette') {
        setTimeout(() => renderWorkoutRoulette(), 50);
      } else if (tabId === 'tabMeta') {
        setTimeout(() => renderMetaLab(), 50);
      }
    }

    function setDatePreset(preset) {
      window.currentPreset = preset;
      document.querySelectorAll('.preset-pill').forEach(b => b.classList.remove('active'));

      const startInput = document.getElementById('dateStart');
      const endInput = document.getElementById('dateEnd');

      if (preset === 'tournament') {
        document.getElementById('presetTournament').classList.add('active');
        window.currentDateStart = '2026-09-14';
        window.currentDateEnd = '';
        startInput.value = '2026-09-14';
        endInput.value = '';
      } else if (preset === 'all') {
        document.getElementById('presetAll').classList.add('active');
        window.currentDateStart = '';
        window.currentDateEnd = '';
        startInput.value = '';
        endInput.value = '';
      } else if (preset === '7days') {
        document.getElementById('preset7Days').classList.add('active');
        const d = new Date('2026-09-10');
        d.setDate(d.getDate() - 7);
        const startStr = d.toISOString().slice(0, 10);
        window.currentDateStart = startStr;
        window.currentDateEnd = '';
        startInput.value = startStr;
        endInput.value = '';
      }

      applyFilterAndRerender();
    }

    function onCustomDateChange() {
      window.currentDateStart = document.getElementById('dateStart').value;
      window.currentDateEnd = document.getElementById('dateEnd').value;
      document.querySelectorAll('.preset-pill').forEach(b => b.classList.remove('active'));
      applyFilterAndRerender();
    }

    function getFilteredActivities() {
      if (!globalData || !globalData.activities) return [];
      return globalData.activities.filter(act => {
        const iso = act.datetime_iso || '';
        const dStr = iso.slice(0, 10);
        if (window.currentDateStart && dStr < window.currentDateStart) return false;
        if (window.currentDateEnd && dStr > window.currentDateEnd) return false;
        return true;
      });
    }

    function applyFilterAndRerender() {
      const acts = getFilteredActivities();
      const badge = document.getElementById('activityCountBadge');
      if (badge) {
        badge.innerText = `Showing ${acts.length} activities (${window.currentDateStart ? window.currentDateStart : 'Earliest'} → ${window.currentDateEnd ? window.currentDateEnd : 'Present'})`;
      }

      resetToPrecalculated();
      renderTrophies();
      initDuelSelectors(true);
      updateDuel();
      renderVirtualJourney();
      renderMomentum();
      renderWorkoutRoulette();
      renderMetaLab();
    }

    function computeAthleteStats(activities) {
      const statsMap = {};

      (globalData.athletes || []).forEach(a => {
        statsMap[a.athlete_name] = {
          athlete_name: a.athlete_name,
          total_points: 0,
          total_distance: 0,
          total_duration_hours: 0,
          total_activities: 0,
          sports: {},
          fastest_pace_val: 999,
          fastest_pace_str: 'N/A',
          max_single_dist: 0,
          max_single_duration: 0,
          night_owl_count: 0,
          dawn_patrol_count: 0,
          active_dates: new Set(),
          hero_class_name: 'Sentinel',
          hero_class_icon: '🛡️',
          hero_class_color: '#fbbf24'
        };
      });

      activities.forEach(act => {
        const name = act.athlete_name;
        if (!statsMap[name]) {
          statsMap[name] = {
            athlete_name: name,
            total_points: 0,
            total_distance: 0,
            total_duration_hours: 0,
            total_activities: 0,
            sports: {},
            fastest_pace_val: 999,
            fastest_pace_str: 'N/A',
            max_single_dist: 0,
            max_single_duration: 0,
            night_owl_count: 0,
            dawn_patrol_count: 0,
            active_dates: new Set(),
            hero_class_name: 'Sentinel',
            hero_class_icon: '🛡️',
            hero_class_color: '#fbbf24'
          };
        }

        const st = statsMap[name];
        const pts = parseFloat(act.points_dynamic || act.points || 0);
        const dist = parseFloat(act.distance_km || 0);
        const durMin = parseFloat(act.duration_minutes || 0);

        st.total_points += pts;
        st.total_distance += dist;
        st.total_duration_hours += durMin / 60;
        st.total_activities += 1;

        const sp = act.activity_type || 'Other';
        st.sports[sp] = (st.sports[sp] || 0) + 1;
        if (dist > st.max_single_dist) st.max_single_dist = dist;
        if (durMin > st.max_single_duration) st.max_single_duration = durMin;

        const iso = act.datetime_iso || act.datetime_utc || '';
        if (iso) {
          const d = new Date(iso);
          if (!isNaN(d)) {
            st.active_dates.add(iso.slice(0, 10));
            const h = d.getHours();
            if (h >= 20) st.night_owl_count += 1;
            if (h < 7 || (h === 7 && d.getMinutes() <= 30)) st.dawn_patrol_count += 1;
          }
        }

        if (act.activity_type && act.activity_type.toLowerCase().includes('run') && dist >= 2.5 && durMin > 0) {
          const paceDec = durMin / dist;
          if (paceDec < st.fastest_pace_val && paceDec > 2.5) {
            st.fastest_pace_val = paceDec;
            st.fastest_pace_str = act.pace || `${Math.floor(paceDec)}:${Math.round((paceDec%1)*60)} /km`;
          }
        }
      });

      Object.values(statsMap).forEach(st => {
        const sc = Object.keys(st.sports).length;
        if (sc >= 2) {
          st.hero_class_name = 'Polymath';
          st.hero_class_icon = '🧙‍♂️';
          st.hero_class_color = '#38bdf8';
        } else if (st.fastest_pace_val < 5.4) {
          st.hero_class_name = 'Assassin';
          st.hero_class_icon = '⚡';
          st.hero_class_color = '#a855f7';
        } else if (st.total_distance >= 25 || st.max_single_dist >= 10) {
          st.hero_class_name = 'Ranger';
          st.hero_class_icon = '🏹';
          st.hero_class_color = '#22c55e';
        } else if ((st.sports['Weight Training']||0) + (st.sports['Workout']||0) + (st.sports['Swim']||0) > 0 || st.max_single_duration >= 60) {
          st.hero_class_name = 'Berserker';
          st.hero_class_icon = '🏋️';
          st.hero_class_color = '#ef4444';
        } else {
          st.hero_class_name = 'Sentinel';
          st.hero_class_icon = '🛡️';
          st.hero_class_color = '#fbbf24';
        }
        st.hero_class = `${st.hero_class_icon} ${st.hero_class_name}`;
      });

      return statsMap;
    }

    /* =========================================================================
       1. TEAM BUILDER - PRECALCULATED & ZERO-LATENCY LOGIC
       ========================================================================= */
    function initSquadDropdown() {
      const sel = document.getElementById('squadSelectDropdown');
      if (!sel) return;
      let opts = '';
      for (let k = 2; k <= 20; k++) {
        const approxPerSquad = Math.round(118 / k);
        opts += `<option value="${k}" ${k === currentTeamCount ? 'selected' : ''}>${k} Squads (~${approxPerSquad} members each)</option>`;
      }
      sel.innerHTML = opts;
    }

    function setSquadCount(count) {
      currentTeamCount = count;
      document.querySelectorAll('.tb-squad-btn').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById(`squadBtn${count}`);
      if (activeBtn) activeBtn.classList.add('active');

      const sel = document.getElementById('squadSelectDropdown');
      if (sel) sel.value = count;

      resetToPrecalculated();
    }

    function resetToPrecalculated() {
      const mode = (window.currentDateStart && window.currentDateStart >= '2026-09-14') ? 'tournament' : 'all_time';
      if (PRECALC_SQUADS && PRECALC_SQUADS[mode] && PRECALC_SQUADS[mode][currentTeamCount]) {
        // Deep copy precalculated member arrays
        activeRosters = PRECALC_SQUADS[mode][currentTeamCount].map(arr => arr.slice());
      } else {
        // Fallback
        activeRosters = Array.from({ length: currentTeamCount }, () => []);
      }
      renderTeamBuilder();
    }

    function setViewMode(mode) {
      viewMode = mode;
      document.getElementById('viewActiveOnly').classList.toggle('active', mode === 'active');
      document.getElementById('viewFullRoster').classList.toggle('active', mode === 'full');
      renderTeamBuilder();
    }

    function onSearchMember(query) {
      memberFilterQuery = query.toLowerCase().trim();
      renderTeamBuilder();
    }

    function moveAthlete(athleteName, targetIdx) {
      targetIdx = parseInt(targetIdx);
      for (let i = 0; i < currentTeamCount; i++) {
        activeRosters[i] = (activeRosters[i] || []).filter(n => n !== athleteName);
      }
      if (activeRosters[targetIdx]) {
        activeRosters[targetIdx].push(athleteName);
      }
      renderTeamBuilder();
    }

    function calculateTeamSynergies(memberNames, statsMap) {
      const members = memberNames.map(n => statsMap[n] || {
        athlete_name: n,
        total_points: 0,
        total_distance: 0,
        total_duration_hours: 0,
        total_activities: 0,
        sports: {},
        night_owl_count: 0,
        dawn_patrol_count: 0,
        hero_class: '🛡️ Sentinel',
        hero_class_name: 'Sentinel',
        hero_class_color: '#fbbf24'
      });

      const activeBuffs = [];
      let totalBuffPct = 0;

      const allSports = new Set();
      members.forEach(m => Object.keys(m.sports).forEach(s => allSports.add(s.toLowerCase())));
      const hasRun = Array.from(allSports).some(s => s.includes('run'));
      const hasWalk = Array.from(allSports).some(s => s.includes('walk') || s.includes('hike'));
      const hasOther = Array.from(allSports).some(s => s.includes('ride') || s.includes('train') || s.includes('workout') || s.includes('swim'));
      if (hasRun && hasWalk && hasOther) {
        activeBuffs.push({ name: "✨ Tri-Sport Mastery", pct: 8, desc: "Roster spans Running, Walking, & Cycling/Workouts" });
        totalBuffPct += 8;
      }

      const totalNight = members.reduce((sum, m) => sum + m.night_owl_count, 0);
      const totalDawn = members.reduce((sum, m) => sum + m.dawn_patrol_count, 0);
      if (totalNight >= 1 && totalDawn >= 1) {
        activeBuffs.push({ name: "🌙 24-Hour Watch", pct: 5, desc: "Features both Dawn Patrol and Night Owl athletes" });
        totalBuffPct += 5;
      }

      const uniqueClasses = new Set(members.filter(m => m.total_activities > 0).map(m => m.hero_class_name));
      if (uniqueClasses.size >= 3) {
        activeBuffs.push({ name: "🛡️ Class Quintet", pct: 10, desc: `Balanced party of ${uniqueClasses.size} distinct Hero Classes` });
        totalBuffPct += 10;
      }

      if (uniqueClasses.has('Ranger') && uniqueClasses.has('Assassin')) {
        activeBuffs.push({ name: "⚡ Speed & Stamina", pct: 6, desc: "Pairs endurance Ranger with speed Assassin" });
        totalBuffPct += 6;
      }

      const basePoints = members.reduce((sum, m) => sum + m.total_points, 0);
      const adjustedPoints = Math.round(basePoints * (1 + totalBuffPct / 100));
      const totalDist = members.reduce((sum, m) => sum + m.total_distance, 0);
      const totalHours = members.reduce((sum, m) => sum + m.total_duration_hours, 0);

      const activeMembers = members.filter(m => m.total_activities > 0).sort((a, b) => b.total_points - a.total_points);
      const reserveMembers = members.filter(m => m.total_activities === 0).sort((a, b) => a.athlete_name.localeCompare(b.athlete_name));

      return {
        basePoints: Math.round(basePoints),
        totalBuffPct,
        adjustedPoints,
        totalDist: (Math.round(totalDist * 10) / 10).toFixed(1),
        totalHours: (Math.round(totalHours * 10) / 10).toFixed(1),
        activeBuffs,
        activeMembers,
        reserveMembers,
        totalMemberCount: members.length
      };
    }

    function renderTeamBuilder() {
      const statsMap = computeAthleteStats(getFilteredActivities());
      const grid = document.getElementById('tbSquadGrid');
      const balanceMeter = document.getElementById('tbBalanceMeter');
      if (!grid || !balanceMeter) return;

      let totalActiveScorers = 0;
      Object.values(statsMap).forEach(s => { if (s.total_activities > 0) totalActiveScorers++; });
      document.getElementById('activeScorerCount').innerText = totalActiveScorers;

      const squadData = [];
      for (let i = 0; i < currentTeamCount; i++) {
        const meta = SQUAD_METAS[i % SQUAD_METAS.length];
        const data = calculateTeamSynergies(activeRosters[i] || [], statsMap);
        squadData.push({ meta, data, idx: i });
      }

      // Render Balance Meter
      const totalAdj = squadData.reduce((sum, s) => sum + s.data.adjustedPoints, 0) || 1;
      let meterHtml = '';
      squadData.forEach(s => {
        const pct = ((s.data.adjustedPoints / totalAdj) * 100).toFixed(1);
        meterHtml += `<div class="tb-meter-segment" style="width:${pct}%; background:${s.meta.color};" title="${s.meta.name}: ${s.data.adjustedPoints} pts (${pct}%)"></div>`;
      });
      balanceMeter.innerHTML = meterHtml;

      // Status text
      const maxPts = Math.max(...squadData.map(s => s.data.adjustedPoints));
      const minPts = Math.min(...squadData.map(s => s.data.adjustedPoints));
      const delta = maxPts - minPts;
      const statusEl = document.getElementById('tbBalanceStatus');
      if (delta <= 30) {
        statusEl.innerHTML = `⚖️ Statistically Even: Δ ${delta} pts variance across ${currentTeamCount} squads`;
        statusEl.style.color = 'var(--accent-green)';
      } else {
        const leader = squadData.find(s => s.data.adjustedPoints === maxPts);
        statusEl.innerHTML = `⚡ Leader: ${leader.meta.name} (+${delta} pts delta)`;
        statusEl.style.color = 'var(--gold)';
      }

      // Render Squad Columns
      grid.innerHTML = squadData.map(s => {
        const { meta, data, idx } = s;

        let synergyHtml = '';
        if (data.activeBuffs.length === 0) {
          synergyHtml = `<span style="font-size:10.5px; color:var(--text-dim); font-style:italic;">No active synergies.</span>`;
        } else {
          synergyHtml = data.activeBuffs.map(b => `
            <span class="tb-synergy-pill" style="background:${meta.bg}; border-color:${meta.border}; color:${meta.color};" title="${b.desc}">
              ${b.name} <strong style="color:#fff;">+${b.pct}%</strong>
            </span>
          `).join('');
        }

        // Filter members by search query if any
        let displayedActive = data.activeMembers;
        let displayedReserve = data.reserveMembers;
        if (memberFilterQuery) {
          displayedActive = displayedActive.filter(m => m.athlete_name.toLowerCase().includes(memberFilterQuery));
          displayedReserve = displayedReserve.filter(m => m.athlete_name.toLowerCase().includes(memberFilterQuery));
        }

        const renderPlayerRow = (m, isReserve) => {
          let moveOptions = '';
          for (let o = 0; o < currentTeamCount; o++) {
            if (o !== idx) {
              moveOptions += `<option value="${o}">Move → ${SQUAD_METAS[o % SQUAD_METAS.length].name}</option>`;
            }
          }

          const initials = m.athlete_name.split(' ').map(p => p[0]).join('').slice(0, 2).toUpperCase();

          const ptsVal = Math.round(m.total_points || 0);

          return `
            <div class="tb-player-card ${isReserve ? 'reserve' : ''}">
              <div class="tb-player-info">
                <div class="tb-player-avatar">${initials}</div>
                <div>
                  <div class="tb-player-name" title="${m.athlete_name}">${m.athlete_name}</div>
                  <span class="tb-class-badge" style="background:${m.hero_class_color}22; border:1px solid ${m.hero_class_color}44; color:${m.hero_class_color};">
                    ${m.hero_class}
                  </span>
                </div>
              </div>
              <div style="display:flex; align-items:center; gap:8px;">
                <div class="tb-player-stats">
                  <div class="tb-player-pts-tag ${ptsVal === 0 ? 'zero-pts' : ''}">
                    ${ptsVal.toLocaleString()} <span class="pts-unit">pts</span>
                  </div>
                  <div class="tb-player-sub">${(Math.round((m.total_distance || 0) * 10) / 10).toFixed(1)} km • ${m.total_activities || 0} logs</div>
                </div>
                <select class="tb-move-select" onchange="moveAthlete('${m.athlete_name.replace(/'/g, "\\'")}', this.value)">
                  <option value="${idx}" selected>Team</option>
                  ${moveOptions}
                </select>
              </div>
            </div>
          `;
        };

        const activeRows = displayedActive.map(m => renderPlayerRow(m, false)).join('');
        const reserveRows = displayedReserve.map(m => renderPlayerRow(m, true)).join('');

        let listContent = activeRows;
        if (viewMode === 'full') {
          if (displayedReserve.length > 0) {
            listContent += `
              <div style="font-size:11px; font-weight:800; text-transform:uppercase; color:var(--text-dim); margin-top:8px; padding-top:8px; border-top:1px dashed var(--card-border);">
                Registered Candidates (${displayedReserve.length})
              </div>
              ${reserveRows}
            `;
          }
        }

        if (!listContent.trim()) {
          listContent = `<div style="text-align:center; padding:18px; color:var(--text-dim); font-size:12px;">No matching members</div>`;
        }

        return `
          <div class="tb-squad-card" style="border-top: 4px solid ${meta.color};">
            <div class="tb-squad-header">
              <div class="tb-squad-name" style="color:${meta.color};">
                <span>${meta.icon}</span> ${meta.name}
              </div>
              <div style="text-align:right;">
                <div class="tb-squad-score" style="color:${meta.color};">${data.adjustedPoints.toLocaleString()}</div>
                <div style="font-size:10.5px; color:var(--text-muted);">Base: ${data.basePoints.toLocaleString()} pts (+${data.totalBuffPct}%)</div>
              </div>
            </div>

            <div class="tb-squad-meta-bar">
              <span>🏃‍♂️ ${data.totalDist} km</span>
              <span>⏱️ ${data.totalHours} hrs</span>
              <span>👥 ${data.activeMembers.length} active (${data.totalMemberCount} total)</span>
            </div>

            <div class="tb-synergy-tray">
              ${synergyHtml}
            </div>

            <div class="tb-roster-list">
              ${listContent}
            </div>
          </div>
        `;
      }).join('');
    }

    function copyTeamRoster() {
      const statsMap = computeAthleteStats(getFilteredActivities());
      const lines = [];
      lines.push("🏆 CONNECTIVITY SPORTS DAY 2026 - BALANCED SQUADS 🏆");
      lines.push("Period: " + (window.currentPreset === 'tournament' ? 'Official Contest (Sep 14+)' : (window.currentPreset === '7days' ? 'Last 7 Days' : 'All-Time')));
      lines.push("Total Squads: " + currentTeamCount);
      lines.push("====================================================");
      lines.push("");

      for (let i = 0; i < currentTeamCount; i++) {
        const meta = SQUAD_METAS[i % SQUAD_METAS.length];
        const teamData = calculateTeamSynergies(activeRosters[i] || [], statsMap);
        lines.push(meta.icon + " " + meta.name.toUpperCase());
        lines.push("Total Score: " + teamData.adjustedPoints.toLocaleString() + " pts (Base: " + teamData.basePoints.toLocaleString() + " pts + " + teamData.totalBuffPct + "% Synergy Buff)");
        lines.push("Distance: " + teamData.totalDist + " km | Hours: " + teamData.totalHours + " hrs | Squad Size: " + teamData.totalMemberCount + " (" + teamData.activeMembers.length + " active)");
        if (teamData.activeBuffs.length > 0) {
          lines.push("Active Buffs: " + teamData.activeBuffs.map(b => b.name + " (+" + b.pct + "%)").join(" | "));
        }
        lines.push("Active Scorers:");
        teamData.activeMembers.forEach(m => {
          lines.push(" • " + m.athlete_name + " (" + m.hero_class + ") — " + Math.round(m.total_points).toLocaleString() + " pts (" + (Math.round(m.total_distance * 10) / 10).toFixed(1) + " km)");
        });
        if (teamData.reserveMembers.length > 0) {
          lines.push("Registered Candidates (" + teamData.reserveMembers.length + "): " + teamData.reserveMembers.map(r => r.athlete_name).join(", "));
        }
        lines.push("");
      }
      lines.push("View & Simulate in The Arena: https://lupilgaming.github.io/Strava2026/arena.html");

      const fullText = lines.join(String.fromCharCode(10));
      navigator.clipboard.writeText(fullText).then(() => {
        showToast("✅ Squad roster copied to clipboard!");
      }).catch(() => {
        alert("Roster generated! Please copy from console or share card.");
      });
    }

    /* =========================================================================
       2. WORKOUT ROULETTE
       ========================================================================= */
    let lastDareIdx = 0;
    function spinRoulette() {
      let nextIdx;
      do {
        nextIdx = Math.floor(Math.random() * DARES.length);
      } while (nextIdx === lastDareIdx && DARES.length > 1);
      lastDareIdx = nextIdx;

      const dare = DARES[nextIdx];
      const display = document.getElementById('rouletteDisplay');
      display.style.opacity = '0.3';
      display.style.transform = 'scale(0.96)';

      setTimeout(() => {
        document.getElementById('dareIcon').innerText = dare.icon;
        document.getElementById('dareTitle').innerText = dare.title;
        document.getElementById('dareDesc').innerText = dare.desc;
        document.getElementById('darePts').innerText = `Est. Reward: ${dare.pts}`;

        display.style.opacity = '1';
        display.style.transform = 'scale(1)';
      }, 200);
    }

    /* =========================================================================
       3. MOMENTUM TRACKER
       ========================================================================= */
    function renderMomentum() {
      const statsMap = computeAthleteStats(getFilteredActivities());
      const athletes = Object.values(statsMap).sort((a, b) => b.total_activities - a.total_activities || b.total_points - a.total_points);

      const listEl = document.getElementById('momentumList');
      if (!listEl) return;

      const top6 = athletes.slice(0, 6);
      listEl.innerHTML = top6.map((a, idx) => `
        <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 14px; background:rgba(15,23,42,0.6); border-radius:10px; font-size:13px; border:1px solid var(--card-border);">
          <div style="display:flex; align-items:center; gap:10px;">
            <span style="font-weight:800; color:var(--text-dim); font-size:12px;">#${idx+1}</span>
            <span style="font-weight:700; color:#fff;">${a.athlete_name}</span>
            <span style="font-size:11px; color:${a.hero_class_color}; font-weight:700;">${a.hero_class}</span>
          </div>
          <span style="font-size:12px; font-weight:800; color:var(--gold);">🔥 ${a.total_activities} sessions</span>
        </div>
      `).join('');
    }

    /* =========================================================================
       4. VIRTUAL ROAD TRIP
       ========================================================================= */
    function renderVirtualJourney() {
      const activities = getFilteredActivities();
      const totalKm = activities.reduce((sum, a) => sum + parseFloat(a.distance_km || 0), 0);

      document.getElementById('journeyKmDisplay').innerText = `${totalKm.toFixed(1)} km`;

      const maxKm = MILESTONES[MILESTONES.length - 1].km;
      const progressPct = Math.min(100, Math.max(0, (totalKm / maxKm) * 100));
      document.getElementById('progressFill').style.width = `${progressPct.toFixed(1)}%`;

      let nextMilestone = MILESTONES.find(m => m.km > totalKm);
      if (!nextMilestone) nextMilestone = MILESTONES[MILESTONES.length - 1];

      const kmLeft = Math.max(0, nextMilestone.km - totalKm);
      document.getElementById('nextCityTarget').innerText = `${nextMilestone.city} (${kmLeft.toFixed(1)} km to go)`;

      const container = document.getElementById('milestonesContainer');
      container.innerHTML = MILESTONES.map(m => {
        const isUnlocked = totalKm >= m.km;
        const isTarget = m === nextMilestone && !isUnlocked;
        let statusClass = isUnlocked ? 'unlocked' : (isTarget ? 'active-target' : 'locked');
        let badgeText = isUnlocked ? 'Conquered' : (isTarget ? 'Current Goal' : 'Locked');

        return `
          <div class="milestone-card ${statusClass}">
            <div class="milestone-badge">${badgeText}</div>
            <div style="font-size:24px; margin-bottom:4px;">${m.icon}</div>
            <div style="font-weight:800; font-size:13px; color:#fff;">${m.city}</div>
            <div style="font-size:11px; color:var(--text-muted);">${m.km} km</div>
          </div>
        `;
      }).join('');
    }

    /* =========================================================================
       5. 1v1 DUEL ARENA
       ========================================================================= */
    function initDuelSelectors(preserveSelection = true) {
      const redSel = document.getElementById('fighterRed');
      const blueSel = document.getElementById('fighterBlue');
      if (!redSel || !blueSel) return;

      const currentRed = preserveSelection ? redSel.value : '';
      const currentBlue = preserveSelection ? blueSel.value : '';

      const filteredActivities = getFilteredActivities();
      const statsMap = computeAthleteStats(filteredActivities);
      const athletes = Object.values(statsMap).sort((a, b) => b.total_points - a.total_points || a.athlete_name.localeCompare(b.athlete_name));

      redSel.innerHTML = athletes.map((a, i) => {
        const isSelected = currentRed ? a.athlete_name === currentRed : i === 0;
        return `<option value="${a.athlete_name}" ${isSelected ? 'selected' : ''}>${a.athlete_name} (${Math.round(a.total_points).toLocaleString()} pts)</option>`;
      }).join('');

      blueSel.innerHTML = athletes.map((a, i) => {
        const isSelected = currentBlue ? a.athlete_name === currentBlue : i === 1;
        return `<option value="${a.athlete_name}" ${isSelected ? 'selected' : ''}>${a.athlete_name} (${Math.round(a.total_points).toLocaleString()} pts)</option>`;
      }).join('');

      if (currentRed && athletes.some(a => a.athlete_name === currentRed)) {
        redSel.value = currentRed;
      } else if (athletes.length > 0) {
        redSel.value = athletes[0].athlete_name;
      }

      if (currentBlue && athletes.some(a => a.athlete_name === currentBlue)) {
        blueSel.value = currentBlue;
      } else if (athletes.length > 1) {
        blueSel.value = athletes[1].athlete_name;
      } else if (athletes.length > 0) {
        blueSel.value = athletes[0].athlete_name;
      }
    }

    function updateDuel() {
      const redSel = document.getElementById('fighterRed');
      const blueSel = document.getElementById('fighterBlue');
      if (!redSel || !blueSel) return;

      const nameRed = redSel.value;
      const nameBlue = blueSel.value;

      const statsMap = computeAthleteStats(getFilteredActivities());
      const aRed = statsMap[nameRed] || { athlete_name: nameRed, total_distance: 0, total_activities: 0, total_duration_hours: 0, total_points: 0, fastest_pace_val: 999, fastest_pace_str: 'N/A' };
      const aBlue = statsMap[nameBlue] || { athlete_name: nameBlue, total_distance: 0, total_activities: 0, total_duration_hours: 0, total_points: 0, fastest_pace_val: 999, fastest_pace_str: 'N/A' };

      const redScoreEl = document.getElementById('fighterRedScore');
      if (redScoreEl) {
        redScoreEl.textContent = `${Math.round(aRed.total_points).toLocaleString()} pts`;
      }
      const blueScoreEl = document.getElementById('fighterBlueScore');
      if (blueScoreEl) {
        blueScoreEl.textContent = `${Math.round(aBlue.total_points).toLocaleString()} pts`;
      }

      const stats = [
        { label: "Total Points", val1: Math.round(aRed.total_points).toLocaleString(), val2: Math.round(aBlue.total_points).toLocaleString(), raw1: aRed.total_points, raw2: aBlue.total_points },
        { label: "Distance", val1: `${(Math.round(aRed.total_distance * 10) / 10).toFixed(1)} km`, val2: `${(Math.round(aBlue.total_distance * 10) / 10).toFixed(1)} km`, raw1: aRed.total_distance, raw2: aBlue.total_distance },
        { label: "Activities", val1: `${aRed.total_activities} logs`, val2: `${aBlue.total_activities} logs`, raw1: aRed.total_activities, raw2: aBlue.total_activities },
        { label: "Time on Trail", val1: `${(Math.round(aRed.total_duration_hours * 10) / 10).toFixed(1)} hrs`, val2: `${(Math.round(aBlue.total_duration_hours * 10) / 10).toFixed(1)} hrs`, raw1: aRed.total_duration_hours, raw2: aBlue.total_duration_hours },
        { label: "Hero Class", val1: `${aRed.hero_class_icon || '🛡️'} ${aRed.hero_class_name || 'Sentinel'}`, val2: `${aBlue.hero_class_icon || '🛡️'} ${aBlue.hero_class_name || 'Sentinel'}`, raw1: 0, raw2: 0, isText: true }
      ];

      const rowsEl = document.getElementById('duelStatsRows');
      rowsEl.innerHTML = stats.map(s => {
        let highlightLeft = !s.isText && s.raw1 > s.raw2 ? 'text-decoration: underline;' : '';
        let highlightRight = !s.isText && s.raw2 > s.raw1 ? 'text-decoration: underline;' : '';
        return `
          <div class="duel-stat-row">
            <span class="duel-val-left" style="${highlightLeft}">${s.val1}</span>
            <span class="duel-stat-label">${s.label}</span>
            <span class="duel-val-right" style="${highlightRight}">${s.val2}</span>
          </div>
        `;
      }).join('');

      let verdict = "";
      if (aRed.total_points > aBlue.total_points * 1.1) {
        verdict = `🏆 Tale of the Tape: <strong>${aRed.athlete_name}</strong> holds a commanding points lead (+${Math.round(aRed.total_points - aBlue.total_points)} pts)!`;
      } else if (aBlue.total_points > aRed.total_points * 1.1) {
        verdict = `🏆 Tale of the Tape: <strong>${aBlue.athlete_name}</strong> holds a commanding points lead (+${Math.round(aBlue.total_points - aRed.total_points)} pts)!`;
      } else {
        verdict = `⚖️ Dead Heat! Both athletes are closely matched within striking distance!`;
      }
      document.getElementById('duelVerdict').innerHTML = verdict;

      const maxPts = Math.max(aRed.total_points, aBlue.total_points, 100);
      const maxDist = Math.max(aRed.total_distance, aBlue.total_distance, 10);
      const maxActs = Math.max(aRed.total_activities, aBlue.total_activities, 5);
      const maxTime = Math.max(aRed.total_duration_hours, aBlue.total_duration_hours, 2);

      const norm = (val, max) => Math.min(100, Math.round((val / (max || 1)) * 100));

      const radarData = {
        labels: ['Total Points', 'Total Distance', 'Session Volume', 'Endurance Time', 'Consistency'],
        datasets: [
          {
            label: aRed.athlete_name,
            data: [
              norm(aRed.total_points, maxPts),
              norm(aRed.total_distance, maxDist),
              norm(aRed.total_activities, maxActs),
              norm(aRed.total_duration_hours, maxTime),
              norm(aRed.active_dates ? aRed.active_dates.size : 1, 10)
            ],
            fill: true,
            backgroundColor: 'rgba(239, 68, 68, 0.25)',
            borderColor: '#ef4444',
            pointBackgroundColor: '#ef4444'
          },
          {
            label: aBlue.athlete_name,
            data: [
              norm(aBlue.total_points, maxPts),
              norm(aBlue.total_distance, maxDist),
              norm(aBlue.total_activities, maxActs),
              norm(aBlue.total_duration_hours, maxTime),
              norm(aBlue.active_dates ? aBlue.active_dates.size : 1, 10)
            ],
            fill: true,
            backgroundColor: 'rgba(59, 130, 246, 0.25)',
            borderColor: '#3b82f6',
            pointBackgroundColor: '#3b82f6'
          }
        ]
      };

      const ctx = document.getElementById('duelRadarChart').getContext('2d');
      if (duelRadarChartInstance) {
        duelRadarChartInstance.data = radarData;
        duelRadarChartInstance.update();
      } else {
        duelRadarChartInstance = new Chart(ctx, {
          type: 'radar',
          data: radarData,
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              r: {
                angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                grid: { color: 'rgba(255, 255, 255, 0.08)' },
                pointLabels: { color: '#94a3b8', font: { size: 10, weight: '700' } },
                ticks: { display: false, max: 100, min: 0 }
              }
            },
            plugins: {
              legend: {
                labels: { color: '#f8fafc', font: { weight: '700', size: 12 } }
              }
            }
          }
        });
      }
    }

    /* =========================================================================
       6. THE TROPHY ROOM
       ========================================================================= */
    function renderTrophies() {
      const activities = getFilteredActivities();
      const statsMap = computeAthleteStats(activities);
      const athletes = Object.values(statsMap);

      const nightOwls = {};
      const earlyBirds = {};
      let fastestPace = { athlete: 'N/A', paceStr: 'N/A', paceVal: 999, dist: 0 };
      let longestSingle = { athlete: 'N/A', dist: 0 };

      athletes.forEach(a => {
        nightOwls[a.athlete_name] = a.night_owl_count;
        earlyBirds[a.athlete_name] = a.dawn_patrol_count;
        if (a.fastest_pace_val < fastestPace.paceVal && a.fastest_pace_val > 2.5) {
          fastestPace = { athlete: a.athlete_name, paceStr: a.fastest_pace_str, paceVal: a.fastest_pace_val, dist: a.max_single_dist };
        }
        if (a.max_single_dist > longestSingle.dist) {
          longestSingle = { athlete: a.athlete_name, dist: a.max_single_dist };
        }
      });

      const topNightOwl = Object.entries(nightOwls).sort((a, b) => b[1] - a[1])[0] || ['N/A', 0];
      const topEarlyBird = Object.entries(earlyBirds).sort((a, b) => b[1] - a[1])[0] || ['N/A', 0];
      const topPoints = athletes.sort((a, b) => b.total_points - a.total_points)[0] || { athlete_name: 'N/A', total_points: 0 };

      const trophies = [
        { icon: "⚡", title: "Speed Demon", criteria: "Fastest sustained pace recorded on an outdoor run (>= 2.5 km)", holder: fastestPace.athlete, stat: fastestPace.paceStr !== 'N/A' ? `${fastestPace.paceStr} pace` : 'Awaiting runs' },
        { icon: "🦉", title: "The Night Owl", criteria: "Most workouts logged in the evening after 8:00 PM", holder: topNightOwl[0], stat: `${topNightOwl[1]} night logs` },
        { icon: "🌅", title: "Dawn Patrol", criteria: "Most workouts logged in the early morning before 7:00 AM", holder: topEarlyBird[0], stat: `${topEarlyBird[1]} sunrise logs` },
        { icon: "🫁", title: "Iron Lungs", criteria: "Single longest continuous distance logged in an activity", holder: longestSingle.athlete, stat: `${(Math.round(longestSingle.dist * 10) / 10).toFixed(1)} km single effort` },
        { icon: "🎯", title: "Points Titan", criteria: "Overall leader in Dynamic MET points in active window", holder: topPoints.athlete_name, stat: `${Math.round(topPoints.total_points).toLocaleString()} pts` },
        { icon: "🏅", title: "Half-Marathoner", criteria: "Awarded to any athlete who has crossed the 21.1 km barrier", holder: longestSingle.dist >= 21.1 ? longestSingle.athlete : "Open Contender", stat: longestSingle.dist >= 21.1 ? `${longestSingle.dist} km logged` : "Target: 21.1 km" }
      ];

      const container = document.getElementById('trophiesContainer');
      if (container) {
        container.innerHTML = trophies.map(t => `
          <div class="trophy-card">
            <div class="trophy-icon-box">${t.icon}</div>
            <div class="trophy-title">${t.title}</div>
            <div class="trophy-desc">${t.criteria}</div>
            <div class="trophy-holder-box">
              <span class="trophy-holder-name">${t.holder}</span>
              <span class="trophy-stat-pill">${t.stat}</span>
            </div>
          </div>
        `).join('');
      }
    }

    /* =========================================================================
       6. META ANALYSIS & STRATEGY LAB LOGIC
       ========================================================================= */
    function calcFootPoints(dist, paceMin) {
      const d = Math.max(0, parseFloat(dist || 0));
      if (d <= 0) return 0;
      const p = Math.max(3.0, Math.min(20.0, parseFloat(paceMin || 6.5)));
      const v = 60.0 / p;
      const rawRate = 15.0 + 7.2 * v;
      const neutralRate = 80.0;
      const w = 1.0 / (1.0 + (d / 16.0));
      const rate = neutralRate + w * (rawRate - neutralRate);
      return Math.round(d * rate * 100) / 100;
    }

    function calcCyclingPoints(dist) {
      const d = Math.max(0, parseFloat(dist || 0));
      if (d <= 0) return 0;
      const rate = 12.0 + 9.5 * (d / (18.0 + d));
      return Math.round(d * rate * 100) / 100;
    }

    function getSlowMetMult(dayCount) {
      const c = parseInt(dayCount || 1, 10);
      if (c <= 1) return 1.00;
      if (c === 2) return 1.10;
      if (c === 3) return 1.20;
      return 1.30;
    }

    const DAILY_ROULETTE_QUESTS = [
      {
        dayIdx: 0, dayName: "Sunday", sport: "Gym / Workout", icon: "🧘",
        title: "Active Recovery & Mobility Sunday",
        desc: "Log at least 30 minutes of functional workout, gym session, yoga, or mobility training.",
        criteria: "Gym / Workout >= 30 min", bonusPct: 15,
        matchFn: (act) => /workout|weight|gym|yoga|pilates/i.test(act.activity_type) && parseFloat(act.duration_minutes || 0) >= 30.0
      },
      {
        dayIdx: 1, dayName: "Monday", sport: "Run", icon: "🏃‍♂️",
        title: "Speedway Monday Tempo Run",
        desc: "Log a continuous outdoor or treadmill run of at least 4.0 km.",
        criteria: "Run >= 4.0 km", bonusPct: 15,
        matchFn: (act) => /run|trail/i.test(act.activity_type) && parseFloat(act.distance_km || 0) >= 4.0
      },
      {
        dayIdx: 2, dayName: "Tuesday", sport: "Weight Training", icon: "🏋️",
        title: "Iron Forge Tuesday Strength",
        desc: "Log at least 35 minutes of gym weight training or resistance work.",
        criteria: "Gym / Weights >= 35 min", bonusPct: 15,
        matchFn: (act) => /weight|gym|strength|crossfit|workout/i.test(act.activity_type) && parseFloat(act.duration_minutes || 0) >= 35.0
      },
      {
        dayIdx: 3, dayName: "Wednesday", sport: "Ride", icon: "🚴‍♂️",
        title: "Midweek Velocity Cruise",
        desc: "Log an outdoor road or virtual cycle ride of at least 15.0 km.",
        criteria: "Cycling >= 15.0 km", bonusPct: 15,
        matchFn: (act) => /ride|cycle/i.test(act.activity_type) && parseFloat(act.distance_km || 0) >= 15.0
      },
      {
        dayIdx: 4, dayName: "Thursday", sport: "Walk", icon: "🚶‍♂️",
        title: "Restorative Stride Thursday",
        desc: "Log a brisk walking session of at least 4.0 km to lower cortisol and flush lactate.",
        criteria: "Walk >= 4.0 km", bonusPct: 20,
        matchFn: (act) => /walk|hike/i.test(act.activity_type) && parseFloat(act.distance_km || 0) >= 4.0
      },
      {
        dayIdx: 5, dayName: "Friday", sport: "Swim / Gym", icon: "🏊‍♂️",
        title: "Aqua Flow & Strength Friday",
        desc: "Log a swim of at least 800m or a 30+ min gym, weight training, or calisthenics session.",
        criteria: "Swim >= 800m or Gym/Weights >= 30 min", bonusPct: 15,
        matchFn: (act) => (/swim/i.test(act.activity_type) && parseFloat(act.distance_km || 0) >= 0.8) || (/workout|weight|gym|crossfit/i.test(act.activity_type) && parseFloat(act.duration_minutes || 0) >= 30.0)
      },
      {
        dayIdx: 6, dayName: "Saturday", sport: "Endurance", icon: "⛰️",
        title: "Endurance Odyssey Saturday",
        desc: "Log a weekend endurance effort: either a Run >= 8.0 km or a Ride >= 25.0 km.",
        criteria: "Run >= 8.0 km OR Ride >= 25.0 km", bonusPct: 20,
        matchFn: (act) => (/run/i.test(act.activity_type) && parseFloat(act.distance_km || 0) >= 8.0) || (/ride|cycle/i.test(act.activity_type) && parseFloat(act.distance_km || 0) >= 25.0)
      }
    ];

    function renderWorkoutRoulette() {
      const today = new Date();
      const dayOfWeek = today.getDay();
      const quest = DAILY_ROULETTE_QUESTS[dayOfWeek];

      const dateStr = today.toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' });
      const dateEl = document.getElementById('bountyDateDisplay');
      if (dateEl) dateEl.innerText = dateStr;

      const titleEl = document.getElementById('bountyTitle');
      if (titleEl) titleEl.innerText = quest.title;

      const iconEl = document.getElementById('bountyIcon');
      if (iconEl) iconEl.innerText = quest.icon;

      const tagEl = document.getElementById('bountyMultiplierTag');
      if (tagEl) tagEl.innerText = `⚡ +${quest.bonusPct}% Bonus Multiplier Active`;

      const descEl = document.getElementById('bountyDesc');
      if (descEl) descEl.innerText = `${quest.desc} Earns a special +${quest.bonusPct}% multiplier boost on your points!`;

      const activities = getFilteredActivities();
      const todayIsoStr = today.toISOString().slice(0, 10);
      let dayActs = activities.filter(a => (a.datetime_iso || a.datetime_utc || '').slice(0, 10) === todayIsoStr);

      if (dayActs.length === 0 && activities.length > 0) {
        const sortedDates = Array.from(new Set(activities.map(a => (a.datetime_iso || a.datetime_utc || '').slice(0, 10)))).sort();
        const latestDate = sortedDates[sortedDates.length - 1];
        if (latestDate) {
          const lDateObj = new Date(latestDate);
          const lQuest = DAILY_ROULETTE_QUESTS[lDateObj.getDay()];
          dayActs = activities.filter(a => (a.datetime_iso || a.datetime_utc || '').slice(0, 10) === latestDate);
          if (dateEl) dateEl.innerText = `${lDateObj.toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' })} (Latest Contest Day)`;
          if (titleEl) titleEl.innerText = lQuest.title;
          if (iconEl) iconEl.innerText = lQuest.icon;
          if (descEl) descEl.innerText = `${lQuest.desc} Earns a special +${lQuest.bonusPct}% multiplier boost!`;
          if (tagEl) tagEl.innerText = `⚡ +${lQuest.bonusPct}% Bonus Multiplier Active`;
        }
      }

      const claimersListEl = document.getElementById('bountyClaimersList');
      const claimCountEl = document.getElementById('bountyClaimCount');
      if (!claimersListEl) return;

      const claimers = [];
      dayActs.forEach(act => {
        if (quest.matchFn(act)) {
          const pts = parseFloat(act.points_dynamic || act.points || 0);
          const bonusPts = Math.round(pts * (quest.bonusPct / 100.0) * 10) / 10;
          claimers.push({
            name: act.athlete_name,
            sport: act.activity_type,
            pts: pts,
            bonusPts: bonusPts,
            dist: act.distance_km,
            dur: act.duration_minutes
          });
        }
      });

      if (claimCountEl) claimCountEl.innerText = `${claimers.length} Claimed`;

      if (claimers.length > 0) {
        claimersListEl.innerHTML = claimers.map(c => `
          <div style="background:rgba(34,197,94,0.12); border:1px solid rgba(34,197,94,0.35); padding:6px 12px; border-radius:10px; display:inline-flex; align-items:center; gap:8px;">
            <span>🏅</span>
            <strong style="color:#fff;">${c.name}</strong>
            <span style="color:var(--text-muted); font-size:11px;">(${c.sport})</span>
            <span style="background:rgba(251,191,36,0.2); color:var(--gold); font-weight:800; padding:2px 6px; border-radius:6px; font-size:11px;">+${c.bonusPts} Bonus pts</span>
          </div>
        `).join('');
      } else {
        claimersListEl.innerHTML = `
          <div style="color:var(--text-dim); font-size:12px; padding:4px 0;">
            No athletes have logged this quest yet for this day. Be the first to claim today's +${quest.bonusPct}% bonus!
          </div>
        `;
      }
    }

    function update10kVs5kSimulator() {
      const slider = document.getElementById('metaPaceSlider');
      if (!slider) return;
      const paceVal = parseFloat(slider.value);
      const paceMins = Math.floor(paceVal);
      const paceSecs = Math.round((paceVal - paceMins) * 60);
      const paceStr = `${paceMins}:${paceSecs < 10 ? '0' : ''}${paceSecs} /km`;
      const speedKmh = (60.0 / paceVal).toFixed(1);

      const totalDist = parseFloat(document.getElementById('metaDistSlider')?.value || 10.0);
      const distSingle = totalDist;
      const distSplit = totalDist / 2.0;

      const distDisp = document.getElementById('distSliderDisplay');
      if (distDisp) distDisp.innerText = `${totalDist.toFixed(1)} km (1x ${distSingle.toFixed(1)}k vs 2x ${distSplit.toFixed(1)}k)`;

      const paceDisp = document.getElementById('paceSliderDisplay');
      if (paceDisp) paceDisp.innerText = `${paceStr} (${speedKmh} km/h)`;

      const hasAdvantage = document.getElementById('splitAdvantageToggle')?.checked ?? true;
      const paceSplitVal = hasAdvantage ? Math.max(3.5, paceVal - 0.333) : paceVal;
      const pSplitMins = Math.floor(paceSplitVal);
      const pSplitSecs = Math.round((paceSplitVal - pSplitMins) * 60);
      const paceSplitStr = `${pSplitMins}:${pSplitSecs < 10 ? '0' : ''}${pSplitSecs} /km`;

      const ptsSingle = calcFootPoints(distSingle, paceVal);
      const ptsSplitSingle = calcFootPoints(distSplit, paceSplitVal);
      const ptsDouble = Math.round((2 * ptsSplitSingle) * 100) / 100;
      const diff = Math.round((ptsDouble - ptsSingle) * 10) / 10;
      const ratio = (ptsDouble / (ptsSingle || 1)).toFixed(3);

      const durSingle = (distSingle * paceVal).toFixed(1);
      const durSplitSingle = (distSplit * paceSplitVal).toFixed(1);
      const durSplitTotal = (2 * durSplitSingle).toFixed(1);

      const p10kEl = document.getElementById('ptsDisplay10k');
      if (p10kEl) p10kEl.innerHTML = `${ptsSingle.toFixed(1)} <span style="font-size:16px; font-weight:600; color:var(--text-muted);">pts</span>`;

      const p2x5kEl = document.getElementById('ptsDisplay2x5k');
      if (p2x5kEl) p2x5kEl.innerHTML = `${ptsDouble.toFixed(1)} <span style="font-size:16px; font-weight:600; color:var(--text-muted);">pts</span>`;

      const card10kTitle = document.querySelector('#card10k span[style*="font-weight:800"]');
      if (card10kTitle) card10kTitle.innerText = `🏃‍♂️ Singular ${distSingle.toFixed(1)}K Run`;

      const card2x5kTitle = document.querySelector('#card2x5k span[style*="font-weight:800"]');
      if (card2x5kTitle) card2x5kTitle.innerText = `🏃‍♂️🏃‍♂️ Two ${distSplit.toFixed(1)}K Runs (Split "Doubles")`;

      const detail10k = document.getElementById('paceDetail10k');
      if (detail10k) detail10k.innerText = `Pace: ${paceStr} • Moving Duration: ${durSingle} min`;

      const detail2x5k = document.getElementById('paceDetail2x5k');
      if (detail2x5k) detail2x5k.innerText = `Each ${distSplit.toFixed(1)}K: ${paceSplitStr} (${durSplitSingle} min) • Total Moving: ${durSplitTotal} min`;

      const deltaBadge = document.getElementById('deltaBadge2x5k');
      if (deltaBadge) {
        if (diff > 0) {
          deltaBadge.style.background = 'rgba(34,197,94,0.18)';
          deltaBadge.style.color = '#22c55e';
          deltaBadge.style.borderColor = 'rgba(34,197,94,0.35)';
          deltaBadge.innerText = `+${diff.toFixed(1)} pts advantage (${ratio}x)`;
        } else if (diff < 0) {
          deltaBadge.style.background = 'rgba(239,68,68,0.18)';
          deltaBadge.style.color = '#ef4444';
          deltaBadge.style.borderColor = 'rgba(239,68,68,0.35)';
          deltaBadge.innerText = `${diff.toFixed(1)} pts deficit (${ratio}x)`;
        } else {
          deltaBadge.style.background = 'rgba(255,255,255,0.1)';
          deltaBadge.style.color = '#fff';
          deltaBadge.innerText = `Equal points (1.000x)`;
        }
      }

      const card10k = document.getElementById('card10k');
      const card2x5k = document.getElementById('card2x5k');
      if (card10k && card2x5k) {
        if (diff > 0) {
          card2x5k.classList.add('winner');
          card10k.classList.remove('winner');
        } else {
          card10k.classList.add('winner');
          card2x5k.classList.remove('winner');
        }
      }

      const verdictBox = document.getElementById('duelVerdictBox');
      if (verdictBox) {
        if (diff >= 30) {
          verdictBox.innerHTML = `
            <strong>Coach's Tactical Verdict:</strong> 🏃‍♂️🏃‍♂️ <strong>Split Doubles Dominate on Points (+${diff.toFixed(1)} pts)</strong>.<br>
            At ${totalDist.toFixed(1)} km, splitting into two ${distSplit.toFixed(1)} km bouts preserves high-speed rewards under the distance dampening formula and allows a faster split pace. 
            However, doing two runs requires <strong>+40 min in operational prep & shower overhead</strong>. Choose the singular run when time is tight; choose split runs when maximizing points and biomechanical freshness.
          `;
        } else if (diff > 0) {
          verdictBox.innerHTML = `
            <strong>Coach's Tactical Verdict:</strong> ⚖️ <strong>Slight Mathematical Edge to Split Doubles (+${diff.toFixed(1)} pts)</strong>.<br>
            At this pace and distance, distance dampening yields nearly equivalent base points. The singular ${distSingle.toFixed(1)}K is practically superior due to saving 40+ minutes in gear changes, warmups, and showers.
          `;
        } else {
          verdictBox.innerHTML = `
            <strong>Coach's Tactical Verdict:</strong> 🏃‍♂️ <strong>Singular Push Wins for Slower/Recovery Paces</strong>.<br>
            At paces slower than 6:45/km, the distance dampening curve pulls the per-km rate UP towards the 80 pts/km neutral threshold on longer distances. Here, the singular ${distSingle.toFixed(1)}K awards equal or higher points with half the logistical friction!
          `;
        }
      }
    }

    function applyRoutinePreset(type) {
      document.querySelectorAll('.routine-preset-pill').forEach(b => b.classList.remove('active'));
      switchRoutineMode('freq');
      const runs = document.getElementById('sliderRuns');
      const gym = document.getElementById('sliderGym');
      const walks = document.getElementById('sliderWalks');
      const rides = document.getElementById('sliderRides');
      const swims = document.getElementById('sliderSwims');

      if (!runs || !gym || !walks || !rides || !swims) return;

      if (type === 'iron') {
        document.getElementById('presetBtnIron')?.classList.add('active');
        runs.value = 3; gym.value = 3; walks.value = 0; rides.value = 0; swims.value = 0;
      } else if (type === 'split') {
        document.getElementById('presetBtnSplit')?.classList.add('active');
        runs.value = 2; gym.value = 2; walks.value = 2; rides.value = 0; swims.value = 0;
      } else if (type === 'daily') {
        document.getElementById('presetBtnDaily')?.classList.add('active');
        runs.value = 7; gym.value = 0; walks.value = 0; rides.value = 0; swims.value = 0;
      } else if (type === 'apex') {
        document.getElementById('presetBtnApex')?.classList.add('active');
        runs.value = 1; gym.value = 1; walks.value = 1; rides.value = 1; swims.value = 0;
      } else if (type === 'walker') {
        document.getElementById('presetBtnWalker')?.classList.add('active');
        runs.value = 0; gym.value = 0; walks.value = 7; rides.value = 0; swims.value = 0;
      }
      updateRoutineArchitect();
    }

    window.routineMode = 'freq';

    function switchRoutineMode(mode) {
      window.routineMode = mode;
      document.getElementById('modeBtnFreq')?.classList.toggle('active', mode === 'freq');
      document.getElementById('modeBtnVolume')?.classList.toggle('active', mode === 'volume');

      const boxFreq = document.getElementById('routineBoxFreq');
      const boxVol = document.getElementById('routineBoxVolume');
      if (boxFreq && boxVol) {
        boxFreq.style.display = mode === 'freq' ? 'flex' : 'none';
        boxVol.style.display = mode === 'volume' ? 'flex' : 'none';
      }
      updateRoutineArchitect();
    }

    function updateRoutineArchitect() {
      const mode = window.routineMode || 'freq';
      let totalWeeklyPts = 0;
      let totalHours = 0;
      let ptsPerHour = 0;
      let stressScore = 0;
      let longevity = 80;

      if (mode === 'freq') {
        const numRuns = parseInt(document.getElementById('sliderRuns')?.value || 0, 10);
        const numGym = parseInt(document.getElementById('sliderGym')?.value || 0, 10);
        const numWalks = parseInt(document.getElementById('sliderWalks')?.value || 0, 10);
        const numRides = parseInt(document.getElementById('sliderRides')?.value || 0, 10);
        const numSwims = parseInt(document.getElementById('sliderSwims')?.value || 0, 10);

        const gymMult = getSlowMetMult(numGym);
        if (document.getElementById('sliderValRuns')) document.getElementById('sliderValRuns').innerText = `${numRuns} days`;
        if (document.getElementById('sliderValGym')) document.getElementById('sliderValGym').innerText = `${numGym} days (${gymMult.toFixed(2)}x Mult)`;
        if (document.getElementById('sliderValWalks')) document.getElementById('sliderValWalks').innerText = `${numWalks} days`;
        if (document.getElementById('sliderValRides')) document.getElementById('sliderValRides').innerText = `${numRides} days`;
        if (document.getElementById('sliderValSwims')) document.getElementById('sliderValSwims').innerText = `${numSwims} days`;

        const ptsPerRun = calcFootPoints(5.0, 5.5);
        const totalRunPts = numRuns * ptsPerRun;
        const ptsPerGym = (45.0 * 4.0) * gymMult;
        const totalGymPts = numGym * ptsPerGym;
        const ptsPerWalk = 5.0 * 35.0;
        const totalWalkPts = numWalks * ptsPerWalk;
        const ptsPerRide = calcCyclingPoints(20.0);
        const totalRidePts = numRides * ptsPerRide;
        const ptsPerSwim = 1.2 * 370.0;
        const totalSwimPts = numSwims * ptsPerSwim;

        totalWeeklyPts = Math.round(totalRunPts + totalGymPts + totalWalkPts + totalRidePts + totalSwimPts);

        const runHours = (numRuns * 27.5) / 60.0;
        const gymHours = (numGym * 45.0) / 60.0;
        const walkHours = (numWalks * 55.0) / 60.0;
        const rideHours = (numRides * 48.0) / 60.0;
        const swimHours = (numSwims * 30.0) / 60.0;
        totalHours = runHours + gymHours + walkHours + rideHours + swimHours;
        ptsPerHour = totalHours > 0 ? Math.round(totalWeeklyPts / totalHours) : 0;

        stressScore = Math.min(100, Math.round(numRuns * 14 + numRides * 4 + numGym * 5 + numSwims * 1 + numWalks * 1));
        const totalActiveSessions = numRuns + numGym + numWalks + numRides + numSwims;
        const estimatedRestDays = Math.max(0, 7 - Math.min(7, numRuns + (numGym > 0 ? 1 : 0) + (numWalks > 0 && numRuns === 0 ? 1 : 0)));

        longevity = 80;
        longevity += (numGym >= 2 ? 10 : (numGym === 1 ? 5 : -5));
        longevity += (numWalks >= 2 ? 10 : 0);
        longevity += (numSwims >= 1 ? 5 : 0);
        if (numRuns >= 6) longevity -= 25;
        if (numRuns >= 5 && numGym >= 5) longevity -= 25;
        if (totalActiveSessions > 10) longevity -= 15;
        if (numRuns <= 3 && numRuns >= 1) longevity += 5;
        longevity = Math.max(20, Math.min(99, longevity));

        const ptsEl = document.getElementById('routineTotalPts');
        if (ptsEl) ptsEl.innerHTML = `${totalWeeklyPts.toLocaleString()} <span style="font-size:16px; font-weight:600; color:var(--text-muted);">pts / week</span>`;

        const hrsEl = document.getElementById('routineTotalHours');
        if (hrsEl) hrsEl.innerText = `~${totalHours.toFixed(1)} hrs / wk`;

        const velEl = document.getElementById('routineVelocityDisplay');
        if (velEl) velEl.innerText = `Points Velocity: ${ptsPerHour} pts / active hour`;

        const coachEl = document.getElementById('routineCoachAdvice');
        if (coachEl) {
          if (numRuns >= 6 && numGym >= 4) {
            coachEl.innerHTML = `<strong>⚠️ Severe Overuse Warning:</strong> Running ${numRuns} days and lifting ${numGym} days creates concurrent training interference (AMPK/mTOR clash). Substitute 2-3 runs with active walks to prevent tendonitis.`;
          } else if (numRuns === 7) {
            coachEl.innerHTML = `<strong>⚠️ 7-Day Running Grinder:</strong> Generating ~${totalWeeklyPts} pts, but 35,000+ continuous ground shocks with zero rest days risks shin splints and plantar fasciitis within 3-4 weeks. Add 1 complete rest day.`;
          } else if (numRuns >= 2 && numGym >= 2 && (numWalks >= 1 || estimatedRestDays >= 1)) {
            coachEl.innerHTML = `<strong>🌟 Elite Equilibrium Routine:</strong> Excellent split! You harvest strong running points (${totalRunPts} pts) while the gym provides joint armor and hits the Slow-MET consistency bonus (${totalGymPts} pts). Highly sustainable.`;
          } else if (numWalks >= 5 && numRuns === 0) {
            coachEl.innerHTML = `<strong>🚶‍♂️ The Pure Restorative Route:</strong> Zero orthopedic danger and maximum cardiovascular health benefits, but requires ~${totalHours.toFixed(1)} hours of walking to earn ${totalWeeklyPts} points. Add 1-2 moderate runs or gym workouts to boost points velocity!`;
          } else {
            coachEl.innerHTML = `<strong>⚖️ Balanced Schedule:</strong> Generating ${totalWeeklyPts} pts across ~${totalHours.toFixed(1)} hours. Maintain hydration, sleep 8+ hours, and take at least 1 non-negotiable rest day every 7-10 days.`;
          }
        }
      } else {
        // Mode: 'volume' (Budget in Hours & KM)
        const budgetHrs = parseFloat(document.getElementById('sliderVolBudget')?.value || 6.0);
        const runKm = parseFloat(document.getElementById('sliderVolRun')?.value || 15.0);
        const gymHrs = parseFloat(document.getElementById('sliderVolGym')?.value || 2.5);
        const walkKm = parseFloat(document.getElementById('sliderVolWalk')?.value || 10.0);
        const rideKm = parseFloat(document.getElementById('sliderVolRide')?.value || 20.0);
        const swimKm = parseFloat(document.getElementById('sliderVolSwim')?.value || 1.0);

        const runHrs = (runKm * 5.5) / 60.0;
        const walkHrs = (walkKm * 11.0) / 60.0;
        const rideHrs = (rideKm * 2.4) / 60.0;
        const swimHrs = (swimKm * 25.0) / 60.0;
        totalHours = runHrs + gymHrs + walkHrs + rideHrs + swimHrs;

        if (document.getElementById('sliderValVolBudget')) document.getElementById('sliderValVolBudget').innerText = `${budgetHrs.toFixed(1)} hours / week`;
        if (document.getElementById('sliderValVolRun')) document.getElementById('sliderValVolRun').innerText = `${runKm.toFixed(1)} km (~${runHrs.toFixed(1)} hrs)`;
        if (document.getElementById('sliderValVolGym')) document.getElementById('sliderValVolGym').innerText = `${gymHrs.toFixed(1)} hours`;
        if (document.getElementById('sliderValVolWalk')) document.getElementById('sliderValVolWalk').innerText = `${walkKm.toFixed(1)} km (~${walkHrs.toFixed(1)} hrs)`;
        if (document.getElementById('sliderValVolRide')) document.getElementById('sliderValVolRide').innerText = `${rideKm.toFixed(1)} km (~${rideHrs.toFixed(1)} hrs)`;
        if (document.getElementById('sliderValVolSwim')) document.getElementById('sliderValVolSwim').innerText = `${swimKm.toFixed(1)} km (~${swimHrs.toFixed(1)} hrs)`;

        const gymDaysEst = Math.max(1, Math.round(gymHrs / 0.75));
        const gymMult = getSlowMetMult(gymDaysEst);

        const ptsRun = calcFootPoints(runKm, 5.5);
        const ptsGym = (gymHrs * 60.0 * 4.0) * gymMult;
        const ptsWalk = walkKm * 35.0;
        const ptsRide = calcCyclingPoints(rideKm);
        const ptsSwim = swimKm * 380.0;

        totalWeeklyPts = Math.round(ptsRun + ptsGym + ptsWalk + ptsRide + ptsSwim);
        ptsPerHour = totalHours > 0 ? Math.round(totalWeeklyPts / totalHours) : 0;

        stressScore = Math.min(100, Math.round((runKm * 2.2) + (rideKm * 0.4) + (gymHrs * 6.0) + (swimKm * 2.0) + (walkKm * 0.3)));

        longevity = 80;
        if (gymHrs >= 2.0) longevity += 12;
        if (walkKm >= 8.0) longevity += 10;
        if (swimKm >= 1.0) longevity += 8;
        if (runKm >= 40.0) longevity -= 25;
        if (totalHours > budgetHrs * 1.2) longevity -= 15;
        longevity = Math.max(20, Math.min(99, longevity));

        const ptsEl = document.getElementById('routineTotalPts');
        if (ptsEl) ptsEl.innerHTML = `${totalWeeklyPts.toLocaleString()} <span style="font-size:16px; font-weight:600; color:var(--text-muted);">pts / week</span>`;

        const hrsEl = document.getElementById('routineTotalHours');
        const budgetDelta = totalHours - budgetHrs;
        if (hrsEl) {
          if (budgetDelta > 0.5) {
            hrsEl.innerHTML = `<span style="color:#ef4444;">${totalHours.toFixed(1)} hrs</span> / ${budgetHrs.toFixed(1)}h budget (+${budgetDelta.toFixed(1)}h over)`;
          } else {
            hrsEl.innerHTML = `<span style="color:#22c55e;">${totalHours.toFixed(1)} hrs</span> / ${budgetHrs.toFixed(1)}h budget`;
          }
        }

        const velEl = document.getElementById('routineVelocityDisplay');
        if (velEl) velEl.innerText = `Points Velocity: ${ptsPerHour} pts / active hour (Budgeted: ${budgetHrs.toFixed(1)} hrs)`;

        const coachEl = document.getElementById('routineCoachAdvice');
        if (coachEl) {
          if (totalHours > budgetHrs) {
            coachEl.innerHTML = `<strong>⚠️ Time Budget Exceeded:</strong> You planned ${totalHours.toFixed(1)} active hours against a ${budgetHrs.toFixed(1)}h budget. Running (${runKm.toFixed(1)}km = ${runHrs.toFixed(1)}h) and Walking (${walkKm.toFixed(1)}km = ${walkHrs.toFixed(1)}h) consume the most time. Reduce walking distance or pick higher-velocity running/swimming to stay within budget!`;
          } else if (runKm >= 35.0 && gymHrs >= 4.0) {
            coachEl.innerHTML = `<strong>⚠️ Heavy Orthopedic Volume:</strong> ${runKm.toFixed(1)} km of running plus ${gymHrs.toFixed(1)} hrs of gym demands strict recovery. Ensure at least 2 non-running days per week to avoid patellar tendon overload.`;
          } else {
            coachEl.innerHTML = `<strong>🎯 Clean Volume Balance:</strong> Consuming ${totalHours.toFixed(1)} hours of your ${budgetHrs.toFixed(1)}h weekly budget, delivering ~${totalWeeklyPts.toLocaleString()} points (${ptsPerHour} pts/hr). Great time management!`;
          }
        }
      }

      const impactLabel = document.getElementById('routineImpactLabel');
      const impactFill = document.getElementById('routineImpactFill');
      if (impactFill && impactLabel) {
        impactFill.style.width = `${stressScore}%`;
        if (stressScore > 75) {
          impactLabel.innerText = `⚠️ Extreme Overuse (${stressScore}/100)`;
          impactLabel.style.color = '#ef4444';
          impactFill.style.background = '#ef4444';
        } else if (stressScore > 50) {
          impactLabel.innerText = `🟡 Elevated Strain (${stressScore}/100)`;
          impactLabel.style.color = '#f59e0b';
          impactFill.style.background = '#f59e0b';
        } else if (stressScore > 25) {
          impactLabel.innerText = `🟢 Optimal Load (${stressScore}/100)`;
          impactLabel.style.color = '#22c55e';
          impactFill.style.background = '#22c55e';
        } else {
          impactLabel.innerText = `⚪ Light Recovery (${stressScore}/100)`;
          impactLabel.style.color = '#38bdf8';
          impactFill.style.background = '#38bdf8';
        }
      }

      const longLabel = document.getElementById('routineLongevityLabel');
      const longFill = document.getElementById('routineLongevityFill');
      if (longFill && longLabel) {
        longFill.style.width = `${longevity}%`;
        longLabel.innerText = `${longevity} / 100`;
        if (longevity >= 85) {
          longLabel.style.color = '#22c55e';
          longFill.style.background = '#22c55e';
        } else if (longevity >= 65) {
          longLabel.style.color = '#f59e0b';
          longFill.style.background = '#f59e0b';
        } else {
          longLabel.style.color = '#ef4444';
          longFill.style.background = '#ef4444';
        }
      }
    }

    function renderLeaderMetas() {
      const acts = getFilteredActivities();
      const statsMap = computeAthleteStats(acts);
      const athletes = Object.values(statsMap).filter(a => a.total_points > 0).sort((a, b) => b.total_points - a.total_points);

      const tbody = document.getElementById('leaderMetasTbody');
      if (!tbody) return;

      if (athletes.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; color:var(--text-muted); padding:20px;">No active athlete data in this window.</td></tr>';
        return;
      }

      tbody.innerHTML = athletes.map((a, idx) => {
        const sports = a.sports || {};
        let topSport = 'Other';
        let maxSportCount = 0;
        Object.entries(sports).forEach(([sp, cnt]) => {
          if (cnt > maxSportCount) {
            maxSportCount = cnt;
            topSport = sp;
          }
        });

        let metaTitle = 'Balanced Polymath';
        let metaBadgeStyle = 'background:rgba(56,189,248,0.15); color:#38bdf8; border:1px solid rgba(56,189,248,0.3);';
        let longevScore = '8.5 / 10';
        let longevColor = '#22c55e';

        const singleDist = a.max_single_dist || 0;
        const singleDur = a.max_single_duration || 0;
        const pts = a.total_points;
        const actCount = a.total_activities;
        const durHrs = a.total_duration_hours || (a.total_duration_minutes ? a.total_duration_minutes / 60 : 1);
        const ptsPerHour = durHrs > 0 ? Math.round(pts / durHrs) : 0;

        if (singleDist >= 40.0 || (singleDist >= 15.0 && (sports['Swim'] || 0) > 0)) {
          metaTitle = '🔱 Apex Triathlete Titan';
          metaBadgeStyle = 'background:rgba(239,68,68,0.18); color:#f87171; border:1px solid rgba(239,68,68,0.35);';
          longevScore = '7.4 / 10';
          longevColor = '#f59e0b';
        } else if (singleDist >= 14.0 && topSport === 'Run') {
          metaTitle = '⚡ Heavy Singularity (Long Run)';
          metaBadgeStyle = 'background:rgba(252,76,2,0.18); color:var(--strava-orange); border:1px solid rgba(252,76,2,0.35);';
          longevScore = '6.8 / 10';
          longevColor = '#f59e0b';
        } else if ((sports['Weight Training'] || 0) + (sports['Workout'] || 0) >= 4 && (sports['Walk'] || 0) >= 3) {
          metaTitle = '⚖️ Interleaved Gym + Walk Master';
          metaBadgeStyle = 'background:rgba(16,185,129,0.18); color:#34d399; border:1px solid rgba(16,185,129,0.35);';
          longevScore = '9.6 / 10';
          longevColor = '#22c55e';
        } else if ((sports['Weight Training'] || 0) + (sports['Workout'] || 0) >= 3 && singleDur >= 75) {
          metaTitle = '🏋️ Heavy Gym & Calisthenics';
          metaBadgeStyle = 'background:rgba(168,85,247,0.18); color:#c084fc; border:1px solid rgba(168,85,247,0.35);';
          longevScore = '8.9 / 10';
          longevColor = '#22c55e';
        } else if (topSport === 'Walk' && actCount >= 6) {
          metaTitle = '🌿 High-Volume Walk Consistency';
          metaBadgeStyle = 'background:rgba(34,197,94,0.18); color:#22c55e; border:1px solid rgba(34,197,94,0.35);';
          longevScore = '9.9 / 10';
          longevColor = '#22c55e';
        } else if (actCount >= 5 && topSport === 'Run') {
          metaTitle = '🔥 Continuous Running Grinder';
          metaBadgeStyle = 'background:rgba(234,179,8,0.18); color:#fbbf24; border:1px solid rgba(234,179,8,0.35);';
          longevScore = '7.2 / 10';
          longevColor = '#f59e0b';
        } else if (actCount > 0 && (pts / actCount) >= 600) {
          metaTitle = '🏹 Apex Burst Specialist';
          metaBadgeStyle = 'background:rgba(236,72,153,0.18); color:#f472b6; border:1px solid rgba(236,72,153,0.35);';
          longevScore = '7.0 / 10';
          longevColor = '#f59e0b';
        }

        return `
          <tr>
            <td>
              <div style="display:flex; align-items:center; gap:8px;">
                <span style="color:var(--text-dim); font-size:12px; font-weight:800;">#${idx+1}</span>
                <strong style="color:#fff;">${a.athlete_name}</strong>
              </div>
            </td>
            <td>
              <span class="lead-meta-pill" style="${metaBadgeStyle}">${metaTitle}</span>
            </td>
            <td>
              <span style="font-weight:700; color:#cbd5e1;">${topSport} (${maxSportCount} acts)</span>
            </td>
            <td>
              <strong style="color:var(--gold);">${Math.round(pts).toLocaleString()} pts</strong>
            </td>
            <td>
              <span style="color:var(--text-muted); font-size:12.5px;">${singleDist > 0 ? singleDist.toFixed(1) + ' km' : (singleDur > 0 ? singleDur.toFixed(0) + ' min' : 'N/A')}</span>
            </td>
            <td>
              <span style="font-weight:700; color:#38bdf8;">${ptsPerHour} pts/hr</span>
            </td>
            <td>
              <strong style="color:${longevColor};">${longevScore}</strong>
            </td>
          </tr>
        `;
      }).join('');
    }

    function renderMetaLab() {
      update10kVs5kSimulator();
      updateRoutineArchitect();
      renderLeaderMetas();
    }

    /* Initialize Data Loading */
    async function loadArenaData() {
      initSquadDropdown();

      // Read precalculated squads
      try {
        const precalcEl = document.getElementById('precalculated-squads-data');
        if (precalcEl && precalcEl.textContent.trim()) {
          PRECALC_SQUADS = JSON.parse(precalcEl.textContent);
        }
      } catch (err) {
        console.error('Failed to parse precalculated squads:', err);
      }

      // Read fallback data
      try {
        const fallbackEl = document.getElementById('fallback-data');
        if (fallbackEl && fallbackEl.textContent.trim()) {
          globalData = JSON.parse(fallbackEl.textContent);
          initArena();
        }
      } catch (err) {
        console.error('Failed to parse embedded data:', err);
      }

      // Live fetch attempt
      try {
        const resp = await fetch('dashboard_data.json?t=' + Date.now(), { cache: 'no-store' });
        if (resp.ok) {
          globalData = await resp.json();
          initArena();
        }
      } catch (e) {}
    }

    function initArena() {
      if (!globalData) return;
      applyFilterAndRerender();
    }

    loadArenaData();
  </script>
</body>
</html>
"""

    full_arena_html = arena_template.replace("<!-- FALLBACK_DATA_PLACEHOLDER -->", json_str)
    full_arena_html = full_arena_html.replace("<!-- PRECALCULATED_SQUADS_PLACEHOLDER -->", precalc_json_str)
    full_arena_html = full_arena_html.replace("{num_members}", str(len(members)))

    destinations = [
        os.path.join(root_dir, "arena.html"),
        os.path.join(year_dir, "arena.html"),
        os.path.join(web_dir, "arena.html"),
        os.path.join(export_dir, "arena.html")
    ]

    for dest in destinations:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(full_arena_html)
        print(f"[+] Wrote arena.html -> {dest}")

if __name__ == "__main__":
    build_arena()
