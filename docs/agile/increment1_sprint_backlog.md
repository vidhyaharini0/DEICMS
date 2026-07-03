# Increment 1 — Sprint Backlog

**Sprint goal:** A working evidence repository — investigators log in, manage cases, upload hashed evidence, and every action is audited.
**Dates:** Mon 4 May – Fri 22 May 2026 (14 working days, day 0–14)
**Committed:** 11 stories · **40 story points** — all delivered
**UML produced:** Use Case Diagram, Class Diagram, ER Diagram (`diagrams/increment1_*.svg`)

## Committed stories & task breakdown

| Story | Pts | Tasks (est. hours) | Status |
|---|---|---|---|
| US-01 Login/logout | 3 | Flask-Login setup (3h) · login/logout routes+templates (4h) · idle-timeout hook (2h) · audit hooks (2h) | Done |
| US-02 RBAC | 5 | Role model & helpers (3h) · route guards (5h) · role-based navigation (3h) · tests (3h) | Done |
| US-03 Case CRUD | 5 | Case model (2h) · create/edit/list/view routes (6h) · search & filters (3h) · soft archive (2h) · case membership (3h) | Done |
| US-04 Evidence upload | 5 | Evidence model (2h) · upload route + allow-list (5h) · evidence number generator (1h) · initial custody entry (3h) · templates (3h) | Done |
| US-05 SHA-256 | 2 | Hash-on-upload (2h) · original/current hash columns + display (2h) | Done |
| US-06 Metadata | 3 | Pillow EXIF extraction (3h) · python-magic MIME detection (2h) · JSON storage + display (2h) | Done |
| US-07 Evidence edit | 3 | Edit route & form (3h) · category enum (1h) · audit on edit (2h) | Done |
| US-08 Custody logging | 5 | CustodyLog model (2h) · transfer route + holder check (5h) · custody log view (3h) · location/reason capture (2h) | Done |
| US-09 Audit trail | 5 | AuditRecord model (2h) · ORM append-only guard (3h) · event hooks across routes (4h) · trail views + filters (3h) | Done |
| US-10 Audit formulas | 3 | Time-gap check (2h) · duplicate detection query (2h) · role-mismatch lookup (2h) · JSON endpoint (1h) | Done |
| US-11 Admin accounts | 1 | Admin-only creation route (2h) · password policy hook (1h) | Done |

## Daily burndown (story points remaining)

| Day | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ideal | 40.0 | 37.1 | 34.3 | 31.4 | 28.6 | 25.7 | 22.9 | 20.0 | 17.1 | 14.3 | 11.4 | 8.6 | 5.7 | 2.9 | 0 |
| Actual | 40 | 40 | 38 | 36 | 33 | 30 | 28 | 26 | 23 | 20 | 16 | 12 | 8 | 4 | 0 |

Chart: `diagrams/increment1_agile_burndown_chart.svg`

## Sprint review (summary)

All 40 points delivered. Days 0–1 produced no burned points: environment setup (Flask app factory, SQLAlchemy configuration, Git repository) took longer than planned and US-01 was only finished on day 2. Velocity recovered from day 9 by pairing the audit-trail hooks (US-09) with routes already being written for US-03/US-04 instead of retrofitting them.

## Retrospective (summary)

- **Went well:** the application-factory pattern made testing painless from the first week; committing the audit hooks together with each route avoided a "logging sprint" at the end.
- **Went poorly:** zero-burn start; underestimated route/template boilerplate for CRUD.
- **Actions for Increment 2:** reserve day 0 for spike/design work on the graph algorithm (its complexity drove the 13-point estimate); define the signing payload format before writing any custody code.
