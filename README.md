# DEICMS — Digital Evidence Integrity & Chain-of-Custody Management System

**Software Engineering course project** — Bachelor's Degree in Data Analysis
Student: Vidhya Harini Vijayarajan Sangeetha (ID 533994)

DEICMS is a web application for managing digital forensic evidence with full
auditability, integrity verification, and role-based access control. It models
the real-world requirement that evidence is only admissible in court if its
**chain of custody** is unbroken and provable: who held it, when, and whether
it was altered.

The system was developed following the **Agile Incremental Model** in three
increments, as defined in the accepted project proposal
(`SE_Project_Proposal_DEICMS_v4.docx`).

---

## Feature categorisation (per project requirements)

### A. Data / repository / DB-oriented functionalities

- Full CRUD for the five core entities: **Case**, **Evidence Item**,
  **Investigator**, **Custody Log**, **Audit Record** (plus **Case Access**
  for case-level permissions), on a relational schema via SQLAlchemy.
- Search and filtering of cases by status, date, and assignee; soft-delete
  and archiving patterns.
- Simple audit formulas over database fields: custody time-gap detection
  (configurable 72-hour threshold), duplicate log-entry detection, and
  role-permission mismatch lookup.

### B. Third-party services / libraries

- **SHA-256 hashing** — Python `hashlib`; fingerprints every file at upload
  and at each integrity check.
- **Ed25519 digital signatures** — `cryptography`; every custody transfer is
  signed by the outgoing investigator.
- **File metadata extraction** — Pillow (EXIF) + `python-magic` (magic-byte
  MIME validation; executables rejected).
- **ORM / DB** — SQLAlchemy + SQLite (PostgreSQL-ready).
- **AI language model** — NVIDIA NIM API (Llama 3.1, OpenAI-compatible
  endpoint) for the investigation assistant.
- **Anomaly detection** — scikit-learn Isolation Forest over custody
  activity feature vectors.
- **PDF generation** — ReportLab, for court-style chain-of-custody reports.
- **2FA** — PyOTP (TOTP) + qrcode.

### C. Complex application logic (implemented from scratch)

1. **Chain-of-Custody Graph Integrity Verification** — builds a DAG of all
   custody events, DFS-traverses it with three checks per node (hash
   re-computation, Ed25519 signature verification, timestamp monotonicity),
   collects every failure in one pass, and computes a chain completeness
   score with an Intact / Partially Verified / Broken verdict.
2. **Multi-Factor Evidence Risk Scoring** — eight risk signals (covering
   S1–S6 from the proposal plus file-type and duplicate-entry factors), each
   normalised with a curve suited to its distribution (linear / logarithmic /
   sigmoid), combined via an admin-configurable weighted sum, amplified by
   factor-interaction rules, classified against admin-configurable
   thresholds, and explained with generated recommendations.
3. **Custody Chain Reconstruction** — heuristic best-first search that fills
   gaps in incomplete custody chains using multi-criteria plausibility
   scoring (temporal proximity, role consistency, location consistency,
   behavioural consistency) and labels every link Confirmed / Inferred /
   Unresolved with an overall confidence score.
4. **Evidence Lifecycle State Machine** — formal automaton over the states
   Collected → Submitted → Under Analysis ↔ Transferred → Archived (+ Flagged),
   with role-gated transitions, precondition validation, mandatory
   justification, audit logging of both successes and rejections, and
   automatic full risk-score recalculation on every transition.
5. **AI Investigation Assistant orchestration** — six-stage custom pipeline:
   keyword-frequency intent classification, intent-driven multi-table context
   retrieval, template-based prompt construction, LLM call, response
   validation (length / refusal / off-topic), and **hallucination detection**
   that cross-checks every case number, evidence ID, and investigator name
   in the answer against the retrieved database context.

Security hardening implemented alongside: CSRF protection, login rate
limiting and account lockout, TOTP 2FA, case-level access control, magic-byte
upload validation, AES-256-GCM evidence encryption at rest, encrypted private
keys, HTTPS (self-signed dev certificate), append-only audit trail, idle
session timeout, and tamper-evident signed ZIP case export.

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python 3 + Flask (application factory, blueprints) |
| Database | SQLite (dev) / PostgreSQL-ready via SQLAlchemy |
| Auth | Flask-Login, Flask-WTF (CSRF), Flask-Limiter, PyOTP |
| Crypto | hashlib (SHA-256), cryptography (Ed25519, AES-256-GCM, X.509) |
| Metadata | Pillow (EXIF), python-magic (MIME) |
| ML / AI | scikit-learn (Isolation Forest), NVIDIA NIM (Llama 3.1) |
| Reporting | ReportLab (PDF) |
| Frontend | HTML5 + Bootstrap 5 (Jinja2 templates) |
| Testing | pytest + pytest-cov |

---

## Getting started

```bash
python -m venv venv
venv\Scripts\activate          # Windows (source venv/bin/activate on Linux/macOS)
pip install -r requirements.txt

# Create a .env file in the project root:
#   SECRET_KEY=<long random string>
#   NVIDIA_API_KEY=nvapi-...   (optional - assistant falls back to a mock)

python seed.py                 # optional demo data
python run.py                  # serves https://localhost:5001
```

The first run generates a self-signed TLS certificate and creates the SQLite
database automatically.

## Testing

```bash
python -m pytest tests/ -v --cov=app
```

The suite covers all three increments: models and CRUD (Increment 1), state
machine / graph integrity / chain reconstruction (Increment 2), and risk
scoring / anomaly detection / AI assistant / routes (Increment 3).

## Project structure

```
deicms/
├── app/
│   ├── __init__.py          # application factory
│   ├── models/              # SQLAlchemy models (6 entities)
│   ├── logic/               # algorithms & services (category B + C)
│   ├── routes/              # Flask blueprints
│   └── templates/           # Jinja2 UI
├── diagrams/                # UML artefacts per increment (SVG)
├── tests/                   # pytest suite per increment
├── config.py, run.py, seed.py, generate_cert.py
└── SE_Project_Proposal_DEICMS_v4.docx
```

## UML artefacts

The `diagrams/` folder contains the artefacts referenced by the project
report: use case, class, and ER diagrams (Increment 1); sequence, activity,
and state diagrams for the complex algorithms (Increment 2); risk-scoring
activity, AI-orchestration sequence, component, and deployment diagrams plus
the burndown chart (Increment 3).

---

> **Academic project.** Built to demonstrate software engineering practice;
> not hardened for production deployment.
