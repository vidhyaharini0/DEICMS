# Part II — Increment 1: Core Case & Evidence Management

---

## 5. Increment 1 Planning

### 5.1 Sprint Goal

The goal of the first increment was to build the foundation on which everything else would stand: a working evidence repository in which investigators log in, manage cases, register hashed evidence, and have every action recorded in a tamper-evident trail. Expressed as a single sentence, the sprint goal was *"an authenticated, role-aware system in which cases and evidence can be managed and every action is audited."* Nothing in this increment is algorithmically complex — that is by design. The increment exists to make the later algorithms possible by giving them a concrete, stable data model and a body of real records to operate on, and to retire the routine-but-numerous risks of authentication, authorisation, file handling, and persistence before the harder work begins.

The increment was budgeted at **forty story points** across eleven user stories, planned over a fourteen-working-day cycle. The stories, their categories, priorities, and point estimates are listed in Table 5.1, and each is elaborated with its acceptance criteria in Section 5.2.

**Table 5.1 — Increment 1 sprint backlog**

| ID | User story | Category | MoSCoW | Points |
|---|---|---|---|---|
| US-01 | Secure login and logout | A / Security | Must | 3 |
| US-02 | Role-based access control | A | Must | 5 |
| US-03 | Case CRUD, search and archive | A | Must | 5 |
| US-04 | Upload and register evidence | A | Must | 5 |
| US-05 | SHA-256 fingerprint at upload | B | Must | 2 |
| US-06 | EXIF / MIME metadata extraction | B | Must | 3 |
| US-07 | Edit and categorise evidence | A | Must | 3 |
| US-08 | Record custody transfers and access events | A | Must | 5 |
| US-09 | Append-only audit trail | A | Must | 5 |
| US-10 | Formula-based audit checks | A | Should | 3 |
| US-11 | Admin-only account creation | A | Must | 1 |

### 5.2 User Stories and Acceptance Criteria

The eleven stories are stated below with the acceptance criteria that made "done" objective. The criteria are drawn from the product backlog and are the same criteria against which the increment was reviewed.

**US-01 — Secure login and logout (3 points).** *As an investigator, I want to log in with my credentials and be logged out when idle, so that only authorised people can access evidence data.* The story is satisfied when valid credentials open an authenticated session and invalid ones are rejected without revealing whether the email or the password was wrong; when passwords are stored only as salted hashes and never in plaintext; when a session expires after a configurable period of inactivity through a sliding timeout; and when every login, logout, and failed attempt is written to the audit trail.

**US-02 — Role-based access control (5 points).** *As an administrator, I want each account to hold exactly one of four roles, so that permissions match responsibilities.* The story is satisfied when every account holds one of Admin, Lead Investigator, Analyst, or Read-Only; when each route enforces the minimum role required and unauthorised access is redirected with an explanatory message rather than silently failing; when a Read-Only user cannot trigger any state-changing action; and when role changes are themselves restricted to administrators and recorded in the audit trail.

**US-03 — Case CRUD, search and archive (5 points).** *As a lead investigator, I want to create, search, update, and archive cases, so that investigations are tracked from opening to closure.* The story is satisfied when a case carries a unique case number, a title, a jurisdiction, a status, and timestamps; when cases can be filtered by status and searched; when archiving is a soft operation that never physically deletes case data; and when case membership, recorded in the Case Access table, controls which investigators can see the case.

**US-04 — Upload and register evidence (5 points).** *As an investigator, I want to upload a digital file and register it as an evidence item within a case, so that it enters a managed chain of custody.* The story is satisfied when upload accepts only allow-listed file types and rejects everything else; when a unique evidence number is generated and the uploader becomes the item's first custodian; and when an initial custody-log entry is created atomically with the evidence record so that no item can exist without a custody history.

**US-05 — SHA-256 fingerprint at upload (2 points).** *As an investigator, I want every uploaded file fingerprinted with SHA-256, so that any later modification is detectable.* The story is satisfied when an original hash is computed at upload and never changed thereafter, when a current hash tracks the latest verified state, and when the hash is displayed on the evidence page and recorded in the initial custody entry.

**US-06 — EXIF / MIME metadata extraction (3 points).** *As an analyst, I want metadata extracted automatically, so that provenance details are preserved without manual entry.* The story is satisfied when EXIF fields are extracted from images and stored, and when the declared file extension is validated against the file's actual magic bytes, with full rejection of content-type mismatches deferred to the hardening story in Increment 3 but the extraction and detection in place here.

**US-07 — Edit and categorise evidence (3 points).** *As an investigator, I want to edit evidence metadata and assign a category, so that items stay accurate and findable.* The story is satisfied when the title, description, and category of an item are editable by authorised roles, when edits are audited, and when the file itself and its hashes remain immutable through the editing path.

**US-08 — Record custody transfers and access events (5 points).** *As an investigator, I want every hand-off and access recorded with who, when, where, and why, so that the chain of custody is complete.* The story is satisfied when a transfer records the investigators it moves between, its timestamp, its location, and its reason; when only the current holder or an administrator can transfer an item; and when the custody log is viewable per item in chronological order. (Digital signing of these events is a Category B/C concern delivered in Increment 2; this story delivers the record itself.)

**US-09 — Append-only audit trail (5 points).** *As an auditor, I want every significant event logged immutably, so that activity can be reviewed after the fact.* The story is satisfied when logins, failed attempts, CRUD operations, file access, and data modifications are recorded with the actor, the originating IP address, a timestamp, and an outcome; when updates and deletes on audit records are blocked at the ORM layer so the history cannot be rewritten; and when trails can be filtered per evidence item and per investigator.

**US-10 — Formula-based audit checks (3 points).** *As an auditor, I want automatic checks for custody time-gaps, duplicate entries, and role mismatches, so that obvious irregularities surface without manual review.* The story is satisfied when gaps between consecutive custody transfers above a configurable threshold are flagged, when duplicate log entries sharing investigator, evidence, and timestamp are detected by query, and when accesses by an investigator whose role is not permitted for the evidence category are detected by a single lookup.

**US-11 — Admin-only account creation (1 point).** *As an administrator, I want to be the only one who can create investigator accounts, so that no one can self-register into an evidence system.* The story is satisfied when no public registration route exists, when the account-creation route requires the Admin role, and when each new account is issued a role, a policy-checked strong password, and a freshly generated Ed25519 key pair.

### 5.3 Increment 1 UML Artefacts

The increment produced three UML artefacts, each addressing a different view of the foundation. The **use-case diagram** (Figure 6.1) captures the actors and the actions available to each, showing how the four investigator roles and the external authenticator relate to the system's use cases and how higher roles inherit the capabilities of lower ones. The **class diagram** (Figure 6.2) captures the static structure — the six entity classes with their attributes and methods, together with the logic-layer modules — and is the reference for the implementation that follows. The **entity-relationship diagram** (Figure 4.3) captures the database schema in detail, including the field types and the relationships that encode the domain rules. These three artefacts are discussed in the next chapter as the design that the implementation realises.

---

## 6. Analysis and Design

### 6.1 Use-Case Analysis

The use-case diagram frames the system from the outside, in terms of what each actor can accomplish. Four human actors correspond to the four roles, and a fifth actor — the authenticator application that provides TOTP codes — appears because two-factor authentication involves an external party. The diagram's organising principle is *capability inheritance*: the Read-Only auditor can view cases, evidence, custody logs, and audit trails; the Analyst can do all of that and additionally analyse evidence, run integrity checks, and use the assistant; the Lead Investigator can do all of that and additionally create and manage cases, manage members, upload and transfer evidence, and export packages; and the Administrator can do everything, plus manage accounts. Several use cases are marked with `«include»` relationships to sub-use-cases they always entail — logging in includes verifying a TOTP code when two-factor authentication is enabled, uploading evidence includes validating the file type, and transferring custody includes signing the event — which makes explicit that these are not optional add-ons but integral parts of the parent action. Modelling the roles this way at the analysis stage directly informed the authorisation design: because capabilities strictly nest, the implementation could express most authorisation as a minimum-role check rather than a per-action access matrix.

### 6.2 Static Design: the Class Model

The class diagram realises the six entities as classes. The **Investigator** class carries the identity and credential attributes and a cluster of methods that encapsulate account behaviour — password setting and checking, the role predicates (`is_admin`, `can_manage`, `can_analyse`), the lockout logic, and the two-factor predicate — so that authorisation questions are answered by asking the object rather than by scattering role comparisons through the routes. The **Case**, **Evidence Item**, **Custody Log**, and **Audit Record** classes are primarily data-carrying, with the Evidence Item as the richest because it is the system's central object. The **Case Access** class is the association class that implements case-level authorisation, and it carries the small set of static helper methods — `get_permission`, `can_access`, `can_manage_members`, `grant`, and (added later) `accessible_case_ids` — through which every case-scoped decision in the system is made. Alongside the entities, the class diagram shows the logic-layer modules that the later increments fill in, so that the single diagram serves as a map of the whole codebase; in Increment 1 the relevant ones are the cryptographic key-generation helpers and the password validator.

A design decision visible in this model is the deliberate placement of behaviour on the Investigator class rather than in the authentication routes. Concentrating the role predicates and the lockout logic on the entity means that the same question — may this user manage cases? is this account locked? — is answered identically wherever it is asked, which is both a correctness property and a maintainability one. The alternative, comparing role strings inline in each route, would have scattered the authorisation policy across the codebase and made it impossible to change in one place.

### 6.3 Data Design: the Entity-Relationship Model

The entity-relationship diagram gives the schema at the level of columns, types, keys, and cardinalities, and it is the authoritative reference for the persistence layer. Its structure was described in Section 4.4; what matters at the design stage of this increment is the set of decisions it records. Each entity has a surrogate integer primary key and, where the domain has a natural identifier, a separate unique business key — the case number, the evidence number, the investigator email — so that the human-facing identifier can be formatted and validated independently of the database key. Foreign keys implement the relationships: an evidence item references its case, custody logs and audit records reference the evidence and investigators they concern, and the case-access rows reference both a case and an investigator. Two of the Evidence Item columns shown in the diagram — the integrity status and the soft-delete flag — were added after the original schema, during the maintenance work, and the diagram marks them accordingly; they are mentioned here because the entity-relationship diagram is a living artefact that was kept in step with the schema as it evolved rather than frozen at the moment of first design.

The schema evolution itself was handled by a lightweight idempotent migration routine that runs at application startup, inspecting the existing columns and adding any that are missing. This is a pragmatic alternative to a full migration framework, appropriate to a single-developer academic project, and it means that a database created under an earlier version of the schema is brought up to date automatically rather than having to be rebuilt — a small but real piece of engineering that keeps the persisted data and the evolving model consistent.

---

## 7. Implementation

### 7.1 Authentication and Session Management

Authentication is implemented on Flask-Login. The login route verifies the submitted credentials against the stored hash, and on success establishes a session, records a login event in the audit trail, and — if the account has two-factor authentication enabled — first diverts through a one-time-password verification step before completing the login. The deliberate refusal to reveal whether a failed login was due to an unknown email or a wrong password, satisfying US-01's acceptance criterion, is a small but important design choice that denies an attacker the ability to enumerate valid accounts. Sessions are governed by a sliding idle timeout implemented as a `before_request` hook that records the time of each request and logs the user out if the gap since the previous activity exceeds the configured limit, on the next request after the limit is passed. Every authentication event — success, failure, and logout — is written to the audit trail, so that the record of who accessed the system and when is as complete as the record of what they did to evidence.

### 7.2 Role-Based Access Control

Authorisation rests on the four-role model and is enforced at two granularities. The coarser granularity is the role check: each route that requires elevated privilege calls the relevant predicate on the current user — `is_admin` for administration, `can_manage` for case and evidence management, `can_analyse` for analytical actions — and redirects with an explanatory flash message if the check fails. Because the roles' capabilities strictly nest, as the use-case analysis established, these predicates express the whole role policy in three methods on the Investigator class. The finer granularity is case-level access, implemented by the Case Access table and its helper methods; in Increment 1 this governs which cases appear in a user's case list and which a user may open, and in later work it is extended to every aggregate view. Keeping the two granularities distinct — role for *what kind of action* and case membership for *which data* — is what allows the system to express, for example, that an Analyst may analyse evidence (a role capability) but only within the cases they belong to (a membership constraint).

### 7.3 Case Management

The case routes implement the full create-read-update-archive lifecycle. A new case is assigned a generated case number of the form `CASE-<year>-<nnn>`, where the sequence number is derived from the current case count; because deletion in the system is soft, the count does not decrease when cases are archived, so this simple scheme remains collision-free in normal single-user operation, though it is acknowledged as a point that a concurrent multi-user deployment would need to strengthen. The case list is scoped to the requesting investigator's memberships — administrators see all cases, everyone else sees only the cases they belong to — and is paginated so that the view stays responsive as the case count grows. Opening a case is guarded by a case-access check, and the case view lists the case's evidence items, filtered to exclude any that have been soft-deleted. Archiving sets the case status without removing any data, honouring the soft-delete philosophy that pervades the system.

### 7.4 Evidence Registration, Hashing and Metadata

The evidence-upload route is where several of the increment's stories converge. A submitted file is first checked against the allow-list of permitted extensions and rejected if it does not match. Its bytes are then hashed with SHA-256 to produce the original fingerprint that will serve as the ground truth for all future integrity checks, and this same value initialises the current hash. Metadata is extracted — EXIF fields from images through Pillow, and the true MIME type through python-magic — and stored alongside the item. The file is written to the uploads area and, from Increment 3 onward, encrypted at rest. An evidence record is created with a generated evidence number, its category and initial lifecycle state, the uploader as both creator and current holder, and the extracted metadata; and, crucially, an initial custody-log entry of type *Upload* is created in the same transaction, so that the invariant "every evidence item has a custody history from the moment it exists" holds without exception. A corresponding audit record is written. The SHA-256 fingerprinting (US-05) and the metadata extraction (US-06) are the increment's two Category B features: the application calls `hashlib` and the metadata libraries but implements neither hashing nor EXIF parsing itself, and the report is careful to claim only the surrounding registration logic as its own.

### 7.5 The Custody Log

Custody events are recorded in the Custody Log table, which in this increment captures uploads and the manual transfers introduced by US-08. A transfer records the outgoing and incoming investigators, a timestamp, a location, and a reason, and it is permitted only to the item's current holder or an administrator, enforcing the rule that one cannot hand off what one does not hold. The custody log for an item is presented in chronological order, giving the human-readable chain of custody that the whole system exists to protect. The cryptographic signing of these events, which turns the record from a claim into a non-repudiable proof, is deferred to Increment 2; what this increment establishes is the complete, ordered record itself, and the discipline that no custody event is ever created outside this log.

### 7.6 The Append-Only Audit Trail

The audit trail is the system's memory, and its defining property is that it cannot be rewritten. This is enforced not by convention but at the ORM layer: SQLAlchemy event listeners on the Audit Record model intercept any attempt to update or delete an audit record and raise an error, so that the append-only guarantee is a property of the data-access layer rather than something each route must remember to respect. Every significant event across the system writes an audit record carrying the event type, the acting investigator, the evidence and case it concerns where applicable, the originating IP address, an outcome of success, failure, or warning, and a timestamp. The trail can be viewed per evidence item and per investigator by authorised users, and in full by administrators. Building this in Increment 1, and wiring the audit writes into each route as the route was written rather than retrofitting them later, meant that the system had a complete history from its first increment — a decision that the retrospective identifies as one of the increment's better ones.

### 7.7 Formula-Based Audit Checks

The three formula checks are the increment's clearest example of Category A "formula" functionality: each is a direct computation over database fields rather than an algorithm. The time-gap check walks an item's custody entries in order and flags any interval between consecutive transfers that exceeds a configurable threshold, defaulting to seventy-two hours, because an unexplained gap in custody is exactly the kind of irregularity that undermines admissibility. The duplicate-entry check finds custody records that share the same event type, the same pair of investigators, and the same timestamp, a pattern indicative of accidental double-recording or deliberate log injection. The role-mismatch check compares the role of an investigator who accessed an item against the roles permitted for that item's category, flagging accesses that fall outside the permitted set. In Increment 1 these checks are exposed through a JSON endpoint for on-demand inspection; a later design decision, made during the maintenance work, wires the duplicate and role-mismatch checks directly into the risk scorer so that these simple Category A computations become inputs to the complex Category C algorithm — an integration discussed in Part IV.

### 7.8 Administrative Account Creation

Because a forensic system must never permit self-registration, account creation is an administrative action. The public registration route that a conventional web application would offer does not exist; instead, the administration blueprint provides an account-creation route guarded by the Admin role. Creating an account validates the requested password against the strength policy — a minimum of twelve characters with upper- and lower-case letters, a digit, and a special character — generates a fresh Ed25519 key pair, stores the public key and the encrypted private key, and records the creation in the audit trail. The password policy is enforced through a small dedicated validator module that returns a list of human-readable rule violations, so that the same policy is applied identically wherever a password is set.

---

## 8. Testing

Increment 1 was validated by the unit and integration tests in the increment's test module together with the cryptographic and formula tests that accompanied it. The tests exercise the entities and their relationships, the role predicates, the case and evidence CRUD paths, the hashing and the initial custody-entry invariant, the append-only enforcement on audit records, and the three formula checks. The testing approach at this stage was primarily example-based: for each acceptance criterion, a test constructs the minimal set of records needed to exercise it and asserts the expected outcome — that an unauthorised role is redirected, that a soft-archived case retains its data, that an audit record cannot be updated, that a seventy-two-hour gap is flagged while a shorter one is not. Building this test module in the first increment established the fixtures and patterns — an in-memory database per test, helper functions to create investigators and cases — that every later test module reused, which is a large part of why the later increments could be tested so much more cheaply. The full testing strategy across all increments, and the final coverage figures, are consolidated in Part VI.

---

## 9. Sprint Review, Burndown and Retrospective

### 9.1 Sprint Review

At the review, all eleven stories were demonstrated against their acceptance criteria and all forty story points were accepted. The increment delivered a system that could be logged into, that enforced its four roles and case memberships, that managed cases and registered hashed evidence with extracted metadata, that recorded custody and audited every action immutably, and that ran the three formula checks. In terms of the five guarantees of the problem statement, Increment 1 fully delivered the tamper-evident complete record and case-scoped access, laid the foundation for provable integrity by capturing the intake hash and the ordered custody log, and left the enforcement of procedural rules and the analytical prioritisation to the increments designed for them.

### 9.2 Burndown

The burndown chart for the increment (Figure 9.1) plots the ideal and actual story points remaining across the fourteen-day cycle. The actual line runs above the ideal for the first several days: days zero to two produced no burned points at all, because environment setup — the Flask application factory, the SQLAlchemy configuration, and the Git repository — took longer than planned and the first story was not completed until day two. From about day nine the actual line converges back toward the ideal, and all forty points were delivered by day fourteen. The chart's shape is therefore a slow start followed by a recovery, and the annotation on the chart records exactly this.

### 9.3 Retrospective

The retrospective drew three conclusions. What went well was the choice of the application-factory pattern, which made the system testable from the very first week and paid for the small up-front cost many times over, and the decision to write the audit-trail hooks into each route as the route was built rather than in a separate later pass, which meant the system was never without a complete history. What went less well was the zero-burn start: the environment and scaffolding work was real work that had not been represented as points, so the burndown looked alarming before it looked healthy, and the estimate for the routine CRUD-and-template work had been slightly optimistic. The concrete actions carried into Increment 2 were two: to reserve the first day of the next increment explicitly for a design spike on the graph integrity algorithm, whose thirteen-point estimate reflected real uncertainty, and to fix the canonical format of the data that custody signing would sign *before* writing any signing code, so that the signer and the verifier could not disagree about what bytes were signed. Both actions, as the Increment 2 chapter records, proved to be well judged.

*[End of Part II]*
