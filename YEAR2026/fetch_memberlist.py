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

def fetch_club_members(club_id: str = "1649493", max_pages: int = 15, min_delay: float = 2.0, out_csv: str = "memberlist.csv"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    for cfg_path in [
        os.path.join(base_dir, "config.json"),
        "config.json",
        "../config.json",
        os.path.join(base_dir, "..", "config.json")
    ]:
        if os.path.exists(cfg_path):
            try:
                with open(cfg_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    session.headers.update(cfg.get("http_headers", {}))
                    session.cookies.update(cfg.get("session_cookies", {}))
                break
            except Exception:
                pass

    out_csv_path = out_csv if os.path.isabs(out_csv) else os.path.join(base_dir, out_csv)
    existing_members = {}
    for p in [out_csv_path, os.path.join(base_dir, "memberlist.csv"), "memberlist.csv"]:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    for r in csv.DictReader(f):
                        aid = str(r.get("athlete_id", "")).strip()
                        aname = str(r.get("athlete_name", "")).strip()
                        purl = str(r.get("profile_url", "")).strip() or f"https://www.strava.com/athletes/{aid}"
                        if aid and aname:
                            existing_members[aid] = {
                                "athlete_id": aid,
                                "athlete_name": aname,
                                "profile_url": purl
                            }
                if existing_members:
                    break
            except Exception:
                pass

    scraped_members = {}
    print(f"\n[+] Fetching latest member list for Strava Club ID: {club_id} (max_pages={max_pages})")
    with tqdm(total=max_pages, desc="Scraping Club Pages", unit="page") as pbar:
        for page in range(1, max_pages + 1):
            url = f"https://www.strava.com/clubs/{club_id}/members?page={page}&page_uses_modern_javascript=true"
            found_on_page = 0
            try:
                resp = session.get(url, timeout=15)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
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
                                if aid and aid not in scraped_members:
                                    scraped_members[aid] = {
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
                            if aid not in scraped_members:
                                scraped_members[aid] = {
                                    "athlete_id": aid,
                                    "athlete_name": name,
                                    "profile_url": f"https://www.strava.com/athletes/{aid}"
                                }
                                found_on_page += 1

                    pbar.set_postfix({"scraped": len(scraped_members)})
                    if found_on_page == 0 and page > 1:
                        pbar.update(max_pages - pbar.n)
                        break
                elif resp.status_code == 429:
                    pbar.write(f"[!] Rate limited (429) on page {page}. Stopping further pagination.")
                    break
            except Exception as e:
                pbar.write(f"[!] Error on page {page}: {e}")
                break

            pbar.update(1)
            time.sleep(min_delay)

    # Merge scraped results with existing members
    new_athletes_found = 0
    if len(scraped_members) > 0:
        # If scrape succeeded and got reasonable results, update members
        members = dict(existing_members)
        for aid, data in scraped_members.items():
            if aid not in members:
                new_athletes_found += 1
            members[aid] = data
    else:
        # Network / rate-limit failure guard: retain existing members rather than wiping
        print("[!] Warning: Scrape returned 0 members (possible rate limit or offline). Retaining existing memberlist.")
        members = dict(existing_members)

    # Fallback to local cached lists if both scrape and existing members are empty
    if len(members) < 10:
        fallback_files = [
            os.path.join(base_dir, "archive", "db.csv"),
            os.path.join(base_dir, "archive", "out.csv"),
            os.path.join(base_dir, "..", "memberlist.csv")
        ]
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
    if not member_list:
        print("[!] Error: No members could be discovered or loaded. Leaving memberlist intact.")
        return []

    fieldnames = ["athlete_id", "athlete_name", "profile_url"]
    
    # Save to primary and mirror destinations
    dest_paths = [out_csv_path]
    for sub in ["YEAR2026", "web", "export"]:
        target_dir = os.path.join(base_dir, sub)
        if os.path.exists(target_dir):
            dest_paths.append(os.path.join(target_dir, "memberlist.csv"))

    for dest in set(dest_paths):
        try:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(member_list)
        except Exception as err:
            print(f"[-] Notice: Could not sync memberlist to {dest}: {err}")

    print(f"[OK] Successfully saved {len(member_list)} members ({new_athletes_found} new) to {out_csv_path}\n")
    return member_list

if __name__ == "__main__":
    club = sys.argv[1] if len(sys.argv) > 1 else "1649493"
    fetch_club_members(club_id=club)
