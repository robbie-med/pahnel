# PanelTracker

Lightweight patient panel management for family medicine. Runs locally, fast, no external dependencies beyond Python + Flask.

## Quick Start

```bash
pip3 install flask
python3 seed.py    # Load demo data (15 patients, 2 families)
python3 app.py     # Start server on http://localhost:5000
```

Open http://localhost:5000 in your browser.

## Starting Fresh (No Demo Data)

```bash
rm panel.db
python3 app.py
```

The database initializes automatically on first run. Add patients from the UI.

## Features

- **Dashboard** — overdue reminders, meds running out, pending labs, pending referrals, overdue screenings, upcoming visits
- **Patient directory** — search by name/phone, filter by tag or active problem
- **Patient chart** — allergies (always visible), sticky notes, problems, medications, labs, preventive care, referrals, family tree, contact log
- **Medication tracking** — auto-calculates run-out dates, warns before meds expire
- **Preventive care engine** — age/sex-based screening rules (colonoscopy, mammogram, pap, lipids, A1c, DEXA, vaccines, etc.)
- **Family trees** — interactive vis.js graph, cross-linked between patients
- **Referral tracking** — consult sent/received workflow
- **Contact log** — timestamped call/visit notes
- **Tags** — freeform labels (pregnant, palliative, snowbird, etc.)
- **Chronic disease registries** — one-click filter by condition across your panel
- **Visit prep** — pre-visit checklist pulling all gaps, overdue items, pending results
- **Reminder popups** — browser notifications for overdue tasks
- **Scales** — SQLite with WAL mode + indexes, handles 2,500+ patients easily

## Tech Stack

- Python 3 + Flask
- SQLite (single file: `panel.db`)
- Vanilla HTML/CSS/JS (no build step)
- vis.js for family tree visualization
