# Chapter 5 — The Development Iterations

---

## 5.0 Overview

This chapter documents the five iterations through which DEICMS was built: three development increments and two maintenance iterations, summarised in Table 4.9 of the previous chapter. Each is presented with the same structure — sprint goal, sprint backlog, UML artefacts produced, sprint review, burndown chart and retrospective — so that the iterations can be compared with one another and so that every retrospective action can be traced into the iteration that executed it.

The presentation is deliberately uniform. A reader who wants to know what changed between Increment 2 and Increment 3 can compare two burndown charts drawn to the same scale and two retrospectives written to the same four headings, rather than two narratives written in different shapes.

---

## 5.1 Increment 1 — Core Case and Evidence Management

### 5.1.1 Sprint Goal

The goal of the first increment was to build the foundation on which everything else would stand: a working evidence repository in which investigators log in, manage cases, register hashed evidence, and have every action recorded in a tamper-evident trail. Expressed as a single sentence, the sprint goal was *"an authenticated, role-aware system in which cases and evidence can be managed and every action is audited."*

Nothing in this increment is algorithmically complex — that is by design. The increment exists to make the later algorithms possible by giving them a concrete, stable data model and a body of real records to operate on, and to retire the routine-but-numerous risks of authentication, authorisation, file handling and persistence before the harder work begins.

### 5.1.2 Sprint Backlog

**Table 5.1 — Increment 1 sprint backlog**

| ID | User story | Category | MoSCoW | Points |
|---|---|---|---|---|
| US-01 | Secure login and logout | A / Security | Must | 3 |
| US-02 | Role-based access control | A | Must | 5 |
| US-03 | Case CRUD, search and archive | A | Must | 5 |
| US-04 | Upload and register evidence | A | Must | 5 |
| US-05 | SHA-256 fingerprint at upload | B | Must | 2 |
| US-06 | EXIF / MIME metadata extraction | B | Must | 3 |
| US-07 | Edit and categorise evidence | A | Must | 3 |
| US-08 | Record custody transfers and access events | A | Must | 5 |
| US-09 | Append-only audit trail | A | Must | 5 |
| US-10 | Formula-based audit checks | A | Should | 3 |
| US-11 | Admin-only account creation | A | Must | 1 |
| | **Total** | | | **40** |

Full acceptance criteria for every story are given in Section 7.5 and Appendix A; the implementation is described in Chapter 10.

### 5.1.3 UML Artefacts Produced

The use-case diagram (Figure 8.1), the class diagram (Figure 8.2) and the entity-relationship diagram (Figure 8.3), all presented in Chapter 8.

### 5.1.4 Sprint Review

All eleven stories were demonstrated against their acceptance criteria and all forty story points were accepted. The increment delivered a system that could be logged into, that enforced its four roles and case memberships, that managed cases and registered hashed evidence with extracted metadata, that recorded custody and audited every action immutably, and that ran the three formula checks.

Measured against the five guarantees of Table 1.1, Increment 1 fully delivered **G3** (tamper-evident complete record) and **G2** (case-scoped access, at the record level), laid the foundation for **G1** by capturing the intake hash and the ordered custody log, and left **G4** and **G5** to the increments designed for them.

### 5.1.5 Burndown

**[FIGURE 5.1 — Increment 1 burndown chart]**

The chart plots ideal and actual story points remaining across the fourteen-day cycle. The actual line runs above the ideal for the first several days: days zero to two produced no burned points at all, because environment setup — the Flask application factory, the SQLAlchemy configuration and the Git repository — took longer than planned, and the first story was not completed until day two. From about day nine the actual line converges back toward the ideal, and all forty points were delivered by day fourteen. The chart's shape is therefore a slow start followed by a recovery.

### 5.1.6 Retrospective

**Table 5.2 — Increment 1 retrospective**

| Category | Finding |
|---|---|
| **What went well** | The application-factory pattern made the system testable from the first week and repaid its small up-front cost many times over |
| **What went well** | Writing audit-trail hooks into each route as the route was built, rather than in a later pass, meant the system was never without a complete history |
| **What went less well** | The zero-burn start: environment and scaffolding work was real work not represented as points, so the burndown looked alarming before it looked healthy |
| **What went less well** | The estimate for routine CRUD-and-template work was slightly optimistic |
| **Action A1-1** | Reserve day zero of Increment 2 explicitly for a design spike on the graph integrity algorithm, whose 13-point estimate reflected real uncertainty |
| **Action A1-2** | Fix the canonical format of the data that custody signing will sign *before* writing any signing code, so signer and verifier cannot disagree about what bytes are signed |

Both actions were carried out, and Section 5.2.6 records that both proved well judged.

---

## 5.2 Increment 2 — Integrity Algorithms and Lifecycle

### 5.2.1 Sprint Goal

Where the first increment built a repository that could *store* a chain of custody, the second built the machinery that makes that chain *provable and rule-bound*. The sprint goal was *"make the chain of custody cryptographically verifiable and procedurally enforced"* — to turn the ordered custody records of Increment 1 from a set of claims into a set of proofs, and to turn the evidence lifecycle from an informal sequence of statuses into a formal automaton that the system enforces.

This is the increment in which the first three of the project's five complex algorithms were designed and built, and it was therefore the increment of highest technical risk, which is precisely why it was placed in the middle of the schedule.

### 5.2.2 Sprint Backlog

**Table 5.3 — Increment 2 sprint backlog**

| ID | User story | Category | MoSCoW | Points |
|---|---|---|---|---|
| US-12 | Ed25519-signed custody events | B | Must | 5 |
| US-13 | Graph integrity verification algorithm | C | Must | 13 |
| US-14 | Evidence lifecycle state machine | C | Must | 8 |
| US-15 | Custody chain reconstruction algorithm | C | Must | 8 |
| US-16 | Integrity verification report UI | A | Should | 2 |
| US-17 | Chain reconstruction report UI | A | Should | 2 |
| | **Total** | | | **38** |

Two of the six stories carried the bulk of the increment's weight and its risk; the two report interfaces were deliberately small, because their value lies in exposing the algorithms' output rather than in themselves.

### 5.2.3 UML Artefacts Produced

The sequence diagram of graph integrity verification (Figure 8.4), the state machine diagram of the evidence lifecycle (Figure 8.8) and the activity diagram of chain reconstruction (Figure 8.7), all presented in Chapter 8. Because this increment's work is algorithmic, its artefacts are behavioural rather than structural.

### 5.2.4 Sprint Review

All six stories were demonstrated against their acceptance criteria and all thirty-eight points accepted. The increment delivered signed custody events, a graph verifier that walks an entire chain and reports a verdict with a completeness score and located failures, a state machine that enforces the lifecycle with role guards and preconditions, and a reconstruction algorithm that fills gaps honestly with confidence labelling.

Against the five guarantees, Increment 2 completed **G1** (provable integrity) and delivered **G4** (enforced procedural rules) in full, leaving only **G5** for Increment 3.

### 5.2.5 Burndown

**[FIGURE 5.2 — Increment 2 burndown chart]**

This chart shows the roughest middle of the project. The actual line tracks the ideal for the first several days, then **plateaus across days five to seven**, during which almost no points were burned. The plateau is the graph-integrity rework: the depth-first traversal, initially written to stop at the first failure, had to be reworked to accumulate all failures while continuing, and that rework surfaced a payload-format mismatch between the signer and the verifier that took further time to diagnose. From about day eight the line resumes its descent and steepens, because the state machine and the reconstruction algorithm were able to reuse the test fixtures and graph-building patterns established while building the verifier, and all thirty-eight points were delivered by day fourteen.

### 5.2.6 Retrospective

**Table 5.4 — Increment 2 retrospective**

| Category | Finding |
|---|---|
| **What went well** | Action A1-1 paid off directly: freezing the canonical payload format before writing signing code is what made the eventual payload-mismatch bug tractable rather than mysterious |
| **What went well** | Building reusable test fixtures while constructing the first algorithm sharply reduced the cost of testing the second and third |
| **What went less well** | The three-day plateau, whose lesson was estimation-related: the 13-point estimate for the verifier was correct in magnitude but wrong in its reasoning — the cryptographic checks that had seemed hard were straightforward library calls, while the traversal semantics that had seemed straightforward were the real difficulty |
| **Action A2-1** | Write the acceptance criteria of each complex algorithm as unit tests *before* implementing it, so that the definition of "all failures found" or "score in range" is pinned down in advance |
| **Action A2-2** | Keep the language model behind an interface so that the assistant pipeline can be tested without external credits |

Both actions were carried out, and Section 5.3.6 records that both paid off measurably.

---

## 5.3 Increment 3 — Risk Scoring, AI Assistant and Hardening

### 5.3.1 Sprint Goal

The first two increments produced a system that stored a chain of custody, proved its integrity and enforced its lifecycle. The third turns that trustworthy record into something an investigator can *act on efficiently*, and hardens the whole system to the standard a forensic application demands. The sprint goal was *"turn verified records into judgement, and make the system safe to deploy."*

This was the largest increment. It contains two of the project's five complex algorithms alongside a cluster of third-party integrations and security features, and it was placed last deliberately: the risk scorer depends on the integrity verifier and the state machine built in Increment 2, and the assistant's most valuable capability — answering integrity questions — depends on being able to run a fresh verification.

### 5.3.2 Sprint Backlog

**Table 5.5 — Increment 3 sprint backlog**

| ID | User story | Category | MoSCoW | Points |
|---|---|---|---|---|
| US-18 | Multi-factor risk scoring algorithm | C | Must | 8 |
| US-19 | Admin-configurable risk weights | C / A | Should | 3 |
| US-20 | AI assistant orchestration pipeline | C | Must | 8 |
| US-21 | Hallucination detection | C | Must | 3 |
| US-22 | Isolation Forest anomaly detection | B | Could | 5 |
| US-23 | Risk and anomaly dashboards | A | Should | 3 |
| US-24 | 2FA, lockout and session timeout | Security / B | Should | 5 |
| US-25 | Encryption at rest and magic-byte checks | Security / B | Should | 3 |
| US-26 | Tamper-evident signed ZIP export | B | Should | 2 |
| US-27 | PDF chain-of-custody report | B | Could | 2 |
| | **Total** | | | **42** |

### 5.3.3 UML Artefacts Produced

The activity diagram of risk scoring (Figure 8.6), the sequence diagram of the AI orchestration workflow (Figure 8.5), and the component and deployment diagrams of the whole system (Figures 8.9 and 8.10), all presented in Chapter 8. The last two were completed in this increment because only now were all the modules in place to be drawn.

### 5.3.4 Sprint Review

All ten stories were demonstrated and all forty-two points accepted. The increment delivered the multi-factor risk scorer with configurable weights, the six-stage AI assistant with hallucination detection, the Isolation Forest anomaly pipeline, the dashboards, the full security-hardening suite, and the signed export and PDF report.

With this increment the fifth guarantee — **G5**, analytical prioritisation — was delivered, completing the set, and the system reached the functional scope defined at the outset.

### 5.3.5 Burndown

**[FIGURE 5.3 — Increment 3 burndown chart]**

This is the steadiest of the three charts, tracking within about two points of the ideal throughout, with a slight early slip on days one to three recovered by day four. The steadiness is directly attributable to the two actions carried in from Increment 2: writing the risk-scoring tests before the implementation caught the normalisation edge cases before they could reach a route and cause a late surprise, and hiding the language model behind a mock seam meant the assistant pipeline could be built and tested continuously rather than being blocked on external credits or network availability. The security stories integrated cleanly because the audit and custody layers from earlier increments already exposed the hooks they needed.

### 5.3.6 Retrospective

**Table 5.6 — Increment 3 retrospective**

| Category | Finding |
|---|---|
| **What went well** | Both carried-in actions paid off measurably, and the burndown is the evidence |
| **General principle recorded** | The parts of the system given the most tests and the most isolation — the algorithms and the external model — caused the fewest surprises |
| **What went less well** | The one significant defect class that emerged did so in exactly the area that had *not* been given a dedicated test focus: access scoping in the aggregate views and the assistant |
| **Action A3-1** | Raise the access-scoping defects as a formal maintenance iteration rather than patching them silently within the increment |

Action A3-1 is the reason Section 5.4 exists. An honest agile process surfaces the defects its own testing reveals and schedules the work to fix them rather than quietly absorbing them.

---

## 5.4 Maintenance Iteration M1 — Access-Scoping Change Requests

### 5.4.1 Change After Delivery in the Incremental Model

The three increments delivered the full functional scope defined at the project's outset, and at the end of Increment 3 the system met all of its acceptance criteria and passed its test suite. In a plan-driven project that would have been the end of the engineering narrative. In an incremental, agile project it is not, because one of the model's defining strengths is that it accommodates change discovered *after* a working version exists without treating that change as a failure of planning.

M1 is presented as a first-class iteration, with the same planning-and-reflection structure as the increments, for two reasons. First, handling change after delivery is a core software-engineering activity that a report demonstrating the discipline should show rather than hide. Second, the specific defects M1 resolved are instructive: they were not crashes or failing tests — the system worked and its tests were green — but **authorisation** defects, the most dangerous kind for a forensic system and precisely the kind ordinary functional testing does not catch.

The iteration was scoped at **ten story points** across two change-request stories. Both were classified *must-have* despite arising after the planned scope was complete, because a data-leakage defect in a system whose entire purpose is controlled access cannot be deferred.

### 5.4.2 Defect Discovery Through Review Testing

The defects were found not by the automated test suite but by deliberate **review testing**, in which the tester persona actively attempted to do things the system should forbid, rather than confirming that permitted actions work.

This distinction is the iteration's first lesson. The automated tests written during the three increments were, appropriately, *positive* tests: they confirmed that an administrator could see the dashboard, that a lead investigator could rank items by risk, that the assistant answered questions. None asked the adversarial question — *can a user see data they should not?* — because each test constructed only the data it needed and then checked the feature worked on it. The leakage was invisible to that style of testing because it manifests only when data from *another* case exists and a user without access to it views an aggregate.

**Table 5.7 — M1 change requests**

| CR | Story | Defect observed | Points |
|---|---|---|---|
| CR-01 | US-28 | The dashboard, risk dashboard and anomaly view queried every case, evidence item and audit record in the system regardless of the viewer's role or memberships | 5 |
| CR-02 | US-29 | The AI assistant retrieved context globally, could not answer identity questions, retained conversation history across logout, and took one to two minutes to respond | 5 |

### 5.4.3 CR-01 — Role-Scoped Dashboard and Aggregated Views

**Root cause.** The dashboard and risk routes had been written in Increment 3 to query entities globally, because at the time the case-scoping concern had been associated with the case-list and record-detail routes rather than recognised as a property *every aggregate must share*. There was no single place expressing "the set of cases this user may see"; the case list computed it inline, and nothing else reused it.

**Solution.** The fix introduced exactly that missing abstraction: a single helper, `accessible_case_ids`, returning the set of case identifiers a given investigator may see — a sentinel meaning "all cases" for an administrator, the list of memberships for anyone else, and an empty list for a user belonging to no case. Every aggregate query was then routed through it. Centralising the rule in one helper is the essential engineering move: the scoping is defined once and applied uniformly, and a future aggregate view cannot omit it without the omission being conspicuous.

**Beyond the fix.** Scoping the dashboard raised a design question the global version never had to answer: what should a read-only user with no shared cases *see*, if not everything? A naive scoping would have left a blank page. The solution turned the constraint into a feature by making the dashboard **role-tailored** — each role sees panels matched to its work, every role has a "your recent activity" panel guaranteeing no dashboard is ever empty, and a user belonging to no case sees an explanatory message rather than a blank or a global view. This is an example of a security requirement *improving* rather than degrading the user experience.

### 5.4.4 CR-02 — Access-Scoped AI Assistant and Chat Isolation

Four related problems were addressed at their roots. Retrieval was routed through the same `accessible_case_ids` helper, so the assistant retrieves only from accessible cases and a request outside that set returns an access-denied line. An *identity* intent was added and checked with priority, and the authenticated user's identity injected into the prompt, so "who am I" and "my cases" are answerable. The stored conversation was tagged with the owning user's identifier and cleared on both login and logout. The latency was reduced by defaulting to a smaller, faster model and adding a request timeout together with a browser-side abort.

### 5.4.5 Regression Testing

The iteration's second lesson is embodied in its testing. Because the defects escaped positive-only tests, the fixes were accompanied by a dedicated module of fourteen tests written in the **adversarial** style. These construct a scenario with two leads, an analyst and a read-only auditor, and two cases with memberships deliberately arranged so that one lead and the analyst belong to the first case, the other lead to the second, and the auditor to neither — then assert the *negative* properties directly. Alongside the new module, the full existing suite was re-run to confirm that scoping every aggregate had not broken previously passing behaviour.

### 5.4.6 Iteration Review and Reflection

**Table 5.8 — M1 reflection**

| Lesson | Content |
|---|---|
| **On testing** | Positive functional tests, however thorough, do not exercise authorisation boundaries. A system with an access-control requirement needs *negative* tests that actively attempt forbidden actions — a practice adopted from this point on |
| **On abstraction and its timing** | The leakage existed because the scoping rule was expressed inline in one place rather than as a reusable helper, so later surfaces could not reuse it and silently omitted it. Introducing `accessible_case_ids` did not only fix the present defects; it made the class of defect much harder to reintroduce, because the correct behaviour is now the easy, obvious thing to call |

Both lessons are of a kind that surfaces only once a working system exists to be probed — which is itself the argument for the incremental model.

---

## 5.5 Maintenance Iteration M2 — Correctness and Security Hardening

### 5.5.1 Origin: a Final Review and Regression Pass

Where M1 was triggered by exploratory review testing, M2 came out of a final review pass over the whole system once the access-scoping fixes had settled — a deliberate read of every logic module, model and route, together with a full re-run of the test suite, before the project was considered finished. The review produced a findings list recording each defect with its cause and a recommended remedy, and **no code was changed until the whole list existed**, so that fixes could be prioritised by severity rather than patched in the order they happened to be noticed.

Reading a working system is a different activity from testing it, and that difference is why the pass was worth doing. Testing asks whether the code does what a test expects; reading asks whether the code actually *means* what it appears to mean. Several defects found here are of a kind testing is structurally poor at catching — a feature that silently does nothing, a computation that reads a field which does not exist, a permission check applied to the wrong identifier — because the tests around them pass happily while the underlying behaviour is wrong. This complements M1's lesson: M1 showed that authorisation defects need adversarial testing; M2 showed that certain correctness defects need reading rather than running.

### 5.5.2 Findings

**Table 5.9 — M2 findings**

| # | Finding | Theme | Severity | Resolution |
|---|---|---|---|---|
| D1 | Evidence deletion set a non-existent attribute and persisted nothing, while writing an audit record stating the item had been removed | Correctness | Critical | Added a real `is_deleted` column and the startup migration; changed the route to record an honest soft delete; filtered deleted items from every listing path |
| D2 | The highest-weighted risk factor (0.25) read an `integrity_status` column that did not exist, so a quarter of the risk algorithm returned a constant | Correctness | Critical | Added a real `integrity_status` column written back from the graph verifier, closing the loop between the Increment 2 verifier and the Increment 3 scorer |
| D3 | Evidence routes checked access against the case identifier in the URL but loaded the item by its own identifier, permitting cross-case access | Correctness / Security | Critical | Verify that the loaded item's case matches the access that was checked |
| D4 | Custody signing failure could abort a transfer or leave an unverifiable record | Correctness | High | Standardised fail-visible behaviour: an explicit unsigned sentinel with a user warning, reported by the verifier as unverified |
| D5 | Two risk factors counted integrity-check and warning audit events, so running a verification *raised* an item's risk | Correctness | High | Pointed both factors at the genuine Category A formula checks, producing the deliberate cross-category integration described in Chapter 16 |
| D6 | Mixed timezone-aware and naive timestamps risked comparison errors | Correctness | Medium | Routed the custody timestamp default through the shared local-time helper |
| H1 | Untrusted model output rendered as HTML in the chat (stored XSS) | Security | High | Escape the output, then re-apply only the intended lightweight formatting after escaping |
| H2 | No Content-Security-Policy or complementary hardening headers | Security | Medium | Added CSP plus `X-Content-Type-Options`, `X-Frame-Options` and `Referrer-Policy` |
| H3 | No warning when running with insecure default secrets | Security | Low | Emit a clear startup warning whenever either secret is at its default |
| R1 | Unbounded case and evidence listings | Robustness | Low | Paginated both |
| R2 | The intent classifier mis-ranked self-referential questions | Robustness | Low | Added a priority rule, pinned down by a dedicated test module |

Of these, **D1 and D2 are the most instructive**. D1 made the audit trail — the system's most trusted artefact — state something false, which for a chain-of-custody system is the worst category of defect. D2 silently disabled a quarter of the flagship risk algorithm while every surrounding test passed. Neither was in the path of any test's expectation, which is the point.

### 5.5.3 Schema Migration and Regression Testing

Two fixes added columns to the Evidence Item entity, and a database created under the earlier schema would lack them. Rather than requiring a rebuild, the columns were added to the lightweight startup migration routine introduced in Increment 1, which inspects the existing columns and adds any that are missing. Every fix was accompanied by tests, and the complete suite re-run. The final result is a suite of **one hundred and seventy-two tests, all passing**.

### 5.5.4 Iteration Review and Reflection

M2 delivered eleven fixes and left the system materially more trustworthy than the version that had passed all its tests at the end of Increment 3. Its central reflection complements M1's: a distinct class of correctness defect is best caught by *reading* code against its intent, because the surrounding tests pass while the behaviour is quietly wrong.

That two critical findings had survived a full increment and a green test suite is not an indictment of the testing but an illustration of its limits — a test confirms that the code does what the test expects, and neither defect was in the path of any expectation. The practical conclusion is that **testing and review are complementary rather than substitutable**: the suite guards against regression in behaviour that is exercised, while periodic review guards against behaviour that is specified but silently absent.

---

## 5.6 Comparison with a Plan-Driven Execution

It is worth asking directly what would have happened had this project been executed as a waterfall, since the professor's question *why did you choose this model?* deserves an answer grounded in evidence rather than preference.

**Table 5.10 — What a waterfall execution would have produced**

| Project event | What actually happened (agile incremental) | What waterfall would have produced |
|---|---|---|
| The graph verifier's traversal semantics changed during construction | Reworked inside Increment 2; the burndown recorded a three-day plateau and the project continued | The design document would have been signed off with stop-at-first-failure semantics; the change would have required a formal change request against an approved design |
| The external language model was retired by its provider | Absorbed by an ordered fallback list; one day's work | Discovered at system-integration testing, after all development was complete and with no schedule slack remaining |
| Access-scoping defects in aggregates and the assistant | Found by review testing on a running system, then fixed as a planned iteration | Not discoverable before system testing, because no running system exists until then; the fix would have touched code declared complete |
| Two critical correctness defects found by reading code | Fixed in M2 with a full regression suite as a safety net | The regression suite would not have existed until the testing phase, so each fix would carry unmeasured risk |
| Estimates calibrated against measured velocity | Velocity observed in Increment 1 and used to load Increments 2 and 3 | Estimates fixed at the planning phase with no opportunity to recalibrate |

The pattern is consistent: every significant discovery in this project was made **by having working software early enough to probe**. That is precisely the property waterfall does not provide, and it is the substantive reason for the choice — not a preference for agility as a style.

The honest counter-argument should also be stated. Waterfall would have produced more thorough up-front documentation, and in a domain with legal and evidentiary obligations that documentation has genuine value; a forensic product sold commercially might well be required to demonstrate phase-gated design review. The report's position is not that waterfall is inferior in general, but that for a project whose dominant risk was *algorithmic feasibility* rather than *requirement volatility or contractual compliance*, incremental delivery retired the dominant risk and waterfall would not have.

## 5.7 Summary

This chapter defined the four fundamental process activities, contrasted plan-driven and agile families, surveyed six process models with a comparison against this project's needs, and set out the agile method vocabulary — the manifesto, its five principles, Extreme Programming and Scrum's three phases, three roles and four ceremonies. It then recorded the selection of the Agile Incremental Model as a decision with explicit alternatives, consequences and validation criteria, stated the definition of done, and explained the story-point estimation method and the independence of size from MoSCoW priority.

The five iterations were then documented in full — three increments each with sprint goal, backlog, UML artefacts, review, burndown and retrospective, and two maintenance iterations with their findings, fixes and reflections. Every retrospective action was tracked into the iteration that executed it. Finally, the process choice was tested against a counterfactual waterfall execution, event by event.

The next chapter turns from the process itself to its management: how the work was broken down, scheduled, risk-assessed and quality-assured.

---

\newpage
