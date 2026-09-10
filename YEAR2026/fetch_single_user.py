import os
import sys
import re
import csv
import json
import time
import datetime
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from points import convert_distance_to_km, convert_duration_to_minutes, calculate_activity_points, format_pace, is_indoor_ride

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9"
}

CSV_FIELDNAMES = [
    "activity_id", "athlete_id", "athlete_name", "activity_type",
    "datetime_utc", "distance_km", "duration_minutes", "points", "pace", "is_indoor", "activity_url"
]

LOG_FIELDNAMES = [
    "timestamp", "activity_id", "activity_url", "athlete_id", "athlete_name", "status", "error_message"
]

def load_config() -> dict:
    for cfg_path in ["config.json", "../config.json", os.path.join(os.path.dirname(__file__), "config.json")]:
        if os.path.exists(cfg_path):
            try:
                with open(cfg_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    return {}

def load_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    cfg = load_config()
    if cfg.get("http_headers"):
        session.headers.update(cfg["http_headers"])
    if cfg.get("session_cookies"):
        session.cookies.update(cfg["session_cookies"])

    strava_cookie = os.environ.get("STRAVA_SESSION")
    if strava_cookie:
        session.cookies.set("_strava4_session", strava_cookie)

    return session

def log_activity_status(log_file: str, act_id: str, act_url: str, aid: str, aname: str, status: str, error_msg: str = ""):
    file_exists = os.path.exists(log_file) and os.path.getsize(log_file) > 0
    with open(log_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.datetime.now().isoformat(),
            "activity_id": act_id,
            "activity_url": act_url,
            "athlete_id": aid,
            "athlete_name": aname,
            "status": status,
            "error_message": error_msg
        })
        f.flush()

def append_activity_to_csv(csv_file: str, act_dict: dict):
    file_exists = os.path.exists(csv_file) and os.path.getsize(csv_file) > 0
    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(act_dict)
        f.flush()

def resolve_athlete_name(athlete_id: str) -> str:
    for path in ["memberlist.csv", "../memberlist.csv", "db.csv", "../archive/db.csv"]:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for row in csv.DictReader(f):
                        if str(row.get("athlete_id", "")).strip() == str(athlete_id).strip():
                            return row.get("athlete_name", "").strip() or f"Athlete {athlete_id}"
            except Exception:
                pass
    return f"Athlete {athlete_id}"

def get_target_months(months_back: int = 2) -> list:
    today = datetime.date.today()
    months = []
    for i in range(months_back):
        y = today.year
        m = today.month - i
        while m <= 0:
            m += 12
            y -= 1
        months.append(f"{y}{m:02d}")
    return months

def discover_activity_ids(session: requests.Session, athlete_id: str, months_back: int = 2) -> list:
    cfg = load_config()
    session_cookie = cfg.get("session_cookies", {}).get("_strava4_session", "")
    target_months = get_target_months(months_back=months_back)

    chrome_path = r"C:\Users\ds-ga\Downloads\chrome-win64\chrome-win64\chrome.exe"
    driver_path = r"C:\Users\ds-ga\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

    options = Options()
    if os.path.exists(chrome_path):
        options.binary_location = chrome_path
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")

    service = webdriver.ChromeService(executable_path=driver_path) if os.path.exists(driver_path) else None
    driver = webdriver.Chrome(service=service, options=options) if service else webdriver.Chrome(options=options)

    activity_ids = []
    seen = set()

    try:
        driver.get("https://www.strava.com")
        if session_cookie:
            driver.add_cookie({"name": "_strava4_session", "value": session_cookie, "domain": ".strava.com", "path": "/"})

        # 1. Scrape monthly interval tables (#activity-log)
        for month in target_months:
            driver.get("about:blank")
            url = f"https://www.strava.com/athletes/{athlete_id}#interval_type?chart_type=miles&interval_type=month&interval={month}&year_offset=0&num_entries=1000"
            driver.get(url)
            time.sleep(3.5)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            log_sec = soup.find(id="activity-log")
            search_scope = log_sec if log_sec else soup

            for a in search_scope.find_all("a", href=re.compile(r"/activities/\d+")):
                m = re.search(r"/activities/(\d+)", a.get("href", ""))
                if m:
                    aid = m.group(1)
                    if aid not in seen:
                        seen.add(aid)
                        activity_ids.append(aid)

        # 2. Also check recent activities from athlete main profile feed
        driver.get(f"https://www.strava.com/athletes/{athlete_id}")
        time.sleep(2.5)
        soup_feed = BeautifulSoup(driver.page_source, "html.parser")
        feed_sec = soup_feed.find(class_=re.compile(r"feed|activity", re.I))
        search_feed = feed_sec if feed_sec else soup_feed
        for a in search_feed.find_all("a", href=re.compile(r"/activities/\d+")):
            m = re.search(r"/activities/(\d+)", a.get("href", ""))
            if m:
                aid = m.group(1)
                if aid not in seen:
                    seen.add(aid)
                    activity_ids.append(aid)

    except Exception as e:
        print(f"[!] Browser discovery notice: {e}")
    finally:
        driver.quit()

    # Fallback to requests if browser discovery yielded 0
    if not activity_ids:
        for yyyymm in target_months:
            url = f"https://www.strava.com/athletes/{athlete_id}/interval_type?chart_type=miles&interval_type=month&interval={yyyymm}&year_offset=0&num_entries=1000"
            try:
                r = session.get(url, timeout=12)
                if r.status_code == 200:
                    for act_id in re.findall(r"/activities/(\d+)", r.text):
                        if act_id not in seen:
                            seen.add(act_id)
                            activity_ids.append(act_id)
            except Exception:
                pass

    return activity_ids

def parse_activity_page(html: str, act_id: str, athlete_id: str, athlete_name: str, act_url: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    act_type = "Workout"
    datetime_utc = ""
    distance_km = 0.0
    duration_minutes = 0.0

    # 1. Sport type from title
    title = soup.find("title").text if soup.find("title") else ""
    if "|" in title:
        parts = [p.strip() for p in title.split("|")]
        if len(parts) >= 2 and parts[1] in ["Run", "Ride", "Walk", "Hike", "Swim", "Workout", "Weight Training", "Yoga"]:
            act_type = parts[1]

    # 2. Check __NEXT_DATA__
    script = soup.find("script", id="__NEXT_DATA__")
    if script and script.string:
        try:
            data = json.loads(script.string)
            activity = data.get("props", {}).get("pageProps", {}).get("activity", {})
            if activity:
                act_type = activity.get("activityKind", {}).get("sportType") or activity.get("type") or act_type
                datetime_utc = activity.get("startLocal") or activity.get("startDateLocal") or ""
                ath_info = activity.get("athlete", {})
                first = ath_info.get("firstName", "")
                last = ath_info.get("lastName", "")
                if first or last:
                    athlete_name = f"{first} {last}".strip()
                if "distance" in activity and activity["distance"] is not None:
                    distance_km = round(float(activity["distance"]) / 1000.0, 2)
                if "movingTime" in activity and activity["movingTime"] is not None:
                    duration_minutes = round(float(activity["movingTime"]) / 60.0, 2)
        except Exception:
            pass

    # 3. Rails inline-stats & activity-stats list items
    if distance_km == 0.0 or duration_minutes == 0.0:
        for li in soup.select(".inline-stats li, .activity-stats li"):
            txt = " ".join(li.text.split())
            txt_l = txt.lower()
            if "dist" in txt_l and distance_km == 0.0:
                val = re.sub(r"dist\w*", "", txt, flags=re.I).strip()
                distance_km = convert_distance_to_km(val)
            elif ("moving time" in txt_l or "time" in txt_l or "duration" in txt_l) and duration_minutes == 0.0:
                val = re.sub(r"(moving\s+)?(time|duration)", "", txt, flags=re.I).strip()
                duration_minutes = convert_duration_to_minutes(val)

    # 4. Fallback timestamp
    if not datetime_utc:
        time_tag = soup.find("time")
        if time_tag:
            datetime_utc = time_tag.text.strip() or time_tag.get("datetime") or ""

    # Standardize activity type name
    type_lower = act_type.lower()
    if "walk" in type_lower: act_type = "Walk"
    elif "trail" in type_lower: act_type = "Trail Run"
    elif "run" in type_lower: act_type = "Run"
    elif "ride" in type_lower or "cycle" in type_lower: act_type = "Ride"
    elif "weight" in type_lower or "gym" in type_lower: act_type = "Weight Training"
    elif "yoga" in type_lower: act_type = "Yoga"
    elif "hike" in type_lower: act_type = "Hike"
    elif "swim" in type_lower: act_type = "Swim"

    indoor_flag = is_indoor_ride(act_type, distance_km)

    pace_str = ""
    if type_lower in ["run", "trail run", "walk", "hike"]:
        pace_str = format_pace(distance_km, duration_minutes)

    points = calculate_activity_points(act_type, distance_km, duration_minutes, is_indoor=indoor_flag)

    return {
        "activity_id": act_id,
        "athlete_id": athlete_id,
        "athlete_name": athlete_name,
        "activity_type": act_type,
        "datetime_utc": datetime_utc,
        "distance_km": distance_km,
        "duration_minutes": duration_minutes,
        "points": points,
        "pace": pace_str,
        "is_indoor": "true" if indoor_flag else "false",
        "activity_url": act_url
    }


def fetch_single_user(athlete_id: str, months_back: int = 2, activities_csv: str = "activities.csv", log_csv: str = "activity_log.csv"):
    m = re.search(r"/athletes/(\d+)", str(athlete_id))
    if m:
        athlete_id = m.group(1)

    session = load_session()
    athlete_name = resolve_athlete_name(athlete_id)
    print(f"\n[+] Fetching activities for {athlete_name} (ID: {athlete_id})...")

    activity_ids = discover_activity_ids(session, athlete_id, months_back=months_back)
    print(f"[*] Found {len(activity_ids)} activity link(s) for target months")

    if not activity_ids:
        print(f"[-] No activities discovered for {athlete_name}")
        return 0

    existing_ids = set()
    if os.path.exists(activities_csv):
        try:
            with open(activities_csv, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    aid = r.get("activity_id")
                    if aid:
                        existing_ids.add(str(aid).strip())
        except Exception:
            pass

    added_count = 0
    with tqdm(enumerate(activity_ids), total=len(activity_ids), desc=f"Processing {athlete_name[:18]}", unit="act") as pbar:
        for idx, act_id in pbar:
            act_url = f"https://www.strava.com/activities/{act_id}"
            if act_id in existing_ids:
                log_activity_status(log_csv, act_id, act_url, athlete_id, athlete_name, "SUCCESS", "Already in CSV")
                continue

            try:
                r = session.get(act_url, timeout=12)
                if r.status_code == 200:
                    record = parse_activity_page(r.text, act_id, athlete_id, athlete_name, act_url)
                    
                    # Ensure activity is in current year 2026 (reject historical PRs from 2025 or earlier)
                    dt_str = record.get("datetime_utc", "")
                    m_prev_year = re.search(r"\b(202[0-5]|201\d)\b", dt_str)
                    if m_prev_year:
                        log_activity_status(log_csv, act_id, act_url, athlete_id, athlete_name, "SKIPPED", f"Historical year {m_prev_year.group(1)}")
                        continue

                    append_activity_to_csv(activities_csv, record)
                    existing_ids.add(act_id)
                    added_count += 1
                    log_activity_status(log_csv, act_id, act_url, athlete_id, athlete_name, "SUCCESS")
                else:
                    log_activity_status(log_csv, act_id, act_url, athlete_id, athlete_name, "FAILURE", f"HTTP {r.status_code}")
            except Exception as e:
                log_activity_status(log_csv, act_id, act_url, athlete_id, athlete_name, "FAILURE", str(e))

            time.sleep(0.3)

    print(f"[+] Finished: {added_count} new activities recorded in {activities_csv}")
    return added_count

if __name__ == "__main__":
    aid = sys.argv[1] if len(sys.argv) > 1 else "156538003"
    m_back = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    fetch_single_user(aid, months_back=m_back)
