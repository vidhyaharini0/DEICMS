# Chapter 7 — Requirements Engineering

---

## 7.1 The Requirements Engineering Process

Requirements engineering is the process of establishing the services a customer requires from a system and the constraints under which it operates and is developed. The requirements themselves are the descriptions of those services and constraints.

A requirement may be written at very different levels of abstraction, and this is inevitable because requirements serve a dual function. At the start of a procurement they must be written openly enough that several competing solutions could satisfy them; once a contract has been awarded, the same needs must be restated in enough detail that the client can validate what the software will actually do. Both documents may legitimately be called "the requirements".

This produces the standard two-level distinction.

**Table 7.1 — Types of requirement**

| Type | Describes | Written for | DEICMS location |
|---|---|---|---|
| **User requirements** | The services the system provides and its operational constraints, in natural language | Customers, client managers, end users | Section 7.4 |
| **System requirements** | A structured, detailed description of the system's functions, services and operational constraints | System architects, software developers, client engineers | Sections 6.5 to 6.8 |

The audiences differ and so the documents differ: client managers and end users read user requirements; system architects and developers read system requirements; client engineers read both.

**Table 7.2 — The requirements engineering activities as performed in DEICMS**

| Activity | Purpose | How it was performed |
|---|---|---|
| **Elicitation and analysis** | Discover the requirements | Domain analysis of forensic chain-of-custody procedure; persona construction; derivation from the five guarantees (Section 7.3) |
| **Specification** | Record them in a usable form | 29 user stories with acceptance criteria; the FR, NFR, domain and system tables in this chapter |
| **Validation** | Confirm they are the right requirements | Acceptance-criteria review at each sprint review; traceability matrix (Appendix D) |
| **Management** | Control change to them | Product backlog under version control; change requests CR-01 and CR-02 raised formally in M1 |

Because DEICMS is an academic project without an external customer, the elicitation activity had no interview stage. Rather than pretend otherwise, requirements were derived by **domain analysis** — reasoning from the legal obligations that govern digital evidence — and anchored to personas so that each requirement traces to a concrete responsibility rather than an abstract actor. The limits of this approach are stated in Section 7.12.

## 7.2 Stakeholders and Personas

Four personas correspond to the system's four roles. They are used throughout the user stories so that every requirement is anchored to a stated need.

**Table 7.3 — Stakeholder personas**

| Persona | Role | Responsibility | Defining need | Must **not** be able to |
|---|---|---|---|---|
| **Amelia** | Administrator | The system itself, not any single investigation: accounts, roles, unlocking, risk configuration, oversight | Control and visibility across the whole system | — (the only role with global scope) |
| **Luca** | Lead Investigator | Owns cases: opens investigations, adds members, uploads and transfers evidence, drives lifecycle, produces the court-ready export | Manage his own cases efficiently and be alerted to items needing attention | See or act on cases he is not a member of |
| **Nadia** | Analyst | Works on evidence within her assigned cases: examines items, runs integrity checks, queries the assistant, holds custody during analysis | A focused workbench of the items she is responsible for | Create accounts, change roles, or reach other cases |
| **Riya** | Read-Only Auditor | Reviews without modifying: inspects custody chains and audit trails in shared cases to confirm procedure was followed | Transparency over the items she may review | Trigger any state-changing action, anywhere |

The four personas embody the least-privilege principle: each sees and can do exactly what their responsibility requires, and the difference between them is enforced by the role and case-access model rather than by convention. The final column is not decoration — it is the source of the negative requirements that Section 7.12 records as the ones ordinary functional testing does not verify.

## 7.3 Requirements Elicitation

Requirements were elicited by three complementary routes.

**Domain analysis.** The legal doctrine governing admissibility of digital evidence specifies what must be demonstrable: continuous custody, content integrity, authorised handling, and a complete record. Each of these translates directly into a system obligation, and together they became the five guarantees of Table 1.1.

**Persona-driven derivation.** For each of the four personas, the question *what must this person be able to do, and what must they be prevented from doing?* was answered systematically. The first half produced functional requirements; the second half produced the confidentiality and least-privilege non-functional requirements — and, later, the adversarial tests of M1.

**Categorisation-driven completeness check.** Because the coursework requires balance across three feature categories, the requirement set was checked against the categorisation (Section 7.10) and gaps were visible as under-populated categories. This is an unusual elicitation route, and it is disclosed as such: it is a constraint of the assignment rather than of the domain, and Section 16.6 examines whether it distorted the result.

## 7.4 User Requirements

User requirements are stated in natural language, from the user's point of view, without prescribing a solution.

**Table 7.4 — User requirements**

| ID | Role | Requirement |
|---|---|---|
| UR-01 | All | Log in securely with credentials and be logged out automatically after a period of inactivity |
| UR-02 | Administrator | Create investigator accounts and assign each one a role |
| UR-03 | Administrator | Unlock an account that has been locked by repeated failed logins |
| UR-04 | Administrator | Review the complete system-wide audit trail |
| UR-05 | Administrator | Tune the risk-scoring weights and classification thresholds to the unit's priorities |
| UR-06 | Lead Investigator | Open, search, update and archive cases |
| UR-07 | Lead Investigator | Grant and revoke other investigators' access to a case |
| UR-08 | Lead Investigator | See the items in my cases that need my attention, ranked by risk |
| UR-09 | Lead Investigator | Produce a tamper-evident export package of a case for court |
| UR-10 | Lead Investigator | Upload a digital file and register it as evidence within a case |
| UR-11 | Analyst | Transfer custody of an item to another investigator, recording why |
| UR-12 | Analyst | Verify that an item's entire custody history is intact |
| UR-12a | Analyst | Examine the evidence items in the cases I am assigned to |
| UR-13 | Analyst | See a plausible reconstruction when custody records are incomplete |
| UR-14 | Analyst | Ask questions in plain English about the data I am permitted to see |
| UR-15 | Analyst | Move an item through its lifecycle only in ways procedure allows |
| UR-16 | Read-Only Auditor | Inspect the custody chain and audit trail of items in cases shared with me |
| UR-17 | Read-Only Auditor | Print a chain-of-custody report for an item |
| UR-18 | All | Never see data belonging to a case I am not a member of, in any view |

UR-18 is stated as a user requirement rather than only as a non-functional one because it is a promise made to *every* user about *every other* user's data, and it was the requirement whose incomplete application produced the M1 defects.

## 7.5 Functional Requirements

Functional requirements describe the system's services — what it should do, how it should react to particular inputs, and in some cases what it should *not* do. They depend on the type of software, its expected users, and the type of system in which it is used.

Table 7.5 is the complete functional requirement set. Each row records the requirement, its feature category, its MoSCoW priority, the increment that delivered it, the user story it derives from, and the test module that verifies it. The final two columns are what make the table a traceability instrument rather than a list.

**Table 7.5 — Functional requirements**

| ID | Requirement | Cat. | MoSCoW | Increment | Story | Verified by |
|---|---|---|---|---|---|---|
| FR-01 | The system shall authenticate an investigator by email and password, rejecting invalid credentials without revealing which field was wrong | A / Sec | Must | 1 | US-01 | `test_increment1` |
| FR-02 | The system shall store passwords only as salted hashes, never in plaintext | A / Sec | Must | 1 | US-01 | `test_increment1` |
| FR-03 | The system shall expire a session after a configurable period of inactivity through a sliding timeout | A / Sec | Must | 1, 3 | US-01, US-24 | `test_increment3` |
| FR-04 | The system shall assign each account exactly one of four roles: Admin, Lead Investigator, Analyst, Read-Only | A | Must | 1 | US-02 | `test_increment1` |
| FR-05 | The system shall enforce the minimum required role on every route, redirecting unauthorised access with an explanatory message | A | Must | 1 | US-02 | `test_increment1`, `test_scoping` |
| FR-06 | The system shall prevent a Read-Only user from triggering any state-changing action | A | Must | 1 | US-02 | `test_scoping` |
| FR-07 | The system shall allow authorised users to create, search, update and archive cases | A | Must | 1 | US-03 | `test_increment1` |
| FR-08 | The system shall archive a case as a soft operation that never physically deletes case data | A | Must | 1 | US-03 | `test_increment1` |
| FR-09 | The system shall scope every user's view of cases to those they are a member of | A | Must | 1, M1 | US-02, US-28 | `test_scoping` |
| FR-10 | The system shall accept uploads only of allow-listed file types and reject all others | A / Sec | Must | 1 | US-04 | `test_increment1` |
| FR-11 | The system shall generate a unique evidence number and make the uploader the first custodian | A | Must | 1 | US-04 | `test_increment1` |
| FR-12 | The system shall create an initial custody entry atomically with the evidence record, so no item can exist without a custody history | A | Must | 1 | US-04 | `test_increment1` |
| FR-13 | The system shall compute a SHA-256 fingerprint at upload, store it as the original hash, and never alter it | B | Must | 1 | US-05 | `test_increment1` |
| FR-14 | The system shall extract EXIF metadata from images and validate the declared extension against the file's magic bytes | B | Must | 1, 3 | US-06, US-25 | `test_increment1`, `test_increment3` |
| FR-15 | The system shall allow authorised roles to edit an item's title, description and category while leaving the file and its hashes immutable | A | Must | 1 | US-07 | `test_increment1` |
| FR-16 | The system shall record every custody transfer with the investigators involved, timestamp, location and reason | A | Must | 1 | US-08 | `test_increment1` |
| FR-17 | The system shall permit only the current holder or an administrator to transfer an item | A / Sec | Must | 1 | US-08 | `test_increment2` |
| FR-18 | The system shall record logins, failed attempts, CRUD operations, file access and data modifications with actor, IP address, timestamp and outcome | A | Must | 1 | US-09 | `test_increment1` |
| FR-19 | The system shall block updates and deletes on audit records at the ORM layer, so history cannot be rewritten | A | Must | 1 | US-09 | `test_increment1` |
| FR-20 | The system shall detect custody time-gaps above a configurable threshold, duplicate log entries, and role-permission mismatches | A | Should | 1 | US-10 | `test_increment1` |
| FR-21 | The system shall expose no public registration route; account creation shall require the Admin role | A / Sec | Must | 1 | US-11 | `test_increment1` |
| FR-22 | The system shall issue each new account a policy-checked strong password and a freshly generated Ed25519 key pair | B / Sec | Must | 1 | US-11 | `test_increment1` |
| FR-23 | The system shall sign every upload and transfer event with the outgoing investigator's private key over a canonical payload | B | Must | 2 | US-12 | `test_increment2` |
| FR-24 | The system shall make the digital-signature column non-nullable, so an unsigned custody record cannot exist | B / Sec | Must | 2 | US-12 | `test_increment2` |
| FR-25 | The system shall build the custody events of an item into a graph and traverse it from the upload root | C | Must | 2 | US-13 | `test_increment2` |
| FR-26 | The system shall subject each node to three checks — hash consistency, signature validity and strictly increasing timestamps — collecting all failures in a single pass | C | Must | 2 | US-13 | `test_increment2` |
| FR-27 | The system shall report a verdict of Intact, Partially Verified or Broken, with a completeness score, an ordered failure list and a verified timeline | C | Must | 2 | US-13 | `test_increment2` |
| FR-28 | The system shall define the evidence lifecycle as a transition table in which each transition carries a minimum role and a set of preconditions | C | Must | 2 | US-14 | `test_increment2` |
| FR-29 | The system shall reject an illegal transition with the exact unmet condition, and audit the rejection | C | Must | 2 | US-14 | `test_increment2` |
| FR-30 | The system shall require a justification for every successful transition and recalculate the item's risk score | C | Must | 2, 3 | US-14, US-18 | `test_increment2` |
| FR-31 | The system shall detect gaps between confirmed custody records and generate candidate filling records from the access log | C | Must | 2 | US-15 | `test_increment2` |
| FR-32 | The system shall select the most plausible candidate by best-first search above a threshold, marking the gap unresolved otherwise | C | Must | 2 | US-15 | `test_increment2` |
| FR-33 | The system shall label every link Confirmed, Inferred or Unresolved, and never present an inferred link as confirmed | C | Must | 2 | US-15 | `test_increment2` |
| FR-34 | The system shall present the verification result as a page showing verdict, completeness and failures, with a JSON endpoint | A | Should | 2 | US-16 | `test_increment2` |
| FR-35 | The system shall present the reconstruction result as a timeline distinguishing link types and showing each inference's reasoning | A | Should | 2 | US-17 | `test_increment2` |
| FR-36 | The system shall extract eight risk factors per item and normalise each with a curve suited to its distribution | C | Must | 3 | US-18 | `test_increment3` |
| FR-37 | The system shall combine the factors by a weighted sum amplified by interaction rules, with the total bonus capped | C | Must | 3 | US-18 | `test_increment3` |
| FR-38 | The system shall classify the final score into a level and accompany it with per-factor explanations and recommendations | C | Must | 3 | US-18 | `test_increment3` |
| FR-39 | The system shall allow an administrator to edit the factor weights and thresholds, re-normalising weights to sum to one and requiring strictly increasing thresholds | C / A | Should | 3 | US-19 | `test_increment3` |
| FR-40 | The system shall classify a natural-language question's intent among seven intents plus unknown | C | Must | 3 | US-20 | `test_intent_classifier` |
| FR-41 | The system shall retrieve database context for the question, scoped to the user's accessible cases | C / Sec | Must | 3, M1 | US-20, US-29 | `test_scoping` |
| FR-42 | The system shall degrade gracefully to a context-aware mock when no API key is configured or all candidate models fail | C | Must | 3 | US-20 | `test_increment3` |
| FR-43 | The system shall cross-check every case number, evidence identifier and investigator name in the model's reply against the retrieved context and warn on unknown references | C | Must | 3 | US-21 | `test_increment3` |
| FR-44 | The system shall build a six-dimensional feature vector per item and flag statistical outliers with an Isolation Forest | B | Could | 3 | US-22 | `test_increment3` |
| FR-45 | The system shall present anomaly results as "suggested for review" alongside the deterministic risk score, never as a confirmed judgement | B | Could | 3 | US-22 | `test_increment3` |
| FR-46 | The system shall provide a risk-ranked table, an anomaly view and a per-item risk detail page | A | Should | 3 | US-23 | `test_increment3` |
| FR-47 | The system shall support TOTP two-factor authentication, lock an account after five consecutive failures for a configured period, and time out idle sessions | B / Sec | Should | 3 | US-24 | `test_increment3` |
| FR-48 | The system shall encrypt stored evidence files with AES-256-GCM and store private keys encrypted under a derived key | B / Sec | Should | 3 | US-25 | `test_increment3` |
| FR-49 | The system shall produce a tamper-evident signed ZIP export of a case | B | Should | 3 | US-26 | `test_increment3` |
| FR-50 | The system shall produce a printable per-item PDF chain-of-custody report | B | Could | 3 | US-27 | `test_increment3` |
| FR-51 | The system shall compute every aggregate — counts, charts, rankings, exports — over only the cases the viewer may access | A / Sec | Must | M1 | US-28 | `test_scoping` |
| FR-52 | The system shall present each role a dashboard of panels matched to its work, and an explanatory message rather than a blank page when the user belongs to no case | A | Must | M1 | US-28 | `test_scoping` |
| FR-53 | The system shall answer identity questions ("who am I", "my cases") from the authenticated user | C | Must | M1 | US-29 | `test_intent_classifier` |
| FR-54 | The system shall tag stored conversation history with its owner and clear it on both login and logout | A / Sec | Must | M1 | US-29 | `test_scoping` |
| FR-55 | The system shall soft-delete evidence, preserving custody and audit history, and exclude deleted items from every listing | A | Must | M2 | D1 | `test_integration` |
| FR-56 | The system shall write an integrity status back to the evidence item after verification, so that a failed verification raises the item's risk | C | Must | M2 | D2 | `test_integration` |

**Summary:** 56 functional requirements — 27 delivered in Increment 1, 13 in Increment 2, 10 in Increment 3, and 6 across the two maintenance iterations, with several spanning more than one increment.

## 7.6 Non-Functional Requirements

Non-functional requirements are constraints on the services or functions offered by the system: timing constraints, constraints on the development process, standards, and similar. They describe *how the system behaves* rather than what it does. Crucially, a non-functional requirement that is not measurable is not verifiable, so each row below carries both a metric and a verification method.

**Table 7.6 — Non-functional requirements**

| ID | Requirement | Quality attribute | Metric / criterion | Increment | Verified by |
|---|---|---|---|---|---|
| NFR-01 | No user shall see case data outside their membership, in any view including aggregates, exports and AI answers | Security — confidentiality | Zero cross-case records returned in adversarial tests | 1, M1 | `test_scoping` (14 tests) |
| NFR-02 | Evidence content shall be verifiable against its intake hash at any time | Security — integrity | SHA-256 recomputation matches `original_hash` | 1, 2 | `test_increment2` |
| NFR-03 | Custody records shall be non-repudiable | Security — integrity | Ed25519 signature verifies against the signer's stored public key | 2 | `test_increment2` |
| NFR-04 | The record of what happened shall be complete and append-only | Auditability | UPDATE and DELETE on audit records raise at the ORM layer | 1 | `test_increment1` |
| NFR-05 | An unavailable external model shall not make the system unusable | Availability / robustness | Assistant returns a context-aware response with the service unreachable | 3, M2 | `test_increment3` |
| NFR-06 | A slow external call shall fail cleanly rather than hang the interface | Robustness | 20 s per-model timeout, 60 s total budget, 90 s browser abort | M1, M2 | Manual + configuration review |
| NFR-07 | Each role shall be presented an interface matched to its work | Usability | Four distinct dashboard compositions; no empty dashboard for any role | M1 | `test_scoping` |
| NFR-08 | A change shall be localisable to a single module wherever possible | Maintainability | Business logic contains no framework imports; routes contain no algorithms | 1 onward | Code review; Section 3.5 |
| NFR-09 | The persistence layer shall not be tied to one database engine | Portability | No engine-specific SQL in application logic; engine selected by one configuration value | 1 | Code review |
| NFR-10 | Integrity verification shall be linear in the size of the custody graph | Performance | *O(V + E)* established analytically | 2 | Section 11.7 |
| NFR-11 | Risk scoring shall be linear in the number of custody records for an item | Performance | *O(n)* established analytically | 3 | Section 11.7 |
| NFR-12 | Passwords shall meet a strength policy | Security — authentication | Minimum 12 characters, enforced at creation | 1, 3 | `test_increment3` |
| NFR-13 | Session cookies shall not be readable by scripts, shall be sent only over TLS, and shall resist cross-origin submission | Security — session | `HttpOnly`, `Secure`, `SameSite=Lax` set | 3 | Configuration review |
| NFR-14 | The application shall send content-security and complementary hardening headers | Security — defence in depth | CSP, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` present | M2 | Header inspection |
| NFR-15 | Untrusted text — user input and model output alike — shall never be rendered as markup | Security — injection | Output HTML-escaped before any formatting pass | M2 | Code review |
| NFR-16 | The system shall refuse to start in production with default secrets, and warn in development | Security — configuration | Production profile raises; development emits a startup warning | M2 | `test_*` output |
| NFR-17 | Listings shall remain responsive as data grows | Performance / robustness | Case and evidence listings paginated | M2 | Manual |
| NFR-18 | The automated test suite shall run without network access | Verifiability | 172 tests, no external calls, in-memory database per test | 3 onward | Suite execution |

## 7.7 Domain Requirements

Domain requirements are constraints imposed on the system by the domain of operation rather than by any stakeholder's preference. They are the requirements a customer will not think to state because, within the domain, they are assumed — and they are therefore the ones most often missed.

**Table 7.7 — Domain requirements arising from forensic practice**

| ID | Domain requirement | Origin in the domain | Consequence for the design |
|---|---|---|---|
| DR-01 | The chain of custody must be continuous: no period may exist in which no custodian is recorded | Admissibility doctrine | Custody entry created atomically with the evidence record; gaps detected and reported rather than ignored |
| DR-02 | Evidence content must be demonstrably unchanged from the moment of seizure | Admissibility doctrine | `original_hash` is immutable; verification recomputes rather than trusting a cached result |
| DR-03 | A custody record must identify who created it, in a way that person cannot later repudiate | Evidentiary standard | Ed25519 signature over a canonical payload; non-nullable signature column |
| DR-04 | The record of handling must survive the deletion of the item | Evidence of misconduct is itself evidence | Soft deletion throughout; custody and audit history never cascade-deleted |
| DR-05 | Only certain lifecycle transitions are legally meaningful, and some require preconditions | Forensic procedure | Formal state machine; archiving requires a passed integrity check |
| DR-06 | An item's handling must be reviewable by someone who did not handle it | Independent audit | Read-Only role with full visibility and no capability |
| DR-07 | An automated judgement must be distinguishable from a recorded fact | Evidentiary weight | Inferred custody links never presented as confirmed; anomaly output labelled "suggested for review" |

DR-07 deserves particular emphasis because it constrains the system in a way that a purely technical reading would miss. Two of the system's outputs — the reconstructed chain and the anomaly flags — are *inferences*, and presenting an inference with the same visual authority as a recorded fact would be a domain error even if the inference were usually right. This is why the reconstruction algorithm labels every link and why the Isolation Forest results carry a hedged caption.

## 7.8 System Requirements

**Table 7.8 — System requirements**

| Category | Requirement |
|---|---|
| Software — runtime | Python 3 |
| Software — framework | Flask (application factory pattern, ten blueprints) |
| Software — persistence | SQLAlchemy ORM over SQLite in development; PostgreSQL-ready |
| Software — cryptography | `hashlib` (SHA-256); `cryptography` (Ed25519, AES-256-GCM, Fernet) |
| Software — metadata | Pillow (EXIF); python-magic (magic-byte MIME detection) |
| Software — machine learning | scikit-learn (Isolation Forest) |
| Software — reporting | ReportLab (PDF generation) |
| Software — authentication | PyOTP (TOTP second factor); Flask-Login; Flask-WTF (CSRF); Flask-Limiter (rate limiting) |
| Software — external service | NVIDIA NIM inference API over an OpenAI-compatible HTTPS interface |
| Software — testing | pytest; pytest-cov |
| Hardware | Standard workstation; no specialised hardware required |
| Network | HTTPS on the application host; outbound HTTPS to the inference API (optional — the system degrades gracefully without it) |
| Storage | Local filesystem for encrypted evidence files; SQLite database file in WAL mode |

## 7.9 Constraints

**Table 7.9 — Project constraints and their design consequences**

| ID | Constraint | Type | Design consequence |
|---|---|---|---|
| C-01 | Single developer | Resource | Scrum ceremonies adapted to individual equivalents; velocity calibrated from one person's throughput |
| C-02 | One academic semester | Schedule | Three increments of fourteen working days; *won't-have* list used to protect the boundary |
| C-03 | The complex algorithms must be original work, not library calls | Academic | Category C features implemented from first principles; the boundary with Category B stated explicitly in Chapter 16 |
| C-04 | No paid infrastructure | Resource | SQLite rather than a hosted database; self-signed TLS; a free-tier inference endpoint with a mock fallback |
| C-05 | No external customer available for elicitation or acceptance | Requirements | Requirements derived by domain analysis and personas; validation performed against written acceptance criteria rather than customer sign-off |
| C-06 | The feature set must balance across three prescribed categories | Academic | Categorisation used as a completeness check during elicitation (Section 7.3), with the risk of distortion examined in Section 16.6 |

## 7.10 Feature Categorisation (A / B / C)

The coursework requires that functionality be categorised into three kinds and that the proposal be balanced across them. The categorisation was performed by assigning each feature to exactly one category **on the basis of where its essential difficulty lies**.

**Table 7.10 — The three categories and their criteria**

| Category | Definition | Test applied |
|---|---|---|
| **A — Data / repository** | Stores, retrieves, updates and deletes structured records, or computes straightforward formula-based values over them | Could this be expressed as a query plus a simple arithmetic or set operation? |
| **B — Third-party services** | Consumes an external library, API or pre-trained model as-is; the application invokes an interface but does not implement the underlying algorithm | Is the interesting work done by someone else's code? |
| **C — Complex application logic** | Algorithmically non-trivial and designed and implemented by the developer: a custom data structure, a multi-step algorithm with branching, or a heuristic search | Would removing the third-party calls still leave a substantial algorithm? |

**Table 7.11 — Feature allocation across the categories**

| Category | Features | Count |
|---|---|---|
| **A** | CRUD over six entities; case search and archiving; case-access membership; append-only audit trail; three formula checks (time-gap, duplicate entry, role mismatch); role-scoped aggregates and role-tailored dashboards; integrity and reconstruction report pages; soft deletion | 9 groups |
| **B** | SHA-256 (`hashlib`); Ed25519 signatures and AES-256-GCM encryption (`cryptography`); EXIF extraction (Pillow); magic-byte MIME detection (python-magic); ORM (SQLAlchemy); hosted LLM (NVIDIA NIM); Isolation Forest (scikit-learn); PDF generation (ReportLab); TOTP (PyOTP) | 9 |
| **C** | Graph integrity verification; multi-factor risk scoring; custody chain reconstruction; evidence lifecycle state machine; AI orchestration workflow with hallucination detection | 5 |

The **balance** is assessed in full in Chapter 16. In brief, the system is not top-heavy in any one category: the data layer is a six-entity model rather than a token database, the third-party integrations are numerous and varied rather than a single API call, and the complex-logic layer contributes five substantial algorithms rather than one.

The categorisation also produced a deliberate **integration between categories** that strengthens the design: the Category A formula checks feed the Category C risk scorer, so that the simple duplicate and role-mismatch computations become inputs to the complex scoring algorithm rather than sitting in isolation. That this integration was initially broken — and repaired as finding D5 in M2 — is recorded in Section 5.5.2.

Where a Category C feature calls a Category B library — the integrity verifier calls `hashlib` and the signature primitives, the assistant calls the language model — the library plays the role of a **primitive operation inside a larger algorithm** that the developer designed, in the same way that arithmetic operators are primitives inside a formula. The graph construction, the traversal, the multi-condition validation, the scoring, the search and the orchestration are the developer's own work.

## 7.11 Prioritisation and the Product Backlog

Requirements were prioritised using **MoSCoW**.

**Table 7.12 — MoSCoW allocation**

| Priority | Meaning | DEICMS content |
|---|---|---|
| **Must have** | Without it the system fails its core purpose | Authentication and access control; case and evidence CRUD; hashing; custody logging; the audit trail; digital signing; the graph integrity verifier; the state machine; the reconstruction algorithm; the risk scorer; the AI assistant with hallucination detection; both M1 change requests |
| **Should have** | Adds substantial value; the system remains coherent without any one | The formula checks; the two report interfaces; configurable risk weights; the dashboards; two-factor authentication and hardening; encryption at rest; the signed export |
| **Could have** | Genuinely optional enhancement | Isolation Forest anomaly detection; the PDF custody report |
| **Won't have this time** | Explicitly out of scope, recorded so the boundary is transparent | Production database deployment; public CA certificate; notifications; full-text search over evidence content; multi-language interface; mobile client; model fine-tuning; multi-tenant hosting |

Each backlog story carries acceptance criteria that make "done" objective, a MoSCoW priority, a story-point estimate, a feature-category tag, and the increment in which it was delivered. The full catalogue of twenty-nine stories — twenty-seven original plus the two M1 change-request stories — is reproduced in Appendix A. The second maintenance iteration's work is catalogued as defect findings (Table 5.9) rather than as backlog stories, because repairing a defect restores a requirement already accepted rather than introducing a new one.

The *Could have* tier is the sacrificial scope identified in risk R-04: had capacity fallen short, US-22 and US-27 were the two stories designated to be dropped. Neither was, but designating them in advance is what made the risk mitigable.

## 7.12 Requirements Validation and Traceability

**Validation** asks whether the requirements define the system the customer actually wants. Four checks were applied to every requirement.

**Table 7.13 — Validation checks**

| Check | Question | How applied |
|---|---|---|
| **Validity** | Does the system provide the functions that best support the customer's needs? | Each FR traces to a user requirement, which traces to a persona's stated responsibility |
| **Consistency** | Are there any requirement conflicts? | Checked at each increment planning; one conflict was found and resolved — FR-06 (Read-Only may not change state) against FR-30 (transitions require justification), resolved by giving Read-Only no available transitions at all rather than a rejected one |
| **Completeness** | Are all functions required by the customer included? | Checked against the five guarantees of Table 1.1 at each sprint review; the guarantee-to-increment mapping in Sections 5.1.4, 5.2.4 and 5.3.4 is that check's record |
| **Realism** | Can the requirements be implemented within budget and technology? | Story-point estimation against measured velocity; the 13-point estimate on US-13 is the record of a realism concern raised in advance |

**Traceability** is the property that each requirement can be followed forward to the design, code and test that satisfy it, and backward to the need that justifies it. The full traceability matrix is Appendix D; Table 7.5 above carries its forward direction inline.

Two **honest limitations** of the requirements process should be recorded.

First, **there was no external customer**, so validation was performed against written acceptance criteria rather than stakeholder sign-off. The developer wrote both the criteria and the code, which is a weaker form of validation than the process nominally implies. The mitigation applied was to write every acceptance criterion *before* implementation and to phrase it as an observable outcome rather than an implementation description, so that the criterion could not be quietly retro-fitted to whatever was built.

Second, **negative requirements were under-specified initially**. UR-18 and NFR-01 state what users must *not* see, but the original requirement set expressed this at the level of record access rather than as a property of every aggregate. The requirement was right; its scope of application was incomplete. This is precisely the gap that produced the M1 defects, and the lesson recorded in Section 5.4.6 — that a system with an access-control requirement needs adversarial tests — is at root a *requirements* lesson as much as a testing one: a negative requirement must enumerate the surfaces it governs, or it will be applied only to the surfaces its author had in mind.

## 7.13 Summary

This chapter established the requirements for DEICMS at both the user and system levels. Four personas were derived from the domain's four roles, each with an explicit statement of what it must *not* be able to do. Eighteen user requirements, fifty-six functional requirements, eighteen non-functional requirements, seven domain requirements and six constraints were specified in tabular form, with every functional requirement traced to its category, priority, increment, user story and verifying test module. The three-way feature categorisation was defined by the test applied to each feature, and the deliberate integration between Category A formulas and the Category C risk scorer was noted. MoSCoW prioritisation identified the sacrificial scope in advance. Validation was assessed against validity, consistency, completeness and realism, and two limitations of the process were recorded — the absence of an external customer, and the under-specification of negative requirements that led directly to the M1 defects.

The next chapter turns these requirements into models.

---

\newpage
