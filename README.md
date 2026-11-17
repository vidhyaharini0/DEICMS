# DEICMS - Digital Evidence Integrity & Chain-of-Custody Management System

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-000000?style=for-the-badge&logo=flask)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite)
![Tests](https://img.shields.io/badge/Tests-216%20passing-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

A web application for managing digital forensic evidence and its **chain of
custody** from intake to export, built so that tampering with an exhibit is
either impossible or evident, every action is attributable to a person, and
the system's own history cannot be rewritten.

> **Version 2.0.** This release adds the full Software Engineering treatment -
> a Scrum process with six sprints, requirements at two levels, 26 UML
> diagrams, and a 96-page engineering report. Version 1.0, the original System
> Security submission, remains available under the
> [v1.0 tag](../../releases/tag/v1.0).

---

## Why this system exists

Digital evidence can be altered without leaving a visible trace. What makes it
admissible in court is not the evidence itself but the record of its
handling - who held it, when, and what was done to it. Break that chain and
the evidence is worthless, however genuine it is.

DEICMS enforces five guarantees:

| | Guarantee |
|---|---|
| **G1** | Content can be shown unchanged since intake, or shown precisely where it changed |
| **G2** | A person sees only the investigations they are assigned to, in every view |
| **G3** | The record of what happened is complete and cannot be amended |
| **G4** | An exhibit moves only as its procedure permits |
| **G5** | Exhibits can be ranked by the attention they need, with the reasoning exposed |

---

## Feature categorization

The project is deliberately balanced across three categories. Chapter 2 of the
report assesses that balance on four independent measures.

### A - Data and repository functionalities (30)

Full CRUD over six entities - Case, EvidenceItem, Investigator, CustodyLog,
AuditRecord and CaseAccess - plus scoped aggregates, paginated listings, and
three formula-based audit checks: custody time gaps against a configurable
threshold, duplicate log entries, and role-permission mismatches.

### B - Third-party services (11)

Content hashing, Ed25519 signatures, EXIF extraction, magic-byte content-type
validation, SQLAlchemy, a hosted language model, scikit-learn's Isolation
Forest, ReportLab, AES-256-GCM encryption, TOTP second factor, and rate
limiting. Each is consumed as-is; the report states what each provides and
what the project supplies around it.

### C - Complex application logic (5)

Designed and implemented within the project. Each has its own section in the
report with pseudocode, complexity analysis, and at least two UML behavioral
diagrams.

| Algorithm | What makes it complex |
|---|---|
| **Chain integrity verification** <br>`app/logic/graph_integrity.py` | Builds a DAG of custody events and walks it depth-first, applying three independent checks at every node and **accumulating all failures in one pass** rather than halting at the first |
| **Multi-factor risk assessment** <br>`app/logic/risk_scoring.py` | Eight indicators, each normalized by a curve suited to its own distribution, combined by weighted sum, amplified by five interaction rules, with the total amplification **capped at 0.30** |
| **Custody chain reconstruction** <br>`app/logic/chain_reconstruction.py` | Heuristic best-first search over candidate records scored on four plausibility criteria, which **declines to infer** below a 0.40 threshold rather than guessing |
| **Evidence lifecycle state machine** <br>`app/logic/state_machine.py` | Six states and fourteen transitions declared **as data**, each gated by permitted role and preconditions, with a four-gate validation pipeline and audited refusals |
| **Assistant orchestration** <br>`app/logic/ai_assistant.py` | Six stages around a language model: intent classification, **access scoping**, retrieval, prompt construction, budgeted invocation with fallback, and reference validation |

Anomaly detection with an Isolation Forest feeds the same dashboard as the
risk scorer but is classified **B, not C** - the library implements the
detection and the project supplies only the feature vector.

---

## Security design

**Digital signatures.** Each investigator is issued an Ed25519 key pair at
account creation. Every custody event is signed over a canonical payload -
six fields with deterministic ordering - so the bytes signed at creation are
identical to those reconstructed at verification.

**Encryption at rest.** Evidence content is encrypted with AES-256-GCM
(authenticated, so tampering is detected on decryption). Private keys are
wrapped with Fernet under a key derived via PBKDF2-HMAC-SHA256, so a stolen
database alone yields unusable keys.

**Append-only audit trail.** ORM event listeners raise on any update or delete
of an audit record, so the guarantee binds code that has not been written yet.

**Access control on two axes.** Four roles - Administrator, Lead Investigator,
Analyst, Read-Only Viewer - combined with case-level membership. Every
aggregate routes through a single function that answers "which investigations
may this account see".

**Web hardening.** CSRF protection, rate limiting, `HttpOnly` + `Secure` +
`SameSite` cookies, content-security and framing directives, account lockout,
idle-session timeout, magic-byte upload validation, and TLS in development via
a self-signed certificate.

---

## Engineering process

Developed with **Scrum** across six sprints. Three delivered the planned
system; three arose from defects found after acceptance, each by a different
means.

| Sprint | Focus | Points | Origin |
|---|---|---|---|
| 1 | Foundation - cases, evidence, custody, audit | 40 | Planned |
| 2 | Integrity - verification, lifecycle, reconstruction | 38 | Planned |
| 3 | Assessment - risk, assistant, reporting | 42 | Planned |
| 4 | Access scoping | 10 | Found by **adversarial testing** |
| 5 | Defect repair | 11 findings | Found by **structured code reading** |
| 6 | Quality enforcement | 23 | Found by **audit against the specification** |

**Artifacts:** a product backlog of 36 stories across six documented
refinements, sprint backlogs decomposed into tasks with hour estimates,
burndown charts, reviews against acceptance criteria, and retrospectives whose
actions are traced to where they took effect.

**Requirements:** 22 user requirements, 61 system functional requirements,
9 user quality requirements, 21 system quality requirements, 7 domain
requirements. Every system requirement traces to a user requirement, a user
story, a sprint, and a verifying test. No requirement names a technology - the
mechanisms belong to the design chapter.

**Verification:** 216 tests, 78% statement coverage overall and 80% across the
five algorithms. Every one of the 21 system quality requirements carries a
measurement method, an acceptance value, and a named automated test.

---

## UML model

**26 diagrams in 13 of UML's 14 types**, generated from PlantUML source so a
diagram cannot drift from its description.

| Category | Diagrams |
|---|---|
| **Structural** | Class (domain, persistent, traceability), Object, Package, Component, Composite structure, Deployment, Profile |
| **Behavioral** | Use case (4), Activity (6), State machine (2), Sequence (3), Communication, Timing |

The relational schema is modelled as a **class diagram with `«table»`
stereotypes** rather than as an ER diagram, so one notation describes the
whole system. See [`diagrams/INDEX.md`](diagrams/INDEX.md).

---

## Quick start

**Prerequisites:** Python 3.10+, and `libmagic` on Linux/macOS
(`sudo apt install libmagic1` or `brew install libmagic`; bundled on Windows).

```bash
git clone https://github.com/vidhyaharini0/DEICMS.git
cd DEICMS

python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS / Linux

pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
SECRET_KEY=replace-with-a-long-random-string
KEY_ENCRYPTION_SECRET=replace-with-another-long-random-string
NVIDIA_API_KEY=your-key-if-using-the-assistant
```

Without a model key the assistant falls back to a context-only answer and says
so. Development defaults are used if the secrets are absent; production
**refuses to start** with absent or known-weak secrets.

```bash
python seed.py      # demo investigators, cases and evidence
python run.py       # https://localhost:5001
```

A self-signed certificate is generated on first launch, so expect a one-time
browser warning.

---

## Testing

```bash
pytest tests/ -v --cov=app
```

| Suite | Tests | Covers |
|---|---|---|
| `test_increment1.py` | 10 | Authentication, authorization, registration, audit |
| `test_increment2.py` | 17 | Signing, integrity verification, lifecycle, reconstruction |
| `test_increment3.py` | 93 | Risk scoring, assistant, second factor, encryption, export |
| `test_scoping.py` | 14 | Adversarial authorization across every aggregate |
| `test_nfr.py` | 44 | All 21 system quality requirements |
| `test_integration.py` | 16 | End-to-end flows |
| `test_intent_classifier.py` | 10 | Seven intents, UNKNOWN, tie-breaking |
| `test_day2.py` | 12 | Early foundation behavior |

The suite requires **no network access**, which is what makes the language
model pipeline testable at all.

---

## Project structure

```
DEICMS/
├── app/
│   ├── __init__.py          Application factory, extensions, security hooks
│   ├── models/              Six SQLAlchemy entities
│   ├── logic/               Algorithms and services
│   ├── routes/              Ten Flask blueprints, 41 routes
│   ├── templates/
│   └── static/
├── tests/                   Eight pytest suites, 216 tests
├── diagrams/                26 PlantUML sources, rendered PNGs, burndown charts
├── docs/
│   ├── DEICMS_Project_Report.pdf      The 96-page engineering report
│   ├── DEICMS_Project_Report.docx
│   ├── SE_Project_Proposal.docx
│   ├── DEICMS_Security_Concepts.docx  From the v1.0 System Security work
│   ├── RESET_DATABASE.md
│   └── report-source/       Chapter markdown the report is built from
├── screenshots/             Figures used in the report
├── demo_files/              Sample evidence for demonstrations
├── tools/
│   ├── build_report.py      Assembles the report from markdown
│   ├── make_demo_files.py
│   └── flush_db.py
├── config.py  run.py  seed.py  generate_cert.py
└── requirements.txt
```

Rebuild the report with `python tools/build_report.py` (needs `pandoc`, and
`plantuml.jar` if the diagrams are to be re-rendered).

---

## Known limitations

Stated plainly, and discussed in full in Chapter 13 of the report.

- **No customer.** Requirements were derived from domain sources rather than
  from a stakeholder who could contest them. Verification is strong;
  validation is correspondingly weak.
- **Coverage gaps.** Chain reconstruction sits at 65%, the lowest in the
  project - its plausibility function has four criteria each present or
  absent, giving sixteen combinations.
- **Untested areas.** No concurrency, load, penetration or browser testing.
  Live model behavior is never exercised, only the pipeline around it.
- **Deployment.** Development server, single process, SQLite, self-signed
  certificate. There is no key-rotation procedure.
- **Hallucination detection verifies references, not reasoning.** A reply
  citing only real identifiers while drawing a wrong conclusion passes.

---

## Disclaimer

An academic project, built to explore and demonstrate software engineering and
security concepts. It implements real cryptographic primitives but has not
been audited or hardened for production. **Do not use it to handle real,
sensitive, or legally significant evidence.**

---

## Acknowledgements

Developed at the **University of Messina**, Department of Mathematics,
Computer Sciences, Physical Sciences and Earth Sciences (MIFT), Bachelor's
Degree in Data Analysis.

Version 1.0 was submitted for the System Security course; version 2.0 for the
Software Engineering course.

**Author:** Vidhya Harini Vijayarajan Sangeetha

## License

MIT - see [LICENSE](LICENSE).
