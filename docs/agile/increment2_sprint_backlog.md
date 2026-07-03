# Increment 2 — Sprint Backlog

**Sprint goal:** Make the chain of custody provable — signed custody events, whole-chain graph verification, a formal lifecycle state machine, and honest reconstruction of gapped chains.
**Dates:** Mon 25 May – Fri 12 Jun 2026 (14 working days, day 0–14)
**Committed:** 6 stories · **38 story points** — all delivered
**UML produced:** Sequence Diagram (graph integrity verification), Activity Diagram (chain reconstruction), State Diagram (evidence lifecycle) (`diagrams/increment2_*.svg`)

## Committed stories & task breakdown

| Story | Pts | Tasks (est. hours) | Status |
|---|---|---|---|
| US-12 Ed25519 signing | 5 | canonical payload format spike (2h) · sign on transfer/upload (4h) · key pair per account (2h) · verify helper (2h) · NOT NULL migration (1h) | Done |
| US-13 Graph integrity | 13 | DAG construction from custody logs (5h) · DFS traversal engine (6h) · hash re-computation check (3h) · signature check (3h) · timestamp monotonicity check (2h) · completeness score + verdict (3h) · failure collection & report object (4h) · unit tests (5h) | Done |
| US-14 State machine | 8 | transition table w/ roles & preconditions (4h) · validation pipeline (4h) · rejection messages + audit (3h) · justification capture (2h) · risk recalc hook (2h) · tests (4h) | Done |
| US-15 Chain reconstruction | 8 | gap detection (4h) · candidate generation from access logs (4h) · plausibility scoring, 4 criteria (5h) · best-first selection + threshold (3h) · confidence labelling + report (3h) · tests (4h) | Done |
| US-16 Integrity report UI | 2 | report template (3h) · JSON endpoint (1h) | Done |
| US-17 Reconstruction UI | 2 | timeline template w/ confidence badges (3h) · wiring (1h) | Done |

## Daily burndown (story points remaining)

| Day | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ideal | 38.0 | 35.3 | 32.6 | 29.9 | 27.1 | 24.4 | 21.7 | 19.0 | 16.3 | 13.6 | 10.9 | 8.1 | 5.4 | 2.7 | 0 |
| Actual | 38 | 36 | 34 | 32 | 30 | 29 | 29 | 28 | 26 | 23 | 20 | 16 | 11 | 6 | 0 |

Chart: `diagrams/increment2_agile_burndown_chart.svg`

## Sprint review (summary)

All 38 points delivered, with the roughest mid-sprint of the project. Days 5–7 plateaued on US-13: the DFS traversal initially stopped at the first failure, which contradicted the acceptance criterion "all failures in a single pass", and reworking it surfaced a payload-mismatch bug between the signing route and the verifier's reconstruction of the signed bytes. Freezing the canonical payload format (day 0 spike, as planned in the Increment 1 retrospective) is what made the fix tractable. Velocity accelerated once the graph engine's test fixtures existed, because US-14 and US-15 reused them.

## Retrospective (summary)

- **Went well:** the day-0 design spike on the payload format paid off directly; reusable test fixtures cut the cost of the second and third algorithms; the state machine's transition table proved trivially extensible.
- **Went poorly:** 3-day plateau on the traversal rework; the 13-point estimate for US-13 was right for the wrong reasons (verification checks were easy, traversal semantics were hard).
- **Actions for Increment 3:** write acceptance-criteria-shaped unit tests *before* implementing the scoring algorithm; keep the LLM behind an interface so the pipeline is testable without API credits.
