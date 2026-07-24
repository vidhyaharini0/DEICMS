# Part VII — Conclusions and Appendices

---

## 25. Project Retrospective, Velocity Analysis and Future Work

### 25.1 Project-Level Retrospective

Read as a whole rather than increment by increment, the project tells a coherent story about how a system's weaknesses are found and fixed, and that story is the most valuable thing the retrospective has to offer. The three increments each closed with a retrospective whose actions fed the next, and the two maintenance iterations each closed with a lesson, and taken together they trace a single arc: the project learned, repeatedly and concretely, that the parts of a system given the most isolation and the most adversarial scrutiny are the parts that behave, while the parts that escape that scrutiny are where the real defects hide.

The arc is visible in the sequence of lessons. Increment 1 learned that scaffolding is real work that estimates must account for, and that wiring cross-cutting concerns such as auditing into each route as it is built is cheaper than retrofitting them. Increment 2 learned that the difficulty of an algorithm is not always where it appears to be — the cryptographic checks that looked hard were library calls, while the traversal semantics that looked simple were the real work — and that fixing the format of signed data before writing the signer and verifier prevents a whole class of subtle bug. Increment 3 learned that hiding an external dependency behind a testable seam and writing an algorithm's acceptance criteria as tests before implementing it together produce the steadiest progress, and it also produced, in its own retrospective, the observation that the one defect class it had not given a dedicated test focus — access scoping in aggregates — was exactly where a defect emerged. Maintenance iteration M1 acted on that observation, closing the scoping leak and, more importantly, adopting adversarial authorisation testing as a standing practice. Maintenance iteration M2 completed the lesson by showing that a green test suite can coexist with critical defects, and that a distinct class of correctness bug — a feature that silently does nothing — is caught by reading code against its intent rather than by running it. The project therefore ends holding two complementary quality practices it did not begin with: adversarial testing of the boundaries, and periodic review of the code against its specification. That it acquired both by experience rather than by prescription is the clearest evidence that the incremental process did what it is supposed to do.

### 25.2 Velocity Analysis

The project's velocity across the three increments was strikingly stable. Each increment committed to a budget of story points and delivered all of them: forty in the first increment, thirty-eight in the second, and forty-two in the third, for a mean velocity of forty points per increment and a total of one hundred and twenty points of committed scope delivered in full. The first maintenance iteration added a further ten points, also delivered in full, bringing the point-estimated total to one hundred and thirty; the second maintenance iteration was defect-repair driven and is measured by its eleven findings rather than by a point budget.

**Table 25.1 — Velocity across the increments**

| Iteration | Committed | Delivered | Notes |
|---|---|---|---|
| Increment 1 | 40 | 40 | Slow start (setup), recovered by day 14 |
| Increment 2 | 38 | 38 | Mid-sprint plateau (integrity rework), recovered |
| Increment 3 | 42 | 42 | Steadiest; tracked ideal within ~2 points |
| Maintenance M1 | 10 | 10 | Two access-scoping change requests |
| Maintenance M2 | — | 11 findings | Defect-repair; catalogued as findings |
| **Total (points)** | **130** | **130** | Mean increment velocity 40.0 |

That every committed point was delivered should be read with a critical eye rather than as an unqualified success, and the retrospective does so. Full delivery in every increment is partly a genuine result of realistic estimation and stable scope, and partly an artefact of a single-developer project in which the estimator and the implementer are the same person, so that estimates could be, and were, adjusted with perfect knowledge of the implementer's pace. The more informative signal is not that the totals were met but the *shape* of each burndown: the slow start in Increment 1, the mid-sprint plateau in Increment 2, and the steady tracking in Increment 3. Those shapes tell the real story of where the work was hard, and it is no coincidence that the steadiest burndown belongs to the increment that had the benefit of two increments' worth of accumulated retrospective actions. Velocity, in other words, is most honestly read here as a measure of how well the process was working rather than of how much was produced, and by that reading it improved across the project.

### 25.3 Was the Process Choice Right?

With the project complete, the choice of the agile incremental model over a plan-driven one can be assessed against outcomes rather than expectations, and the assessment is favourable. The decisive argument for the incremental model at the outset was that technical risk was concentrated in the complex algorithms and that committing their full design on paper before building them would have wasted effort; that argument was borne out precisely, because the graph verifier's design did change under implementation in exactly the way a waterfall plan would have frozen and then had to unfreeze. The secondary argument, that inter-increment feedback would improve the work, was borne out even more strongly than expected, because the two maintenance iterations — the clearest demonstrations of the model's value — were only possible because working software existed early enough to be probed adversarially and read critically while the project was still under way. A plan-driven project would have discovered the scoping leak and the dead soft-delete after delivery, if at all. The one honest caveat is that the model's collaborative ceremonies had to be adapted for a single developer, and the report has been candid about that adaptation throughout; but the core of the model — build a working increment, reflect, adjust, repeat — applied without modification and delivered its promised benefits.

### 25.4 Future Work

The boundary of the delivered system was drawn deliberately, and the work beyond that boundary falls into two groups. The first is the explicitly deferred scope recorded in the product backlog's won't-have list: a production PostgreSQL deployment behind a multi-process server, email and push notifications, full-text search over evidence *content* rather than metadata, a multi-language interface, a mobile client, and any fine-tuning of the language model. None of these would add to the software-engineering demonstration, which is why they were excluded, but each is a natural extension for a system intended to be operated rather than assessed.

The second group is the set of limitations the report has named as it went, each of which points to concrete future work. The self-signed development certificate would be replaced by one from a recognised authority. The Content-Security-Policy would be tightened from its current inline-permitting form to a nonce-based policy, removing the `unsafe-inline` allowance once the templates were refactored to avoid embedded scripts and styles. The insecure default secrets, currently flagged by a startup warning, would be made mandatory configuration that refuses to start without real values. The sequential case and evidence numbering, adequate for single-user operation, would be made robust under concurrency. And the system would be subjected to the load and penetration testing that an academic project does not warrant but a deployment would demand. Recording these as future work rather than as failings is consistent with the report's approach throughout: the value of naming a limitation precisely is that it becomes a specification for the work that would remove it.

### 25.5 Concluding Remarks

DEICMS set out to be a system whose entire purpose is to be trustworthy — to manage digital evidence in a way that makes tampering either impossible or evident, that confines every user to the data they are entitled to, that records its own history immutably, that enforces the procedures of its domain, and that helps its users reason about risk. It delivered on those aims across three increments and two maintenance iterations, with five complex algorithms implemented from scratch, a rich data model, a varied and honestly-attributed set of third-party integrations, a layered security posture, and a suite of one hundred and seventy-two tests. More than the artefact, though, the project produced a demonstration of software-engineering practice: a defensible choice of process, honestly executed; a categorisation of features approached with rigour rather than as a labelling exercise; and, above all, a willingness to find and document the system's own defects rather than to present it as flawless. That last quality — the treatment of the maintenance iterations not as embarrassments to be hidden but as the process working as intended — is the one the report would most want to be judged by, because in a system built to be trustworthy, the trustworthiness of the account of how it was built is not a separate matter.

---

## 26. References

The following sources informed the design, the technology choices, and the engineering practices described in this report.

1. Beck, K., et al. (2001). *Manifesto for Agile Software Development.* agilemanifesto.org.
2. Schwaber, K., and Sutherland, J. *The Scrum Guide.* scrumguides.org.
3. Sommerville, I. *Software Engineering.* Pearson.
4. Pressman, R. S., and Maxim, B. R. *Software Engineering: A Practitioner's Approach.* McGraw-Hill.
5. Fowler, M. *The Practical Test Pyramid* and *Refactoring.* martinfowler.com; Addison-Wesley.
6. Pallets Projects. *Flask Documentation.* flask.palletsprojects.com.
7. *SQLAlchemy Documentation.* sqlalchemy.org.
8. Python Cryptographic Authority. *`cryptography` Library Documentation.* cryptography.io.
9. National Institute of Standards and Technology. *FIPS PUB 180-4: Secure Hash Standard (SHA-256).*
10. Josefsson, S., and Liusvaara, I. (2017). *RFC 8032: Edwards-Curve Digital Signature Algorithm (EdDSA / Ed25519).* IETF.
11. National Institute of Standards and Technology. *SP 800-38D: Galois/Counter Mode (AES-GCM).*
12. M'Raihi, D., et al. (2011). *RFC 6238: TOTP — Time-Based One-Time Password Algorithm.* IETF.
13. Liu, F. T., Ting, K. M., and Zhou, Z.-H. (2008). *Isolation Forest.* IEEE ICDM.
14. Pedregosa, F., et al. (2011). *scikit-learn: Machine Learning in Python.* JMLR.
15. *ReportLab User Guide.* reportlab.com.
16. OWASP Foundation. *OWASP Top Ten* and *Content Security Policy Cheat Sheet.* owasp.org.
17. Scientific Working Group on Digital Evidence (SWGDE). *Best Practices for Digital Evidence Collection* and chain-of-custody guidance.
18. NVIDIA. *NIM (NVIDIA Inference Microservices) API Documentation.*

*(URLs are given in short form; full addresses are available from the cited organisations.)*

---

## 27. Appendices

### Appendix A — User-Story Catalogue

The twenty-seven original stories and the two maintenance change-request stories, with their category, MoSCoW priority, story-point estimate, and delivering iteration. Full acceptance criteria appear in the planning chapter of each increment (Parts II–V).

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
| US-13 | Graph integrity verification algorithm | C | Must | 13 | 2 |
| US-14 | Evidence lifecycle state machine | C | Must | 8 | 2 |
| US-15 | Custody chain reconstruction algorithm | C | Must | 8 | 2 |
| US-16 | Integrity verification report UI | A | Should | 2 | 2 |
| US-17 | Chain reconstruction report UI | A | Should | 2 | 2 |
| US-18 | Multi-factor risk scoring algorithm | C | Must | 8 | 3 |
| US-19 | Admin-configurable risk weights | C / A | Should | 3 | 3 |
| US-20 | AI assistant orchestration pipeline | C | Must | 8 | 3 |
| US-21 | Hallucination detection | C | Must | 3 | 3 |
| US-22 | Isolation Forest anomaly detection | B | Could | 5 | 3 |
| US-23 | Risk and anomaly dashboards | A | Should | 3 | 3 |
| US-24 | 2FA, lockout and session timeout | Sec / B | Should | 5 | 3 |
| US-25 | Encryption at rest and magic-byte checks | Sec / B | Should | 3 | 3 |
| US-26 | Tamper-evident signed ZIP export | B | Should | 2 | 3 |
| US-27 | PDF chain-of-custody report | B | Could | 2 | 3 |
| US-28 | Role-scoped dashboard and aggregated views | A / Sec | Must | 5 | M1 |
| US-29 | Access-scoped AI assistant and chat isolation | C / Sec | Must | 5 | M1 |

The maintenance-iteration-M2 defect findings (D1–D6, H1–H3, R1–R2) are catalogued in the product backlog and detailed in Part V, Chapter 21.

### Appendix B — HTTP Interface Reference

The application exposes the following routes, grouped by blueprint. Methods are shown as G (GET) and P (POST); all routes require authentication except the login and one-time-password routes.

| Method | Path | Purpose |
|---|---|---|
| G/P | `/login` (and `/`) | Log in |
| G | `/logout` | Log out |
| G/P | `/verify-otp` | Second-factor verification |
| G/P | `/2fa/setup`, `/2fa/disable` | Enrol / disable TOTP two-factor authentication |
| G | `/dashboard` | Role-tailored dashboard |
| G | `/cases` | List accessible cases (paginated) |
| G/P | `/cases/new` | Create a case |
| G | `/cases/<id>` | View a case and its evidence |
| G/P | `/cases/<id>/edit` | Edit a case |
| P | `/cases/<id>/archive` | Archive a case |
| P | `/cases/<id>/members/add`, `/members/remove` | Manage case membership |
| G | `/cases/<id>/export` | Download the signed ZIP export |
| G/P | `/cases/<id>/evidence/upload` | Upload and register evidence |
| G | `/cases/<id>/evidence/<eid>` | View an evidence item |
| G/P | `/cases/<id>/evidence/<eid>/edit` | Edit evidence metadata |
| P | `/cases/<id>/evidence/<eid>/delete` | Soft-delete an evidence item |
| G/P | `/evidence/<eid>/transfer` | Record a signed custody transfer |
| G/P | `/evidence/<eid>/change-state` | Trigger a lifecycle transition |
| G | `/evidence/<eid>/custody-log` | View the custody log |
| G | `/evidence/<eid>/verify` (+ `/verify/json`) | Run graph integrity verification |
| G | `/evidence/<eid>/reconstruct` | Run custody-chain reconstruction |
| G | `/evidence/<eid>/custody-report.pdf` | Download the PDF custody report |
| G | `/risk/dashboard` | Risk-ranked evidence (scoped) |
| G | `/risk/anomaly` | Isolation Forest anomaly view |
| G | `/risk/evidence/<eid>` (+ `/json`) | Per-item risk report |
| G | `/audit` | Global audit trail (Admin only) |
| G | `/audit/evidence/<eid>` (+ `/formula-check`) | Per-item audit trail and formula checks |
| G | `/assistant/` | AI assistant chat page |
| P | `/assistant/chat`, `/assistant/clear` | Assistant query / clear history |
| G | `/admin/users` (+ `/new`) | List / create investigator accounts |
| P | `/admin/users/<id>/change-role`, `/toggle-active`, `/unlock` | Account management |
| G/P | `/admin/risk-settings` | Configure risk weights and thresholds |

### Appendix C — Database Schema Reference

The six entities and their principal columns. Primary keys are integer surrogates; unique business keys and foreign keys are noted.

**Investigator** — id (PK); full_name; email (unique); password_hash; role (enum: Admin, Lead Investigator, Analyst, Read-Only); public_key; private_key_encrypted; is_active; failed_login_count; locked_until; totp_secret; created_at; updated_at.

**Case** — id (PK); case_number (unique); title; description; jurisdiction; status; is_archived; date_opened; date_closed; created_by_id (FK → Investigator); assigned_to_id (FK → Investigator); created_at.

**Evidence Item** — id (PK); evidence_number (unique); case_id (FK → Case); title; description; category (enum); lifecycle_state (enum); file_name; file_path; file_mime_type; original_hash; current_hash; exif_metadata; uploaded_by_id (FK); current_holder_id (FK); risk_score; risk_level (enum); **integrity_status** (enum: VERIFIED/NOT_CHECKED/FAILED); **is_deleted** (bool); created_at; updated_at.

**Custody Log** — id (PK); evidence_id (FK → Evidence Item); event_type (enum: Upload, Transfer, Access, Verification); from_investigator_id (FK); to_investigator_id (FK); timestamp; location; reason; file_hash_at_event; digital_signature (NOT NULL); notes.

**Audit Record** — id (PK); event_type (enum); investigator_id (FK); evidence_id (FK); case_id (FK); description; ip_address; result (enum: Success/Failure/Warning); integrity_check_result; timestamp. *Updates and deletes are blocked at the ORM layer (append-only).*

**Case Access** — id (PK); case_id (FK → Case); investigator_id (FK → Investigator); permission (enum: Owner/Member/ReadOnly); granted_at; granted_by_id (FK). *Unique on (case_id, investigator_id).*

### Appendix D — Glossary and Acronyms

**AES-256-GCM** — Advanced Encryption Standard, 256-bit key, Galois/Counter Mode; an authenticated encryption scheme used for evidence at rest.
**Chain of custody** — the documented, unbroken record of who has held an item of evidence and what was done to it, required for legal admissibility.
**CSP** — Content-Security-Policy; an HTTP header restricting the origins from which a page may load resources.
**CSRF** — Cross-Site Request Forgery; an attack in which a user is tricked into submitting an unwanted state-changing request.
**DAG** — Directed Acyclic Graph; the in-memory structure into which the custody history is built for verification.
**DEICMS** — Digital Evidence Integrity & Chain-of-Custody Management System; this project.
**DFS** — Depth-First Search; the traversal used by the graph integrity verifier.
**Ed25519** — an Edwards-curve digital signature scheme used to sign custody events.
**EXIF** — Exchangeable Image File Format metadata embedded in image files.
**Fernet** — an authenticated symmetric-encryption token format used to protect private keys at rest.
**HSTS** — HTTP Strict-Transport-Security; a header preventing fallback from HTTPS to HTTP.
**IDOR** — Insecure Direct Object Reference; an access-control flaw fixed in maintenance iteration M2.
**Isolation Forest** — an unsupervised machine-learning algorithm for anomaly detection.
**LLM** — Large Language Model; the pre-trained model underlying the AI assistant.
**MIME** — Multipurpose Internet Mail Extensions; the content-type of a file, validated against its magic bytes.
**MoSCoW** — a prioritisation scheme: Must, Should, Could, Won't-have.
**NIM** — NVIDIA Inference Microservices; the OpenAI-compatible endpoint through which the language model is consumed.
**ORM** — Object-Relational Mapper; SQLAlchemy, mapping Python objects to database rows.
**SHA-256** — Secure Hash Algorithm producing a 256-bit fingerprint, used for file integrity.
**TOTP** — Time-based One-Time Password; the second authentication factor.
**WAL** — Write-Ahead Log; SQLite's journaling mode, relevant to inspecting the live database (see `flush_db.py`).
**XSS** — Cross-Site Scripting; an injection attack whose stored variant in the chat was fixed in maintenance iteration M2.

*[End of Part VII — End of Report]*
