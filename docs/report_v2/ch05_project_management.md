# Chapter 5 — Project Management

---

## 5.1 Planning Approach

Project management in an agile process differs from project management in a plan-driven one, and the difference is not that agile projects are unplanned. It is that planning happens **repeatedly at a short horizon** rather than **once at a long one**. The project was therefore planned at three levels of granularity, each with its own artefact and its own revision frequency.

**Table 5.1 — The three levels of planning**

| Level | Horizon | Artefact | Revised |
|---|---|---|---|
| **Release planning** | The whole project | Product backlog with MoSCoW priorities and the allocation of stories to increments | At each increment boundary |
| **Iteration planning** | One increment (14 working days) | Sprint backlog with story points and task breakdown | Once, at the start of each increment; scope frozen thereafter |
| **Daily planning** | One day | A written note of yesterday, today and blockers | Daily |

The rule inherited from Scrum was applied strictly: **once an increment began, its scope and end date did not change**. Work discovered mid-increment was written to the product backlog for the next planning session rather than absorbed silently. The one exception in the project's history — the access-scoping defects found at the end of Increment 3 — was handled correctly by that rule: rather than being patched into an increment that had already closed, it was raised as maintenance iteration M1 with its own planning (Section 4.12).

## 5.2 Work Breakdown Structure

The work breakdown structure decomposes the project from deliverable to task. Three levels were used: the increment, the user story, and the task. Table 5.2 shows the decomposition of one representative story from each increment; the full story catalogue is Appendix A.

**Table 5.2 — Representative work breakdown (three levels)**

| Level 1 — Increment | Level 2 — User story | Level 3 — Tasks |
|---|---|---|
| Increment 1 | US-09 Append-only audit trail (5 pts) | Define the AuditRecord entity; add the recorder utility; block UPDATE and DELETE at the ORM event level; add per-evidence, per-investigator and global trail views; write the append-only tests |
| Increment 2 | US-13 Graph integrity verification (13 pts) | Design spike on graph representation; freeze the canonical signature payload; build the graph from custody logs; implement depth-first traversal; implement the three per-node checks; accumulate rather than short-circuit failures; compute the completeness score; build the report object; write the algorithm tests |
| Increment 3 | US-20 AI assistant orchestration (8 pts) | Design the six-stage pipeline; implement intent classification; implement scoped context retrieval; implement prompt construction with history trimming; implement model invocation behind a seam; implement response validation; build the chat interface; write per-stage tests against the mock backend |
| M1 | US-28 Role-scoped aggregates (5 pts) | Introduce the `accessible_case_ids` helper; route every aggregate query through it; design role-tailored dashboard panels; add the empty-state message; write adversarial scoping tests |

The decomposition rule was that a **task is a unit of work completable in under one working day**. A story that could not be broken into such tasks was, by that fact, too large and was either split or flagged as carrying unquantified risk — which is exactly what happened with US-13, whose thirteen-point estimate is the record of that flag.

## 5.3 Project Timeline and Milestones

**Table 5.3 — Project timeline and milestones**

| Phase | Duration | Milestone | Exit criterion |
|---|---|---|---|
| Inception | Pre-increment | Proposal approved | Feature categorisation reviewed and accepted |
| Increment 1 | 14 working days | M-1: Working repository | 11 stories accepted; audit trail complete; 40 points delivered |
| Increment 2 | 14 working days | M-2: Provable integrity | 6 stories accepted; chain verifiable end to end; 38 points delivered |
| Increment 3 | 14 working days | M-3: Functional scope complete | 10 stories accepted; all five guarantees delivered; 42 points delivered |
| Maintenance M1 | Short iteration | M-4: Access scoping uniform | Adversarial scoping suite passing; full prior suite still green |
| Maintenance M2 | Short iteration | M-5: Review findings closed | 11 findings resolved; 172 tests passing |
| Closure | Documentation | M-6: Report and diagrams complete | Report, UML set and traceability matrix delivered |

Milestones M-1 to M-3 correspond to the sprint reviews; each is a **business milestone** in the RUP sense — a point at which the system could, in principle, have been shown to a stakeholder as a working subset — rather than a phase boundary in the waterfall sense.

## 5.4 Risk Management

Risks were identified at the outset and reviewed at each increment boundary. Each carries a probability, an impact, a resulting exposure, and a mitigation. Table 5.4 is the project risk register in its final state, including the outcome of each risk — which is the column that makes a risk register evidence rather than a formality.

**Table 5.4 — Project risk register**

| ID | Risk | Category | Prob. | Impact | Exposure | Mitigation | Outcome |
|---|---|---|---|---|---|---|---|
| R-01 | A complex algorithm proves infeasible within its estimate | Technical | Medium | High | **High** | Place algorithms in the middle increment, after the foundation stabilises; reserve a day-zero design spike | **Partially occurred** — US-13 required rework, causing a 3-day plateau; absorbed within the increment |
| R-02 | The external language model is unavailable or changes | Technical / external | Medium | Medium | **Medium** | Invoke the model behind a single seam; provide a context-aware mock fallback | **Occurred** — the model was retired by the provider (HTTP 410); absorbed by an ordered fallback list |
| R-03 | Security defect in access control | Technical / quality | Medium | **Critical** | **High** | Role and case-access model designed in Increment 1; adversarial review testing | **Occurred twice** — M1 (aggregates) and M2 D3 (cross-case IDOR); both found and fixed before delivery |
| R-04 | Single-developer capacity misjudged | Schedule | Medium | High | **High** | Calibrate velocity from Increment 1 rather than assuming it; hold MoSCoW *Could* stories as the sacrificial scope | Did not occur; all three increments met their totals |
| R-05 | Requirements misunderstood, producing the wrong system | Requirements | Low | High | Medium | Personas and testable acceptance criteria written before implementation; review against criteria at each increment | Did not occur |
| R-06 | Scope creep from attractive but unplanned features | Schedule | Medium | Medium | **Medium** | Frozen increment scope; new ideas written to the product backlog, not built | Did not occur; the *won't-have* list held |
| R-07 | Third-party library incompatibility or deprecation | Technical / external | Low | Medium | Low | Prefer widely-used, stable libraries; pin versions in `requirements.txt` | Did not occur for libraries; see R-02 for the hosted model |
| R-08 | Data loss during development | Operational | Low | High | Medium | Git configuration management from the first commit; all artefacts versioned alongside the code | Did not occur; the repository is the authoritative record |
| R-09 | Test suite becomes slow or unreliable, discouraging its use | Quality | Low | Medium | Low | In-memory database per test; no external network calls in the suite | Did not occur; the suite runs in seconds |
| R-10 | Estimation bias from estimator and implementer being one person | Process | **High** | Low | Medium | Acknowledged openly; the *shape* of the burndown treated as more informative than whether the total was met | Occurred by construction; discussed in Sections 4.8 and 18.2 |

Three observations about this register are worth making explicitly, because a risk register whose risks all failed to materialise is usually a register that was written after the fact.

First, **three of the ten risks actually occurred**, and in each case the mitigation is what absorbed the impact — the design spike for R-01, the seam and fallback for R-02, the adversarial testing for R-03. Second, **R-03 was correctly rated the highest-exposure risk** and it was the one that occurred twice, which is the strongest available evidence that the rating was sound rather than decorative. Third, **R-10 was rated high-probability and was accepted rather than mitigated**, because no mitigation is available to a single-developer project; the honest response to an unmitigable risk is to disclose it, not to invent a control.

## 5.5 Configuration Management and Version Control

Setting up a configuration management environment is the canonical practical expression of the principle of **anticipation of change** (Section 3.7), and it was the first task of Increment 1 rather than an afterthought.

**Table 5.5 — Configuration management practices**

| Practice | Implementation | Purpose |
|---|---|---|
| Version control | Git repository initialised before the first line of application code | An auditable record of how the system evolved |
| Commit discipline | Commits at logical boundaries with descriptive messages | Each commit is a comprehensible unit of change |
| Artefact co-versioning | Diagrams, backlogs and this report versioned alongside the code | No artefact can drift out of step with the implementation without the divergence being visible |
| Dependency pinning | `requirements.txt` with pinned versions | Reproducible environment; protects against R-07 |
| Secret management | Secrets in `.env`, excluded from version control; production profile refuses to boot on defaults | Credentials never enter the repository history |
| Schema evolution | Lightweight startup migration that inspects existing columns and adds missing ones | An existing database is brought up to date without a rebuild |

The artefact co-versioning practice deserves emphasis because it is easy to state and easy to neglect. A UML diagram stored outside version control drifts silently away from the code it claims to describe; one stored inside it produces a visible diff whenever the code changes and the diagram does not. This is the mechanism by which the report's claims about the system remain checkable rather than aspirational.

## 5.6 Quality Assurance Strategy

Quality assurance operated at four levels, each catching a different class of problem. The project's own history demonstrates that the levels are complementary rather than redundant — a point developed at length in Chapter 11 and in the M2 reflection.

**Table 5.6 — Quality assurance levels**

| Level | Mechanism | Catches | Evidence from this project |
|---|---|---|---|
| 1 | **Definition of done** applied per story (Table 4.8) | Incomplete work presented as complete | No story was accepted without passing tests and an audit path |
| 2 | **Automated test suite** — 172 tests across seven modules | Regression; behaviour that is exercised and breaks | The full suite was re-run after every maintenance fix |
| 3 | **Adversarial review testing** — deliberately attempting forbidden actions | Authorisation defects that positive tests cannot see | Found both M1 defects |
| 4 | **Structured code review** — reading the code against its intent | Behaviour that is specified but silently absent | Found all eleven M2 findings, including two critical ones |

The structure of this table is itself a project finding. Levels 1 and 2 are the conventional ones, and a project that stopped there would have shipped with a dead soft-delete, a dead risk factor weighted at 0.25, and a cross-case object reference — all while reporting a green suite. Levels 3 and 4 were added in response to what levels 1 and 2 missed, and the conclusion drawn in Section 4.13.4 is that **testing and review are complementary rather than substitutable**.

## 5.7 Summary

This chapter set out how the project was managed. Planning operated at three horizons — release, iteration and day — with increment scope frozen once begun. The work breakdown decomposed increments into stories and stories into sub-day tasks, with the inability to decompose treated as a signal of unquantified risk. Six milestones marked the increments and maintenance iterations, each with an objective exit criterion. A ten-entry risk register was maintained with probability, impact, mitigation and outcome; three risks occurred and were absorbed by their mitigations, the highest-exposure risk was the one that occurred twice, and one unmitigable risk was disclosed rather than falsely controlled. Configuration management was established before the first line of code, with all artefacts versioned alongside it. Quality assurance operated at four complementary levels, two of which were added in response to defects the conventional two had missed.

The next chapter turns to the requirements themselves.

---

\newpage
