# CLAUDE.md — PanelTracker

## What This Is

PanelTracker is a **local, lightweight patient panel management app** for a family medicine doctor. It is NOT an EHR, billing system, or imaging viewer. It exists to prevent the doctor from forgetting to do things for patients — follow up on labs, refill meds, complete screenings, track referrals, and remember personal context.

The user is a family physician. Speak their language. Respect clinical workflows.

## How to Run

```bash
python3 seed.py    # optional: loads 15 demo patients
python3 app.py     # starts on http://localhost:5000
```

Requires: Python 3.10+, Flask 3.1+ (`pip3 install flask`). No npm, no build step, no external services.

To start fresh: `rm panel.db && python3 app.py` (DB auto-creates on boot).

## Tech Stack

| Layer | Tech | Notes |
|-------|------|-------|
| Backend | Python 3 + Flask | Single file: `app.py` |
| Database | SQLite | Single file: `panel.db`, WAL mode, foreign keys ON |
| Frontend | Vanilla JS SPA | Single file: `static/js/app.js`, no framework |
| Styling | Vanilla CSS | `static/css/style.css`, CSS custom properties |
| Family trees | vis.js | Loaded from CDN in `templates/index.html` |
| Notifications | Browser Notifications API | Requests permission on load, checks every 5 min |

## File Map

```
krspt/
├── app.py                    # Flask backend — ALL routes, DB init, helpers
├── schema.sql                # SQLite DDL — all CREATE TABLE + indexes
├── seed.py                   # Demo data generator (15 patients, 2 families)
├── panel.db                  # SQLite database (auto-created, gitignored)
├── requirements.txt          # Just flask
├── templates/
│   └── index.html            # Single HTML shell — sidebar nav, JS/CSS includes
└── static/
    ├── css/style.css          # All styles — CSS custom properties, no preprocessor
    └── js/app.js              # Entire SPA — routing, rendering, API calls, modals
```

## Database Schema (schema.sql)

12 tables, all with proper indexes:

| Table | Purpose | Key columns |
|-------|---------|-------------|
| `patients` | Core demographics | first_name, last_name, dob, sex, phone, email, pharmacy, notes (sticky note), active |
| `family_relationships` | Bidirectional links | patient_id, related_patient_id, relationship (spouse/parent/child/sibling) |
| `allergies` | Per-patient | allergen, reaction, severity (mild/moderate/severe) |
| `problems` | Problem list | description, status (active/inactive/resolved), onset_date, resolved_date |
| `medications` | Med list with run-out tracking | name, dose, frequency, days_supply, last_filled_date, refills_remaining, remind_days_before |
| `labs` | Lab orders + results | test_name, ordered_date, result_date, result_value, status (ordered/pending/resulted/reviewed), followup_needed |
| `reminders` | Manual + auto-generated alerts | title, reason, due_date, completed, source_type (medication/preventive/lab/referral/manual) |
| `contact_log` | Call/visit/message log | contact_date, method (phone/email/in_person/portal/mail), summary, followup_needed |
| `referrals` | Referral tracking | specialty, provider_name, reason, date_sent, consult_received, consult_date |
| `tags` + `patient_tags` | Freeform colored labels | name, color; many-to-many with patients |
| `preventive_care_rules` | Age/sex screening rules | name, sex (M/F/A), min_age, max_age, interval_months, category (screening/immunization/lab) |
| `preventive_care_items` | Per-patient tracking | rule_id, last_done_date, next_due_date, status (due/overdue/completed/declined/not_applicable) |
| `upcoming_visits` | Scheduled visits | visit_date, visit_type, notes |

**Key design decisions:**
- All dates stored as ISO strings (YYYY-MM-DD)
- Medication run-out computed dynamically: `date(last_filled_date, '+' || days_supply || ' days')`
- Family relationships auto-create inverse (add parent → auto-adds child on other side)
- Preventive care items auto-generated per patient on creation based on age/sex rules
- When a preventive item is marked completed with a date, next_due_date auto-computes from interval_months
- `patients.notes` field = the yellow sticky note shown at top of chart
- `patients.active` = soft delete flag (default 1)

## Backend Architecture (app.py)

**Single Flask app, ~790 lines.** All routes under `/api/`.

### DB lifecycle
- `get_db()` — per-request connection from `flask.g`, with WAL + foreign keys
- `init_db()` — runs `schema.sql` + seeds preventive care rules (16 default rules) on first boot
- Auto-initializes via `with app.app_context(): init_db()` at module load

### API Routes

**Dashboard:**
- `GET /api/dashboard` — aggregates: overdue reminders (7-day window), meds running out (14 days), pending labs, pending referrals, overdue preventive care, upcoming visits (7 days), total patient count

**Patients:**
- `GET /api/patients?q=&tag=&problem=&page=&per_page=` — search/filter with pagination, tags attached inline
- `POST /api/patients` — create + auto-generate preventive care items
- `GET /api/patients/<id>` — full chart: demographics, age, allergies, problems, meds (with computed run_out_date), labs, reminders, contact_log, referrals, preventive_care, upcoming_visits, tags, family
- `PUT /api/patients/<id>` — update any demographic field

**Family:**
- `POST /api/patients/<id>/family` — link family member (auto-creates inverse relationship)
- `DELETE /api/patients/<id>/family/<related_id>` — unlink both directions
- `GET /api/patients/<id>/family-tree` — returns vis.js-ready `{nodes, edges}` via recursive walk (depth 3)

**Clinical data (all follow same pattern: POST to add, PUT to update, DELETE to remove):**
- `/api/patients/<id>/allergies`, `/api/allergies/<id>`
- `/api/patients/<id>/problems`, `/api/problems/<id>`
- `/api/patients/<id>/medications`, `/api/medications/<id>`
- `/api/patients/<id>/labs`, `/api/labs/<id>`
- `/api/patients/<id>/reminders`, `/api/reminders/<id>`
- `/api/patients/<id>/contacts`
- `/api/patients/<id>/referrals`, `/api/referrals/<id>`
- `/api/patients/<id>/tags`, `/api/patients/<id>/tags/<tag_id>`
- `/api/preventive/<id>` (PUT only)
- `/api/patients/<id>/visits`, `/api/visits/<id>`

**Tags:**
- `GET /api/tags` — all tags with patient_count
- `POST /api/tags` — create standalone tag
- Tag-add on patient auto-creates tag if name doesn't exist yet

**Visit prep:**
- `GET /api/patients/<id>/visit-prep` — aggregates overdue preventive, pending labs, pending referrals, open reminders, meds running out (30 days), active problems

### Backend patterns
- All update endpoints use dynamic field building: loop over allowed columns, build SET clause
- `dict_row()`/`dict_rows()` convert sqlite3.Row to plain dicts for JSON serialization
- `compute_age(dob_str)` — exact age calculation from ISO date string
- `INVERSE_REL` dict maps relationship → inverse (spouse↔spouse, parent↔child, sibling↔sibling)

## Frontend Architecture (static/js/app.js)

**~1460 lines, vanilla JS SPA.** No router library — uses a `navigate(page, data)` function that renders into `#main-content`.

### Navigation
`navigate(page, data)` — switches between: `dashboard`, `patients`, `patient` (with patient ID), `registry`, `reminders`

### Pages
- **Dashboard** (`renderDashboard`) — 6 stat cards + 6 data panels (overdue reminders, meds running out, pending labs, pending referrals, overdue screenings, upcoming visits)
- **Patient list** (`renderPatientList`) — search bar (debounced 300ms), tag dropdown filter, problem text filter, paginated table
- **Patient chart** (`renderPatientChart`) — header (demographics, tags, action buttons), allergy banner, sticky note, 8 tabs:
  - Overview: 4-panel summary (active problems, open reminders, current meds, action items)
  - Problems: active/resolved split, add/resolve/delete
  - Medications: active/discontinued, refill/edit/stop actions, run-out date coloring
  - Labs: order/update/review workflow with follow-up tracking
  - Preventive Care: due/completed/declined sections, done/decline actions
  - Referrals: add/mark-consult-received workflow
  - Family: vis.js interactive tree + table, link/unlink
  - Contact Log: timestamped entries with method and follow-up tracking
- **Registries** (`renderRegistry`) — quick-filter buttons (Diabetes, HTN, CHF, COPD, Asthma, etc.) + freeform problem search
- **Reminders** (`renderRemindersPage`) — overdue + upcoming split view

### UI patterns
- `showModal(title, bodyHtml, footerHtml)` — generic modal system, IDs prefixed `m-` for form fields
- `toast(msg, type)` — auto-dismiss notification (3.5s)
- `esc(str)` — HTML entity escaping via textContent/innerHTML trick
- `escAttr(str)` — attribute escaping for quotes
- Date display: `formatDate()` → "Jan 15, 2026", `formatDateTime()` adds time
- Urgency coloring: `.overdue` (red, bold) for past-due, `.due-soon` (amber) for within 14 days

### Reminder popup system
- `checkReminders()` runs every 5 minutes via `setInterval`, plus 10s after load
- Sends browser `Notification` if overdue items exist and permission granted
- Shows in-app `.reminder-popup` (bottom-right, animated) for most urgent item
- Actions: Open Chart, Done, Dismiss

### Family tree (vis.js)
- `initFamilyTree(pid)` — fetches `/api/patients/<id>/family-tree`, renders vis.Network
- Hierarchical layout (top-down), color-coded by sex (blue M, pink F, purple O)
- Click a node → navigates to that patient's chart

## CSS Architecture (static/css/style.css)

~617 lines. CSS custom properties in `:root` for theming. Key design tokens:
- Colors: `--primary` (blue), `--danger` (red), `--warning` (amber), `--success` (green), `--info` (cyan)
- Layout: fixed 220px sidebar, main content max-width 1200px
- Components: `.card`, `.data-table`, `.badge`, `.btn`, `.tag`, `.modal-overlay`, `.sticky-note`, `.allergy-banner`, `.tabs`, `.toast`, `.reminder-popup`
- Responsive: dashboard grid collapses to 1 column below 900px

## Demo Data (seed.py)

Seed creates realistic clinical scenarios:

**Martinez family (4 patients):**
- Roberto (67M): Complex — DM2, HTN, HLD, obesity, GERD. 6 meds, pending A1c/CMP, referrals to ophtho/podiatry
- Maria (64F): OA, hypothyroidism, depression. Sticky note: "husband dying, Spanish-speaking"
- Elena (37F): Anxiety, migraine. Interprets for mother
- Carlos (33M): Healthy young adult

**Chen family (4 patients):**
- James (51M): HTN, low back pain. Active PT, pending ortho consult
- Susan (47F): Asthma, iron deficiency anemia. Pending CBC/iron follow-up
- Lily (15F), Max (11M): Pediatric patients

**Solo patients (7):**
- Dorothy Williams (83F): Complex elderly — AFib, CHF, COPD, osteoporosis, DM2. 6 meds, DNR/DNI
- Ahmed Hassan (39M): GERD only
- Priya Patel (35F): Pregnant with GDM, needle phobia
- William Thompson (75M): Prostate cancer (active surveillance), HTN, BPH. Snowbird
- Margaret O'Brien (60F): DM2 (can't tolerate metformin), HTN, obesity. Needs GLP-1 RA discussion
- Jamal Washington (30M): Moderate persistent asthma
- Linda Garcia (53F): Fibromyalgia, HTN, insomnia

**Tags used:** diabetes, hypertension, CHF, COPD, pregnant, elderly, complex, asthma, cancer, palliative

## Scaling Notes

Designed for 100-2500 patients:
- SQLite WAL mode for concurrent read performance
- Indexes on all FK columns, status fields, date fields
- Patient list paginated (default 50/page)
- Dashboard queries use LIMIT 50
- No N+1 queries — tags batch-loaded for patient list
- Family tree walk capped at depth 3

## Known Limitations / Future Work

- No authentication (local-only tool, trusts the user)
- No data export/import (could add CSV)
- No undo for deletions
- Preventive care rules are hardcoded; could be made user-editable
- Registry search is problem-text-only; could also search by medication name
- No keyboard shortcuts
- Sticky note edit button passes content via onclick attribute — may break with quotes/special chars in long notes (could use data attributes instead)
- vis.js loaded from CDN — needs internet on first load (could vendor it)
