# Chapter 9 - Sprints 4 and 5: Maintenance

*Sprint 4 (M1): 5 days · 10 points · access scoping*
*Sprint 5 (M2): 6 days · 11 findings · defect repair*

---

At the end of Sprint 3 the system delivered every committed point, passed
every test, and satisfied every stated acceptance criterion. Two further
sprints were nonetheless necessary. **They are the most informative chapters
in this report, because a process that only ever succeeds demonstrates
nothing about its capacity to detect failure.**

The two sprints found their defects by different means, and that difference is
the point: Sprint 4 found what *testing differently* finds, Sprint 5 found
what *reading* finds.

---

# Sprint 4 (M1) - Access Scoping

## 9.1 How the Defect Was Found

Retrospective action C3 - adversarially test the authorisation boundary - was
carried out. A second account was created with no shared investigations, and
every aggregate view was requested as that account.

**Table 9.1 - What the adversarial pass found**

| Surface | Expected | Actual |
|---|---|---|
| Case list | Own investigations | Own investigations - **correct** |
| Evidence detail | Refused | Refused - **correct** |
| Dashboard totals | Own investigations | **Every investigation in the system** |
| Risk ranking | Own investigations | **Every exhibit in the system** |
| Anomaly view | Own investigations | **Every exhibit in the system** |
| Assistant answers | Own investigations | **Retrieved globally** |
| Export | Own investigations | Refused - correct |

Detail views were protected. Aggregates were not. A user could not open
another investigation's evidence item, but could see its title in a risk
ranking, its count in a dashboard total, and could ask the assistant about it.

## 9.2 Why This Was a Change Request, Not a Defect

No requirement then in force had been broken. UR-03 existed - *"a person must
see only the investigations they have been assigned to"* - but the system
requirements realising it addressed **record access** and never enumerated
aggregates.

**The implementation satisfied its specification. The specification was
incomplete.** Classifying this as a defect would blame the code for a gap in
the requirements, which is both unfair and diagnostically useless: it would
lead to fixing six routes rather than to understanding why six routes were
missed.

It therefore entered the backlog as **new scope**: US-28 and US-29, backlog
v2.0, 10 points.

## 9.3 Sprint Backlog

**Table 9.2 - US-28 (scoped aggregates) decomposed**

| Task | Description | Est. (h) | Realises |
|---|---|---|---|
| T-28.1 | **One function answering "which investigations may this account see"** | 3 | SR-51 |
| T-28.2 | Route every aggregate through it: dashboard, risk, anomaly, export | 6 | SR-51 |
| T-28.3 | Compose each role's overview from panels matched to its work | 5 | SR-52 |
| T-28.4 | Explanatory empty state for an account assigned to nothing | 3 | SR-52 |
| T-28.5 | Adversarial tests: every aggregate, as each of four roles | 6 | C3 |
| | **Total** | **23 h** | |

**Table 9.3 - US-29 (scoped assistant) decomposed**

| Task | Description | Est. (h) | Realises |
|---|---|---|---|
| T-29.1 | **Move scoping before retrieval, not after generation** | 5 | SR-41 |
| T-29.2 | Answer identity questions from the authenticated session | 3 | SR-53 |
| T-29.3 | Attribute retained conversation to its owner | 2 | SR-54 |
| T-29.4 | Discard conversation on entry as well as departure | 2 | SR-54 |
| T-29.5 | Tests: a question about an unassigned investigation | 4 | C3 |
| | **Total** | **16 h** | |

T-28.1 and T-29.1 are the repair; the rest is consequence. **A rule expressed
once can be applied everywhere; a rule expressed inline in each route will be
omitted by the next route.** The single function is the abstraction the
original design lacked, and Figure 9 shows it: every component that reads
case-scoped data depends on one provider.

## 9.4 The Empty State

T-28.4 produced something the original design would never have contained. An
account assigned to no investigation previously saw a dashboard of global
totals; correctly scoped, it would see zeroes.

Zeroes are ambiguous - they could mean "nothing exists" or "nothing is yours".
The empty state explains the situation and says what to do. **A security
constraint forced an interface case to be designed rather than ignored.**

## 9.5 Burndown and Review

**[FIGURE 9.1 - Sprint 4 burndown]**

Short and near-linear; scope was fixed by two change requests with no
discovery work.

**Table 9.4 - Acceptance**

| Criterion | Outcome |
|---|---|
| No aggregate returns a record from an unassigned investigation | Met - 14 adversarial tests |
| Each role's overview is composed for its work | Met |
| An account assigned to nothing sees an explanation | Met |
| A question about an unassigned investigation is refused | Met |
| Refusal is structural: the data never enters the prompt | Met |

## 9.6 Retrospective

**The lesson.** Positive functional tests, however thorough, do not exercise
authorisation boundaries. Ninety-three tests were written in Sprint 3 and not
one asked what an unentitled user receives.

**The second lesson, which generalises further.** A rule applied inline will
be applied inconsistently. The defect was not six mistakes; it was one missing
abstraction, six times.

**Table 9.5 - Actions**

| # | Action |
|---|---|
| D1 | Adversarial authorisation testing becomes standing practice, not a one-off |
| D2 | Any rule governing more than one surface must have exactly one implementation |

---

# Sprint 5 (M2) - Defect Repair

## 9.7 How These Defects Were Found

By **reading the code against its intent**, module by module - not by running
it. The suite was green throughout this sprint, before and after.

**Table 9.6 - The eleven findings**

| ID | Severity | Finding | Root cause |
|---|---|---|---|
| D1 | High | Removing an exhibit destroyed its custody and audit history | Deletion treated as a data operation, not a domain one |
| D2 | High | Verification computed a verdict but never stored it, so the assessment's highest-weighted indicator stayed at its default | Two algorithms sharing a value with no owner for writing it |
| D3 | High | An evidence item was reachable by identifier without checking its investigation | Access checked on the parent route, not the object |
| D4 | Medium | Soft-deleted exhibits still appeared in aggregate counts | The exclusion was applied in listings but not in totals |
| D5 | Medium | Responses carried no content-origin or framing directives | Never specified, therefore never built |
| D6 | Medium | A production configuration with default secrets would start | The check existed for one secret, not all |
| H1 | **High** | Text stored in a conversation was rendered as markup | Model output treated as trusted because it is not user input |
| H2 | Medium | Rate limiting absent on the most expensive endpoint | Cost not considered a security property |
| H3 | Medium | Private keys stored unencrypted at rest | Encryption applied to content, not to credentials |
| R1 | Low | Repeated query inside a loop over custody records | Correctness-first implementation never revisited |
| R2 | Low | Diagram source and code had drifted in two places | DoD condition 7 added mid-project, not applied retroactively |

## 9.8 The Finding That Matters Most

**H1 - stored text rendered as markup.** The conversation transcript inserted
reply text into the page as markup. The reasoning that produced the defect is
worth stating because it is so plausible: *the text comes from the model, not
from the user, so it is not user input.*

But the model's reply contains whatever the retrieved records contain, and the
records contain whatever an investigator typed into a case title. **Untrusted
text does not become trusted by passing through a language model.**

The repair escapes the text before it is inserted. Its sequel is recorded in
Chapter 10: the repair was made and **no test was written**, so the fix could
have been deleted and the entire suite would still have passed. That omission
was not found until Sprint 6.

## 9.9 Why These Are Defects and Carry No Points

Each of the eleven restores a requirement already accepted. D1 restores DR-03,
D2 restores SR-56's intent, H1 restores SNF-17. Estimating them in story
points would count the same capability twice and inflate velocity, so they are
tracked by **findings closed** instead.

**[FIGURE 9.2 - Sprint 5 defect burndown]**

## 9.10 Review and Retrospective

All eleven repaired; each has a regression test **except H1**, which is the
subject of Chapter 10.

**The lesson.** A green test suite can coexist with critical defects. Testing
and reading find different classes of error, and this sprint found a class
that no amount of running the suite would have surfaced - because every one of
these defects was a case the tests did not know to ask about.

**Table 9.7 - Actions**

| # | Action |
|---|---|
| E1 | Periodic structured review adopted as complementary to testing, not as a substitute |
| E2 | A repaired defect requires a regression test before it is closed |

**Action E2 was adopted and then not applied to H1 in the same sprint.** That
is recorded here rather than quietly corrected, because the gap between
adopting a practice and applying it is exactly what Sprint 6 exists to close.

---

\newpage
