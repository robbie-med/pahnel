#!/usr/bin/env python3
"""Seed PanelTracker with realistic demo data."""

import sqlite3
import os
from datetime import date, timedelta
import random

DB = os.path.join(os.path.dirname(__file__), "panel.db")

def d(y, m, day):
    return date(y, m, day).isoformat()

def ago(days):
    return (date.today() - timedelta(days=days)).isoformat()

def future(days):
    return (date.today() + timedelta(days=days)).isoformat()

def seed():
    db = sqlite3.connect(DB)
    db.execute("PRAGMA foreign_keys=ON")

    # Check if already seeded
    count = db.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
    if count > 0:
        print(f"Database already has {count} patients. Skipping seed.")
        return

    # ── The Martinez Family ─────────────────────────────────────────────────

    db.execute("INSERT INTO patients (id,first_name,last_name,dob,sex,phone,email,pharmacy,address,preferred_contact) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (1, "Roberto", "Martinez", d(1958,3,15), "M", "555-0101", "roberto.m@email.com", "CVS Main St", "123 Oak Ave", "phone"))
    db.execute("INSERT INTO patients (id,first_name,last_name,dob,sex,phone,email,pharmacy,address,preferred_contact) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (2, "Maria", "Martinez", d(1960,7,22), "F", "555-0102", "maria.m@email.com", "CVS Main St", "123 Oak Ave", "phone"))
    db.execute("INSERT INTO patients (id,first_name,last_name,dob,sex,phone,email,pharmacy,address,preferred_contact) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (3, "Elena", "Martinez", d(1988,11,5), "F", "555-0103", "elena.m@email.com", "Walgreens 2nd St", "456 Elm St Apt 2B", "email"))
    db.execute("INSERT INTO patients (id,first_name,last_name,dob,sex,phone,email,pharmacy,address,preferred_contact) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (4, "Carlos", "Martinez", d(1992,4,18), "M", "555-0104", None, "CVS Main St", "789 Pine Rd", "phone"))

    # Family relationships
    for (a, b, rel) in [(1,2,"spouse"),(1,3,"parent"),(1,4,"parent"),(2,3,"parent"),(2,4,"parent"),(3,4,"sibling")]:
        inv = {"spouse":"spouse","parent":"child","child":"parent","sibling":"sibling"}[rel]
        db.execute("INSERT INTO family_relationships (patient_id,related_patient_id,relationship) VALUES (?,?,?)", (a,b,rel))
        db.execute("INSERT INTO family_relationships (patient_id,related_patient_id,relationship) VALUES (?,?,?)", (b,a,inv))

    # ── The Chen Family ─────────────────────────────────────────────────────

    db.execute("INSERT INTO patients (id,first_name,last_name,dob,sex,phone,email,pharmacy,address,preferred_contact) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (5, "James", "Chen", d(1975,1,30), "M", "555-0201", "jchen@email.com", "Rite Aid Center", "200 Maple Dr", "email"))
    db.execute("INSERT INTO patients (id,first_name,last_name,dob,sex,phone,email,pharmacy,address,preferred_contact) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (6, "Susan", "Chen", d(1978,9,12), "F", "555-0202", "susanchen@email.com", "Rite Aid Center", "200 Maple Dr", "phone"))
    db.execute("INSERT INTO patients (id,first_name,last_name,dob,sex,phone,email,pharmacy,address,preferred_contact) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (7, "Lily", "Chen", d(2010,6,3), "F", "555-0201", None, "Rite Aid Center", "200 Maple Dr", "phone"))
    db.execute("INSERT INTO patients (id,first_name,last_name,dob,sex,phone,email,pharmacy,address,preferred_contact) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (8, "Max", "Chen", d(2014,2,28), "M", "555-0201", None, "Rite Aid Center", "200 Maple Dr", "phone"))

    for (a, b, rel) in [(5,6,"spouse"),(5,7,"parent"),(5,8,"parent"),(6,7,"parent"),(6,8,"parent"),(7,8,"sibling")]:
        inv = {"spouse":"spouse","parent":"child","child":"parent","sibling":"sibling"}[rel]
        db.execute("INSERT INTO family_relationships (patient_id,related_patient_id,relationship) VALUES (?,?,?)", (a,b,rel))
        db.execute("INSERT INTO family_relationships (patient_id,related_patient_id,relationship) VALUES (?,?,?)", (b,a,inv))

    # ── Additional solo patients ────────────────────────────────────────────

    solo = [
        (9, "Dorothy", "Williams", d(1942,8,19), "F", "555-0301", None, "CVS Main St", "55 Senior Ln", "phone"),
        (10, "Ahmed", "Hassan", d(1985,12,1), "M", "555-0401", "ahmed.h@email.com", "Walgreens 2nd St", "99 Birch Ct", "email"),
        (11, "Priya", "Patel", d(1990,5,14), "F", "555-0501", "priya.p@email.com", "CVS Main St", "321 River Rd", "email"),
        (12, "William", "Thompson", d(1950,10,8), "M", "555-0601", None, "Rite Aid Center", "42 Hill St", "phone"),
        (13, "Margaret", "O'Brien", d(1965,3,25), "F", "555-0701", "mobrien@email.com", "CVS Main St", "88 Lake View", "phone"),
        (14, "Jamal", "Washington", d(1995,7,7), "M", "555-0801", "jamal.w@email.com", "Walgreens 2nd St", "150 College Ave", "email"),
        (15, "Linda", "Garcia", d(1972,11,30), "F", "555-0901", None, "CVS Main St", "67 Sunset Blvd", "phone"),
    ]
    for row in solo:
        db.execute("INSERT INTO patients (id,first_name,last_name,dob,sex,phone,email,pharmacy,address,preferred_contact) VALUES (?,?,?,?,?,?,?,?,?,?)", row)

    # ── Allergies ───────────────────────────────────────────────────────────

    allergies = [
        (1, "Penicillin", "Rash", "moderate"),
        (1, "Sulfa drugs", "Anaphylaxis", "severe"),
        (2, "Aspirin", "GI upset", "mild"),
        (5, "Codeine", "Nausea/vomiting", "moderate"),
        (9, "Latex", "Contact dermatitis", "mild"),
        (9, "Iodine contrast", "Anaphylaxis", "severe"),
        (11, "Amoxicillin", "Hives", "moderate"),
        (12, "ACE inhibitors", "Angioedema", "severe"),
        (13, "Metformin", "GI intolerance", "mild"),
    ]
    for (pid, allergen, reaction, sev) in allergies:
        db.execute("INSERT INTO allergies (patient_id,allergen,reaction,severity) VALUES (?,?,?,?)", (pid, allergen, reaction, sev))

    # ── Problems ────────────────────────────────────────────────────────────

    problems = [
        # Roberto - complex diabetic
        (1, "Type 2 Diabetes Mellitus", "active", d(2005,6,1), None, "A1c last 7.2%, on metformin + glipizide"),
        (1, "Hypertension", "active", d(2003,1,1), None, "On lisinopril 20mg + amlodipine 5mg"),
        (1, "Hyperlipidemia", "active", d(2005,6,1), None, "On atorvastatin 40mg"),
        (1, "Obesity", "active", d(2010,1,1), None, "BMI 34"),
        (1, "GERD", "active", d(2018,3,1), None, None),
        # Maria
        (2, "Osteoarthritis", "active", d(2015,9,1), None, "Bilateral knees, worse on right"),
        (2, "Hypothyroidism", "active", d(2012,4,1), None, "On levothyroxine 75mcg"),
        (2, "Depression", "active", d(2019,1,1), None, "On sertraline 100mg, stable"),
        # Elena
        (3, "Anxiety disorder", "active", d(2016,8,1), None, "On buspirone, doing CBT"),
        (3, "Migraine", "active", d(2015,1,1), None, "Sumatriptan PRN, ~2/month"),
        # James Chen
        (5, "Hypertension", "active", d(2020,3,1), None, "On losartan 50mg"),
        (5, "Low back pain", "active", d(2022,6,1), None, "MRI showed L4-L5 disc bulge, PT ongoing"),
        # Susan Chen
        (6, "Asthma", "active", d(1990,1,1), None, "Mild intermittent, albuterol PRN"),
        (6, "Iron deficiency anemia", "active", ago(90), None, "On ferrous sulfate, Hgb 10.8 last check"),
        # Dorothy Williams - elderly, complex
        (9, "Atrial fibrillation", "active", d(2018,5,1), None, "On apixaban, rate controlled with metoprolol"),
        (9, "CHF, HFpEF", "active", d(2019,2,1), None, "EF 55%, on furosemide 40mg"),
        (9, "COPD", "active", d(2010,1,1), None, "On tiotropium, former smoker"),
        (9, "Osteoporosis", "active", d(2015,8,1), None, "On alendronate, DEXA T-score -2.8"),
        (9, "Type 2 Diabetes Mellitus", "active", d(2008,1,1), None, "A1c 6.9%, on metformin"),
        # Ahmed
        (10, "GERD", "active", d(2021,5,1), None, "On omeprazole 20mg"),
        # Priya - pregnant
        (11, "Pregnancy", "active", ago(120), None, "EDD in ~5 months, routine prenatal"),
        (11, "Gestational diabetes", "active", ago(30), None, "Diet-controlled so far"),
        # William Thompson
        (12, "Prostate cancer", "active", d(2024,1,1), None, "Gleason 6, active surveillance with urology"),
        (12, "Hypertension", "active", d(2005,1,1), None, "On amlodipine 10mg (can't use ACEi)"),
        (12, "BPH", "active", d(2020,1,1), None, "On tamsulosin"),
        # Margaret
        (13, "Type 2 Diabetes Mellitus", "active", d(2018,1,1), None, "Can't tolerate metformin, on empagliflozin"),
        (13, "Hypertension", "active", d(2015,1,1), None, "On lisinopril 10mg"),
        (13, "Obesity", "active", d(2015,1,1), None, "BMI 38, discussed GLP-1 RA"),
        # Jamal
        (14, "Asthma", "active", d(2010,1,1), None, "Moderate persistent, on Advair"),
        # Linda Garcia
        (15, "Fibromyalgia", "active", d(2019,1,1), None, "On duloxetine 60mg"),
        (15, "Hypertension", "active", d(2020,1,1), None, "On lisinopril 20mg"),
        (15, "Insomnia", "active", d(2020,6,1), None, "Sleep hygiene, tried melatonin"),
    ]
    for (pid, desc, status, onset, resolved, notes) in problems:
        db.execute("INSERT INTO problems (patient_id,description,status,onset_date,resolved_date,notes) VALUES (?,?,?,?,?,?)",
            (pid, desc, status, onset, resolved, notes))

    # ── Medications ─────────────────────────────────────────────────────────

    meds = [
        # Roberto
        (1, "Metformin", "1000mg", "BID", 60, 30, ago(25), 3, 7),
        (1, "Glipizide", "10mg", "Daily", 30, 30, ago(25), 3, 7),
        (1, "Lisinopril", "20mg", "Daily", 30, 30, ago(25), 5, 7),
        (1, "Amlodipine", "5mg", "Daily", 30, 30, ago(25), 5, 7),
        (1, "Atorvastatin", "40mg", "Daily", 30, 30, ago(25), 5, 7),
        (1, "Omeprazole", "20mg", "Daily", 30, 30, ago(60), 2, 7),
        # Maria
        (2, "Levothyroxine", "75mcg", "Daily", 30, 30, ago(10), 5, 7),
        (2, "Sertraline", "100mg", "Daily", 30, 30, ago(10), 5, 7),
        (2, "Acetaminophen", "500mg", "TID PRN", 100, 30, ago(45), 99, 7),
        # Elena
        (3, "Buspirone", "10mg", "BID", 60, 30, ago(5), 5, 7),
        (3, "Sumatriptan", "50mg", "PRN", 9, 90, ago(60), 2, 14),
        # James
        (5, "Losartan", "50mg", "Daily", 30, 30, ago(18), 5, 7),
        (5, "Ibuprofen", "400mg", "TID PRN", 90, 30, ago(40), 2, 7),
        # Susan
        (6, "Albuterol inhaler", "90mcg", "Q4H PRN", 1, 90, ago(70), 3, 14),
        (6, "Ferrous sulfate", "325mg", "Daily", 30, 30, ago(15), 5, 7),
        # Dorothy - complex
        (9, "Apixaban", "5mg", "BID", 60, 30, ago(3), 5, 7),
        (9, "Metoprolol succinate", "50mg", "Daily", 30, 30, ago(3), 5, 7),
        (9, "Furosemide", "40mg", "Daily", 30, 30, ago(3), 5, 7),
        (9, "Tiotropium inhaler", "18mcg", "Daily", 1, 30, ago(28), 5, 7),
        (9, "Alendronate", "70mg", "Weekly", 4, 28, ago(20), 5, 7),
        (9, "Metformin", "500mg", "BID", 60, 30, ago(3), 5, 7),
        # Ahmed
        (10, "Omeprazole", "20mg", "Daily", 30, 30, ago(50), 3, 7),
        # Priya
        (11, "Prenatal vitamins", None, "Daily", 30, 30, ago(12), 5, 7),
        # William
        (12, "Amlodipine", "10mg", "Daily", 30, 30, ago(8), 5, 7),
        (12, "Tamsulosin", "0.4mg", "Daily", 30, 30, ago(8), 5, 7),
        # Margaret
        (13, "Empagliflozin", "25mg", "Daily", 30, 30, ago(20), 3, 7),
        (13, "Lisinopril", "10mg", "Daily", 30, 30, ago(20), 3, 7),
        # Jamal
        (14, "Fluticasone/Salmeterol", "250/50", "BID", 1, 30, ago(22), 5, 7),
        (14, "Albuterol inhaler", "90mcg", "Q4H PRN", 1, 90, ago(80), 2, 14),
        # Linda
        (15, "Duloxetine", "60mg", "Daily", 30, 30, ago(35), 3, 7),
        (15, "Lisinopril", "20mg", "Daily", 30, 30, ago(35), 5, 7),
    ]
    for (pid, name, dose, freq, qty, days, filled, refills, remind) in meds:
        db.execute("""INSERT INTO medications (patient_id,name,dose,frequency,quantity_dispensed,days_supply,
            last_filled_date,refills_remaining,remind_days_before) VALUES (?,?,?,?,?,?,?,?,?)""",
            (pid, name, dose, freq, qty, days, filled, refills, remind))

    # ── Labs ────────────────────────────────────────────────────────────────

    labs = [
        # Roberto - pending A1c
        (1, "A1c", ago(5), None, None, "ordered", 0, None),
        (1, "CMP", ago(5), None, None, "ordered", 0, None),
        (1, "Lipid panel", ago(30), ago(27), "TC 198, LDL 112, HDL 42, TG 180", "reviewed", 0, None),
        (1, "A1c", ago(180), ago(177), "7.2%", "reviewed", 1, "Increased glipizide"),
        # Maria - TSH pending
        (2, "TSH", ago(3), None, None, "pending", 0, None),
        (2, "CBC", ago(60), ago(57), "WNL", "reviewed", 0, None),
        # Susan - CBC for anemia follow-up
        (6, "CBC", ago(7), None, None, "pending", 0, None),
        (6, "Iron studies", ago(7), None, None, "pending", 0, None),
        # Dorothy
        (9, "BMP", ago(2), None, None, "ordered", 0, None),
        (9, "BNP", ago(2), None, None, "ordered", 0, None),
        (9, "INR", ago(14), ago(12), "N/A (on apixaban)", "reviewed", 0, None),
        # Priya - prenatal labs
        (11, "Glucose tolerance test", ago(1), None, None, "ordered", 0, None),
        (11, "CBC", ago(30), ago(27), "Hgb 11.2", "reviewed", 0, None),
        # William - PSA
        (12, "PSA", ago(10), None, None, "pending", 0, None),
        # Margaret
        (13, "A1c", ago(90), ago(87), "7.8%", "reviewed", 1, "Consider adding GLP-1 RA"),
        (13, "A1c", ago(4), None, None, "ordered", 0, None),
    ]
    for (pid, test, ordered, result_date, value, status, fu, fu_notes) in labs:
        db.execute("INSERT INTO labs (patient_id,test_name,ordered_date,result_date,result_value,status,followup_needed,followup_notes) VALUES (?,?,?,?,?,?,?,?)",
            (pid, test, ordered, result_date, value, status, fu, fu_notes))

    # ── Reminders ───────────────────────────────────────────────────────────

    reminders = [
        (1, "Call re: A1c result", "A1c was ordered 5 days ago, follow up when resulted", ago(2), "manual"),
        (1, "Schedule foot exam", "Annual diabetic foot exam overdue", ago(10), "manual"),
        (2, "Check TSH result", "TSH pending, adjust levothyroxine if needed", future(2), "lab"),
        (5, "Follow up back pain", "Was starting PT 6 weeks ago, check progress", ago(5), "manual"),
        (6, "Review CBC/iron", "Anemia follow-up, check if ferrous sulfate is working", future(1), "lab"),
        (9, "Call re: BMP", "Check potassium - on furosemide", ago(0), "lab"),
        (9, "Schedule echocardiogram", "Annual echo for CHF monitoring", ago(14), "manual"),
        (11, "Review glucose tolerance test", "Gestational diabetes monitoring", future(3), "lab"),
        (12, "Call re: PSA result", "Active surveillance, compare to prior", future(1), "lab"),
        (13, "Discuss GLP-1 RA", "A1c 7.8% on empagliflozin alone, needs intensification", ago(7), "manual"),
        (14, "Asthma action plan review", "Annual review overdue", ago(20), "manual"),
        (15, "Sleep study referral", "Discussed at last visit, patient agreed", ago(3), "manual"),
    ]
    for (pid, title, reason, due, source) in reminders:
        db.execute("INSERT INTO reminders (patient_id,title,reason,due_date,source_type) VALUES (?,?,?,?,?)",
            (pid, title, reason, due, source))

    # ── Referrals ───────────────────────────────────────────────────────────

    referrals = [
        (1, "Ophthalmology", "Dr. Lee", "Annual diabetic eye exam", ago(45), 0, None, 0, None),
        (1, "Podiatry", "Dr. Foot", "Diabetic foot care", ago(30), 0, None, 0, None),
        (5, "Physical Therapy", "Valley PT", "Low back pain rehab", ago(60), 1, ago(55), 0, None),
        (5, "Orthopedics", "Dr. Bones", "L4-L5 disc evaluation", ago(20), 0, None, 1, "Awaiting consult note"),
        (9, "Cardiology", "Dr. Heart", "Annual CHF follow-up", ago(30), 0, None, 0, None),
        (9, "Pulmonology", "Dr. Lung", "COPD management", ago(90), 1, ago(75), 0, "Spirometry stable"),
        (12, "Urology", "Dr. Stone", "Prostate cancer surveillance", ago(15), 0, None, 0, None),
        (13, "Endocrinology", None, "Diabetes management intensification", ago(10), 0, None, 0, None),
        (15, "Sleep Medicine", None, "Insomnia / possible OSA evaluation", ago(3), 0, None, 0, None),
    ]
    for (pid, spec, prov, reason, sent, received, cdate, fu, notes) in referrals:
        db.execute("INSERT INTO referrals (patient_id,specialty,provider_name,reason,date_sent,consult_received,consult_date,followup_needed,notes) VALUES (?,?,?,?,?,?,?,?,?)",
            (pid, spec, prov, reason, sent, received, cdate, fu, notes))

    # ── Contact log ─────────────────────────────────────────────────────────

    contacts = [
        (1, ago(15), "phone", "Called pt re: A1c 7.2%. Discussed diet, increasing glipizide to 10mg. Will recheck A1c in 3 months.", 1, ago(0)),
        (1, ago(45), "in_person", "Annual physical. Reviewed all meds, ordered labs, referrals to ophtho and podiatry.", 0, None),
        (2, ago(60), "phone", "Called with CBC results, all normal. Continue current meds.", 0, None),
        (5, ago(20), "in_person", "Follow-up for back pain. PT helping, still some pain. Ordered ortho consult. Continue ibuprofen PRN.", 1, future(14)),
        (9, ago(3), "phone", "Called to check on Dorothy. Feeling more SOB, ordered BMP and BNP. May need diuretic adjustment.", 1, ago(0)),
        (11, ago(30), "in_person", "Prenatal visit. Growth appropriate, BP normal. Ordered GTT for GDM screening.", 0, None),
        (13, ago(7), "in_person", "Diabetes follow-up. A1c 7.8%. Discussed adding GLP-1 RA vs increasing empagliflozin. Patient wants to think about it.", 1, future(14)),
    ]
    for (pid, cdate, method, summary, fu, fudate) in contacts:
        db.execute("INSERT INTO contact_log (patient_id,contact_date,method,summary,followup_needed,followup_date) VALUES (?,?,?,?,?,?)",
            (pid, cdate, method, summary, fu, fudate))

    # ── Tags ────────────────────────────────────────────────────────────────

    tags_data = [
        ("diabetes", "#dc2626"),
        ("hypertension", "#2563eb"),
        ("CHF", "#7c3aed"),
        ("COPD", "#0891b2"),
        ("pregnant", "#ec4899"),
        ("elderly", "#f59e0b"),
        ("complex", "#6b21a8"),
        ("asthma", "#06b6d4"),
        ("cancer", "#991b1b"),
        ("palliative", "#4b5563"),
    ]
    for (name, color) in tags_data:
        db.execute("INSERT INTO tags (name, color) VALUES (?,?)", (name, color))

    # Map: tag_name -> tag_id (just use order since we know IDs)
    tag_ids = {}
    for row in db.execute("SELECT id, name FROM tags").fetchall():
        tag_ids[row[1]] = row[0]

    patient_tags = [
        (1, "diabetes"), (1, "hypertension"), (1, "complex"),
        (2, "elderly"),
        (5, "hypertension"),
        (6, "asthma"),
        (9, "CHF"), (9, "COPD"), (9, "diabetes"), (9, "elderly"), (9, "complex"),
        (11, "pregnant"),
        (12, "cancer"), (12, "elderly"),
        (13, "diabetes"), (13, "hypertension"),
        (14, "asthma"),
        (15, "hypertension"),
    ]
    for (pid, tag_name) in patient_tags:
        db.execute("INSERT INTO patient_tags (patient_id, tag_id) VALUES (?,?)", (pid, tag_ids[tag_name]))

    # ── Sticky notes ────────────────────────────────────────────────────────

    db.execute("UPDATE patients SET notes=? WHERE id=?", ("Husband dying of pancreatic cancer — be sensitive.\nPrefers afternoon appointments.\nSpanish-speaking, daughter Elena interprets.", 2))
    db.execute("UPDATE patients SET notes=? WHERE id=?", ("Lives alone, falls risk. Daughter checks in daily.\nHard of hearing — speak loudly and clearly.\nDNR/DNI on file.", 9))
    db.execute("UPDATE patients SET notes=? WHERE id=?", ("Needle phobia — use butterfly needle, offer numbing cream.\nFirst pregnancy, high anxiety.", 11))
    db.execute("UPDATE patients SET notes=? WHERE id=?", ("Snowbird — gone to Florida Nov through April.\nSend 6-month supplies before he leaves.", 12))

    # ── Upcoming visits ─────────────────────────────────────────────────────

    visits = [
        (1, future(2), "follow-up", "A1c recheck, review labs"),
        (6, future(3), "follow-up", "Anemia recheck"),
        (9, future(1), "urgent", "SOB worsening, review BMP/BNP"),
        (11, future(5), "prenatal", "28-week visit"),
        (13, future(4), "follow-up", "Diabetes management, GLP-1 RA decision"),
    ]
    for (pid, vdate, vtype, notes) in visits:
        db.execute("INSERT INTO upcoming_visits (patient_id, visit_date, visit_type, notes) VALUES (?,?,?,?)",
            (pid, vdate, vtype, notes))

    # ── Generate preventive care items ──────────────────────────────────────

    rules = db.execute("SELECT * FROM preventive_care_rules").fetchall()
    patients = db.execute("SELECT id, dob, sex FROM patients").fetchall()

    for p in patients:
        pid = p[0]
        dob = p[1]
        sex = p[2]
        birth = date.fromisoformat(dob)
        today = date.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

        for rule in rules:
            r_id, r_name, r_desc, r_sex, r_min, r_max, r_interval, r_cat = rule
            if r_sex != "A" and r_sex != sex:
                continue
            if age < r_min or age > r_max:
                continue

            # Randomly assign some as completed, some as due/overdue
            rand = random.random()
            if rand < 0.4:
                # Completed recently
                done_date = ago(random.randint(30, 365))
                if r_interval > 0:
                    next_due = (date.fromisoformat(done_date) + timedelta(days=r_interval*30)).isoformat()
                else:
                    next_due = None
                db.execute("INSERT INTO preventive_care_items (patient_id,rule_id,last_done_date,next_due_date,status) VALUES (?,?,?,?,?)",
                    (pid, r_id, done_date, next_due, "completed"))
            elif rand < 0.65:
                # Overdue
                overdue_date = ago(random.randint(30, 365))
                db.execute("INSERT INTO preventive_care_items (patient_id,rule_id,next_due_date,status) VALUES (?,?,?,?)",
                    (pid, r_id, overdue_date, "overdue"))
            else:
                # Due now
                db.execute("INSERT INTO preventive_care_items (patient_id,rule_id,next_due_date,status) VALUES (?,?,?,?)",
                    (pid, r_id, today.isoformat(), "due"))

    db.commit()
    print(f"Seeded {db.execute('SELECT COUNT(*) FROM patients').fetchone()[0]} patients with full data.")
    db.close()


if __name__ == "__main__":
    seed()
