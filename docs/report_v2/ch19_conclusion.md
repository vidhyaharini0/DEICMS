# Chapter 19 — Conclusion

---

## 19.1 Project Retrospective

Read as a whole rather than iteration by iteration, the project tells a coherent story about how a system's weaknesses are found and fixed, and that story is the most valuable thing the retrospective has to offer. The three increments each closed with a retrospective whose actions fed the next; the two maintenance iterations each closed with a lesson. Taken together they trace a single arc: **the parts of a system given the most isolation and the most adversarial scrutiny are the parts that behave, and the parts that escape that scrutiny are where the real defects hide.**

The arc is visible in the sequence of lessons.

**Table 19.1 — The lesson from each iteration, and what it changed**

| Iteration | Lesson learned | What it changed in the next iteration |
|---|---|---|
| **Increment 1** | Scaffolding is real work that estimates must account for; wiring cross-cutting concerns such as auditing into each route as it is built is cheaper than retrofitting | A day-zero design spike was reserved for the graph algorithm; the canonical signature payload was fixed before any signing code was written |
| **Increment 2** | The difficulty of an algorithm is not always where it appears to be — the cryptographic checks that looked hard were library calls, while the traversal semantics that looked simple were the real work | Acceptance criteria for complex algorithms were written as tests *before* implementation; the language model was kept behind a testable seam |
| **Increment 3** | Isolation and test-first development together produce the steadiest progress — **and** the one defect class not given a dedicated test focus is exactly where a defect emerged | The access-scoping defects were raised as a formal maintenance iteration rather than patched silently |
| **M1** | Positive functional tests, however thorough, do not exercise authorisation boundaries; and a rule expressed inline rather than once will be omitted by later surfaces | Adversarial authorisation testing adopted as a standing practice |
| **M2** | A green test suite can coexist with critical defects; a distinct class of correctness bug is caught by *reading* code against its intent rather than by running it | Periodic structured review adopted as complementary to testing |

The project therefore ends holding **two quality practices it did not begin with**: adversarial testing of the boundaries, and periodic review of the code against its intent. That it acquired both by experience rather than by prescription is the clearest evidence that the incremental process did what it is supposed to do — and the sequence in Table 19.1 is, in miniature, the feedback-system behaviour that Lehman's eighth law describes (Section 14.2).

## 19.2 Velocity Analysis

Velocity across the three increments was strikingly stable. Each committed to a budget of story points and delivered all of them.

**Table 19.2 — Velocity across the iterations**

| Iteration | Committed | Delivered | Burndown shape |
|---|---|---|---|
| Increment 1 | 40 | 40 | Slow start through day two (environment setup), recovered from day nine |
| Increment 2 | 38 | 38 | Mid-sprint plateau across days five to seven (integrity rework), then steepened |
| Increment 3 | 42 | 42 | Steadiest; tracked the ideal within about two points throughout |
| Maintenance M1 | 10 | 10 | Two access-scoping change requests |
| Maintenance M2 | — | 11 findings | Defect-repair driven; measured by findings, not points |
| **Total** | **130** | **130** | Mean increment velocity 40.0 |

**That every committed point was delivered should be read with a critical eye rather than as an unqualified success**, and the retrospective does so. Full delivery in every increment is partly a genuine result of realistic estimation and stable scope, and partly an artefact of a single-developer project in which estimator and implementer are the same person, so that estimates could be — and were — adjusted with perfect knowledge of the implementer's pace. This is risk R-10 in the register (Table 6.4), rated high-probability and accepted rather than mitigated, because no mitigation is available.

**The more informative signal is not that the totals were met but the shape of each burndown.** The slow start in Increment 1, the plateau in Increment 2, the steady tracking in Increment 3 — those shapes tell the real story of where the work was hard. And it is no coincidence that the steadiest burndown belongs to the increment that had the benefit of two increments' worth of accumulated retrospective actions.

Velocity, in other words, is most honestly read here as a measure of **how well the process was working** rather than of how much was produced. By that reading it improved across the project.

## 19.3 Was the Process Choice Right?

With the project complete, the choice of the agile incremental model over a plan-driven one can be assessed against outcomes rather than expectations. Section 4.5 recorded the decision with four named factors and a validation criterion; this section is that validation.

**Table 19.3 — The four selection factors, assessed against outcomes**

| Factor claimed at selection | Outcome | Verdict |
|---|---|---|
| Technical risk was concentrated in the complex algorithms, and committing their design on paper first would waste effort | The graph verifier's traversal semantics **did** change under implementation, from stop-at-first-failure to accumulate-all — the exact change a waterfall plan would have frozen and then had to unfreeze | **Borne out precisely** |
| The three feature tiers have a natural dependency order that rewards increments | Increment 2's algorithms needed Increment 1's schema and records; Increment 3's scorer needed Increment 2's verified integrity status | **Borne out** |
| Inter-increment feedback would improve the work | Every retrospective action was executed and its effect observed; Increment 3's burndown is the measurable result | **Borne out more strongly than expected** |
| The structure produces the planning and reflection artefacts the report requires | Five sets of backlogs, burndowns, reviews and retrospectives, all in Chapter 5 | **Borne out** |

The strongest evidence is one the selection did not anticipate. **The two maintenance iterations — the clearest demonstrations of the model's value — were possible only because working software existed early enough to be probed adversarially and read critically while the project was still under way.** A plan-driven project would have discovered the scoping leak and the dead soft-delete after delivery, if at all. Section 5.6 sets this out event by event.

The honest caveats are two, and both have been stated throughout. The model's collaborative ceremonies had to be adapted for a single developer, which weakens the customer-collaboration principle to a role-switching discipline. And the estimation independence that velocity analysis normally assumes does not hold here. Neither caveat touches the core of the model — build a working increment, reflect, adjust, repeat — which applied without modification and delivered its promised benefits.

## 19.4 Achievements

**Table 19.4 — What was delivered, against the objectives of Table 1.3**

| Objective | Delivered |
|---|---|
| O1 — A working web application managing the full evidence lifecycle | ~5,000 lines of application code; ten blueprints; six entities |
| O2 — Role-based and case-based access control on every route and aggregate | Four roles plus case membership, enforced through a single scoping rule |
| O3 — A cryptographically verifiable chain of custody with an append-only trail | Ed25519 signatures on every custody event; append-only enforced at the ORM layer |
| O4 — At least three non-trivial algorithms implemented from first principles | **Five delivered**, each with pseudocode and complexity analysis in Chapter 11 |
| O5 — Third-party services consumed correctly, with the boundary stated | Eleven integrations, each with the boundary tabulated in Chapter 16 |
| O6 — A genuine agile incremental project with per-iteration artefacts | Three increments and two maintenance iterations, fully documented in Chapter 5 |
| O7 — An automated test suite of meaningful coverage | 172 tests passing; ~78% statements, concentrated in the algorithms |
| O8 — Hardening against common web vulnerabilities | Thirty-one controls across six defensive layers (Table 13.3) |

Beyond the artefact, the project produced a **demonstration of software-engineering practice**: a defensible choice of process, honestly executed; a categorisation of features approached with rigour rather than as a labelling exercise; a complete UML model spanning all four perspectives; and a willingness to find and document the system's own defects rather than present it as flawless.

## 19.5 Limitations

Every limitation named in this report is collected here, so that the boundary of the claim is visible in one place.

**Table 19.5 — Consolidated limitations**

| Area | Limitation | Where discussed |
|---|---|---|
| Deployment | Self-signed certificate; development server; SQLite; debug mode enabled | §17.1, Table 13.5 |
| Security | CSP permits inline scripts and styles; insecure defaults possible in development; in-memory rate limiting; no key-rotation procedure | §13.5 |
| Testing | No concurrency, load or penetration testing; live model behaviour untested; no real users | §12.9 |
| Process | Estimator and implementer are the same person; no external customer for validation; team ceremonies adapted rather than practised | §4.8, §7.12, §4.6 |
| Requirements | Negative requirements were initially under-specified — a right requirement incompletely applied | §7.12 |
| Algorithms | The integrity hash check compares recorded hashes against a ground truth, not per-event file snapshots; the Isolation Forest is uninterpretable; the hallucination check verifies references, not reasoning | §11.2.4, §11.6.5, §11.6.4 |
| Implementation | Sequential numbering unverified under concurrency; startup migration adds columns only; one platform-conditional dependency | §10.4.1, §10.2, §17.1 |
| Coverage | Chain reconstruction at 65%, reflecting uncovered candidate-scoring branch combinations | §12.8 |

The report's position throughout has been that **the value of naming a limitation precisely is that it becomes a specification for the work that would remove it.** Table 19.5 is therefore not a list of failings but the agenda of Section 19.6.

## 19.6 Future Work

The work beyond the delivered boundary falls into two groups.

**The explicitly deferred scope** is recorded in the product backlog's *won't-have* list (Table 7.12): a production PostgreSQL deployment behind a multi-process server; email and push notifications; full-text search over evidence *content* rather than metadata; a multi-language interface; a mobile client; and fine-tuning of the language model. None of these would add to the software-engineering demonstration, which is why they were excluded, but each is a natural extension for a system intended to be operated rather than assessed.

**The limitations that point to concrete work** are the ten-step production checklist of Table 17.6, together with four further items: tightening the Content-Security-Policy to a nonce-based policy once the templates are refactored to avoid embedded scripts and styles; making the sequential numbering robust under concurrency; designing a key-rotation procedure, which requires re-encrypting the whole store under a new key while retaining the old; and calibrating the reconstruction heuristics — the four plausibility criteria and the 0.40 threshold — against real usage data, which does not yet exist.

One further direction is worth naming because the project is unusually well placed for it. The test suite is fast, deterministic and requires no network access, which is the prerequisite that usually blocks adoption of **continuous integration** (Section 17.6). Adding an automated pipeline would be a small step from where the project stands and would close the gap between being CI-ready and CI-practising.

## 19.7 Concluding Remarks

DEICMS set out to be a system whose entire purpose is to be trustworthy — to manage digital evidence in a way that makes tampering either impossible or evident, that confines every user to the data they are entitled to, that records its own history immutably, that enforces the procedures of its domain, and that helps its users reason about risk.

It delivered on those aims across three increments and two maintenance iterations: five complex algorithms implemented from first principles, a six-entity data model with real domain constraints, eleven honestly-attributed third-party integrations, thirty-one security controls across six layers, a complete UML model, and a suite of one hundred and seventy-two tests.

More than the artefact, though, the project produced an account of engineering practice. A process was chosen for stated reasons and then judged against what actually happened. Features were categorised by where their difficulty lies, and the categorisation declined to claim what it could not defend. Requirements were traced to tests. Diagrams were versioned alongside the code so they could not drift from it. And defects were found, understood at the level of root cause, and documented rather than quietly repaired.

That last quality is the one the report would most want to be judged by. The two maintenance iterations are presented not as embarrassments to be minimised but as the process working as intended: a green test suite met an adversarial tester and then a careful reader, and both found things the suite could not. **In a system built to be trustworthy, the trustworthiness of the account of how it was built is not a separate matter.**

---

\newpage
