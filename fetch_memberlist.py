import os
import sys
import json
import time
import re
import csv
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

def fetch_club_members(club_id: str = "1649493", max_pages: int = 10, min_delay: float = 2.0, out_csv: str = "memberlist.csv"):
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    for cfg_path in ["config.json", "../config.json"]:
        if os.path.exists(cfg_path):
            try:
                with open(cfg_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    session.headers.update(cfg.get("http_headers", {}))
                    session.cookies.update(cfg.get("session_cookies", {}))
                break
            except Exception:
                pass

    members = {}
    print(f"\n[+] Fetching member list for Strava Club ID: {club_id}")
    with tqdm(total=max_pages, desc="Scraping Club Pages", unit="page") as pbar:
        for page in range(1, max_pages + 1):
            url = f"https://www.strava.com/clubs/{club_id}/members?page={page}&page_uses_modern_javascript=true"
            try:
                resp = session.get(url, timeout=15)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    found_on_page = 0
                    script = soup.find("script", id="__NEXT_DATA__")
                    if script and script.string:
                        try:
                            data = json.loads(script.string)
                            club = data.get("props", {}).get("pageProps", {}).get("club", {})
                            nodes = club.get("members", {}).get("nodes", [])
                            for n in nodes:
                                ath = n.get("athlete", {})
                                aid = str(ath.get("id", "")).strip()
                                name = f"{ath.get('firstName', '')} {ath.get('lastName', '')}".strip()
                                if aid and aid not in members:
                                    members[aid] = {
                                        "athlete_id": aid,
                                        "athlete_name": name or f"Athlete {aid}",
                                        "profile_url": f"https://www.strava.com/athletes/{aid}"
                                    }
                                    found_on_page += 1
                        except Exception:
                            pass
                    for a in soup.find_all("a", href=True):
                        href = a["href"]
                        m = re.search(r"/athletes/(\d+)", href)
                        name = a.get_text().strip()
                        if m and "log" not in href and len(name) > 2:
                            aid = m.group(1)
                            if aid not in members:
                                members[aid] = {
                                    "athlete_id": aid,
                                    "athlete_name": name,
                                    "profile_url": f"https://www.strava.com/athletes/{aid}"
                                }
                                found_on_page += 1

                    pbar.set_postfix({"members": len(members)})
                    if found_on_page == 0 and page > 1:
                        pbar.update(max_pages - pbar.n)
                        break
                elif resp.status_code == 429:
                    pbar.write(f"[!] Rate limited (429) on page {page}. Stopping.")
                    break
            except Exception as e:
                pbar.write(f"[!] Error on page {page}: {e}")
                break

            pbar.update(1)
            time.sleep(min_delay)

    # Fallback to local cached lists if unauthenticated response was truncated
    if len(members) < 10:
        fallback_files = ["../memberlist.csv", "../archive/db.csv", "../archive/out.csv", "db.csv", "out.csv"]
        for fb in fallback_files:
            if os.path.exists(fb):
                try:
                    with open(fb, "r", encoding="utf-8") as f:
                        for line in f:
                            parts = line.strip().split(",")
                            if len(parts) >= 2:
                                link, name = parts[0].strip(), parts[1].strip()
                                m = re.search(r"/athletes/(\d+)", link)
                                if m and "log" not in link and name and name != "athlete_name":
                                    aid = m.group(1)
                                    if aid not in members:
                                        members[aid] = {
                                            "athlete_id": aid,
                                            "athlete_name": name,
                                            "profile_url": f"https://www.strava.com/athletes/{aid}"
                                        }
                    if len(members) >= 10:
                        break
                except Exception:
                    pass

    member_list = list(members.values())
    fieldnames = ["athlete_id", "athlete_name", "profile_url"]
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(member_list)

    print(f"[OK] Saved {len(member_list)} members to {out_csv}\n")
    return member_list

if __name__ == "__main__":
    club = sys.argv[1] if len(sys.argv) > 1 else "1649493"
    fetch_club_members(club_id=club)
