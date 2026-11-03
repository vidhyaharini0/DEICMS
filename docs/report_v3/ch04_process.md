# Chapter 4 - The Software Development Process

---

## 4.1 Choosing a Process

A development process is chosen for a project's particular shape, not adopted
because it is current. This section states the shape, evaluates the
candidates against it, and records the decision with its reasoning, so that
Chapter 11 can judge the decision against what actually happened rather than
against what was hoped.

### 4.1.1 The shape of this project

**Table 4.1 - Project characteristics bearing on the choice**

| Characteristic | Value | Bearing on the choice |
|---|---|---|
| Team size | One developer | Collaborative ceremonies must be adapted or abandoned |
| Customer availability | None - no external client | On-site customer is impossible; the acceptance criterion must substitute |
| Requirements volatility | Low for the data layer, **high for the algorithms** | The algorithms resist being specified fully in advance |
| Technical risk | Concentrated in five custom algorithms | Risk must be attacked early, not deferred |
| Dependency structure | Strongly ordered: data → integrity → assessment | Later work genuinely needs earlier work running |
| Delivery horizon | Fixed academic deadline | Scope must flex; the date cannot |
| Required evidence | Planning and reflection artefacts | The process must produce documents as a by-product |

The third and fourth rows dominate. The data layer could have been specified
completely before a line was written: six entities, their relationships, their
constraints. The five algorithms could not. The traversal semantics of the
integrity verifier, the normalisation curve for each risk indicator, the
plausibility criteria for reconstruction - none of these could be settled
on paper, because settling them required running them against data.

### 4.1.2 Candidates

**Table 4.2 - Process models evaluated**

| Model | Fit to this project | Verdict |
|---|---|---|
| **Waterfall** | Requires requirements frozen before design. Would have frozen the algorithms' design at the point of least knowledge, and the integrity verifier's semantics did in fact change under implementation | **Rejected** - the known-volatile part is the part it freezes hardest |
| **V-model** | Waterfall's discipline with test levels paired to construction phases. The pairing is valuable and was retained (Chapter 9); the rigid sequencing was not | **Rejected as a lifecycle, adopted as a test strategy** |
| **Incremental** | Builds in slices, each adding capability. Matches the dependency order well. But prescribes no artefacts for planning or reflection | **Necessary but not sufficient** |
| **Spiral** | Risk-driven, with explicit risk analysis each cycle. Well matched to the algorithmic risk, but its ceremony is calibrated for large systems with real stakeholder negotiation | **Rejected as disproportionate** |
| **Extreme Programming** | Test-first development, refactoring, small releases, simple design. All directly applicable and all adopted as practices | **Adopted as practices within the chosen framework** |
| **Scrum** | An incremental framework with defined artefacts - product backlog, sprint backlog, increment - and defined events. Provides exactly the planning and reflection structure incremental development lacks | **Selected** |

### 4.1.3 The decision, and its relation to the project proposal

The accepted project proposal named the **Agile Incremental Model** and
undertook to structure the report with one section per increment, each
carrying its own user stories, diagrams and retrospective.

Scrum is an agile incremental framework. The proposal named the family; this
chapter names the member of that family and, more importantly, commits to
implementing its artefacts rather than borrowing its vocabulary. **That
distinction is the substance of the revision.** An earlier version of this
report used Scrum terms - sprint, backlog, retrospective - over a process that
had no prioritised product backlog, no refinement between sprints, and no
decomposition of stories into tasks. Using the vocabulary without the
artefacts is worse than not using it, because it claims a discipline that was
not practised.

**Table 4.3 - Four reasons Scrum was selected**

| # | Reason | Why the alternatives fail it |
|---|---|---|
| R1 | Technical risk sits in work that cannot be specified in advance; Scrum commits only one sprint at a time | Waterfall and the V-model commit the whole design at the point of least knowledge |
| R2 | The three capability tiers have a genuine dependency order that rewards building in slices | A single big-bang delivery would leave integration untested until the end |
| R3 | Feedback between sprints should change the next sprint's plan, through a retrospective whose actions are binding | Incremental development alone prescribes no reflection step |
| R4 | The process must leave behind backlogs, burndowns, reviews and retrospectives as evidence | Spiral produces risk analyses rather than these; plain incremental produces none |

Chapter 13 returns to this table and assesses each reason against the outcome.

## 4.2 Scrum With One Developer - What Was Kept, Adapted and Abandoned

Scrum assumes three roles and five events, all of which presuppose more than
one person. Reporting them as though they were performed would be false. This
section states exactly what was done.

**Table 4.4 - Scrum roles**

| Role | Scrum's definition | How it was discharged here | Honest assessment |
|---|---|---|---|
| Product Owner | Owns and orders the product backlog; represents stakeholder value | Discharged by the developer wearing a separate hat, with ordering decided against the stakeholder concerns of Table 3.3 and the domain requirements of Table 3.8 rather than by preference | **Adapted.** The ordering is defensible but was never contested by a real stakeholder |
| Scrum Master | Removes impediments; guards the process | Discharged by the developer, with the retrospective's actions treated as binding commitments on the next sprint rather than as suggestions | **Adapted.** Nobody independent enforced the process |
| Development Team | Builds the increment | The developer | **Unchanged in function, absent in plurality** |

**Table 4.5 - Scrum events**

| Event | Performed? | Form it took |
|---|---|---|
| Sprint | **Yes, unchanged** | Six fixed-length sprints, each ending in a working increment |
| Sprint Planning | **Yes, adapted** | Backlog items selected against a capacity figure, then decomposed into tasks (Section 4.7) |
| Daily Scrum | **No - abandoned** | A daily stand-up with oneself synchronises nothing. Replaced by a daily written progress note feeding the burndown, which serves the *tracking* purpose but not the *coordination* purpose |
| Sprint Review | **Yes, adapted** | Increment demonstrated against each story's acceptance criteria; outcome recorded per sprint |
| Sprint Retrospective | **Yes, unchanged in substance** | Process examined, actions recorded, actions carried into the next sprint's plan |
| Backlog Refinement | **Yes** | Performed between sprints; the backlog's version history is in Table 4.9 |

**The honest conclusion.** Four of Scrum's five events survive adaptation
because they operate on *artefacts*, which exist regardless of team size. The
Daily Scrum does not, because it operates on *communication between people*.
Claiming to have held it would be the clearest possible example of vocabulary
without substance, which is the fault this revision exists to correct.

## 4.3 Sprint 0 - Initial Planning

Before the first sprint, a planning phase established what Scrum calls the
initial product backlog, and what Sommerville would call the plan-driven
portion of a hybrid process. The two descriptions are compatible: Scrum does
not forbid up-front analysis, it forbids *committing the whole design* up
front.

**Table 4.6 - Sprint 0 outputs**

| Output | Where it lives | Why it was done up front |
|---|---|---|
| Stakeholder and concern analysis | Table 3.3 | Backlog ordering needs a basis |
| User requirements (22) and user quality requirements (9) | Tables 3.4, 3.5 | The product backlog is derived from them |
| System requirements (61) and system quality requirements (21) | Tables 3.6, 3.7 | Acceptance criteria come from here |
| Domain requirements (7) | Table 3.8 | Non-negotiable; must constrain every sprint |
| Conceptual data model | Figure 5.2 | Six entities stable from the outset; no benefit in discovering them incrementally |
| Architectural decision: layered, with business logic isolated | Chapter 5 | A structural decision expensive to reverse later |
| Definition of Ready and Definition of Done | Tables 4.7, 4.8 | A sprint cannot start or finish without them |

**The division of labour between plan-driven and agile work in this project is
therefore explicit:** what was stable was specified up front; what was
volatile was left to the sprint that would build it. The data layer belongs to
the first group and the five algorithms to the second, which is precisely the
distinction drawn in Section 4.1.1.

### 4.3.1 Definition of Ready

**Table 4.7 - A backlog item may enter sprint planning only when all hold**

| # | Condition |
|---|---|
| 1 | Written as a user story: as a *role*, I want *capability*, so that *benefit* |
| 2 | Traced to at least one system requirement in Table 3.6 or 3.7 |
| 3 | Carries acceptance criteria that can be judged true or false |
| 4 | Estimated in story points |
| 5 | Small enough to complete within one sprint |
| 6 | Its dependencies are already delivered or are in the same sprint |

### 4.3.2 Definition of Done

**Table 4.8 - An item is done only when all hold**

| # | Condition |
|---|---|
| 1 | Every acceptance criterion demonstrably satisfied |
| 2 | Automated tests written and passing, including at least one negative case |
| 3 | The whole suite passes, not only the new tests |
| 4 | Business logic contains no interface-layer dependency (SNF-11) |
| 5 | The action is recorded in the audit trail where it changes state |
| 6 | Authorisation enforced at the route, not only hidden in the interface |
| 7 | Diagrams affected by the change updated in the same commit |

Condition 7 was added after Sprint 1, where diagrams drifted from the code
within days. Condition 2's negative-case clause was added after Sprint 5, for
reasons Chapter 9 records.

## 4.4 Product Backlog, Version 1.0

The initial backlog as it stood at the end of Sprint 0, before any sprint
began. It is ordered by priority, and that order - not the identifier - is
what sprint planning consumed.

Priority is MoSCoW. Estimation is story points on a Fibonacci scale, which
measures *relative size*, not duration, and is deliberately independent of
priority: US-13 is the largest item in the backlog at 13 points and is a Must,
while US-11 is a 1-point Must and US-22 is a 5-point Could.

**Table 4.9 - Product backlog v1.0 (end of Sprint 0)**

| Rank | ID | User story | Traces to | Cat | MoSCoW | Pts |
|---|---|---|---|---|---|---|
| 1 | US-01 | As an investigator, I want to sign in securely, so that only authorised people reach case data | SR-01 to SR-03 | A | Must | 3 |
| 2 | US-02 | As an administrator, I want access limited by function, so that nobody exceeds their remit | SR-04 to SR-06, SR-09 | A | Must | 5 |
| 3 | US-11 | As an administrator, I want to be the only one who can create accounts, so that access is controlled at source | SR-21, SR-22 | A | Must | 1 |
| 4 | US-03 | As a lead investigator, I want to open, find and close investigations, so that work is organised | SR-07, SR-08 | A | Must | 5 |
| 5 | US-04 | As an investigator, I want to register an exhibit, so that it enters the system under control | SR-10 to SR-12 | A | Must | 5 |
| 6 | US-05 | As an auditor, I want each exhibit fingerprinted at intake, so that later change is detectable | SR-13 | B | Must | 2 |
| 7 | US-08 | As an investigator, I want every handover recorded, so that the chain is unbroken | SR-16, SR-17 | A | Must | 5 |
| 8 | US-09 | As an auditor, I want an unalterable history, so that the record can be trusted | SR-18, SR-19 | A | Must | 5 |
| 9 | US-06 | As an analyst, I want content checked against its declared type, so that disguised files are refused | SR-14 | B | Must | 3 |
| 10 | US-07 | As an analyst, I want to describe and classify an exhibit, so that it can be found and understood | SR-15 | A | Must | 3 |
| 11 | US-10 | As an auditor, I want obvious handling anomalies surfaced, so that gaps are noticed early | SR-20 | A | Should | 3 |
| 12 | US-12 | As a court, I want custody records attributable to their author, so that authorship is beyond dispute | SR-23, SR-24 | B | Must | 5 |
| 13 | US-13 | As an investigator, I want the whole custody history verified, so that tampering anywhere is found | SR-25 to SR-27 | **C** | Must | **13** |
| 14 | US-14 | As a lead investigator, I want exhibits to move only through permitted states, so that procedure is enforced | SR-28 to SR-30 | **C** | Must | 8 |
| 15 | US-15 | As an investigator, I want missing custody links reconstructed, so that incomplete histories remain usable | SR-31 to SR-33 | **C** | Must | 8 |
| 16 | US-16 | As an investigator, I want to read a verification result, so that I can act on it | SR-34 | A | Should | 2 |
| 17 | US-17 | As an investigator, I want to read a reconstruction, so that I can judge its inferences | SR-35 | A | Should | 2 |
| 18 | US-18 | As a lead investigator, I want exhibits ranked by attention needed, so that effort goes where it matters | SR-36 to SR-38 | **C** | Must | 8 |
| 19 | US-20 | As an investigator, I want to ask questions in ordinary language, so that I need not learn the schema | SR-40 to SR-42 | **C** | Must | 8 |
| 20 | US-21 | As an investigator, I want unsupported statements flagged, so that I do not act on invention | SR-43 | **C** | Must | 3 |
| 21 | US-24 | As an administrator, I want a second authentication factor and lockout, so that stolen passwords are insufficient | SR-47 | B | Should | 5 |
| 22 | US-25 | As a custodian, I want evidence unreadable without authorisation, so that losing the medium is not losing the case | SR-48 | B | Should | 3 |
| 23 | US-19 | As an administrator, I want to tune what counts as risky, so that the system matches our practice | SR-39 | **C**/A | Should | 3 |
| 24 | US-23 | As a lead investigator, I want ranked and anomalous views, so that I can survey a caseload | SR-46 | A | Should | 3 |
| 25 | US-26 | As an investigator, I want a verifiable export, so that a third party can check our work | SR-49 | B | Should | 2 |
| 26 | US-22 | As an analyst, I want statistical outliers surfaced, so that unusual handling is noticed | SR-44, SR-45 | B | Could | 5 |
| 27 | US-27 | As an investigator, I want a printable custody report, so that the file can be lodged on paper | SR-50 | B | Could | 2 |
| | | **Total committed scope at v1.0** | | | | **120** |

**Won't have this time** (recorded so the boundary is explicit): production
deployment behind a multi-process server; notifications; full-text search over
exhibit *content*; a multi-language interface; a mobile client; fine-tuning of
the language model. None adds to the engineering demonstration.

### 4.4.1 How the order was decided

Four rules, applied in sequence, produced the ranking:

1. **Domain requirements first.** DR-01 (custody begins at collection) makes
   US-04 and US-08 prerequisites for everything else, whatever their MoSCoW
   value.
2. **Dependency before preference.** US-13 cannot be built before US-12, which
   cannot be built before US-08. The dependency graph, not desirability, fixes
   large parts of the order.
3. **Risk early within a tier.** Among items of equal priority and satisfied
   dependencies, the one carrying the most uncertainty goes first - which is
   why the 13-point US-13 opens Sprint 2 rather than closing it.
4. **MoSCoW breaks remaining ties.** Musts before Shoulds before Coulds.

Rule 3 is the one that distinguishes a risk-aware ordering from an arbitrary
one, and it is the rule that paid off: the traversal-semantics change
described in Chapter 7 was discovered on day two of Sprint 2 rather than at
its end.

## 4.5 Backlog Refinement Across the Project

A product backlog that does not change between sprints is not being managed.
Refinement was performed between every pair of sprints: re-ordering on new
knowledge, splitting items found too large, adding items discovered during
review, and re-estimating where the first estimate proved wrong.

**Table 4.10 - Backlog version history**

| Version | At | Change | Cause |
|---|---|---|---|
| v1.0 | End of Sprint 0 | 27 stories, 120 points | Initial planning |
| v1.1 | Before Sprint 2 | US-13 re-estimated 8 → **13**; US-16, US-17 split out of US-13 as separate reporting stories | The design spike showed presentation was distinct work from traversal |
| v1.2 | Before Sprint 3 | US-22 lowered from Should to **Could**; US-24 raised from Could to **Should** | Review of Sprint 2 showed authentication hardening mattered more than statistical anomaly detection |
| v2.0 | After Sprint 3 review | **US-28, US-29 added** (10 points) | Adversarial testing found aggregates unscoped - a change request, not a defect, because no stated requirement had been broken |
| v2.1 | After Sprint 4 | **D1 to D6, H1 to H3, R1, R2 added** as defect items, not stories | Structured code review found 11 issues; a defect restores an accepted requirement rather than adding one |
| v3.0 | After Sprint 5 | **US-30 to US-36 added** (23 points) | An audit found quality requirements stated without the means to verify them |
| | | **Final scope: 36 stories, 153 points, 11 defects** | |

**Table 4.10a - Items added to the backlog after v1.0**

| ID | User story | Traces to | Added at | Pts |
|---|---|---|---|---|
| US-28 | As an administrator, I want every total and ranking confined to the viewer's own investigations, so that aggregates cannot leak what detail views protect | SR-51, SR-52, SR-59 | v2.0 | 5 |
| US-29 | As an investigator, I want the assistant confined to my investigations, so that a question cannot retrieve what a page would refuse | SR-41, SR-53, SR-54 | v2.0 | 5 |
| US-30 | As an assessor, I want every quality requirement to carry a measurement and a pass value, so that a claim about quality can fail | SR-57 to SR-61, Table 3.7 | v3.0 | 5 |
| US-31 | As an administrator, I want transport and session hardening verified rather than asserted, so that removing it breaks a test | SR-60, SNF-15, SNF-16 | v3.0 | 3 |
| US-32 | As an administrator, I want an unsafe production configuration refused, and the refusal itself exercised | SR-61, SNF-18 | v3.0 | 3 |
| US-33 | As an investigator, I want listings to stay responsive as a case grows, so that a large case remains workable | SR-57, SNF-10 | v3.0 | 3 |
| US-34 | As an assessor, I want algorithmic cost measured rather than argued, so that a regression in complexity is caught | SR-58, SNF-07 to SNF-09 | v3.0 | 5 |
| US-35 | As an investigator, I want each role's overview demonstrably distinct, so that scoping is visible and not merely claimed | SR-59, SNF-21 | v3.0 | 2 |
| US-36 | As an auditor, I want the injection repair guarded by a test, so that a fixed defect cannot silently return | SNF-17 | v3.0 | 2 |
| | **Added after v1.0** | | | **33** |

Two entries in Table 4.10 deserve comment.

**v2.0 records a change request, not a defect.** The aggregates leaked data
across cases, but no requirement then in force said they must not - UR-03
existed, but the system requirements realising it addressed record access
only. Calling this a defect would blame the implementation for a gap in the
specification. It was the requirement's scope that was incomplete, so it
entered the backlog as new scope.

**v2.1 records defects, which do not carry story points.** Points estimate
*new capability*. Repairing a defect restores capability already accepted and
already paid for; estimating it in points would inflate velocity by counting
the same work twice.

## 4.6 Sprint Planning and the Sprint Backlog

Sprint planning answers two questions: *what* can be delivered, and *how* will
it be done. Scrum's answer to the second is that selected stories are
decomposed by the developers into tasks. A sprint backlog that lists only
stories has skipped this step, and cannot support a burndown at useful
resolution.

**Table 4.11 - From product backlog to task, with one worked example**

| Level | Artefact | Example | Owned by |
|---|---|---|---|
| 1 | Product backlog item | US-13: *verify the whole custody history* (13 pts) | Product Owner |
| 2 | Acceptance criteria | Reports a verdict; locates **every** failure, not the first; gives a completeness proportion | Product Owner |
| 3 | Sprint backlog item | Selected into Sprint 2 | Development Team |
| 4 | **Tasks** | See Table 4.12 | Development Team |

**Table 4.12 - US-13 decomposed into tasks (Sprint 2)**

| Task | Description | Est. (h) | Traces to |
|---|---|---|---|
| T-13.1 | Design spike: decide the structure the custody records build into | 4 | SR-25 |
| T-13.2 | Build records into that structure, rooted at registration | 6 | SR-25 |
| T-13.3 | Implement the content-consistency examination | 4 | SR-26 |
| T-13.4 | Implement the authorship examination | 5 | SR-26 |
| T-13.5 | Implement the chronological examination | 3 | SR-26 |
| T-13.6 | Accumulate failures without halting the walk | 4 | SR-26 |
| T-13.7 | Compute the completeness proportion | 2 | SR-27 |
| T-13.8 | Assemble the finding object and its serialised form | 3 | SR-27 |
| T-13.9 | Write failing tests for all three examination kinds first | 6 | DoD 2 |
| T-13.10 | Update the sequence and activity diagrams | 2 | DoD 7 |
| | **Total** | **39 h** | |

Task T-13.6 is the one that justified the design spike. The first design
halted the walk at the first failure, which satisfied a naive reading of the
story but violated its second acceptance criterion. **The task decomposition
is where that mismatch surfaced**, because writing T-13.6 as a separate task
forced the question of what happens after a failure to be answered explicitly
rather than by default.

### 4.6.1 Capacity and the point of a velocity figure

The first sprint had no velocity history, so its capacity was set by available
hours and an assumed rate, and was deliberately conservative. From Sprint 2
onward, capacity was set by the previous sprint's observed velocity.

**Table 4.13 - Capacity basis per sprint**

| Sprint | Capacity basis | Committed |
|---|---|---|
| 1 | Estimated from available hours; no history | 40 |
| 2 | Sprint 1 velocity (40), reduced for the 13-point unknown | 38 |
| 3 | Mean of Sprints 1-2 (39), raised on two sprints of stable delivery | 42 |
| 4 (M1) | Change-request sprint; scope fixed by the two stories | 10 |
| 5 (M2) | Defect sprint; no point commitment (see Section 4.5) | - |
| 6 (M3) | Mean of Sprints 1-3 (40), reduced for a short fixed window | 23 |

**A caution that Chapter 13 develops.** Velocity is meaningful when the
estimator and the implementer are different people, because then the estimate
is an independent prediction. Here they are the same person, so an estimate
can be - and unconsciously is - adjusted to the implementer's known pace.
Every sprint delivering exactly its commitment should therefore be read as
*weak* evidence about estimation accuracy and *strong* evidence only about
scope stability. This is risk R-10 in the register, rated high-probability and
**accepted rather than mitigated**, because no mitigation is available to a
single developer.

## 4.7 The Six Sprints

**Table 4.14 - Sprint overview**

| Sprint | Name | Stories | Pts | Delivered | Chapter |
|---|---|---|---|---|---|
| 1 | Foundation: cases, exhibits, custody, audit | US-01 to US-11 | 40 | 40 | 6 |
| 2 | Integrity: verification, lifecycle, reconstruction | US-12 to US-17 | 38 | 38 | 7 |
| 3 | Assessment: risk, assistant, reporting | US-18 to US-27 | 42 | 42 | 8 |
| 4 (M1) | Access scoping | US-28, US-29 | 10 | 10 | 9 |
| 5 (M2) | Defect repair | D1-D6, H1-H3, R1-R2 | - | 11 findings | 9 |
| 6 (M3) | Quality enforcement | US-30 to US-36 | 23 | 23 | 10 |
| | **Total** | **36 stories** | **153** | **153 + 11** | |

Each of Chapters 6 to 10 follows the same structure: sprint goal, refined
backlog, sprint backlog with tasks, design and UML for what that sprint built,
implementation, tests, burndown, review against acceptance criteria, and
retrospective with binding actions.

**Sprints 4, 5 and 6 are the ones worth attention.** Sprints 1 to 3 delivered
the planned system. Sprints 4, 5 and 6 each arose from a defect found after
acceptance - by adversarial testing, by structured code reading, and by audit
against the specification respectively - and together they exercise the
detection and response an incremental model is chosen for.

---

\newpage
