import os
import json
import shutil

ROOT_DIR = r"C:\Users\ds-ga\Documents\automations\strava club download"
YEAR_DIR = os.path.join(ROOT_DIR, "YEAR2026")
WEB_DIR = os.path.join(ROOT_DIR, "web")
EXPORT_DIR = os.path.join(ROOT_DIR, "export")

# Load dashboard_data.json
json_path = os.path.join(ROOT_DIR, "dashboard_data.json")
if not os.path.exists(json_path):
    json_path = os.path.join(YEAR_DIR, "dashboard_data.json")

with open(json_path, "r", encoding="utf-8") as f:
    dashboard_data = json.load(f)

json_str = json.dumps(dashboard_data, indent=2)

html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  <title>Strava 2026 Club Leaderboard & Analytics</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@500;600;700;800;900&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script>
    (function() {
      try {
        let t = sessionStorage.getItem('strava_theme_manual');
        if (!t) {
          t = Math.random() < 0.5 ? 'obsidian' : 'default';
        }
        if (t === 'obsidian') {
          document.documentElement.classList.add('theme-obsidian');
        }
      } catch(e) {}
    })();
  </script>
  <style>
    :root {
      --bg-dark: #090d16;
      --card-bg: rgba(26, 35, 52, 0.7);
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
      --bronze-glow: rgba(217, 119, 6, 0.3);
      --accent-blue: #38bdf8;
      --accent-green: #22c55e;
      --accent-purple: #a855f7;
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
        radial-gradient(at 0% 0%, rgba(252, 76, 2, 0.14) 0px, transparent 45%),
        radial-gradient(at 100% 100%, rgba(56, 189, 248, 0.09) 0px, transparent 45%),
        radial-gradient(at 50% 30%, rgba(168, 85, 247, 0.04) 0px, transparent 50%);
      color: var(--text-primary);
      min-height: 100vh;
      padding-bottom: 70px;
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
      width: 38px;
      height: 38px;
      background: linear-gradient(135deg, #fc4c02, #ff6a2b);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 16px var(--orange-glow);
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
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 1px;
      font-weight: 600;
    }

    .nav-actions {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }

    /* Schema Selector Pill Group */
    .schema-toggle-group {
      display: inline-flex;
      align-items: center;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 30px;
      padding: 3px;
      box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.4);
    }

    .schema-pill {
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      border: none;
      background: transparent;
      color: var(--text-muted);
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .schema-pill:hover {
      color: #fff;
    }

    .schema-pill.active-dynamic {
      background: linear-gradient(135deg, #fc4c02, #ff6a2b);
      color: #fff;
      box-shadow: 0 0 14px var(--orange-glow);
    }

    .schema-pill.active-legacy {
      background: linear-gradient(135deg, #7c3aed, #a855f7);
      color: #fff;
      box-shadow: 0 0 14px rgba(168, 85, 247, 0.45);
    }

    .sync-badge {
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--card-border);
      padding: 6px 12px;
      border-radius: 20px;
      font-size: 12px;
      color: var(--text-muted);
    }

    .pulse-dot {
      width: 8px;
      height: 8px;
      background: var(--accent-green);
      border-radius: 50%;
      box-shadow: 0 0 8px var(--accent-green);
      animation: pulse 2s infinite;
    }

    @keyframes pulse {
      0% { transform: scale(0.95); opacity: 0.8; }
      50% { transform: scale(1.2); opacity: 1; }
      100% { transform: scale(0.95); opacity: 0.8; }
    }

    .btn {
      padding: 8px 15px;
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

    .btn-orange {
      background: linear-gradient(135deg, #fc4c02, #ff6a2b);
      color: #fff;
      box-shadow: 0 4px 14px var(--orange-glow);
    }
    .btn-orange:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px var(--orange-glow);
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

    /* Main Container */
    .container {
      max-width: 1340px;
      margin: 0 auto;
      padding: 28px 24px;
    }

    /* Schema Notice Banner */
    .schema-banner {
      background: rgba(30, 41, 59, 0.4);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 10px 18px;
      margin-bottom: 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 13px;
      color: var(--text-muted);
    }

    .schema-banner-text strong {
      color: var(--text-primary);
    }

    /* Hero Summary KPIs */
    .hero-summary {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 18px;
      margin-bottom: 36px;
    }

    .summary-card {
      background: var(--card-bg);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid var(--card-border);
      border-radius: 18px;
      padding: 20px 22px;
      position: relative;
      overflow: hidden;
      transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }
    .summary-card:hover {
      transform: translateY(-3px);
      border-color: var(--card-hover-border);
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.35);
    }

    .summary-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 10px;
    }

    .summary-label {
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--text-muted);
    }

    .summary-icon {
      font-size: 20px;
    }

    .summary-value {
      font-family: 'Outfit', sans-serif;
      font-size: 30px;
      font-weight: 800;
      color: var(--text-primary);
      line-height: 1.1;
      margin-bottom: 6px;
    }

    .summary-sub {
      font-size: 12px;
      color: var(--text-dim);
    }

    /* Podium Section */
    .section-title {
      font-family: 'Outfit', sans-serif;
      font-size: 20px;
      font-weight: 800;
      margin-bottom: 18px;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .podium-container {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      margin-bottom: 40px;
    }

    .podium-card {
      background: var(--card-bg);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border-radius: 20px;
      padding: 24px;
      position: relative;
      overflow: hidden;
      text-align: center;
      border: 1px solid var(--card-border);
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      cursor: pointer;
    }
    .podium-card:hover {
      transform: translateY(-6px);
      box-shadow: 0 16px 36px rgba(0, 0, 0, 0.5);
    }

    .podium-card.gold {
      border-color: rgba(251, 191, 36, 0.4);
      background: linear-gradient(180deg, rgba(251, 191, 36, 0.12) 0%, rgba(26, 35, 52, 0.8) 100%);
      box-shadow: 0 0 25px rgba(251, 191, 36, 0.15);
    }
    .podium-card.silver {
      border-color: rgba(203, 213, 225, 0.3);
      background: linear-gradient(180deg, rgba(203, 213, 225, 0.08) 0%, rgba(26, 35, 52, 0.8) 100%);
    }
    .podium-card.bronze {
      border-color: rgba(217, 119, 6, 0.35);
      background: linear-gradient(180deg, rgba(217, 119, 6, 0.1) 0%, rgba(26, 35, 52, 0.8) 100%);
    }

    .podium-badge {
      position: absolute;
      top: 14px;
      right: 14px;
      font-size: 11px;
      font-weight: 800;
      padding: 4px 10px;
      border-radius: 12px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .gold .podium-badge { background: rgba(251, 191, 36, 0.2); color: var(--gold); border: 1px solid rgba(251, 191, 36, 0.4); }
    .silver .podium-badge { background: rgba(203, 213, 225, 0.2); color: var(--silver); border: 1px solid rgba(203, 213, 225, 0.4); }
    .bronze .podium-badge { background: rgba(217, 119, 6, 0.2); color: var(--bronze); border: 1px solid rgba(217, 119, 6, 0.4); }

    .podium-avatar {
      width: 64px;
      height: 64px;
      border-radius: 50%;
      margin: 10px auto 14px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      font-weight: 800;
      color: #fff;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
    }
    .gold .podium-avatar { border: 3px solid var(--gold); box-shadow: 0 0 20px var(--gold-glow); background: linear-gradient(135deg, #d97706, #fbbf24); }
    .silver .podium-avatar { border: 3px solid var(--silver); box-shadow: 0 0 16px var(--silver-glow); background: linear-gradient(135deg, #475569, #94a3b8); }
    .bronze .podium-avatar { border: 3px solid var(--bronze); box-shadow: 0 0 16px var(--bronze-glow); background: linear-gradient(135deg, #78350f, #b45309); }

    .podium-name {
      font-family: 'Outfit', sans-serif;
      font-size: 18px;
      font-weight: 800;
      color: #fff;
      margin-bottom: 6px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .podium-points {
      font-family: 'Outfit', sans-serif;
      font-size: 24px;
      font-weight: 900;
      color: var(--strava-orange);
      margin-bottom: 14px;
    }

    .podium-stats {
      display: flex;
      justify-content: space-around;
      border-top: 1px solid var(--card-border);
      padding-top: 12px;
      font-size: 12px;
      color: var(--text-muted);
    }
    .podium-stat-item {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }
    .podium-stat-val {
      font-weight: 700;
      color: var(--text-primary);
    }

    /* Visualizations Grid */
    .viz-grid {
      display: grid;
      grid-template-columns: 3fr 2fr;
      gap: 20px;
      margin-bottom: 40px;
      align-items: stretch;
    }

    .viz-card {
      background: var(--card-bg);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      width: 100%;
      box-sizing: border-box;
    }

    .viz-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 16px;
      width: 100%;
    }

    .viz-title {
      font-family: 'Outfit', sans-serif;
      font-size: 16px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .viz-badge {
      font-size: 11px;
      color: var(--text-muted);
      background: rgba(255, 255, 255, 0.05);
      padding: 4px 10px;
      border-radius: 12px;
      border: 1px solid var(--card-border);
    }

    .chart-box {
      position: relative;
      flex-grow: 1;
      width: 100%;
      min-height: 290px;
      max-height: 330px;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    .chart-box canvas {
      max-width: 100% !important;
      margin: 0 auto !important;
    }

    .radar-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 14px;
      justify-content: center;
    }

    .radar-pill {
      font-size: 11px;
      padding: 4px 10px;
      border-radius: 12px;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }
    .radar-pill:hover {
      border-color: var(--strava-orange);
    }
    .radar-pill.active {
      background: rgba(255, 255, 255, 0.08);
      font-weight: 700;
    }

    /* Controls Toolbar */
    .controls-bar {
      background: var(--card-bg);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid var(--card-border);
      border-radius: 18px;
      padding: 16px 20px;
      margin-bottom: 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 14px;
    }

    .filter-group {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }

    .search-input {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 8px 14px;
      color: var(--text-primary);
      font-size: 13px;
      width: 220px;
      outline: none;
      transition: border-color 0.2s ease;
    }
    .search-input:focus {
      border-color: var(--strava-orange);
    }

    .select-input {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 8px 14px;
      color: var(--text-primary);
      font-size: 13px;
      outline: none;
      cursor: pointer;
    }
    .select-input:focus {
      border-color: var(--strava-orange);
    }

    .table-bar-meta {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }

    .results-count {
      font-size: 12px;
      color: var(--text-muted);
    }

    .table-scroll-hint {
      display: none;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 600;
      color: var(--strava-orange);
      background: rgba(252, 76, 2, 0.1);
      border: 1px solid rgba(252, 76, 2, 0.25);
      border-radius: 20px;
      padding: 3px 10px;
    }

    @media (max-width: 860px) {
      .table-scroll-hint {
        display: inline-flex;
      }
    }

    /* Leaderboard Table */
    .table-container {
      background: var(--card-bg);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      overflow-x: auto;
      overflow-y: hidden;
      -webkit-overflow-scrolling: touch;
      touch-action: pan-x pan-y;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
      position: relative;
    }

    .table-container::-webkit-scrollbar {
      height: 6px;
    }
    .table-container::-webkit-scrollbar-track {
      background: rgba(15, 23, 42, 0.6);
      border-radius: 0 0 16px 16px;
    }
    .table-container::-webkit-scrollbar-thumb {
      background: #334155;
      border-radius: 4px;
    }
    .table-container::-webkit-scrollbar-thumb:hover {
      background: var(--strava-orange);
    }

    .table-container .data-table {
      min-width: 820px;
    }

    .data-table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
    }

    .data-table th {
      background: rgba(15, 23, 42, 0.9);
      color: var(--text-muted);
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      padding: 14px 18px;
      border-bottom: 1px solid var(--card-border);
      cursor: pointer;
      user-select: none;
      white-space: nowrap;
    }
    .data-table th:hover {
      color: var(--text-primary);
    }

    .data-table td {
      padding: 16px 18px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      font-size: 13px;
      white-space: nowrap;
    }

    .data-table tbody tr {
      transition: background-color 0.15s ease;
      cursor: pointer;
      -webkit-tap-highlight-color: rgba(252, 76, 2, 0.1);
    }
    .data-table tbody tr:hover {
      background-color: rgba(252, 76, 2, 0.06);
    }

    .rank-cell {
      font-family: 'Outfit', sans-serif;
      font-size: 16px;
      font-weight: 800;
      width: 60px;
      min-width: 60px;
    }
    .rank-top1 { color: var(--gold); }
    .rank-top2 { color: var(--silver); }
    .rank-top3 { color: var(--bronze); }

    .athlete-cell {
      display: flex;
      align-items: center;
      gap: 12px;
      min-width: 180px;
    }

    .athlete-badge {
      width: 38px;
      height: 38px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
      font-weight: 800;
      color: #fff;
      flex-shrink: 0;
    }

    .athlete-name {
      font-weight: 700;
      color: var(--text-primary);
    }

    .sport-tags {
      display: flex;
      gap: 4px;
      margin-top: 3px;
    }
    .sport-tag {
      background: rgba(255, 255, 255, 0.06);
      border-radius: 6px;
      padding: 2px 6px;
      font-size: 10px;
      color: var(--text-muted);
    }

    .points-cell {
      font-family: 'Outfit', sans-serif;
      font-size: 16px;
      font-weight: 800;
      color: var(--strava-orange);
    }

    /* Modal Styling */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(5, 8, 15, 0.85);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      z-index: 200;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    .modal-overlay.active {
      display: flex;
    }

    .modal-content {
      background: #0d1322;
      border: 1px solid var(--card-border);
      border-radius: 24px;
      padding: 28px;
      width: 100%;
      max-width: 820px;
      max-height: 90vh;
      overflow-y: auto;
      position: relative;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.7);
    }

    .modal-close {
      position: absolute;
      top: 20px;
      right: 20px;
      background: rgba(255, 255, 255, 0.08);
      border: none;
      border-radius: 50%;
      width: 34px;
      height: 34px;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 18px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s ease;
    }
    .modal-close:hover {
      background: var(--strava-orange);
      color: #fff;
    }

    .modal-athlete-header {
      display: flex;
      align-items: center;
      gap: 18px;
      margin-bottom: 24px;
      border-bottom: 1px solid var(--card-border);
      padding-bottom: 20px;
    }

    .modal-avatar {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      font-weight: 800;
      color: #fff;
      box-shadow: 0 4px 16px rgba(0,0,0,0.5);
    }

    .modal-stat-cards {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      margin-bottom: 24px;
    }

    .modal-stat-card {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 14px;
      text-align: center;
    }

    .modal-stat-label {
      font-size: 11px;
      text-transform: uppercase;
      color: var(--text-muted);
      font-weight: 600;
      margin-bottom: 4px;
    }

    .modal-stat-value {
      font-family: 'Outfit', sans-serif;
      font-size: 18px;
      font-weight: 800;
      color: #fff;
    }

    /* Schema Modal Tabs */
    .schema-tabs {
      display: flex;
      gap: 8px;
      border-bottom: 1px solid var(--card-border);
      margin-bottom: 18px;
      padding-bottom: 8px;
    }

    .schema-tab-btn {
      background: transparent;
      border: 1px solid transparent;
      border-radius: 10px;
      padding: 8px 16px;
      font-size: 13px;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .schema-tab-btn:hover {
      color: var(--text-primary);
      background: rgba(255, 255, 255, 0.05);
    }
    .schema-tab-btn.active {
      background: rgba(252, 76, 2, 0.15);
      border-color: rgba(252, 76, 2, 0.4);
      color: var(--strava-orange);
    }

    .schema-tab-pane {
      display: none;
    }
    .schema-tab-pane.active {
      display: block;
    }

    .formula-card {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(252, 76, 2, 0.25);
      border-radius: 14px;
      padding: 16px 20px;
      margin-bottom: 18px;
    }

    .formula-box {
      font-family: 'Courier New', Courier, monospace;
      font-size: 13px;
      background: rgba(0, 0, 0, 0.35);
      border-radius: 8px;
      padding: 12px 14px;
      color: #38bdf8;
      line-height: 1.6;
      margin: 10px 0;
      border-left: 3px solid var(--strava-orange);
    }

    /* ========================================================
       OBSIDIAN STEALTH THEME & THEME SWITCHER
       ======================================================== */
    .theme-toggle-btn {
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      border: 1px solid rgba(255, 255, 255, 0.12);
      background: rgba(15, 23, 42, 0.7);
      color: var(--text-muted);
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
      user-select: none;
    }
    .theme-toggle-btn:hover {
      background: rgba(30, 41, 59, 0.9);
      color: #fff;
      border-color: rgba(255, 255, 255, 0.25);
      transform: translateY(-1px);
    }

    html.theme-obsidian,
    body.theme-obsidian {
      --bg-dark: #09090b;
      --card-bg: rgba(22, 22, 26, 0.88);
      --card-border: rgba(255, 255, 255, 0.08);
      --card-hover-border: rgba(245, 158, 11, 0.45);
      --strava-orange: #f59e0b;
      --strava-orange-light: #fbbf24;
      --orange-glow: rgba(245, 158, 11, 0.35);
      --text-primary: #f4f4f6;
      --text-muted: #8b8b98;
      --text-dim: #52525c;
      --gold: #f59e0b;
      --gold-glow: rgba(245, 158, 11, 0.35);
      --silver: #94a3b8;
      --silver-glow: rgba(148, 163, 184, 0.25);
      --bronze: #b45309;
      --bronze-glow: rgba(180, 83, 9, 0.3);
      --accent-blue: #38bdf8;
      --accent-green: #10b981;
      --accent-purple: #a855f7;

      background-color: #09090b !important;
      background-image: 
        radial-gradient(circle at 50% 0%, #17171e 0%, #09090b 60%),
        linear-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.015) 1px, transparent 1px) !important;
      background-size: 100% 100%, 40px 40px, 40px 40px !important;
    }

    body.theme-obsidian .navbar {
      background: rgba(14, 14, 18, 0.92);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
    }

    body.theme-obsidian .brand-logo {
      background: #18181c;
      border: 1px solid rgba(255, 255, 255, 0.16);
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.5);
    }

    body.theme-obsidian .brand-title {
      background: linear-gradient(90deg, #ffffff, #e4e4e7);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    body.theme-obsidian .brand-subtitle {
      color: #8b8b98;
    }

    body.theme-obsidian .theme-toggle-btn {
      background: #181820;
      border-color: rgba(245, 158, 11, 0.35);
      color: #f59e0b;
    }
    body.theme-obsidian .theme-toggle-btn:hover {
      background: #242430;
      border-color: #f59e0b;
      box-shadow: 0 0 10px rgba(245, 158, 11, 0.25);
    }

    body.theme-obsidian .schema-toggle-group {
      background: #141418;
      border: 1px solid rgba(255, 255, 255, 0.08);
    }

    body.theme-obsidian .schema-pill.active-dynamic {
      background: #24242e;
      color: #f59e0b;
      border: 1px solid rgba(245, 158, 11, 0.4);
      box-shadow: 0 0 12px rgba(245, 158, 11, 0.25);
    }

    body.theme-obsidian .schema-pill.active-legacy {
      background: #24242e;
      color: #c084fc;
      border: 1px solid rgba(168, 85, 247, 0.4);
      box-shadow: 0 0 12px rgba(168, 85, 247, 0.25);
    }

    body.theme-obsidian .sync-badge {
      background: #141418;
      border: 1px solid rgba(255, 255, 255, 0.08);
      color: #a1a1aa;
    }

    body.theme-obsidian .btn-orange {
      background: linear-gradient(135deg, #d97706, #f59e0b);
      box-shadow: 0 0 14px rgba(245, 158, 11, 0.35);
      color: #09090b;
      font-weight: 700;
    }
    body.theme-obsidian .btn-orange:hover {
      background: linear-gradient(135deg, #f59e0b, #fbbf24);
      box-shadow: 0 0 20px rgba(245, 158, 11, 0.5);
    }

    body.theme-obsidian .btn-outline {
      background: #16161b;
      border-color: rgba(255, 255, 255, 0.08);
      color: #d4d4d8;
    }
    body.theme-obsidian .btn-outline:hover {
      border-color: #f59e0b;
      color: #f59e0b;
    }

    body.theme-obsidian .schema-banner {
      background: #141418;
      border: 1px solid rgba(255, 255, 255, 0.08);
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
    }

    body.theme-obsidian .summary-card {
      background: #16161a;
      border: 1px solid rgba(255, 255, 255, 0.07);
      border-top: 1.5px solid rgba(255, 255, 255, 0.14);
      border-radius: 14px;
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    body.theme-obsidian .summary-card:hover {
      background: #1c1c22;
      border-color: rgba(245, 158, 11, 0.4);
      transform: translateY(-2px);
    }

    body.theme-obsidian .podium-card {
      background: #16161a;
      border: 1px solid rgba(255, 255, 255, 0.07);
      border-top: 1.5px solid rgba(255, 255, 255, 0.14);
      border-radius: 16px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    }
    body.theme-obsidian .podium-card:hover {
      background: #1c1c22;
      transform: translateY(-4px);
    }
    body.theme-obsidian .podium-card.rank-1 {
      border-color: rgba(245, 158, 11, 0.35);
      background: linear-gradient(180deg, rgba(245, 158, 11, 0.08) 0%, #16161a 100%);
      box-shadow: 0 10px 30px rgba(245, 158, 11, 0.12);
    }

    body.theme-obsidian .viz-card {
      background: #16161a;
      border: 1px solid rgba(255, 255, 255, 0.07);
      border-top: 1.5px solid rgba(255, 255, 255, 0.14);
      border-radius: 14px;
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }

    body.theme-obsidian .viz-badge {
      background: #202028;
      border: 1px solid rgba(255, 255, 255, 0.08);
      color: #a1a1aa;
    }

    body.theme-obsidian .radar-pill {
      background: #181820;
      border: 1px solid rgba(255, 255, 255, 0.08);
      color: #a1a1aa;
    }
    body.theme-obsidian .radar-pill:hover {
      color: #fff;
      border-color: rgba(255, 255, 255, 0.2);
    }
    body.theme-obsidian .radar-pill.active {
      background: #272734;
      border-color: #f59e0b;
      color: #f59e0b;
      box-shadow: 0 0 10px rgba(245, 158, 11, 0.2);
    }

    body.theme-obsidian .filter-bar {
      background: #16161a;
      border: 1px solid rgba(255, 255, 255, 0.07);
      border-radius: 14px;
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }

    body.theme-obsidian .filter-input,
    body.theme-obsidian .filter-select {
      background: #111114;
      border: 1px solid rgba(255, 255, 255, 0.09);
      color: #f4f4f6;
    }
    body.theme-obsidian .filter-input:focus,
    body.theme-obsidian .filter-select:focus {
      border-color: #f59e0b;
    }

    body.theme-obsidian .table-container {
      background: #16161a;
      border: 1px solid rgba(255, 255, 255, 0.07);
      border-radius: 14px;
      box-shadow: 0 8px 28px rgba(0, 0, 0, 0.35);
    }

    body.theme-obsidian .data-table th {
      background: #121216;
      border-bottom: 1px solid rgba(255, 255, 255, 0.07);
      color: #8b8b98;
    }

    body.theme-obsidian .data-table td {
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    }

    body.theme-obsidian .data-table tbody tr:hover {
      background: #1c1c22;
    }

    body.theme-obsidian .modal-box {
      background: #131317;
      border: 1px solid rgba(255, 255, 255, 0.12);
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.85);
    }

    body.theme-obsidian .stat-box {
      background: #18181f;
      border: 1px solid rgba(255, 255, 255, 0.07);
    }

    body.theme-obsidian .formula-card {
      background: #18181f;
      border: 1px solid rgba(255, 255, 255, 0.07);
    }

    body.theme-obsidian .formula-code {
      background: #0f0f13;
      border-left: 3px solid #f59e0b;
      color: #f59e0b;
    }

    /* Responsive */
    @media (max-width: 1024px) {
      .hero-summary { grid-template-columns: repeat(3, 1fr); }
      .viz-grid { grid-template-columns: 1fr; justify-items: center; }
      .viz-card { width: 100%; max-width: 600px; margin: 0 auto; }
      .podium-container { grid-template-columns: 1fr; }
    }
    @media (max-width: 768px) {
      .viz-grid { grid-template-columns: 1fr; justify-items: center; }
      .viz-card { width: 100%; max-width: 520px; margin: 0 auto; align-items: center; }
      .viz-header { flex-direction: column; text-align: center; gap: 8px; justify-content: center; }
      .chart-box { min-height: 300px; max-height: 350px; width: 100%; justify-content: center; }
      .radar-pills { justify-content: center; width: 100%; }
    }
    @media (max-width: 640px) {
      .container { padding: 18px 12px; }
      .hero-summary { grid-template-columns: 1fr 1fr; }
      .controls-bar { flex-direction: column; align-items: stretch; gap: 10px; }
      .filter-group { flex-direction: column; align-items: stretch; }
      .search-input { width: 100%; }
      .table-bar-meta { justify-content: space-between; width: 100%; }
      .modal-stat-cards { grid-template-columns: 1fr 1fr; }
      .table-container { border-radius: 14px; }
      .data-table th, .data-table td { padding: 12px 14px; font-size: 12px; }
      .rank-cell { font-size: 14px; width: 50px; min-width: 50px; }
      .athlete-badge { width: 32px; height: 32px; font-size: 12px; }
      .viz-card { max-width: 100%; }
    }
  </style>
</head>
<body>

  <!-- Sticky Navbar -->
  <nav class="navbar">
    <a href="#" class="brand">
      <div class="brand-logo">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="#ffffff"><path d="M15.387 17.944l-2.089-4.116h-3.065L15.387 24l5.15-10.172h-3.066m-7.008-5.599l2.836 5.598h4.172L10.463 0l-7.008 13.828h4.172"/></svg>
      </div>
      <div>
        <div class="brand-title">Connectivity Sports Day 2026</div>
        <div class="brand-subtitle">Official Strava Leaderboard & Analytics</div>
      </div>
    </a>

    <div class="nav-actions">
      <!-- Theme Switcher (Default / Obsidian) -->
      <button id="themeToggleBtn" class="theme-toggle-btn" onclick="toggleTheme()" title="Switch Theme (Default / Obsidian)">
        <span id="themeToggleIcon">🌙</span>
        <span id="themeToggleText">Obsidian</span>
      </button>

      <!-- Interactive Schema Toggle -->
      <div class="schema-toggle-group" title="Switch between Dynamic MET and Legacy 2025 Scoring Systems">
        <button id="schemaBtnDynamic" class="schema-pill active-dynamic" onclick="setScoringSchema('dynamic')">
          <span>⚡</span> Dynamic MET
        </button>
        <button id="schemaBtnLegacy" class="schema-pill" onclick="setScoringSchema('legacy')">
          <span>🏛️</span> Legacy 2025
        </button>
      </div>

      <div class="sync-badge">
        <span class="pulse-dot"></span>
        <span id="lastSyncedText">Synced: Live</span>
      </div>

      <a href="arena.html" class="btn btn-orange" style="box-shadow: 0 0 16px rgba(252, 76, 2, 0.45); text-decoration: none; display: inline-flex; align-items: center; gap: 6px;" title="Enter The Arena: Badges, 1v1 Duels & Challenges">
        <span>⚡</span> The Arena ↗
      </a>

      <button id="schemaBtn" class="btn btn-outline" title="View Points Marking Schema & Rules" onclick="openSchemaModal()">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
        Marking Schema
      </button>

      <button id="exportCsvBtn" class="btn btn-outline" title="Export all activities as CSV">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
        Export CSV
      </button>
    </div>
  </nav>

  <div class="container">

    <!-- Schema Active Banner -->
    <div class="schema-banner">
      <div class="schema-banner-text" id="schemaBannerText">
        <span id="schemaBannerIcon">⚡</span> <strong>Active Scoring System:</strong> <span id="schemaBannerTitle">Dynamic MET Schema</span> — Continuous pace-weighted speed scaling with endurance distance dampening.
      </div>
      <div style="font-size:12px; color:var(--text-dim);">Toggle system anytime in the top navigation</div>
    </div>

    <!-- KPI Summary Cards -->
    <div class="hero-summary">
      <div class="summary-card">
        <div class="summary-header">
          <span class="summary-label">Total Athletes</span>
          <span class="summary-icon">👥</span>
        </div>
        <div id="sumAthletes" class="summary-value">0</div>
        <div class="summary-sub" id="sumAthletesSub">Active in competition</div>
      </div>
      <div class="summary-card">
        <div class="summary-header">
          <span class="summary-label">Total Activities</span>
          <span class="summary-icon">⚡</span>
        </div>
        <div id="sumActivities" class="summary-value">0</div>
        <div class="summary-sub">Logged in 2026</div>
      </div>
      <div class="summary-card">
        <div class="summary-header">
          <span class="summary-label">Total Distance</span>
          <span class="summary-icon">🏃</span>
        </div>
        <div id="sumDistance" class="summary-value">0.0 <span style="font-size: 15px; color: var(--text-muted); font-weight: 600;">km</span></div>
        <div class="summary-sub">Cumulative distance</div>
      </div>
      <div class="summary-card">
        <div class="summary-header">
          <span class="summary-label">Total Duration</span>
          <span class="summary-icon">⏱️</span>
        </div>
        <div id="sumDuration" class="summary-value">0.0 <span style="font-size: 15px; color: var(--text-muted); font-weight: 600;">hrs</span></div>
        <div class="summary-sub">Time spent training</div>
      </div>
      <div class="summary-card" id="sumPointsCard" style="border-color: rgba(252, 76, 2, 0.35);">
        <div class="summary-header">
          <span id="sumPointsLabel" class="summary-label" style="color: var(--strava-orange);">Club Total Points</span>
          <span class="summary-icon">🏆</span>
        </div>
        <div id="sumPoints" class="summary-value" style="color: var(--strava-orange);">0 <span style="font-size: 15px; font-weight: 600;">pts</span></div>
        <div class="summary-sub" id="sumPointsSub">⚡ Dynamic MET Score</div>
      </div>
    </div>

    <!-- Podium Section -->
    <div class="section-title">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fbbf24" stroke-width="2.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
      Top Competitors Podium
    </div>
    <div id="podiumSection" class="podium-container"></div>

    <!-- Visualizations Grid -->
    <div class="viz-grid">
      <!-- Radar Chart -->
      <div class="viz-card">
        <div class="viz-header">
          <div class="viz-title">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fc4c02" stroke-width="2.2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            Multi-Dimensional Athlete Radar
          </div>
          <span class="viz-badge">Top 5 Compared</span>
        </div>
        <div class="chart-box">
          <canvas id="radarChart"></canvas>
        </div>
        <div id="radarPills" class="radar-pills"></div>
      </div>

      <!-- Donut Chart -->
      <div class="viz-card">
        <div class="viz-header">
          <div class="viz-title">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.2"><circle cx="12" cy="12" r="10"></circle><path d="M12 2a10 10 0 0 1 10 10h-10z"></path></svg>
            Points Volume Distribution
          </div>
          <span class="viz-badge" id="donutBadge">Points Breakdown</span>
        </div>
        <div class="chart-box">
          <canvas id="donutChart"></canvas>
        </div>
      </div>
    </div>

    <!-- Filter Controls Bar -->
    <div class="controls-bar">
      <div class="filter-group">
        <input type="text" id="searchInput" class="search-input" placeholder="🔍 Search athlete or sport...">
        <select id="sportFilter" class="select-input">
          <option value="ALL">All Activity Types</option>
        </select>
        <select id="dateFilter" class="select-input">
          <option value="CONTEST" selected>🏆 Contest: Sep 14 - Latest</option>
          <option value="ALL">All Time (September 2026)</option>
          <option value="PAST_7_DAYS">Past 7 Days</option>
          <option value="PAST_14_DAYS">Past 14 Days</option>
          <option value="PAST_20_DAYS">Past 20 Days</option>
          <option value="PAST_30_DAYS">Past 30 Days</option>
          <option value="CUSTOM">Custom Date Range...</option>
        </select>
        <div id="customDateBox" style="display: none; align-items: center; gap: 8px;">
          <input type="date" id="startDateInput" class="select-input" style="padding: 7px 10px;">
          <span style="color: var(--text-dim); font-size: 12px;">to</span>
          <input type="date" id="endDateInput" class="select-input" style="padding: 7px 10px;">
        </div>
        <select id="sortBy" class="select-input">
          <option value="points">Sort: Highest Points</option>
          <option value="distance">Sort: Most Distance</option>
          <option value="duration">Sort: Most Duration</option>
          <option value="activities">Sort: Most Activities</option>
          <option value="name">Sort: Name (A-Z)</option>
        </select>
        <button id="resetFiltersBtn" class="btn btn-outline" style="padding: 7px 12px; font-size: 12px;" title="Reset all filters">Reset</button>
      </div>

      <div class="table-bar-meta">
        <div id="resultsCounter" class="results-count">Showing all athletes</div>
        <div class="table-scroll-hint">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m18 8 4 4-4 4M6 8l-4 4 4 4M2 12h20"/></svg>
          <span>Swipe horizontally for full stats</span>
        </div>
      </div>
    </div>

    <!-- Leaderboard Table -->
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Athlete</th>
            <th>Activities</th>
            <th>Sports</th>
            <th>Distance</th>
            <th>Duration</th>
            <th id="thPoints">Points (⚡ Dynamic)</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody id="leaderboardTbody"></tbody>
      </table>
    </div>

  </div>

  <!-- Athlete Detail Modal -->
  <div id="athleteModal" class="modal-overlay">
    <div class="modal-content">
      <button id="modalClose" class="modal-close" title="Close modal">&times;</button>
      <div id="modalBody"></div>
    </div>
  </div>

  <!-- Marking Schema Modal -->
  <div id="schemaModal" class="modal-overlay">
    <div class="modal-content" style="max-width: 740px; max-height: 88vh; overflow-y: auto;">
      <button id="schemaModalClose" class="modal-close" onclick="closeSchemaModal()" title="Close">&times;</button>
      
      <div style="display:flex; align-items:center; gap:14px; margin-bottom:16px; border-bottom:1px solid var(--card-border); padding-bottom:14px;">
        <div style="width:44px; height:44px; border-radius:12px; background:linear-gradient(135deg, #fc4c02, #ff6a2b); display:flex; align-items:center; justify-content:center; box-shadow:0 0 16px var(--orange-glow); flex-shrink:0;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.5"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"></path><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"></path><path d="M4 22h16"></path><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"></path><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"></path><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"></path></svg>
        </div>
        <div>
          <h2 style="font-family:'Outfit', sans-serif; font-size:22px; font-weight:800; color:#fff; letter-spacing:-0.5px;">Marking Schema & Competition Rules</h2>
          <div style="font-size:12px; color:var(--text-muted); margin-top:2px;">Connectivity Sports Day 2026 • Dual Scoring Architecture</div>
        </div>
      </div>

      <!-- Tabs Navigation -->
      <div class="schema-tabs">
        <button id="tabBtnDynamic" class="schema-tab-btn active" onclick="switchSchemaTab('tabDynamic')">⚡ Dynamic MET Schema (Active)</button>
        <button id="tabBtnLegacy" class="schema-tab-btn" onclick="switchSchemaTab('tabLegacy')">🏛️ Legacy 2025 Schema</button>
        <button id="tabBtnSafeguards" class="schema-tab-btn" onclick="switchSchemaTab('tabSafeguards')">🛡️ Anti-Cheat & Safeguards</button>
        <button id="tabBtnJustifications" class="schema-tab-btn" onclick="switchSchemaTab('tabJustifications')">⚖️ System Rationale & Justifications</button>
      </div>

      <!-- TAB 1: DYNAMIC MET SCHEMA -->
      <div id="tabDynamic" class="schema-tab-pane active">
        
        <!-- Foot Sports Formula Card -->
        <div class="formula-card">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <h3 style="font-family:'Outfit', sans-serif; font-size:15px; font-weight:800; color:var(--strava-orange); text-transform:uppercase; letter-spacing:0.5px;">
              🏃 Running vs 🚶 Walking: Calibrated Sports-Science Dual Engine
            </h3>
            <span style="font-size:11px; background:rgba(252, 76, 2, 0.15); color:var(--strava-orange); padding:2px 8px; border-radius:10px; font-weight:700;">Option 1: Decoupled</span>
          </div>
          <p style="font-size:12.5px; color:var(--text-muted); line-height:1.5; margin-bottom:10px;">
            To maintain sporting parity between outdoor cardio and resistance workouts, <strong>Running</strong> scales with continuous physical velocity ($85 - 115\text{ pts/km}$), while <strong>Walking</strong> is calibrated to a steady baseline of <strong>$35.0\text{ pts/km}$</strong> ($175\text{ pts}$ per $5\text{ km}$ hour). This prevents casual walking commutes from eclipsing dedicated 1-hour gym and strength sessions ($240 - 360\text{ pts}$).
          </p>

          <div style="background:rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.05); border-radius:8px; padding:10px 12px; font-size:12px; font-family:monospace; line-height:1.7; color:var(--text-primary); margin-bottom:10px;">
            <div><strong>🏃 Running Rate:</strong> <code>BaseRate = 30.0 + (7.0 × V)</code> pts/km &nbsp;|&nbsp; <code>w(D) = 1.0 / (1.0 + (D / 12.0))</code></div>
            <div><strong>🚶 Walking Rate:</strong> <strong style="color:var(--accent-blue);">35.0 pts / km</strong> (proportional to 3.3–3.8 METs; duration fallback = 3.0 pts/min)</div>
          </div>

          <!-- Speed Reference Table -->
          <table class="data-table" style="font-size:12px; margin-top:10px;">
            <thead>
              <tr>
                <th>Sport & Effort / Pace</th>
                <th>Velocity</th>
                <th>Effective Rate</th>
                <th>5 km Workout</th>
                <th>Equivalence / Comparison</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>⚡ Fast Tempo Run (4:30 /km)</td>
                <td>13.3 km/h</td>
                <td style="color:var(--accent-green); font-weight:700;">112.1 pts/km</td>
                <td><strong>560 pts</strong></td>
                <td>Top-tier cardiovascular endurance</td>
              </tr>
              <tr>
                <td>🏃 Aerobic Base Run (6:00 /km)</td>
                <td>10.0 km/h</td>
                <td style="color:var(--accent-green); font-weight:700;">95.6 pts/km</td>
                <td><strong>478 pts</strong></td>
                <td>Standard high-MET running baseline</td>
              </tr>
              <tr>
                <td>🏃‍♂️ Easy Recovery Jog (8:00 /km)</td>
                <td>7.5 km/h</td>
                <td style="color:var(--accent-blue); font-weight:700;">83.2 pts/km</td>
                <td><strong>416 pts</strong></td>
                <td>Light aerobic jogging</td>
              </tr>
              <tr style="background:rgba(56,189,248,0.06);">
                <td>🚶 Brisk Walk / Hike (10:00 – 13:00 /km)</td>
                <td>4.6 – 6.0 km/h</td>
                <td style="color:var(--accent-blue); font-weight:700;">35.0 pts/km</td>
                <td><strong>175 pts</strong></td>
                <td>Calibrated below 1-hr Gym (240–360 pts)</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Slow-MET Weekly Frequency Escalator Card -->
        <div class="formula-card" style="border-color: rgba(168, 85, 247, 0.35); background: rgba(168, 85, 247, 0.05); margin-top: 14px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <h3 style="font-family:'Outfit', sans-serif; font-size:15px; font-weight:800; color:var(--accent-purple); text-transform:uppercase; letter-spacing:0.5px;">
              🏋️ Slow-MET Consistency Escalator (Gym, Weights, Yoga, Workout)
            </h3>
            <span style="font-size:11px; background:rgba(168, 85, 247, 0.2); color:var(--accent-purple); padding:2px 8px; border-radius:10px; font-weight:700;">Habit & Dedication Multiplier</span>
          </div>
          <p style="font-size:12.5px; color:var(--text-muted); line-height:1.5; margin-bottom:8px;">
            To welcome new participants and reward dedicated gym regulars, non-distance resistance and studio workouts receive an <strong>escalating weekly consistency multiplier</strong>. Running, swimming, cycling, and walking are strictly outside this system.
          </p>

          <table class="data-table" style="font-size:12px; margin-top:8px; margin-bottom:10px;">
            <thead>
              <tr>
                <th>Active Gym Days in Week</th>
                <th>Multiplier Tier</th>
                <th>Effective Rate</th>
                <th>60-Min Session</th>
                <th>Weekly Cumulative (4x 60m)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Day 1</strong> (Introductory)</td>
                <td><span style="font-weight:700; color:var(--text-muted);">1.00× (Base)</span></td>
                <td>4.0 pts / min (240 /hr)</td>
                <td>240 pts</td>
                <td>240 pts</td>
              </tr>
              <tr>
                <td><strong>Day 2</strong> (Committed)</td>
                <td><span style="font-weight:700; color:var(--accent-blue);">1.10× (+10%)</span></td>
                <td>4.4 pts / min (264 /hr)</td>
                <td>264 pts</td>
                <td>504 pts</td>
              </tr>
              <tr>
                <td><strong>Day 3</strong> (Consistent Regular)</td>
                <td><span style="font-weight:700; color:var(--accent-green);">1.20× (+20%)</span></td>
                <td>4.8 pts / min (288 /hr)</td>
                <td>288 pts</td>
                <td>792 pts</td>
              </tr>
              <tr>
                <td><strong>Day 4+</strong> (Iron Discipline)</td>
                <td><span style="font-weight:700; color:var(--gold);">1.30× (+30%)</span></td>
                <td>5.2 pts / min (312 /hr)</td>
                <td>312 pts</td>
                <td><strong>1,104 pts</strong></td>
              </tr>
            </tbody>
          </table>

          <div style="font-size:11.5px; color:var(--text-dim); line-height:1.4;">
            🛡️ <em>Integrity Controls:</em> Qualifying session threshold is &ge; 25 minutes moving time. At most <strong>1 credit per calendar day</strong> increments the weekly tier (multiple sessions on the same day receive points at that day's tier but do not double-advance the streak).
          </div>
        </div>

        <!-- Cyclist Cohort Percentile Card -->
        <div class="formula-card" style="border-color: rgba(56, 189, 248, 0.35); background: rgba(56, 189, 248, 0.05); margin-top: 14px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <h3 style="font-family:'Outfit', sans-serif; font-size:15px; font-weight:800; color:var(--accent-blue); text-transform:uppercase; letter-spacing:0.5px;">
              🚴 Outdoor Cycling Percentile Engine (Commute Normalization)
            </h3>
            <span style="font-size:11px; background:rgba(56, 189, 248, 0.2); color:var(--accent-blue); padding:2px 8px; border-radius:10px; font-weight:700;">Cohort Empirical CDF</span>
          </div>
          <p style="font-size:12.5px; color:var(--text-muted); line-height:1.5; margin-bottom:8px;">
            Because mechanical gear ratios allow casual 5 km bike commutes to effortlessly rack up points, total cycling score is normalized by placing cumulative distance on the <strong>empirical percentile rank (P) of all club cyclists</strong> (derived from 213+ historical and current rides).
          </p>

          <div class="formula-box">
            <div><strong>1. 100th Percentile Ceiling:</strong> <code>Ceiling = 25.0 pts/km × Max All-Time Cyclist km (335.80) × Factor (0.10) = 839.5 pts</code></div>
            <div><strong>2. Empirical Percentile:</strong> <code>P = (Rank in All-Time Cyclist Cohort / N) × 100%</code></div>
            <div><strong>3. Cycling Score:</strong> <code>Total Cycling Pts = min(Distance × 25.0, Ceiling × P)</code></div>
            <div><strong>4. Per-Ride Allocation:</strong> Apportioned proportionally by distance: <code>Ride Pts = Ride Distance × (Total Cycling Pts / Total Distance)</code></div>
          </div>
        </div>

        <!-- All Sports Table -->
        <div style="margin-bottom:20px; margin-top: 14px;">
          <h3 style="font-family:'Outfit', sans-serif; font-size:14px; font-weight:700; color:#fff; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:10px;">
            Cross-Sport Caloric Effort Ratios
          </h3>
          <table class="data-table" style="font-size:12.5px;">
            <thead>
              <tr>
                <th>Sport</th>
                <th>Unit / Basis</th>
                <th>Multiplier / Scoring</th>
                <th>Equivalence / Rationale</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><span style="font-weight:600;">🏃 Running / Trail Run</span></td>
                <td>Distance (GPS)</td>
                <td style="color:var(--accent-green); font-weight:700;">69 – 113 pts / km</td>
                <td>Continuous pace function: Recovery (~8:00/km) ~70 pts/km; Aerobic base (~6:00/km) ~86 pts/km; Fast tempo (~4:25/km) ~113 pts/km</td>
              </tr>
              <tr>
                <td><span style="font-weight:600;">🚶 Walking / Hike</span></td>
                <td>Distance (GPS)</td>
                <td style="color:var(--accent-blue); font-weight:700;">35 pts / km</td>
                <td>Calibrated Option 1 baseline (3.3–3.8 METs; 1-hr walk ~175 pts &lt; 1-hr gym = 240 pts)</td>
              </tr>
              <tr>
                <td><span style="font-weight:600;">🚴 Outdoor Cycling</span></td>
                <td>Distance (GPS)</td>
                <td style="color:var(--accent-blue); font-weight:700;">Cohort Percentile (P)</td>
                <td>Ceiling = 839.5 pts. Commute rides normalized; long endurance rides honored.</td>
              </tr>
              <tr>
                <td>
                  <span style="font-weight:600;">🚴‍♂️ Indoor / Stationary Ride</span>
                  <span style="background:rgba(56,189,248,0.15); color:var(--accent-blue); padding:1px 5px; border-radius:4px; font-size:10px; margin-left:4px;">Indoor</span>
                </td>
                <td>Duration (Time)</td>
                <td style="color:var(--accent-blue); font-weight:700;">4 pts / min (240 /hr)</td>
                <td>Stationary cardio effort without GPS distance</td>
              </tr>
              <tr>
                <td><span style="font-weight:600;">🏋️ Weight Training / Gym / Workout / Yoga</span></td>
                <td>Duration (Time)</td>
                <td style="color:var(--accent-purple); font-weight:700;">4 – 7 pts / min (240 – 420 /hr)</td>
                <td>Cardio & resistance session with escalating weekly consistency multiplier (1.0x &rarr; 1.75x)</td>
              </tr>
              <tr>
                <td><span style="font-weight:600;">🏊 Swimming</span></td>
                <td>Duration or Pace (100m)</td>
                <td style="color:var(--accent-blue); font-weight:700;">5 pts / min or 250 – 450 pts / km</td>
                <td>High-MET dense full-body cardiovascular workout</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div style="background:rgba(252,76,2,0.08); border:1px solid rgba(252,76,2,0.25); border-radius:12px; padding:12px 16px; font-size:12.5px; color:var(--text-primary); margin-bottom:16px;">
          <strong style="color:var(--strava-orange);">🔥 Uncapped Dedication Policy:</strong> Absolutely NO daily point caps! Morning sessions, evening workouts, and weekend endurance challenges count 100% towards your rank.
        </div>

      </div>

      <!-- TAB 2: LEGACY 2025 SCHEMA -->
      <div id="tabLegacy" class="schema-tab-pane">
        <div style="margin-bottom:18px;">
          <p style="font-size:13px; color:var(--text-muted); line-height:1.6; margin-bottom:14px;">
            The <strong>Legacy 2025 Schema</strong> is the historical fixed-multiplier system used in previous club competitions. It is retained for full historical continuity and direct comparative transparency via the toggle above.
          </p>

          <table class="data-table" style="font-size:13px; margin-bottom:16px;">
            <thead>
              <tr>
                <th>Sport</th>
                <th>Unit</th>
                <th>Fixed Multiplier</th>
                <th>Example</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>🏃 Running / Trail Run</td>
                <td>Distance</td>
                <td style="color:var(--accent-green); font-weight:700;">120 pts / km</td>
                <td>10 km = 1,200 pts</td>
              </tr>
              <tr>
                <td>🚶 Walking / Hiking</td>
                <td>Distance</td>
                <td style="color:var(--accent-green); font-weight:700;">100 pts / km</td>
                <td>5 km = 500 pts</td>
              </tr>
              <tr>
                <td>🚴 Outdoor Cycling</td>
                <td>Distance</td>
                <td style="color:var(--accent-blue); font-weight:700;">40 pts / km</td>
                <td>20 km = 800 pts</td>
              </tr>
              <tr>
                <td>🚴‍♂️ Indoor Ride / Trainer</td>
                <td>Duration</td>
                <td style="color:var(--accent-blue); font-weight:700;">10 pts / min</td>
                <td>60 min = 600 pts</td>
              </tr>
              <tr>
                <td>🏋️ Gym / Weight Training</td>
                <td>Duration</td>
                <td style="color:var(--accent-purple); font-weight:700;">10 pts / min</td>
                <td>60 min = 600 pts</td>
              </tr>
              <tr>
                <td>🏊 Swimming</td>
                <td>Duration</td>
                <td style="color:var(--accent-blue); font-weight:700;">10 pts / min</td>
                <td>30 min = 300 pts</td>
              </tr>
            </tbody>
          </table>

          <div style="background:rgba(168,85,247,0.1); border:1px solid rgba(168,85,247,0.3); border-radius:12px; padding:14px; font-size:12px; color:var(--text-primary); line-height:1.6;">
            <strong>💡 Why we upgraded to Dynamic MET in 2026:</strong> Fixed multipliers created self-labeling friction (e.g. runners logging walks to test points, or power-walkers missing pace rewards) and caused stationary duration points to severely outpace high-intensity outdoor efforts. The Dynamic MET model resolves all these discrepancies scientifically.
          </div>
        </div>
      </div>

      <!-- TAB 3: ANTI-CHEAT & SAFEGUARDS -->
      <div id="tabSafeguards" class="schema-tab-pane">
        <div style="font-size:13px; color:var(--text-muted); line-height:1.6;">
          <h4 style="font-size:14px; font-weight:700; color:#fff; margin-bottom:12px; display:flex; align-items:center; gap:8px;">
            <span style="color:var(--accent-green);">🛡️</span> Automated Integrity Controls & Anomaly Filters
          </h4>
          <ul style="padding-left:18px; margin-bottom:18px; display:flex; flex-direction:column; gap:10px;">
            <li>
              <strong style="color:#fff;">Strict Moving Time Policy:</strong>
              Scoring is strictly bound to active moving time. Pauses at traffic lights or rest stops never accrue unearned points.
            </li>
            <li>
              <strong style="color:#fff;">Forgotten Watch Timer Defense:</strong>
              An automated boundary filter catches activities where timers were accidentally left running for hours (e.g. a 35-hour swim timer is clamped to realistic human athletic limits).
            </li>
            <li>
              <strong style="color:#fff;">Activity Ownership Deduplication:</strong>
              When multiple athletes participate in a group activity or tag each other, the pipeline verifies genuine club membership and awards points strictly to the genuine recording athlete.
            </li>
            <li>
              <strong style="color:#fff;">Automated Incomplete Data Recovery:</strong>
              If an activity is recorded with distance but a 0-duration glitch occurred, calibrated median pacing automatically restores moving time without penalizing the athlete.
            </li>
            <li>
              <strong style="color:#fff;">Pace Tracking:</strong>
              Recorded and displayed in standard <code>MM:SS /km</code> format for all foot workouts.
            </li>
          </ul>
        </div>
      </div>

      <!-- TAB 4: JUSTIFICATIONS & RATIONALE -->
      <div id="tabJustifications" class="schema-tab-pane">
        <div style="display:flex; flex-direction:column; gap:16px;">
          
          <!-- Justification 1: Slow-MET Consistency -->
          <div class="formula-card" style="border-color: rgba(168, 85, 247, 0.4); background: rgba(168, 85, 247, 0.06); padding: 18px 20px;">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
              <span style="font-size:22px;">🏋️</span>
              <div>
                <h3 style="font-family:'Outfit', sans-serif; font-size:16px; font-weight:800; color:var(--accent-purple); margin:0;">
                  Why Gym & Slow-MET Activities Receive a Weekly Consistency Escalator
                </h3>
                <div style="font-size:11.5px; color:var(--text-muted); margin-top:2px;">Addressing the Resistance Training Dilemma & Onboarding Fairness</div>
              </div>
            </div>

            <div style="font-size:12.8px; color:var(--text-muted); line-height:1.6; display:flex; flex-direction:column; gap:10px;">
              <div>
                <strong style="color:#fff;">1. The Problem with Raw Duration in Strength Training:</strong><br>
                Resistance training, HIIT, and gym workouts impose intense physiological and muscular strain, but yield zero GPS distance. Under a flat duration rate of 240 pts/hr, an intense 60-minute weight session yielded only 240 points—barely more than a quick 20-minute casual bike ride or a short jog. This created a severe onboarding barrier for non-runners and penalized athletes whose primary fitness journey is strength-focused.
              </div>
              <div>
                <strong style="color:#fff;">2. Physiological Adaptation through Habitual Regularity:</strong><br>
                Unlike running where score grows with distance, resistance training adaptations (muscle hypertrophy, neuromuscular recruitment, metabolic conditioning) depend critically on <em>weekly regularity</em> (3 to 5 sessions per week). By introducing an escalating weekly frequency multiplier (1.00&times; &rarr; 1.25&times; &rarr; 1.50&times; &rarr; 1.75&times;), the system directly rewards dedication, discipline, and habit formation, allowing a committed 4-day-per-week gym athlete to earn 1,320 points and remain competitive with 5K/10K base runners.
              </div>
              <div>
                <strong style="color:#fff;">3. Why Running, Swimming, and Cycling are Excluded:</strong><br>
                Running, swimming, and cycling already possess continuous physical speed and distance equations where effort is organically captured per kilometer. Layering consistency bonuses on top of high-MET cardio would lead to exponential score runaway, destroying cross-sport parity.
              </div>
            </div>
          </div>

          <!-- Justification 2: Cycling Percentile -->
          <div class="formula-card" style="border-color: rgba(56, 189, 248, 0.4); background: rgba(56, 189, 248, 0.06); padding: 18px 20px;">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
              <span style="font-size:22px;">🚴</span>
              <div>
                <h3 style="font-family:'Outfit', sans-serif; font-size:16px; font-weight:800; color:var(--accent-blue); margin:0;">
                  Why Cycling Uses an All-Time Cohort Percentile Ceiling
                </h3>
                <div style="font-size:11.5px; color:var(--text-muted); margin-top:2px;">Eliminating Commute Distortions While Honoring True Endurance Distance</div>
              </div>
            </div>

            <div style="font-size:12.8px; color:var(--text-muted); line-height:1.6; display:flex; flex-direction:column; gap:10px;">
              <div>
                <strong style="color:#fff;">1. The Commute Inflation Distortion:</strong><br>
                Bicycles are mechanically geared vehicles with rolling friction coefficients under 0.005. A relaxed 5 km commute requires negligible metabolic exertion (~20 minutes of leisurely spinning), yet at a flat 25 pts/km, it yielded 125&ndash;150 points. A few daily errands effortlessly outscored grueling 60-minute workouts or 5 km runs. Conversely, massive 70&ndash;100 km weekend rides generated 1,700&ndash;2,500+ points in a single morning, overpowering the entire multi-sport leaderboard.
              </div>
              <div>
                <strong style="color:#fff;">2. Real Community Empirical Benchmark:</strong><br>
                Rather than inventing an arbitrary flat distance cap, our pipeline analyzed the club's all-time historical archive of <strong>213 rides and 15+ cyclists</strong>. In this community, the median ride is 3.1 km, and the 75th percentile is 5.1 km. By grounding the percentile rank in this empirical cohort, the system accurately distinguishes between everyday utility commutes and exceptional endurance cycling.
              </div>
              <div>
                <strong style="color:#fff;">3. The 100th Percentile Ceiling Formula:</strong><br>
                <code>Ceiling = 25.0 pts/km &times; Max All-Time Cyclist km (335.80) &times; Factor (0.10) = 839.5 pts</code><br>
                An athlete's total cycling volume is scaled by their percentile position P, ensuring that routine 5 km commute rides stay in a balanced range (~80&ndash;95 pts) while an epic 70+ km ride is rewarded with a substantial score (~690 pts) without breaking the multi-sport competition.
              </div>
            </div>
          </div>

          <!-- Justification 3: Walking Calibration & Activity Share Audit -->
          <div class="formula-card" style="border-color: rgba(245, 158, 11, 0.4); background: rgba(245, 158, 11, 0.06); padding: 18px 20px;">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
              <span style="font-size:22px;">🚶</span>
              <div>
                <h3 style="font-family:'Outfit', sans-serif; font-size:16px; font-weight:800; color:var(--gold); margin:0;">
                  Why Walking Rates Are Calibrated (35 pts/km) & Activity Share Audit
                </h3>
                <div style="font-size:11.5px; color:var(--text-muted); margin-top:2px;">Aligning Caloric Expenditure, True METs, & Cross-Sport Fairness</div>
              </div>
            </div>

            <div style="font-size:12.8px; color:var(--text-muted); line-height:1.6; display:flex; flex-direction:column; gap:12px;">
              <div>
                <strong style="color:#fff;">1. Empirical Competition-Wide Audit:</strong><br>
                A forensic analysis of all club activities across the competition window revealed an acute mathematical imbalance between low-intensity walking and high-strain resistance training:
              </div>

              <!-- Required Audit Table -->
              <table class="data-table" style="font-size:12px; margin-top:4px; margin-bottom:6px;">
                <thead>
                  <tr>
                    <th>Sport Type</th>
                    <th>Total Club Hours</th>
                    <th>Total Points</th>
                    <th>Effective Pts / Hour</th>
                    <th>True Physiological METs</th>
                    <th>Balance Assessment</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>🏊 Swim</strong></td>
                    <td>3.9 hrs</td>
                    <td>3,199 pts</td>
                    <td><strong>827.3 pts/hr</strong></td>
                    <td>8.0 &ndash; 10.0</td>
                    <td><span style="color:var(--accent-blue); font-weight:600;">High aerobic exertion</span></td>
                  </tr>
                  <tr>
                    <td><strong>🏃 Run</strong></td>
                    <td>41.9 hrs</td>
                    <td>32,438 pts</td>
                    <td><strong>774.4 pts/hr</strong></td>
                    <td>9.8 &ndash; 11.5</td>
                    <td><span style="color:var(--accent-green); font-weight:600;">High aerobic exertion</span></td>
                  </tr>
                  <tr style="background:rgba(239,68,68,0.08);">
                    <td><strong>🚶 Walk (Uncalibrated Baseline)</strong></td>
                    <td>27.7 hrs</td>
                    <td>11,681 pts</td>
                    <td><strong>421.3 pts/hr</strong></td>
                    <td>3.3 &ndash; 3.8</td>
                    <td><span style="color:#f87171; font-weight:700;">Severe Over-rewarding (+55% vs Gym)</span></td>
                  </tr>
                  <tr>
                    <td><strong>🤸 Studio / HIIT</strong></td>
                    <td>11.3 hrs</td>
                    <td>3,216 pts</td>
                    <td><strong>285.2 pts/hr</strong></td>
                    <td>6.0 &ndash; 8.0</td>
                    <td><span style="color:var(--accent-purple); font-weight:600;">Moderate / High anaerobic</span></td>
                  </tr>
                  <tr>
                    <td><strong>🏋️ Weight Training (Gym)</strong></td>
                    <td>11.7 hrs</td>
                    <td>3,158 pts</td>
                    <td><strong>270.9 pts/hr</strong></td>
                    <td>4.5 &ndash; 6.0</td>
                    <td><span style="color:var(--accent-purple); font-weight:600;">Resistance & muscular strain</span></td>
                  </tr>
                  <tr>
                    <td><strong>🚴 Ride (Cycling)</strong></td>
                    <td>8.3 hrs</td>
                    <td>1,874 pts</td>
                    <td><strong>224.5 pts/hr</strong></td>
                    <td>4.0 &ndash; 6.5</td>
                    <td><span style="color:var(--accent-blue); font-weight:600;">Reined in by Percentile Ceiling</span></td>
                  </tr>
                </tbody>
              </table>

              <div>
                <strong style="color:#fff;">2. The Physiological Reality:</strong><br>
                Under the uncalibrated unified foot-sports equation, a casual 1-hour walk (covering ~5.5 km) generated <strong>421.3 points</strong>, easily eclipsing an intense 1-hour heavy weight training session (240&ndash;300 pts) despite walking having a substantially lower metabolic demand (3.3&ndash;3.8 METs vs 4.5&ndash;6.0 METs). This discouraged gym participants and created a distortion where non-running, non-gym members climbed into top leaderboard spots purely through routine walking.
              </div>

              <div>
                <div>
                  <strong style="color:#fff;">3. The Calibrated Solution (Option 1):</strong><br>
                  Walking is decoupled from running and calibrated to a steady rate of <strong>35.0 pts / km</strong> (~175 pts for an hour-long 5 km walk). This ensures:
                  <ul style="padding-left:18px; margin-top:4px;">
                    <li>1 hour of walking (~175 pts) properly sits below 1 hour of gym training (240&ndash;360 pts).</li>
                    <li>1 hour of hard running (750+ pts) remains the premier high-MET cardiovascular activity.</li>
                    <li>Daily walking is still recognized and encouraged, but cannot overshadow intense multi-sport disciplines.</li>
                  </ul>
                </div>

                <!-- Post-Calibration New Points Table -->
                <div style="margin-top:10px;">
                  <strong style="color:#fff;">4. Post-Calibration Live Audit: New Points & Balance per Activity:</strong><br>
                  <div style="font-size:12px; color:var(--text-muted); margin-bottom:6px; margin-top:2px;">
                    Empirical results measured across all club activities under the active calibrated Dynamic MET scoring engine:
                  </div>
                  <table class="data-table" style="font-size:12px; margin-top:4px; margin-bottom:6px;">
                    <thead>
                      <tr>
                        <th>Sport Type</th>
                        <th>Activities</th>
                        <th>Total Club Hours</th>
                        <th>Total Dynamic Points</th>
                        <th>Effective Pts / Hour</th>
                        <th>Benchmark Unit Rate</th>
                        <th>Equilibrium & Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td><strong>🏊 Swim</strong></td>
                        <td>7 acts</td>
                        <td>3.9 hrs</td>
                        <td>3,199 pts</td>
                        <td style="color:var(--accent-blue); font-weight:700;">827.3 pts/hr</td>
                        <td>~13.8 pts/min (or pace/100m)</td>
                        <td><span style="color:var(--accent-blue); font-weight:600;">Premier full-body aerobic MET</span></td>
                      </tr>
                      <tr>
                        <td><strong>🏃 Run</strong></td>
                        <td>55 acts</td>
                        <td>47.9 hrs</td>
                        <td>33,105 pts</td>
                        <td style="color:var(--accent-green); font-weight:700;">691.5 pts/hr</td>
                        <td>~86 pts/km base (69–113 pts/km)</td>
                        <td><span style="color:var(--accent-green); font-weight:600;">Premier cardio endurance</span></td>
                      </tr>
                      <tr>
                        <td><strong>🤸 Studio / Workout (HIIT)</strong></td>
                        <td>13 acts</td>
                        <td>16.3 hrs</td>
                        <td>4,410 pts</td>
                        <td style="color:var(--accent-purple); font-weight:700;">270.0 pts/hr</td>
                        <td>4.5 pts/min</td>
                        <td><span style="color:var(--accent-purple); font-weight:600;">High anaerobic density</span></td>
                      </tr>
                      <tr>
                        <td><strong>🏋️ Weight Training (Gym)</strong></td>
                        <td>14 acts</td>
                        <td>13.5 hrs</td>
                        <td>3,411 pts</td>
                        <td style="color:var(--accent-purple); font-weight:700;">252.2 pts/hr</td>
                        <td>4.0–5.2 pts/min (with weekly escalator)</td>
                        <td><span style="color:var(--accent-purple); font-weight:600;">Rewards habitual consistency</span></td>
                      </tr>
                      <tr>
                        <td><strong>🚴 Ride (Cycling)</strong></td>
                        <td>15 acts</td>
                        <td>8.9 hrs</td>
                        <td>1,973 pts</td>
                        <td style="color:var(--accent-blue); font-weight:700;">221.9 pts/hr</td>
                        <td>Cohort Percentile Engine (Ceiling 839.5)</td>
                        <td><span style="color:var(--accent-blue); font-weight:600;">Commute inflation eliminated</span></td>
                      </tr>
                      <tr style="background:rgba(34,197,94,0.08); border-left:3px solid var(--accent-green);">
                        <td><strong>🚶 Walk (Calibrated Baseline)</strong></td>
                        <td>70 acts</td>
                        <td>34.3 hrs</td>
                        <td>6,341 pts</td>
                        <td style="color:var(--accent-green); font-weight:700;">184.9 pts/hr</td>
                        <td>35.0 pts/km (duration fallback 3.0/m)</td>
                        <td><span style="color:var(--accent-green); font-weight:700;">Balanced below Gym (185 &lt; 252 pts/hr)</span></td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

          <!-- Justification 4: Automated Integrity & Anomaly Filtering Engine -->
          <div class="formula-card" style="border-color: rgba(239, 68, 68, 0.4); background: rgba(239, 68, 68, 0.06); padding: 18px 20px;">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
              <span style="font-size:22px;">🛡️</span>
              <div>
                <h3 style="font-family:'Outfit', sans-serif; font-size:16px; font-weight:800; color:#f87171; margin:0;">
                  Automated Activity Integrity & Anomaly Filtering Engine
                </h3>
                <div style="font-size:11.5px; color:var(--text-muted); margin-top:2px;">Protecting Competition Fairness from GPS Multipath Glitches & Sport Mislabeling</div>
              </div>
            </div>

            <div style="font-size:12.8px; color:var(--text-muted); line-height:1.6; display:flex; flex-direction:column; gap:10px;">
              <div>
                <strong style="color:#fff;">1. Mislabeled Walk Pace Normalization:</strong><br>
                When a workout is recorded as a "Walk" but exhibits physical velocities &gt; 8.6 km/h (&lt; 7:00 /km pace, indicative of running or cycling), the pipeline automatically ignores the inflated distance and re-estimates the true distance based on the athlete's validated median walking pace multiplied by moving time.
              </div>
              <div>
                <strong style="color:#fff;">2. Sensor Spike & Elite Pace Auto-Nerf:</strong><br>
                GPS multipath drift, indoor signal jumps, or bicycle rides miscategorized as runs can generate improbable speeds. Any run at &lt; 4:15 /km (or long runs &ge; 10 km at &lt; 5:00 /km) is flagged as an anomaly or potential bike ride and auto-normalized to realistic tempo baselines (&ge; 4:39 /km for short, &ge; 5:20 /km for 10k+), ensuring points reflect authentic physical exertion.
              </div>
              <div>
                <strong style="color:#fff;">3. Motorized Velocity Suppression:</strong><br>
                Any foot activity logged with sustained velocity &gt; 18 km/h (&lt; 3:20 /km pace, exceeding human aerobic thresholds) is automatically flagged for vehicle transit and normalized to duration-based median walking pace.
              </div>
            </div>
          </div>

        </div>
      </div>

      <div style="text-align:right; border-top:1px solid var(--card-border); padding-top:14px;">
        <button class="btn btn-orange" onclick="closeSchemaModal()" style="padding:7px 20px; font-size:12px;">Close</button>
      </div>
    </div>
  </div>

  <!-- Fallback Embedded Data -->
  <script id="fallback-data" type="application/json">
<!-- FALLBACK_DATA_PLACEHOLDER -->
  </script>

  <script>
    let globalData = null;
    let filteredAthletes = [];
    let currentFilteredActivities = [];
    let radarChartInstance = null;
    let donutChartInstance = null;
    let selectedRadarAthleteIds = new Set();
    let currentSchema = localStorage.getItem('strava_scoring_schema') || 'dynamic';
    let currentTheme = 'default';
    let lastSportBreakdown = null;
    let lastTotalSportPoints = 0;
    let lastFilteredAthletes = null;

    const SPORT_ICONS = {
      'Run': '🏃',
      'Trail Run': '🏃',
      'Ride': '🚴',
      'Virtual Ride': '🚴',
      'EBike Ride': '⚡',
      'Walk': '🚶',
      'Hike': '🥾',
      'Weight Training': '🏋️',
      'Workout': '💪',
      'Swim': '🏊',
      'Yoga': '🧘',
      'Badminton': '🏸',
      'Cricket': '🏏',
      'Tennis': '🎾',
      'Table Tennis': '🏓',
      'Football': '⚽',
      'Soccer': '⚽',
      'Basketball': '🏀',
      'Rowing': '🚣',
      'Default': '⚡'
    };

    function getSportIcon(type) {
      return SPORT_ICONS[type] || SPORT_ICONS['Default'];
    }

    function getAvatarColor(name) {
      const colors = [
        'linear-gradient(135deg, #fc4c02, #ff6a2b)',
        'linear-gradient(135deg, #0284c7, #38bdf8)',
        'linear-gradient(135deg, #059669, #34d399)',
        'linear-gradient(135deg, #7c3aed, #a855f7)',
        'linear-gradient(135deg, #d97706, #fbbf24)',
        'linear-gradient(135deg, #e11d48, #fb7185)'
      ];
      let hash = 0;
      for (let i = 0; i < name.length; i++) {
        hash = name.charCodeAt(i) + ((hash << 5) - hash);
      }
      return colors[Math.abs(hash) % colors.length];
    }

    function switchSchemaTab(tabId) {
      document.querySelectorAll('.schema-tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.schema-tab-pane').forEach(pane => pane.classList.remove('active'));

      if (tabId === 'tabDynamic') {
        document.getElementById('tabBtnDynamic').classList.add('active');
        document.getElementById('tabDynamic').classList.add('active');
      } else if (tabId === 'tabLegacy') {
        document.getElementById('tabBtnLegacy').classList.add('active');
        document.getElementById('tabLegacy').classList.add('active');
      } else if (tabId === 'tabSafeguards') {
        document.getElementById('tabBtnSafeguards').classList.add('active');
        document.getElementById('tabSafeguards').classList.add('active');
      } else if (tabId === 'tabJustifications') {
        document.getElementById('tabBtnJustifications').classList.add('active');
        document.getElementById('tabJustifications').classList.add('active');
      }
    }

    function initTheme() {
      let manual = null;
      try {
        manual = sessionStorage.getItem('strava_theme_manual');
      } catch (e) {}

      if (manual === 'default' || manual === 'obsidian') {
        currentTheme = manual;
      } else {
        // Randomly load either Obsidian or Current Default with 50/50 probability
        currentTheme = Math.random() < 0.5 ? 'obsidian' : 'default';
      }
      applyTheme(currentTheme, false);
    }

    function toggleTheme() {
      const next = currentTheme === 'obsidian' ? 'default' : 'obsidian';
      try {
        sessionStorage.setItem('strava_theme_manual', next);
      } catch (e) {}
      applyTheme(next, true);
    }

    function applyTheme(theme, reRenderCharts = false) {
      currentTheme = theme;
      const isObs = theme === 'obsidian';
      document.documentElement.classList.toggle('theme-obsidian', isObs);
      document.body.classList.toggle('theme-obsidian', isObs);

      const icon = document.getElementById('themeToggleIcon');
      const text = document.getElementById('themeToggleText');
      const btn = document.getElementById('themeToggleBtn');

      if (btn && icon && text) {
        if (isObs) {
          icon.innerText = '⚡';
          text.innerText = 'Default';
          btn.title = 'Theme: Obsidian Stealth (Click to switch to Default)';
        } else {
          icon.innerText = '🌙';
          text.innerText = 'Obsidian';
          btn.title = 'Theme: Classic Default (Click to switch to Obsidian)';
        }
      }

      if (reRenderCharts) {
        if (donutChartInstance && lastSportBreakdown) {
          renderDonutChart(lastSportBreakdown, lastTotalSportPoints);
        }
        if (radarChartInstance && lastFilteredAthletes) {
          renderRadarSection(lastFilteredAthletes);
        }
      }
    }

    function setScoringSchema(mode) {
      currentSchema = mode;
      localStorage.setItem('strava_scoring_schema', mode);
      updateSchemaButtons();
      applyFilters();
      if (document.getElementById('athleteModal').classList.contains('active')) {
        const aid = window.location.hash.replace('#athlete=', '');
        if (aid) openAthleteModal(aid);
      }
    }

    function updateSchemaButtons() {
      const btnDyn = document.getElementById('schemaBtnDynamic');
      const btnLeg = document.getElementById('schemaBtnLegacy');
      const bannerTitle = document.getElementById('schemaBannerTitle');
      const bannerText = document.getElementById('schemaBannerText');
      const sumPointsLabel = document.getElementById('sumPointsLabel');
      const sumPointsSub = document.getElementById('sumPointsSub');
      const sumPointsCard = document.getElementById('sumPointsCard');
      const thPoints = document.getElementById('thPoints');

      if (currentSchema === 'legacy') {
        btnDyn.className = 'schema-pill';
        btnLeg.className = 'schema-pill active-legacy';
        if (bannerTitle) bannerTitle.innerText = 'Legacy 2025 Schema';
        if (bannerText) bannerText.innerHTML = '<span>🏛️</span> <strong>Active Scoring System:</strong> <span>Legacy 2025 Schema</span> — Fixed unit rates (Run 120, Walk 100, Ride 40, Gym/Indoor 10).';
        if (sumPointsLabel) sumPointsLabel.innerHTML = 'Club Total Points <span style="font-size:10px; color:var(--accent-purple);">(Legacy 2025)</span>';
        if (sumPointsSub) sumPointsSub.innerText = '🏛️ Historical 2025 Fixed Multipliers';
        if (sumPointsCard) sumPointsCard.style.borderColor = 'rgba(168, 85, 247, 0.4)';
        if (thPoints) thPoints.innerText = 'Points (🏛️ Legacy)';
      } else {
        btnDyn.className = 'schema-pill active-dynamic';
        btnLeg.className = 'schema-pill';
        if (bannerTitle) bannerTitle.innerText = 'Dynamic MET Schema';
        if (bannerText) bannerText.innerHTML = '<span>⚡</span> <strong>Active Scoring System:</strong> <span>Dynamic MET Schema</span> — Continuous pace-weighted speed scaling with endurance distance dampening.';
        if (sumPointsLabel) sumPointsLabel.innerHTML = 'Club Total Points <span style="font-size:10px; color:var(--strava-orange);">(⚡ Dynamic MET)</span>';
        if (sumPointsSub) sumPointsSub.innerText = '⚡ Dynamic MET Pace-Weighted';
        if (sumPointsCard) sumPointsCard.style.borderColor = 'rgba(252, 76, 2, 0.35)';
        if (thPoints) thPoints.innerText = 'Points (⚡ Dynamic)';
      }
    }

    async function loadDashboardData() {
      // 1. Instant 0ms Paint using embedded dataset (zero network lag)
      try {
        const fallbackEl = document.getElementById('fallback-data');
        if (fallbackEl && fallbackEl.textContent.trim()) {
          globalData = JSON.parse(fallbackEl.textContent);
          console.log('Loaded dashboard data instantly from embedded dataset.');
          initDashboard();
        }
      } catch (err) {
        console.warn('Embedded data parse notice:', err);
      }

      // 2. Background fresh sync check across candidate paths
      const candidateUrls = [
        'dashboard_data.json?t=' + Date.now(),
        './dashboard_data.json?t=' + Date.now(),
        'web/dashboard_data.json?t=' + Date.now(),
        'export/dashboard_data.json?t=' + Date.now(),
        '../dashboard_data.json?t=' + Date.now()
      ];

      for (const url of candidateUrls) {
        try {
          const resp = await fetch(url, { cache: 'no-store' });
          if (resp.ok) {
            const freshData = await resp.json();
            const freshTime = freshData && freshData.summary ? freshData.summary.last_updated : null;
            const currTime = globalData && globalData.summary ? globalData.summary.last_updated : null;
            if (!globalData || freshTime !== currTime) {
              globalData = freshData;
              console.log('Updated dashboard data from live sync:', url);
              initDashboard();
            }
            return;
          }
        } catch (e) {}
      }
    }

    function initDashboard() {
      if (!globalData) return;

      initTheme();
      updateSchemaButtons();

      if (globalData.summary && globalData.summary.last_updated) {
        const raw = globalData.summary.last_updated;
        const d = new Date(raw);
        const formatted = isNaN(d) ? raw : d.toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
        document.getElementById('lastSyncedText').innerText = `Synced: ${formatted}`;
      }

      const sportSelect = document.getElementById('sportFilter');
      const sports = globalData.sport_breakdown || [];
      sportSelect.innerHTML = '<option value="ALL">All Activity Types</option>';
      sports.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s.activity_type;
        opt.innerText = `${getSportIcon(s.activity_type)} ${s.activity_type} (${s.count})`;
        sportSelect.appendChild(opt);
      });

      const initialTop = (globalData.athletes || []).slice(0, 5);
      selectedRadarAthleteIds = new Set(initialTop.map(a => a.athlete_id));

      document.getElementById('searchInput').addEventListener('input', applyFilters);
      document.getElementById('sportFilter').addEventListener('change', applyFilters);
      document.getElementById('dateFilter').addEventListener('change', handleDateFilterChange);
      document.getElementById('startDateInput').addEventListener('change', applyFilters);
      document.getElementById('endDateInput').addEventListener('change', applyFilters);
      document.getElementById('sortBy').addEventListener('change', applyFilters);
      document.getElementById('resetFiltersBtn').addEventListener('click', resetFilters);

      document.getElementById('modalClose').onclick = closeAthleteModal;
      document.getElementById('athleteModal').onclick = (e) => {
        if (e.target.id === 'athleteModal') closeAthleteModal();
      };
      document.getElementById('schemaModal').onclick = (e) => {
        if (e.target.id === 'schemaModal') closeSchemaModal();
      };
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          closeAthleteModal();
          closeSchemaModal();
        }
      });

      document.getElementById('exportCsvBtn').onclick = exportActivitiesCSV;

      applyFilters();

      checkHash();
      window.addEventListener('hashchange', checkHash);
      window.addEventListener('resize', () => {
        if (donutChartInstance) {
          const isMobile = window.innerWidth < 768;
          const targetPos = isMobile ? 'bottom' : 'right';
          if (donutChartInstance.options.plugins.legend.position !== targetPos) {
            donutChartInstance.options.plugins.legend.position = targetPos;
            donutChartInstance.update();
          }
        }
      });
    }

    function checkHash() {
      const hash = window.location.hash;
      if (hash.startsWith('#athlete=')) {
        const aid = hash.replace('#athlete=', '');
        openAthleteModal(aid);
      }
    }

    function handleDateFilterChange() {
      const mode = document.getElementById('dateFilter').value;
      const customBox = document.getElementById('customDateBox');
      if (mode === 'CUSTOM') {
        customBox.style.display = 'inline-flex';
      } else {
        customBox.style.display = 'none';
      }
      applyFilters();
    }

    function resetFilters() {
      document.getElementById('searchInput').value = '';
      document.getElementById('sportFilter').value = 'ALL';
      document.getElementById('dateFilter').value = 'CONTEST';
      document.getElementById('customDateBox').style.display = 'none';
      document.getElementById('startDateInput').value = '';
      document.getElementById('endDateInput').value = '';
      document.getElementById('sortBy').value = 'points';
      applyFilters();
    }

    function applyFilters() {
      if (!globalData || !globalData.activities) return;

      const search = document.getElementById('searchInput').value.trim().toLowerCase();
      const sport = document.getElementById('sportFilter').value;
      const dateMode = document.getElementById('dateFilter').value;
      const sortBy = document.getElementById('sortBy').value;

      let refDate = new Date();
      if (globalData.activities.length > 0) {
        const validDates = globalData.activities
          .map(a => new Date(a.datetime_iso || a.datetime_utc))
          .filter(d => !isNaN(d));
        if (validDates.length > 0) {
          refDate = new Date(Math.max(...validDates));
        }
      }

      let cutoffDate = null;
      if (dateMode === 'PAST_7_DAYS') {
        cutoffDate = new Date(refDate);
        cutoffDate.setDate(refDate.getDate() - 7);
      } else if (dateMode === 'PAST_14_DAYS') {
        cutoffDate = new Date(refDate);
        cutoffDate.setDate(refDate.getDate() - 14);
      } else if (dateMode === 'PAST_20_DAYS') {
        cutoffDate = new Date(refDate);
        cutoffDate.setDate(refDate.getDate() - 20);
      } else if (dateMode === 'PAST_30_DAYS') {
        cutoffDate = new Date(refDate);
        cutoffDate.setDate(refDate.getDate() - 30);
      }

      let startDate = null;
      let endDate = null;
      if (dateMode === 'CONTEST') {
        startDate = new Date('2026-09-14T00:00:00');
      } else if (dateMode === 'CUSTOM') {
        const sVal = document.getElementById('startDateInput').value;
        const eVal = document.getElementById('endDateInput').value;
        if (sVal) startDate = new Date(sVal + 'T00:00:00');
        if (eVal) endDate = new Date(eVal + 'T23:59:59');
      }

      const filteredActivities = globalData.activities.filter(act => {
        if (sport !== 'ALL' && act.activity_type !== sport) return false;

        if (search) {
          const nameMatch = (act.athlete_name || '').toLowerCase().includes(search);
          const typeMatch = (act.activity_type || '').toLowerCase().includes(search);
          if (!nameMatch && !typeMatch) return false;
        }

        const actDateStr = act.datetime_iso || act.datetime_utc;
        if (actDateStr) {
          const actDate = new Date(actDateStr);
          if (!isNaN(actDate)) {
            if (cutoffDate && actDate < cutoffDate) return false;
            if (startDate && actDate < startDate) return false;
            if (endDate && actDate > endDate) return false;
          }
        }

        return true;
      });

      currentFilteredActivities = filteredActivities;

      const athleteMap = {};
      const sportMap = {};

      filteredActivities.forEach(act => {
        const aid = act.athlete_id;
        const aname = act.athlete_name;
        const dist = parseFloat(act.distance_km || 0);
        const dur = parseFloat(act.duration_minutes || 0);
        
        // Active points according to selected schema
        const pts = currentSchema === 'legacy' 
          ? parseFloat(act.points_legacy !== undefined ? act.points_legacy : act.points || 0)
          : parseFloat(act.points_dynamic !== undefined ? act.points_dynamic : act.points || 0);
        
        const ptsDynamic = parseFloat(act.points_dynamic !== undefined ? act.points_dynamic : act.points || 0);
        const ptsLegacy = parseFloat(act.points_legacy !== undefined ? act.points_legacy : act.points || 0);

        const stype = act.activity_type || 'Workout';

        if (!athleteMap[aid]) {
          athleteMap[aid] = {
            athlete_id: aid,
            athlete_name: aname,
            total_activities: 0,
            types_set: new Set(),
            total_distance_km: 0.0,
            total_duration_minutes: 0.0,
            total_points: 0.0,
            total_points_dynamic: 0.0,
            total_points_legacy: 0.0
          };
        }

        const ath = athleteMap[aid];
        ath.total_activities += 1;
        ath.types_set.add(stype);
        ath.total_distance_km += dist;
        ath.total_duration_minutes += dur;
        ath.total_points += pts;
        ath.total_points_dynamic += ptsDynamic;
        ath.total_points_legacy += ptsLegacy;

        if (!sportMap[stype]) {
          sportMap[stype] = { activity_type: stype, count: 0, total_points: 0, total_distance_km: 0 };
        }
        sportMap[stype].count += 1;
        sportMap[stype].total_points += pts;
        sportMap[stype].total_distance_km += dist;
      });

      filteredAthletes = Object.values(athleteMap).map(ath => ({
        ...ath,
        unique_types: ath.types_set.size,
        activity_types: Array.from(ath.types_set),
        total_distance_km: Math.round(ath.total_distance_km * 100) / 100,
        total_duration_minutes: Math.round(ath.total_duration_minutes * 100) / 100,
        total_points: Math.round(ath.total_points * 100) / 100,
        total_points_dynamic: Math.round(ath.total_points_dynamic * 100) / 100,
        total_points_legacy: Math.round(ath.total_points_legacy * 100) / 100
      }));

      filteredAthletes.sort((a, b) => {
        if (sortBy === 'distance') return b.total_distance_km - a.total_distance_km;
        if (sortBy === 'duration') return b.total_duration_minutes - a.total_duration_minutes;
        if (sortBy === 'activities') return b.total_activities - a.total_activities;
        if (sortBy === 'name') return a.athlete_name.localeCompare(b.athlete_name);
        return b.total_points - a.total_points;
      });

      const maxDist = Math.max(...filteredAthletes.map(a => a.total_distance_km), 1.0);
      const maxDur = Math.max(...filteredAthletes.map(a => a.total_duration_minutes), 1.0);
      const maxPts = Math.max(...filteredAthletes.map(a => a.total_points), 1.0);
      const maxCnt = Math.max(...filteredAthletes.map(a => a.total_activities), 1);
      const maxDiv = Math.max(...filteredAthletes.map(a => a.unique_types), 1);

      filteredAthletes.forEach((ath, rank) => {
        ath.rank = rank + 1;
        ath.radar_metrics = {
          distance: Math.round((ath.total_distance_km / maxDist) * 1000) / 10,
          duration: Math.round((ath.total_duration_minutes / maxDur) * 1000) / 10,
          points: Math.round((ath.total_points / maxPts) * 1000) / 10,
          frequency: Math.round((ath.total_activities / maxCnt) * 1000) / 10,
          diversity: Math.round((ath.unique_types / maxDiv) * 1000) / 10
        };
      });

      const sportBreakdown = Object.values(sportMap).sort((a, b) => b.total_points - a.total_points);
      const totalSportPoints = Math.round(sportBreakdown.reduce((acc, s) => acc + s.total_points, 0) * 10) / 10;

      const summaryPayload = {
        total_athletes: filteredAthletes.length,
        total_activities: filteredActivities.length,
        total_distance_km: Math.round(filteredAthletes.reduce((acc, a) => acc + a.total_distance_km, 0) * 100) / 100,
        total_duration_hours: Math.round((filteredAthletes.reduce((acc, a) => acc + a.total_duration_minutes, 0) / 60) * 10) / 10,
        total_points: Math.round(filteredAthletes.reduce((acc, a) => acc + a.total_points, 0) * 100) / 100
      };

      lastSportBreakdown = sportBreakdown;
      lastTotalSportPoints = totalSportPoints;
      lastFilteredAthletes = filteredAthletes;

      renderSummary(summaryPayload);
      renderPodium(filteredAthletes);
      renderRadarSection(filteredAthletes);
      renderDonutChart(sportBreakdown, totalSportPoints);
      renderLeaderboardTable(filteredAthletes);

      document.getElementById('resultsCounter').innerText = `Showing ${filteredAthletes.length} of ${globalData.athletes.length} athletes (${filteredActivities.length} activities)`;
    }

    function renderSummary(s) {
      document.getElementById('sumAthletes').innerText = s.total_athletes.toLocaleString();
      document.getElementById('sumActivities').innerText = s.total_activities.toLocaleString();
      document.getElementById('sumDistance').innerHTML = `${s.total_distance_km.toLocaleString()} <span style="font-size: 15px; color: var(--text-muted); font-weight: 600;">km</span>`;
      document.getElementById('sumDuration').innerHTML = `${s.total_duration_hours.toLocaleString()} <span style="font-size: 15px; color: var(--text-muted); font-weight: 600;">hrs</span>`;
      document.getElementById('sumPoints').innerHTML = `${s.total_points.toLocaleString()} <span style="font-size: 15px; font-weight: 600;">pts</span>`;
    }

    function renderPodium(athletes) {
      const podiumEl = document.getElementById('podiumSection');
      podiumEl.innerHTML = '';
      if (!athletes || athletes.length === 0) {
        podiumEl.innerHTML = '<div style="grid-column: 1 / -1; text-align: center; color: var(--text-muted); padding: 20px;">No athletes match active filters</div>';
        return;
      }

      const top3 = athletes.slice(0, 3);
      const classes = ['gold', 'silver', 'bronze'];
      const medals = ['🥇 Gold', '🥈 Silver', '🥉 Bronze'];

      top3.forEach((ath, i) => {
        const initials = ath.athlete_name.split(' ').map(n => n[0]).join('').slice(0, 2);
        const card = document.createElement('div');
        card.className = `podium-card ${classes[i]}`;
        card.onclick = () => openAthleteModal(ath.athlete_id);
        card.title = `Click to view all activities for ${ath.athlete_name}`;
        card.innerHTML = `
          <div class="podium-badge">${medals[i]}</div>
          <div class="podium-avatar">${initials}</div>
          <div class="podium-name">${ath.athlete_name}</div>
          <div class="podium-points">${ath.total_points.toLocaleString()} pts</div>
          <div class="podium-stats">
            <div class="podium-stat-item">
              <span>Distance</span>
              <span class="podium-stat-val">🏃 ${ath.total_distance_km} km</span>
            </div>
            <div class="podium-stat-item">
              <span>Duration</span>
              <span class="podium-stat-val">⏱️ ${Math.round(ath.total_duration_minutes)} m</span>
            </div>
            <div class="podium-stat-item">
              <span>Acts</span>
              <span class="podium-stat-val">⚡ ${ath.total_activities}</span>
            </div>
          </div>
        `;
        podiumEl.appendChild(card);
      });
    }

    function renderRadarSection(athletes) {
      const availableIds = new Set(athletes.map(a => a.athlete_id));
      for (const id of Array.from(selectedRadarAthleteIds)) {
        if (!availableIds.has(id)) selectedRadarAthleteIds.delete(id);
      }
      if (selectedRadarAthleteIds.size === 0) {
        athletes.slice(0, 5).forEach(a => selectedRadarAthleteIds.add(a.athlete_id));
      }

      const pillsContainer = document.getElementById('radarPills');
      pillsContainer.innerHTML = '';
      const displayAthletes = athletes.slice(0, 10);
      const isObs = currentTheme === 'obsidian';
      const colors = isObs
        ? ['#f59e0b', '#38bdf8', '#f43f5e', '#10b981', '#a855f7', '#e2e8f0', '#0ea5e9', '#ec4899']
        : ['#fc4c02', '#38bdf8', '#22c55e', '#a855f7', '#fbbf24', '#f43f5e', '#06b6d4', '#eab308'];

      displayAthletes.forEach((ath, idx) => {
        const isSel = selectedRadarAthleteIds.has(ath.athlete_id);
        const pill = document.createElement('div');
        const color = colors[idx % colors.length];
        pill.className = `radar-pill ${isSel ? 'active' : ''}`;
        pill.style.color = isSel ? color : 'var(--text-muted)';
        pill.style.borderColor = isSel ? color : 'var(--card-border)';
        pill.innerHTML = `<span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:${color};"></span> ${ath.athlete_name}`;
        pill.onclick = () => {
          if (selectedRadarAthleteIds.has(ath.athlete_id)) {
            if (selectedRadarAthleteIds.size > 1) selectedRadarAthleteIds.delete(ath.athlete_id);
          } else {
            selectedRadarAthleteIds.add(ath.athlete_id);
          }
          renderRadarSection(athletes);
        };
        pillsContainer.appendChild(pill);
      });

      const chartAthletes = athletes.filter(a => selectedRadarAthleteIds.has(a.athlete_id));
      renderRadarChart(chartAthletes);
    }

    function renderRadarChart(selectedAthletes) {
      const ctx = document.getElementById('radarChart').getContext('2d');
      if (radarChartInstance) radarChartInstance.destroy();

      const colors = ['#fc4c02', '#38bdf8', '#22c55e', '#a855f7', '#fbbf24', '#f43f5e', '#06b6d4', '#eab308'];

      const datasets = selectedAthletes.map((ath, idx) => {
        const color = colors[idx % colors.length];
        return {
          label: ath.athlete_name,
          data: [
            ath.radar_metrics.distance,
            ath.radar_metrics.duration,
            ath.radar_metrics.points,
            ath.radar_metrics.frequency,
            ath.radar_metrics.diversity
          ],
          rawMetrics: {
            dist: ath.total_distance_km,
            dur: ath.total_duration_minutes,
            pts: ath.total_points,
            cnt: ath.total_activities,
            div: ath.unique_types
          },
          backgroundColor: color + '22',
          borderColor: color,
          pointBackgroundColor: color,
          pointBorderColor: '#fff',
          pointHoverRadius: 6,
          borderWidth: 2.2
        };
      });

      radarChartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
          labels: ['Distance (km)', 'Duration (time)', 'Points Score', 'Activity Count', 'Sport Diversity'],
          datasets: datasets
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            r: {
              angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
              grid: { color: 'rgba(255, 255, 255, 0.08)' },
              pointLabels: {
                color: '#cbd5e1',
                font: { family: 'Inter', size: window.innerWidth < 768 ? 10 : 12, weight: '600' }
              },
              ticks: { display: false, max: 100, min: 0 }
            }
          },
          plugins: {
            legend: {
              position: 'top',
              align: 'center',
              labels: {
                color: '#f8fafc',
                font: { family: 'Inter', size: window.innerWidth < 768 ? 11 : 12, weight: '500' },
                boxWidth: 10,
                padding: 10
              }
            },
            tooltip: {
              backgroundColor: '#0f172a',
              titleColor: '#fff',
              bodyColor: '#cbd5e1',
              borderColor: 'rgba(255, 255, 255, 0.1)',
              borderWidth: 1,
              padding: 10,
              callbacks: {
                label: function(context) {
                  const val = context.parsed.r;
                  const raw = context.dataset.rawMetrics;
                  let rawStr = '';
                  if (context.dataIndex === 0) rawStr = ` (${raw.dist} km)`;
                  else if (context.dataIndex === 1) rawStr = ` (${Math.round(raw.dur)} mins)`;
                  else if (context.dataIndex === 2) rawStr = ` (${raw.pts} pts)`;
                  else if (context.dataIndex === 3) rawStr = ` (${raw.cnt} acts)`;
                  else if (context.dataIndex === 4) rawStr = ` (${raw.div} sports)`;
                  return `${context.dataset.label}: ${val}%${rawStr}`;
                }
              }
            }
          }
        }
      });
    }

    function renderDonutChart(sportBreakdown, totalPoints) {
      const ctx = document.getElementById('donutChart').getContext('2d');
      if (donutChartInstance) donutChartInstance.destroy();

      const labels = sportBreakdown.map(s => `${getSportIcon(s.activity_type)} ${s.activity_type}`);
      const data = sportBreakdown.map(s => Math.round(s.total_points * 10) / 10);
      const counts = sportBreakdown.map(s => s.count);
      const isMobile = window.innerWidth < 768;

      const isObs = currentTheme === 'obsidian';
      const donutColors = isObs
        ? ['#f59e0b', '#38bdf8', '#10b981', '#a855f7', '#f43f5e', '#64748b', '#e2e8f0', '#0ea5e9']
        : ['#fc4c02', '#38bdf8', '#22c55e', '#a855f7', '#fbbf24', '#f43f5e', '#06b6d4', '#eab308'];

      donutChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            backgroundColor: donutColors,
            borderWidth: 2,
            borderColor: isObs ? '#16161a' : '#1e293b'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '70%',
          plugins: {
            legend: {
              position: isMobile ? 'bottom' : 'right',
              align: 'center',
              labels: {
                color: '#f8fafc',
                font: { family: 'Inter', size: isMobile ? 11 : 12, weight: '500' },
                boxWidth: 12,
                padding: isMobile ? 8 : 12
              }
            },
            tooltip: {
              backgroundColor: '#0f172a',
              titleColor: '#fff',
              bodyColor: '#cbd5e1',
              borderColor: 'rgba(255, 255, 255, 0.1)',
              borderWidth: 1,
              padding: 10,
              callbacks: {
                label: function(context) {
                  const pts = context.parsed;
                  const pct = totalPoints > 0 ? ((pts / totalPoints) * 100).toFixed(1) : 0;
                  const count = counts[context.dataIndex] || 0;
                  return ` ${Math.round(pts).toLocaleString()} pts (${pct}%) • ${count} activities`;
                }
              }
            }
          }
        }
      });
    }

    function renderLeaderboardTable(list) {
      const tbody = document.getElementById('leaderboardTbody');
      tbody.innerHTML = '';
      if (!list || list.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; color: var(--text-muted); padding: 30px;">No athletes match the current search or filters</td></tr>';
        return;
      }

      list.forEach((ath, idx) => {
        const rank = idx + 1;
        let rankHtml = `#${rank}`;
        if (rank === 1) rankHtml = `<span class="rank-top1">🥇 #1</span>`;
        else if (rank === 2) rankHtml = `<span class="rank-top2">🥈 #2</span>`;
        else if (rank === 3) rankHtml = `<span class="rank-top3">🥉 #3</span>`;

        const initials = ath.athlete_name.split(' ').map(n => n[0]).join('').slice(0, 2);
        const avatarBg = getAvatarColor(ath.athlete_name);

        const sportTags = (ath.activity_types || []).slice(0, 3).map(st => `
          <span class="sport-tag">${getSportIcon(st)} ${st}</span>
        `).join('');

        const hours = Math.floor(ath.total_duration_minutes / 60);
        const mins = Math.round(ath.total_duration_minutes % 60);
        const durFormatted = hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;

        const tr = document.createElement('tr');
        tr.onclick = () => openAthleteModal(ath.athlete_id);
        tr.title = 'Click to open athlete profile';
        tr.innerHTML = `
          <td class="rank-cell">${rankHtml}</td>
          <td>
            <div class="athlete-cell">
              <div class="athlete-badge" style="background: ${avatarBg};">${initials}</div>
              <div>
                <div class="athlete-name">${ath.athlete_name}</div>
                <div class="sport-tags">${sportTags}</div>
              </div>
            </div>
          </td>
          <td><span style="font-weight: 600;">${ath.total_activities}</span></td>
          <td>${ath.unique_types}</td>
          <td style="font-weight: 600;">${ath.total_distance_km} km</td>
          <td>${durFormatted}</td>
          <td class="points-cell">${ath.total_points.toLocaleString()} pts</td>
          <td>
            <button class="btn btn-outline" style="padding: 4px 10px; font-size: 11px;">View ↗</button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    function openAthleteModal(athleteId, showAll = false) {
      if (!globalData) return;
      const athlete = (filteredAthletes || []).find(a => a.athlete_id === String(athleteId)) || 
                      (globalData.athletes || []).find(a => a.athlete_id === String(athleteId));
      if (!athlete) return;

      const allAthleteActs = (globalData.activities || []).filter(act => act.athlete_id === String(athleteId));
      let activities = (currentFilteredActivities && currentFilteredActivities.length > 0)
        ? currentFilteredActivities.filter(act => act.athlete_id === String(athleteId))
        : allAthleteActs;

      const excludedCount = allAthleteActs.length - activities.length;
      if (showAll) {
        activities = allAthleteActs;
      }

      const initials = athlete.athlete_name.split(' ').map(n => n[0]).join('').slice(0, 2);
      const avatarBg = getAvatarColor(athlete.athlete_name);
      const hours = Math.floor(athlete.total_duration_minutes / 60);
      const mins = Math.round(athlete.total_duration_minutes % 60);
      const durFormatted = hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;

      let actRows = activities.map(act => {
        const icon = getSportIcon(act.activity_type);
        const dateDisplay = act.datetime_display || act.datetime_utc || 'N/A';
        const url = act.activity_url || `https://www.strava.com/activities/${act.activity_id}`;
        const isIndoor = act.is_indoor === true || String(act.is_indoor) === 'true';
        const typeBadge = isIndoor ? '<span style="background:rgba(56,189,248,0.15); color:var(--accent-blue); padding:1px 6px; border-radius:4px; font-size:10px; margin-left:4px;">Indoor</span>' : '';
        const paceDisplay = act.pace ? `<span style="font-family:monospace; color:var(--accent-green); font-size:12px;">${act.pace}</span>` : '<span style="color:var(--text-dim);">—</span>';
        
        let integrityBadge = '';
        let distTitle = '';
        if (act.integrity_flag === 'MISLABELED_WALK') {
          integrityBadge = `<span title="Speed exceeded 8.6 km/h. Distance & points estimated from median walking pace." style="background:rgba(239,68,68,0.18); color:#f87171; border:1px solid rgba(239,68,68,0.4); padding:1px 6px; border-radius:4px; font-size:10px; margin-left:4px;">🚨 Adjusted Walk</span>`;
          distTitle = `title="Logged: ${act.original_distance_km || act.distance_km} km (Pace ${act.original_pace || act.pace}). Distance normalized via median walking pace."`;
        } else if (act.integrity_flag === 'SENSOR_PACE_ANOMALY') {
          integrityBadge = `<span title="Sub-4:15 pace flagged as sensor anomaly or potential cycle. Auto-nerfed to tempo baseline." style="background:rgba(245,158,11,0.18); color:#fbbf24; border:1px solid rgba(245,158,11,0.4); padding:1px 6px; border-radius:4px; font-size:10px; margin-left:4px;">⚠️ Sensor Anomaly Nerfed</span>`;
          distTitle = `title="Logged: ${act.original_distance_km || act.distance_km} km (Pace ${act.original_pace || act.pace}). Auto-nerfed to tempo baseline."`;
        } else if (act.integrity_flag === 'SUSPECT_ENDURANCE_PACE') {
          integrityBadge = `<span title="10+ km run logged at < 5:00/km pace flagged as suspect endurance pace / sensor spike. Auto-normalized to tempo baseline." style="background:rgba(245,158,11,0.18); color:#fbbf24; border:1px solid rgba(245,158,11,0.4); padding:1px 6px; border-radius:4px; font-size:10px; margin-left:4px;">⚠️ Suspect 10k+ Pace</span>`;
          distTitle = `title="Logged: ${act.original_distance_km || act.distance_km} km (Pace ${act.original_pace || act.pace}). 10+ km sub-5:00 pace normalized to tempo baseline."`;
        } else if (act.integrity_flag === 'VEHICLE_SPEED') {
          integrityBadge = `<span title="Speed exceeded 18 km/h on foot sport. Normalized to median pace." style="background:rgba(239,68,68,0.18); color:#f87171; border:1px solid rgba(239,68,68,0.4); padding:1px 6px; border-radius:4px; font-size:10px; margin-left:4px;">🚗 Vehicle Velocity Adjusted</span>`;
          distTitle = `title="Logged: ${act.original_distance_km || act.distance_km} km (Pace ${act.original_pace || act.pace}). Speed exceeded 18 km/h, normalized."`;
        }

        const isOutsideFilter = showAll && currentFilteredActivities && !currentFilteredActivities.some(a => a.activity_id === act.activity_id);
        const filterTag = isOutsideFilter ? '<span style="background:rgba(100,116,139,0.25); color:#94a3b8; border:1px solid rgba(148,163,184,0.3); padding:1px 6px; border-radius:4px; font-size:10px; margin-left:4px;" title="Activity falls outside active contest date filter">Pre-Contest</span>' : '';

        const actPts = currentSchema === 'legacy'
          ? (act.points_legacy !== undefined ? act.points_legacy : act.points)
          : (act.points_dynamic !== undefined ? act.points_dynamic : act.points);

        return `
          <tr style="${isOutsideFilter ? 'opacity: 0.65;' : ''}">
            <td>
              <span style="display:inline-flex; align-items:center; gap:4px; font-weight:600; flex-wrap:wrap;">
                <span>${icon}</span> ${act.activity_type} ${typeBadge} ${integrityBadge} ${filterTag}
              </span>
            </td>
            <td style="color: var(--text-muted); font-size: 13px;">${dateDisplay}</td>
            <td style="font-weight:600;" ${distTitle}>${act.distance_km} km ${act.integrity_flag ? '<span style="color:#f87171; font-size:11px;" title="Adjusted by integrity filter">*</span>' : ''}</td>
            <td>${Math.round(act.duration_minutes)} mins</td>
            <td>${paceDisplay}</td>
            <td style="font-weight:700; color:var(--strava-orange);">${actPts} pts</td>
            <td>
              <a href="${url}" target="_blank" rel="noopener noreferrer" style="color:var(--accent-blue); text-decoration:none; font-size:12px; font-weight:600; display:inline-flex; align-items:center; gap:4px;">
                Strava
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
              </a>
            </td>
          </tr>
        `;
      }).join('');

      let filterNotice = '';
      if (excludedCount > 0 && !showAll) {
        filterNotice = `
          <div style="background:rgba(56,189,248,0.08); border:1px solid rgba(56,189,248,0.25); border-radius:8px; padding:8px 12px; margin-bottom:12px; font-size:12px; color:#cbd5e1; display:flex; justify-content:space-between; align-items:center;">
            <span>Showing <strong>${activities.length}</strong> activities within active time filter (${excludedCount} prior activities hidden).</span>
            <button class="btn btn-outline" style="padding:3px 10px; font-size:11px;" onclick="openAthleteModal('${athleteId}', true)">Show All (${allAthleteActs.length})</button>
          </div>
        `;
      } else if (showAll && excludedCount > 0) {
        filterNotice = `
          <div style="background:rgba(234,179,8,0.08); border:1px solid rgba(234,179,8,0.25); border-radius:8px; padding:8px 12px; margin-bottom:12px; font-size:12px; color:#fbbf24; display:flex; justify-content:space-between; align-items:center;">
            <span>Showing all <strong>${allAthleteActs.length}</strong> activities (including pre-contest uploads).</span>
            <button class="btn btn-outline" style="padding:3px 10px; font-size:11px;" onclick="openAthleteModal('${athleteId}', false)">Show Filtered (${allAthleteActs.length - excludedCount})</button>
          </div>
        `;
      }

      const modalBody = document.getElementById('modalBody');
      const schemaTag = currentSchema === 'legacy' ? '🏛️ Legacy Points' : '⚡ Dynamic Points';

      const dynPtsStr = (athlete.total_points_dynamic || athlete.total_points || 0).toLocaleString();
      const legPtsStr = (athlete.total_points_legacy || athlete.total_points || 0).toLocaleString();

      modalBody.innerHTML = `
        <div class="modal-athlete-header">
          <div class="modal-avatar" style="background: ${avatarBg};">${initials}</div>
          <div>
            <h2 style="font-family:'Outfit', sans-serif; font-size:24px; font-weight:800; color:#fff; margin-bottom:4px;">
              ${athlete.athlete_name}
            </h2>
            <div style="display:flex; align-items:center; gap:12px; font-size:13px; color:var(--text-muted);">
              <span>Rank #${athlete.rank || 1} Overall</span>
              <span>•</span>
              <span style="color:var(--text-primary); font-weight:600;">${schemaTag}</span>
              <span>•</span>
              <a href="https://www.strava.com/athletes/${athlete.athlete_id}" target="_blank" rel="noopener noreferrer" style="color:var(--strava-orange); text-decoration:none; font-weight:600;">
                Strava Profile ↗
              </a>
            </div>
          </div>
        </div>

        <div class="modal-stat-cards">
          <div class="modal-stat-card">
            <div class="modal-stat-label">Total Points</div>
            <div class="modal-stat-value" style="color: var(--strava-orange);">${athlete.total_points.toLocaleString()}</div>
          </div>
          <div class="modal-stat-card">
            <div class="modal-stat-label">Total Distance</div>
            <div class="modal-stat-value">${athlete.total_distance_km} km</div>
          </div>
          <div class="modal-stat-card">
            <div class="modal-stat-label">Total Time</div>
            <div class="modal-stat-value">${durFormatted}</div>
          </div>
          <div class="modal-stat-card">
            <div class="modal-stat-label">Activities</div>
            <div class="modal-stat-value">${athlete.total_activities}</div>
          </div>
        </div>

        <!-- Dual Schema Comparison Pill -->
        <div style="background:rgba(15,23,42,0.6); border:1px solid var(--card-border); border-radius:12px; padding:10px 16px; font-size:12px; display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
          <span style="color:var(--text-muted);">Dual-Schema Comparison:</span>
          <div style="display:flex; gap:16px;">
            <span style="color:var(--strava-orange); font-weight:700;">⚡ Dynamic: ${dynPtsStr} pts</span>
            <span style="color:var(--accent-purple); font-weight:700;">🏛️ Legacy: ${legPtsStr} pts</span>
          </div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
          <h3 style="font-family:'Outfit', sans-serif; font-size:16px; font-weight:700;">Activity History (${activities.length})</h3>
        </div>

        ${filterNotice}

        <div style="max-height: 380px; overflow: auto; -webkit-overflow-scrolling: touch; border: 1px solid var(--card-border); border-radius: 14px;">
          <table class="data-table" style="min-width: 580px;">
            <thead>
              <tr>
                <th>Type</th>
                <th>Date</th>
                <th>Distance</th>
                <th>Duration</th>
                <th>Pace</th>
                <th>${schemaTag}</th>
                <th>Link</th>
              </tr>
            </thead>
            <tbody>
              ${actRows || '<tr><td colspan="7" style="text-align:center; color:var(--text-muted); padding:20px;">No activities recorded</td></tr>'}
            </tbody>
          </table>
        </div>
      `;

      document.getElementById('athleteModal').classList.add('active');
      window.location.hash = `athlete=${athleteId}`;
    }

    function closeAthleteModal() {
      document.getElementById('athleteModal').classList.remove('active');
      if (window.location.hash.startsWith('#athlete=')) {
        history.replaceState(null, null, ' ');
      }
    }

    function openSchemaModal() {
      document.getElementById('schemaModal').classList.add('active');
    }

    function closeSchemaModal() {
      document.getElementById('schemaModal').classList.remove('active');
    }

    function exportActivitiesCSV() {
      const acts = (currentFilteredActivities && currentFilteredActivities.length > 0) ? currentFilteredActivities : ((globalData && globalData.activities) ? globalData.activities : []);
      if (acts.length === 0) return;

      const headers = ['activity_id', 'athlete_id', 'athlete_name', 'activity_type', 'datetime_utc', 'distance_km', 'duration_minutes', 'points_dynamic', 'points_legacy', 'pace', 'is_indoor', 'activity_url'];
      let csvContent = headers.join(',') + '\\n';

      acts.forEach(act => {
        const row = headers.map(h => {
          let val = act[h] !== undefined ? String(act[h]) : '';
          if (val.includes(',') || val.includes('"') || val.includes('\\n')) {
            val = '"' + val.replace(/"/g, '""') + '"';
          }
          return val;
        });
        csvContent += row.join(',') + '\\n';
      });

      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', 'strava_2026_activities.csv');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }

    loadDashboardData();
  </script>
</body>
</html>
'''

full_html = html_template.replace("<!-- FALLBACK_DATA_PLACEHOLDER -->", json_str)

destinations = [
    os.path.join(ROOT_DIR, "index.html"),
    os.path.join(YEAR_DIR, "index.html"),
    os.path.join(WEB_DIR, "index.html"),
    os.path.join(EXPORT_DIR, "index.html")
]

for dest in destinations:
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"[+] Wrote index.html -> {dest}")

# Ensure .nojekyll in ROOT_DIR for GitHub Pages
nojekyll_path = os.path.join(ROOT_DIR, ".nojekyll")
with open(nojekyll_path, "w", encoding="utf-8") as f:
    f.write("")
print(f"[+] Created .nojekyll -> {nojekyll_path}")

# Sync activities.csv, dashboard_data.json, and memberlist.csv
for target_dir in [YEAR_DIR, WEB_DIR, EXPORT_DIR]:
    os.makedirs(target_dir, exist_ok=True)
    shutil.copy2(os.path.join(ROOT_DIR, "activities.csv"), os.path.join(target_dir, "activities.csv"))
    shutil.copy2(os.path.join(ROOT_DIR, "dashboard_data.json"), os.path.join(target_dir, "dashboard_data.json"))
    mem_src = os.path.join(ROOT_DIR, "memberlist.csv")
    if os.path.exists(mem_src):
        shutil.copy2(mem_src, os.path.join(target_dir, "memberlist.csv"))

print("[+] Synchronized activities.csv, dashboard_data.json, and memberlist.csv to all targets.")

# Also generate The Arena (arena.html) across all targets
try:
    import generate_arena
    generate_arena.build_arena(ROOT_DIR, YEAR_DIR, WEB_DIR, EXPORT_DIR)
    print("[+] Generated The Arena (arena.html) to all targets.")
except Exception as e:
    print(f"[!] Warning on arena generation: {e}")
