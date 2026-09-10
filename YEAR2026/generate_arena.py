import os
import json
import shutil

ROOT_DIR = r"C:\Users\ds-ga\Documents\automations\strava club download"
YEAR_DIR = os.path.join(ROOT_DIR, "YEAR2026")
WEB_DIR = os.path.join(ROOT_DIR, "web")
EXPORT_DIR = os.path.join(ROOT_DIR, "export")

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

    json_str = json.dumps(dashboard_data, indent=2)

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
       TEAM BUILDER STYLES
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
      padding: 7px 14px;
      border-radius: 10px;
      font-size: 12.5px;
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
      transition: width 0.4s ease;
      position: relative;
    }

    /* Squad Cards Grid */
    .tb-squad-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
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
      padding: 18px 20px;
      border-bottom: 1px solid var(--card-border);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .tb-squad-name {
      font-family: 'Outfit', sans-serif;
      font-size: 18px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .tb-squad-score {
      font-family: 'Outfit', sans-serif;
      font-size: 24px;
      font-weight: 900;
      letter-spacing: -0.5px;
    }

    .tb-squad-meta-bar {
      padding: 10px 20px;
      background: rgba(15, 23, 42, 0.4);
      display: flex;
      justify-content: space-between;
      font-size: 11.5px;
      color: var(--text-muted);
      border-bottom: 1px solid var(--card-border);
    }

    .tb-synergy-tray {
      padding: 12px 18px;
      background: rgba(255, 255, 255, 0.02);
      border-bottom: 1px solid var(--card-border);
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      min-height: 48px;
      align-items: center;
    }

    .tb-synergy-pill {
      font-size: 11px;
      font-weight: 700;
      padding: 3px 9px;
      border-radius: 8px;
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
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      flex: 1;
      max-height: 440px;
      overflow-y: auto;
    }

    .tb-player-card {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 10px 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      transition: all 0.2s;
    }
    .tb-player-card:hover {
      background: rgba(30, 41, 59, 0.8);
      border-color: rgba(255, 255, 255, 0.2);
    }

    .tb-player-info {
      display: flex;
      align-items: center;
      gap: 10px;
      min-width: 0;
    }

    .tb-player-avatar {
      width: 32px;
      height: 32px;
      border-radius: 10px;
      background: #1e293b;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      font-weight: 800;
      color: #cbd5e1;
      flex-shrink: 0;
    }

    .tb-player-name {
      font-size: 13px;
      font-weight: 700;
      color: #fff;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .tb-class-badge {
      font-size: 10px;
      font-weight: 800;
      padding: 1px 7px;
      border-radius: 6px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      display: inline-block;
      margin-top: 2px;
    }

    .tb-player-stats {
      text-align: right;
      flex-shrink: 0;
    }

    .tb-player-pts {
      font-family: 'Outfit', sans-serif;
      font-size: 14px;
      font-weight: 800;
      color: var(--gold);
    }

    .tb-player-sub {
      font-size: 10.5px;
      color: var(--text-dim);
    }

    .tb-move-select {
      background: #0f172a;
      border: 1px solid var(--card-border);
      color: var(--text-muted);
      border-radius: 6px;
      font-size: 11px;
      padding: 3px 6px;
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
      padding: 24px;
      margin-bottom: 30px;
    }

    .tb-guide-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin-top: 16px;
    }

    .tb-class-item {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 14px;
    }

    .tb-class-item-title {
      font-size: 13.5px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 6px;
      margin-bottom: 4px;
    }

    .tb-class-item-desc {
      font-size: 12px;
      color: var(--text-muted);
      line-height: 1.4;
    }

    /* =========================================================================
       EXISTING PANELS STYLES (Trophies, Duel, Road Trip, Momentum, Roulette)
       ========================================================================= */
    /* Trophy Cards Grid */
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
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .trophy-card:hover {
      transform: translateY(-4px);
      border-color: var(--card-hover-border);
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(252, 76, 2, 0.15);
    }

    .trophy-icon-box {
      width: 54px;
      height: 54px;
      border-radius: 16px;
      background: linear-gradient(135deg, rgba(252, 76, 2, 0.2), rgba(255, 106, 43, 0.1));
      border: 1px solid rgba(252, 76, 2, 0.3);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28px;
      margin-bottom: 16px;
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

    /* Responsive */
    @media (max-width: 900px) {
      .duel-layout { grid-template-columns: 1fr; }
      .momentum-grid { grid-template-columns: 1fr; }
      .duel-selectors { grid-template-columns: 1fr; }
      .duel-vs-badge { margin: 0 auto; }
      .date-filter-bar { flex-direction: column; align-items: stretch; }
      .filter-left, .filter-right { justify-content: space-between; }
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
          The gamified clubhouse for Connectivity Sports Day 2026. Build balanced squads with RPG party synergies, spin the workout roulette, track momentum velocity, simulate 1v1 duels, and explore algorithmic trophies.
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
            ⚡ Official (Sep 9+)
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
          <input type="date" id="dateStart" class="date-input" value="2026-09-09" onchange="onCustomDateChange()">
        </div>
        <div class="date-input-wrap">
          <span>To:</span>
          <input type="date" id="dateEnd" class="date-input" value="" onchange="onCustomDateChange()">
        </div>
        <div id="activityCountBadge" class="activity-count-badge">Loading...</div>
      </div>
    </div>

    <!-- Arena Navigation Tabs (Reordered with Team Builder 1st, others in reverse order) -->
    <div class="arena-nav-bar">
      <button id="tabBtnTeamBuilder" class="arena-nav-tab active" onclick="switchArenaTab('tabTeamBuilder')">
        <span>👥</span> Team Builder
      </button>
      <button id="tabBtnRoulette" class="arena-nav-tab" onclick="switchArenaTab('tabRoulette')">
        <span>🎲</span> Workout Roulette
      </button>
      <button id="tabBtnMomentum" class="arena-nav-tab" onclick="switchArenaTab('tabMomentum')">
        <span>🔥</span> Momentum Tracker
      </button>
      <button id="tabBtnJourney" class="arena-nav-tab" onclick="switchArenaTab('tabJourney')">
        <span>🗺️</span> Virtual Road Trip
      </button>
      <button id="tabBtnDuel" class="arena-nav-tab" onclick="switchArenaTab('tabDuel')">
        <span>🥊</span> 1v1 Duel Arena
      </button>
      <button id="tabBtnTrophies" class="arena-nav-tab" onclick="switchArenaTab('tabTrophies')">
        <span>🏆</span> The Trophy Room
      </button>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 1: TEAM BUILDER & RPG SYNERGIES -->
    <!-- =================================================================== -->
    <div id="tabTeamBuilder" class="arena-panel active">
      <div class="section-header">
        <div class="section-title">
          <span>👥</span> AI Fair-Play Team Builder & RPG Synergies
        </div>
        <div class="section-desc">
          Partition club athletes into mathematically balanced squads using a multi-objective greedy snake partition. Athletes are assigned RPG Hero Classes based on their Strava profile, unlocking team synergy buffs when drafting diverse, well-rounded squads!
        </div>
      </div>

      <!-- Team Builder Controls -->
      <div class="tb-controls">
        <div class="tb-group">
          <span style="font-size:12.5px; font-weight:700; color:var(--text-muted);">Squad Count:</span>
          <button id="squadBtn2" class="tb-squad-btn active" onclick="setSquadCount(2)">2 Squads</button>
          <button id="squadBtn3" class="tb-squad-btn" onclick="setSquadCount(3)">3 Squads</button>
          <button id="squadBtn4" class="tb-squad-btn" onclick="setSquadCount(4)">4 Squads</button>
        </div>

        <div class="tb-group">
          <button class="btn btn-orange" onclick="autoBalanceTeams()" title="Run AI algorithm to equalize points and sports">
            <span>⚡</span> Auto-Balance
          </button>
          <button class="btn btn-outline" onclick="shuffleTeams()" title="Randomly shuffle roster across squads">
            <span>🎲</span> Shuffle
          </button>
          <button class="btn btn-outline" onclick="copyTeamRoster()" title="Copy formatted roster text to clipboard for Slack / WhatsApp">
            <span>📋</span> Copy Roster
          </button>
        </div>
      </div>

      <!-- Live Balance Meter -->
      <div class="tb-balance-card">
        <div class="tb-balance-header">
          <span id="tbBalanceTitle">⚖️ Squad Balance Meter</span>
          <span id="tbBalanceStatus" style="color:var(--accent-green);">Calculating...</span>
        </div>
        <div id="tbBalanceMeter" class="tb-balance-meter">
          <!-- Injected via JS -->
        </div>
      </div>

      <!-- Squad Columns Grid -->
      <div id="tbSquadGrid" class="tb-squad-grid">
        <!-- Injected via JS -->
      </div>

      <!-- RPG Hero Class & Synergies Explainer -->
      <div class="tb-class-guide">
        <div style="font-family:'Outfit',sans-serif; font-size:18px; font-weight:800; color:#fff; margin-bottom:4px;">
          🧙‍♂️ RPG Hero Classes & Team Synergies
        </div>
        <div style="font-size:12.5px; color:var(--text-muted); line-height:1.5;">
          Every athlete is classified based on their pace, volume, and sport diversity. Combining different classes unlocks powerful team synergy buffs!
        </div>

        <div class="tb-guide-grid">
          <div class="tb-class-item">
            <div class="tb-class-item-title" style="color:#22c55e;">🏹 The Ranger</div>
            <div class="tb-class-item-desc">High-volume endurance specialist (&ge; 25 km distance or long continuous runs/rides).</div>
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

        <div style="margin-top:18px; padding-top:14px; border-top:1px solid var(--card-border); font-size:12px; color:var(--text-dim); display:flex; flex-wrap:wrap; gap:16px;">
          <span>✨ <strong>Tri-Sport Mastery (+8%):</strong> Squad covers Run, Walk, & Ride/Workout.</span>
          <span>🌙 <strong>24-Hour Watch (+5%):</strong> Squad features Dawn Patrol (&lt;7 AM) & Night Owl (&gt;8 PM).</span>
          <span>🛡️ <strong>Class Quintet (+10%):</strong> Squad includes 3+ distinct Hero Classes.</span>
          <span>⚡ <strong>Speed & Stamina (+6%):</strong> Squad pairs a Ranger with an Assassin.</span>
        </div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 2: WORKOUT ROULETTE -->
    <!-- =================================================================== -->
    <div id="tabRoulette" class="arena-panel">
      <div class="section-header">
        <div class="section-title">
          <span>🎲</span> The Workout Roulette
        </div>
        <div class="section-desc">
          Feeling indecisive? Spin the wheel to receive a spontaneous club fitness dare with estimated points!
        </div>
      </div>

      <div class="roulette-box">
        <div style="font-size: 13px; text-transform: uppercase; letter-spacing: 1px; color: var(--strava-orange); font-weight: 800;">
          Your Daily Fitness Dare
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
          🎲 Spin Again
        </button>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 3: MOMENTUM TRACKER -->
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
    <!-- TAB 4: VIRTUAL ROAD TRIP -->
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
    <!-- TAB 5: 1v1 DUEL ARENA -->
    <!-- =================================================================== -->
    <div id="tabDuel" class="arena-panel">
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
          <span class="fighter-label red">🔴 Red Corner</span>
          <select id="fighterRed" class="fighter-select" onchange="updateDuel()"></select>
        </div>

        <div class="duel-vs-badge">VS</div>

        <div class="fighter-select-box">
          <span class="fighter-label blue">🔵 Blue Corner</span>
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
    <!-- TAB 6: THE TROPHY ROOM -->
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

  </div>

  <!-- Toast Element -->
  <div id="toastNotification">
    <span id="toastMsg">✅ Roster copied!</span>
  </div>

  <!-- Embedded fallback JSON data for seamless offline rendering -->
  <script id="fallback-data" type="application/json">
<!-- FALLBACK_DATA_PLACEHOLDER -->
  </script>

  <script>
    let globalData = null;
    let duelRadarChartInstance = null;

    // Date Filter State (Default: Sep 9, 2026 onwards for the official tournament)
    window.currentDateStart = '2026-09-09';
    window.currentDateEnd = '';
    window.currentPreset = 'tournament';

    // Team Builder State
    let currentTeamCount = 2;
    let teamRosters = { 0: [], 1: [], 2: [], 3: [] };

    const SQUAD_METAS = [
      { id: 0, name: "Red Phoenix", color: "#ef4444", bg: "rgba(239, 68, 68, 0.12)", border: "rgba(239, 68, 68, 0.35)", icon: "🔴" },
      { id: 1, name: "Blue Hydra", color: "#3b82f6", bg: "rgba(59, 130, 246, 0.12)", border: "rgba(59, 130, 246, 0.35)", icon: "🔵" },
      { id: 2, name: "Emerald Dragons", color: "#10b981", bg: "rgba(16, 185, 129, 0.12)", border: "rgba(16, 185, 129, 0.35)", icon: "🟢" },
      { id: 3, name: "Golden Gryphons", color: "#f59e0b", bg: "rgba(245, 158, 11, 0.12)", border: "rgba(245, 158, 11, 0.35)", icon: "🟡" }
    ];

    // Road Trip Milestones
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

    // Workout Roulette Dares
    const DARES = [
      {
        icon: "🌅",
        title: "The Sunrise 5k Cruise",
        desc: "Log a continuous 5.0 km run or walk before 7:30 AM. Earn a dynamic pace bonus and lead the Dawn Patrol trophy.",
        pts: "~110 - 145 pts"
      },
      {
        icon: "⚡",
        title: "Negative Split 4k",
        desc: "Run 4 km outdoor where your second 2 km is at least 15 sec/km faster than your first 2 km.",
        pts: "~120 - 160 pts"
      },
      {
        icon: "🚴",
        title: "Virtual Century Sprint",
        desc: "Complete 15.0+ km on an indoor smart trainer or outdoor cycling route maintaining steady cadence.",
        pts: "~95 - 130 pts"
      },
      {
        icon: "🔥",
        title: "The Midday 30m Tabata Burn",
        desc: "Log 30 minutes of high-intensity functional workout or weight training during lunch hour.",
        pts: "~90 - 120 pts"
      },
      {
        icon: "🦉",
        title: "Night Hawk Recovery Stride",
        desc: "Log a 4.0 km walk or gentle jog after 8:30 PM under the stars to claim the Night Owl badge.",
        pts: "~80 - 100 pts"
      },
      {
        icon: "⛰️",
        title: "The Elevation Challenge",
        desc: "Find a route with at least 50m of elevation gain across your run or walk.",
        pts: "~130 - 170 pts"
      }
    ];

    function showToast(msg) {
      const t = document.getElementById('toastNotification');
      document.getElementById('toastMsg').innerText = msg;
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 3200);
    }

    /* Tab Switching */
    function switchArenaTab(tabId) {
      document.querySelectorAll('.arena-panel').forEach(p => p.classList.remove('active'));
      document.querySelectorAll('.arena-nav-tab').forEach(b => b.classList.remove('active'));

      const activePanel = document.getElementById(tabId);
      if (activePanel) activePanel.classList.add('active');

      const btnMap = {
        'tabTeamBuilder': 'tabBtnTeamBuilder',
        'tabRoulette': 'tabBtnRoulette',
        'tabMomentum': 'tabBtnMomentum',
        'tabJourney': 'tabBtnJourney',
        'tabDuel': 'tabBtnDuel',
        'tabTrophies': 'tabBtnTrophies'
      };

      if (btnMap[tabId]) {
        const btn = document.getElementById(btnMap[tabId]);
        if (btn) btn.classList.add('active');
      }

      if (tabId === 'tabDuel' && duelRadarChartInstance) {
        setTimeout(() => duelRadarChartInstance.resize(), 100);
      }
    }

    /* Date Filter Handlers */
    function setDatePreset(preset) {
      window.currentPreset = preset;
      document.querySelectorAll('.preset-pill').forEach(b => b.classList.remove('active'));

      const startInput = document.getElementById('dateStart');
      const endInput = document.getElementById('dateEnd');

      if (preset === 'tournament') {
        document.getElementById('presetTournament').classList.add('active');
        window.currentDateStart = '2026-09-09';
        window.currentDateEnd = '';
        startInput.value = '2026-09-09';
        endInput.value = '';
      } else if (preset === 'all') {
        document.getElementById('presetAll').classList.add('active');
        window.currentDateStart = '';
        window.currentDateEnd = '';
        startInput.value = '';
        endInput.value = '';
      } else if (preset === '7days') {
        document.getElementById('preset7Days').classList.add('active');
        const d = new Date('2026-09-10'); // align with latest dataset date
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
      const s = document.getElementById('dateStart').value;
      const e = document.getElementById('dateEnd').value;
      window.currentDateStart = s;
      window.currentDateEnd = e;

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

      // Re-render components with filtered dataset
      autoBalanceTeams();
      renderTrophies();
      updateDuel();
      renderVirtualJourney();
      renderMomentum();
    }

    /* Athlete Stats Aggregation & Hero Class Assignment */
    function computeAthleteStats(activities) {
      const statsMap = {};

      // Initialize all athletes from global roster
      (globalData.athletes || []).forEach(a => {
        statsMap[a.athlete_name] = {
          athlete_id: a.athlete_id,
          athlete_name: a.athlete_name,
          total_points: 0,
          total_points_legacy: 0,
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
          weekend_count: 0,
          active_dates: new Set(),
          hero_class_name: 'Sentinel',
          hero_class_icon: '🛡️',
          hero_class_desc: 'Consistent Daily Streaker',
          hero_class_color: '#fbbf24'
        };
      });

      // Aggregate filtered activities
      activities.forEach(act => {
        const name = act.athlete_name;
        if (!statsMap[name]) {
          statsMap[name] = {
            athlete_id: act.athlete_id,
            athlete_name: name,
            total_points: 0,
            total_points_legacy: 0,
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
            weekend_count: 0,
            active_dates: new Set(),
            hero_class_name: 'Sentinel',
            hero_class_icon: '🛡️',
            hero_class_desc: 'Consistent Daily Streaker',
            hero_class_color: '#fbbf24'
          };
        }

        const st = statsMap[name];
        const pts = parseFloat(act.points_dynamic || act.points || 0);
        const dist = parseFloat(act.distance_km || 0);
        const durMin = parseFloat(act.duration_minutes || 0);

        st.total_points += pts;
        st.total_points_legacy += parseFloat(act.points_legacy || 0);
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
            if (d.getDay() === 0 || d.getDay() === 6) st.weekend_count += 1;
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

      // Classify Hero Archetypes
      Object.values(statsMap).forEach(st => {
        const sportsCount = Object.keys(st.sports).length;
        const isFastRunner = st.fastest_pace_val < 5.4;
        const isEndurance = st.total_distance >= 25 || st.max_single_dist >= 10;
        const isPowerCrusher = (st.sports['Weight Training'] || 0) + (st.sports['Workout'] || 0) + (st.sports['Swim'] || 0) > 0 || st.max_single_duration >= 60;
        const isStreakMaster = st.active_dates.size >= 4 || st.total_activities >= 5;

        if (sportsCount >= 2) {
          st.hero_class_name = 'Polymath';
          st.hero_class_icon = '🧙‍♂️';
          st.hero_class_desc = 'Hybrid Multi-Sport Athlete';
          st.hero_class_color = '#38bdf8';
        } else if (isFastRunner) {
          st.hero_class_name = 'Assassin';
          st.hero_class_icon = '⚡';
          st.hero_class_desc = 'Sub-5:30 High-Speed Specialist';
          st.hero_class_color = '#a855f7';
        } else if (isEndurance) {
          st.hero_class_name = 'Ranger';
          st.hero_class_icon = '🏹';
          st.hero_class_desc = 'High-Distance Stamina Specialist';
          st.hero_class_color = '#22c55e';
        } else if (isPowerCrusher) {
          st.hero_class_name = 'Berserker';
          st.hero_class_icon = '🏋️';
          st.hero_class_desc = 'High-Intensity Power Crusher';
          st.hero_class_color = '#ef4444';
        } else {
          st.hero_class_name = 'Sentinel';
          st.hero_class_icon = '🛡️';
          st.hero_class_desc = 'Consistent Daily Streaker';
          st.hero_class_color = '#fbbf24';
        }
        st.hero_class = `${st.hero_class_icon} ${st.hero_class_name}`;
      });

      return statsMap;
    }

    /* =========================================================================
       1. TEAM BUILDER & RPG SYNERGIES LOGIC
       ========================================================================= */
    function setSquadCount(count) {
      currentTeamCount = count;
      document.querySelectorAll('.tb-squad-btn').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById(`squadBtn${count}`);
      if (activeBtn) activeBtn.classList.add('active');

      autoBalanceTeams();
    }

    function autoBalanceTeams() {
      const statsMap = computeAthleteStats(getFilteredActivities());
      const athleteList = Object.values(statsMap).sort((a, b) => {
        if (b.total_points !== a.total_points) return b.total_points - a.total_points;
        return b.total_distance - a.total_distance;
      });

      const newRosters = {};
      const squadTotals = {};
      for (let i = 0; i < currentTeamCount; i++) {
        newRosters[i] = [];
        squadTotals[i] = 0;
      }

      // Greedy Snake Partition with load balancing
      athleteList.forEach((ath) => {
        let minTeam = 0;
        let minVal = Infinity;
        for (let i = 0; i < currentTeamCount; i++) {
          if (squadTotals[i] < minVal) {
            minVal = squadTotals[i];
            minTeam = i;
          }
        }
        newRosters[minTeam].push(ath.athlete_name);
        squadTotals[minTeam] += Math.max(ath.total_points, 10);
      });

      // 2-Opt local refinement to minimize variance
      for (let step = 0; step < 40; step++) {
        let improved = false;
        let maxTeam = 0, minTeam = 0;
        for (let i = 0; i < currentTeamCount; i++) {
          if (squadTotals[i] > squadTotals[maxTeam]) maxTeam = i;
          if (squadTotals[i] < squadTotals[minTeam]) minTeam = i;
        }

        const currentDiff = squadTotals[maxTeam] - squadTotals[minTeam];
        if (currentDiff <= 4) break;

        let bestSwap = null;
        let bestNewDiff = currentDiff;
        const maxMembers = newRosters[maxTeam];
        const minMembers = newRosters[minTeam];

        for (let aIdx = 0; aIdx < maxMembers.length; aIdx++) {
          const pA = statsMap[maxMembers[aIdx]] ? statsMap[maxMembers[aIdx]].total_points : 0;
          for (let bIdx = 0; bIdx < minMembers.length; bIdx++) {
            const pB = statsMap[minMembers[bIdx]] ? statsMap[minMembers[bIdx]].total_points : 0;
            const change = pA - pB;
            if (change > 0) {
              const diff = Math.abs((squadTotals[maxTeam] - change) - (squadTotals[minTeam] + change));
              if (diff < bestNewDiff) {
                bestNewDiff = diff;
                bestSwap = { aIdx, bIdx, change };
              }
            }
          }
        }

        if (bestSwap && bestNewDiff < currentDiff - 2) {
          const temp = maxMembers[bestSwap.aIdx];
          maxMembers[bestSwap.aIdx] = minMembers[bestSwap.bIdx];
          minMembers[bestSwap.bIdx] = temp;
          squadTotals[maxTeam] -= bestSwap.change;
          squadTotals[minTeam] += bestSwap.change;
          improved = true;
        }
        if (!improved) break;
      }

      teamRosters = newRosters;
      renderTeamBuilder();
    }

    function shuffleTeams() {
      const statsMap = computeAthleteStats(getFilteredActivities());
      const athleteNames = Object.keys(statsMap).sort(() => Math.random() - 0.5);

      const newRosters = {};
      for (let i = 0; i < currentTeamCount; i++) newRosters[i] = [];

      athleteNames.forEach((name, idx) => {
        newRosters[idx % currentTeamCount].push(name);
      });

      teamRosters = newRosters;
      renderTeamBuilder();
      showToast("🎲 Squads shuffled!");
    }

    function moveAthlete(athleteName, targetIdx) {
      targetIdx = parseInt(targetIdx);
      for (let i = 0; i < currentTeamCount; i++) {
        teamRosters[i] = (teamRosters[i] || []).filter(n => n !== athleteName);
      }
      if (teamRosters[targetIdx]) {
        teamRosters[targetIdx].push(athleteName);
      }
      renderTeamBuilder();
    }

    function calculateTeamSynergies(memberNames, statsMap) {
      const members = memberNames.map(n => statsMap[n]).filter(Boolean);
      const activeBuffs = [];
      let totalBuffPct = 0;

      // 1. Tri-Sport Mastery (+8%)
      const allSports = new Set();
      members.forEach(m => Object.keys(m.sports).forEach(s => allSports.add(s.toLowerCase())));
      const hasRun = Array.from(allSports).some(s => s.includes('run'));
      const hasWalk = Array.from(allSports).some(s => s.includes('walk') || s.includes('hike'));
      const hasOther = Array.from(allSports).some(s => s.includes('ride') || s.includes('train') || s.includes('workout') || s.includes('swim'));
      if (hasRun && hasWalk && hasOther) {
        activeBuffs.push({ name: "✨ Tri-Sport Mastery", pct: 8, desc: "Roster spans Running, Walking, & Cycling/Workouts" });
        totalBuffPct += 8;
      }

      // 2. 24-Hour Watch (+5%)
      const totalNight = members.reduce((sum, m) => sum + m.night_owl_count, 0);
      const totalDawn = members.reduce((sum, m) => sum + m.dawn_patrol_count, 0);
      if (totalNight >= 1 && totalDawn >= 1) {
        activeBuffs.push({ name: "🌙 24-Hour Watch", pct: 5, desc: "Features both Dawn Patrol and Night Owl athletes" });
        totalBuffPct += 5;
      }

      // 3. Class Quintet (+10%)
      const uniqueClasses = new Set(members.map(m => m.hero_class_name));
      if (uniqueClasses.size >= 3) {
        activeBuffs.push({ name: "🛡️ Class Quintet", pct: 10, desc: `Balanced party of ${uniqueClasses.size} distinct Hero Classes` });
        totalBuffPct += 10;
      }

      // 4. Speed & Stamina (+6%)
      if (uniqueClasses.has('Ranger') && uniqueClasses.has('Assassin')) {
        activeBuffs.push({ name: "⚡ Speed & Stamina", pct: 6, desc: "Pairs endurance Ranger with speed Assassin" });
        totalBuffPct += 6;
      }

      const basePoints = members.reduce((sum, m) => sum + m.total_points, 0);
      const adjustedPoints = Math.round(basePoints * (1 + totalBuffPct / 100));
      const totalDist = members.reduce((sum, m) => sum + m.total_distance, 0);
      const totalHours = members.reduce((sum, m) => sum + m.total_duration_hours, 0);

      return {
        basePoints: Math.round(basePoints),
        totalBuffPct,
        adjustedPoints,
        totalDist: (Math.round(totalDist * 10) / 10).toFixed(1),
        totalHours: (Math.round(totalHours * 10) / 10).toFixed(1),
        activeBuffs,
        members
      };
    }

    function renderTeamBuilder() {
      const statsMap = computeAthleteStats(getFilteredActivities());
      const grid = document.getElementById('tbSquadGrid');
      const balanceMeter = document.getElementById('tbBalanceMeter');
      if (!grid || !balanceMeter) return;

      const squadData = [];
      for (let i = 0; i < currentTeamCount; i++) {
        const meta = SQUAD_METAS[i];
        const data = calculateTeamSynergies(teamRosters[i] || [], statsMap);
        squadData.push({ meta, data });
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
      if (delta <= 25) {
        statusEl.innerHTML = `⚖️ Statistically Even: Δ ${delta} pts difference`;
        statusEl.style.color = 'var(--accent-green)';
      } else {
        const leader = squadData.find(s => s.data.adjustedPoints === maxPts);
        statusEl.innerHTML = `⚡ Lead: ${leader.meta.name} (+${delta} pts)`;
        statusEl.style.color = 'var(--gold)';
      }

      // Render Squad Columns
      grid.innerHTML = squadData.map((s, idx) => {
        const { meta, data } = s;

        // Synergy badges
        let synergyHtml = '';
        if (data.activeBuffs.length === 0) {
          synergyHtml = `<span style="font-size:11px; color:var(--text-dim); font-style:italic;">No active synergies. Draft diverse classes to trigger buffs!</span>`;
        } else {
          synergyHtml = data.activeBuffs.map(b => `
            <span class="tb-synergy-pill" style="background:${meta.bg}; border-color:${meta.border}; color:${meta.color};" title="${b.desc}">
              ${b.name} <strong style="color:#fff;">+${b.pct}%</strong>
            </span>
          `).join('');
        }

        // Roster items
        const rosterHtml = data.members.map(m => {
          let moveOptions = '';
          for (let o = 0; o < currentTeamCount; o++) {
            if (o !== idx) {
              moveOptions += `<option value="${o}">Move → ${SQUAD_METAS[o].name}</option>`;
            }
          }

          const initials = m.athlete_name.split(' ').map(p => p[0]).join('').slice(0, 2).toUpperCase();

          return `
            <div class="tb-player-card">
              <div class="tb-player-info">
                <div class="tb-player-avatar">${initials}</div>
                <div>
                  <div class="tb-player-name" title="${m.athlete_name}">${m.athlete_name}</div>
                  <span class="tb-class-badge" style="background:${m.hero_class_color}22; border:1px solid ${m.hero_class_color}44; color:${m.hero_class_color};">
                    ${m.hero_class}
                  </span>
                </div>
              </div>
              <div style="display:flex; align-items:center; gap:12px;">
                <div class="tb-player-stats">
                  <div class="tb-player-pts">${Math.round(m.total_points).toLocaleString()} <span style="font-size:10px; color:var(--text-muted);">pts</span></div>
                  <div class="tb-player-sub">${(Math.round(m.total_distance * 10) / 10).toFixed(1)} km • ${m.total_activities} acts</div>
                </div>
                <select class="tb-move-select" onchange="moveAthlete('${m.athlete_name.replace(/'/g, "\\'")}', this.value)">
                  <option value="${idx}" selected>Team</option>
                  ${moveOptions}
                </select>
              </div>
            </div>
          `;
        }).join('');

        return `
          <div class="tb-squad-card" style="border-top: 4px solid ${meta.color};">
            <div class="tb-squad-header">
              <div class="tb-squad-name" style="color:${meta.color};">
                <span>${meta.icon}</span> ${meta.name}
              </div>
              <div style="text-align:right;">
                <div class="tb-squad-score" style="color:${meta.color};">${data.adjustedPoints.toLocaleString()}</div>
                <div style="font-size:11px; color:var(--text-muted);">Base: ${data.basePoints.toLocaleString()} pts (+${data.totalBuffPct}%)</div>
              </div>
            </div>

            <div class="tb-squad-meta-bar">
              <span>🏃‍♂️ ${data.totalDist} km</span>
              <span>⏱️ ${data.totalHours} hrs</span>
              <span>👥 ${data.members.length} athletes</span>
            </div>

            <div class="tb-synergy-tray">
              ${synergyHtml}
            </div>

            <div class="tb-roster-list">
              ${rosterHtml.length ? rosterHtml : '<div style="text-align:center; padding:20px; color:var(--text-dim); font-size:12px;">Empty Squad</div>'}
            </div>
          </div>
        `;
      }).join('');
    }

    function copyTeamRoster() {
      const statsMap = computeAthleteStats(getFilteredActivities());
      let text = "🏆 CONNECTIVITY SPORTS DAY 2026 - BALANCED SQUADS 🏆\n";
      text += `Period: ${window.currentPreset === 'tournament' ? 'Official Tournament (Sep 9+)' : (window.currentPreset === '7days' ? 'Last 7 Days' : 'All-Time')}\n`;
      text += "====================================================\n\n";

      for (let i = 0; i < currentTeamCount; i++) {
        const meta = SQUAD_METAS[i];
        const teamData = calculateTeamSynergies(teamRosters[i] || [], statsMap);
        text += `${meta.icon} ${meta.name.toUpperCase()}\n`;
        text += `Total Score: ${teamData.adjustedPoints.toLocaleString()} pts (Base: ${teamData.basePoints.toLocaleString()} pts + ${teamData.totalBuffPct}% Synergy Buff)\n`;
        text += `Distance: ${teamData.totalDist} km | Time: ${teamData.totalHours} hrs | Squad Size: ${teamData.members.length}\n`;
        if (teamData.activeBuffs.length > 0) {
          text += `Active Buffs: ${teamData.activeBuffs.map(b => `${b.name} (+${b.pct}%)`).join(' | ')}\n`;
        }
        text += "Roster:\n";
        teamData.members.forEach(m => {
          text += ` • ${m.athlete_name} (${m.hero_class}) — ${Math.round(m.total_points).toLocaleString()} pts (${(Math.round(m.total_distance * 10) / 10).toFixed(1)} km, ${m.total_activities} acts)\n`;
        });
        text += "\n";
      }
      text += "View & Simulate in The Arena: https://lupilgaming.github.io/Strava2026/arena.html\n";

      navigator.clipboard.writeText(text).then(() => {
        showToast("✅ Squad roster copied to clipboard!");
      }).catch(() => {
        alert("Roster generated! Please copy from console or share card.");
      });
    }

    /* =========================================================================
       2. WORKOUT ROULETTE LOGIC
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
       3. MOMENTUM TRACKER LOGIC
       ========================================================================= */
    function renderMomentum() {
      const statsMap = computeAthleteStats(getFilteredActivities());
      const athletes = Object.values(statsMap).sort((a, b) => b.total_activities - a.total_activities || b.total_points - a.total_points);

      const listEl = document.getElementById('momentumList');
      if (!listEl) return;

      const top5 = athletes.slice(0, 6);
      listEl.innerHTML = top5.map((a, idx) => `
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
       4. VIRTUAL ROAD TRIP LOGIC
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
       5. 1v1 DUEL ARENA LOGIC
       ========================================================================= */
    function initDuelSelectors() {
      const statsMap = computeAthleteStats(globalData.activities || []);
      const athletes = Object.values(statsMap).sort((a, b) => b.total_points - a.total_points);

      const redSel = document.getElementById('fighterRed');
      const blueSel = document.getElementById('fighterBlue');
      if (!redSel || !blueSel) return;

      redSel.innerHTML = athletes.map((a, i) => `<option value="${a.athlete_name}" ${i === 0 ? 'selected' : ''}>${a.athlete_name} (${Math.round(a.total_points)} pts)</option>`).join('');
      blueSel.innerHTML = athletes.map((a, i) => `<option value="${a.athlete_name}" ${i === 1 ? 'selected' : ''}>${a.athlete_name} (${Math.round(a.total_points)} pts)</option>`).join('');

      updateDuel();
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

      const stats = [
        { label: "Total Points", val1: Math.round(aRed.total_points).toLocaleString(), val2: Math.round(aBlue.total_points).toLocaleString(), raw1: aRed.total_points, raw2: aBlue.total_points },
        { label: "Distance", val1: `${(Math.round(aRed.total_distance * 10) / 10).toFixed(1)} km`, val2: `${(Math.round(aBlue.total_distance * 10) / 10).toFixed(1)} km`, raw1: aRed.total_distance, raw2: aBlue.total_distance },
        { label: "Activities", val1: `${aRed.total_activities} logs`, val2: `${aBlue.total_activities} logs`, raw1: aRed.total_activities, raw2: aBlue.total_activities },
        { label: "Time on Trail", val1: `${(Math.round(aRed.total_duration_hours * 10) / 10).toFixed(1)} hrs`, val2: `${(Math.round(aBlue.total_duration_hours * 10) / 10).toFixed(1)} hrs`, raw1: aRed.total_duration_hours, raw2: aBlue.total_duration_hours },
        { label: "Hero Class", val1: aRed.hero_class || 'N/A', val2: aBlue.hero_class || 'N/A', raw1: 0, raw2: 0, isText: true }
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

      // Verdict
      let verdict = "";
      if (aRed.total_points > aBlue.total_points * 1.1) {
        verdict = `🏆 Tale of the Tape: <strong>${aRed.athlete_name}</strong> holds a commanding points lead (+${Math.round(aRed.total_points - aBlue.total_points)} pts)!`;
      } else if (aBlue.total_points > aRed.total_points * 1.1) {
        verdict = `🏆 Tale of the Tape: <strong>${aBlue.athlete_name}</strong> holds a commanding points lead (+${Math.round(aBlue.total_points - aRed.total_points)} pts)!`;
      } else {
        verdict = `⚖️ Dead Heat! Both athletes are closely matched within striking distance!`;
      }
      document.getElementById('duelVerdict').innerHTML = verdict;

      // Update Radar Chart
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
       6. TROPHY ROOM LOGIC
       ========================================================================= */
    function renderTrophies() {
      const activities = getFilteredActivities();
      const statsMap = computeAthleteStats(activities);
      const athletes = Object.values(statsMap);

      const nightOwls = {};
      const earlyBirds = {};
      const weekendKms = {};
      const sportDiversity = {};
      let fastestPace = { athlete: 'N/A', paceStr: 'N/A', paceVal: 999, dist: 0 };
      let longestSingle = { athlete: 'N/A', dist: 0, sport: 'N/A' };

      athletes.forEach(a => {
        nightOwls[a.athlete_name] = a.night_owl_count;
        earlyBirds[a.athlete_name] = a.dawn_patrol_count;
        weekendKms[a.athlete_name] = a.weekend_count;
        sportDiversity[a.athlete_name] = Object.keys(a.sports).length || 1;
        if (a.fastest_pace_val < fastestPace.paceVal && a.fastest_pace_val > 2.5) {
          fastestPace = { athlete: a.athlete_name, paceStr: a.fastest_pace_str, paceVal: a.fastest_pace_val, dist: a.max_single_dist };
        }
        if (a.max_single_dist > longestSingle.dist) {
          longestSingle = { athlete: a.athlete_name, dist: a.max_single_dist, sport: Object.keys(a.sports)[0] || 'Sport' };
        }
      });

      const topNightOwl = Object.entries(nightOwls).sort((a, b) => b[1] - a[1])[0] || ['N/A', 0];
      const topEarlyBird = Object.entries(earlyBirds).sort((a, b) => b[1] - a[1])[0] || ['N/A', 0];
      const topWeekend = Object.entries(weekendKms).sort((a, b) => b[1] - a[1])[0] || ['N/A', 0];
      const topDiversity = Object.entries(sportDiversity).sort((a, b) => b[1] - a[1])[0] || ['N/A', 0];
      const topPoints = athletes.sort((a, b) => b.total_points - a.total_points)[0] || { athlete_name: 'N/A', total_points: 0 };

      const trophies = [
        {
          icon: "⚡",
          title: "Speed Demon",
          criteria: "Fastest sustained pace recorded on an outdoor run (>= 2.5 km)",
          holder: fastestPace.athlete,
          stat: fastestPace.paceStr !== 'N/A' ? `${fastestPace.paceStr} pace` : 'Awaiting runs'
        },
        {
          icon: "🦉",
          title: "The Night Owl",
          criteria: "Most workouts logged in the evening after 8:00 PM",
          holder: topNightOwl[0],
          stat: `${topNightOwl[1]} night logs`
        },
        {
          icon: "🌅",
          title: "Dawn Patrol",
          criteria: "Most workouts logged in the early morning before 7:00 AM",
          holder: topEarlyBird[0],
          stat: `${topEarlyBird[1]} sunrise logs`
        },
        {
          icon: "🫁",
          title: "Iron Lungs",
          criteria: "Single longest continuous distance logged in an activity",
          holder: longestSingle.athlete,
          stat: `${(Math.round(longestSingle.dist * 10) / 10).toFixed(1)} km single effort`
        },
        {
          icon: "⚔️",
          title: "Weekend Warrior",
          criteria: "Highest workout volume logged on Saturdays and Sundays",
          holder: topWeekend[0],
          stat: `${topWeekend[1]} weekend sessions`
        },
        {
          icon: "🎯",
          title: "Points Titan",
          criteria: "Overall leader in Dynamic MET points in active window",
          holder: topPoints.athlete_name,
          stat: `${Math.round(topPoints.total_points).toLocaleString()} pts`
        },
        {
          icon: "🧙‍♂️",
          title: "Decathlete Hybrid",
          criteria: "Active across the widest variety of distinct sport disciplines",
          holder: topDiversity[0],
          stat: `${topDiversity[1]} sports logged`
        },
        {
          icon: "🏅",
          title: "Half-Marathoner",
          criteria: "Awarded to any athlete who has crossed the 21.1 km barrier",
          holder: longestSingle.dist >= 21.1 ? longestSingle.athlete : "Open Contender",
          stat: longestSingle.dist >= 21.1 ? `${longestSingle.dist} km logged` : "Target: 21.1 km"
        }
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

    /* Initialize Data Loading */
    async function loadArenaData() {
      const candidateUrls = [
        'dashboard_data.json?t=' + Date.now(),
        './dashboard_data.json?t=' + Date.now(),
        'web/dashboard_data.json?t=' + Date.now(),
        '../dashboard_data.json?t=' + Date.now()
      ];

      for (const url of candidateUrls) {
        try {
          const resp = await fetch(url, { cache: 'no-store' });
          if (resp.ok) {
            globalData = await resp.json();
            initArena();
            return;
          }
        } catch (e) {}
      }

      // Offline fallback
      try {
        const fallbackEl = document.getElementById('fallback-data');
        if (fallbackEl && fallbackEl.textContent.trim()) {
          globalData = JSON.parse(fallbackEl.textContent);
          initArena();
        }
      } catch (err) {
        console.error('Failed to parse embedded data:', err);
      }
    }

    function initArena() {
      if (!globalData) return;
      initDuelSelectors();
      applyFilterAndRerender();
    }

    loadArenaData();
  </script>
</body>
</html>
"""

    full_arena_html = arena_template.replace("<!-- FALLBACK_DATA_PLACEHOLDER -->", json_str)

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
