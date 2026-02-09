#!/usr/bin/env python3
"""PanelTracker — lightweight patient panel management for family docs."""

import sqlite3
import os
from datetime import datetime, date, timedelta
from functools import wraps

from flask import (
    Flask, g, request, jsonify, render_template, abort
)

app = Flask(__name__)
app.config["DATABASE"] = os.path.join(os.path.dirname(__file__), "panel.db")


# ── DB helpers ──────────────────────────────────────────────────────────────

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA journal_mode=WAL")
        g.db.execute("PRAGMA foreign_keys=ON")
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with open(os.path.join(os.path.dirname(__file__), "schema.sql")) as f:
        db.executescript(f.read())
    _seed_preventive_rules(db)
    db.commit()


def _seed_preventive_rules(db):
    """Insert default preventive care rules if table is empty."""
    count = db.execute("SELECT COUNT(*) FROM preventive_care_rules").fetchone()[0]
    if count > 0:
        return
    rules = [
        ("Colonoscopy", "Colorectal cancer screening", "A", 45, 75, 120, "screening"),
        ("Mammogram", "Breast cancer screening", "F", 40, 74, 24, "screening"),
        ("Pap smear", "Cervical cancer screening", "F", 21, 65, 36, "screening"),
        ("Lipid panel", "Cardiovascular risk", "A", 20, 999, 60, "lab"),
        ("A1c", "Diabetes screening / monitoring", "A", 35, 999, 12, "lab"),
        ("DEXA scan", "Bone density screening", "F", 65, 999, 24, "screening"),
        ("AAA ultrasound", "Abdominal aortic aneurysm screen", "M", 65, 75, 0, "screening"),
        ("Lung cancer CT", "Low-dose CT for smokers", "A", 50, 80, 12, "screening"),
        ("Flu vaccine", "Annual influenza vaccine", "A", 6, 999, 12, "immunization"),
        ("Pneumovax", "Pneumococcal vaccine", "A", 65, 999, 0, "immunization"),
        ("Shingrix", "Shingles vaccine (2 doses)", "A", 50, 999, 0, "immunization"),
        ("Tdap", "Tetanus/diphtheria/pertussis", "A", 11, 999, 120, "immunization"),
        ("Td booster", "Tetanus booster", "A", 19, 999, 120, "immunization"),
        ("HIV screening", "One-time or periodic HIV test", "A", 15, 65, 0, "screening"),
        ("Hepatitis C screening", "One-time HCV screen", "A", 18, 79, 0, "screening"),
        ("Depression screening (PHQ-9)", "Annual depression screen", "A", 12, 999, 12, "screening"),
    ]
    db.executemany(
        "INSERT INTO preventive_care_rules (name,description,sex,min_age,max_age,interval_months,category) VALUES (?,?,?,?,?,?,?)",
        rules,
    )


def dict_row(row):
    return dict(row) if row else None


def dict_rows(rows):
    return [dict(r) for r in rows]


def today_str():
    return date.today().isoformat()


def compute_age(dob_str):
    dob = date.fromisoformat(dob_str)
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


# ── CLI init ────────────────────────────────────────────────────────────────

@app.cli.command("init-db")
def init_db_command():
    init_db()
    print("Database initialized.")


# ── Pages ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


# ── Dashboard API ───────────────────────────────────────────────────────────

@app.route("/api/dashboard")
def api_dashboard():
    db = get_db()
    today = today_str()
    week_out = (date.today() + timedelta(days=7)).isoformat()

    # Overdue & upcoming reminders
    reminders = dict_rows(db.execute("""
        SELECT r.*, p.first_name, p.last_name
        FROM reminders r JOIN patients p ON r.patient_id=p.id
        WHERE r.completed=0 AND r.due_date <= ?
        ORDER BY r.due_date
        LIMIT 50
    """, (week_out,)).fetchall())

    # Meds running out within 14 days
    meds_due = dict_rows(db.execute("""
        SELECT m.*, p.first_name, p.last_name,
               date(m.last_filled_date, '+' || m.days_supply || ' days') as run_out_date
        FROM medications m JOIN patients p ON m.patient_id=p.id
        WHERE m.active=1 AND m.last_filled_date IS NOT NULL AND m.days_supply IS NOT NULL
          AND date(m.last_filled_date, '+' || m.days_supply || ' days') <= date(?, '+14 days')
        ORDER BY run_out_date
        LIMIT 50
    """, (today,)).fetchall())

    # Pending labs
    pending_labs = dict_rows(db.execute("""
        SELECT l.*, p.first_name, p.last_name
        FROM labs l JOIN patients p ON l.patient_id=p.id
        WHERE l.status IN ('ordered','pending')
        ORDER BY l.ordered_date
        LIMIT 50
    """).fetchall())

    # Pending referrals (consult not received)
    pending_referrals = dict_rows(db.execute("""
        SELECT r.*, p.first_name, p.last_name
        FROM referrals r JOIN patients p ON r.patient_id=p.id
        WHERE r.consult_received=0
        ORDER BY r.date_sent
        LIMIT 50
    """).fetchall())

    # Overdue preventive care
    overdue_prev = dict_rows(db.execute("""
        SELECT pc.*, pr.name as rule_name, pr.category, p.first_name, p.last_name
        FROM preventive_care_items pc
        JOIN preventive_care_rules pr ON pc.rule_id=pr.id
        JOIN patients p ON pc.patient_id=p.id
        WHERE pc.status IN ('due','overdue') AND (pc.next_due_date IS NULL OR pc.next_due_date <= ?)
        ORDER BY pc.next_due_date
        LIMIT 50
    """, (today,)).fetchall())

    # Upcoming visits in next 7 days
    upcoming_visits = dict_rows(db.execute("""
        SELECT v.*, p.first_name, p.last_name
        FROM upcoming_visits v JOIN patients p ON v.patient_id=p.id
        WHERE v.visit_date BETWEEN ? AND ?
        ORDER BY v.visit_date
    """, (today, week_out)).fetchall())

    # Panel stats
    total_patients = db.execute("SELECT COUNT(*) FROM patients WHERE active=1").fetchone()[0]

    return jsonify({
        "reminders": reminders,
        "meds_due": meds_due,
        "pending_labs": pending_labs,
        "pending_referrals": pending_referrals,
        "overdue_preventive": overdue_prev,
        "upcoming_visits": upcoming_visits,
        "total_patients": total_patients,
    })


# ── Patients CRUD ───────────────────────────────────────────────────────────

@app.route("/api/patients", methods=["GET"])
def list_patients():
    db = get_db()
    q = request.args.get("q", "").strip()
    tag = request.args.get("tag", "").strip()
    problem = request.args.get("problem", "").strip()
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 50))
    offset = (page - 1) * per_page

    query = "SELECT DISTINCT p.* FROM patients p"
    joins = []
    wheres = ["p.active=1"]
    params = []

    if tag:
        joins.append("JOIN patient_tags pt ON p.id=pt.patient_id JOIN tags t ON pt.tag_id=t.id")
        wheres.append("t.name=?")
        params.append(tag)

    if problem:
        joins.append("JOIN problems pr ON p.id=pr.patient_id")
        wheres.append("pr.description LIKE ? AND pr.status='active'")
        params.append(f"%{problem}%")

    if q:
        wheres.append("(p.first_name LIKE ? OR p.last_name LIKE ? OR p.phone LIKE ?)")
        params.extend([f"%{q}%", f"%{q}%", f"%{q}%"])

    sql = query + " " + " ".join(joins)
    if wheres:
        sql += " WHERE " + " AND ".join(wheres)
    count_sql = sql.replace("SELECT DISTINCT p.*", "SELECT COUNT(DISTINCT p.id)")
    total = db.execute(count_sql, params).fetchone()[0]

    sql += " ORDER BY p.last_name, p.first_name LIMIT ? OFFSET ?"
    params.extend([per_page, offset])
    patients = dict_rows(db.execute(sql, params).fetchall())

    # Attach tags to each patient
    if patients:
        pids = [p["id"] for p in patients]
        placeholders = ",".join("?" * len(pids))
        tag_rows = db.execute(f"""
            SELECT pt.patient_id, t.name, t.color
            FROM patient_tags pt JOIN tags t ON pt.tag_id=t.id
            WHERE pt.patient_id IN ({placeholders})
        """, pids).fetchall()
        tag_map = {}
        for tr in tag_rows:
            tag_map.setdefault(tr["patient_id"], []).append({"name": tr["name"], "color": tr["color"]})
        for p in patients:
            p["tags"] = tag_map.get(p["id"], [])

    return jsonify({"patients": patients, "total": total, "page": page, "per_page": per_page})


@app.route("/api/patients", methods=["POST"])
def create_patient():
    db = get_db()
    d = request.json
    cur = db.execute(
        """INSERT INTO patients (first_name,last_name,dob,sex,phone,email,address,pharmacy,preferred_contact,notes)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (d["first_name"], d["last_name"], d["dob"], d["sex"],
         d.get("phone"), d.get("email"), d.get("address"), d.get("pharmacy"),
         d.get("preferred_contact", "phone"), d.get("notes")),
    )
    db.commit()
    patient_id = cur.lastrowid
    _generate_preventive_care(db, patient_id)
    db.commit()
    return jsonify({"id": patient_id}), 201


@app.route("/api/patients/<int:pid>", methods=["GET"])
def get_patient(pid):
    db = get_db()
    p = dict_row(db.execute("SELECT * FROM patients WHERE id=?", (pid,)).fetchone())
    if not p:
        abort(404)
    p["age"] = compute_age(p["dob"])
    p["allergies"] = dict_rows(db.execute("SELECT * FROM allergies WHERE patient_id=? ORDER BY severity DESC", (pid,)).fetchall())
    p["problems"] = dict_rows(db.execute("SELECT * FROM problems WHERE patient_id=? ORDER BY status, onset_date DESC", (pid,)).fetchall())
    p["medications"] = dict_rows(db.execute("SELECT * FROM medications WHERE patient_id=? ORDER BY active DESC, name", (pid,)).fetchall())
    # Compute run-out dates
    for med in p["medications"]:
        if med["last_filled_date"] and med["days_supply"]:
            filled = date.fromisoformat(med["last_filled_date"])
            med["run_out_date"] = (filled + timedelta(days=med["days_supply"])).isoformat()
        else:
            med["run_out_date"] = None
    p["labs"] = dict_rows(db.execute("SELECT * FROM labs WHERE patient_id=? ORDER BY ordered_date DESC", (pid,)).fetchall())
    p["reminders"] = dict_rows(db.execute("SELECT * FROM reminders WHERE patient_id=? ORDER BY completed, due_date", (pid,)).fetchall())
    p["contact_log"] = dict_rows(db.execute("SELECT * FROM contact_log WHERE patient_id=? ORDER BY contact_date DESC", (pid,)).fetchall())
    p["referrals"] = dict_rows(db.execute("SELECT * FROM referrals WHERE patient_id=? ORDER BY date_sent DESC", (pid,)).fetchall())
    p["preventive_care"] = dict_rows(db.execute("""
        SELECT pc.*, pr.name as rule_name, pr.description as rule_description, pr.category, pr.interval_months
        FROM preventive_care_items pc JOIN preventive_care_rules pr ON pc.rule_id=pr.id
        WHERE pc.patient_id=? ORDER BY pc.status, pc.next_due_date
    """, (pid,)).fetchall())
    p["upcoming_visits"] = dict_rows(db.execute("SELECT * FROM upcoming_visits WHERE patient_id=? AND visit_date >= ? ORDER BY visit_date", (pid, today_str())).fetchall())

    # Tags
    p["tags"] = dict_rows(db.execute("""
        SELECT t.id, t.name, t.color FROM tags t
        JOIN patient_tags pt ON t.id=pt.tag_id WHERE pt.patient_id=?
    """, (pid,)).fetchall())

    # Family
    p["family"] = dict_rows(db.execute("""
        SELECT fr.*, p2.first_name, p2.last_name, p2.dob, p2.sex
        FROM family_relationships fr JOIN patients p2 ON fr.related_patient_id=p2.id
        WHERE fr.patient_id=?
    """, (pid,)).fetchall())

    return jsonify(p)


@app.route("/api/patients/<int:pid>", methods=["PUT"])
def update_patient(pid):
    db = get_db()
    d = request.json
    fields = []
    params = []
    for col in ("first_name", "last_name", "dob", "sex", "phone", "email", "address", "pharmacy", "preferred_contact", "notes", "active"):
        if col in d:
            fields.append(f"{col}=?")
            params.append(d[col])
    if not fields:
        return jsonify({"error": "No fields to update"}), 400
    fields.append("updated_at=datetime('now')")
    params.append(pid)
    db.execute(f"UPDATE patients SET {', '.join(fields)} WHERE id=?", params)
    db.commit()
    return jsonify({"ok": True})


# ── Family relationships ────────────────────────────────────────────────────

INVERSE_REL = {"spouse": "spouse", "parent": "child", "child": "parent", "sibling": "sibling"}

@app.route("/api/patients/<int:pid>/family", methods=["POST"])
def add_family(pid):
    db = get_db()
    d = request.json
    related_id = d["related_patient_id"]
    rel = d["relationship"]
    inv = INVERSE_REL.get(rel, rel)
    db.execute("INSERT OR IGNORE INTO family_relationships (patient_id, related_patient_id, relationship) VALUES (?,?,?)", (pid, related_id, rel))
    db.execute("INSERT OR IGNORE INTO family_relationships (patient_id, related_patient_id, relationship) VALUES (?,?,?)", (related_id, pid, inv))
    db.commit()
    return jsonify({"ok": True}), 201


@app.route("/api/patients/<int:pid>/family/<int:rid>", methods=["DELETE"])
def remove_family(pid, rid):
    db = get_db()
    db.execute("DELETE FROM family_relationships WHERE patient_id=? AND related_patient_id=?", (pid, rid))
    db.execute("DELETE FROM family_relationships WHERE patient_id=? AND related_patient_id=?", (rid, pid))
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/patients/<int:pid>/family-tree")
def family_tree(pid):
    """Return nodes + edges for vis.js network graph."""
    db = get_db()
    visited = set()
    nodes = []
    edges = []

    def walk(patient_id, depth=0):
        if patient_id in visited or depth > 3:
            return
        visited.add(patient_id)
        p = db.execute("SELECT id, first_name, last_name, dob, sex FROM patients WHERE id=?", (patient_id,)).fetchone()
        if not p:
            return
        age = compute_age(p["dob"])
        nodes.append({
            "id": p["id"],
            "label": f"{p['first_name']} {p['last_name']}\n{age}y {p['sex']}",
            "color": "#3b82f6" if p["sex"] == "M" else "#ec4899" if p["sex"] == "F" else "#8b5cf6",
            "shape": "box",
            "font": {"color": "#ffffff"},
        })
        rels = db.execute("SELECT * FROM family_relationships WHERE patient_id=?", (patient_id,)).fetchall()
        for r in rels:
            edge_id = tuple(sorted([patient_id, r["related_patient_id"]]))
            edge_key = f"{edge_id[0]}-{edge_id[1]}"
            if edge_key not in {f"{e.get('_key')}" for e in edges}:
                edges.append({
                    "from": patient_id,
                    "to": r["related_patient_id"],
                    "label": r["relationship"],
                    "arrows": "to" if r["relationship"] in ("parent", "child") else "",
                    "_key": edge_key,
                })
            walk(r["related_patient_id"], depth + 1)

    walk(pid)
    for e in edges:
        e.pop("_key", None)
    return jsonify({"nodes": nodes, "edges": edges})


# ── Allergies ───────────────────────────────────────────────────────────────

@app.route("/api/patients/<int:pid>/allergies", methods=["POST"])
def add_allergy(pid):
    db = get_db()
    d = request.json
    cur = db.execute("INSERT INTO allergies (patient_id,allergen,reaction,severity) VALUES (?,?,?,?)",
                     (pid, d["allergen"], d.get("reaction"), d.get("severity", "moderate")))
    db.commit()
    return jsonify({"id": cur.lastrowid}), 201


@app.route("/api/allergies/<int:aid>", methods=["DELETE"])
def delete_allergy(aid):
    db = get_db()
    db.execute("DELETE FROM allergies WHERE id=?", (aid,))
    db.commit()
    return jsonify({"ok": True})


# ── Problems ────────────────────────────────────────────────────────────────

@app.route("/api/patients/<int:pid>/problems", methods=["POST"])
def add_problem(pid):
    db = get_db()
    d = request.json
    cur = db.execute("INSERT INTO problems (patient_id,description,status,onset_date,notes) VALUES (?,?,?,?,?)",
                     (pid, d["description"], d.get("status", "active"), d.get("onset_date"), d.get("notes")))
    db.commit()
    return jsonify({"id": cur.lastrowid}), 201


@app.route("/api/problems/<int:prob_id>", methods=["PUT"])
def update_problem(prob_id):
    db = get_db()
    d = request.json
    fields, params = [], []
    for col in ("description", "status", "onset_date", "resolved_date", "notes"):
        if col in d:
            fields.append(f"{col}=?")
            params.append(d[col])
    if fields:
        fields.append("updated_at=datetime('now')")
        params.append(prob_id)
        db.execute(f"UPDATE problems SET {', '.join(fields)} WHERE id=?", params)
        db.commit()
    return jsonify({"ok": True})


@app.route("/api/problems/<int:prob_id>", methods=["DELETE"])
def delete_problem(prob_id):
    db = get_db()
    db.execute("DELETE FROM problems WHERE id=?", (prob_id,))
    db.commit()
    return jsonify({"ok": True})


# ── Medications ─────────────────────────────────────────────────────────────

@app.route("/api/patients/<int:pid>/medications", methods=["POST"])
def add_medication(pid):
    db = get_db()
    d = request.json
    cur = db.execute(
        """INSERT INTO medications (patient_id,name,dose,frequency,quantity_dispensed,days_supply,
           last_filled_date,refills_remaining,prescriber_notes,remind_days_before)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (pid, d["name"], d.get("dose"), d.get("frequency"), d.get("quantity_dispensed"),
         d.get("days_supply"), d.get("last_filled_date"), d.get("refills_remaining"),
         d.get("prescriber_notes"), d.get("remind_days_before", 7)),
    )
    db.commit()
    return jsonify({"id": cur.lastrowid}), 201


@app.route("/api/medications/<int:mid>", methods=["PUT"])
def update_medication(mid):
    db = get_db()
    d = request.json
    fields, params = [], []
    for col in ("name", "dose", "frequency", "quantity_dispensed", "days_supply",
                "last_filled_date", "refills_remaining", "prescriber_notes", "active", "remind_days_before"):
        if col in d:
            fields.append(f"{col}=?")
            params.append(d[col])
    if fields:
        fields.append("updated_at=datetime('now')")
        params.append(mid)
        db.execute(f"UPDATE medications SET {', '.join(fields)} WHERE id=?", params)
        db.commit()
    return jsonify({"ok": True})


@app.route("/api/medications/<int:mid>", methods=["DELETE"])
def delete_medication(mid):
    db = get_db()
    db.execute("DELETE FROM medications WHERE id=?", (mid,))
    db.commit()
    return jsonify({"ok": True})


# ── Labs ────────────────────────────────────────────────────────────────────

@app.route("/api/patients/<int:pid>/labs", methods=["POST"])
def add_lab(pid):
    db = get_db()
    d = request.json
    cur = db.execute(
        "INSERT INTO labs (patient_id,test_name,ordered_date,result_date,result_value,status,followup_needed,followup_notes) VALUES (?,?,?,?,?,?,?,?)",
        (pid, d["test_name"], d.get("ordered_date", today_str()), d.get("result_date"),
         d.get("result_value"), d.get("status", "ordered"), d.get("followup_needed", 0), d.get("followup_notes")),
    )
    db.commit()
    return jsonify({"id": cur.lastrowid}), 201


@app.route("/api/labs/<int:lid>", methods=["PUT"])
def update_lab(lid):
    db = get_db()
    d = request.json
    fields, params = [], []
    for col in ("test_name", "ordered_date", "result_date", "result_value", "status", "followup_needed", "followup_notes"):
        if col in d:
            fields.append(f"{col}=?")
            params.append(d[col])
    if fields:
        fields.append("updated_at=datetime('now')")
        params.append(lid)
        db.execute(f"UPDATE labs SET {', '.join(fields)} WHERE id=?", params)
        db.commit()
    return jsonify({"ok": True})


@app.route("/api/labs/<int:lid>", methods=["DELETE"])
def delete_lab(lid):
    db = get_db()
    db.execute("DELETE FROM labs WHERE id=?", (lid,))
    db.commit()
    return jsonify({"ok": True})


# ── Reminders ───────────────────────────────────────────────────────────────

@app.route("/api/patients/<int:pid>/reminders", methods=["POST"])
def add_reminder(pid):
    db = get_db()
    d = request.json
    cur = db.execute(
        "INSERT INTO reminders (patient_id,title,reason,due_date,source_type) VALUES (?,?,?,?,?)",
        (pid, d["title"], d.get("reason"), d["due_date"], d.get("source_type", "manual")),
    )
    db.commit()
    return jsonify({"id": cur.lastrowid}), 201


@app.route("/api/reminders/<int:rid>", methods=["PUT"])
def update_reminder(rid):
    db = get_db()
    d = request.json
    if d.get("completed"):
        db.execute("UPDATE reminders SET completed=1, completed_date=datetime('now') WHERE id=?", (rid,))
    else:
        fields, params = [], []
        for col in ("title", "reason", "due_date"):
            if col in d:
                fields.append(f"{col}=?")
                params.append(d[col])
        if fields:
            params.append(rid)
            db.execute(f"UPDATE reminders SET {', '.join(fields)} WHERE id=?", params)
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/reminders/<int:rid>", methods=["DELETE"])
def delete_reminder(rid):
    db = get_db()
    db.execute("DELETE FROM reminders WHERE id=?", (rid,))
    db.commit()
    return jsonify({"ok": True})


# ── Contact log ─────────────────────────────────────────────────────────────

@app.route("/api/patients/<int:pid>/contacts", methods=["POST"])
def add_contact(pid):
    db = get_db()
    d = request.json
    cur = db.execute(
        "INSERT INTO contact_log (patient_id,contact_date,method,summary,followup_needed,followup_date) VALUES (?,?,?,?,?,?)",
        (pid, d.get("contact_date", datetime.now().isoformat()), d.get("method", "phone"),
         d["summary"], d.get("followup_needed", 0), d.get("followup_date")),
    )
    db.commit()
    return jsonify({"id": cur.lastrowid}), 201


# ── Referrals ───────────────────────────────────────────────────────────────

@app.route("/api/patients/<int:pid>/referrals", methods=["POST"])
def add_referral(pid):
    db = get_db()
    d = request.json
    cur = db.execute(
        "INSERT INTO referrals (patient_id,specialty,provider_name,reason,date_sent) VALUES (?,?,?,?,?)",
        (pid, d["specialty"], d.get("provider_name"), d.get("reason"), d.get("date_sent", today_str())),
    )
    db.commit()
    return jsonify({"id": cur.lastrowid}), 201


@app.route("/api/referrals/<int:rid>", methods=["PUT"])
def update_referral(rid):
    db = get_db()
    d = request.json
    fields, params = [], []
    for col in ("specialty", "provider_name", "reason", "date_sent", "consult_received", "consult_date", "followup_needed", "notes"):
        if col in d:
            fields.append(f"{col}=?")
            params.append(d[col])
    if fields:
        fields.append("updated_at=datetime('now')")
        params.append(rid)
        db.execute(f"UPDATE referrals SET {', '.join(fields)} WHERE id=?", params)
        db.commit()
    return jsonify({"ok": True})


# ── Tags ────────────────────────────────────────────────────────────────────

@app.route("/api/tags", methods=["GET"])
def list_tags():
    db = get_db()
    tags = dict_rows(db.execute("SELECT t.*, COUNT(pt.patient_id) as patient_count FROM tags t LEFT JOIN patient_tags pt ON t.id=pt.tag_id GROUP BY t.id ORDER BY t.name").fetchall())
    return jsonify(tags)


@app.route("/api/tags", methods=["POST"])
def create_tag():
    db = get_db()
    d = request.json
    cur = db.execute("INSERT INTO tags (name, color) VALUES (?,?)", (d["name"], d.get("color", "#6b7280")))
    db.commit()
    return jsonify({"id": cur.lastrowid}), 201


@app.route("/api/patients/<int:pid>/tags", methods=["POST"])
def add_patient_tag(pid):
    db = get_db()
    d = request.json
    tag_id = d.get("tag_id")
    if not tag_id and d.get("name"):
        row = db.execute("SELECT id FROM tags WHERE name=?", (d["name"],)).fetchone()
        if row:
            tag_id = row["id"]
        else:
            cur = db.execute("INSERT INTO tags (name, color) VALUES (?,?)", (d["name"], d.get("color", "#6b7280")))
            tag_id = cur.lastrowid
    db.execute("INSERT OR IGNORE INTO patient_tags (patient_id, tag_id) VALUES (?,?)", (pid, tag_id))
    db.commit()
    return jsonify({"ok": True}), 201


@app.route("/api/patients/<int:pid>/tags/<int:tid>", methods=["DELETE"])
def remove_patient_tag(pid, tid):
    db = get_db()
    db.execute("DELETE FROM patient_tags WHERE patient_id=? AND tag_id=?", (pid, tid))
    db.commit()
    return jsonify({"ok": True})


# ── Preventive care ─────────────────────────────────────────────────────────

def _generate_preventive_care(db, patient_id):
    """Generate applicable preventive care items for a patient."""
    p = db.execute("SELECT dob, sex FROM patients WHERE id=?", (patient_id,)).fetchone()
    if not p:
        return
    age = compute_age(p["dob"])
    sex = p["sex"]
    rules = db.execute("SELECT * FROM preventive_care_rules").fetchall()
    for rule in rules:
        if rule["sex"] != "A" and rule["sex"] != sex:
            continue
        if age < rule["min_age"] or age > rule["max_age"]:
            continue
        existing = db.execute("SELECT id FROM preventive_care_items WHERE patient_id=? AND rule_id=?", (patient_id, rule["id"])).fetchone()
        if existing:
            continue
        db.execute(
            "INSERT INTO preventive_care_items (patient_id, rule_id, status, next_due_date) VALUES (?,?,?,?)",
            (patient_id, rule["id"], "due", today_str()),
        )


@app.route("/api/preventive/<int:pcid>", methods=["PUT"])
def update_preventive(pcid):
    db = get_db()
    d = request.json
    fields, params = [], []
    for col in ("last_done_date", "next_due_date", "status", "notes"):
        if col in d:
            fields.append(f"{col}=?")
            params.append(d[col])
    # If marking as completed with a date, auto-compute next due
    if d.get("status") == "completed" and d.get("last_done_date"):
        pc = db.execute("SELECT rule_id FROM preventive_care_items WHERE id=?", (pcid,)).fetchone()
        if pc:
            rule = db.execute("SELECT interval_months FROM preventive_care_rules WHERE id=?", (pc["rule_id"],)).fetchone()
            if rule and rule["interval_months"] > 0:
                done = date.fromisoformat(d["last_done_date"])
                next_due = done + timedelta(days=rule["interval_months"] * 30)
                fields.append("next_due_date=?")
                params.append(next_due.isoformat())
    if fields:
        fields.append("updated_at=datetime('now')")
        params.append(pcid)
        db.execute(f"UPDATE preventive_care_items SET {', '.join(fields)} WHERE id=?", params)
        db.commit()
    return jsonify({"ok": True})


# ── Upcoming visits ─────────────────────────────────────────────────────────

@app.route("/api/patients/<int:pid>/visits", methods=["POST"])
def add_visit(pid):
    db = get_db()
    d = request.json
    cur = db.execute("INSERT INTO upcoming_visits (patient_id, visit_date, visit_type, notes) VALUES (?,?,?,?)",
                     (pid, d["visit_date"], d.get("visit_type", "routine"), d.get("notes")))
    db.commit()
    return jsonify({"id": cur.lastrowid}), 201


@app.route("/api/visits/<int:vid>", methods=["DELETE"])
def delete_visit(vid):
    db = get_db()
    db.execute("DELETE FROM upcoming_visits WHERE id=?", (vid,))
    db.commit()
    return jsonify({"ok": True})


# ── Visit prep ──────────────────────────────────────────────────────────────

@app.route("/api/patients/<int:pid>/visit-prep")
def visit_prep(pid):
    """Aggregate everything needed for pre-visit planning."""
    db = get_db()
    today = today_str()

    overdue_preventive = dict_rows(db.execute("""
        SELECT pc.*, pr.name as rule_name, pr.category
        FROM preventive_care_items pc JOIN preventive_care_rules pr ON pc.rule_id=pr.id
        WHERE pc.patient_id=? AND pc.status IN ('due','overdue')
        ORDER BY pc.next_due_date
    """, (pid,)).fetchall())

    pending_labs = dict_rows(db.execute(
        "SELECT * FROM labs WHERE patient_id=? AND status IN ('ordered','pending') ORDER BY ordered_date", (pid,)
    ).fetchall())

    pending_referrals = dict_rows(db.execute(
        "SELECT * FROM referrals WHERE patient_id=? AND consult_received=0 ORDER BY date_sent", (pid,)
    ).fetchall())

    open_reminders = dict_rows(db.execute(
        "SELECT * FROM reminders WHERE patient_id=? AND completed=0 ORDER BY due_date", (pid,)
    ).fetchall())

    meds_running_out = dict_rows(db.execute("""
        SELECT *, date(last_filled_date, '+' || days_supply || ' days') as run_out_date
        FROM medications WHERE patient_id=? AND active=1
        AND last_filled_date IS NOT NULL AND days_supply IS NOT NULL
        AND date(last_filled_date, '+' || days_supply || ' days') <= date(?, '+30 days')
        ORDER BY run_out_date
    """, (pid, today)).fetchall())

    active_problems = dict_rows(db.execute(
        "SELECT * FROM problems WHERE patient_id=? AND status='active' ORDER BY onset_date DESC", (pid,)
    ).fetchall())

    return jsonify({
        "overdue_preventive": overdue_preventive,
        "pending_labs": pending_labs,
        "pending_referrals": pending_referrals,
        "open_reminders": open_reminders,
        "meds_running_out": meds_running_out,
        "active_problems": active_problems,
    })


# ── Boot ────────────────────────────────────────────────────────────────────

with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
