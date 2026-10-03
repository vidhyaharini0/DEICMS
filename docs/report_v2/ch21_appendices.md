# Chapter 21 - Appendices

---

## Appendix A - User-Story Catalogue

The twenty-seven original stories and the two maintenance change-request stories, with their feature category, MoSCoW priority, story-point estimate and delivering iteration. Acceptance criteria are given in Sections 7.5 and 7.6 and in the planning sections of Chapter 5.

| ID | Title | Category | MoSCoW | Pts | Iteration |
|---|---|---|---|---|---|
| US-01 | Secure login and logout | A / Sec | Must | 3 | 1 |
| US-02 | Role-based access control | A | Must | 5 | 1 |
| US-03 | Case CRUD, search and archive | A | Must | 5 | 1 |
| US-04 | Upload and register evidence | A | Must | 5 | 1 |
| US-05 | SHA-256 fingerprint at upload | B | Must | 2 | 1 |
| US-06 | EXIF / MIME metadata extraction | B | Must | 3 | 1 |
| US-07 | Edit and categorise evidence | A | Must | 3 | 1 |
| US-08 | Record custody transfers and access events | A | Must | 5 | 1 |
| US-09 | Append-only audit trail | A | Must | 5 | 1 |
| US-10 | Formula-based audit checks | A | Should | 3 | 1 |
| US-11 | Admin-only account creation | A | Must | 1 | 1 |
| US-12 | Ed25519-signed custody events | B | Must | 5 | 2 |
| US-13 | Graph integrity verification algorithm | **C** | Must | **13** | 2 |
| US-14 | Evidence lifecycle state machine | **C** | Must | 8 | 2 |
| US-15 | Custody chain reconstruction algorithm | **C** | Must | 8 | 2 |
| US-16 | Integrity verification report UI | A | Should | 2 | 2 |
| US-17 | Chain reconstruction report UI | A | Should | 2 | 2 |
| US-18 | Multi-factor risk scoring algorithm | **C** | Must | 8 | 3 |
| US-19 | Admin-configurable risk weights | C / A | Should | 3 | 3 |
| US-20 | AI assistant orchestration pipeline | **C** | Must | 8 | 3 |
| US-21 | Hallucination detection | **C** | Must | 3 | 3 |
| US-22 | Isolation Forest anomaly detection | B | Could | 5 | 3 |
| US-23 | Risk and anomaly dashboards | A | Should | 3 | 3 |
| US-24 | 2FA, lockout and session timeout | Sec / B | Should | 5 | 3 |
| US-25 | Encryption at rest and magic-byte checks | Sec / B | Should | 3 | 3 |
| US-26 | Tamper-evident signed ZIP export | B | Should | 2 | 3 |
| US-27 | PDF chain-of-custody report | B | Could | 2 | 3 |
| US-28 | Role-scoped dashboard and aggregated views | A / Sec | Must | 5 | M1 |
| US-29 | Access-scoped AI assistant and chat isolation | C / Sec | Must | 5 | M1 |
| | **Total** | | | **130** | |

The M2 defect findings (D1-D6, H1-H3, R1-R2) are catalogued in Table 5.9 rather than as backlog stories, because repairing a defect restores a requirement already accepted rather than introducing a new one.

---

## Appendix B - HTTP Interface Reference

Thirty-three routes across ten blueprints. The authorisation of each is given in full in **Table 8.5** (the use-case catalogue), derived by reading the guard in each route handler; only the paths are listed here.

| Blueprint | Routes |
|---|---|
| `auth` | `/login` · `/logout` · `/verify-otp` · `/2fa/setup` · `/2fa/disable` |
| `dashboard` | `/dashboard` |
| `cases` | `/cases` · `/cases/new` · `/cases/<id>` · `/cases/<id>/edit` · `/cases/<id>/archive` · `/cases/<id>/members/add` · `/cases/<id>/members/remove` |
| `evidence` | `/cases/<id>/evidence/upload` · `/cases/<id>/evidence/<eid>` · `…/edit` · `…/delete` |
| `custody` | `/evidence/<eid>/transfer` · `/custody-log` · `/verify` · `/verify/json` · `/reconstruct` · `/change-state` |
| `risk` | `/risk/dashboard` · `/risk/anomaly` · `/risk/evidence/<eid>` · `/risk/evidence/<eid>/json` |
| `audit` | `/audit` · `/audit/evidence/<eid>` · `/audit/evidence/<eid>/formula-check` |
| `assistant` | `/assistant/` · `/assistant/chat` · `/assistant/clear` |
| `export` | `/cases/<id>/export` · `/evidence/<eid>/custody-report.pdf` |
| `admin` | `/admin/users` · `/admin/users/new` · `/admin/users/<id>/change-role` · `…/toggle-active` · `…/unlock` · `/admin/risk-settings` |

All routes require authentication except `/login` and `/verify-otp`.

---

## Appendix C - Database Schema Reference

The full schema - columns, SQL types, keys, constraints, cardinalities and indexes - is given graphically in **Figure 8.3**. This appendix records only the constraints that carry domain meaning and are therefore referenced elsewhere in the report.

| Table | Constraint | Why it matters |
|---|---|---|
| `investigators` | `email` UNIQUE | Identity; prevents duplicate accounts |
| `investigators` | `role` ENUM of exactly four values | The whole authorisation model rests on this (Table 8.6) |
| `cases` | `case_number` UNIQUE | Business key used in court documents |
| `cases` | `is_archived` BOOLEAN - no DELETE path | Soft archive; DR-04 |
| `evidence_items` | **`original_hash` CHAR(64) NOT NULL, never updated** | The immutable ground truth for all integrity verification (G1) |
| `evidence_items` | `current_hash` separate from `original_hash` | Verification is the comparison of the two; collapsing them destroys the capability |
| `evidence_items` | `integrity_status` ENUM | Written back by the verifier; read by the risk scorer (finding D2) |
| `evidence_items` | `is_deleted` BOOLEAN - no DELETE path | Soft delete preserves custody and audit history (finding D1) |
| `custody_logs` | **`digital_signature` TEXT NOT NULL** | An unsigned custody record cannot be represented (FR-24) |
| `custody_logs` | ≥ 1 row per evidence item | Enforced by atomic creation at upload (FR-12); the verifier's upload-root assumption depends on it |
| `audit_records` | Insert-only, enforced by ORM event listeners | Not expressible in DDL; history cannot be rewritten (FR-19) |
| `case_access` | UNIQUE (`case_id`, `investigator_id`) | Associative entity resolving the many-to-many; source of `accessible_case_ids` |

---

## Appendix D - Requirements Traceability

Forward traceability - requirement → user story → implementing module → verifying test - is carried **inline in Table 7.5**, which lists all fifty-six functional requirements with those columns. It is not repeated here.

**Coverage:** every functional requirement traces to at least one implementing module and at least one verifying test module. No requirement is unimplemented, and none is unverified.

---

## Appendix E - Glossary and Acronyms

**AES-256-GCM** - Advanced Encryption Standard, 256-bit key, Galois/Counter Mode; an authenticated encryption scheme used for evidence at rest. Provides both confidentiality and tamper-detection.

**Append-only** - a persistence discipline in which records may be inserted but never updated or deleted. Enforced in DEICMS at the ORM layer.

**Burndown chart** - a plot of remaining story points against time across an iteration, with an ideal line for comparison. The instrument by which process timeliness is made visible.

**Chain of custody** - the documented, unbroken record of who has held an item of evidence and what was done to it; required for legal admissibility.

**Cohesion** - the degree to which the elements of a module belong together. High cohesion is desirable.

**Coupling** - the degree of interaction between modules. Low coupling is desirable.

**COTS** - Commercial Off-The-Shelf; a large-scale existing system reused rather than built.

**CSP** - Content-Security-Policy; an HTTP header restricting the origins from which a page may load resources.

**CSRF** - Cross-Site Request Forgery; an attack in which a user is tricked into submitting an unwanted state-changing request.

**DAG** - Directed Acyclic Graph; the in-memory structure into which the custody history is built for verification.

**DEICMS** - Digital Evidence Integrity & Chain-of-Custody Management System; this project.

**DevOps** - a set of practices unifying development and operations, characterised by continuous integration, continuous delivery, infrastructure as code and monitoring.

**DFS** - Depth-First Search; the traversal used by the graph integrity verifier.

**Ed25519** - an Edwards-curve digital signature scheme used to sign custody events; chosen for its strong security margin and small keys.

**EXIF** - Exchangeable Image File Format; metadata embedded in image files.

**Fail-visible** - an error-handling posture in which a failure is recorded and made conspicuous rather than silently absorbed (fail-silent) or blocking the operation entirely (fail-closed).

**Fernet** - an authenticated symmetric-encryption token format used to protect private keys at rest.

**HSTS** - HTTP Strict-Transport-Security; a header preventing fallback from HTTPS to HTTP.

**IDOR** - Insecure Direct Object Reference; an access-control flaw in which an object is reached by identifier without verifying the requester's right to it. Fixed as M2 finding D3.

**Isolation Forest** - an unsupervised machine-learning algorithm for anomaly detection, used to flag statistical outliers among evidence items.

**Lehman's laws** - eight empirical observations about how software systems evolve, applied in Section 14.2.

**LLM** - Large Language Model; the pre-trained model underlying the AI assistant.

**MDE** - Model-Driven Engineering; an approach in which models are the primary artefacts and code is generated from them. *Not* practised in this project.

**MIME** - Multipurpose Internet Mail Extensions; the content-type of a file, validated in DEICMS against its magic bytes rather than its extension.

**MoSCoW** - a prioritisation scheme: Must have, Should have, Could have, Won't have this time.

**NIM** - NVIDIA Inference Microservices; the OpenAI-compatible endpoint through which the language model is consumed.

**ORM** - Object-Relational Mapper; SQLAlchemy, mapping Python objects to database rows.

**Plausibility threshold** - the minimum score (0.40) a candidate must reach before the reconstruction algorithm will infer a custody link rather than mark the gap unresolved.

**SHA-256** - Secure Hash Algorithm producing a 256-bit fingerprint, used for evidence file integrity.

**Story point** - a unit of relative size on a Fibonacci scale (1, 2, 3, 5, 8, 13), used in estimation. Independent of MoSCoW priority.

**TDD** - Test-Driven Development; writing a test before the code that satisfies it.

**TOTP** - Time-based One-Time Password; the second authentication factor.

**V-model** - a refinement of the waterfall model pairing each construction phase with the test level that validates it.

**Velocity** - the number of story points a team delivers in one iteration; an observed property, not a target.

**WAL** - Write-Ahead Log; SQLite's journaling mode, relevant to inspecting the live database (see `flush_db.py`).

**XSS** - Cross-Site Scripting; an injection attack whose stored variant in the chat interface was fixed as M2 finding H1.

---

*[End of Report]*
