# Increment 3 — Sprint Backlog

**Sprint goal:** Turn records into judgement — risk scoring, AI-assisted querying with hallucination protection, anomaly detection, security hardening, and court-ready exports.
**Dates:** Mon 15 Jun – Fri 3 Jul 2026 (14 working days, day 0–14)
**Committed:** 10 stories · **42 story points** — all delivered
**UML produced:** Activity Diagram (risk scoring), Sequence Diagram (AI orchestration), Component Diagram, Deployment Diagram (`diagrams/increment3_*.svg`)

## Committed stories & task breakdown

| Story | Pts | Tasks (est. hours) | Status |
|---|---|---|---|
| US-18 Risk scoring | 8 | factor extraction, 8 signals (5h) · normalisation curves (3h) · weighted sum + interaction rules (4h) · classification + recommendations (3h) · tests-first per retro action (5h) | Done |
| US-19 Configurable weights | 3 | settings persistence (2h) · admin Risk Settings page (3h) · re-normalisation + validation (2h) | Done |
| US-20 AI orchestration | 8 | intent classifier (4h) · context retrieval per intent (5h) · prompt templates (3h) · NVIDIA NIM client behind interface + mock (4h) · response validation (3h) | Done |
| US-21 Hallucination detection | 3 | entity extraction regexes (2h) · cross-check vs context + investigator names (3h) · UI/JSON surfacing (2h) | Done |
| US-22 Anomaly detection | 5 | feature engineering, 6 dims (4h) · Isolation Forest integration (3h) · "suggested for review" presentation (2h) | Done |
| US-23 Dashboards | 3 | risk-ranked dashboard (3h) · anomaly dashboard (3h) · per-item risk page (2h) | Done |
| US-24 2FA & lockout | 5 | TOTP enrolment + QR (4h) · login second factor (3h) · lockout & unlock (3h) · rate limiting (2h) | Done |
| US-25 Encryption & magic bytes | 3 | AES-256-GCM file encryption (3h) · magic-byte validation (3h) · private-key encryption (2h) | Done |
| US-26 Signed ZIP export | 2 | manifest + audit bundle (3h) · Ed25519 manifest signature (2h) | Done |
| US-27 PDF custody report | 2 | ReportLab layout (3h) · embedded fresh integrity run (1h) | Done |

## Daily burndown (story points remaining)

| Day | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ideal | 42 | 39 | 36 | 33 | 30 | 27 | 24 | 21 | 18 | 15 | 12 | 9 | 6 | 3 | 0 |
| Actual | 42 | 40 | 37 | 34 | 30 | 28 | 25 | 22 | 19 | 16 | 13 | 10 | 7 | 4 | 0 |

Chart: `diagrams/increment3_agile_burndown_chart.svg`

## Sprint review (summary)

All 42 points delivered — the steadiest sprint of the three, tracking within 2 points of ideal throughout (slight slip days 1–3, recovered by day 4). Both retrospective actions from Increment 2 paid off: writing the risk-scoring tests first caught two normalisation edge cases (equal min/max bounds; negative inputs to the log curve) before they reached a route, and hiding the LLM behind an interface with a context-aware mock meant the entire six-stage pipeline was testable without API credits. The security stories (US-24, US-25) integrated cleanly because the audit and custody layers from earlier increments already exposed the right hooks.

## Retrospective (summary)

- **Went well:** test-first worked measurably; the mock LLM enabled full pipeline coverage; hardening landed without touching algorithm code.
- **Went poorly:** the signed-upload requirement introduced in US-12 (NOT NULL signature) initially broke older test fixtures — schema-tightening needs a test-suite sweep in the same change, not afterwards.
- **Carry-forward for future work:** PostgreSQL migration, notification system, and the Won't-have list in the product backlog.

## Velocity across the project

| Increment | Committed | Delivered | Velocity |
|---|---|---|---|
| 1 | 40 | 40 | 40 |
| 2 | 38 | 38 | 38 |
| 3 | 42 | 42 | 42 |
| **Total / mean** | **120** | **120** | **40.0** |
