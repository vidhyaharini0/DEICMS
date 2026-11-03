# Chapter 6 - Sprint 1: Foundation

*15 working days · 40 points committed · 40 delivered*

---

## 6.1 Sprint Goal

**A working system in which an investigation can be opened, evidence
registered under control, custody recorded, and every action written to a
history that cannot be rewritten.**

The goal names an end state rather than a list of features, because the test
of this sprint is whether the later algorithms have something real to operate
on. An integrity verifier with no custody records to verify is untestable.

## 6.2 Backlog Going In

Product backlog **v1.0** (Table 4.9). The top eleven ranked items were taken,
which exhausted the dependency-free portion of the backlog: US-12 at rank 12
requires signing credentials that US-11 issues, and US-13 requires the custody
records US-08 creates.

**Table 6.1 - Sprint 1 backlog**

| ID | Story | Pts | Realises |
|---|---|---|---|
| US-01 | Sign in securely | 3 | SR-01 to SR-03 |
| US-02 | Access limited by function | 5 | SR-04 to SR-06, SR-09 |
| US-11 | Administrator-only account creation | 1 | SR-21, SR-22 |
| US-03 | Open, find and close investigations | 5 | SR-07, SR-08 |
| US-04 | Register an exhibit | 5 | SR-10 to SR-12 |
| US-05 | Fingerprint at intake | 2 | SR-13 |
| US-08 | Record every handover | 5 | SR-16, SR-17 |
| US-09 | Unalterable history | 5 | SR-18, SR-19 |
| US-06 | Content checked against declared type | 3 | SR-14 |
| US-07 | Describe and classify an exhibit | 3 | SR-15 |
| US-10 | Surface handling anomalies | 3 | SR-20 |
| | **Total** | **40** | |

## 6.3 Sprint Backlog: Stories Decomposed Into Tasks

Only the two stories whose decomposition proved consequential are given in
full; the remaining nine followed the same pattern.

**Table 6.2 - US-09 (unalterable history) decomposed**

| Task | Description | Est. (h) | Realises |
|---|---|---|---|
| T-09.1 | Design the audit record: actor, origin, moment, outcome | 3 | SR-18 |
| T-09.2 | Write the failing test: an audit record cannot be updated | 2 | DoD 2 |
| T-09.3 | Write the failing test: an audit record cannot be deleted | 1 | DoD 2 |
| T-09.4 | Block update and delete at the data-access layer | 5 | SR-19 |
| T-09.5 | Emit audit records from every state-changing route | 8 | SR-18 |
| T-09.6 | Verify origin and outcome are captured on failures too | 3 | SR-18 |
| | **Total** | **22 h** | |

**T-09.4 is the task that carries the requirement.** Hiding the operations in
the interface would have satisfied a casual reading; blocking them at the
data-access layer makes the guarantee bind code that has not been written yet.
A route added in Sprint 3 by an author who never read this chapter still
cannot rewrite history.

**Table 6.3 - US-04 (register an exhibit) decomposed**

| Task | Description | Est. (h) | Realises |
|---|---|---|---|
| T-04.1 | Accept an upload and reject disallowed kinds | 4 | SR-10 |
| T-04.2 | Allocate a system-unique identifier | 2 | SR-11 |
| T-04.3 | Derive and store the intake fingerprint | 3 | SR-13 |
| T-04.4 | Extract embedded metadata | 4 | SR-14 |
| T-04.5 | **Create the first custody record in the same transaction** | 5 | SR-12 |
| T-04.6 | Test that a failure leaves neither record behind | 3 | DR-01 |
| | **Total** | **21 h** | |

T-04.5 and T-04.6 together realise DR-01. If the exhibit could be written and
the custody record fail, an exhibit would exist with no established origin -
inadmissible, and silently so.

## 6.4 Design and Models

**Table 6.4 - Models produced or revised in this sprint**

| Figure | Kind | What it settled |
|---|---|---|
| 1 | Use case, overview | Four actors, the specialisation hierarchy, 41 operations |
| 3 | Use case, reading | The base actor's 20 use cases |
| 4 | Use case, analysis | What each role adds |
| 5 | Class, domain | Six entities with behaviour |
| 6 | Class, persistent | The schema as stereotyped classes |
| 8 | Package | Five layers, dependencies downward only |
| 19 | Activity, partitions | Registration across the layers, including both refusal paths |
| 21 | Profile | The stereotypes the model uses |

**Figure 19** is the one to read for this sprint. It shows registration
crossing four partitions and, crucially, the two paths that end in refusal -
function not entitled, content not matching its declared kind - each of which
writes to the audit trail before stopping. A refusal that is not recorded is
indistinguishable from an attempt that never happened.

## 6.5 Implementation

Ten blueprints and six model modules. Two decisions made here constrained
everything after.

**Business logic was separated from the interface from the first commit**, not
retrofitted. The layering in Figure 8 was a Sprint 0 decision and this sprint
honoured it; by Sprint 6 that separation had become a tested requirement
(SNF-11, SNF-12) rather than a convention.

**Authorisation was placed at the route, never only in the template.** Hiding
a button does not protect an operation. This was the right instinct and it
was still applied incompletely - the gap it left is the subject of Chapter 9.

## 6.6 Verification

**Table 6.5 - Tests written in Sprint 1**

| Area | Cases | Notable |
|---|---|---|
| Authentication | 6 | Identical failure message for unknown account and wrong secret |
| Authorisation by function | 7 | One per role per protected operation |
| Investigation lifecycle | 5 | Closure destroys nothing |
| Registration | 8 | Includes a disguised executable, and the atomicity case |
| Custody | 5 | First record created with the exhibit |
| Audit | 4 | Update and delete both raise at the data layer |
| Formula checks | 4 | Interval, repetition, function mismatch |

## 6.7 Burndown

**[FIGURE 6.1 - Sprint 1 burndown]**

The line is flat through day two and only meets the ideal from day nine. The
cause is not estimation error in the stories themselves but **work the
estimate did not contain**: environment setup, the schema, and wiring the
audit listeners. Scaffolding is real work.

## 6.8 Sprint Review

**Table 6.6 - Acceptance against the stories' criteria**

| Story | Criterion | Outcome |
|---|---|---|
| US-01 | Failure reveals nothing about which field was wrong | Met |
| US-02 | Every protected operation refuses the wrong function | Met |
| US-03 | Closure destroys no data | Met |
| US-04 | No exhibit can exist without a custody record | Met |
| US-05 | Intake fingerprint stored and never altered | Met |
| US-06 | Content contradicting its declared kind is refused | Met |
| US-07 | Description editable, content and fingerprints not | Met |
| US-08 | Handover records parties, moment, place, reason | Met |
| US-09 | History cannot be amended or removed | Met |
| US-10 | Interval, repetition and mismatch surfaced | Met |
| US-11 | No route creates an account except an administrator's | Met |

All forty points accepted.

## 6.9 Retrospective

**What worked.** Writing the audit listeners before the routes that would
depend on them. Treating authorisation as a route concern.

**What did not.** The estimate contained the features and not the foundation
they stand on. And the models drifted from the code within days of being
drawn, because nothing required them to move together.

**Table 6.7 - Actions carried into Sprint 2**

| # | Action | Where it shows |
|---|---|---|
| A1 | Reserve a day-zero design spike for the graph algorithm, estimated separately | Table 4.12, task T-13.1 |
| A2 | Fix the canonical signature payload before any signing code is written | §7.5 |
| A3 | **Add "diagrams updated in the same commit" to the Definition of Done** | Table 4.8, condition 7 |

Action A3 is the one with the longest reach: it is why the diagrams in this
report are generated from versioned source rather than redrawn, and therefore
why no figure here can contradict the code it describes.

---

\newpage
