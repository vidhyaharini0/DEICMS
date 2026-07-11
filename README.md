# DEICMS - Digital Evidence & Investigation Chain Management System

A secure, web-based platform for managing digital forensic evidence and its **chain of custody** from intake to export. DEICMS was built as a **System Security** project to demonstrate applied cryptography, secure web-application engineering, and non-trivial application logic (custody-graph verification, risk scoring, and anomaly detection) in a realistic investigation workflow.

Every action that touches evidence - uploading, viewing, transferring, changing state - is authenticated, authorised, cryptographically signed where appropriate, and written to a tamper-evident audit trail.

> **Academic project.** DEICMS was written to explore and demonstrate security concepts. It is not hardened for real-world deployment (see [Security notes & disclaimer](#security-notes--disclaimer)).

---

## Table of contents

- [Overview](#overview)
- [Key features](#key-features)
- [Tech stack](#tech-stack)
- [Architecture](#architecture)
- [Complex application logic](#complex-application-logic)
- [Security design](#security-design)
- [Getting started](#getting-started)
- [Usage](#usage)
- [Testing](#testing)
- [Project structure](#project-structure)
- [Screenshots](#screenshots)
- [Security notes & disclaimer](#security-notes--disclaimer)

---

## Overview

In a real investigation, evidence is only admissible if its **chain of custody** is unbroken and provable - who held it, when, and whether it was altered. DEICMS models this digitally:

- Investigators log in (with optional multi-factor authentication) and are scoped to the cases they're assigned to.
- Evidence files are uploaded, hashed, validated, and encrypted at rest.
- Every custody transfer is **digitally signed** by the outgoing investigator, binding the transfer to the file's hash at that moment.
- A suite of algorithms continuously assesses integrity, reconstructs incomplete custody chains, scores each item's risk, and flags statistical outliers.
- An **append-only audit trail** records every significant event and cannot be edited or deleted.

The result is a system where tampering is either prevented or made evident.

---

## Key features

**Access control & authentication**

- Role-based access: `Admin`, `Lead Investigator`, `Analyst`, `Read-Only`.
- Case-level access control - investigators only see cases they're members of.
- Multi-factor authentication (TOTP) with QR-code enrolment.
- Account lockout after repeated failed logins, and sliding idle-session timeout.

**Evidence management**

- File upload with SHA-256 hashing on intake.
- **Magic-byte validation** - the file's real content is checked against its declared extension, and executables are rejected outright (defends against renamed malware).
- Automatic metadata / **EXIF** extraction for images.
- Files encrypted at rest with AES-256-GCM.

**Chain of custody**

- Every transfer is Ed25519-signed by the current holder.
- A lifecycle **state machine** enforces legally meaningful transitions (no skipping or unauthorised reversals).
- Graph-based integrity verification and custody-chain reconstruction.

**Analysis & oversight**

- Multi-factor **risk scoring** for every evidence item.
- **Anomaly detection** across all evidence using an Isolation Forest.
- Formula-based audit checks (time gaps, duplicate entries, role mismatches).
- AI investigation assistant.
- Tamper-evident **case export** as a signed ZIP (files + manifest + audit trail).

**Compliance**

- Append-only audit trail (updates and deletes are blocked at the ORM layer).
- Full audit records with actor, evidence, case, IP address, timestamp, and outcome.

---

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Web framework | Flask (application-factory pattern) |
| ORM / database | SQLAlchemy + SQLite (dev); PostgreSQL-ready |
| Auth & sessions | Flask-Login, Flask-WTF (CSRF), Flask-Limiter |
| 2fa | PyOTP (TOTP) + qrcode |
| Cryptography | `cryptography` (Ed25519, AES-256-GCM, Fernet, PBKDF2, X.509/TLS) |
| Image / metadata | Pillow (EXIF) |
| File-type validation | python-magic |
| Machine learning | scikit-learn (Isolation Forest) |
| Reporting | ReportLab |
| Testing | pytest, pytest-cov |

---

## Architecture

DEICMS uses the Flask **application-factory** pattern. Functionality is split into blueprints (route groups), business logic modules, and ORM models.

```
Browser (HTTPS / TLS)
        │
        ▼
Flask app  ►  Blueprints (routes)      auth · cases · evidence · custody ·
        │                                dashboard · audit · risk · assistant ·
        │                                admin · export
        │
        ├►  Logic layer                crypto · file_crypto · keyderive ·
        │                                graph_integrity · chain_reconstruction ·
        │                                state_machine · risk_scoring ·
        │                                anomaly_detection · audit_formulas · validators
        │
        └►  Models (SQLAlchemy ORM)     Investigator · Case · EvidenceItem ·
                                          CustodyLog · AuditRecord · CaseAccess
                                                    │
                                                    ▼
                                              SQLite database
```

Requests are protected by CSRF tokens, rate limiting, an idle-timeout hook, and security response headers (including HSTS on secure responses). The app runs over HTTPS locally using a self-signed certificate generated on first launch.

---

## Complex application logic

These are the algorithmically substantive components (the project's "complex logic" requirement):

**Graph integrity verification** (`app/logic/graph_integrity.py`)
Models an evidence item's custody history as a directed acyclic graph and performs a depth-first traversal with multi-condition validation at every node (signature validity, hash continuity, timestamp ordering, holder consistency). Produces a verdict and a completeness score.

**Custody-chain reconstruction** (`app/logic/chain_reconstruction.py`)
When the custody log has gaps - missing transfers, deleted entries, inconsistent timestamps - it reconstructs the most plausible complete chain from partial evidence and reports a confidence score and any unresolved gaps.

**Evidence lifecycle state machine** (`app/logic/state_machine.py`)
Enforces valid transitions between lifecycle states so evidence can't skip a state, move backwards without authorisation, or be moved by an investigator lacking the required role.

**Multi-factor risk scoring** (`app/logic/risk_scoring.py`)
Combines six normalised factors (integrity status, file-type risk, transfer frequency, role mismatches, inactivity, duplicates) into a weighted score, then applies interaction rules that escalate dangerous factor combinations. Classifies each item LOW / MEDIUM / HIGH / CRITICAL and generates recommendations. All weights, curves, and thresholds are expert-configured constants.

**Anomaly detection** (`app/logic/anomaly_detection.py`)
Builds a 6-dimensional feature vector per evidence item and fits a scikit-learn **Isolation Forest** to find statistical outliers across the whole population - complementing the rule-based risk scorer.

**Audit formula checks** (`app/logic/audit_formulas.py`)
Deterministic database checks for custody time gaps, duplicate log entries, and role-permission mismatches.

---

## Security design

DEICMS applies several layers of cryptographic and web security:

**Digital signatures (Ed25519).** Each investigator is issued an Ed25519 key pair at account creation. On every custody transfer, the outgoing investigator signs a canonical payload - `evidence_id`, event type, timestamp, both parties, and the file's SHA-256 hash - so any later alteration to the transfer or the file is detectable via signature verification.

**Encryption at rest.**
- **Evidence files** are encrypted on disk with **AES-256-GCM** (authenticated encryption - confidentiality *and* tamper detection), stored as `MAGIC | nonce | ciphertext+tag`.
- **Private keys** are wrapped with **Fernet** before storage, so a stolen database alone yields only encrypted, unusable keys.

**Key derivation (PBKDF2).** Symmetric keys are never stored - they're derived on demand from the application master secret using **PBKDF2-HMAC-SHA256** (200,000 iterations) with a distinct salt per purpose. Login passwords are hashed via Werkzeug.

**Append-only audit trail.** The `AuditRecord` model registers ORM hooks that raise on any update or delete, making the audit log tamper-evident at the data layer.

**Web hardening.** CSRF protection, rate limiting, `HttpOnly` + `Secure` + `SameSite=Lax` session cookies, HSTS headers, account lockout, idle-session timeout, and HTTPS/TLS in development via a self-signed certificate.

**Upload defence.** Magic-byte validation rejects renamed executables and enforces that a file's real content matches its declared type.

---

## Quick Start

### Prerequisites

- Python 3.10+ and `pip`
- Git
- On Linux/macOS, `python-magic` needs `libmagic` (`sudo apt install libmagic1` or `brew install libmagic`). On Windows it's bundled via `python-magic-bin`.

### 1. Clone and enter the project

```bash
git clone <your-repo-url>
cd deicms
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=replace-with-a-long-random-string
KEY_ENCRYPTION_SECRET=replace-with-another-long-random-string
NVIDIA_API_KEY=your-key-if-using-the-ai-assistant
```

If omitted, development defaults are used (not safe for production).

### 5. Seed the database (optional but recommended)

Populates investigators, cases, and evidence spanning LOW→CRITICAL risk so you can explore the full system.

```bash
python seed.py
```

### 6. Run

```bash
python run.py
```

A self-signed TLS certificate (`cert.pem` / `key.pem`) is generated automatically on first launch. Open **https://localhost:5001** and accept the one-time browser warning (expected for self-signed certificates in development).

---

## Usage

1. **Log in** with a seeded account (see `seed.py` for credentials) and complete 2fa if enabled.
2. **Create or open a case** and add member investigators.
3. **Upload evidence** - it's hashed, validated, metadata-extracted, and encrypted.
4. **Transfer custody** to another investigator; the transfer is digitally signed.
5. **Verify integrity** or **reconstruct the chain** from an evidence item's page.
6. Review the **risk dashboard**, **anomaly dashboard**, and **audit trail**.
7. **Export a case** as a signed, tamper-evident ZIP package.

---

## Testing

Tests are organised by development increment and run with pytest:

```bash
pytest tests/ -v --cov=app
```

- `tests/test_increment1.py` - core case & evidence management
- `tests/test_increment2.py` - state machine, graph integrity, chain reconstruction
- `tests/test_increment3.py` - risk scoring, AI assistant, anomaly detection, and routes
- `tests/test_day2.py` - key-pair generation and audit formula checks

---

## Project structure

```
deicms/
├ app/
│   ├ __init__.py            # Application factory, extensions, security hooks
│   ├ models/                # SQLAlchemy models
│   │   ├ investigator.py    # Users, roles, 2fa
│   │   ├ case.py
│   │   ├ case_access.py     # Case-level access control
│   │   ├ evidence.py
│   │   ├ custody_log.py     # Signed custody transfers
│   │   └ audit_record.py    # Append-only audit trail
│   ├ logic/                 # Business logic & algorithms
│   │   ├ crypto.py          # Ed25519 keys & signing
│   │   ├ file_crypto.py     # AES-256-GCM file encryption
│   │   ├ keyderive.py       # PBKDF2 key derivation
│   │   ├ graph_integrity.py
│   │   ├ chain_reconstruction.py
│   │   ├ state_machine.py
│   │   ├ risk_scoring.py
│   │   ├ anomaly_detection.py
│   │   ├ audit_formulas.py
│   │   └ validators.py      # Password policy
│   └ routes/                # Flask blueprints
│       ├ auth.py            # Login, logout, 2fa, lockout
│       ├ cases.py
│       ├ evidence.py        # Upload, magic-byte & EXIF handling
│       ├ custody.py         # Signed transfers, integrity, reconstruction
│       ├ dashboard.py
│       ├ audit.py
│       ├ risk.py
│       ├ assistant.py
│       ├ admin.py
│       └ export.py          # Signed ZIP case export
├ tests/                     # pytest suites (by increment)
├ config.py                  # Configuration & security settings
├ run.py                     # Entry point (HTTPS)
├ generate_cert.py           # Self-signed TLS cert generation
├ seed.py                    # Demo data seeder
├ requirements.txt
└ README.md
```

Utility scripts also included: `check_db.py`, `clear_evidence.py`, `deicms_db_audit.py`, `recover_db.py`.

---

## Future Enhancements

- PostgreSQL support for production deployments.
- Docker Compose environment.
- Multi-instance deployment.
- AI explainability for anomaly detection.
- REST API for external integrations.
- Comprehensive logging and monitoring.

---

## Security notes & disclaimer

This project was built for **educational purposes** as part of a System Security course. While it implements real cryptographic primitives and security controls, it has **not** been audited or hardened for production use. Notably:

- Development defaults are used for secrets when environment variables are absent - always set strong `SECRET_KEY` and `KEY_ENCRYPTION_SECRET` values.
- The local TLS certificate is self-signed.
- SQLite is used for development; a production deployment should use PostgreSQL and a proper secrets manager.

Do not use DEICMS to handle real, sensitive, or legally significant evidence.
