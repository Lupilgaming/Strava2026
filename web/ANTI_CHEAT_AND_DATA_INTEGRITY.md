# 🛡️ Strava 2026 Club Leaderboard: Anti-Cheating, Data Integrity & Scoring Engine

This document provides the complete architectural specification for automated data sanitization, anomaly recovery, dynamic pace classification, and scoring schema design for the Strava 2026 Club Leaderboard.

---

## 1. Executive Summary & Data Integrity Principles

```
                             RAW ACTIVITY DATA
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         ▼                           ▼                           ▼
 ┌───────────────┐           ┌───────────────┐           ┌───────────────┐
 │ Group Feed    │           │ Clock Runaway │           │ Missing /     │
 │ Leakage       │           │ (> 10 hrs /   │           │ Incomplete    │
 │ (18 acts)     │           │ paused break) │           │ Data Points   │
 └───────┬───────┘           └───────┬───────┘           └───────┬───────┘
         └───────────────────────────┼───────────────────────────┘
                                     ▼
                     ┌───────────────────────────────┐
                     │     DATA INTEGRITY PIPELINE   │
                     │ 1. Ownership & Membership     │
                     │ 2. Moving Time Normalization  │
                     │ 3. Automated Data Recovery    │
                     │ 4. Dynamic Pace Segregation   │
                     └───────────────┬───────────────┘
                                     ▼
                     VERIFIED LEADERBOARD DATASET
```

### Foundational Pillars:
1. **Activity Uniqueness**: Every `activity_id` must exist at most once across the entire platform.
2. **True DOM Ownership**: Attribution is strictly bound to the authentic activity author, never companion widgets or viewer feeds.
3. **Club Membership Verification**: Non-members appearing in scraped companion tags are isolated and prevented from entering club standings.
4. **Moving Time as Primary Measure**: Idle pauses and traffic light stops are excluded from athletic scoring, while elapsed time serves as an anomaly check.
5. **Automated Recovery for Incomplete Data**: Activities with missing duration or pace are mathematically reconstructed using calibrated median athlete pacing.
6. **Wide-Threshold Walk vs. Run Segregation**: Classification utilizes calculated pace with an athlete-intent transition buffer rather than raw self-declared labels.

---

## 2. Moving Time vs. Elapsed Time Policy

Strava provides two distinct temporal metrics:
* **`moving_time`**: Filtered active duration during which GPS or accelerometer detected actual physical movement.
* **`elapsed_time`**: Total wall-clock duration from start button to stop/save button, including idle pauses, restaurant breaks, and pauses.

### Policy Rules:
1. **Primary Duration Metric**: All duration points, speed, and pace calculations shall use **`moving_time`** by default.
   $$\text{Duration}_{\text{scored}} = \text{moving\_time}$$
2. **The Runaway Clock Trap (Upper Bound)**:
   When an athlete forgets to stop their device, `moving_time` can falsely accumulate via GPS jitter or sensor drift.
   * **Rule**: If $\text{moving\_time} > 1.5 \times \text{elapsed\_time}$ (watch firmware counter overflow) OR $\text{elapsed\_time} > T_{max}(\text{sport})$, the activity triggers **Clock Runaway Normalization**.
3. **Idle Pause Inflation Trap**:
   If an athlete leaves Strava paused for 6 hours during a hike or run, $\text{elapsed\_time}$ may read 8 hours while $\text{moving\_time}$ is 1.5 hours. Taking `moving_time` prevents idle hours from inflating points.

---

## 3. Dynamic Walk vs. Run Segregation (Wide-Threshold Model)

Self-declared labels on Strava are frequently inverted:
* Athletes often label $6:20\text{ min/km}$ runs as "Walk" (e.g., Narendra Babu's $5.5\text{ km}$ at $6:26\text{ /km}$).
* Casual strolls at $14:00\text{ min/km}$ are occasionally tagged as "Run" for higher points.
* Endurance runners and beginners legitimately run/jog at $8:00 - 9:30\text{ min/km}$ (e.g., Sai Harshita's $15.0\text{ km}$ at $8:40\text{ /km}$).

To be fair to beginner runners while preventing walking from gaming run multipliers, we establish a **3-Zone Wide-Threshold Boundary Model**:

```
0:00        2:45                   7:30                              10:30               22:00
 ├───────────┼───────────────────────┼─────────────────────────────────┼───────────────────┤
 │  VEHICLE  │    UNAMBIGUOUS RUN    │      TRANSITION ZONE (WIDE)     │  UNAMBIGUOUS WALK │  GPS DRIFT
 │  (Reject) │     (120 pts/km)      │  (Honors Intent + Slow Runner)  │   (100 pts/km)    │  (Sedentary)
 └───────────┴───────────────────────┴─────────────────────────────────┴───────────────────┘
```

### Zone Definitions:

| Zone | Calculated Pace Range | Speed (km/h) | Default Classification | Scoring Multiplier Policy |
| :--- | :---: | :---: | :--- | :--- |
| **Zone 0: Vehicle / Scooter** | $< 2:45\text{ min/km}$ | $> 21.8\text{ km/h}$ | **Flagged / Rejected** | Flagged for manual review or converted to cycling if on wheels. |
| **Zone 1: Unambiguous Run** | $2:45 - 7:30\text{ min/km}$ | $8.0 - 21.8\text{ km/h}$ | **Run** | **Run Points** (120/km) regardless of self-tag. Reclassifies fast walks (e.g. Narendra Babu 6:26/km) as Runs. |
| **Zone 2: Wide Transition Band** | $7:30 - 10:30\text{ min/km}$ | $5.7 - 8.0\text{ km/h}$ | **Athlete Intent Buffer** | • If tagged as **Run**: Honored as **Run** (protects beginner runners, recovery jogs, and long-haul endurance).<br>• If tagged as **Walk**: Honored as **Walk**.<br>• If distance $> 7\text{ km}$: Elevated to Run if sustained jogging. |
| **Zone 3: Unambiguous Walk** | $10:30 - 22:00\text{ min/km}$ | $2.7 - 5.7\text{ km/h}$ | **Walk** | **Walk Points** (100/km). Activities tagged "Run" in this zone are classified as Walk to prevent gaming. |
| **Zone 4: Stationary Drift** | $> 22:00\text{ min/km}$ | $< 2.7\text{ km/h}$ | **Sedentary Pause** | Distance stripped of drift; duration normalized. |

---

## 4. Automated Recovery Action for Incomplete Data

When an activity has missing fields due to device dropout or scraper limits, our engine mathematically recovers values:

### Scenario A: Distance Recorded, Duration Missing ($0.0\text{ min}$)
* **Real-World Case**: Row 59 Walk ($7.0\text{ km}$ Walk, duration previously $0$).
* **Recovery Formula**:
  $$\text{Duration}_{\text{recovered}} = \text{Distance} \times P_{\text{baseline}}$$
  * If classified as **Run**: $P_{\text{baseline}} = \text{Median Athlete Run Pace}$ (or default $6:30\text{ min/km}$).
  * If classified as **Walk**: $P_{\text{baseline}} = \text{Median Athlete Walk Pace}$ (or default $9:30\text{ min/km}$).
  * If classified as **Outdoor Ride**: $P_{\text{baseline}} = 2.5\text{ min/km}$ ($24\text{ km/h}$).

### Scenario B: Duration Recorded, Distance Missing ($0.0\text{ km}$)
* If sport is **Ride**: Automatically classified as **Indoor Stationary Ride**.
  * Tagged `is_indoor: true`.
  * Awarded duration-based cardio points.
* If sport is **Run / Walk**: Automatically classified as **Treadmill Workout / Indoor Track**.
  * Handled via duration cardio points rather than being zeroed out.

### Scenario C: Swim Runaway Timer Normalization
* When swim moving time exceeds physical limits ($> 120\text{ min}$):
  $$\text{Corrected Duration} = \min\left(\text{Elapsed Time}, \frac{\text{Distance (meters)}}{100} \times 2.5\text{ min}\right)$$
  (Calibrated to standard master swimmer pace of $2:30\text{ /100m}$).

---

## 5. Scoring Schema Analysis & Proposed Improvements

### Current Schema Limitations:
1. **Inflation**: Scores reach $40,000+$ points, making individual workouts feel negligible.
2. **Run vs. Walk Ratio ($120 : 100$)**: Running requires $3\times$ higher cardiovascular power output than walking per minute, yet earns only $20\%$ more points per km. A $5\text{ km}$ walk ($50\text{ mins}$) gives $500\text{ pts}$, while a $5\text{ km}$ run ($25\text{ mins}$) gives $600\text{ pts}$.
3. **Gym / Swim Duration Disparity ($10\text{ pts/min} = 600\text{ pts/hr}$)**: One hour of lifting weights yields the same points as a $5\text{ km}$ run ($600\text{ pts}$) or a $15\text{ km}$ bike ride.

---

### Comparison of Proposed Schemas

| Sport | Current Legacy Schema | Option A: Normalized 100-Base (Recommended) | Option B: Caloric / MET Effort Equivalence | Option C: Balanced Legacy |
| :--- | :---: | :---: | :---: | :---: |
| **Run / Trail Run** | 120 pts / km | **100 pts / km** | 15 pts / km | 120 pts / km |
| **Walk / Hike** | 100 pts / km | **50 pts / km** | 8 pts / km | 70 pts / km |
| **Outdoor Cycling** | 40 pts / km | **25 pts / km** | 4 pts / km | 35 pts / km |
| **Indoor / Stationary Cycling** | 10 pts / min | **4 pts / min** (240/hr) | 1.5 pts / min (90/hr) | 6 pts / min (360/hr) |
| **Weight Training / Gym** | 10 pts / min | **4 pts / min** (240/hr) | 1.5 pts / min (90/hr) | 5 pts / min (300/hr) |
| **Swimming** | 10 pts / min | **5 pts / min** (300/hr) | 2.0 pts / min (120/hr) | 8 pts / min (480/hr) |

---

### Leaderboard Impact Simulation on Club Data

| Athlete | Current Points | Option A (100-Base) | Option B (Caloric/MET) | Option C (Balanced Legacy) |
| :--- | :---: | :---: | :---: | :---: |
| **Satyaprakash Karsharma** (52 acts) | 41,086.7 | **26,856.0** | 3,824.5 | **33,731.2** |
| **Muni Asheesh Potta** (7 acts) | 9,534.0 | **7,945.0** | 1,191.8 | **9,534.0** |
| **Sai Harshita** (15 acts) | 8,902.2 | **7,277.5** | 1,074.2 | **8,775.3** |
| **srikar ranganath** (8 acts) | 7,171.2 | **5,976.0** | 896.4 | **7,171.2** |
| **Srinivas K R** (2 acts) | 4,435.2 | **3,696.0** | 554.4 | **4,435.2** |
| **Divyansh** (5 acts) | 2,480.0 | **1,528.0** | 247.0 | **2,045.0** |

### Why Option A (Normalized 100-Base) is Recommended:
1. **Mental Math is Instant**: Running $1\text{ km} = 100\text{ pts}$. A $5\text{K} = 500\text{ pts}$. A $10\text{K} = 1,000\text{ pts}$.
2. **Equitable Ratios**: Walking $5\text{ km}$ ($250\text{ pts}$) vs Running $5\text{ km}$ ($500\text{ pts}$) accurately mirrors metabolic exertion.
3. **Balanced Gym/Indoor Cardio**: A 1-hour gym or indoor spinning workout ($240\text{ pts}$) equals a brisk $5\text{ km}$ walk or a moderate $2.4\text{ km}$ run, preventing non-GPS logs from dominating endurance runners.
