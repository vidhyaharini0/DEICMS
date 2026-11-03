# Chapter 12 - Verification and Validation

---

## 12.1 Strategy

Verification asks whether the system was built right; validation asks whether
the right system was built. The project answers the two with different
confidence: verification is extensive, while validation is limited by the
absence of a customer (Section 12.8).

The test strategy follows the **V-model's pairing of construction phases with
test levels** - adopted as a test strategy while its sequencing was rejected
as a lifecycle (Section 4.1.2).

**Table 12.1 - Construction phase paired with test level**

| Construction phase | Paired test level | Where it lives |
|---|---|---|
| System requirements (Ch. 3) | Acceptance tests against acceptance criteria | Each sprint review |
| Architecture (Ch. 5) | Architectural boundary tests | `test_nfr::TestArchitecturalBoundaries` |
| Module design (Ch. 11) | Unit tests per algorithm | `test_increment2`, `test_increment3` |
| Implementation | Integration tests across modules | `test_integration` |
| Quality requirements (§3.7) | Measurement against acceptance values | `test_nfr` |

## 12.2 The Suite

**Table 12.2 - 216 tests by module**

| Module | Tests | Covers |
|---|---|---|
| `test_increment3` | 93 | Risk assessment, assistant, second factor, encryption, export |
| `test_increment2` | 17 | Signing, integrity verification, lifecycle, reconstruction |
| `test_integration` | 16 | End-to-end flows across modules |
| `test_scoping` | 14 | Adversarial authorisation across every aggregate |
| `test_day2` | 12 | Early foundation behaviour |
| `test_increment1` | 10 | Authentication, authorisation, registration, audit |
| `test_intent_classifier` | 10 | Seven intents, UNKNOWN, tie-breaking |
| **`test_nfr`** | **44** | **All 21 system quality requirements** |
| **Total** | **216** | |

The suite requires **no network access** (SNF-20), which is what allows the
assistant pipeline to be tested at all: the model sits behind a seam that
tests substitute, a decision taken as retrospective action B2 in Sprint 2.

## 12.3 Coverage

Measured over the whole suite.

**Table 12.3 - Coverage by area**

| Area | Statements | Covered | Reading |
|---|---|---|---|
| **Category C algorithms** | 892 | **80%** | The project's own logic, deliberately the focus |
| Category B wrappers | 193 | 94% | Small surfaces, easily exercised |
| Domain models | 225 | 87% | Constraints and guards |
| Routes and interface | 1,161 | 71% | Form handling and rendering paths |
| Other | 194 | 81% | Application setup, formulae, validators |
| **Total** | **2,665** | **78%** | |

**Table 12.4 - The five Category C modules individually**

| Module | Coverage | Comment |
|---|---|---|
| `risk_scoring.py` | **97%** | Every indicator, every rule and the cap tested individually |
| `graph_integrity.py` | **91%** | Each check kind, plus the multiple-failure case |
| `state_machine.py` | 83% | Every permitted transition and one refusal of each kind |
| `ai_assistant.py` | 72% | Prompt-template branches per intent are numerous |
| `chain_reconstruction.py` | **65%** | **The lowest in the project** |

### 12.3.1 Why reconstruction is the least covered

`chain_reconstruction.py` reaches 65% because its plausibility function has
four criteria, each of which may be present or absent depending on the data
available, giving sixteen combinations of live criteria before the threshold
decision is even reached. The tests cover the four that occur in realistic
data and the two boundary cases either side of the threshold; the remainder
are untested.

The gap is a genuine limitation and forms the first entry in Section 13.4's
future work.

### 12.3.2 Why route coverage is lower

Routes sit at 71%, pulled down by `auth.py` (44%), `evidence.py` (56%),
`admin.py` (59%) and `cases.py` (59%). The uncovered paths are predominantly
form re-rendering after validation failure and template branches.

Testing effort was directed at the algorithms rather than at rendering paths.
A rendering defect is visible to the first user who encounters it, whereas an
algorithmic defect in a custody verifier may be both invisible and
consequential.

## 12.4 Testing the Quality Requirements

Before Sprint 6, nine of eighteen quality requirements named only code review,
configuration inspection, a manual check, or an analytical argument.

**Table 12.5 - Quality verification, before and after Sprint 6**

| | Before | After |
|---|---|---|
| Quality requirements | 18 | 21 (user and system levels separated) |
| With an automated test | **8** | **21** |
| Verified by "manual" or "code review" | 9 | 0 |
| Complexity claims measured rather than argued | 0 | 3 |
| Fixed defects without a regression test | 1 | 0 |

Section 10.1 records how this was found, and Section 3.7 is the resulting
table.

## 12.5 Adversarial Testing

Introduced after Sprint 3's defect (Chapter 9) and now standing practice.

**Table 12.6 - What adversarial tests ask that functional tests do not**

| Functional test asks | Adversarial test asks |
|---|---|
| Does an entitled user get the right answer? | What does an **unentitled** user get? |
| Does the operation succeed? | Does it fail **closed**, and is the failure recorded? |
| Is the record protected? | Is the **aggregate over** the record protected? |
| Was the defect fixed? | Would the fix's **removal** break a test? |

The fourth row is the one Sprint 6 added, and it is the one that caught the
unguarded verification route and the five-sprint-old repair with no test.

## 12.6 Validation Against Acceptance Criteria

Each sprint review judged its stories against criteria written before
implementation. From Sprint 3 onward, Category C criteria existed as **failing
tests** before any implementation (retrospective action B1).

**Table 12.7 - Acceptance outcome by sprint**

| Sprint | Stories | Accepted | Notes |
|---|---|---|---|
| 1 | 11 | 11 | - |
| 2 | 6 | 6 | US-13 accepted only after the traversal rework (§7.5) |
| 3 | 10 | 10 | All criteria met; the scoping defect was outside them |
| 4 (M1) | 2 | 2 | - |
| 5 (M2) | 11 findings | 11 | Ten with regression tests; H1 without, until Sprint 6 |
| 6 (M3) | 7 | 7 | - |

Sprint 3 met every criterion while leaving a defect in every aggregate it had
built, because no criterion addressed an unentitled user. Acceptance criteria
verify what they describe and nothing further.

## 12.7 What Is Not Tested

**Table 12.8 - Untested areas, and the risk each carries**

| Area | Why not tested | Risk carried |
|---|---|---|
| Concurrency | Single-process development; no load harness | Sequential identifier allocation is unverified under concurrent registration |
| Load and volume | No performance environment | Measured scaling is analytic-scale, not production-scale |
| Penetration testing | Out of scope and beyond the author's competence to do credibly | Controls are tested individually, not probed as a whole |
| Live model behaviour | The suite forbids network access | Only the pipeline is verified, never a real reply |
| Real users | No external customer | Usability is argued, never observed |
| Browser rendering | No browser automation | Interface behaviour verified server-side only |

The last two bear on validation rather than verification, which is the subject
of the next section.

## 12.8 The Limit of Validation in This Project

Verification is extensive: 216 tests, every requirement traced to at least
one, every quality requirement measured.

Validation is correspondingly weak, and testing does not repair it. The
project had no customer. Requirements were derived from domain sources and
from reasoning about what a forensic process demands, rather than from a
stakeholder able to say that a requirement had been misunderstood, and every
acceptance criterion was written by the same person who implemented the code
and judged the result.

The system can therefore be shown to satisfy its requirements, while the
requirements cannot be shown to be the right ones. Section 3.10 gives one case
in which they were not - a negative requirement scoped to fewer surfaces than
it governed - found by adversarial testing, the substitute available to a
project without a customer.

The limitation follows from the conditions of the exercise rather than from
any deficiency in the system.

---

\newpage
