# DEICMS — Product Backlog

**Project:** Digital Evidence Integrity & Chain-of-Custody Management System
**Process:** Agile Incremental Model — 3 increments × 3 weeks (14 working-day sprints, day 0–14)
**Estimation:** Planning-poker story points, Fibonacci scale (1, 2, 3, 5, 8, 13)
**Prioritisation:** MoSCoW (Must / Should / Could / Won't-this-time)
**Total scope:** 27 user stories · 120 story points

Feature categories follow the course requirement and the accepted proposal:

| Tag | Category |
|---|---|
| **A** | Data / repository / DB-oriented (CRUD, formulae) |
| **B** | Third-party services (libraries, APIs, pre-trained models) |
| **C** | Complex application logic (custom algorithms) |
| **SEC** | Cross-cutting security hardening |

## Personas

- **Amelia (Admin):** manages accounts, roles, system settings, and oversees every case.
- **Luca (Lead Investigator):** owns cases, uploads and transfers evidence, exports court packages.
- **Nadia (Analyst):** analyses evidence assigned to her cases, runs integrity checks, queries the AI assistant.
- **Riya (Read-Only auditor):** reviews custody chains and audit trails without modifying anything.

---

## Backlog overview

| ID | User story (summary) | Cat. | MoSCoW | Pts | Increment |
|---|---|---|---|---|---|
| US-01 | Log in / log out securely | A/SEC | Must | 3 | 1 |
| US-02 | Role-based access control | A | Must | 5 | 1 |
| US-03 | Case CRUD, search & archive | A | Must | 5 | 1 |
| US-04 | Upload & register evidence files | A | Must | 5 | 1 |
| US-05 | SHA-256 fingerprint at upload | B | Must | 2 | 1 |
| US-06 | EXIF / MIME metadata extraction | B | Must | 3 | 1 |
| US-07 | Edit & categorise evidence | A | Must | 3 | 1 |
| US-08 | Record custody transfers & access events | A | Must | 5 | 1 |
| US-09 | Append-only audit trail | A | Must | 5 | 1 |
| US-10 | Formula-based audit checks | A | Should | 3 | 1 |
| US-11 | Admin-only account creation | A | Must | 1 | 1 |
| US-12 | Ed25519-signed custody events | B | Must | 5 | 2 |
| US-13 | Graph integrity verification algorithm | C | Must | 13 | 2 |
| US-14 | Evidence lifecycle state machine | C | Must | 8 | 2 |
| US-15 | Custody chain reconstruction algorithm | C | Must | 8 | 2 |
| US-16 | Integrity verification report UI | A | Should | 2 | 2 |
| US-17 | Chain reconstruction report UI | A | Should | 2 | 2 |
| US-18 | Multi-factor risk scoring algorithm | C | Must | 8 | 3 |
| US-19 | Admin-configurable risk weights | C/A | Should | 3 | 3 |
| US-20 | AI assistant orchestration pipeline | C | Must | 8 | 3 |
| US-21 | Hallucination detection | C | Must | 3 | 3 |
| US-22 | Isolation Forest anomaly detection | B | Could | 5 | 3 |
| US-23 | Risk & anomaly dashboards | A | Should | 3 | 3 |
| US-24 | 2FA, lockout & session timeout | SEC/B | Should | 5 | 3 |
| US-25 | Encryption at rest & magic-byte checks | SEC/B | Should | 3 | 3 |
| US-26 | Tamper-evident signed ZIP export | B | Should | 2 | 3 |
| US-27 | PDF chain-of-custody report | B | Could | 2 | 3 |
| US-28 | Role-scoped dashboard & aggregated views | A/SEC | Must | 5 | M1 |
| US-29 | Access-scoped AI assistant & chat isolation | C/SEC | Must | 5 | M1 |

**Increment totals:** Increment 1 = 40 pts · Increment 2 = 38 pts · Increment 3 = 42 pts · Maintenance M1 = 10 pts

**Maintenance iteration M1** (post-acceptance change requests raised during review testing) is described at the end of this document.

---

## User stories with acceptance criteria

### Increment 1 — Core Case & Evidence Management

**US-01 — Secure login/logout (3 pts, Must, A/SEC)**
*As an investigator, I want to log in with my credentials and be logged out when idle, so that only authorised people access evidence data.*
Acceptance criteria:
- Valid credentials open an authenticated session; invalid ones are rejected with no user enumeration.
- Passwords are stored only as salted hashes.
- Sessions expire after 30 minutes of inactivity (sliding timeout).
- Every login, logout, and failed attempt is written to the audit trail.

**US-02 — Role-based access control (5 pts, Must, A)**
*As an admin, I want each account to hold exactly one role (Admin, Lead Investigator, Analyst, Read-Only), so that permissions match responsibilities.*
Acceptance criteria:
- Every route enforces the minimum role; unauthorised access redirects with an explanatory message.
- Read-Only users cannot trigger any state-changing action.
- Role changes are admin-only and audited.

**US-03 — Case CRUD, search & archive (5 pts, Must, A)**
*As a lead investigator, I want to create, search, update, and archive cases, so that investigations are tracked from opening to closure.*
Acceptance criteria:
- A case has a unique case number, title, jurisdiction, status (Open/Active/Pending/Closed), and timestamps.
- Cases can be filtered by status and searched by title/number.
- Archiving is a soft operation — no case data is ever physically deleted.
- Case membership (case-level access) controls who sees the case.

**US-04 — Upload & register evidence (5 pts, Must, A)**
*As an investigator, I want to upload a digital file and register it as an evidence item in a case, so that it enters a managed chain of custody.*
Acceptance criteria:
- Upload accepts the allow-listed extensions and rejects everything else.
- A unique evidence number is generated; uploader becomes the first custody holder.
- An Upload custody-log entry is created atomically with the evidence record.

**US-05 — SHA-256 fingerprint (2 pts, Must, B — `hashlib`)**
*As an investigator, I want every uploaded file fingerprinted with SHA-256, so that any later modification is detectable.*
Acceptance criteria:
- `original_hash` is computed at upload and never changes; `current_hash` tracks the latest verified state.
- The hash is shown on the evidence page and stored in the custody log entry.

**US-06 — Metadata extraction (3 pts, Must, B — Pillow / python-magic)**
*As an analyst, I want EXIF and MIME metadata extracted automatically, so that provenance details are preserved without manual entry.*
Acceptance criteria:
- Images yield EXIF fields (camera, timestamps, GPS if present) stored as JSON.
- The declared extension is validated against magic bytes (full enforcement in US-25).

**US-07 — Edit & categorise evidence (3 pts, Must, A)**
*As an investigator, I want to edit evidence metadata and assign a category, so that items stay accurate and findable.*
Acceptance criteria:
- Title, description, and category (Image/Video/Audio/Document/Database/Log File/Other) are editable by authorised roles.
- Edits are audited; the file itself and its hashes are immutable through this path.

**US-08 — Custody transfers & access events (5 pts, Must, A)**
*As an investigator, I want every hand-over and access recorded (who, when, where, why), so that the chain of custody is complete.*
Acceptance criteria:
- A transfer records from/to investigator, timestamp, location, and reason.
- Only the current holder (or an Admin) can transfer an item.
- The custody log is viewable per evidence item, oldest first.

**US-09 — Append-only audit trail (5 pts, Must, A)**
*As an auditor, I want every significant system event logged immutably, so that activity can be reviewed after the fact.*
Acceptance criteria:
- Logins, failed attempts, CRUD operations, file access, state changes, and integrity results are recorded with actor, IP, timestamp, and outcome.
- Updates/deletes on audit records are blocked at the ORM layer.
- Trails are filterable per evidence item and per investigator.

**US-10 — Formula-based audit checks (3 pts, Should, A — formulae)**
*As an auditor, I want automatic checks for custody time gaps, duplicate entries, and role mismatches, so that obvious irregularities surface without manual review.*
Acceptance criteria:
- Gaps between consecutive transfers above a configurable threshold (default 72 h) are flagged.
- Duplicate log entries (same investigator, evidence, timestamp) are detected by query.
- Role-permission mismatches are detected by a single lookup and logged as warnings.

**US-11 — Admin-only account creation (1 pt, Must, A)**
*As an admin, I want to be the only one who can create investigator accounts, so that no one self-registers into an evidence system.*
Acceptance criteria:
- No public registration route exists; `/admin/users/new` requires the Admin role.
- New accounts get a role, a strong password (policy-checked), and an Ed25519 key pair.

### Increment 2 — Integrity Algorithms & State Machine

**US-12 — Ed25519-signed custody events (5 pts, Must, B — `cryptography`)**
*As a lead investigator, I want each custody event digitally signed by the outgoing holder, so that records cannot be forged or repudiated.*
Acceptance criteria:
- A canonical JSON payload (evidence, event type, timestamp, parties, file hash) is signed at every Upload and Transfer.
- Signatures verify against the signer's stored public key.
- The signature column is NOT NULL — unsigned custody records cannot exist.

**US-13 — Graph integrity verification (13 pts, Must, C)**
*As an analyst, I want the entire custody history verified — not just the latest record — so that tampering anywhere in the chain is detected.*
Acceptance criteria:
- Custody events are built into a DAG and traversed by DFS from the upload root.
- Each node passes three checks: hash re-computation, signature verification, strict timestamp ordering.
- All failures are collected in a single pass with node ID, type, and reason.
- Output: verdict (Intact / Partially Verified / Broken), completeness score (verified/total %), failure list, verified timeline.

**US-14 — Lifecycle state machine (8 pts, Must, C)**
*As a lead investigator, I want evidence to move only through legally meaningful states, so that procedural rules are enforced by the system.*
Acceptance criteria:
- States: Collected → Submitted → Under Analysis ↔ Transferred → Archived; any state → Flagged.
- Each transition has a minimum role and preconditions (e.g. custody log must exist before analysis).
- Rejected transitions return the exact unmet condition and are audited.
- Every successful transition requires a justification and triggers a risk-score recalculation.

**US-15 — Custody chain reconstruction (8 pts, Must, C)**
*As an analyst, I want plausible reconstruction of gapped custody chains, so that partial records still support the investigation honestly.*
Acceptance criteria:
- Gaps are detected where the expected holder does not match the next record.
- Candidates are generated from access logs within the gap window and scored on temporal proximity, role consistency, location consistency, and behavioural consistency.
- Greedy best-first selection fills each gap only above a plausibility threshold; otherwise the gap is Unresolved.
- Every link is labelled Confirmed / Inferred / Unresolved; an overall confidence score is reported. Inferred records are never presented as confirmed.

**US-16 — Integrity report UI (2 pts, Should, A)**
*As an analyst, I want a readable verification report page, so that I can interpret the algorithm's output quickly.*
Acceptance criteria: verdict banner, completeness percentage, failure table with positions, verified timeline; JSON endpoint for programmatic access.

**US-17 — Reconstruction report UI (2 pts, Should, A)**
*As an analyst, I want the reconstructed timeline displayed with confidence labels, so that certain and estimated links are visually distinct.*
Acceptance criteria: full timeline with Confirmed/Inferred/Unresolved badges, per-link reasoning, overall confidence score.

### Increment 3 — Risk Scoring, AI Assistant & Hardening

**US-18 — Multi-factor risk scoring (8 pts, Must, C)**
*As a lead investigator, I want each item scored across multiple interacting risk signals, so that I can prioritise attention without reading every log.*
Acceptance criteria:
- Eight factors covering proposal signals S1–S6 plus file-type and duplicate-entry risk, each normalised with a curve fitting its distribution (linear / logarithmic / sigmoid).
- Weighted sum plus interaction rules that amplify dangerous factor combinations.
- Output: base score, interaction bonus, final score in [0,1], LOW/MEDIUM/HIGH/CRITICAL level, per-factor explanations, generated recommendations.
- Items ranked highest-risk first on the dashboard.

**US-19 — Configurable weights & thresholds (3 pts, Should, C/A)**
*As an admin, I want to tune factor weights and classification thresholds, so that scoring reflects our unit's priorities.*
Acceptance criteria: admin-only settings page; weights re-normalised to sum to 1.0; thresholds strictly increasing; persisted across restarts; changes audited.

**US-20 — AI assistant orchestration (8 pts, Must, C)**
*As an investigator, I want to ask questions in plain English and get database-grounded answers, so that I can query case state without learning the UI's every corner.*
Acceptance criteria:
- Six-stage pipeline: intent classification (keyword frequency), intent-driven context retrieval, template prompt construction, LLM call (NVIDIA NIM / Llama 3.1), response validation, hallucination check (US-21).
- The system degrades gracefully to a context-aware mock when no API key is configured.
- Conversation history (last turns) is maintained per session.

**US-21 — Hallucination detection (3 pts, Must, C)**
*As an investigator, I want the system to flag answers that reference entities not in the database, so that I never act on invented information.*
Acceptance criteria: every case number, evidence ID, and investigator name in the reply is cross-checked against the retrieved context; unknown references produce visible warnings in the chat UI and the JSON API.

**US-22 — Anomaly detection (5 pts, Could, B — scikit-learn)**
*As a lead investigator, I want statistical outliers in custody activity flagged, so that unusual behaviour is suggested for review.*
Acceptance criteria: 6-dimensional feature vectors per item; Isolation Forest flags outliers; results labelled "suggested for review", shown alongside deterministic risk scores.

**US-23 — Risk & anomaly dashboards (3 pts, Should, A)**
*As a lead investigator, I want dashboards ranking items by risk and anomaly status, so that the highest-priority evidence is one click away.*
Acceptance criteria: risk-ranked table with level badges; anomaly dashboard with feature breakdown; per-evidence risk detail page with factor chart.

**US-24 — 2FA, lockout & timeout (5 pts, Should, SEC/B — PyOTP)**
*As an admin, I want optional TOTP 2FA, automatic lockout after failed logins, and idle timeouts, so that stolen passwords alone don't grant access.*
Acceptance criteria: QR-code TOTP enrolment; login requires the code when enabled; 5 failures lock the account 15 minutes; admin can unlock; rate limiting on the login route.

**US-25 — Encryption at rest & magic bytes (3 pts, Should, SEC/B)**
*As an admin, I want stored evidence encrypted and uploads content-validated, so that a stolen disk or a renamed executable causes no harm.*
Acceptance criteria: AES-256-GCM encryption of stored files (hashes computed on plaintext); magic-byte validation rejects files whose content contradicts their extension; executables rejected outright; private keys encrypted at rest.

**US-26 — Signed ZIP case export (2 pts, Should, B)**
*As a lead investigator, I want a tamper-evident export package, so that a case can be handed to another party verifiably.*
Acceptance criteria: ZIP contains decrypted evidence, manifest.json with per-file SHA-256, full audit trail, and an Ed25519 signature of the manifest with verification instructions.

**US-27 — PDF custody report (2 pts, Could, B — ReportLab)**
*As a lead investigator, I want a printable chain-of-custody report per item, so that court submissions have a standard document.*
Acceptance criteria: PDF contains identification block, cryptographic integrity summary with a fresh graph-verification run, full custody table, and generation footer; downloadable from the evidence page.

---

## Maintenance iteration M1 — access-scoping change requests

During review testing after the three increments were accepted, two defects
were found where aggregated views leaked data across case boundaries. They
were handled as a short maintenance iteration with two change-request stories.

**CR-01 / US-28 — Role-scoped dashboard & aggregated views (5 pts, Must, A/SEC)**
*As a non-Admin investigator, I want the dashboard, risk dashboard, and anomaly views to show only the cases and evidence I have access to, so that I never see investigations outside my remit.*
Defect: the dashboard and the risk/anomaly pages queried every case, evidence item, and audit record system-wide, regardless of the logged-in role.
Acceptance criteria:
- A single `CaseAccess.accessible_case_ids(user)` helper returns None for Admin (all cases) or the user's case-ID list otherwise; every aggregated view filters through it.
- Dashboard panels are tailored per role (Admin sees system + security alerts; Lead sees pending actions; Analyst sees a workbench; Read-Only sees a review queue), and every role always has a non-empty "Your recent activity" panel.
- A Read-Only user with no shared cases sees an explanatory empty state, not global data or a blank page.
- Per-item risk and audit-formula endpoints enforce the same case-access check (HTTP 403 on cross-case access).

**CR-02 / US-29 — Access-scoped AI assistant & chat isolation (5 pts, Must, C/SEC)**
*As an investigator, I want the AI assistant to answer only about my accessible cases, to know who I am, and to never show me another user's conversation, so that the chatbot respects the same boundaries as the rest of the system.*
Defects: (a) the assistant's context retrieval queried all recent cases/evidence/transfers globally, so a Lead Investigator could list every case; (b) it could not answer "who am I" or "my cases"; (c) chat history persisted in the session across logout, so the next user on the same browser saw the previous user's conversation; (d) responses took 1-2 minutes.
Acceptance criteria:
- Context retrieval is scoped to `accessible_case_ids(user)`; cross-case IDs return an access-denied line instead of data.
- A new IDENTITY intent (checked with priority) answers "who am I" / "my cases" from the authenticated user and their accessible cases.
- Chat history is tagged with the owner's user ID and cleared on login and logout, so it can never leak between users.
- The LLM call has a request timeout and defaults to a faster model; the UI aborts and reports if a response is too slow.

---

## Won't-have (this release)

Deferred explicitly to keep scope honest: PostgreSQL deployment, e-mail notifications, full-text evidence content search, multi-language UI, mobile client, LLM fine-tuning.
