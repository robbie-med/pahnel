/* PanelTracker — Single Page Application */

const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];
const main = () => $("#main-content");

// ── State ──────────────────────────────────────────────────────────────────

let currentPage = "dashboard";
let currentPatientId = null;
let dashboardData = null;
let reminderPopups = [];
let reminderCheckInterval = null;

// ── API helpers ────────────────────────────────────────────────────────────

async function api(path, opts = {}) {
    const { method = "GET", body } = opts;
    const config = { method, headers: {} };
    if (body) {
        config.headers["Content-Type"] = "application/json";
        config.body = JSON.stringify(body);
    }
    const res = await fetch(`/api${path}`, config);
    if (!res.ok) {
        const err = await res.text();
        throw new Error(err || res.statusText);
    }
    return res.json();
}

// ── Toast ──────────────────────────────────────────────────────────────────

function toast(msg, type = "info") {
    const el = document.createElement("div");
    el.className = `toast ${type}`;
    el.textContent = msg;
    $("#toast-container").appendChild(el);
    setTimeout(() => el.remove(), 3500);
}

// ── Navigation ─────────────────────────────────────────────────────────────

function navigate(page, data) {
    currentPage = page;
    $$(".sidebar nav a").forEach(a => a.classList.toggle("active", a.dataset.page === page));
    switch (page) {
        case "dashboard": renderDashboard(); break;
        case "patients": renderPatientList(); break;
        case "patient": currentPatientId = data; renderPatientChart(); break;
        case "registry": renderRegistry(); break;
        case "reminders": renderRemindersPage(); break;
    }
}

// ── Dashboard ──────────────────────────────────────────────────────────────

async function renderDashboard() {
    main().innerHTML = "<p class='text-muted'>Loading dashboard...</p>";
    try {
        dashboardData = await api("/dashboard");
        const d = dashboardData;
        const overdueReminders = d.reminders.filter(r => r.due_date <= todayStr());
        const upcomingReminders = d.reminders.filter(r => r.due_date > todayStr());

        main().innerHTML = `
        <h2 style="margin-bottom:16px; font-size:20px;">Dashboard</h2>
        <div class="dashboard-stats">
            <div class="stat-card">
                <div class="stat-value">${d.total_patients}</div>
                <div class="stat-label">Active Patients</div>
            </div>
            <div class="stat-card">
                <div class="stat-value ${overdueReminders.length ? 'text-danger' : ''}">${overdueReminders.length}</div>
                <div class="stat-label">Overdue Reminders</div>
            </div>
            <div class="stat-card">
                <div class="stat-value ${d.meds_due.length ? 'text-warning' : ''}">${d.meds_due.length}</div>
                <div class="stat-label">Meds Running Out</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${d.pending_labs.length}</div>
                <div class="stat-label">Pending Labs</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${d.pending_referrals.length}</div>
                <div class="stat-label">Pending Referrals</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${d.overdue_preventive.length}</div>
                <div class="stat-label">Overdue Screenings</div>
            </div>
        </div>

        <div class="dashboard-grid">
            <!-- Overdue reminders -->
            <div class="card">
                <div class="card-header">
                    <h2><span class="text-danger">&#9888;</span> Overdue Reminders</h2>
                </div>
                <div class="card-body">
                    ${overdueReminders.length ? `
                    <table class="data-table">
                        <tr><th>Patient</th><th>Task</th><th>Due</th><th></th></tr>
                        ${overdueReminders.map(r => `
                        <tr>
                            <td class="clickable" onclick="navigate('patient',${r.patient_id})">${r.last_name}, ${r.first_name}</td>
                            <td>${esc(r.title)}${r.reason ? `<br><span class="text-sm text-muted">${esc(r.reason)}</span>` : ''}</td>
                            <td class="overdue">${formatDate(r.due_date)}</td>
                            <td><button class="btn btn-xs btn-success" onclick="completeReminder(${r.id})">Done</button></td>
                        </tr>`).join('')}
                    </table>` : '<p class="text-muted">All clear!</p>'}
                </div>
            </div>

            <!-- Meds running out -->
            <div class="card">
                <div class="card-header">
                    <h2><span class="text-warning">&#9883;</span> Meds Running Out</h2>
                </div>
                <div class="card-body">
                    ${d.meds_due.length ? `
                    <table class="data-table">
                        <tr><th>Patient</th><th>Medication</th><th>Runs Out</th></tr>
                        ${d.meds_due.map(m => `
                        <tr>
                            <td class="clickable" onclick="navigate('patient',${m.patient_id})">${m.last_name}, ${m.first_name}</td>
                            <td>${esc(m.name)} ${m.dose || ''}</td>
                            <td class="${m.run_out_date <= todayStr() ? 'overdue' : 'due-soon'}">${formatDate(m.run_out_date)}</td>
                        </tr>`).join('')}
                    </table>` : '<p class="text-muted">No refills due soon.</p>'}
                </div>
            </div>

            <!-- Pending labs -->
            <div class="card">
                <div class="card-header">
                    <h2><span class="text-info">&#9879;</span> Pending Labs</h2>
                </div>
                <div class="card-body">
                    ${d.pending_labs.length ? `
                    <table class="data-table">
                        <tr><th>Patient</th><th>Test</th><th>Ordered</th><th>Status</th></tr>
                        ${d.pending_labs.map(l => `
                        <tr>
                            <td class="clickable" onclick="navigate('patient',${l.patient_id})">${l.last_name}, ${l.first_name}</td>
                            <td>${esc(l.test_name)}</td>
                            <td>${formatDate(l.ordered_date)}</td>
                            <td><span class="badge badge-info">${l.status}</span></td>
                        </tr>`).join('')}
                    </table>` : '<p class="text-muted">No pending labs.</p>'}
                </div>
            </div>

            <!-- Pending referrals -->
            <div class="card">
                <div class="card-header">
                    <h2>&#9993; Pending Referrals</h2>
                </div>
                <div class="card-body">
                    ${d.pending_referrals.length ? `
                    <table class="data-table">
                        <tr><th>Patient</th><th>Specialty</th><th>Sent</th></tr>
                        ${d.pending_referrals.map(r => `
                        <tr>
                            <td class="clickable" onclick="navigate('patient',${r.patient_id})">${r.last_name}, ${r.first_name}</td>
                            <td>${esc(r.specialty)}${r.provider_name ? ` — ${esc(r.provider_name)}` : ''}</td>
                            <td>${formatDate(r.date_sent)}</td>
                        </tr>`).join('')}
                    </table>` : '<p class="text-muted">All consults received.</p>'}
                </div>
            </div>

            <!-- Overdue preventive care -->
            <div class="card">
                <div class="card-header">
                    <h2><span class="text-purple">&#9733;</span> Overdue Screenings</h2>
                </div>
                <div class="card-body">
                    ${d.overdue_preventive.length ? `
                    <table class="data-table">
                        <tr><th>Patient</th><th>Screening</th><th>Due</th></tr>
                        ${d.overdue_preventive.map(p => `
                        <tr>
                            <td class="clickable" onclick="navigate('patient',${p.patient_id})">${p.last_name}, ${p.first_name}</td>
                            <td>${esc(p.rule_name)} <span class="badge badge-${p.category === 'immunization' ? 'info' : 'warning'}">${p.category}</span></td>
                            <td class="overdue">${p.next_due_date ? formatDate(p.next_due_date) : 'Due now'}</td>
                        </tr>`).join('')}
                    </table>` : '<p class="text-muted">Screenings up to date.</p>'}
                </div>
            </div>

            <!-- Upcoming visits -->
            <div class="card">
                <div class="card-header">
                    <h2>&#128197; Upcoming Visits (7 days)</h2>
                </div>
                <div class="card-body">
                    ${d.upcoming_visits.length ? `
                    <table class="data-table">
                        <tr><th>Patient</th><th>Date</th><th>Type</th><th></th></tr>
                        ${d.upcoming_visits.map(v => `
                        <tr>
                            <td class="clickable" onclick="navigate('patient',${v.patient_id})">${v.last_name}, ${v.first_name}</td>
                            <td>${formatDate(v.visit_date)}</td>
                            <td>${esc(v.visit_type)}</td>
                            <td><button class="btn btn-xs" onclick="showVisitPrep(${v.patient_id})">Prep</button></td>
                        </tr>`).join('')}
                    </table>` : '<p class="text-muted">No visits scheduled.</p>'}
                </div>
            </div>
        </div>`;

        $("#panel-count").textContent = `${d.total_patients} active patients`;
    } catch (e) {
        main().innerHTML = `<p class="text-danger">Error loading dashboard: ${esc(e.message)}</p>`;
    }
}


// ── Patient list ───────────────────────────────────────────────────────────

let patientSearchTimeout = null;

async function renderPatientList(query = "", tagFilter = "", problemFilter = "") {
    main().innerHTML = `
    <div class="flex justify-between items-center mb-4">
        <h2 style="font-size:20px;">Patients</h2>
        <button class="btn btn-primary" onclick="showAddPatientModal()">+ New Patient</button>
    </div>
    <div class="search-bar">
        <span class="search-icon">&#128269;</span>
        <input type="text" id="patient-search" placeholder="Search by name or phone..." value="${esc(query)}" oninput="debouncePatientSearch(this.value)">
    </div>
    <div id="filter-bar" class="flex gap-2 mb-4">
        <select id="tag-filter" onchange="filterByTag(this.value)" style="width:auto;min-width:140px;">
            <option value="">All tags</option>
        </select>
        <input type="text" id="problem-filter" placeholder="Filter by problem..." value="${esc(problemFilter)}" onchange="filterByProblem(this.value)" style="width:200px;">
    </div>
    <div id="patient-list-container"><p class="text-muted">Loading...</p></div>`;

    // Load tags for filter
    const tags = await api("/tags");
    const tagSelect = $("#tag-filter");
    tags.forEach(t => {
        const opt = document.createElement("option");
        opt.value = t.name;
        opt.textContent = `${t.name} (${t.patient_count})`;
        if (t.name === tagFilter) opt.selected = true;
        tagSelect.appendChild(opt);
    });

    await loadPatientList(query, tagFilter, problemFilter);
}

async function loadPatientList(query = "", tag = "", problem = "", page = 1) {
    const params = new URLSearchParams();
    if (query) params.set("q", query);
    if (tag) params.set("tag", tag);
    if (problem) params.set("problem", problem);
    params.set("page", page);
    params.set("per_page", 50);

    const data = await api(`/patients?${params}`);
    const container = $("#patient-list-container");
    if (!data.patients.length) {
        container.innerHTML = `<div class="empty-state"><div class="icon">&#9823;</div><p>No patients found.</p></div>`;
        return;
    }

    container.innerHTML = `
    <table class="data-table">
        <tr><th>Name</th><th>DOB</th><th>Phone</th><th>Tags</th></tr>
        ${data.patients.map(p => `
        <tr class="clickable" onclick="navigate('patient',${p.id})">
            <td><strong>${esc(p.last_name)}, ${esc(p.first_name)}</strong></td>
            <td>${formatDate(p.dob)} (${computeAge(p.dob)}y)</td>
            <td>${esc(p.phone || '—')}</td>
            <td>${(p.tags || []).map(t => `<span class="tag" style="background:${t.color}">${esc(t.name)}</span>`).join(' ')}</td>
        </tr>`).join('')}
    </table>
    <div class="flex justify-between items-center mt-4">
        <span class="text-sm text-muted">${data.total} patients</span>
        <div class="btn-group">
            ${page > 1 ? `<button class="btn btn-sm" onclick="loadPatientList('${esc(query)}','${esc(tag)}','${esc(problem)}',${page-1})">Previous</button>` : ''}
            ${data.total > page * data.per_page ? `<button class="btn btn-sm" onclick="loadPatientList('${esc(query)}','${esc(tag)}','${esc(problem)}',${page+1})">Next</button>` : ''}
        </div>
    </div>`;
}

function debouncePatientSearch(val) {
    clearTimeout(patientSearchTimeout);
    patientSearchTimeout = setTimeout(() => {
        const tag = $("#tag-filter")?.value || "";
        const prob = $("#problem-filter")?.value || "";
        loadPatientList(val, tag, prob);
    }, 300);
}

function filterByTag(tag) {
    const q = $("#patient-search")?.value || "";
    const prob = $("#problem-filter")?.value || "";
    loadPatientList(q, tag, prob);
}

function filterByProblem(prob) {
    const q = $("#patient-search")?.value || "";
    const tag = $("#tag-filter")?.value || "";
    loadPatientList(q, tag, prob);
}


// ── Patient chart ──────────────────────────────────────────────────────────

async function renderPatientChart() {
    const pid = currentPatientId;
    main().innerHTML = "<p class='text-muted'>Loading patient...</p>";

    try {
        const p = await api(`/patients/${pid}`);
        const allergiesHtml = p.allergies.length ? `
        <div class="allergy-banner">
            <span class="label">Allergies:</span>
            ${p.allergies.map(a => `<span class="allergy-item ${a.severity === 'severe' ? 'severe' : ''}">${esc(a.allergen)}${a.reaction ? ` (${esc(a.reaction)})` : ''}</span>`).join('')}
            <button class="btn btn-xs" onclick="showAddAllergyModal(${pid})">+</button>
        </div>` : `<div class="allergy-banner" style="background:#f0fdf4;border-color:#86efac;">
            <span class="label" style="color:#16a34a;">NKDA</span>
            <button class="btn btn-xs" onclick="showAddAllergyModal(${pid})">+ Add Allergy</button>
        </div>`;

        const stickyHtml = p.notes ? `
        <div class="sticky-note">
            <div class="sticky-label">Note</div>
            ${esc(p.notes)}
            <button class="btn btn-xs" style="position:absolute;top:8px;right:8px;" onclick="editStickyNote(${pid},'${escAttr(p.notes)}')">Edit</button>
        </div>` : `<button class="btn btn-xs mb-2" onclick="editStickyNote(${pid},'')">+ Add Sticky Note</button>`;

        main().innerHTML = `
        <div>
            <button class="btn btn-sm mb-4" onclick="navigate('patients')">&larr; Back to Patients</button>

            <div class="patient-header">
                <div>
                    <h1>${esc(p.last_name)}, ${esc(p.first_name)}</h1>
                    <div class="patient-meta">
                        <span>${p.sex === 'M' ? 'Male' : p.sex === 'F' ? 'Female' : 'Other'}, ${p.age}y (DOB: ${formatDate(p.dob)})</span>
                        <span>&#9743; ${esc(p.phone || 'No phone')}</span>
                        <span>&#9993; ${esc(p.email || 'No email')}</span>
                        <span>&#127973; ${esc(p.pharmacy || 'No pharmacy')}</span>
                    </div>
                    <div class="mt-2">
                        ${(p.tags || []).map(t => `<span class="tag" style="background:${t.color}">${esc(t.name)} <span class="tag-remove" onclick="removePatientTag(${pid},${t.id})">&times;</span></span>`).join(' ')}
                        <button class="btn btn-xs" onclick="showAddTagModal(${pid})">+ Tag</button>
                    </div>
                </div>
                <div class="btn-group">
                    <button class="btn btn-sm" onclick="showEditPatientModal(${pid})">Edit</button>
                    <button class="btn btn-sm btn-primary" onclick="showAddReminderModal(${pid})">+ Reminder</button>
                    <button class="btn btn-sm" onclick="showAddContactModal(${pid})">+ Contact Log</button>
                </div>
            </div>

            ${allergiesHtml}
            ${stickyHtml}

            <div class="tabs" id="chart-tabs">
                <div class="tab active" onclick="switchTab('overview',${pid})">Overview</div>
                <div class="tab" onclick="switchTab('problems',${pid})">Problems (${p.problems.filter(x=>x.status==='active').length})</div>
                <div class="tab" onclick="switchTab('meds',${pid})">Medications (${p.medications.filter(x=>x.active).length})</div>
                <div class="tab" onclick="switchTab('labs',${pid})">Labs (${p.labs.length})</div>
                <div class="tab" onclick="switchTab('preventive',${pid})">Preventive (${p.preventive_care.filter(x=>x.status==='due'||x.status==='overdue').length} due)</div>
                <div class="tab" onclick="switchTab('referrals',${pid})">Referrals</div>
                <div class="tab" onclick="switchTab('family',${pid})">Family</div>
                <div class="tab" onclick="switchTab('contacts',${pid})">Contact Log</div>
            </div>

            <div id="tab-content"></div>
        </div>`;

        switchTab("overview", pid, p);
    } catch (e) {
        main().innerHTML = `<p class="text-danger">Error: ${esc(e.message)}</p>`;
    }
}

async function switchTab(tab, pid, cachedPatient) {
    $$("#chart-tabs .tab").forEach((t, i) => t.classList.toggle("active", t.textContent.toLowerCase().startsWith(tab)));
    const container = $("#tab-content");
    const p = cachedPatient || await api(`/patients/${pid}`);

    switch (tab) {
        case "overview":
            container.innerHTML = renderOverviewTab(p);
            break;
        case "problems":
            container.innerHTML = renderProblemsTab(p);
            break;
        case "meds":
            container.innerHTML = renderMedsTab(p);
            break;
        case "labs":
            container.innerHTML = renderLabsTab(p);
            break;
        case "preventive":
            container.innerHTML = renderPreventiveTab(p);
            break;
        case "referrals":
            container.innerHTML = renderReferralsTab(p);
            break;
        case "family":
            container.innerHTML = renderFamilyTab(p);
            await initFamilyTree(pid);
            break;
        case "contacts":
            container.innerHTML = renderContactsTab(p);
            break;
    }
}

function renderOverviewTab(p) {
    const activeProblems = p.problems.filter(x => x.status === "active");
    const activeMeds = p.medications.filter(x => x.active);
    const openReminders = p.reminders.filter(x => !x.completed);
    const duePrev = p.preventive_care.filter(x => x.status === "due" || x.status === "overdue");
    const pendingLabs = p.labs.filter(x => x.status === "ordered" || x.status === "pending");
    const pendingRefs = p.referrals.filter(x => !x.consult_received);

    return `
    <div class="dashboard-grid">
        <div class="card">
            <div class="card-header"><h2>Active Problems (${activeProblems.length})</h2></div>
            <div class="card-body">
                ${activeProblems.length ? `<ul style="list-style:none;padding:0;">${activeProblems.map(pr => `<li style="padding:4px 0;border-bottom:1px solid var(--border);">${esc(pr.description)} ${pr.onset_date ? `<span class="text-sm text-muted">since ${formatDate(pr.onset_date)}</span>` : ''}</li>`).join('')}</ul>` : '<p class="text-muted">No active problems.</p>'}
            </div>
        </div>

        <div class="card">
            <div class="card-header"><h2>Open Reminders (${openReminders.length})</h2></div>
            <div class="card-body">
                ${openReminders.length ? `<ul style="list-style:none;padding:0;">${openReminders.map(r => `<li style="padding:4px 0;border-bottom:1px solid var(--border);" class="flex justify-between items-center">
                    <span>${esc(r.title)} ${r.reason ? `<span class="text-sm text-muted">— ${esc(r.reason)}</span>` : ''}</span>
                    <span class="flex gap-1 items-center"><span class="${r.due_date <= todayStr() ? 'overdue' : 'text-muted'} text-sm">${formatDate(r.due_date)}</span>
                    <button class="btn btn-xs btn-success" onclick="completeReminder(${r.id})">Done</button></span>
                </li>`).join('')}</ul>` : '<p class="text-muted">No open reminders.</p>'}
            </div>
        </div>

        <div class="card">
            <div class="card-header"><h2>Current Medications (${activeMeds.length})</h2></div>
            <div class="card-body">
                ${activeMeds.length ? `<ul style="list-style:none;padding:0;">${activeMeds.slice(0,8).map(m => {
                    const runout = m.run_out_date;
                    const urgent = runout && runout <= todayStr();
                    const soon = runout && !urgent && runout <= futureDate(14);
                    return `<li style="padding:4px 0;border-bottom:1px solid var(--border);"><strong>${esc(m.name)}</strong> ${m.dose || ''} ${m.frequency || ''} ${runout ? `<span class="text-sm ${urgent ? 'overdue' : soon ? 'due-soon' : 'text-muted'}">runs out ${formatDate(runout)}</span>` : ''}</li>`;
                }).join('')}${activeMeds.length > 8 ? `<li class="text-sm text-muted" style="padding:4px 0;">+${activeMeds.length - 8} more</li>` : ''}</ul>` : '<p class="text-muted">No active medications.</p>'}
            </div>
        </div>

        <div class="card">
            <div class="card-header"><h2>Action Items</h2></div>
            <div class="card-body">
                <ul style="list-style:none;padding:0;">
                    ${pendingLabs.map(l => `<li style="padding:4px 0;border-bottom:1px solid var(--border);"><span class="badge badge-info">Lab</span> ${esc(l.test_name)} — ${l.status} (ordered ${formatDate(l.ordered_date)})</li>`).join('')}
                    ${pendingRefs.map(r => `<li style="padding:4px 0;border-bottom:1px solid var(--border);"><span class="badge badge-warning">Referral</span> ${esc(r.specialty)} — awaiting consult (sent ${formatDate(r.date_sent)})</li>`).join('')}
                    ${duePrev.map(pc => `<li style="padding:4px 0;border-bottom:1px solid var(--border);"><span class="badge badge-danger">Screening</span> ${esc(pc.rule_name)} — ${pc.status}</li>`).join('')}
                    ${(!pendingLabs.length && !pendingRefs.length && !duePrev.length) ? '<li class="text-muted">No pending action items.</li>' : ''}
                </ul>
            </div>
        </div>
    </div>`;
}

function renderProblemsTab(p) {
    const active = p.problems.filter(x => x.status === "active");
    const inactive = p.problems.filter(x => x.status !== "active");
    return `
    <div class="card">
        <div class="card-header">
            <h2>Problems</h2>
            <button class="btn btn-sm btn-primary" onclick="showAddProblemModal(${p.id})">+ Add</button>
        </div>
        <div class="card-body">
            ${active.length ? `
            <h3 style="font-size:13px;font-weight:600;margin-bottom:8px;">Active</h3>
            <table class="data-table">
                <tr><th>Problem</th><th>Onset</th><th>Notes</th><th></th></tr>
                ${active.map(pr => `<tr>
                    <td>${esc(pr.description)}</td>
                    <td>${pr.onset_date ? formatDate(pr.onset_date) : '—'}</td>
                    <td class="text-sm text-muted">${esc(pr.notes || '')}</td>
                    <td class="btn-group">
                        <button class="btn btn-xs" onclick="resolveProblem(${pr.id})">Resolve</button>
                        <button class="btn btn-xs btn-danger" onclick="deleteProblem(${pr.id})">Del</button>
                    </td>
                </tr>`).join('')}
            </table>` : '<p class="text-muted mb-4">No active problems.</p>'}

            ${inactive.length ? `
            <h3 style="font-size:13px;font-weight:600;margin:16px 0 8px;">Inactive / Resolved</h3>
            <table class="data-table">
                <tr><th>Problem</th><th>Status</th><th>Resolved</th></tr>
                ${inactive.map(pr => `<tr style="opacity:0.6;">
                    <td>${esc(pr.description)}</td>
                    <td><span class="badge badge-${pr.status === 'resolved' ? 'success' : 'info'}">${pr.status}</span></td>
                    <td>${pr.resolved_date ? formatDate(pr.resolved_date) : '—'}</td>
                </tr>`).join('')}
            </table>` : ''}
        </div>
    </div>`;
}

function renderMedsTab(p) {
    const active = p.medications.filter(x => x.active);
    const inactive = p.medications.filter(x => !x.active);
    return `
    <div class="card">
        <div class="card-header">
            <h2>Medications</h2>
            <button class="btn btn-sm btn-primary" onclick="showAddMedModal(${p.id})">+ Add</button>
        </div>
        <div class="card-body">
            ${active.length ? `
            <table class="data-table">
                <tr><th>Medication</th><th>Dose</th><th>Frequency</th><th>Last Filled</th><th>Runs Out</th><th>Refills</th><th></th></tr>
                ${active.map(m => {
                    const urgent = m.run_out_date && m.run_out_date <= todayStr();
                    const soon = m.run_out_date && !urgent && m.run_out_date <= futureDate(14);
                    return `<tr>
                        <td><strong>${esc(m.name)}</strong></td>
                        <td>${esc(m.dose || '—')}</td>
                        <td>${esc(m.frequency || '—')}</td>
                        <td>${m.last_filled_date ? formatDate(m.last_filled_date) : '—'}</td>
                        <td class="${urgent ? 'overdue' : soon ? 'due-soon' : ''}">${m.run_out_date ? formatDate(m.run_out_date) : '—'}</td>
                        <td>${m.refills_remaining ?? '—'}</td>
                        <td class="btn-group">
                            <button class="btn btn-xs" onclick="refillMed(${m.id},${m.days_supply || 30})">Refill</button>
                            <button class="btn btn-xs" onclick="showEditMedModal(${m.id})">Edit</button>
                            <button class="btn btn-xs btn-danger" onclick="stopMed(${m.id})">Stop</button>
                        </td>
                    </tr>`;
                }).join('')}
            </table>` : '<p class="text-muted">No active medications.</p>'}

            ${inactive.length ? `
            <h3 style="font-size:13px;font-weight:600;margin:16px 0 8px;">Discontinued</h3>
            <table class="data-table">
                ${inactive.map(m => `<tr style="opacity:0.6;"><td>${esc(m.name)}</td><td>${esc(m.dose || '')}</td><td>${esc(m.frequency || '')}</td></tr>`).join('')}
            </table>` : ''}
        </div>
    </div>`;
}

function renderLabsTab(p) {
    return `
    <div class="card">
        <div class="card-header">
            <h2>Labs</h2>
            <button class="btn btn-sm btn-primary" onclick="showAddLabModal(${p.id})">+ Order Lab</button>
        </div>
        <div class="card-body">
            ${p.labs.length ? `
            <table class="data-table">
                <tr><th>Test</th><th>Ordered</th><th>Result Date</th><th>Value</th><th>Status</th><th>Follow-up</th><th></th></tr>
                ${p.labs.map(l => `<tr>
                    <td>${esc(l.test_name)}</td>
                    <td>${formatDate(l.ordered_date)}</td>
                    <td>${l.result_date ? formatDate(l.result_date) : '—'}</td>
                    <td>${esc(l.result_value || '—')}</td>
                    <td><span class="badge badge-${l.status === 'reviewed' ? 'success' : l.status === 'resulted' ? 'warning' : 'info'}">${l.status}</span></td>
                    <td>${l.followup_needed ? `<span class="text-danger">Yes</span> ${esc(l.followup_notes || '')}` : '—'}</td>
                    <td class="btn-group">
                        ${l.status !== 'reviewed' ? `<button class="btn btn-xs" onclick="showEditLabModal(${l.id})">Update</button>` : ''}
                    </td>
                </tr>`).join('')}
            </table>` : '<p class="text-muted">No labs recorded.</p>'}
        </div>
    </div>`;
}

function renderPreventiveTab(p) {
    const due = p.preventive_care.filter(x => x.status === "due" || x.status === "overdue");
    const done = p.preventive_care.filter(x => x.status === "completed");
    const declined = p.preventive_care.filter(x => x.status === "declined" || x.status === "not_applicable");

    return `
    <div class="card">
        <div class="card-header"><h2>Preventive Care</h2></div>
        <div class="card-body">
            ${due.length ? `
            <h3 style="font-size:13px;font-weight:600;margin-bottom:8px;">Due / Overdue</h3>
            <table class="data-table">
                <tr><th>Screening</th><th>Category</th><th>Next Due</th><th>Last Done</th><th></th></tr>
                ${due.map(pc => `<tr>
                    <td><strong>${esc(pc.rule_name)}</strong><br><span class="text-sm text-muted">${esc(pc.rule_description || '')}</span></td>
                    <td><span class="badge badge-${pc.category === 'immunization' ? 'info' : pc.category === 'lab' ? 'warning' : 'danger'}">${pc.category}</span></td>
                    <td class="overdue">${pc.next_due_date ? formatDate(pc.next_due_date) : 'Now'}</td>
                    <td>${pc.last_done_date ? formatDate(pc.last_done_date) : 'Never'}</td>
                    <td class="btn-group">
                        <button class="btn btn-xs btn-success" onclick="markPreventiveDone(${pc.id})">Done</button>
                        <button class="btn btn-xs" onclick="declinePreventive(${pc.id})">Decline</button>
                    </td>
                </tr>`).join('')}
            </table>` : '<p class="text-muted mb-4">All screenings up to date!</p>'}

            ${done.length ? `
            <h3 style="font-size:13px;font-weight:600;margin:16px 0 8px;">Completed</h3>
            <table class="data-table">
                ${done.map(pc => `<tr>
                    <td>${esc(pc.rule_name)}</td>
                    <td>${pc.last_done_date ? formatDate(pc.last_done_date) : '—'}</td>
                    <td class="text-muted">${pc.next_due_date ? `Next: ${formatDate(pc.next_due_date)}` : 'One-time'}</td>
                </tr>`).join('')}
            </table>` : ''}

            ${declined.length ? `
            <h3 style="font-size:13px;font-weight:600;margin:16px 0 8px;">Declined / N/A</h3>
            <table class="data-table">
                ${declined.map(pc => `<tr style="opacity:0.6;"><td>${esc(pc.rule_name)}</td><td>${pc.status}</td><td class="text-sm">${esc(pc.notes || '')}</td></tr>`).join('')}
            </table>` : ''}
        </div>
    </div>`;
}

function renderReferralsTab(p) {
    return `
    <div class="card">
        <div class="card-header">
            <h2>Referrals</h2>
            <button class="btn btn-sm btn-primary" onclick="showAddReferralModal(${p.id})">+ Add</button>
        </div>
        <div class="card-body">
            ${p.referrals.length ? `
            <table class="data-table">
                <tr><th>Specialty</th><th>Provider</th><th>Reason</th><th>Sent</th><th>Consult Rcvd</th><th></th></tr>
                ${p.referrals.map(r => `<tr>
                    <td><strong>${esc(r.specialty)}</strong></td>
                    <td>${esc(r.provider_name || '—')}</td>
                    <td class="text-sm">${esc(r.reason || '—')}</td>
                    <td>${formatDate(r.date_sent)}</td>
                    <td>${r.consult_received ? `<span class="badge badge-success">Yes</span> ${r.consult_date ? formatDate(r.consult_date) : ''}` : '<span class="badge badge-warning">No</span>'}</td>
                    <td>${!r.consult_received ? `<button class="btn btn-xs btn-success" onclick="markConsultReceived(${r.id})">Received</button>` : ''}</td>
                </tr>`).join('')}
            </table>` : '<p class="text-muted">No referrals.</p>'}
        </div>
    </div>`;
}

function renderFamilyTab(p) {
    return `
    <div class="card">
        <div class="card-header">
            <h2>Family Tree</h2>
            <button class="btn btn-sm btn-primary" onclick="showAddFamilyModal(${p.id})">+ Link Family Member</button>
        </div>
        <div class="card-body">
            <div id="family-tree-container"></div>
            ${p.family.length ? `
            <table class="data-table mt-4">
                <tr><th>Name</th><th>Relationship</th><th>DOB</th><th></th></tr>
                ${p.family.map(f => `<tr>
                    <td class="clickable" onclick="navigate('patient',${f.related_patient_id})"><strong>${esc(f.first_name)} ${esc(f.last_name)}</strong></td>
                    <td>${esc(f.relationship)}</td>
                    <td>${formatDate(f.dob)} (${computeAge(f.dob)}y ${f.sex})</td>
                    <td><button class="btn btn-xs btn-danger" onclick="removeFamily(${p.id},${f.related_patient_id})">Unlink</button></td>
                </tr>`).join('')}
            </table>` : '<p class="text-muted mt-4">No family members linked. Click "+ Link Family Member" to connect patients in the same family.</p>'}
        </div>
    </div>`;
}

function renderContactsTab(p) {
    return `
    <div class="card">
        <div class="card-header">
            <h2>Contact Log</h2>
            <button class="btn btn-sm btn-primary" onclick="showAddContactModal(${p.id})">+ Add Entry</button>
        </div>
        <div class="card-body">
            ${p.contact_log.length ? `
            <table class="data-table">
                <tr><th>Date</th><th>Method</th><th>Summary</th><th>Follow-up</th></tr>
                ${p.contact_log.map(c => `<tr>
                    <td>${formatDateTime(c.contact_date)}</td>
                    <td><span class="badge badge-info">${c.method}</span></td>
                    <td>${esc(c.summary)}</td>
                    <td>${c.followup_needed ? `<span class="text-danger">Yes</span> ${c.followup_date ? formatDate(c.followup_date) : ''}` : '—'}</td>
                </tr>`).join('')}
            </table>` : '<p class="text-muted">No contact history.</p>'}
        </div>
    </div>`;
}


// ── Family tree vis.js ─────────────────────────────────────────────────────

async function initFamilyTree(pid) {
    const container = document.getElementById("family-tree-container");
    if (!container) return;
    try {
        const data = await api(`/patients/${pid}/family-tree`);
        if (!data.nodes.length) {
            container.innerHTML = '<div class="empty-state"><p>No family connections yet.</p></div>';
            return;
        }
        const network = new vis.Network(container, {
            nodes: new vis.DataSet(data.nodes),
            edges: new vis.DataSet(data.edges),
        }, {
            layout: { hierarchical: { direction: "UD", sortMethod: "directed", levelSeparation: 100 } },
            physics: false,
            interaction: { hover: true },
            edges: { font: { size: 11, color: "#64748b" }, color: { color: "#94a3b8" } },
        });
        network.on("click", params => {
            if (params.nodes.length) navigate("patient", params.nodes[0]);
        });
    } catch (e) {
        container.innerHTML = `<p class="text-danger text-sm">Error loading family tree.</p>`;
    }
}


// ── Registry page ──────────────────────────────────────────────────────────

async function renderRegistry() {
    main().innerHTML = `
    <h2 style="font-size:20px;margin-bottom:16px;">Chronic Disease Registries</h2>
    <p class="text-muted mb-4">Filter your panel by active problem to manage chronic disease populations.</p>
    <div class="form-row mb-4">
        <div class="form-group">
            <label>Filter by problem</label>
            <input type="text" id="registry-search" placeholder='e.g. "diabetes", "CHF", "COPD"' onchange="loadRegistry(this.value)">
        </div>
        <div class="form-group">
            <label>Quick filters</label>
            <div class="btn-group" style="flex-wrap:wrap;">
                <button class="btn btn-sm" onclick="loadRegistry('diabetes')">Diabetes</button>
                <button class="btn btn-sm" onclick="loadRegistry('hypertension')">Hypertension</button>
                <button class="btn btn-sm" onclick="loadRegistry('CHF')">CHF</button>
                <button class="btn btn-sm" onclick="loadRegistry('COPD')">COPD</button>
                <button class="btn btn-sm" onclick="loadRegistry('asthma')">Asthma</button>
                <button class="btn btn-sm" onclick="loadRegistry('depression')">Depression</button>
                <button class="btn btn-sm" onclick="loadRegistry('anxiety')">Anxiety</button>
                <button class="btn btn-sm" onclick="loadRegistry('warfarin')">On Warfarin</button>
            </div>
        </div>
    </div>
    <div id="registry-results"></div>`;
}

async function loadRegistry(term) {
    const el = $("#registry-search");
    if (el) el.value = term;
    const container = $("#registry-results");
    container.innerHTML = '<p class="text-muted">Searching...</p>';

    // Search for patients with this problem OR medication
    const data = await api(`/patients?problem=${encodeURIComponent(term)}&per_page=100`);
    container.innerHTML = `
    <div class="card">
        <div class="card-header">
            <h2>Results for "${esc(term)}" (${data.total} patients)</h2>
        </div>
        <div class="card-body">
            ${data.patients.length ? `
            <table class="data-table">
                <tr><th>Name</th><th>Age/Sex</th><th>Phone</th><th>Tags</th></tr>
                ${data.patients.map(p => `<tr class="clickable" onclick="navigate('patient',${p.id})">
                    <td><strong>${esc(p.last_name)}, ${esc(p.first_name)}</strong></td>
                    <td>${computeAge(p.dob)}y ${p.sex}</td>
                    <td>${esc(p.phone || '—')}</td>
                    <td>${(p.tags || []).map(t => `<span class="tag" style="background:${t.color}">${esc(t.name)}</span>`).join(' ')}</td>
                </tr>`).join('')}
            </table>` : '<p class="text-muted">No patients found with this condition.</p>'}
        </div>
    </div>`;
}


// ── Reminders page ─────────────────────────────────────────────────────────

async function renderRemindersPage() {
    const d = await api("/dashboard");
    const all = d.reminders;
    const overdue = all.filter(r => r.due_date <= todayStr());
    const upcoming = all.filter(r => r.due_date > todayStr());

    main().innerHTML = `
    <h2 style="font-size:20px;margin-bottom:16px;">All Reminders</h2>
    <div class="card">
        <div class="card-header"><h2 class="text-danger">Overdue (${overdue.length})</h2></div>
        <div class="card-body">
            ${overdue.length ? `<table class="data-table">
                <tr><th>Patient</th><th>Task</th><th>Reason</th><th>Due</th><th></th></tr>
                ${overdue.map(r => `<tr>
                    <td class="clickable" onclick="navigate('patient',${r.patient_id})">${r.last_name}, ${r.first_name}</td>
                    <td>${esc(r.title)}</td>
                    <td class="text-sm">${esc(r.reason || '')}</td>
                    <td class="overdue">${formatDate(r.due_date)}</td>
                    <td><button class="btn btn-xs btn-success" onclick="completeReminder(${r.id})">Done</button></td>
                </tr>`).join('')}
            </table>` : '<p class="text-muted">None overdue!</p>'}
        </div>
    </div>
    <div class="card">
        <div class="card-header"><h2>Upcoming (${upcoming.length})</h2></div>
        <div class="card-body">
            ${upcoming.length ? `<table class="data-table">
                <tr><th>Patient</th><th>Task</th><th>Reason</th><th>Due</th><th></th></tr>
                ${upcoming.map(r => `<tr>
                    <td class="clickable" onclick="navigate('patient',${r.patient_id})">${r.last_name}, ${r.first_name}</td>
                    <td>${esc(r.title)}</td>
                    <td class="text-sm">${esc(r.reason || '')}</td>
                    <td>${formatDate(r.due_date)}</td>
                    <td><button class="btn btn-xs btn-success" onclick="completeReminder(${r.id})">Done</button></td>
                </tr>`).join('')}
            </table>` : '<p class="text-muted">No upcoming reminders.</p>'}
        </div>
    </div>`;
}


// ── Modals ──────────────────────────────────────────────────────────────────

function showModal(title, bodyHtml, footerHtml) {
    // Remove existing modal
    const existing = $(".modal-overlay");
    if (existing) existing.remove();

    const overlay = document.createElement("div");
    overlay.className = "modal-overlay";
    overlay.onclick = (e) => { if (e.target === overlay) overlay.remove(); };
    overlay.innerHTML = `
    <div class="modal">
        <div class="modal-header">
            <h3>${title}</h3>
            <button class="modal-close" onclick="this.closest('.modal-overlay').remove()">&times;</button>
        </div>
        <div class="modal-body">${bodyHtml}</div>
        ${footerHtml ? `<div class="modal-footer">${footerHtml}</div>` : ''}
    </div>`;
    document.body.appendChild(overlay);
}

function closeModal() {
    const m = $(".modal-overlay");
    if (m) m.remove();
}

// ── Add patient modal ──

function showAddPatientModal() {
    showModal("New Patient", `
    <div class="form-row">
        <div class="form-group"><label>First Name *</label><input id="m-fname" required></div>
        <div class="form-group"><label>Last Name *</label><input id="m-lname" required></div>
    </div>
    <div class="form-row-3">
        <div class="form-group"><label>Date of Birth *</label><input type="date" id="m-dob" required></div>
        <div class="form-group"><label>Sex *</label><select id="m-sex"><option value="M">Male</option><option value="F">Female</option><option value="O">Other</option></select></div>
        <div class="form-group"><label>Phone</label><input id="m-phone" type="tel"></div>
    </div>
    <div class="form-row">
        <div class="form-group"><label>Email</label><input id="m-email" type="email"></div>
        <div class="form-group"><label>Pharmacy</label><input id="m-pharmacy"></div>
    </div>
    <div class="form-group"><label>Address</label><input id="m-address"></div>
    <div class="form-group"><label>Preferred Contact</label><select id="m-prefcontact"><option value="phone">Phone</option><option value="email">Email</option><option value="mail">Mail</option></select></div>
    `, `<button class="btn" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="saveNewPatient()">Save Patient</button>`);
}

async function saveNewPatient() {
    try {
        const data = {
            first_name: $("#m-fname").value.trim(),
            last_name: $("#m-lname").value.trim(),
            dob: $("#m-dob").value,
            sex: $("#m-sex").value,
            phone: $("#m-phone").value.trim(),
            email: $("#m-email").value.trim(),
            pharmacy: $("#m-pharmacy").value.trim(),
            address: $("#m-address").value.trim(),
            preferred_contact: $("#m-prefcontact").value,
        };
        if (!data.first_name || !data.last_name || !data.dob) {
            toast("Please fill in required fields.", "error");
            return;
        }
        const res = await api("/patients", { method: "POST", body: data });
        toast("Patient created!", "success");
        closeModal();
        navigate("patient", res.id);
    } catch (e) { toast(e.message, "error"); }
}

// ── Edit patient modal ──

async function showEditPatientModal(pid) {
    const p = await api(`/patients/${pid}`);
    showModal("Edit Patient", `
    <div class="form-row">
        <div class="form-group"><label>First Name</label><input id="m-fname" value="${escAttr(p.first_name)}"></div>
        <div class="form-group"><label>Last Name</label><input id="m-lname" value="${escAttr(p.last_name)}"></div>
    </div>
    <div class="form-row-3">
        <div class="form-group"><label>DOB</label><input type="date" id="m-dob" value="${p.dob}"></div>
        <div class="form-group"><label>Sex</label><select id="m-sex"><option value="M" ${p.sex==='M'?'selected':''}>Male</option><option value="F" ${p.sex==='F'?'selected':''}>Female</option><option value="O" ${p.sex==='O'?'selected':''}>Other</option></select></div>
        <div class="form-group"><label>Phone</label><input id="m-phone" value="${escAttr(p.phone||'')}"></div>
    </div>
    <div class="form-row">
        <div class="form-group"><label>Email</label><input id="m-email" value="${escAttr(p.email||'')}"></div>
        <div class="form-group"><label>Pharmacy</label><input id="m-pharmacy" value="${escAttr(p.pharmacy||'')}"></div>
    </div>
    <div class="form-group"><label>Address</label><input id="m-address" value="${escAttr(p.address||'')}"></div>
    `, `<button class="btn" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="saveEditPatient(${pid})">Save</button>`);
}

async function saveEditPatient(pid) {
    try {
        await api(`/patients/${pid}`, { method: "PUT", body: {
            first_name: $("#m-fname").value.trim(),
            last_name: $("#m-lname").value.trim(),
            dob: $("#m-dob").value,
            sex: $("#m-sex").value,
            phone: $("#m-phone").value.trim(),
            email: $("#m-email").value.trim(),
            pharmacy: $("#m-pharmacy").value.trim(),
            address: $("#m-address").value.trim(),
        }});
        toast("Patient updated!", "success");
        closeModal();
        renderPatientChart();
    } catch (e) { toast(e.message, "error"); }
}

// ── Sticky note ──

function editStickyNote(pid, current) {
    showModal("Sticky Note", `
    <div class="form-group"><label>Quick note (always visible on chart)</label>
        <textarea id="m-sticky" rows="4">${esc(current)}</textarea>
    </div>
    `, `<button class="btn" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="saveStickyNote(${pid})">Save</button>`);
}

async function saveStickyNote(pid) {
    try {
        await api(`/patients/${pid}`, { method: "PUT", body: { notes: $("#m-sticky").value } });
        toast("Note saved!", "success");
        closeModal();
        renderPatientChart();
    } catch (e) { toast(e.message, "error"); }
}

// ── Allergy modal ──

function showAddAllergyModal(pid) {
    showModal("Add Allergy", `
    <div class="form-group"><label>Allergen *</label><input id="m-allergen" placeholder="e.g. Penicillin"></div>
    <div class="form-row">
        <div class="form-group"><label>Reaction</label><input id="m-reaction" placeholder="e.g. Hives, anaphylaxis"></div>
        <div class="form-group"><label>Severity</label><select id="m-severity"><option value="mild">Mild</option><option value="moderate" selected>Moderate</option><option value="severe">Severe</option></select></div>
    </div>
    `, `<button class="btn" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="saveAllergy(${pid})">Save</button>`);
}

async function saveAllergy(pid) {
    try {
        await api(`/patients/${pid}/allergies`, { method: "POST", body: {
            allergen: $("#m-allergen").value.trim(),
            reaction: $("#m-reaction").value.trim(),
            severity: $("#m-severity").value,
        }});
        toast("Allergy added!", "success");
        closeModal();
        renderPatientChart();
    } catch (e) { toast(e.message, "error"); }
}

// ── Problem modal ──

function showAddProblemModal(pid) {
    showModal("Add Problem", `
    <div class="form-group"><label>Problem *</label><input id="m-problem" placeholder="e.g. Type 2 Diabetes Mellitus"></div>
    <div class="form-row">
        <div class="form-group"><label>Onset Date</label><input type="date" id="m-onset"></div>
        <div class="form-group"><label>Status</label><select id="m-pstatus"><option value="active">Active</option><option value="inactive">Inactive</option></select></div>
    </div>
    <div class="form-group"><label>Notes</label><textarea id="m-pnotes"></textarea></div>
    `, `<button class="btn" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="saveProblem(${pid})">Save</button>`);
}

async function saveProblem(pid) {
    try {
        await api(`/patients/${pid}/problems`, { method: "POST", body: {
            description: $("#m-problem").value.trim(),
            onset_date: $("#m-onset").value || null,
            status: $("#m-pstatus").value,
            notes: $("#m-pnotes").value.trim() || null,
        }});
        toast("Problem added!", "success");
        closeModal();
        renderPatientChart();
    } catch (e) { toast(e.message, "error"); }
}

async function resolveProblem(probId) {
    await api(`/problems/${probId}`, { method: "PUT", body: { status: "resolved", resolved_date: todayStr() } });
    toast("Problem resolved.", "success");
    renderPatientChart();
}

async function deleteProblem(probId) {
    if (!confirm("Delete this problem?")) return;
    await api(`/problems/${probId}`, { method: "DELETE" });
    renderPatientChart();
}

// ── Medication modal ──

function showAddMedModal(pid) {
    showModal("Add Medication", `
    <div class="form-group"><label>Medication Name *</label><input id="m-medname" placeholder="e.g. Metformin"></div>
    <div class="form-row">
        <div class="form-group"><label>Dose</label><input id="m-meddose" placeholder="e.g. 500mg"></div>
        <div class="form-group"><label>Frequency</label><input id="m-medfreq" placeholder="e.g. BID"></div>
    </div>
    <div class="form-row-3">
        <div class="form-group"><label>Qty Dispensed</label><input type="number" id="m-medqty"></div>
        <div class="form-group"><label>Days Supply</label><input type="number" id="m-meddays" value="30"></div>
        <div class="form-group"><label>Refills Remaining</label><input type="number" id="m-medrefills"></div>
    </div>
    <div class="form-row">
        <div class="form-group"><label>Last Filled</label><input type="date" id="m-medfilled" value="${todayStr()}"></div>
        <div class="form-group"><label>Remind Days Before</label><input type="number" id="m-medremind" value="7"></div>
    </div>
    <div class="form-group"><label>Notes</label><textarea id="m-mednotes"></textarea></div>
    `, `<button class="btn" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="saveMed(${pid})">Save</button>`);
}

async function saveMed(pid) {
    try {
        await api(`/patients/${pid}/medications`, { method: "POST", body: {
            name: $("#m-medname").value.trim(),
            dose: $("#m-meddose").value.trim() || null,
            frequency: $("#m-medfreq").value.trim() || null,
            quantity_dispensed: parseInt($("#m-medqty").value) || null,
            days_supply: parseInt($("#m-meddays").value) || null,
            last_filled_date: $("#m-medfilled").value || null,
            refills_remaining: parseInt($("#m-medrefills").value) || null,
            prescriber_notes: $("#m-mednotes").value.trim() || null,
            remind_days_before: parseInt($("#m-medremind").value) || 7,
        }});
        toast("Medication added!", "success");
        closeModal();
        renderPatientChart();
    } catch (e) { toast(e.message, "error"); }
}

async function showEditMedModal(mid) {
    // Fetch from existing data
    showModal("Edit Medication", `
    <div class="form-row">
        <div class="form-group"><label>Days Supply</label><input type="number" id="m-meddays"></div>
        <div class="form-group"><label>Last Filled</label><input type="date" id="m-medfilled" value="${todayStr()}"></div>
    </div>
    <div class="form-row">
        <div class="form-group"><label>Refills Remaining</label><input type="number" id="m-medrefills"></div>
        <div class="form-group"><label>Remind Days Before</label><input type="number" id="m-medremind" value="7"></div>
    </div>
    `, `<button class="btn" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="saveEditMed(${mid})">Save</button>`);
}

async function saveEditMed(mid) {
    const body = {};
    const days = $("#m-meddays").value;
    const filled = $("#m-medfilled").value;
    const refills = $("#m-medrefills").value;
    const remind = $("#m-medremind").value;
    if (days) body.days_supply = parseInt(days);
    if (filled) body.last_filled_date = filled;
    if (refills) body.refills_remaining = parseInt(refills);
    if (remind) body.remind_days_before = parseInt(remind);
    await api(`/medications/${mid}`, { method: "PUT", body });
    toast("Medication updated!", "success");
    closeModal();
    renderPatientChart();
}

async function refillMed(mid, daysSupply) {
    await api(`/medications/${mid}`, { method: "PUT", body: { last_filled_date: todayStr(), days_supply: daysSupply } });
    toast("Refill recorded!", "success");
    renderPatientChart();
}

async function stopMed(mid) {
    if (!confirm("Discontinue this medication?")) return;
    await api(`/medications/${mid}`, { method: "PUT", body: { active: 0 } });
    toast("Medication discontinued.", "success");
    renderPatientChart();
}

// ── Lab modal ──

function showAddLabModal(pid) {
    showModal("Order Lab", `
    <div class="form-group"><label>Test Name *</label><input id="m-labtest" placeholder="e.g. CBC, CMP, A1c"></div>
    <div class="form-row">
        <div class="form-group"><label>Order Date</label><input type="date" id="m-labdate" value="${todayStr()}"></div>
        <div class="form-group"><label>Status</label><select id="m-labstatus"><option value="ordered">Ordered</option><option value="pending">Pending</option></select></div>
    </div>
    `, `<button class="btn" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="saveLab(${pid})">Save</button>`);
}

async function saveLab(pid) {
    try {
        await api(`/patients/${pid}/labs`, { method: "POST", body: {
            test_name: $("#m-labtest").value.trim(),
            ordered_date: $("#m-labdate").value,
            status: $("#m-labstatus").value,
        }});
        toast("Lab ordered!", "success");
        closeModal();
        renderPatientChart();
    } catch (e) { toast(e.message, "error"); }
}

function showEditLabModal(lid) {
    showModal("Update Lab Result", `
    <div class="form-row">
        <div class="form-group"><label>Result Date</label><input type="date" id="m-labresdate" value="${todayStr()}"></div>
        <div class="form-group"><label>Status</label><select id="m-labstatus"><option value="resulted">Resulted</option><option value="reviewed">Reviewed</option></select></div>
    </div>
    <div class="form-group"><label>Result Value</label><input id="m-labval" placeholder="e.g. 6.8%, 142 mg/dL"></div>
    <div class="form-row">
        <div class="form-group"><label>Follow-up Needed?</label><select id="m-labfu"><option value="0">No</option><option value="1">Yes</option></select></div>
        <div class="form-group"><label>Follow-up Notes</label><input id="m-labfunotes"></div>
    </div>
    `, `<button class="btn" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="saveEditLab(${lid})">Save</button>`);
}

async function saveEditLab(lid) {
    await api(`/labs/${lid}`, { method: "PUT", body: {
        result_date: $("#m-labresdate").value || null,
        result_value: $("#m-labval").value.trim() || null,
        status: $("#m-labstatus").value,
        followup_needed: parseInt($("#m-labfu").value),
        followup_notes: $("#m-labfunotes").value.trim() || null,
    }});
    toast("Lab updated!", "success");
    closeModal();
    renderPatientChart();
}

// ── Reminder modal ──

function showAddReminderModal(pid) {
    showModal("Add Reminder", `
    <div class="form-group"><label>Title *</label><input id="m-remtitle" placeholder="e.g. Call about K+ result"></div>
    <div class="form-group"><label>Reason</label><input id="m-remreason" placeholder="e.g. K+ was 5.8, needs recheck"></div>
    <div class="form-group"><label>Due Date *</label><input type="date" id="m-remdue" value="${todayStr()}"></div>
    `, `<button class="btn" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="saveReminder(${pid})">Save</button>`);
}

async function saveReminder(pid) {
    try {
        await api(`/patients/${pid}/reminders`, { method: "POST", body: {
            title: $("#m-remtitle").value.trim(),
            reason: $("#m-remreason").value.trim() || null,
            due_date: $("#m-remdue").value,
        }});
        toast("Reminder added!", "success");
        closeModal();
        renderPatientChart();
    } catch (e) { toast(e.message, "error"); }
}

async function completeReminder(rid) {
    await api(`/reminders/${rid}`, { method: "PUT", body: { completed: 1 } });
    toast("Reminder completed!", "success");
    if (currentPage === "dashboard") renderDashboard();
    else if (currentPage === "reminders") renderRemindersPage();
    else if (currentPage === "patient") renderPatientChart();
}

// ── Contact modal ──

function showAddContactModal(pid) {
    showModal("Add Contact Log", `
    <div class="form-row">
        <div class="form-group"><label>Date</label><input type="datetime-local" id="m-cdate" value="${new Date().toISOString().slice(0,16)}"></div>
        <div class="form-group"><label>Method</label><select id="m-cmethod"><option value="phone">Phone</option><option value="in_person">In Person</option><option value="email">Email</option><option value="portal">Portal</option><option value="mail">Mail</option><option value="other">Other</option></select></div>
    </div>
    <div class="form-group"><label>Summary *</label><textarea id="m-csummary" placeholder="e.g. Called pt re: K+ of 5.8, told to recheck in 1 week"></textarea></div>
    <div class="form-row">
        <div class="form-group"><label>Follow-up Needed?</label><select id="m-cfu"><option value="0">No</option><option value="1">Yes</option></select></div>
        <div class="form-group"><label>Follow-up Date</label><input type="date" id="m-cfudate"></div>
    </div>
    `, `<button class="btn" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="saveContact(${pid})">Save</button>`);
}

async function saveContact(pid) {
    try {
        await api(`/patients/${pid}/contacts`, { method: "POST", body: {
            contact_date: $("#m-cdate").value,
            method: $("#m-cmethod").value,
            summary: $("#m-csummary").value.trim(),
            followup_needed: parseInt($("#m-cfu").value),
            followup_date: $("#m-cfudate").value || null,
        }});
        toast("Contact logged!", "success");
        closeModal();
        renderPatientChart();
    } catch (e) { toast(e.message, "error"); }
}

// ── Referral modal ──

function showAddReferralModal(pid) {
    showModal("Add Referral", `
    <div class="form-row">
        <div class="form-group"><label>Specialty *</label><input id="m-refspec" placeholder="e.g. Cardiology"></div>
        <div class="form-group"><label>Provider</label><input id="m-refprov" placeholder="e.g. Dr. Smith"></div>
    </div>
    <div class="form-group"><label>Reason</label><input id="m-refreason" placeholder="e.g. Chest pain workup"></div>
    <div class="form-group"><label>Date Sent</label><input type="date" id="m-refdate" value="${todayStr()}"></div>
    `, `<button class="btn" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="saveReferral(${pid})">Save</button>`);
}

async function saveReferral(pid) {
    try {
        await api(`/patients/${pid}/referrals`, { method: "POST", body: {
            specialty: $("#m-refspec").value.trim(),
            provider_name: $("#m-refprov").value.trim() || null,
            reason: $("#m-refreason").value.trim() || null,
            date_sent: $("#m-refdate").value,
        }});
        toast("Referral added!", "success");
        closeModal();
        renderPatientChart();
    } catch (e) { toast(e.message, "error"); }
}

async function markConsultReceived(rid) {
    await api(`/referrals/${rid}`, { method: "PUT", body: { consult_received: 1, consult_date: todayStr() } });
    toast("Consult marked received!", "success");
    renderPatientChart();
}

// ── Tag modal ──

function showAddTagModal(pid) {
    showModal("Add Tag", `
    <div class="form-group"><label>Tag Name</label><input id="m-tagname" placeholder='e.g. "pregnant", "palliative", "snowbird"'></div>
    <div class="form-group"><label>Color</label><input type="color" id="m-tagcolor" value="#6b7280"></div>
    `, `<button class="btn" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="saveTag(${pid})">Save</button>`);
}

async function saveTag(pid) {
    try {
        await api(`/patients/${pid}/tags`, { method: "POST", body: {
            name: $("#m-tagname").value.trim(),
            color: $("#m-tagcolor").value,
        }});
        toast("Tag added!", "success");
        closeModal();
        renderPatientChart();
    } catch (e) { toast(e.message, "error"); }
}

async function removePatientTag(pid, tid) {
    await api(`/patients/${pid}/tags/${tid}`, { method: "DELETE" });
    renderPatientChart();
}

// ── Family modal ──

async function showAddFamilyModal(pid) {
    const data = await api("/patients?per_page=2500");
    const patients = data.patients.filter(p => p.id !== pid);
    showModal("Link Family Member", `
    <div class="form-group">
        <label>Select Patient</label>
        <select id="m-fampatient">
            ${patients.map(p => `<option value="${p.id}">${esc(p.last_name)}, ${esc(p.first_name)} (${computeAge(p.dob)}y ${p.sex})</option>`).join('')}
        </select>
    </div>
    <div class="form-group">
        <label>Relationship (to this patient)</label>
        <select id="m-famrel">
            <option value="spouse">Spouse</option>
            <option value="parent">Parent</option>
            <option value="child">Child</option>
            <option value="sibling">Sibling</option>
        </select>
    </div>
    `, `<button class="btn" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="saveFamily(${pid})">Link</button>`);
}

async function saveFamily(pid) {
    try {
        await api(`/patients/${pid}/family`, { method: "POST", body: {
            related_patient_id: parseInt($("#m-fampatient").value),
            relationship: $("#m-famrel").value,
        }});
        toast("Family member linked!", "success");
        closeModal();
        renderPatientChart();
    } catch (e) { toast(e.message, "error"); }
}

async function removeFamily(pid, rid) {
    if (!confirm("Unlink this family member?")) return;
    await api(`/patients/${pid}/family/${rid}`, { method: "DELETE" });
    renderPatientChart();
}

// ── Preventive care actions ────────────────────────────────────────────────

async function markPreventiveDone(pcid) {
    await api(`/preventive/${pcid}`, { method: "PUT", body: { status: "completed", last_done_date: todayStr() } });
    toast("Marked as done!", "success");
    renderPatientChart();
}

async function declinePreventive(pcid) {
    const notes = prompt("Reason for declining (optional):");
    await api(`/preventive/${pcid}`, { method: "PUT", body: { status: "declined", notes: notes || null } });
    toast("Marked as declined.", "success");
    renderPatientChart();
}


// ── Visit prep ─────────────────────────────────────────────────────────────

async function showVisitPrep(pid) {
    const data = await api(`/patients/${pid}/visit-prep`);
    const p = await api(`/patients/${pid}`);
    showModal(`Visit Prep — ${p.first_name} ${p.last_name}`, `
    <div style="max-height:60vh;overflow-y:auto;">
        <h4 style="margin-bottom:8px;">Active Problems</h4>
        <ul>${data.active_problems.map(pr => `<li>${esc(pr.description)}</li>`).join('') || '<li class="text-muted">None</li>'}</ul>

        <h4 style="margin:12px 0 8px;">Overdue Screenings</h4>
        <ul>${data.overdue_preventive.map(pc => `<li class="text-danger">${esc(pc.rule_name)} (${pc.category})</li>`).join('') || '<li class="text-muted">Up to date</li>'}</ul>

        <h4 style="margin:12px 0 8px;">Pending Labs</h4>
        <ul>${data.pending_labs.map(l => `<li>${esc(l.test_name)} — ${l.status} (${formatDate(l.ordered_date)})</li>`).join('') || '<li class="text-muted">None</li>'}</ul>

        <h4 style="margin:12px 0 8px;">Pending Referrals</h4>
        <ul>${data.pending_referrals.map(r => `<li>${esc(r.specialty)} — sent ${formatDate(r.date_sent)}</li>`).join('') || '<li class="text-muted">None</li>'}</ul>

        <h4 style="margin:12px 0 8px;">Meds Running Out (30 days)</h4>
        <ul>${data.meds_running_out.map(m => `<li>${esc(m.name)} — runs out ${formatDate(m.run_out_date)}</li>`).join('') || '<li class="text-muted">None</li>'}</ul>

        <h4 style="margin:12px 0 8px;">Open Reminders</h4>
        <ul>${data.open_reminders.map(r => `<li>${esc(r.title)} — due ${formatDate(r.due_date)}</li>`).join('') || '<li class="text-muted">None</li>'}</ul>
    </div>
    `, `<button class="btn" onclick="closeModal()">Close</button><button class="btn btn-primary" onclick="closeModal();navigate('patient',${pid})">Open Chart</button>`);
}


// ── Reminder popup system ──────────────────────────────────────────────────

async function checkReminders() {
    try {
        const d = await api("/dashboard");
        const overdue = d.reminders.filter(r => r.due_date <= todayStr());
        const meds = d.meds_due.filter(m => m.run_out_date <= todayStr());

        if (overdue.length + meds.length > 0 && Notification.permission === "granted") {
            const count = overdue.length + meds.length;
            new Notification("PanelTracker", {
                body: `${count} item(s) need attention: ${overdue.length} overdue reminders, ${meds.length} meds out of stock`,
                icon: "/static/css/style.css", // placeholder
            });
        }

        // Show in-app popup for most urgent
        const popup = document.querySelector(".reminder-popup");
        if (popup) popup.remove();

        if (overdue.length > 0) {
            const r = overdue[0];
            const div = document.createElement("div");
            div.className = "reminder-popup";
            div.innerHTML = `
            <h4>${esc(r.title)}</h4>
            <p>${esc(r.first_name)} ${esc(r.last_name)} — ${r.reason ? esc(r.reason) : 'Due ' + formatDate(r.due_date)}</p>
            <div class="btn-group mt-2">
                <button class="btn btn-sm btn-primary" onclick="navigate('patient',${r.patient_id});this.closest('.reminder-popup').remove()">Open Chart</button>
                <button class="btn btn-sm btn-success" onclick="completeReminder(${r.id});this.closest('.reminder-popup').remove()">Done</button>
                <button class="btn btn-sm" onclick="this.closest('.reminder-popup').remove()">Dismiss</button>
            </div>`;
            document.body.appendChild(div);
        }
    } catch (e) { /* silent */ }
}


// ── Utility functions ──────────────────────────────────────────────────────

function esc(str) {
    if (!str) return "";
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

function escAttr(str) {
    return (str || "").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

function todayStr() {
    return new Date().toISOString().slice(0, 10);
}

function futureDate(days) {
    const d = new Date();
    d.setDate(d.getDate() + days);
    return d.toISOString().slice(0, 10);
}

function formatDate(str) {
    if (!str) return "—";
    try {
        const d = new Date(str + (str.length === 10 ? "T00:00:00" : ""));
        return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
    } catch { return str; }
}

function formatDateTime(str) {
    if (!str) return "—";
    try {
        const d = new Date(str);
        return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric", hour: "numeric", minute: "2-digit" });
    } catch { return str; }
}

function computeAge(dob) {
    const d = new Date(dob + "T00:00:00");
    const today = new Date();
    let age = today.getFullYear() - d.getFullYear();
    if (today.getMonth() < d.getMonth() || (today.getMonth() === d.getMonth() && today.getDate() < d.getDate())) age--;
    return age;
}


// ── Init ───────────────────────────────────────────────────────────────────

// Request notification permission
if ("Notification" in window && Notification.permission === "default") {
    Notification.requestPermission();
}

// Start
renderDashboard();

// Check reminders every 5 minutes
reminderCheckInterval = setInterval(checkReminders, 5 * 60 * 1000);
// Initial check after 10 seconds
setTimeout(checkReminders, 10000);
