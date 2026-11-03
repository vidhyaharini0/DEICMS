# Chapter 7 - Sprint 2: Integrity

*15 working days · 38 points committed · 38 delivered*

---

## 7.1 Sprint Goal

**A custody history that can be proved sound or shown precisely where it is
not, and an exhibit that can move only as its procedure permits.**

This is the sprint in which the project stops being a records system and
becomes the thing it was proposed as. Three of the five Category C algorithms
are built here.

## 7.2 Backlog Refinement Before Planning

Refinement produced backlog **v1.1** (Table 4.10), with two changes:

| Change | Cause |
|---|---|
| US-13 re-estimated from 8 to **13** | The day-zero spike (retrospective action A1) showed the traversal was larger than a first reading suggested |
| US-16 and US-17 **split out** of US-13 and US-15 | Presenting a result is distinct work from computing one, and bundling them hid two points of interface work inside an algorithm story |

**The re-estimate is the retrospective working.** A1 existed because Sprint 1
underestimated foundation work; applying it to US-13 caught a second
underestimate before it became a plateau.

**Table 7.1 - Sprint 2 backlog**

| ID | Story | Pts | Realises | Category |
|---|---|---|---|---|
| US-12 | Custody records attributable to their author | 5 | SR-23, SR-24 | B |
| US-13 | Verify the whole custody history | **13** | SR-25 to SR-27 | **C** |
| US-14 | Exhibits move only through permitted states | 8 | SR-28 to SR-30 | **C** |
| US-15 | Reconstruct missing custody links | 8 | SR-31 to SR-33 | **C** |
| US-16 | Read a verification result | 2 | SR-34 | A |
| US-17 | Read a reconstruction | 2 | SR-35 | A |
| | **Total** | **38** | | |

## 7.3 Sprint Backlog: Tasks

US-13's decomposition is given in full in **Table 4.12** as the worked example
of the product-backlog-to-task chain. Two further decompositions matter here.

**Table 7.2 - US-12 (attributable custody records) decomposed**

| Task | Description | Est. (h) | Realises |
|---|---|---|---|
| T-12.1 | **Fix the canonical payload: six fields, deterministic ordering** | 3 | A2 |
| T-12.2 | Sign at creation using the creator's private means | 4 | SR-23 |
| T-12.3 | Verify against the signer's public means | 3 | SR-23 |
| T-12.4 | Make the signature column non-nullable | 1 | SR-24 |
| T-12.5 | Test that an altered field fails verification | 3 | DoD 2 |
| | **Total** | **14 h** | |

T-12.1 is retrospective action A2 discharged. **The bytes signed at creation
must be identical to the bytes reconstructed at verification**, so the
serialisation is fixed with deterministic key ordering before any signing code
exists. Settling this first avoided the class of defect where signatures
verify in tests and fail in production because a field order changed.

**Table 7.3 - US-14 (lifecycle enforcement) decomposed**

| Task | Description | Est. (h) | Realises |
|---|---|---|---|
| T-14.1 | Express the policy as a transition table, not as branching code | 5 | SR-28 |
| T-14.2 | Gate 1: the pair must exist | 2 | SR-28 |
| T-14.3 | Gate 2: the function must be permitted | 3 | SR-28 |
| T-14.4 | Gate 3: every precondition must hold | 5 | SR-29 |
| T-14.5 | Gate 4: a justification must be supplied | 2 | SR-30 |
| T-14.6 | Name the exact unmet condition in every refusal | 3 | SR-29 |
| T-14.7 | **Audit refusals as readily as successes** | 2 | SR-29 |
| T-14.8 | Re-assess risk immediately after a successful transition | 3 | SR-30 |
| T-14.9 | Tests: every permitted transition, and one refusal of each kind | 6 | DoD 2 |
| | **Total** | **31 h** | |

## 7.4 Design and Models

**Table 7.4 - Models produced in this sprint**

| Figure | Kind | Algorithm |
|---|---|---|
| 12 | Sequence | Integrity verification |
| 23 | Activity | Integrity verification |
| 10 | Composite structure | Internals of the verification engine |
| 15 | State machine | The evidence lifecycle |
| 24 | Activity | The transition validation pipeline |
| 18 | Activity | Chain reconstruction |
| 25 | Sequence | Chain reconstruction |

The algorithms themselves are described in **Chapter 11**, sections 11.2, 11.4
and 11.5, rather than repeated here. This chapter records what the sprint
*cost* and what it *learned*; Chapter 11 records what the algorithms *are*.

## 7.5 The Design Change That Defined the Sprint

On day five the verification engine was complete and passing its tests. It
stopped at the first failure.

That satisfied US-13's first acceptance criterion and violated its second,
which required **every** failing node to be located. The discovery occurred
because T-13.6 had been written as a separate task - "accumulate failures
without halting the walk" - which forced the question of what happens after a
failure to be answered explicitly rather than by default.

The rework consumed days five to seven and is visible as the plateau in the
burndown. It cost three days and was discovered on day five rather than at
delivery. **A plan-driven process would have frozen the stop-at-first design
in the specification phase and discovered the mismatch during acceptance
testing**, with the whole dependent interface built on top of it.

This is the single clearest piece of evidence for the process choice of
Section 4.1.3, and Chapter 13 returns to it.

## 7.6 Verification

**Table 7.5 - Tests written in Sprint 2**

| Area | Cases | Notable |
|---|---|---|
| Signing and verification | 4 | An altered field fails; an unsigned record cannot be stored |
| Integrity: clean chain | 2 | Intact at 100% completeness |
| Integrity: single failures | 3 | One per check kind: content, authorship, order |
| Integrity: **multiple failures** | 1 | Three failures, all three reported in one run |
| Lifecycle: permitted | 5 | Representative transitions across all six states |
| Lifecycle: refused | 3 | Pair absent, function denied, precondition unmet |
| Lifecycle: auditing | 1 | A refusal appears in the audit trail |
| Reconstruction | 4 | Complete chain, resolvable gap, no candidate, below threshold |

The multiple-failure test is the acceptance criterion made executable. It is
the test that would have failed on day five.

## 7.7 Burndown

**[FIGURE 7.1 - Sprint 2 burndown]**

Flat across days five to seven - the traversal rework - then steeper than
ideal to the end. The shape says something the totals cannot: **the work was
not uniformly difficult, and the difficulty was not where it was expected.**
The cryptographic signing that looked hard was library calls; the traversal
semantics that looked simple were the real work.

## 7.8 Sprint Review

**Table 7.6 - Acceptance against the stories' criteria**

| Story | Criterion | Outcome |
|---|---|---|
| US-12 | Authorship establishable; alteration detectable | Met |
| US-12 | An unsigned custody record cannot exist | Met |
| US-13 | Reports a verdict and a completeness proportion | Met |
| US-13 | **Locates every failure, not the first** | Met *after rework* |
| US-14 | Only permitted transitions succeed | Met |
| US-14 | A refusal names the exact unmet condition | Met |
| US-14 | Refusals are audited | Met |
| US-15 | Gaps detected; candidates scored; threshold respected | Met |
| US-15 | An inferred link is never presented as confirmed | Met |
| US-16, US-17 | Results readable, and available as data | Met |

All thirty-eight points accepted.

## 7.9 Retrospective

**What worked.** The day-zero spike (A1). Fixing the canonical payload before
writing signing code (A2) - no signature defect occurred in this sprint or
any later one.

**What did not.** The acceptance criteria for US-13 were written in prose and
read loosely. Had the second criterion existed as a *test* before the
implementation, the stop-at-first design would have failed immediately rather
than passing for five days.

**Table 7.7 - Actions carried into Sprint 3**

| # | Action | Where it shows |
|---|---|---|
| B1 | **Write acceptance criteria for Category C stories as failing tests before implementation** | §8.3; the normalisation and cap tests |
| B2 | Keep the external model behind a testable seam from the start | §8.5 |
| B3 | Estimate presentation work separately from the algorithm that produces it | Backlog v1.1, already applied |

Action B1 is the most consequential action taken in the project. Sprint 3's
burndown is the direct result, and Section 8.9 assesses it.

---

\newpage
