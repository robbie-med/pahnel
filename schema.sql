-- PanelTracker schema

CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    dob TEXT NOT NULL,  -- ISO date
    sex TEXT NOT NULL CHECK(sex IN ('M','F','O')),
    phone TEXT,
    email TEXT,
    address TEXT,
    pharmacy TEXT,
    preferred_contact TEXT DEFAULT 'phone' CHECK(preferred_contact IN ('phone','email','mail')),
    notes TEXT,  -- sticky note
    active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_patients_name ON patients(last_name, first_name);
CREATE INDEX IF NOT EXISTS idx_patients_dob ON patients(dob);
CREATE INDEX IF NOT EXISTS idx_patients_active ON patients(active);

CREATE TABLE IF NOT EXISTS family_relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    related_patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    relationship TEXT NOT NULL,  -- 'spouse','parent','child','sibling'
    UNIQUE(patient_id, related_patient_id)
);

CREATE INDEX IF NOT EXISTS idx_family_patient ON family_relationships(patient_id);
CREATE INDEX IF NOT EXISTS idx_family_related ON family_relationships(related_patient_id);

CREATE TABLE IF NOT EXISTS allergies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    allergen TEXT NOT NULL,
    reaction TEXT,
    severity TEXT DEFAULT 'moderate' CHECK(severity IN ('mild','moderate','severe')),
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_allergies_patient ON allergies(patient_id);

CREATE TABLE IF NOT EXISTS problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    status TEXT DEFAULT 'active' CHECK(status IN ('active','inactive','resolved')),
    onset_date TEXT,
    resolved_date TEXT,
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_problems_patient ON problems(patient_id);
CREATE INDEX IF NOT EXISTS idx_problems_status ON problems(status);

CREATE TABLE IF NOT EXISTS medications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    dose TEXT,
    frequency TEXT,
    quantity_dispensed INTEGER,
    days_supply INTEGER,
    last_filled_date TEXT,  -- ISO date
    refills_remaining INTEGER,
    prescriber_notes TEXT,
    active INTEGER DEFAULT 1,
    remind_days_before INTEGER DEFAULT 7,  -- days before run-out to remind
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_meds_patient ON medications(patient_id);
CREATE INDEX IF NOT EXISTS idx_meds_active ON medications(active);
CREATE INDEX IF NOT EXISTS idx_meds_runout ON medications(last_filled_date, days_supply);

CREATE TABLE IF NOT EXISTS labs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    test_name TEXT NOT NULL,
    ordered_date TEXT NOT NULL,
    result_date TEXT,
    result_value TEXT,
    status TEXT DEFAULT 'pending' CHECK(status IN ('ordered','pending','resulted','reviewed')),
    followup_needed INTEGER DEFAULT 0,
    followup_notes TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_labs_patient ON labs(patient_id);
CREATE INDEX IF NOT EXISTS idx_labs_status ON labs(status);

CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    reason TEXT,
    due_date TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    completed_date TEXT,
    auto_generated INTEGER DEFAULT 0,  -- 1 if system-generated (med refill, screening)
    source_type TEXT,  -- 'medication','preventive','lab','referral','manual'
    source_id INTEGER,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_reminders_due ON reminders(due_date);
CREATE INDEX IF NOT EXISTS idx_reminders_patient ON reminders(patient_id);
CREATE INDEX IF NOT EXISTS idx_reminders_completed ON reminders(completed);

CREATE TABLE IF NOT EXISTS contact_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    contact_date TEXT DEFAULT (datetime('now')),
    method TEXT DEFAULT 'phone' CHECK(method IN ('phone','email','mail','in_person','portal','other')),
    summary TEXT NOT NULL,
    followup_needed INTEGER DEFAULT 0,
    followup_date TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_contact_patient ON contact_log(patient_id);
CREATE INDEX IF NOT EXISTS idx_contact_date ON contact_log(contact_date);

CREATE TABLE IF NOT EXISTS referrals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    specialty TEXT NOT NULL,
    provider_name TEXT,
    reason TEXT,
    date_sent TEXT NOT NULL,
    consult_received INTEGER DEFAULT 0,
    consult_date TEXT,
    followup_needed INTEGER DEFAULT 0,
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_referrals_patient ON referrals(patient_id);
CREATE INDEX IF NOT EXISTS idx_referrals_pending ON referrals(consult_received);

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    color TEXT DEFAULT '#6b7280'
);

CREATE TABLE IF NOT EXISTS patient_tags (
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY(patient_id, tag_id)
);

CREATE INDEX IF NOT EXISTS idx_ptags_patient ON patient_tags(patient_id);
CREATE INDEX IF NOT EXISTS idx_ptags_tag ON patient_tags(tag_id);

-- Preventive care rules: define what screenings are due based on age/sex
CREATE TABLE IF NOT EXISTS preventive_care_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,  -- e.g. "Colonoscopy"
    description TEXT,
    sex TEXT CHECK(sex IN ('M','F','A')),  -- A = all
    min_age INTEGER,
    max_age INTEGER,
    interval_months INTEGER,  -- how often in months
    category TEXT  -- 'screening','immunization','lab'
);

-- Track when each patient last had each preventive item
CREATE TABLE IF NOT EXISTS preventive_care_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    rule_id INTEGER NOT NULL REFERENCES preventive_care_rules(id),
    last_done_date TEXT,
    next_due_date TEXT,
    status TEXT DEFAULT 'due' CHECK(status IN ('due','overdue','completed','declined','not_applicable')),
    notes TEXT,
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_prev_patient ON preventive_care_items(patient_id);
CREATE INDEX IF NOT EXISTS idx_prev_status ON preventive_care_items(status);
CREATE INDEX IF NOT EXISTS idx_prev_due ON preventive_care_items(next_due_date);

-- Upcoming visits for pre-visit prep
CREATE TABLE IF NOT EXISTS upcoming_visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    visit_date TEXT NOT NULL,
    visit_type TEXT DEFAULT 'routine',
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_visits_date ON upcoming_visits(visit_date);
CREATE INDEX IF NOT EXISTS idx_visits_patient ON upcoming_visits(patient_id);
