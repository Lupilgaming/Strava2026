# 🏃‍♂️ Strava 2026 Club Leaderboard & Analytics

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Site-orange?logo=github)](https://lupilgaming.github.io/Strava2026/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Live interactive leaderboard and multi-dimensional analytics dashboard for the Strava Connectivity Sports Day 2026 club competition.

🌐 **Live Dashboard**: [https://lupilgaming.github.io/Strava2026/](https://lupilgaming.github.io/Strava2026/)

---

## 🏆 Features

- **Status Hero Cards**: Real-time aggregated metrics for Total Athletes, Activities, Distance (km), Duration (hrs), and Club Total Points.
- **Top 3 Podium**: Gold 🥇, Silver 🥈, and Bronze 🥉 cards with glowing badges and summary stats.
- **5-Axis Athlete Radar (Spider Chart)**: Standardized multi-dimensional comparison across Distance, Duration, Points, Activity Frequency, and Sport Diversity. Includes interactive athlete toggle pills.
- **Activity Type Breakdown**: Donut chart showing distribution across Run, Ride, Weight Training, Swim, Walk, and Workout.
- **Dynamic Filters**: Instant search by athlete name, sport dropdown, date range filter (All Time, Past 7/14/20/30 Days, Custom Range), and sort options.
- **Leaderboard Table**: Sticky dark glass table with rank medals, athlete avatars, sport badges, distance, duration, and points.
- **Athlete Detail Modal**: Click any athlete to view their complete activity log with dates, distances, durations, points, and direct links to Strava activities.
- **Instant CSV Export**: Download the full activity dataset directly from the dashboard.

---

## 📊 Scoring Formula

- **Walk**: 100 points per km
- **Run / Trail Run**: 120 points per km
- **Ride / Virtual Ride / E-Bike**: 40 points per km
- **Other Activities (Weight Training, Swim, Workout, Hike)**: 10 points per minute of duration

---

## 🚀 Local Development

To view the dashboard locally:
```bash
python -m http.server 8000
```
Then open `http://localhost:8000` in your browser.
