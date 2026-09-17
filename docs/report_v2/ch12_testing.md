# Chapter 12 — Software Testing and Quality Assurance

---

## 12.1 Testing Objectives and Philosophy

### 12.1.1 The Two Goals of Testing

Program testing has two distinct goals, and conflating them is the commonest way a test suite becomes falsely reassuring.

The first goal is **to demonstrate to the developer and the customer that the software meets its requirements**. For custom software this means there should be at least one test for every requirement in the requirements document. This goal leads to **validation testing**: the system is expected to perform correctly on a set of test cases reflecting its expected use, and a successful test is one that shows the system operating as intended.

The second goal is **to discover situations in which the behaviour of the software is incorrect, undesirable, or does not conform to its specification**. This goal leads to **defect testing**, in which test cases are designed to *expose* defects. Such cases may be deliberately obscure and need not reflect normal use. Here a successful test is one that **makes the system perform incorrectly** and so exposes a defect.

**Table 12.1 — The two goals, and where each is served in DEICMS**

| | Validation testing | Defect testing |
|---|---|---|
| Purpose | Demonstrate the software meets its requirements | Discover faults where behaviour does not conform |
| Test cases reflect | Expected use | Deliberately obscure conditions |
| A *successful* test | Shows the system operates as intended | Makes the system fail |
| In DEICMS | The increment test modules; the integration module's full workflows; sprint-review demonstrations against acceptance criteria | The adversarial scoping module; boundary cases in the algorithm tests; the M2 review pass |

The project's own history makes the distinction concrete. At the end of Increment 3 the validation testing was thorough and entirely green — and two critical defects and a pervasive authorisation leak were nonetheless present, because **no test had been written whose success would consist of the system failing**. Sections 12.4 and 12.5 describe the defect testing that was then added.

### 12.1.2 Verification, Validation and Quality Assurance

Three terms are routinely confused and are distinguished here.

**Table 12.2 — Verification, validation and quality assurance**

| Term | Question | In DEICMS |
|---|---|---|
| **Verification** | *Are we building the product right?* Does the software meet the specification? | The 172 automated tests |
| **Validation** | *Are we building the right product?* Does the software meet the user requirements? | Sprint reviews, at which each story was demonstrated against its acceptance criteria |
| **Software quality assurance** | Not the same as testing: creating and enforcing standards and methods that improve the process and **prevent** defects occurring | The definition of done (Table 4.8), the coding standards (Table 10.2), and the four-level QA strategy (Table 6.6) |

The aim of verification and validation together is to establish confidence that the system is **fit for purpose**. That confidence level is not absolute; it depends on the software's purpose, on user expectations, and on the marketing environment. For DEICMS the purpose is forensic, so the confidence bar is set high for integrity and authorisation and deliberately lower for, say, dashboard layout — a prioritisation made explicit in Table 2.3 and visible in the coverage distribution of Section 12.8.

### 12.1.3 The Testing Axioms

Nine axioms govern testing. They are not proved; they are the starting assumptions from which sensible testing practice follows. Table 12.3 states each and records how DEICMS responded — including the two the project learned the hard way.

**Table 12.3 — The testing axioms and the project's response**

| # | Axiom | DEICMS response |
|---|---|---|
| 1 | **It is impossible to test a program completely** | The number of inputs, outputs and paths is too large, and the specification is open to interpretation. The suite therefore targets the highest-risk paths rather than attempting completeness |
| 2 | **Software testing is a risk-based exercise** | Effort was concentrated where failure is most costly: the five algorithms and the authorisation boundaries. Route handlers and templates were tested more lightly, deliberately |
| 3 | **Testing cannot show the absence of bugs** | Demonstrated within this project: a green 172-test suite coexisted with two critical defects (M2, findings D1 and D2) |
| 4 | **The more bugs you find, the more bugs there are** | Bearing this out, M1's two defects prompted the systematic review that found eleven more in M2 — defects cluster |
| 5 | **Not all bugs found will be fixed** | All eleven M2 findings were fixed, but several known limitations were accepted rather than resolved and are recorded in Sections 12.9 and 13.5 |
| 6 | **It is difficult to say when a bug is indeed a bug** | Finding D5 is the clearest case: the risk factors computed *something* without error, and only reading them against their intended meaning revealed that running a verification perversely raised an item's risk |
| 7 | **Specifications are never final** | The access-scoping requirement was stated but its scope of application was incomplete (Section 7.12), and the temporal gap-detection mode was added to reconstruction after the structural mode proved insufficient |
| 8 | **Software testers are not the most popular members of a project** | The single-developer analogue: the tester persona's findings created work for the developer persona. Keeping the roles consciously separate (Section 4.6) is what stopped the developer's optimism from silencing the tester's suspicion |
| 9 | **Software testing is a disciplined and technical profession** | Test data was derived systematically from acceptance criteria and input-domain boundaries, not by choosing convenient examples (Table 3.3) |

Axioms 3 and 8 are the two that shaped this project most, and both did so *after* they were violated rather than before.

### 12.1.4 Testing Philosophy

The testing here was shaped by a single guiding idea: **the parts of the system most likely to be wrong, and most costly if wrong, should be given the most direct and the most adversarial tests.** In a chain-of-custody system the parts most costly if wrong are the algorithms that decide whether an item's history is intact and how risky it is, and the authorisation logic that decides who may see what. The suite therefore concentrates on the business-logic layer and the authorisation boundaries, and treats thin route handlers and templates more lightly, because a defect in a route that merely wires an engine to a template is both less likely and less damaging than a defect in the engine.

## 12.2 Development Testing

Development testing comprises all testing activities carried out by the team developing the system. It operates at three levels.

**Table 12.4 — The three levels of development testing**

| Level | Scope | Tests what | DEICMS instance |
|---|---|---|---|
| **Unit testing** | Individual units — functions, methods, object classes | That each unit operates as expected; tests should cover all its features | The algorithm tests: normalisation curves, graph traversal, transition table, intent classification |
| **Component testing** | Several units composed into a component | The **component interfaces** — because defects arise from interactions between units, not within them | The engine-level tests: constructing a scorer or verifier and asserting on its structured result |
| **System testing** | The whole system, or a substantial subsystem | Interactions between components; emergent behaviour | The integration module: login → create case → upload → transfer → verify → export |

Unit tests should cover all of a unit's features, exercising both **normal operation** and **abnormal inputs that cause the unit to fail**. Both are present here, and the abnormal cases are the ones test-first thinking produced: equal normalisation bounds, a negative input to the logarithmic curve, an evidence item with no custody records, an empty reconstruction chain.

Component testing focuses on interfaces because that is where the defects are. Four interface error types are worth naming, with the DEICMS instance of each.

**Table 12.5 — Interface error types**

| Error type | Description | Instance in this project |
|---|---|---|
| **Interface misuse** | A calling component calls another and makes an error in its use | Defect D3: the evidence route passed a case identifier from the URL to the access check, but loaded the item by a different identifier |
| **Interface misunderstanding** | The caller embeds incorrect assumptions about the callee's behaviour | Defect D5: the risk scorer assumed two audit-event queries counted duplicates and role mismatches; they counted integrity checks and warnings |
| **Timing errors** | Caller and callee operate at different speeds and stale information is used | Defect D6: mixed timezone-aware and naive timestamps risked comparison errors between components that produced and consumed them |
| **Missing interface** | The expected interface does not exist at all | Defect D2: the risk scorer read an `integrity_status` attribute that no component ever wrote — the interface between verifier and scorer did not exist |

That all four canonical interface error types occurred in one project, and all four were found by review rather than by testing, is the strongest available argument for Section 12.5's conclusion.

### 12.2.1 Organisation of the Suite

The suite mirrors the project's structure, which makes a failure easy to localise.

**Table 12.6 — Test modules**

| Module | Tests | Covers |
|---|---|---|
| `test_increment1` | 10 | Entities and relationships, role predicates, case and evidence CRUD, hashing, the initial-custody invariant, append-only enforcement |
| `test_day2` | 12 | Cryptographic key generation and the three audit formula checks |
| `test_increment2` | 17 | State machine transitions and guards, graph integrity verification, chain reconstruction, signing and verification |
| `test_increment3` | 93 | Risk scoring normalisation and interaction rules, all six assistant pipeline stages, anomaly detection, dashboards, 2FA, encryption, export |
| `test_integration` | 16 | Complete investigator workflows end to end through the HTTP interface |
| `test_scoping` | 14 | **Adversarial** authorisation tests introduced in M1 |
| `test_intent_classifier` | 10 | Intent ranking, including the self-referential priority rule from M2 |
| | **172** | |

The suite runs in well under two minutes and **requires no external services**, because the one external dependency is invoked through a seam the tests replace with a deterministic mock.

## 12.3 Test-Driven Development

Test-driven development interleaves testing and code development: tests are written **before** the code, and development proceeds incrementally, a test at a time, with code not written until its test passes.

**Table 12.7 — The TDD cycle, and where DEICMS applied it**

| Step | Action |
|---|---|
| 1 | Identify the increment of functionality required — usually small, implementable in a few lines |
| 2 | Write a test for it and implement it as an automated test |
| 3 | Run the test, along with all other implemented tests. It fails, because the functionality does not exist |
| 4 | Implement the functionality and re-run the test |
| 5 | Once all tests pass, move to the next increment |

TDD was adopted **for the complex algorithms from Increment 3 onward**, as retrospective action A2-1 (Table 5.4). It was not applied to routes and templates, where the cost exceeds the benefit.

Its benefits, and the evidence for each in this project:

**Table 12.8 — TDD benefits and the evidence here**

| Benefit | Evidence in DEICMS |
|---|---|
| **Code coverage** — every code segment has at least one associated test | Risk scoring reached 97% statement coverage; anomaly detection 100% |
| **Regression testing** — a suite develops incrementally as the program is developed | The suite that made M1 and M2 fixes safe to attempt existed because it had grown alongside the code |
| **Simplified debugging** — when a test fails, the problem is in the newly written code | The Increment 3 burndown is the steadiest of the three (Figure 5.3), directly attributed to this |
| **System documentation** — the tests state what the code should do | The normalisation tests are the clearest existing specification of each factor's curve |

The most valuable effect was subtler than any of these: writing the acceptance criteria as tests first turned *"the score must be in range"* and *"all failures must be found"* from prose into **executable checks the implementation then had to satisfy**. The second of those is precisely the criterion the first graph-verifier implementation violated by short-circuiting — and had TDD been in force during Increment 2, the three-day plateau would probably have been shorter.

## 12.4 Release Testing

Release testing is the process of testing a **particular release** of a system intended for use outside the development team. It differs from development testing in two ways: a separate team should ideally be responsible for it, and its goal is to convince the supplier that the system is **good enough for use** — it is therefore a form of *validation* testing rather than defect testing.

For a single-developer project no separate team exists, so the adaptation is stated plainly: release testing was performed by the developer **wearing the tester persona deliberately and separately** (Section 4.6). The weakness of this arrangement is obvious and is not disguised — the person who knows how the system is built is poorly placed to be surprised by it.

Release testing in DEICMS took two forms.

**Requirements-based testing.** Each requirement was examined and a test or set of tests derived for it. The traceability matrix (Appendix D) is the record: every functional requirement in Table 7.5 carries the test module that verifies it. This is the practical expression of the rule that for custom software there should be at least one test per requirement.

**Scenario testing.** Rather than testing features in isolation, typical scenarios of use were devised and the system tested against them end to end. The integration module's sixteen tests are these scenarios: an investigator logs in, creates a case, uploads evidence, transfers custody, runs verification and reconstruction, exports the signed package, downloads the PDF report, and edits the risk settings. Scenario testing exercises the interactions that unit tests by construction cannot.

## 12.5 User Testing

User testing is a stage in which users or customers provide input and advice. It is essential even when comprehensive system and release testing have been carried out, because **influences from the user's working environment have a major effect on reliability, performance, usability and robustness** that cannot be replicated in a development environment.

**Table 12.9 — Types of user testing**

| Type | Description | Available here? |
|---|---|---|
| **Alpha testing** | Users work with the development team to test the software at the developer's site | Simulated through the persona-based review testing described below |
| **Beta testing** | A release is made available to users to experiment and raise problems with the developers | Not available — no user population |
| **Acceptance testing** | Customers formally test a system to decide whether to accept it | Substituted by acceptance-criteria review at each sprint review |

The honest position is that **DEICMS had no external users**, so genuine user testing did not occur. What substituted for it was **persona-based review testing**: the tester persona adopted each of the four roles in turn and attempted to do what that role would actually do — and, critically, what that role should *not* be able to do.

This is where the project's most important defects were found, and it is worth being precise about why. Logged in as a lead investigator belonging to one case, the tester opened the dashboard and saw charts and a top-risk table counting items from cases the investigator was not a member of. The same probing of the risk and anomaly views showed the same global scope. The assistant, asked to list all cases, returned every case in the system. After logging out and back in as a different user, the previous user's conversation was still present.

None of these was visible to the automated suite, because **each test constructed only the data it needed and then checked the feature worked on it**. The leakage manifests only when data from *another* case exists and a user without access to it views an aggregate — a configuration no positive test creates. This is the concrete form of Axiom 3, and it is why user-level testing is not an optional supplement to automated testing but a different instrument measuring a different thing.

## 12.6 Testing and the V-Model

Although DEICMS was not developed with a V-model process (Section 4.3.2), the model's central insight was adopted: **each construction activity is paired with the test level that validates its output**, and the test is planned when the construction activity is planned rather than at the end.

**Table 12.10 — Construction activities paired with their validating test level**

| Construction activity | Output | Validating test level | DEICMS instrument |
|---|---|---|---|
| Requirements specification | User and functional requirements | **Acceptance testing** | Sprint-review demonstration against acceptance criteria |
| Architectural design | Layers, modules, interfaces | **System testing** | `test_integration` — full workflows across all layers |
| Detailed design | Engine classes and their contracts | **Integration / component testing** | Engine-level tests asserting on structured results |
| Implementation | Functions and methods | **Unit testing** | Per-function tests of curves, guards, classifiers |

The pairing is what makes the traceability matrix in Appendix D possible: a requirement is not merely listed, it is listed alongside the level at which it is verified.

## 12.7 Test Case Catalogue

**Table 12.11 — Representative test cases across the levels**

| ID | Level | Test | Expected result | Module |
|---|---|---|---|---|
| T-01 | Unit | Password hashed, never stored in plaintext | Stored value differs from input; verification succeeds | `test_increment1` |
| T-02 | Unit | Login with unknown email vs wrong password | Identical error message in both cases | `test_increment1` |
| T-03 | Unit | Attempt to UPDATE an audit record | Raises; record unchanged | `test_increment1` |
| T-04 | Unit | Custody gap of 72 h vs 71 h | 72 h flagged; 71 h not | `test_day2` |
| T-05 | Unit | Ed25519 signature over the canonical payload | Verifies against the signer's public key | `test_day2` |
| T-06 | Component | Verify a clean custody chain | Verdict `Intact`, completeness 1.0, no failures | `test_increment2` |
| T-07 | Component | Verify with the stored file replaced | Hash failure detected and located at the root node | `test_increment2` |
| T-08 | Component | Verify with a non-increasing timestamp | Temporal anomaly detected at that node | `test_increment2` |
| T-09 | Component | Verify an item with no custody records | Verdict `Broken` | `test_increment2` |
| T-10 | Component | Transition Submitted → Under Analysis with no custody log | Rejected with the exact unmet precondition | `test_increment2` |
| T-11 | Component | Transition Under Analysis → Archived without an Intact verdict | Rejected | `test_increment2` |
| T-12 | Component | Read-Only investigator requests available transitions | Empty set | `test_increment2` |
| T-13 | Component | Reconstruct a gapless chain | Confidence 1.0, all links `Confirmed` | `test_increment2` |
| T-14 | Component | Reconstruct an empty chain | Confidence 0.0 | `test_increment2` |
| T-15 | Unit | Normalisation with equal upper and lower bounds | Returns a defined value; no division by zero | `test_increment3` |
| T-16 | Unit | Logarithmic curve with a negative input | Clamped, not raised | `test_increment3` |
| T-17 | Unit | Risk weights sum | Exactly 1.0 after re-normalisation | `test_increment3` |
| T-18 | Unit | Interaction bonus with both thresholds met vs one met | Fires only when both are met | `test_increment3` |
| T-19 | Unit | Final score bound | Always within [0, 1] | `test_increment3` |
| T-20 | Unit | Intent classification across all seven intents | Correct intent for each | `test_intent_classifier` |
| T-21 | Unit | "What are the cases assigned to me?" | Classified as *identity*, not *case query* | `test_intent_classifier` |
| T-22 | Component | Full assistant pipeline against the mock backend | Reply returned; all six stages executed | `test_increment3` |
| T-23 | Component | Executable uploaded with an image extension | Rejected on magic-byte mismatch | `test_increment3` |
| T-24 | System | Login → case → upload → transfer → verify → export | Signed package produced; manifest verifies | `test_integration` |
| T-25 | System | PDF custody report generation | Contains a fresh integrity verdict | `test_integration` |
| T-26 | **Adversarial** | `accessible_case_ids` for each of the four roles | Admin sentinel; member list; empty list | `test_scoping` |
| T-27 | **Adversarial** | Lead's dashboard with a second case present | No trace of the non-member case | `test_scoping` |
| T-28 | **Adversarial** | Read-Only user with no memberships | Explanatory empty state, no data | `test_scoping` |
| T-29 | **Adversarial** | Cross-case per-item risk request | Refused with an authorisation error | `test_scoping` |
| T-30 | **Adversarial** | Assistant asked to describe an inaccessible case | Refuses; no data leaked | `test_scoping` |
| T-31 | **Adversarial** | Chat history after logout and re-login as another user | Previous user's history absent | `test_scoping` |

## 12.8 Coverage Analysis

Measured across the application package, the suite covers approximately **78% of statements**. That headline figure is far less informative than its distribution, which is exactly what the testing philosophy predicts: **the layers that matter most are covered most**.

**Table 12.12 — Statement coverage of the core logic and data layers**

| Module | Coverage | Category |
|---|---|---|
| Anomaly detection (`anomaly_detection`) | 100% | B |
| Risk scoring (`risk_scoring`) | 97% | **C** |
| Cryptography (`crypto`) | 95% | B / security |
| Audit formulas (`audit_formulas`) | 94% | A |
| Graph integrity verifier (`graph_integrity`) | 90% | **C** |
| Evidence lifecycle state machine (`state_machine`) | 83% | **C** |
| AI assistant orchestration (`ai_assistant`) | 78% | **C** |
| Custody chain reconstruction (`chain_reconstruction`) | 65% | **C** |
| Data models (Evidence, Case, Custody, Case Access, …) | 88–97% | A |
| Dashboard route | 98% | A |
| **Whole application package** | **~78%** | |

The pattern is intended. The five complex algorithms and the cryptographic and formula code — the Category C and security-critical work — are covered from the high eighties to one hundred per cent, with one exception.

**The exception is chain reconstruction at 65%, and it deserves an explanation rather than a footnote.** The figure reflects the many candidate-scoring branches that execute only for particular gap configurations: a candidate with a matching location but a mismatched role, a candidate that is temporally close but behaviourally isolated, and so on across the four criteria. The test scenarios construct several such configurations but not the full combinatorial space. This is the honest consequence of Axiom 1 — exhaustive testing is impossible — and the appropriate response was to ensure the *decision points* are covered, which they are, rather than to manufacture scenarios for coverage's sake.

Coverage that is **not** achieved is concentrated in three places: route handlers that merely wire an engine to a template; defensive error branches taken when an external service is unavailable, a file is missing, or a rarely-reached validation fails; and templates, exercised by the integration tests for their happy paths but not for every conditional. This is the appropriate place for coverage to thin. A report claiming 100% would be claiming to test glue code and low-risk error branches at a maintenance cost that would not be repaid.

## 12.9 What the Coverage Does and Does Not Establish

An honest account of quality is more valuable than an inflated one, so the boundary is stated explicitly.

**Table 12.13 — The boundary of what testing establishes here**

| The suite **does** establish | The suite does **not** establish |
|---|---|
| The algorithms compute what their acceptance criteria require, across the normal and degenerate cases the tests describe | That the system is free of defects — M2 is proof that a green suite can coexist with critical bugs |
| The full investigator workflows function end to end | Behaviour under concurrency — no concurrent access is exercised |
| The authorisation boundaries hold against the adversarial scenarios the scoping module constructs | Behaviour under load — no performance or stress testing was performed |
| That a change breaking any of the above will fail the suite — so the suite serves as a regression guard | Behaviour of the live language model — the tests exercise the mock seam |
| That the system runs on a second platform — the suite passes on Linux as well as Windows | Usability with real users — no user population existed |

The project's response to the right-hand column is the complementary practice drawn from M2: **periodic structured code review**, to catch the class of defect that testing structurally misses. The conclusion recorded in Section 5.5.4 is worth restating here in testing terms: *a test confirms that the code does what the test expects*, so a defect that is not in the path of any expectation is invisible to it. Reading the code against its intent is a different instrument, and the four interface errors catalogued in Table 12.5 are what it found.

## 12.10 Summary

This chapter documented the testing and quality assurance of DEICMS. It distinguished validation testing from defect testing and showed that the project's most serious defects survived a thorough validation suite precisely because no defect testing existed until M1. It defined verification, validation and quality assurance, and applied the nine testing axioms, recording that axioms 3 and 8 shaped the project only after they had been violated.

Development testing was presented at its three levels, with the four canonical interface error types each matched to an actual defect found in this project — all four found by review rather than testing. Test-driven development was described with the evidence for each of its four benefits. Release testing and user testing were described with their single-developer adaptations stated plainly, including the acknowledgement that no genuine user testing occurred and that persona-based review testing substituted for it. The V-model's construction-to-test pairing was applied. A catalogue of thirty-one representative test cases was given across all levels, and coverage was reported with its distribution explained — including a direct explanation of the one module at 65% rather than a footnote.

Finally, the boundary of what the testing establishes was stated on both sides. The next chapter treats the quality that dominates all others in this system.

---

\newpage
