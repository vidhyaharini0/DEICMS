# Chapter 15 - Appendices

---

## Appendix A - Complete User Story Cataloge

Thirty-six stories, 153 points. Ranking within a sprint follows the four rules
of Section 4.4.1. Acceptance criteria are given in the sprint chapters.

| ID | Title | Cat | MoSCoW | Pts | Sprint |
|---|---|---|---|---|---|
| US-01 | Secure sign-in | A | Must | 3 | 1 |
| US-02 | Access limited by function | A | Must | 5 | 1 |
| US-03 | Open, find and close investigations | A | Must | 5 | 1 |
| US-04 | Register an exhibit | A | Must | 5 | 1 |
| US-05 | Fingerprint at intake | B | Must | 2 | 1 |
| US-06 | Content checked against declared type | B | Must | 3 | 1 |
| US-07 | Describe and classify an exhibit | A | Must | 3 | 1 |
| US-08 | Record every handover | A | Must | 5 | 1 |
| US-09 | Unalterable history | A | Must | 5 | 1 |
| US-10 | Surface handling anomalies | A | Should | 3 | 1 |
| US-11 | Administrator-only account creation | A | Must | 1 | 1 |
| US-12 | Attributable custody records | B | Must | 5 | 2 |
| US-13 | Verify the whole custody history | **C** | Must | **13** | 2 |
| US-14 | Exhibits move only as permitted | **C** | Must | 8 | 2 |
| US-15 | Reconstruct missing custody links | **C** | Must | 8 | 2 |
| US-16 | Read a verification result | A | Should | 2 | 2 |
| US-17 | Read a reconstruction | A | Should | 2 | 2 |
| US-18 | Exhibits ranked by attention needed | **C** | Must | 8 | 3 |
| US-19 | Tune what counts as risky | **C**/A | Should | 3 | 3 |
| US-20 | Ask questions in ordinary language | **C** | Must | 8 | 3 |
| US-21 | Unsupported statements flagged | **C** | Must | 3 | 3 |
| US-22 | Statistical outliers surfaced | B | Could | 5 | 3 |
| US-23 | Ranked and anomalous views | A | Should | 3 | 3 |
| US-24 | Second factor and lockout | B | Should | 5 | 3 |
| US-25 | Evidence unreadable without authorization | B | Should | 3 | 3 |
| US-26 | Verifiable export | B | Should | 2 | 3 |
| US-27 | Printable custody report | B | Could | 2 | 3 |
| US-28 | Scoped aggregates | A | Must | 5 | 4 |
| US-29 | Scoped assistant | **C** | Must | 5 | 4 |
| US-30 | Quality requirements carry measurements | A | Must | 5 | 6 |
| US-31 | Transport and session hardening verified | A | Must | 3 | 6 |
| US-32 | Unsafe configuration refused and exercised | A | Must | 3 | 6 |
| US-33 | Listings bounded as data grows | A | Must | 3 | 6 |
| US-34 | Algorithmic cost measured | **C** | Must | 5 | 6 |
| US-35 | Role interfaces demonstrably distinct | A | Must | 2 | 6 |
| US-36 | Injection repair guarded by a test | A | Must | 2 | 6 |
| | **Total** | | | **153** | |

The eleven M2 findings (D1-D6, H1-H3, R1-R2) are cataloged in Table 9.6 as
defects rather than stories, and carry no points for the reason in Section
4.5.

## Appendix B - Route Reference

Forty-one routes across ten blueprints - one per use case. Authorization is
given in full in Chapter 2's categorization and the use-case diagrams
(Figures 1 to 4); only paths are listed here.

| Blueprint | Routes |
|---|---|
| `auth` | `/login` · `/logout` · `/verify-otp` · `/2fa/setup` · `/2fa/disable` |
| `dashboard` | `/dashboard` |
| `cases` | `/cases` · `/cases/new` · `/cases/<id>` · `/edit` · `/archive` · `/members/add` · `/members/remove` |
| `evidence` | `/cases/<id>/evidence/upload` · `/<eid>` · `/<eid>/edit` · `/<eid>/delete` |
| `custody` | `/evidence/<eid>/transfer` · `/custody-log` · `/verify` · `/verify/json` · `/reconstruct` · `/change-state` |
| `risk` | `/risk/dashboard` · `/risk/anomaly` · `/risk/evidence/<eid>` · `/risk/evidence/<eid>/json` |
| `audit` | `/audit` · `/audit/evidence/<eid>` · `/audit/evidence/<eid>/formula-check` |
| `assistant` | `/assistant/` · `/assistant/chat` · `/assistant/clear` |
| `export` | `/cases/<id>/export` · `/evidence/<eid>/custody-report.pdf` |
| `admin` | `/admin/users` · `/users/new` · `/users/<id>/change-role` · `/toggle-active` · `/unlock` · `/admin/risk-settings` |

All require authentication except `/login` and `/verify-otp`.

**Authorization summary, derived from the route guards rather than from the
design:** Read-Only Viewer 20, Forensic Analyst 25, Lead Investigator 32,
Administrator 41.

## Appendix C - UML Diagram Index

Twenty-six diagrams in thirteen UML kinds, each placed beside the text it
illustrates. All are rendered from PlantUML source in `diagrams/`.

| Kind | Figures |
|---|---|
| Use case | 6.1 overview, 6.2 cases and evidence, 6.3 the Read-Only Viewer, 6.4 what each role adds |
| Class | 5.6 domain, 5.7 persistent (`«table»`), 3.1 traceability metamodel |
| Object | 5.8 a flagged exhibit |
| Package | 5.1 layered architecture |
| Component | 5.3 components and interfaces |
| Composite structure | 5.4 integrity engine internals |
| Deployment | 5.5 nodes, artifacts, trust boundary |
| Sequence | 11.2 integrity, 11.10 assistant, 11.6 reconstruction |
| Communication | 11.4 risk assessment collaboration |
| State machine | 11.7 evidence lifecycle, 5.2 account access |
| Activity | 11.3 risk, 11.5 reconstruction, 6.5 registration (partitions), 11.1 integrity, 11.8 transition pipeline, 11.9 assistant |
| Timing | 11.11 bounded waiting |
| Profile | 5.9 stereotype declarations |

**Non-UML figures** are the six burndown charts (6.6, 7.1, 8.1, 9.1, 9.2,
10.1), which are Scrum artifacts rather than models, and the screenshots of
Chapter 16.

## Appendix D - Traceability Summary

Carried inline in Tables 3.4, 3.6 and 3.7 rather than duplicated here.

| Check | Result |
|---|---|
| User requirements realized by at least one system requirement | 22 of 22 |
| System functional requirements traced to a user requirement | 61 of 61 |
| System functional requirements carried by a user story | 61 of 61 |
| System quality requirements with a measurement and acceptance value | 21 of 21 |
| System quality requirements with a named automated test | 21 of 21 |
| Requirements naming a technology rather than a problem | 0 |

## Appendix E - Glossary

**Append-only** - a persistence discipline permitting insertion but never
update or deletion; enforced here at the data-access layer.

**Backlog refinement (grooming)** - re-ordering, splitting, adding and
re-estimating product backlog items between sprints. Table 4.10 records six
such revisions.

**Chain of custody** - the documented, unbroken record of who held an exhibit
and what was done to it; a condition of legal admissibility.

**DAG** - directed acyclic graph; the structure the custody history is built
into for verification.

**Definition of Done / Definition of Ready** - the conditions under which an
item may be considered complete, or may enter sprint planning. Tables 4.8 and 4.7.

**Fail-visible** - recording a failure conspicuously rather than absorbing it
silently or blocking the operation.

**MoSCoW** - Must, Should, Could, Won't have this time.

**Plausibility threshold** - the minimum score (0.40) a candidate must reach
before reconstruction will infer a link rather than mark a gap unresolved.

**Sprint backlog** - the stories selected for a sprint, decomposed into tasks
by the development team. Tables 4.12, 6.2, 7.2, 8.3.

**Story point** - a unit of relative size on a Fibonacci scale, independent of
priority and of duration.

**Stereotype** - UML's own extension mechanism, used here so the relational
schema can be modeled without a second notation. Figure 5.9.

**Velocity** - points delivered in one sprint; an observed property, not a
target. Section 13.2 explains why it is weak evidence in a single-developer
project.

---

\newpage
