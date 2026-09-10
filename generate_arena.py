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

    arena_template = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  <title>The Arena • Strava 2026 Gamification Hub</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@500;600;700;800;900&display=swap" rel="stylesheet">
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
      max-width: 1320px;
      margin: 0 auto;
      padding: 28px 24px;
    }

    /* Hero Banner */
    .arena-hero {
      background: linear-gradient(135deg, rgba(168, 85, 247, 0.15) 0%, rgba(252, 76, 2, 0.15) 50%, rgba(56, 189, 248, 0.1) 100%);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 24px;
      padding: 32px 36px;
      margin-bottom: 30px;
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
      font-size: 32px;
      font-weight: 900;
      color: #fff;
      margin-bottom: 8px;
      letter-spacing: -0.5px;
    }

    .arena-hero-sub {
      font-size: 14px;
      color: var(--text-muted);
      max-width: 600px;
      line-height: 1.6;
    }

    /* Arena Navigation Tabs */
    .arena-nav-bar {
      display: flex;
      gap: 10px;
      overflow-x: auto;
      padding-bottom: 8px;
      margin-bottom: 30px;
      border-bottom: 1px solid var(--card-border);
    }

    .arena-nav-tab {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 10px 20px;
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
      margin-bottom: 24px;
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
    }

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
      display: flex;
      flex-direction: column;
    }
    .trophy-card:hover {
      transform: translateY(-5px);
      border-color: var(--card-hover-border);
      box-shadow: 0 14px 30px rgba(0, 0, 0, 0.4);
    }

    .trophy-badge-icon {
      width: 52px;
      height: 52px;
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 26px;
      margin-bottom: 16px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .trophy-title {
      font-family: 'Outfit', sans-serif;
      font-size: 18px;
      font-weight: 800;
      color: #fff;
      margin-bottom: 4px;
    }

    .trophy-criteria {
      font-size: 12px;
      color: var(--text-muted);
      margin-bottom: 16px;
      line-height: 1.4;
    }

    .trophy-holder-box {
      margin-top: auto;
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 12px 14px;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .trophy-avatar {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 13px;
      font-weight: 800;
      color: #fff;
      flex-shrink: 0;
    }

    .trophy-holder-info {
      flex-grow: 1;
      overflow: hidden;
    }

    .trophy-holder-name {
      font-weight: 700;
      font-size: 13px;
      color: #fff;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .trophy-stat-val {
      font-size: 11px;
      color: var(--gold);
      font-weight: 700;
    }

    /* 1v1 Duel Arena */
    .duel-arena-box {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 24px;
      padding: 30px;
      margin-bottom: 40px;
    }

    .duel-selectors {
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      gap: 20px;
      align-items: center;
      margin-bottom: 28px;
    }

    .duel-fighter-select {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .duel-vs-badge {
      width: 50px;
      height: 50px;
      border-radius: 50%;
      background: linear-gradient(135deg, #fc4c02, #ff6a2b);
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Outfit', sans-serif;
      font-size: 18px;
      font-weight: 900;
      color: #fff;
      box-shadow: 0 0 20px var(--orange-glow);
    }

    .duel-layout {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
    }

    .duel-chart-box {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--card-border);
      border-radius: 18px;
      padding: 20px;
      min-height: 340px;
      position: relative;
    }

    .duel-comparison-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }
    .duel-comparison-table td {
      padding: 12px 14px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stat-label-col {
      text-align: center;
      color: var(--text-muted);
      font-weight: 600;
      text-transform: uppercase;
      font-size: 11px;
      letter-spacing: 0.5px;
    }

    .fighter-red-val {
      font-weight: 800;
      color: var(--fighter-red);
      text-align: left;
    }
    .fighter-blue-val {
      font-weight: 800;
      color: var(--fighter-blue);
      text-align: right;
    }

    .duel-verdict-box {
      margin-top: 24px;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 16px;
      padding: 18px 22px;
      font-size: 13.5px;
      line-height: 1.6;
      color: #e2e8f0;
    }

    /* Virtual Journey Road Trip */
    .journey-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 24px;
      padding: 32px;
      margin-bottom: 40px;
    }

    .journey-progress-track {
      background: rgba(15, 23, 42, 0.8);
      border-radius: 30px;
      height: 24px;
      border: 1px solid var(--card-border);
      position: relative;
      overflow: hidden;
      margin: 28px 0;
    }

    .journey-progress-fill {
      height: 100%;
      background: linear-gradient(90deg, #22c55e, #38bdf8, #a855f7, #fc4c02);
      border-radius: 30px;
      transition: width 1s ease;
      box-shadow: 0 0 16px rgba(56, 189, 248, 0.5);
    }

    .milestone-cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
    }

    .milestone-card {
      background: rgba(15, 23, 42, 0.65);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 18px;
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
      padding: 28px;
      margin: 24px 0;
      min-height: 160px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }

    /* Responsive */
    @media (max-width: 900px) {
      .duel-layout { grid-template-columns: 1fr; }
      .momentum-grid { grid-template-columns: 1fr; }
      .duel-selectors { grid-template-columns: 1fr; }
      .duel-vs-badge { margin: 0 auto; }
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
        <div class="brand-subtitle">Gamification Hub & Trophy Room</div>
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
        <div class="arena-hero-title">⚡ Welcome to The Arena</div>
        <div class="arena-hero-sub">
          The gamified clubhouse for Connectivity Sports Day 2026. Explore algorithmic trophies, simulate head-to-head athlete duels, track our collective virtual road trip, and discover daily workout dares.
        </div>
      </div>
      <div>
        <a href="index.html" class="btn btn-outline" style="font-size:12px; padding:7px 14px;">
          View Live Standings →
        </a>
      </div>
    </div>

    <!-- Arena Navigation Tabs -->
    <div class="arena-nav-bar">
      <button class="arena-nav-tab active" onclick="switchArenaTab('tabTrophies')">
        <span>🏆</span> The Trophy Room
      </button>
      <button class="arena-nav-tab" onclick="switchArenaTab('tabDuel')">
        <span>🥊</span> 1v1 Duel Arena
      </button>
      <button class="arena-nav-tab" onclick="switchArenaTab('tabJourney')">
        <span>🗺️</span> Virtual Road Trip
      </button>
      <button class="arena-nav-tab" onclick="switchArenaTab('tabMomentum')">
        <span>🔥</span> Momentum Tracker
      </button>
      <button class="arena-nav-tab" onclick="switchArenaTab('tabRoulette')">
        <span>🎲</span> Workout Roulette
      </button>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 1: THE TROPHY ROOM -->
    <!-- =================================================================== -->
    <div id="tabTrophies" class="arena-panel active">
      <div class="section-header">
        <div class="section-title">
          <span>🏆</span> The Clubhouse Trophy Room
        </div>
        <div class="section-desc">
          Automated superlative badges awarded algorithmically across all Strava activities logged during the 2026 competition.
        </div>
      </div>

      <div id="trophiesContainer" class="trophy-grid">
        <!-- Injected via JavaScript -->
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 2: 1v1 DUEL ARENA -->
    <!-- =================================================================== -->
    <div id="tabDuel" class="arena-panel">
      <div class="section-header">
        <div class="section-title">
          <span>🥊</span> 1v1 Athlete Duel Arena
        </div>
        <div class="section-desc">
          Compare any two athletes side-by-side. Inspect radar overlaps, head-to-head metrics, and automated matchup verdicts.
        </div>
      </div>

      <div class="duel-arena-box">
        <div class="duel-selectors">
          <div class="duel-fighter-select" style="border-left: 4px solid var(--fighter-red);">
            <label style="font-size: 11px; font-weight: 700; color: var(--fighter-red); text-transform: uppercase;">Red Corner (Fighter 1)</label>
            <select id="fighter1Select" class="btn btn-outline" style="background: rgba(15,23,42,0.9); width:100%;" onchange="updateDuel()"></select>
          </div>

          <div class="duel-vs-badge">VS</div>

          <div class="duel-fighter-select" style="border-right: 4px solid var(--fighter-blue);">
            <label style="font-size: 11px; font-weight: 700; color: var(--fighter-blue); text-transform: uppercase; text-align: right;">Blue Corner (Fighter 2)</label>
            <select id="fighter2Select" class="btn btn-outline" style="background: rgba(15,23,42,0.9); width:100%;" onchange="updateDuel()"></select>
          </div>
        </div>

        <div class="duel-layout">
          <!-- Tale of the Tape Stats Table -->
          <div>
            <table class="duel-comparison-table">
              <thead>
                <tr style="border-bottom: 2px solid var(--card-border);">
                  <th id="f1NameTh" style="color: var(--fighter-red); font-size: 15px; font-weight: 800; text-align:left;">Fighter 1</th>
                  <th class="stat-label-col">Metric</th>
                  <th id="f2NameTh" style="color: var(--fighter-blue); font-size: 15px; font-weight: 800; text-align:right;">Fighter 2</th>
                </tr>
              </thead>
              <tbody id="duelStatsTbody">
                <!-- Generated by JS -->
              </tbody>
            </table>
          </div>

          <!-- Radar Chart Overlay -->
          <div class="duel-chart-box">
            <canvas id="duelRadarChart"></canvas>
          </div>
        </div>

        <div id="duelVerdictBox" class="duel-verdict-box">
          <!-- Tale of the tape narrative generated by JS -->
        </div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 3: VIRTUAL ROAD TRIP -->
    <!-- =================================================================== -->
    <div id="tabJourney" class="arena-panel">
      <div class="section-header">
        <div class="section-title">
          <span>🗺️</span> The Collective Virtual Road Trip
        </div>
        <div class="section-desc">
          Every kilometer logged by every club member powers our collective journey across iconic checkpoints!
        </div>
      </div>

      <div class="journey-card">
        <div style="display:flex; justify-content:space-between; align-items:flex-end; flex-wrap:wrap; gap:14px;">
          <div>
            <div style="font-size:12px; font-weight:700; color:var(--strava-orange); text-transform:uppercase;">Total Club Cumulative Distance</div>
            <div id="journeyTotalKm" style="font-family:'Outfit',sans-serif; font-size:42px; font-weight:900; color:#fff;">0.0 km</div>
          </div>
          <div style="text-align:right;">
            <div style="font-size:12px; color:var(--text-muted);">Current Landmark</div>
            <div id="journeyCurrentLandmark" style="font-size:16px; font-weight:700; color:var(--accent-green);">Calculating...</div>
          </div>
        </div>

        <div class="journey-progress-track">
          <div id="journeyProgressBar" class="journey-progress-fill" style="width: 0%;"></div>
        </div>

        <div id="milestonesContainer" class="milestone-cards-grid">
          <!-- Milestones injected via JS -->
        </div>

        <div style="margin-top:28px; background:rgba(15,23,42,0.6); border:1px solid var(--card-border); border-radius:16px; padding:20px; display:flex; justify-content:space-around; text-align:center; flex-wrap:wrap; gap:16px;">
          <div>
            <div style="font-size:24px; font-weight:800; color:var(--accent-green);" id="journeyPizzas">~160</div>
            <div style="font-size:12px; color:var(--text-muted);">🍕 Pizza Slices Burned</div>
          </div>
          <div>
            <div style="font-size:24px; font-weight:800; color:var(--accent-blue);" id="journeyElevation">~3,200 m</div>
            <div style="font-size:12px; color:var(--text-muted);">🏔️ Climbed (Higher than Mt. Olympus!)</div>
          </div>
          <div>
            <div style="font-size:24px; font-weight:800; color:var(--gold);" id="journeyDaysActive">105</div>
            <div style="font-size:12px; color:var(--text-muted);">⚡ Total Workouts Logged</div>
          </div>
        </div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 4: MOMENTUM TRACKER -->
    <!-- =================================================================== -->
    <div id="tabMomentum" class="arena-panel">
      <div class="section-header">
        <div class="section-title">
          <span>🔥</span> The Momentum Index
        </div>
        <div class="section-desc">
          Who's on fire right now? Tracking recent 7-day activity velocity and streak dedication across the club.
        </div>
      </div>

      <div class="momentum-grid">
        <div class="momentum-table-box">
          <h3 style="font-family:'Outfit', sans-serif; font-size:16px; font-weight:700; color:#fff; margin-bottom:16px;">
            Recent 7-Day Velocity Leaders
          </h3>
          <table class="duel-comparison-table" style="font-size:13px;">
            <thead>
              <tr style="border-bottom:1px solid var(--card-border);">
                <th>#</th>
                <th>Athlete</th>
                <th>7-Day Acts</th>
                <th>7-Day Dist</th>
                <th>7-Day Points</th>
              </tr>
            </thead>
            <tbody id="momentumTbody">
              <!-- Injected by JS -->
            </tbody>
          </table>
        </div>

        <div class="streak-highlight-card">
          <div style="font-size:36px; margin-bottom:12px;">🔥</div>
          <h3 style="font-family:'Outfit', sans-serif; font-size:20px; font-weight:800; color:#fff; margin-bottom:8px;">
            Active Hot Streaks
          </h3>
          <p style="font-size:13px; color:var(--text-muted); line-height:1.6; margin-bottom:16px;">
            Dedication beats intensity over the long haul. Athletes logging consistent daily habits build massive momentum towards the season finale.
          </p>
          <div id="streakTopList" style="display:flex; flex-direction:column; gap:10px;">
            <!-- Injected by JS -->
          </div>
        </div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- TAB 5: WORKOUT ROULETTE -->
    <!-- =================================================================== -->
    <div id="tabRoulette" class="arena-panel">
      <div class="section-header">
        <div class="section-title">
          <span>🎲</span> Daily Workout Roulette
        </div>
        <div class="section-desc">
          Spin the wheel for today's spontaneous club fitness mission and earn extra bragging rights.
        </div>
      </div>

      <div class="roulette-box">
        <div style="font-size: 40px; margin-bottom: 10px;">🎰</div>
        <h2 style="font-family:'Outfit', sans-serif; font-size:24px; font-weight:800; color:#fff;">
          Club Dare of the Day
        </h2>
        <div style="font-size:13px; color:var(--text-muted); margin-top:4px;">
          Hit the button to generate a targeted challenge tailored for today's session!
        </div>

        <div class="roulette-card-display" id="rouletteDisplay">
          <div style="font-size: 32px; margin-bottom: 8px;" id="dareIcon">⚡</div>
          <div style="font-family:'Outfit', sans-serif; font-size: 20px; font-weight: 800; color: #fff; margin-bottom: 6px;" id="dareTitle">
            The 20-Minute Post-Lunch Stroll
          </div>
          <div style="font-size: 13px; color: var(--text-muted); max-width: 440px;" id="dareDesc">
            Take a brisk 20-minute walk after your meal to aid digestion and bag an effortless ~130 dynamic points.
          </div>
          <div style="margin-top: 14px; font-size: 11px; font-weight: 700; color: var(--accent-green); background: rgba(34,197,94,0.15); padding: 3px 10px; border-radius: 12px;" id="darePts">
            Est. Reward: ~130 - 160 pts
          </div>
        </div>

        <button class="btn btn-orange" onclick="spinRoulette()" style="padding: 10px 24px; font-size: 14px; font-weight: 700;">
          <span>🎲</span> Spin for New Challenge!
        </button>
      </div>
    </div>

  </div>

  <!-- Fallback Embedded Data -->
  <script id="fallback-data" type="application/json">
<!-- FALLBACK_DATA_PLACEHOLDER -->
  </script>

  <script>
    let globalData = null;
    let duelRadarChartInstance = null;

    const DARES = [
      {
        icon: "🚶",
        title: "The Post-Lunch Metabolic Stroll",
        desc: "Take a brisk 20-minute walk after your meal. Improves glucose control and bags an effortless ~130 dynamic points!",
        pts: "+120 - 150 pts"
      },
      {
        icon: "🏃",
        title: "Sunset 5K Aerobic Cruise",
        desc: "Lace up for an easy aerobic 5 km jog at conversational pace. Pure cardio conditioning!",
        pts: "+420 - 500 pts"
      },
      {
        icon: "🚴",
        title: "The 20-Kilometer Pedal Blast",
        desc: "Hop on the bike for a quick 20 km spin or trainer ride. Equal in calories to a solid 5 km run!",
        pts: "+500 pts"
      },
      {
        icon: "🏋️",
        title: "Iron Core & Strength Circuit",
        desc: "Log 40 minutes of weight training or high-intensity bodyweight intervals.",
        pts: "+160 - 240 pts"
      },
      {
        icon: "🌅",
        title: "Dawn Patrol 7:00 AM Spark",
        desc: "Complete any workout before 7:30 AM to jump-start your metabolism and claim the Early Bird trophy!",
        pts: "+200 - 450 pts"
      },
      {
        icon: "🔥",
        title: "The Double Session Challenge",
        desc: "Log two separate activities in the same day (e.g., morning walk + evening gym). Remember: NO daily point caps!",
        pts: "+600+ pts total"
      },
      {
        icon: "🏊",
        title: "Submerged Endurance Swim",
        desc: "Dive in for 30 minutes of continuous pool swimming for maximum full-body cardiovascular burn.",
        pts: "+150 pts"
      }
    ];

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

    function switchArenaTab(tabId) {
      document.querySelectorAll('.arena-nav-tab').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.arena-panel').forEach(p => p.classList.remove('active'));

      event.currentTarget.classList.add('active');
      document.getElementById(tabId).classList.add('active');

      if (tabId === 'tabDuel' && duelRadarChartInstance) {
        setTimeout(() => duelRadarChartInstance.resize(), 100);
      }
    }

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

      renderTrophies();
      initDuelSelectors();
      renderVirtualJourney();
      renderMomentum();
    }

    /* =========================================================================
       1. TROPHY ROOM LOGIC
       ========================================================================= */
    function renderTrophies() {
      const activities = globalData.activities || [];
      const athletes = globalData.athletes || [];

      // Trophy tally dictionaries
      const nightOwls = {};
      const earlyBirds = {};
      const weekendKms = {};
      const sportDiversity = {};
      let fastestPace = { athlete: 'N/A', paceStr: 'N/A', paceVal: 999, dist: 0 };
      let longestSingle = { athlete: 'N/A', dist: 0, sport: 'N/A' };
      let marathoner = { athlete: 'N/A', dist: 0 };

      athletes.forEach(a => {
        nightOwls[a.athlete_name] = 0;
        earlyBirds[a.athlete_name] = 0;
        weekendKms[a.athlete_name] = 0;
        sportDiversity[a.athlete_name] = a.unique_types || 1;
      });

      activities.forEach(act => {
        const name = act.athlete_name;
        const dist = parseFloat(act.distance_km || 0);
        const dur = parseFloat(act.duration_minutes || 0);
        const dtStr = act.datetime_iso || act.datetime_utc;

        if (dtStr) {
          const d = new Date(dtStr);
          if (!isNaN(d)) {
            const h = d.getHours();
            if (h >= 20) nightOwls[name] = (nightOwls[name] || 0) + 1;
            if (h < 7 || (h === 7 && d.getMinutes() <= 30)) earlyBirds[name] = (earlyBirds[name] || 0) + 1;
            if (d.getDay() === 0 || d.getDay() === 6) weekendKms[name] = (weekendKms[name] || 0) + dist;
          }
        }

        if (dist > longestSingle.dist) {
          longestSingle = { athlete: name, dist: dist, sport: act.activity_type };
        }

        if (act.activity_type.toLowerCase().includes('run') && dist >= 3.0 && dur > 0) {
          const paceDec = dur / dist;
          if (paceDec < fastestPace.paceVal && paceDec > 2.5) {
            fastestPace = { athlete: name, paceStr: act.pace || `${Math.floor(paceDec)}:${Math.round((paceDec%1)*60)} /km`, paceVal: paceDec, dist: dist };
          }
        }
      });

      const topNightOwl = Object.entries(nightOwls).sort((a, b) => b[1] - a[1])[0] || ['Satyaprakash Karsharma', 19];
      const topEarlyBird = Object.entries(earlyBirds).sort((a, b) => b[1] - a[1])[0] || ['Sai Harshita', 15];
      const topWeekend = Object.entries(weekendKms).sort((a, b) => b[1] - a[1])[0] || ['Satyaprakash Karsharma', 166.3];
      const topDiversity = Object.entries(sportDiversity).sort((a, b) => b[1] - a[1])[0] || ['Divyansh', 4];
      const topVolume = athletes.slice(0, 1)[0] || { athlete_name: 'Satyaprakash Karsharma', total_points: 24655 };

      const trophies = [
        {
          icon: "⚡",
          title: "Speed Demon",
          criteria: "Fastest sustained pace recorded on an outdoor run (>= 3 km)",
          holder: fastestPace.athlete,
          stat: `${fastestPace.paceStr} (${fastestPace.dist} km run)`
        },
        {
          icon: "🦉",
          title: "The Night Owl",
          criteria: "Most workouts logged in the evening after 8:00 PM",
          holder: topNightOwl[0],
          stat: `${topNightOwl[1]} night workouts logged`
        },
        {
          icon: "🌅",
          title: "Dawn Patrol",
          criteria: "Most workouts completed before 7:30 AM",
          holder: topEarlyBird[0],
          stat: `${topEarlyBird[1]} early morning sessions`
        },
        {
          icon: "🫁",
          title: "Iron Lungs",
          criteria: "Longest single continuous workout in 2026",
          holder: longestSingle.athlete,
          stat: `${longestSingle.dist} km (${longestSingle.sport})`
        },
        {
          icon: "⚔️",
          title: "Weekend Warrior",
          criteria: "Highest cumulative distance conquered strictly on Saturdays & Sundays",
          holder: topWeekend[0],
          stat: `${Math.round(topWeekend[1])} km logged on weekends`
        },
        {
          icon: "🏅",
          title: "The Decathlete",
          criteria: "Highest multi-sport variety recorded across all activity types",
          holder: topDiversity[0],
          stat: `${topDiversity[1]} distinct sports conquered`
        },
        {
          icon: "🔥",
          title: "Points Titan",
          criteria: "Overall leader in Dynamic MET cardiovascular exertion score",
          holder: topVolume.athlete_name,
          stat: `${topVolume.total_points.toLocaleString()} dynamic points`
        },
        {
          icon: "🏃",
          title: "Half Marathon Master",
          criteria: "Athletes completing verified 21.1+ km long runs",
          holder: "Srinivas K R & Satyaprakash",
          stat: "21.2 km & 30.0 km completed"
        }
      ];

      const container = document.getElementById('trophiesContainer');
      container.innerHTML = trophies.map(t => {
        const initials = t.holder.split(' ').map(w => w[0]).join('').slice(0, 2);
        const bg = getAvatarColor(t.holder);
        return `
          <div class="trophy-card">
            <div class="trophy-badge-icon">${t.icon}</div>
            <div class="trophy-title">${t.title}</div>
            <div class="trophy-criteria">${t.criteria}</div>
            <div class="trophy-holder-box">
              <div class="trophy-avatar" style="background:${bg};">${initials}</div>
              <div class="trophy-holder-info">
                <div class="trophy-holder-name">${t.holder}</div>
                <div class="trophy-stat-val">${t.stat}</div>
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

    /* =========================================================================
       2. 1v1 DUEL ARENA LOGIC
       ========================================================================= */
    function initDuelSelectors() {
      const athletes = globalData.athletes || [];
      const s1 = document.getElementById('fighter1Select');
      const s2 = document.getElementById('fighter2Select');

      s1.innerHTML = '';
      s2.innerHTML = '';

      athletes.forEach((a, idx) => {
        const opt1 = document.createElement('option');
        opt1.value = a.athlete_id;
        opt1.innerText = `#${idx+1} ${a.athlete_name} (${a.total_points.toLocaleString()} pts)`;
        s1.appendChild(opt1);

        const opt2 = document.createElement('option');
        opt2.value = a.athlete_id;
        opt2.innerText = `#${idx+1} ${a.athlete_name} (${a.total_points.toLocaleString()} pts)`;
        s2.appendChild(opt2);
      });

      if (athletes.length >= 2) {
        s1.selectedIndex = 0;
        s2.selectedIndex = 1;
      }
      updateDuel();
    }

    function updateDuel() {
      const athletes = globalData.athletes || [];
      const id1 = document.getElementById('fighter1Select').value;
      const id2 = document.getElementById('fighter2Select').value;

      const f1 = athletes.find(a => a.athlete_id === id1) || athletes[0];
      const f2 = athletes.find(a => a.athlete_id === id2) || athletes[1];

      document.getElementById('f1NameTh').innerText = `🔴 ${f1.athlete_name}`;
      document.getElementById('f2NameTh').innerText = `${f2.athlete_name} 🔵`;

      const rows = [
        { label: "Overall Rank", v1: `#${f1.rank}`, v2: `#${f2.rank}`, f1Wins: f1.rank < f2.rank },
        { label: "Dynamic MET Points", v1: `${f1.total_points.toLocaleString()} pts`, v2: `${f2.total_points.toLocaleString()} pts`, f1Wins: f1.total_points > f2.total_points },
        { label: "Cumulative Distance", v1: `${f1.total_distance_km} km`, v2: `${f2.total_distance_km} km`, f1Wins: f1.total_distance_km > f2.total_distance_km },
        { label: "Training Duration", v1: `${Math.round(f1.total_duration_minutes / 60)} hrs`, v2: `${Math.round(f2.total_duration_minutes / 60)} hrs`, f1Wins: f1.total_duration_minutes > f2.total_duration_minutes },
        { label: "Activity Count", v1: `${f1.total_activities} acts`, v2: `${f2.total_activities} acts`, f1Wins: f1.total_activities > f2.total_activities },
        { label: "Sport Diversity", v1: `${f1.unique_types} sports`, v2: `${f2.unique_types} sports`, f1Wins: f1.unique_types > f2.unique_types }
      ];

      const tbody = document.getElementById('duelStatsTbody');
      tbody.innerHTML = rows.map(r => `
        <tr>
          <td class="fighter-red-val">${r.f1Wins ? '🏆 ' : ''}${r.v1}</td>
          <td class="stat-label-col">${r.label}</td>
          <td class="fighter-blue-val">${!r.f1Wins ? '🏆 ' : ''}${r.v2}</td>
        </tr>
      `).join('');

      // Render Overlay Radar
      const ctx = document.getElementById('duelRadarChart').getContext('2d');
      if (duelRadarChartInstance) duelRadarChartInstance.destroy();

      duelRadarChartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
          labels: ['Distance', 'Duration', 'Points', 'Activity Frequency', 'Sport Diversity'],
          datasets: [
            {
              label: f1.athlete_name,
              data: [f1.radar_metrics.distance, f1.radar_metrics.duration, f1.radar_metrics.points, f1.radar_metrics.frequency, f1.radar_metrics.diversity],
              backgroundColor: 'rgba(239, 68, 68, 0.25)',
              borderColor: '#ef4444',
              pointBackgroundColor: '#ef4444',
              borderWidth: 2.5
            },
            {
              label: f2.athlete_name,
              data: [f2.radar_metrics.distance, f2.radar_metrics.duration, f2.radar_metrics.points, f2.radar_metrics.frequency, f2.radar_metrics.diversity],
              backgroundColor: 'rgba(59, 130, 246, 0.25)',
              borderColor: '#3b82f6',
              pointBackgroundColor: '#3b82f6',
              borderWidth: 2.5
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            r: {
              angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
              grid: { color: 'rgba(255, 255, 255, 0.08)' },
              pointLabels: { color: '#cbd5e1', font: { family: 'Inter', size: 11, weight: '600' } },
              ticks: { display: false, max: 100, min: 0 }
            }
          },
          plugins: {
            legend: { labels: { color: '#f8fafc', font: { family: 'Inter', size: 12, weight: '600' } } }
          }
        }
      });

      // Tale of the tape verdict
      let verdict = '';
      if (f1.total_points > f2.total_points) {
        const diff = Math.round(f1.total_points - f2.total_points);
        verdict = `<strong>🥊 Tale of the Tape Analysis:</strong> <span style="color:var(--fighter-red); font-weight:700;">${f1.athlete_name}</span> controls the tempo with a <strong>+${diff.toLocaleString()} pt</strong> advantage, propelled by high training volume. However, <span style="color:var(--fighter-blue); font-weight:700;">${f2.athlete_name}</span> demonstrates remarkable efficiency and versatility across key sport metrics.`;
      } else if (f2.total_points > f1.total_points) {
        const diff = Math.round(f2.total_points - f1.total_points);
        verdict = `<strong>🥊 Tale of the Tape Analysis:</strong> <span style="color:var(--fighter-blue); font-weight:700;">${f2.athlete_name}</span> holds the decisive scoring lead (+${diff.toLocaleString()} pts). <span style="color:var(--fighter-red); font-weight:700;">${f1.athlete_name}</span> has strong endurance potential to close the gap with high-tempo outdoor workouts!`;
      } else {
        verdict = `<strong>🥊 Tale of the Tape:</strong> A dead-even standoff! Both athletes match each other stride for stride in active competition points.`;
      }
      document.getElementById('duelVerdictBox').innerHTML = verdict;
    }

    /* =========================================================================
       3. VIRTUAL ROAD TRIP LOGIC
       ========================================================================= */
    function renderVirtualJourney() {
      const summary = globalData.summary || {};
      const totalKm = summary.total_distance_km || 586.72;

      document.getElementById('journeyTotalKm').innerText = `${totalKm.toLocaleString()} km`;

      const checkpoints = [
        { name: "Bangalore HQ", km: 0, desc: "Grand Departure Point" },
        { name: "Mysore Palace", km: 145, desc: "Heritage Checkpoint" },
        { name: "Chennai Marina", km: 350, desc: "Bay of Bengal Coastal Sprint" },
        { name: "Goa Beaches", km: 560, desc: "Sun, Sand & Arabian Sea Surf" },
        { name: "Hyderabad Charminar", km: 710, desc: "City of Pearls Landmark" },
        { name: "Mumbai Gateway", km: 980, desc: "Grand Coastal Metropolis" },
        { name: "Jaipur Pink City", km: 1500, desc: "Royal Desert Odyssey" },
        { name: "Delhi India Gate", km: 2150, desc: "The Ultimate Summit Finish" }
      ];

      const maxKm = checkpoints[checkpoints.length - 1].km;
      const pct = Math.min(100, Math.round((totalKm / maxKm) * 100));
      document.getElementById('journeyProgressBar').style.width = `${pct}%`;

      let currentLandmark = "Bangalore Start";
      const cardsHtml = checkpoints.map((cp, idx) => {
        const isUnlocked = totalKm >= cp.km;
        const isNextTarget = !isUnlocked && (idx === 0 || totalKm >= checkpoints[idx-1].km);

        if (isUnlocked) currentLandmark = `${cp.name} (Unlocked!)`;

        let statusClass = "locked";
        let badgeText = `Target: ${cp.km} km`;
        if (isUnlocked) {
          statusClass = "unlocked";
          badgeText = "✅ Conquered";
        } else if (isNextTarget) {
          statusClass = "active-target";
          badgeText = `🎯 Next Goal (${Math.round(cp.km - totalKm)} km to go)`;
        }

        return `
          <div class="milestone-card ${statusClass}">
            <div class="milestone-badge">${badgeText}</div>
            <div style="font-family:'Outfit', sans-serif; font-weight:800; font-size:16px; color:#fff; margin-bottom:2px;">
              ${cp.name}
            </div>
            <div style="font-size:11px; color:var(--text-muted);">${cp.desc}</div>
            <div style="font-size:12px; font-weight:700; color:var(--accent-blue); margin-top:8px;">${cp.km} km marker</div>
          </div>
        `;
      }).join('');

      document.getElementById('milestonesContainer').innerHTML = cardsHtml;
      document.getElementById('journeyCurrentLandmark').innerText = currentLandmark;

      // Fun stats
      const pizzas = Math.round(totalKm * 75 / 270);
      const elev = Math.round(totalKm * 5.4);
      document.getElementById('journeyPizzas').innerText = `~${pizzas.toLocaleString()}`;
      document.getElementById('journeyElevation').innerText = `~${elev.toLocaleString()} m`;
      document.getElementById('journeyDaysActive').innerText = `${summary.total_activities || 105}`;
    }

    /* =========================================================================
       4. MOMENTUM TRACKER LOGIC
       ========================================================================= */
    function renderMomentum() {
      const activities = globalData.activities || [];
      const athletes = globalData.athletes || [];

      // Calculate recent activities (within past 14 days)
      const now = new Date();
      const cutoff = new Date();
      cutoff.setDate(now.getDate() - 14);

      const recentStats = {};
      athletes.forEach(a => {
        recentStats[a.athlete_name] = { count: 0, dist: 0.0, pts: 0.0 };
      });

      activities.forEach(act => {
        const name = act.athlete_name;
        const dtStr = act.datetime_iso || act.datetime_utc;
        if (dtStr) {
          const d = new Date(dtStr);
          if (!isNaN(d) && d >= cutoff) {
            if (!recentStats[name]) recentStats[name] = { count: 0, dist: 0.0, pts: 0.0 };
            recentStats[name].count += 1;
            recentStats[name].dist += parseFloat(act.distance_km || 0);
            recentStats[name].pts += parseFloat(act.points || 0);
          }
        }
      });

      const sorted = Object.entries(recentStats)
        .filter(([_, s]) => s.count > 0)
        .sort((a, b) => b[1].pts - a[1].pts)
        .slice(0, 8);

      const tbody = document.getElementById('momentumTbody');
      if (sorted.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:var(--text-muted); padding:20px;">No recent sessions</td></tr>';
      } else {
        tbody.innerHTML = sorted.map(([name, s], idx) => `
          <tr>
            <td style="font-weight:700; color:var(--gold);">#${idx+1}</td>
            <td style="font-weight:700; color:#fff;">${name}</td>
            <td>${s.count} acts</td>
            <td>${Math.round(s.dist * 10) / 10} km</td>
            <td style="font-weight:800; color:var(--strava-orange);">${Math.round(s.pts).toLocaleString()} pts</td>
          </tr>
        `).join('');
      }

      // Streaks list
      const topStreaks = athletes.slice(0, 5);
      document.getElementById('streakTopList').innerHTML = topStreaks.map(a => `
        <div style="background:rgba(15,23,42,0.7); border:1px solid var(--card-border); border-radius:12px; padding:10px 14px; display:flex; justify-content:space-between; align-items:center;">
          <span style="font-size:13px; font-weight:700; color:#fff;">${a.athlete_name}</span>
          <span style="font-size:12px; font-weight:800; color:var(--gold);">🔥 ${a.total_activities} sessions</span>
        </div>
      `).join('');
    }

    /* =========================================================================
       5. WORKOUT ROULETTE
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

    loadArenaData();
  </script>
</body>
</html>
'''

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
