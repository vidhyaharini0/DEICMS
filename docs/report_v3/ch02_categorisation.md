# Chapter 2 - Feature Categorisation and Balance

---

DEICMS delivers forty-six functionalities across three categories: data and
repository operations, third-party services, and complex application logic
designed and implemented within the project. The sections below list them,
motivate each categorisation, and assess the resulting balance.

## 2.1 The Three Categories

**Table 2.1 - Category definitions and the test applied to each functionality**

| | Category | Definition | Test applied |
|---|---|---|---|
| **A** | Data / repository / DB-oriented | CRUD operations, formulae | Is the behaviour obtained by storing, retrieving or arithmetically combining records? |
| **B** | Third-party services | Libraries, APIs, tools, pre-trained models | Is the behaviour obtained by calling something that implements it? |
| **C** | Complex application logic | Algorithm and workflow mostly implemented by the author; may exploit third-party services inside an elaborated logic | Does the behaviour require a data structure, control flow or search that this project designed? |

A pre-trained model is a third-party service unless the project builds a
substantial workflow around the information it produces. That rule governs two
decisions here, and it is applied in both directions:

- The language model is **B**; the six-stage pipeline around it is **C**
  (Section 11.6).
- The Isolation Forest is **B**, although it feeds the same dashboard as a
  Category C algorithm, because the library implements the detection itself.

The decisive question is not whether a functionality calls a library, but
whether replacing that library with an equivalent would require any of the
project's own design to change. For the hash function inside the integrity
verifier it would not, so the verifier is C. For the Isolation Forest it
would, so it is B.

## 2.2 Category A - Data, Repository and Formula Functionalities

Thirty functionalities. The complexity here lives in the data model and its
constraints, not in any algorithm.

**Table 2.2 - Category A functionalities**

| # | Functionality | Entity | Realises |
|---|---|---|---|
| A1 | Create an investigation | Case | SR-07 |
| A2 | Search and list investigations | Case | SR-07 |
| A3 | Amend an investigation | Case | SR-07 |
| A4 | Close an investigation without data loss | Case | SR-08 |
| A5 | Confine the investigation list to the viewer's memberships | Case, CaseAccess | SR-09 |
| A6 | Register an exhibit | EvidenceItem | SR-10, SR-11 |
| A7 | Amend an exhibit's description and classification | EvidenceItem | SR-15 |
| A8 | Classify an exhibit by kind | EvidenceItem | SR-15 |
| A9 | Remove an exhibit without destroying its history | EvidenceItem | SR-55 |
| A10 | Create an investigator account | Investigator | SR-21 |
| A11 | Assign and change an account's function | Investigator | SR-04 |
| A12 | Suspend and restore an account | Investigator | SR-04 |
| A13 | Release a locked account | Investigator | SR-47 |
| A14 | List accounts | Investigator | SR-04 |
| A15 | Record a custody handover | CustodyLog | SR-16 |
| A16 | Record an access event | CustodyLog | SR-16 |
| A17 | Restrict handover to the present custodian | CustodyLog | SR-17 |
| A18 | View an exhibit's custody log | CustodyLog | SR-16 |
| A19 | Record system events with actor, origin, moment, outcome | AuditRecord | SR-18 |
| A20 | Record integrity-check outcomes | AuditRecord | SR-18 |
| A21 | View the audit trail per exhibit | AuditRecord | SR-18 |
| A22 | View the global audit trail (administrator) | AuditRecord | SR-18 |
| A23 | Grant case membership | CaseAccess | SR-09 |
| A24 | Revoke case membership | CaseAccess | SR-09 |
| A25 | **Formula:** interval between consecutive handovers above a threshold | CustodyLog | SR-20 |
| A26 | **Formula:** repeated log entries by actor, exhibit and moment | CustodyLog | SR-20 |
| A27 | **Formula:** acts inconsistent with the actor's function | AuditRecord | SR-20 |
| A28 | Scoped aggregates: counts, charts, rankings | all | SR-51 |
| A29 | Role-composed overview with an explanatory empty state | all | SR-52 |
| A30 | Paginated listings | Case, EvidenceItem, AuditRecord | SR-57 |

**Motivation.** Every row is a persistence operation or arithmetic over stored
fields. A25 to A27 are formula-based checks: timestamp subtraction against a
configurable threshold, equality over three columns, and set membership of a
function in a permitted list. None requires a data structure or a search, and
none is therefore classified as C.

## 2.3 Category B - Third-Party Services

Eleven integrations, consumed as they are.

**Table 2.3 - Category B functionalities**

| # | Functionality | Component | What it provides | What this project supplies |
|---|---|---|---|---|
| B1 | Content fingerprinting | Hash library | The digest function | When to compute it, and what to compare it with |
| B2 | Custody-record signing | Signature library | Key generation, sign, verify | The canonical payload and when to sign |
| B3 | Embedded metadata extraction | Imaging library | EXIF parsing | Which fields to keep and persist |
| B4 | Content-type detection | Magic-byte library | Type identification from bytes | The allow-list and the refusal policy |
| B5 | Object-relational mapping | ORM | Mapping and query generation | The schema and its constraints |
| B6 | Natural-language generation | Hosted language model | The sentence | Everything around it (Section 11.6) |
| B7 | Statistical outlier detection | Isolation Forest | **The algorithm itself** | The feature vector only |
| B8 | Printable report generation | PDF library | Layout and serialisation | The report's content and structure |
| B9 | Content encryption at rest | Cryptography library | The cipher | What to encrypt, and key handling |
| B10 | Second-factor codes | TOTP library | Code generation and validation | Enrolment and the lockout policy |
| B11 | Request rate limiting | Limiter | Counting and refusal | Which endpoints, and at what rates |

**Motivation.** In every row the behaviour named in column three is
implemented elsewhere. B7 warrants particular note: anomaly detection appears
in the interface beside a Category C algorithm, but the library implements the
detection and the project supplies only the feature vector, so it is
classified B.

## 2.4 Category C - Complex Application Logic

Five algorithms, each designed and implemented within the project. Chapter 11
gives each a full section with pseudocode, UML behavioural diagrams,
complexity analysis and the design decision that defines it; the motivation
for each categorisation is summarised below.

**Table 2.4 - Category C functionalities, with motivation**

| # | Algorithm | What makes it complex | Why not A | Why not B |
|---|---|---|---|---|
| **C1** | **Chain integrity verification** (§11.2) | Builds a directed acyclic graph of custody events and traverses it depth-first, applying three independent checks at every node and **accumulating all failures in one pass** rather than halting at the first | No query answers "where and in what way is this chain unsound"; the predecessor relation and the branching are structure, not rows | Hash and signature libraries are used as primitive operations inside the traversal; replacing either changes nothing in the design |
| **C2** | **Multi-factor risk assessment** (§11.3) | Eight indicators, each normalised by a curve chosen for its own distribution, combined by weighted sum, amplified by five interaction rules, with the total amplification capped | A weighted sum is arithmetic; the per-indicator normalisation choice, the interaction model and the cap are design | No library models this domain's notion of risk |
| **C3** | **Custody chain reconstruction** (§11.4) | Heuristic best-first search: detects discontinuities, generates candidates, scores each on four criteria, selects above a threshold and **declines below it** | There is no correct answer to retrieve; the algorithm evaluates possibilities and reports confidence | No library infers missing custody |
| **C4** | **Evidence lifecycle state machine** (§11.5) | A formal automaton declared as data: six states, fourteen transitions, each gated by permitted function and preconditions, with a four-gate validation pipeline and audited refusals | A status column is data; a role-gated, precondition-constrained automaton with explained refusals is control | No library knows this domain's procedure |
| **C5** | **Assistant orchestration** (§11.6) | Six stages: intent classification over seven intents, **access-scoped** retrieval, template selection, budgeted invocation with fallback, context-only degradation, and reference validation against the retrieved records | Retrieval is queries; the pipeline that decides what to retrieve and what to do with the answer is not | **The model is B.** The pipeline is C, and the substitution of one model for another changed no stage, no requirement and no test |

C5 is the workflow built around a pre-trained model, and C1 is invoked
**inside** it: an integrity question causes the assistant to run a fresh
verification and include its result in the retrieved context. Two Category C
algorithms compose, with a Category B model producing only the final sentence.

## 2.5 Balance Across the Three Categories

Counting functionalities alone is misleading: thirty CRUD operations are not
thirty times the work of one graph algorithm. Balance is therefore assessed on
four measures.

**Table 2.5 - Balance across four measures**

| Measure | A | B | C | Reading |
|---|---|---|---|---|
| Functionalities | 30 (66%) | 11 (24%) | 5 (11%) | A dominates by count, as CRUD always will |
| System requirements | 30 (50%) | 11 (18%) | 19 (32%) | C requires three to four requirements each |
| **Story points** (130 planned) | 47 (36%) | 27 (21%) | **56 (43%)** | **C is the largest share of estimated effort** |
| **Source lines** (4,711) | 2,302 (49%) | 439 (9%) | **1,970 (42%)** | C is 4.5 times the size of B |

**Table 2.6 - Category C by module**

| Module | Lines | Algorithm |
|---|---|---|
| `ai_assistant.py` | 662 | C5 |
| `risk_scoring.py` | 445 | C2 |
| `chain_reconstruction.py` | 331 | C3 |
| `graph_integrity.py` | 323 | C1 |
| `state_machine.py` | 209 | C4 |
| **Total** | **1,970** | |

The whole of Category B is **439 lines**, less than any two Category C modules
combined.

The distribution is balanced by effort rather than by count. Category A is
the largest by functionality count, as it will be in any system with a
substantial data model; Category C is the largest by estimated effort and
nearly the largest by code size; Category B is the smallest by both measures.

## 2.6 Functionality Added After Assessment

Functionality was added to a thin category on two occasions.

**Table 2.7 - Functionality added after a balance assessment**

| When | Category found thin | Added | Effect |
|---|---|---|---|
| Proposal revision, before implementation | **C** - the first draft offered rule-based checks that were really formulae in disguise | C1, C2 and C3 replaced them; C4 and C5 were re-argued at the level of their workflow rather than their output | C went from a contested claim to five defensible algorithms |
| Sprint 6, after a specification audit | **A and the quality attributes** - enforcement existed but was unverified | A30 (paginated listings) implemented; 21 system quality requirements given measurements, acceptance criteria and tests | 8 of 18 quality requirements verified became 21 of 21 |

The first is the more substantial. An earlier draft of the proposal classified
a set of threshold checks over stored fields as complex logic. On review they
were re-categorised as Category A formulae, where they remain as A25 to A27,
and three algorithms were designed to occupy Category C in their place.

## 2.7 Mapping to the Delivery Sequence

**Table 2.8 - Category by sprint**

| Sprint | A | B | C | Character |
|---|---|---|---|---|
| 1 - Foundation | 35 pts | 5 pts | - | The data layer the algorithms operate on |
| 2 - Integrity | 4 pts | 5 pts | **29 pts** | C1, C3, C4 |
| 3 - Assessment | 3 pts | 17 pts | **22 pts** | C2, C5, plus most third-party work |
| 4 (M1) - Scoping | 5 pts | - | 5 pts | Access scoping, including inside C5 |
| 5 (M2) - Defects | - | - | - | Eleven findings, no new scope |
| 6 (M3) - Quality | 23 pts | - | - | Verification of what the other five built |

Category A comes first because the algorithms require records to operate on;
Category C is concentrated in Sprints 2 and 3; Category B is spread across
both, each integration attaching to the feature that needs it. Section 4.4.1
gives the four rules that produced this ordering.

---

\newpage
