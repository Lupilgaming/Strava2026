import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def grab_session_cookie():
    chrome_binary = r"C:\Users\ds-ga\Downloads\chrome-win64\chrome-win64\chrome.exe"
    chromedriver_binary = r"C:\Users\ds-ga\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

    options = Options()
    if os.path.exists(chrome_binary):
        options.binary_location = chrome_binary

    service = webdriver.ChromeService(executable_path=chromedriver_binary) if os.path.exists(chromedriver_binary) else None
    driver = webdriver.Chrome(service=service, options=options) if service else webdriver.Chrome(options=options)

    try:
        print("[*] Opening Strava login page in Chrome...")
        driver.get("https://www.strava.com/login")
        print("[*] Please log into your Strava account in the opened Chrome window.")
        
        session_cookie = ""
        start_time = time.time()
        while time.time() - start_time < 120:
            cookies = {c["name"]: c["value"] for c in driver.get_cookies()}
            if "_strava4_session" in cookies:
                session_cookie = cookies["_strava4_session"]
                print("[+] Detected authenticated Strava session cookie!")
                break
            time.sleep(2)

        if session_cookie:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
            cfg = {}
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    try: cfg = json.load(f)
                    except: cfg = {}
            
            cfg.setdefault("session_cookies", {})["_strava4_session"] = session_cookie
            cfg.setdefault("http_headers", {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            })
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(cfg, f, indent=2)
            print(f"[+] Successfully saved session cookie to {config_path}")
            return session_cookie
        else:
            print("[-] Login timed out or session cookie not found.")
            return None
    finally:
        driver.quit()

if __name__ == "__main__":
    grab_session_cookie()
