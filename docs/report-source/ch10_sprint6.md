# Chapter 10 - Sprint 6: Quality Enforcement

*8 working days · 23 points committed · 23 delivered*

---

## 10.1 Why There Is a Sixth Sprint

Sprint 6 began with an audit of the eighteen non-functional requirements,
checking each against the code that enforced it and the test that would fail
if that enforcement were removed.

**Table 10.1 - State of the eighteen quality requirements before Sprint 6**

| Verdict | Count |
|---|---|
| Implemented **and** automatically tested | **8** |
| Implemented but never tested | 7 |
| Asserted analytically, never measured | 2 |
| **Claim did not match the code** | 1 |

Nine of eighteen named only code review, configuration inspection, a manual
check or an analytical argument as their verification method. A verification
method that does not re-run cannot fail, and a requirement that cannot fail is
not a requirement.

## 10.2 Sprint Goal

**Every quality requirement carries a measurement, a value that constitutes a
pass, and a test that applies it - so that removing an enforcement breaks a
test rather than going unnoticed.**

## 10.3 Backlog Refinement

Backlog **v3.0**: seven stories, 23 points (Table 4.10a). Capacity was set at
the mean of Sprints 1 to 3 (40), reduced for a short fixed window.

**Table 10.2 - Sprint 6 backlog**

| ID | Story | Pts | Realizes |
|---|---|---|---|
| US-30 | Quality requirements carry a measurement and a pass value | 5 | Table 3.7 |
| US-34 | Algorithmic cost measured rather than argued | 5 | SNF-07 to SNF-09 |
| US-31 | Transport and session hardening verified | 3 | SNF-15, SNF-16 |
| US-32 | Unsafe production configuration refused, and the refusal exercised | 3 | SNF-18 |
| US-33 | Listings bounded as data grows | 3 | SNF-10 |
| US-35 | Role interfaces demonstrably distinct | 2 | SNF-21 |
| US-36 | The injection repair guarded by a test | 2 | SNF-17 |
| | **Total** | **23** | |

## 10.4 US-30: Making the Quality Requirements Real

The eighteen quality requirements were rewritten as the two-level set of
Chapter 3: nine **user** quality requirements, deliberately unmeasurable and
expressed in the stakeholder's language, and twenty-one **system** quality
requirements, each carrying a measurement method, an acceptance criterion and
a named test.

**Table 10.3 - The same requirement, before and after**

| | Before | After |
|---|---|---|
| Statement | "Listings shall remain responsive as data grows" | **UNF-05** (user): the system must respond quickly enough not to interrupt an investigator's work. **SNF-10** (system): no listing shall render in time proportional to the whole collection |
| Measurement | - | Create 45 investigations and 45 exhibits; request each listing |
| Acceptance | "Case and evidence listings paginated" | At most 20 rows rendered per page; navigation present |
| Verified by | *Manual* | `test_nfr::TestListingResponsiveness` |

## 10.5 US-33: The Requirement That Was Simply False

The original NFR-17 claimed *"case **and evidence** listings paginated"*.
Investigations paginated at 20 and audit records at 25. The evidence listing
inside an investigation did not paginate at all:

```
evidence_items = (case.evidence_items
              .filter_by(is_deleted=False)
              .order_by(EvidenceItem.created_at.desc())
              .all())
```

An investigation with four hundred exhibits would render four hundred rows.

The repair changed the code rather than the requirement. Softening the
requirement to match the implementation would have been the smaller edit, but
an exhibit-heavy investigation is the realiztic case for a forensic system
rather than an edge case.

## 10.6 US-34: Complexity Measured Rather Than Argued

The claims that verification is linear in chain size and assessment linear in
record count were supported by analysis alone. Analysis cannot regress.

The tests now build chains at two sizes an order of magnitude apart, time
both, and assert the **growth ratio**:

| Claim | Measurement | Pass |
|---|---|---|
| Verification linear in chain size | 20 and 200 elements, best of three | Tenfold size under thirtyfold time |
| Assessment linear in record count | 20 and 200 records, best of three | Tenfold records under thirtyfold time |
| A 100-element chain verifies within tolerance | Single run | Under 5 seconds |

The thresholds are deliberately loose: they detect a change in the shape of
the cost rather than certifying a particular machine's speed. A quadratic
implementation would require roughly a hundredfold increase and would fail.

## 10.7 US-36: The Regression Test That Should Have Existed

Finding H1 in Sprint 5 - text rendered as markup - was repaired and closed
with no test, in a sprint whose own retrospective action E2 required one.

In consequence the escape function could have been deleted and all 172 tests
would still have passed: a defect found, understood, documented and repaired
was protected by nothing.

Three tests now guard it: an investigation title containing markup renders
escaped; stored conversation cannot close the element containing it; and the
escape helper is asserted to run *before* insertion rather than merely to
exist.

Sprint 5's retrospective had recorded that a repaired defect requires a
regression test before it is closed. The practice was adopted and, in the same
sprint, not applied to the defect that prompted it.

## 10.8 US-31, US-32, US-35: Enforcement Made Visible

| Story | Enforcement that existed | Test that now guards it |
|---|---|---|
| US-31 | Session token restricted; four response directives sent | 10 tests, on both unauthenticated and authenticated responses |
| US-32 | Production refuses absent or weak secrets | 6 tests, against absent, weak and sound configurations |
| US-35 | Four role-specific overviews | 7 tests, including that all four renderings differ |

US-32 required a small refactor. The check ran as inline code at import time,
executing once per process and never exercisable against a hypothetical bad
configuration; extracting it into a function made the requirement testable.
Correct code is not sufficient if the requirement governing it cannot be
exercised.

## 10.9 A Defect Found During the Sprint

Reviewing the use-case model against the routes revealed that
`GET /evidence/<id>/verify` had **no role guard**, and is not a read: it
writes the verdict onto the exhibit and, on a Broken verdict, drives it to
Flagged through a transition that deliberately bypasses the role check.

A Read-Only Viewer could therefore change an exhibit's lifecycle state,
contradicting SR-06.

**Table 10.4 - Root cause**

| | |
|---|---|
| Classified by | Its **name**: "verify" sounds like a read |
| Should have been classified by | Its **effect**: it writes |
| Repair | Analysis guard on verification and reconstruction; refused at the route, hidden in the interface |
| Guarded by | 6 tests, including that a Read-Only account changes neither the verdict nor the state |

This is the same shape as M1 and M2: a correct algorithm in a context whose
constraints it did not know about (Section 11.9).

## 10.10 Burndown and Review

**[FIGURE 10.1 - Sprint 6 burndown]**

Day four is flat: US-33 could not be tested until the evidence listing was
actually paginated, so a requirement had to be **met** before it could be
**verified**.

**Table 10.5 - Acceptance**

| Criterion | Outcome |
|---|---|
| Every system quality requirement names a measurement and an acceptance value | Met - 21 of 21 |
| Every system quality requirement names an automated test | Met - 21 of 21 |
| Removing an enforcement breaks a test | Met - verified by deleting each and observing the failure |
| The suite still runs without network access | Met |

**Table 10.6 - The suite before and after**

| | Before | After |
|---|---|---|
| Tests | 172 | **216** |
| Quality requirements with an automated test | 8 of 18 | **21 of 21** |
| Fixed defects without a regression test | 1 (H1) | 0 |

## 10.11 Retrospective

**The lesson.** A requirement and its verification form one artifact. Treating
them separately allows a specification to describe a quality the system does
not possess, undetected until something checks.

**Process observation.** Sprints 4, 5 and 6 each arose from a defect found by
a different means: adversarial testing, structured code reading, and a review
against the specification. In no case did a sprint find its own defects, which
is the condition that makes successive increments necessary.

**Table 10.7 - Actions**

| # | Action |
|---|---|
| F1 | A quality requirement is not accepted without a measurement, a pass value and a test |
| F2 | An operation is classified by its effect, never by its name |
| F3 | Before any release, re-derive the authorization matrix from the routes rather than from the design |

---

\newpage
