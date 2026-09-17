# Chapter 4 — Software Development Process

---

## 4.1 The Four Fundamental Process Activities

A software process is a set of related activities that leads to the production of a software product. There are many different software processes, but all of them involve four fundamental activities.

**Table 4.1 — The four fundamental process activities in DEICMS**

| Activity | Definition | How DEICMS performed it |
|---|---|---|
| **Specification** | Defining what the system should do | Personas, five guarantees, 29 user stories with acceptance criteria, FR/NFR tables (Chapter 6) |
| **Development** | Designing and implementing the system | UML modelling (Chapter 7), architecture (Chapter 8), implementation (Chapters 9 and 10) |
| **Validation** | Checking that it does what the customer wants | 172 automated tests plus per-increment sprint reviews against acceptance criteria (Chapter 11) |
| **Evolution** | Changing the system in response to changing needs | Two maintenance iterations, M1 and M2 (Sections 4.12 and 4.13; Chapter 13) |

A **software process description** identifies these activities and the ordering between them. It may also include the *products* that are the outcomes of each activity, the *roles* that reflect the responsibilities of the people involved, and the *pre- and post-conditions* that must hold before and after an activity is enacted.

The critical observation — and the one that separates process models from each other — is that these activities are **interleaved, not sequential**. In a plan-driven process they are separated in time; in an agile process they are interleaved within every cycle. Neither arrangement changes what the activities *are*, only when each is performed and how often.

## 4.2 Plan-Driven and Agile Processes

Processes divide broadly into two families.

In a **plan-driven** process, all of the activities are planned in advance and progress is measured against that plan. The plan is the instrument of control: deviation from it is visible, and management consists largely of keeping the work aligned with it.

In an **agile** process, planning is incremental, and it is easier to change the process to reflect changing customer requirements. Control comes from short feedback cycles rather than from a long-range plan.

**There are no right or wrong software processes.** In practice most real processes include elements of both, and the engineering question is not which family is superior but which mixture fits the risk profile of the work at hand.

**Table 4.2 — Plan-driven versus agile characteristics**

| Dimension | Plan-driven | Agile |
|---|---|---|
| Requirements | Fixed early, changed through formal control | Expected to evolve; welcomed late |
| Planning horizon | The whole project | The current iteration |
| Documentation | Extensive, produced as phase deliverables | Minimal sufficient; working software is the primary measure |
| Delivery | One delivery at the end | A working increment every cycle |
| Risk management | Analysed up front; retired late | Retired continuously by building the risky part early |
| Measure of progress | Phase completion against the plan | Working, accepted functionality |
| Suits | Stable requirements, safety-critical or contractual work, large distributed teams | Uncertain requirements, high technical risk, small co-located teams |

## 4.3 A Survey of Process Models

A **software process model** is a simplified representation of a software process, presented from a particular perspective. The principal models are surveyed below; in practice, most large systems are developed using a process that incorporates elements from several of them.

### 4.3.1 The Waterfall Model

The waterfall model presents the fundamental activities as separate, sequential **phases**: requirements definition, system and software design, implementation and unit testing, integration and system testing, and operation and maintenance. Each phase must in principle be complete and signed off before the next begins, and its output is a set of documents that becomes the input to its successor.

Its strengths are real: it produces thorough documentation, it makes progress measurable against a clear plan, and it suits work where requirements are genuinely stable and where a contractual or regulatory obligation demands phase sign-off. Its weakness is equally real: it is inflexible in the face of change, because a requirement that changes after the design phase invalidates documents that have already been signed off, and it defers all integration and validation to the end, so that technical risk accumulates until a single late moment.

### 4.3.2 The V-Model

The V-model is a refinement of the waterfall that makes the relationship between construction and verification explicit. The descending arm holds the specification and design phases; the ascending arm holds the corresponding test phases; and each construction phase is paired with the test level that validates it — requirements with acceptance testing, system design with system testing, detailed design with integration testing, implementation with unit testing.

Its contribution is the insight that **test planning belongs to the phase whose output it validates**, not to the end of the project. This idea survives the model: DEICMS is not developed with a V-model, but the pairing of each requirement with the test level that verifies it is applied in Section 11.6 and in the traceability matrix of Appendix D.

### 4.3.3 Incremental Development

Incremental development interleaves specification, development and validation, and delivers the system as a series of versions, each adding functionality to its predecessor. It is the basis of agile approaches, though it does not require them: incremental delivery can be managed in a plan-driven way.

Its advantages follow from delivering early and often: the cost of accommodating changing requirements is reduced, because less analysis and documentation has to be redone; customer feedback is obtained on something that actually runs; and more rapid delivery of useful functionality is possible. Its disadvantages are that the process is less visible, because there are fewer document deliverables against which to measure progress, and that system structure tends to degrade as increments are added unless time is spent on refactoring.

### 4.3.4 The Spiral Model

Boehm's spiral model represents the process as a spiral rather than a sequence, with each loop passing through four sectors: objective setting, risk assessment and reduction, development and validation, and planning of the next loop. Its distinguishing feature is that **risk is explicitly assessed and resolved throughout**, and the model is fundamentally risk-driven: each loop chooses its development approach according to the risks that dominate it.

### 4.3.5 Reuse-Oriented Software Engineering

In reuse-oriented development the process is organised around integrating existing components rather than writing new ones. Its stages are requirements specification, component analysis, requirements modification, system design with reuse, development and integration, and system validation. The significant feature is that requirements may be **modified to fit the available components**, trading a degree of requirement fidelity for a large reduction in development effort and risk.

### 4.3.6 The Rational Unified Process

The Rational Unified Process is a modern hybrid that derives from the UML and associated process work. It is described from three perspectives — a dynamic perspective giving the phases over time, a static perspective giving the activities undertaken, and a practice perspective giving good practices to follow. Its four phases are **inception**, **elaboration**, **construction** and **transition**, and unlike waterfall phases these are iterative: several iterations occur within each phase. RUP's essential contribution is the separation of *phases*, which are business milestones, from *workflows*, which are technical activities that recur across all phases.

### 4.3.7 Comparison

**Table 4.3 — Comparison of process models against this project's needs**

| Model | Change handling | Risk retired | Documentation | Fit for DEICMS | Verdict |
|---|---|---|---|---|---|
| **Waterfall** | Poor — change invalidates signed-off documents | Late, at integration | Heavy, phase-gated | Algorithm designs would be fixed on paper before feasibility was known | **Rejected** |
| **V-model** | Poor — inherits waterfall rigidity | Late, though testing is planned early | Heavy | Same rigidity; its test-pairing idea was adopted without the model | **Rejected, idea retained** |
| **Incremental** | Good — each increment re-plans | Continuously | Moderate | Matches the natural dependency order of the three feature tiers | **Selected** |
| **Spiral** | Good — risk-driven loops | Continuously and explicitly | Moderate to heavy | Its ceremony exceeds what a single-developer, single-semester project can sustain | **Rejected, risk focus retained** |
| **Reuse-oriented** | Moderate | Early, by avoiding construction | Light | Category C requires original algorithms, so requirements cannot be bent to fit components | **Rejected as a whole process; applied within Category B** |
| **RUP** | Good | Continuously | Heavy — many prescribed artefacts | Artefact overhead disproportionate for one developer | **Rejected** |

## 4.4 Agile Methods: the Manifesto, Extreme Programming and Scrum

### 4.4.1 Why Agile Methods Arose

Rapid development and delivery is now often the most important requirement for software systems. Businesses operate in fast-changing conditions, and it is practically impossible to produce a set of stable software requirements; software has to evolve quickly to reflect changing business needs. Dissatisfaction with the overheads of the design-heavy methods of the 1980s and 1990s led to the creation of agile methods, which focus on the code rather than the design, are based on an iterative approach, and are intended to deliver working software quickly and evolve it quickly to meet changing requirements. The aim is to reduce process overhead — for example by limiting documentation — and to respond quickly to change without excessive rework. The main agile methods are Extreme Programming, Scrum, Lean Software Development and Crystal.

### 4.4.2 The Agile Manifesto and Its Principles

The Agile Manifesto expresses four value preferences: **individuals and interactions** over processes and tools; **working software** over comprehensive documentation; **customer collaboration** over contract negotiation; and **responding to change** over following a plan. The formulation is deliberately comparative — there is value in the items on the right, but more in those on the left.

**Table 4.4 — The five agile principles and their application in DEICMS**

| Principle | Statement | Application in DEICMS |
|---|---|---|
| **Customer involvement** | Customers should be closely involved throughout, providing and prioritising requirements and evaluating iterations | Adapted: the product-owner role was held consciously and separately by the developer, who wrote and prioritised the backlog and accepted stories at each review (Section 4.6) |
| **Incremental delivery** | The software is developed in increments, with the customer specifying the requirements for each | Three increments of 40, 38 and 42 points, each delivering a working, demonstrable system |
| **People not process** | The skills of the team should be recognised and exploited; members develop their own ways of working | Ceremonies were adapted to a single developer rather than imitated (Section 4.6) |
| **Embrace change** | Expect the system requirements to change, and design the system to accommodate it | Two maintenance iterations absorbed post-delivery change as planned work, not as failure |
| **Maintain simplicity** | Focus on simplicity in both the software and the process; eliminate complexity where possible | Generality was declined where it added risk without demand (Section 3.8) |

### 4.4.3 Extreme Programming

Extreme Programming takes recognised good practice to "extreme" levels: if testing is good, test all the time; if code review is good, review continuously. Its characteristic practices include incremental planning through story cards, small releases, simple design, **test-first development**, refactoring, pair programming, collective ownership, continuous integration, sustainable pace and an on-site customer.

Two XP practices were adopted in DEICMS and one was not. **Test-first development** was adopted from Increment 3 onward, as a direct action from the Increment 2 retrospective, and is credited in Section 4.11 with the steadiness of that increment's burndown. **Refactoring** was adopted continuously, most visibly in the introduction of the `accessible_case_ids` helper in M1. **Pair programming** was impossible with one developer; the partial substitute was the deliberate role separation described in Section 4.6, and the structured review pass that produced M2.

### 4.4.4 Scrum

Scrum is the most widely used agile framework. It differs from XP in focusing on **managing iterative development** rather than prescribing specific technical practices, which is why the two are frequently combined.

Scrum has three phases: an **initial phase** establishing the general objectives and the software architecture; a series of **sprint cycles**, each developing an increment of the system; and a **project closure phase**, which completes the documentation and assesses the lessons learned.

**Table 4.5 — Scrum roles and their adaptation to a single-developer project**

| Role | Responsibility | DEICMS adaptation |
|---|---|---|
| **Product Owner** | Maximises the value of the product; manages the product backlog; business-oriented; keeps the team *building the right thing* | Held by the developer when writing and prioritising user stories, setting MoSCoW priorities, and accepting stories at review |
| **Scrum Master** | Ensures Scrum is understood and enacted; servant-leader, coach and facilitator; keeps the team *building it fast* | Held by the developer when running planning, keeping the burndown, and conducting retrospectives |
| **Development Team** | Delivers a potentially releasable increment of "done" product each sprint; self-organising; keeps the team *building things right* | Held by the developer when designing, implementing and testing |

**Table 4.6 — Scrum ceremonies and their DEICMS equivalents**

| Ceremony | Purpose | DEICMS equivalent |
|---|---|---|
| Sprint planning | Select from the top of the product backlog what the team commits to deliver; scope and end date do not then change | A planning session opening each increment, selecting stories into the sprint backlog and breaking them into estimated tasks |
| Daily scrum | A short meeting reporting three things — done since yesterday, to be done by tomorrow, and blocks; the burndown chart supports self-management | A short daily written note of yesterday, today and blockers |
| Sprint review | A demonstration to the product owner and stakeholders; feedback gathered on what was built | A review at which each story was demonstrated against its acceptance criteria and accepted or rejected |
| Sprint retrospective | The team reviews its way of working: what went well, what could improve, what to commit to improving | A retrospective producing named actions carried into the next increment — every one of which is tracked in Sections 4.9 to 4.13 |

Taking on all three Scrum roles simultaneously is not recommended, because Scrum exists to address problems of interpersonal cooperation that do not arise for a single developer. This report states the adaptation openly rather than describing ceremonies that did not occur, on the principle that an honest account of an adapted process is worth more than a fictional account of a textbook one. The adaptation had one genuine benefit: consciously switching roles is what caused the tester persona to probe adversarially in M1 rather than assume the developer persona had got it right.

## 4.5 Process Model Selection for DEICMS

The project adopted the **Agile Incremental Model**, organised into three increments plus two maintenance iterations, with Scrum-derived ceremonies adapted to a single developer. Four factors were decisive, and each is a property of this project rather than a general preference for agility.

**Factor 1 — Technical risk concentrated in the complex algorithms.** The graph integrity verifier, the risk scorer and the chain reconstructor were the parts of the system whose feasibility and shape were least certain at the outset. A plan-driven model would have committed their full design on paper before any of them had been built, and the near-certainty of discovering during implementation that the design needed to change would have invalidated large amounts of up-front documentation. This was not hypothetical: the verifier's design *did* change substantially during construction, when the traversal had to be reworked from stop-at-first-failure to accumulate-all-failures (Section 4.10).

**Factor 2 — A natural dependency order that rewards increments.** The three feature tiers depend on one another in exactly one sensible order. The algorithms of Increment 2 needed a concrete schema and real records to operate on, which Increment 1 supplied. The risk scorer and AI assistant of Increment 3 needed verified integrity primitives, which Increment 2 supplied. Incremental delivery is not an imposition on this structure; it *is* this structure.

**Factor 3 — The value of feedback between increments.** Each retrospective produced concrete process adjustments that measurably improved the next increment — most consequentially the adoption of test-first development for algorithms, which arose from Increment 2's retrospective and is visible in Increment 3's burndown. A plan-driven model has no natural place for that mid-project learning.

**Factor 4 — Reporting fit.** The coursework requires the report to be organised according to the chosen process, with a section per increment for an agile model. The incremental structure produces exactly the planning-and-reflection artefacts — user stories, sprint backlogs, burndown charts, retrospectives — that make an agile report substantial and verifiable.

**Table 4.7 — The selection decision recorded as an architectural decision record**

| Field | Content |
|---|---|
| **Decision** | Adopt the Agile Incremental Model with Scrum-derived ceremonies, three increments of fourteen working days, plus maintenance iterations as required |
| **Status** | Accepted; retained through project completion |
| **Context** | Single developer; one semester; high technical risk concentrated in five original algorithms; a coursework requirement for per-increment documentation |
| **Alternatives rejected** | Waterfall (change handling), V-model (same rigidity), Spiral (ceremony cost), RUP (artefact overhead), Reuse-oriented (Category C forbids bending requirements to components) |
| **Consequences, positive** | Risk retired continuously; working software from week two; two post-delivery defect classes found and fixed inside the process; retrospective learning compounded across increments |
| **Consequences, negative** | Less up-front documentation than a plan-driven process would have produced; process visibility depends on the burndowns and this report rather than on phase deliverables; the single-developer adaptation weakens the customer-collaboration principle |
| **Validated by** | Section 18.3, which revisits the decision against what actually happened |

## 4.6 Roles, Ceremonies and the Definition of Done

The role and ceremony adaptations are given in Tables 4.5 and 4.6. What remains to be stated is the **definition of done**, which was applied uniformly to every story in every iteration.

**Table 4.8 — Definition of done**

| # | Condition | Rationale |
|---|---|---|
| DoD-1 | Code implemented and integrated into the running application | A story that works only on a branch is not delivered |
| DoD-2 | All acceptance criteria demonstrably met at review | Makes "done" objective rather than a judgement |
| DoD-3 | Covered by automated tests, and those tests pass | Protects the story against later regression |
| DoD-4 | The full existing suite still passes | Prevents a story from being done at another story's expense |
| DoD-5 | Any action touching evidence is recorded in the audit trail | A forensic system may never have an unaudited path |
| DoD-6 | The increment leaves the schema and the system in a consistent state | No story may leave a half-migration behind |

DoD-6 is why, for example, the digital-signature column on custody records was made non-nullable in the same change that introduced signing, rather than in a later tidying pass. A definition of done that permits an increment to leave the schema inconsistent is not a definition of done.

## 4.7 The Increment Plan

**Table 4.9 — The five iterations**

| Iteration | Title | Duration | Stories | Points | Principal deliverable |
|---|---|---|---|---|---|
| Increment 1 | Core Case & Evidence Management | 14 working days | 11 | 40 | A working repository with authentication, RBAC, CRUD, hashing and an append-only audit trail |
| Increment 2 | Integrity Algorithms & State Machine | 14 working days | 6 | 38 | Signed custody events, graph integrity verification, the lifecycle state machine, chain reconstruction |
| Increment 3 | Risk Scoring, AI Assistant & Hardening | 14 working days | 10 | 42 | Risk scoring, the AI assistant, anomaly detection, dashboards, security hardening, export and reporting |
| M1 | Access-Scoping Change Requests | Maintenance | 2 | 10 | Uniform case scoping across every aggregate; role-tailored dashboards; access-scoped assistant |
| M2 | Correctness & Security Hardening | Maintenance | 11 findings | — | Eleven correctness, security and robustness fixes found by structured review |

The sequencing placed the **riskiest work in the middle**: after the foundation had stabilised but before schedule pressure peaked. This is a deliberate application of the spiral model's risk-driven insight inside an incremental frame.

## 4.8 Estimation Method

Because the sprint backlogs and burndown charts are expressed in story points, it is worth setting out precisely how those numbers were arrived at, so that the figures quoted throughout the report are understood as the product of a method rather than as arbitrary values.

Estimation used **story points on a Fibonacci scale** — 1, 2, 3, 5, 8, 13 — rather than hours. The distinction matters. An hour estimate claims to predict how long something will take, which is a prediction developers are famously poor at making; a story point claims only that one piece of work is about twice the size of another, which is a judgement people make far more reliably. The Fibonacci sequence is used because its gaps widen as the numbers grow: it is possible to distinguish a 3 from a 5 with some confidence, but nobody can honestly distinguish a 7 from an 8, and the absence of those intermediate values prevents false precision. The widening gaps also encode a real property of estimation — that uncertainty grows with size, so large items deserve coarser buckets.

**Table 4.10 — Story-point scale and its application**

| Points | Meaning | Representative stories |
|---|---|---|
| 1 | Trivial; a single small piece that reuses existing patterns | US-11 admin-only account creation |
| 2 | Simple; essentially a library call plus its wiring | US-05 SHA-256 fingerprint, US-26 signed ZIP export, US-27 PDF report, US-16 and US-17 report interfaces |
| 3 | Small; a few parts, but no new design work | US-01 login, US-06 metadata extraction, US-10 formula checks, US-19 configurable weights, US-21 hallucination detection, US-23 dashboards |
| 5 | Moderate; multi-part and substantial, but well understood | US-02 role-based access control, US-03 case CRUD, US-04 evidence upload, US-08 custody logging, US-09 audit trail, US-12 digital signing, US-22 anomaly detection, US-24 two-factor authentication |
| 8 | Large; genuine design work, typically a new algorithm | US-14 state machine, US-15 chain reconstruction, US-18 risk scoring, US-20 AI orchestration |
| 13 | Very large; significant unknowns at the time of estimation | US-13 graph integrity verification |

Estimates were assigned **relatively**, anchored on a reference story rather than judged in isolation. US-05, the SHA-256 fingerprint — call a hashing function, store the result in a column, display it — served as the natural 2, and every other story was sized by asking whether it was about the same, roughly twice as large, or several times larger. This anchoring is what keeps a scale internally consistent when one person applies it across several months.

The resulting distribution is itself evidence that the method was applied honestly rather than retrofitted. Every story estimated at 8 is one of the five complex Category C algorithms; every story estimated at 2 is a thin wrapper over a third-party library; and the single 13 in the entire project went to the graph integrity verifier, the one item whose difficulty genuinely could not be predicted in advance. That last judgement proved correct in a way the estimate could not have anticipated: US-13 is precisely where Increment 2's three-day mid-sprint plateau occurred.

It is important to note that **story points and MoSCoW priority are independent dimensions**, even though they appear side by side in the same backlog tables. A point value answers *how large is this?*; a MoSCoW priority answers *what happens if time runs out?*. The two do not correlate, and deliberately so. US-11, admin-only account creation, is the smallest story in the project at 1 point yet is a Must, because a forensic system that permits self-registration is unacceptable regardless of how little code the restriction requires. Conversely US-22, the Isolation Forest anomaly detection, is a 5-point story but only a Could, because it represents real work whose absence would leave the system coherent. Keeping size and importance separate is what allows scope to be cut sensibly under pressure: one drops the least important work, not the largest.

The increment totals quoted throughout this report are **derived quantities rather than planning targets**: each is the arithmetic sum of the estimates of the stories allocated to that increment. Increment 1 totals forty points across eleven stories (3+5+5+5+2+3+3+5+5+3+1), Increment 2 thirty-eight points across six (5+13+8+8+2+2), and Increment 3 forty-two points across ten (8+3+8+3+5+3+5+3+2+2); maintenance iteration M1 contributes a further ten points (5+5), giving a project total of one hundred and thirty points. That the three increment totals fall within the narrow band of thirty-eight to forty-two is a consequence of **capacity rather than coincidence**. Each increment occupied a fixed cycle of fourteen working days undertaken by a single developer, so the volume of work admitted to an increment was bounded by the throughput observed in the preceding one. Increment 1 established that bound empirically by completing forty points within its cycle; forty points per increment therefore became the project's measured velocity, and the two subsequent increments were loaded against that measurement rather than against an assumed rate. This ordering — estimate the work, measure the capacity, then fit the plan to the measurement — is the relationship between estimation and planning prescribed by agile practice, in which velocity is treated as an observed property of the team rather than a target imposed upon it.

A methodological limitation must be acknowledged, noted in Section 4.5 and revisited in the velocity analysis of Section 18.2: a single-developer project places the estimator and the implementer in the same person, so estimates can be adjusted with perfect knowledge of the implementer's pace. The report therefore treats the *shape* of each burndown chart — where progress stalled and where it recovered — as more informative than the fact that each increment's total was met.

---

## 4.9 Increment 1 — Core Case and Evidence Management

### 4.9.1 Sprint Goal

The goal of the first increment was to build the foundation on which everything else would stand: a working evidence repository in which investigators log in, manage cases, register hashed evidence, and have every action recorded in a tamper-evident trail. Expressed as a single sentence, the sprint goal was *"an authenticated, role-aware system in which cases and evidence can be managed and every action is audited."*

Nothing in this increment is algorithmically complex — that is by design. The increment exists to make the later algorithms possible by giving them a concrete, stable data model and a body of real records to operate on, and to retire the routine-but-numerous risks of authentication, authorisation, file handling and persistence before the harder work begins.

### 4.9.2 Sprint Backlog

**Table 4.11 — Increment 1 sprint backlog**

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

Full acceptance criteria for every story are given in Section 6.5 and Appendix A; the implementation is described in Chapter 9.

### 4.9.3 UML Artefacts Produced

The use-case diagram (Figure 7.1), the class diagram (Figure 7.4) and the entity-relationship diagram (Figure 7.5), all presented in Chapter 7.

### 4.9.4 Sprint Review

All eleven stories were demonstrated against their acceptance criteria and all forty story points were accepted. The increment delivered a system that could be logged into, that enforced its four roles and case memberships, that managed cases and registered hashed evidence with extracted metadata, that recorded custody and audited every action immutably, and that ran the three formula checks.

Measured against the five guarantees of Table 1.1, Increment 1 fully delivered **G3** (tamper-evident complete record) and **G2** (case-scoped access, at the record level), laid the foundation for **G1** by capturing the intake hash and the ordered custody log, and left **G4** and **G5** to the increments designed for them.

### 4.9.5 Burndown

**[FIGURE 4.1 — Increment 1 burndown chart]**

The chart plots ideal and actual story points remaining across the fourteen-day cycle. The actual line runs above the ideal for the first several days: days zero to two produced no burned points at all, because environment setup — the Flask application factory, the SQLAlchemy configuration and the Git repository — took longer than planned, and the first story was not completed until day two. From about day nine the actual line converges back toward the ideal, and all forty points were delivered by day fourteen. The chart's shape is therefore a slow start followed by a recovery.

### 4.9.6 Retrospective

**Table 4.12 — Increment 1 retrospective**

| Category | Finding |
|---|---|
| **What went well** | The application-factory pattern made the system testable from the first week and repaid its small up-front cost many times over |
| **What went well** | Writing audit-trail hooks into each route as the route was built, rather than in a later pass, meant the system was never without a complete history |
| **What went less well** | The zero-burn start: environment and scaffolding work was real work not represented as points, so the burndown looked alarming before it looked healthy |
| **What went less well** | The estimate for routine CRUD-and-template work was slightly optimistic |
| **Action A1-1** | Reserve day zero of Increment 2 explicitly for a design spike on the graph integrity algorithm, whose 13-point estimate reflected real uncertainty |
| **Action A1-2** | Fix the canonical format of the data that custody signing will sign *before* writing any signing code, so signer and verifier cannot disagree about what bytes are signed |

Both actions were carried out, and Section 4.10.6 records that both proved well judged.

---

## 4.10 Increment 2 — Integrity Algorithms and Lifecycle

### 4.10.1 Sprint Goal

Where the first increment built a repository that could *store* a chain of custody, the second built the machinery that makes that chain *provable and rule-bound*. The sprint goal was *"make the chain of custody cryptographically verifiable and procedurally enforced"* — to turn the ordered custody records of Increment 1 from a set of claims into a set of proofs, and to turn the evidence lifecycle from an informal sequence of statuses into a formal automaton that the system enforces.

This is the increment in which the first three of the project's five complex algorithms were designed and built, and it was therefore the increment of highest technical risk, which is precisely why it was placed in the middle of the schedule.

### 4.10.2 Sprint Backlog

**Table 4.13 — Increment 2 sprint backlog**

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

### 4.10.3 UML Artefacts Produced

The sequence diagram of graph integrity verification (Figure 7.6), the state machine diagram of the evidence lifecycle (Figure 7.9) and the activity diagram of chain reconstruction (Figure 7.8), all presented in Chapter 7. Because this increment's work is algorithmic, its artefacts are behavioural rather than structural.

### 4.10.4 Sprint Review

All six stories were demonstrated against their acceptance criteria and all thirty-eight points accepted. The increment delivered signed custody events, a graph verifier that walks an entire chain and reports a verdict with a completeness score and located failures, a state machine that enforces the lifecycle with role guards and preconditions, and a reconstruction algorithm that fills gaps honestly with confidence labelling.

Against the five guarantees, Increment 2 completed **G1** (provable integrity) and delivered **G4** (enforced procedural rules) in full, leaving only **G5** for Increment 3.

### 4.10.5 Burndown

**[FIGURE 4.2 — Increment 2 burndown chart]**

This chart shows the roughest middle of the project. The actual line tracks the ideal for the first several days, then **plateaus across days five to seven**, during which almost no points were burned. The plateau is the graph-integrity rework: the depth-first traversal, initially written to stop at the first failure, had to be reworked to accumulate all failures while continuing, and that rework surfaced a payload-format mismatch between the signer and the verifier that took further time to diagnose. From about day eight the line resumes its descent and steepens, because the state machine and the reconstruction algorithm were able to reuse the test fixtures and graph-building patterns established while building the verifier, and all thirty-eight points were delivered by day fourteen.

### 4.10.6 Retrospective

**Table 4.14 — Increment 2 retrospective**

| Category | Finding |
|---|---|
| **What went well** | Action A1-1 paid off directly: freezing the canonical payload format before writing signing code is what made the eventual payload-mismatch bug tractable rather than mysterious |
| **What went well** | Building reusable test fixtures while constructing the first algorithm sharply reduced the cost of testing the second and third |
| **What went less well** | The three-day plateau, whose lesson was estimation-related: the 13-point estimate for the verifier was correct in magnitude but wrong in its reasoning — the cryptographic checks that had seemed hard were straightforward library calls, while the traversal semantics that had seemed straightforward were the real difficulty |
| **Action A2-1** | Write the acceptance criteria of each complex algorithm as unit tests *before* implementing it, so that the definition of "all failures found" or "score in range" is pinned down in advance |
| **Action A2-2** | Keep the language model behind an interface so that the assistant pipeline can be tested without external credits |

Both actions were carried out, and Section 4.11.6 records that both paid off measurably.

---

## 4.11 Increment 3 — Risk Scoring, AI Assistant and Hardening

### 4.11.1 Sprint Goal

The first two increments produced a system that stored a chain of custody, proved its integrity and enforced its lifecycle. The third turns that trustworthy record into something an investigator can *act on efficiently*, and hardens the whole system to the standard a forensic application demands. The sprint goal was *"turn verified records into judgement, and make the system safe to deploy."*

This was the largest increment. It contains two of the project's five complex algorithms alongside a cluster of third-party integrations and security features, and it was placed last deliberately: the risk scorer depends on the integrity verifier and the state machine built in Increment 2, and the assistant's most valuable capability — answering integrity questions — depends on being able to run a fresh verification.

### 4.11.2 Sprint Backlog

**Table 4.15 — Increment 3 sprint backlog**

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

### 4.11.3 UML Artefacts Produced

The activity diagram of risk scoring (Figure 7.7), the sequence diagram of the AI orchestration workflow (Figure 7.10), and the component and deployment diagrams of the whole system (Figures 7.11 and 7.12), all presented in Chapter 7. The last two were completed in this increment because only now were all the modules in place to be drawn.

### 4.11.4 Sprint Review

All ten stories were demonstrated and all forty-two points accepted. The increment delivered the multi-factor risk scorer with configurable weights, the six-stage AI assistant with hallucination detection, the Isolation Forest anomaly pipeline, the dashboards, the full security-hardening suite, and the signed export and PDF report.

With this increment the fifth guarantee — **G5**, analytical prioritisation — was delivered, completing the set, and the system reached the functional scope defined at the outset.

### 4.11.5 Burndown

**[FIGURE 4.3 — Increment 3 burndown chart]**

This is the steadiest of the three charts, tracking within about two points of the ideal throughout, with a slight early slip on days one to three recovered by day four. The steadiness is directly attributable to the two actions carried in from Increment 2: writing the risk-scoring tests before the implementation caught the normalisation edge cases before they could reach a route and cause a late surprise, and hiding the language model behind a mock seam meant the assistant pipeline could be built and tested continuously rather than being blocked on external credits or network availability. The security stories integrated cleanly because the audit and custody layers from earlier increments already exposed the hooks they needed.

### 4.11.6 Retrospective

**Table 4.16 — Increment 3 retrospective**

| Category | Finding |
|---|---|
| **What went well** | Both carried-in actions paid off measurably, and the burndown is the evidence |
| **General principle recorded** | The parts of the system given the most tests and the most isolation — the algorithms and the external model — caused the fewest surprises |
| **What went less well** | The one significant defect class that emerged did so in exactly the area that had *not* been given a dedicated test focus: access scoping in the aggregate views and the assistant |
| **Action A3-1** | Raise the access-scoping defects as a formal maintenance iteration rather than patching them silently within the increment |

Action A3-1 is the reason Section 4.12 exists. An honest agile process surfaces the defects its own testing reveals and schedules the work to fix them rather than quietly absorbing them.

---

## 4.12 Maintenance Iteration M1 — Access-Scoping Change Requests

### 4.12.1 Change After Delivery in the Incremental Model

The three increments delivered the full functional scope defined at the project's outset, and at the end of Increment 3 the system met all of its acceptance criteria and passed its test suite. In a plan-driven project that would have been the end of the engineering narrative. In an incremental, agile project it is not, because one of the model's defining strengths is that it accommodates change discovered *after* a working version exists without treating that change as a failure of planning.

M1 is presented as a first-class iteration, with the same planning-and-reflection structure as the increments, for two reasons. First, handling change after delivery is a core software-engineering activity that a report demonstrating the discipline should show rather than hide. Second, the specific defects M1 resolved are instructive: they were not crashes or failing tests — the system worked and its tests were green — but **authorisation** defects, the most dangerous kind for a forensic system and precisely the kind ordinary functional testing does not catch.

The iteration was scoped at **ten story points** across two change-request stories. Both were classified *must-have* despite arising after the planned scope was complete, because a data-leakage defect in a system whose entire purpose is controlled access cannot be deferred.

### 4.12.2 Defect Discovery Through Review Testing

The defects were found not by the automated test suite but by deliberate **review testing**, in which the tester persona actively attempted to do things the system should forbid, rather than confirming that permitted actions work.

This distinction is the iteration's first lesson. The automated tests written during the three increments were, appropriately, *positive* tests: they confirmed that an administrator could see the dashboard, that a lead investigator could rank items by risk, that the assistant answered questions. None asked the adversarial question — *can a user see data they should not?* — because each test constructed only the data it needed and then checked the feature worked on it. The leakage was invisible to that style of testing because it manifests only when data from *another* case exists and a user without access to it views an aggregate.

**Table 4.17 — M1 change requests**

| CR | Story | Defect observed | Points |
|---|---|---|---|
| CR-01 | US-28 | The dashboard, risk dashboard and anomaly view queried every case, evidence item and audit record in the system regardless of the viewer's role or memberships | 5 |
| CR-02 | US-29 | The AI assistant retrieved context globally, could not answer identity questions, retained conversation history across logout, and took one to two minutes to respond | 5 |

### 4.12.3 CR-01 — Role-Scoped Dashboard and Aggregated Views

**Root cause.** The dashboard and risk routes had been written in Increment 3 to query entities globally, because at the time the case-scoping concern had been associated with the case-list and record-detail routes rather than recognised as a property *every aggregate must share*. There was no single place expressing "the set of cases this user may see"; the case list computed it inline, and nothing else reused it.

**Solution.** The fix introduced exactly that missing abstraction: a single helper, `accessible_case_ids`, returning the set of case identifiers a given investigator may see — a sentinel meaning "all cases" for an administrator, the list of memberships for anyone else, and an empty list for a user belonging to no case. Every aggregate query was then routed through it. Centralising the rule in one helper is the essential engineering move: the scoping is defined once and applied uniformly, and a future aggregate view cannot omit it without the omission being conspicuous.

**Beyond the fix.** Scoping the dashboard raised a design question the global version never had to answer: what should a read-only user with no shared cases *see*, if not everything? A naive scoping would have left a blank page. The solution turned the constraint into a feature by making the dashboard **role-tailored** — each role sees panels matched to its work, every role has a "your recent activity" panel guaranteeing no dashboard is ever empty, and a user belonging to no case sees an explanatory message rather than a blank or a global view. This is an example of a security requirement *improving* rather than degrading the user experience.

### 4.12.4 CR-02 — Access-Scoped AI Assistant and Chat Isolation

Four related problems were addressed at their roots. Retrieval was routed through the same `accessible_case_ids` helper, so the assistant retrieves only from accessible cases and a request outside that set returns an access-denied line. An *identity* intent was added and checked with priority, and the authenticated user's identity injected into the prompt, so "who am I" and "my cases" are answerable. The stored conversation was tagged with the owning user's identifier and cleared on both login and logout. The latency was reduced by defaulting to a smaller, faster model and adding a request timeout together with a browser-side abort.

### 4.12.5 Regression Testing

The iteration's second lesson is embodied in its testing. Because the defects escaped positive-only tests, the fixes were accompanied by a dedicated module of fourteen tests written in the **adversarial** style. These construct a scenario with two leads, an analyst and a read-only auditor, and two cases with memberships deliberately arranged so that one lead and the analyst belong to the first case, the other lead to the second, and the auditor to neither — then assert the *negative* properties directly. Alongside the new module, the full existing suite was re-run to confirm that scoping every aggregate had not broken previously passing behaviour.

### 4.12.6 Iteration Review and Reflection

**Table 4.18 — M1 reflection**

| Lesson | Content |
|---|---|
| **On testing** | Positive functional tests, however thorough, do not exercise authorisation boundaries. A system with an access-control requirement needs *negative* tests that actively attempt forbidden actions — a practice adopted from this point on |
| **On abstraction and its timing** | The leakage existed because the scoping rule was expressed inline in one place rather than as a reusable helper, so later surfaces could not reuse it and silently omitted it. Introducing `accessible_case_ids` did not only fix the present defects; it made the class of defect much harder to reintroduce, because the correct behaviour is now the easy, obvious thing to call |

Both lessons are of a kind that surfaces only once a working system exists to be probed — which is itself the argument for the incremental model.

---

## 4.13 Maintenance Iteration M2 — Correctness and Security Hardening

### 4.13.1 Origin: a Final Review and Regression Pass

Where M1 was triggered by exploratory review testing, M2 came out of a final review pass over the whole system once the access-scoping fixes had settled — a deliberate read of every logic module, model and route, together with a full re-run of the test suite, before the project was considered finished. The review produced a findings list recording each defect with its cause and a recommended remedy, and **no code was changed until the whole list existed**, so that fixes could be prioritised by severity rather than patched in the order they happened to be noticed.

Reading a working system is a different activity from testing it, and that difference is why the pass was worth doing. Testing asks whether the code does what a test expects; reading asks whether the code actually *means* what it appears to mean. Several defects found here are of a kind testing is structurally poor at catching — a feature that silently does nothing, a computation that reads a field which does not exist, a permission check applied to the wrong identifier — because the tests around them pass happily while the underlying behaviour is wrong. This complements M1's lesson: M1 showed that authorisation defects need adversarial testing; M2 showed that certain correctness defects need reading rather than running.

### 4.13.2 Findings

**Table 4.19 — M2 findings**

| # | Finding | Theme | Severity | Resolution |
|---|---|---|---|---|
| D1 | Evidence deletion set a non-existent attribute and persisted nothing, while writing an audit record stating the item had been removed | Correctness | Critical | Added a real `is_deleted` column and the startup migration; changed the route to record an honest soft delete; filtered deleted items from every listing path |
| D2 | The highest-weighted risk factor (0.25) read an `integrity_status` column that did not exist, so a quarter of the risk algorithm returned a constant | Correctness | Critical | Added a real `integrity_status` column written back from the graph verifier, closing the loop between the Increment 2 verifier and the Increment 3 scorer |
| D3 | Evidence routes checked access against the case identifier in the URL but loaded the item by its own identifier, permitting cross-case access | Correctness / Security | Critical | Verify that the loaded item's case matches the access that was checked |
| D4 | Custody signing failure could abort a transfer or leave an unverifiable record | Correctness | High | Standardised fail-visible behaviour: an explicit unsigned sentinel with a user warning, reported by the verifier as unverified |
| D5 | Two risk factors counted integrity-check and warning audit events, so running a verification *raised* an item's risk | Correctness | High | Pointed both factors at the genuine Category A formula checks, producing the deliberate cross-category integration described in Chapter 15 |
| D6 | Mixed timezone-aware and naive timestamps risked comparison errors | Correctness | Medium | Routed the custody timestamp default through the shared local-time helper |
| H1 | Untrusted model output rendered as HTML in the chat (stored XSS) | Security | High | Escape the output, then re-apply only the intended lightweight formatting after escaping |
| H2 | No Content-Security-Policy or complementary hardening headers | Security | Medium | Added CSP plus `X-Content-Type-Options`, `X-Frame-Options` and `Referrer-Policy` |
| H3 | No warning when running with insecure default secrets | Security | Low | Emit a clear startup warning whenever either secret is at its default |
| R1 | Unbounded case and evidence listings | Robustness | Low | Paginated both |
| R2 | The intent classifier mis-ranked self-referential questions | Robustness | Low | Added a priority rule, pinned down by a dedicated test module |

Of these, **D1 and D2 are the most instructive**. D1 made the audit trail — the system's most trusted artefact — state something false, which for a chain-of-custody system is the worst category of defect. D2 silently disabled a quarter of the flagship risk algorithm while every surrounding test passed. Neither was in the path of any test's expectation, which is the point.

### 4.13.3 Schema Migration and Regression Testing

Two fixes added columns to the Evidence Item entity, and a database created under the earlier schema would lack them. Rather than requiring a rebuild, the columns were added to the lightweight startup migration routine introduced in Increment 1, which inspects the existing columns and adds any that are missing. Every fix was accompanied by tests, and the complete suite re-run. The final result is a suite of **one hundred and seventy-two tests, all passing**.

### 4.13.4 Iteration Review and Reflection

M2 delivered eleven fixes and left the system materially more trustworthy than the version that had passed all its tests at the end of Increment 3. Its central reflection complements M1's: a distinct class of correctness defect is best caught by *reading* code against its intent, because the surrounding tests pass while the behaviour is quietly wrong.

That two critical findings had survived a full increment and a green test suite is not an indictment of the testing but an illustration of its limits — a test confirms that the code does what the test expects, and neither defect was in the path of any expectation. The practical conclusion is that **testing and review are complementary rather than substitutable**: the suite guards against regression in behaviour that is exercised, while periodic review guards against behaviour that is specified but silently absent.

---

## 4.14 Comparison with a Plan-Driven Execution

It is worth asking directly what would have happened had this project been executed as a waterfall, since the professor's question *why did you choose this model?* deserves an answer grounded in evidence rather than preference.

**Table 4.20 — What a waterfall execution would have produced**

| Project event | What actually happened (agile incremental) | What waterfall would have produced |
|---|---|---|
| The graph verifier's traversal semantics changed during construction | Reworked inside Increment 2; the burndown recorded a three-day plateau and the project continued | The design document would have been signed off with stop-at-first-failure semantics; the change would have required a formal change request against an approved design |
| The external language model was retired by its provider | Absorbed by an ordered fallback list; one day's work | Discovered at system-integration testing, after all development was complete and with no schedule slack remaining |
| Access-scoping defects in aggregates and the assistant | Found by review testing on a running system, then fixed as a planned iteration | Not discoverable before system testing, because no running system exists until then; the fix would have touched code declared complete |
| Two critical correctness defects found by reading code | Fixed in M2 with a full regression suite as a safety net | The regression suite would not have existed until the testing phase, so each fix would carry unmeasured risk |
| Estimates calibrated against measured velocity | Velocity observed in Increment 1 and used to load Increments 2 and 3 | Estimates fixed at the planning phase with no opportunity to recalibrate |

The pattern is consistent: every significant discovery in this project was made **by having working software early enough to probe**. That is precisely the property waterfall does not provide, and it is the substantive reason for the choice — not a preference for agility as a style.

The honest counter-argument should also be stated. Waterfall would have produced more thorough up-front documentation, and in a domain with legal and evidentiary obligations that documentation has genuine value; a forensic product sold commercially might well be required to demonstrate phase-gated design review. The report's position is not that waterfall is inferior in general, but that for a project whose dominant risk was *algorithmic feasibility* rather than *requirement volatility or contractual compliance*, incremental delivery retired the dominant risk and waterfall would not have.

## 4.15 Summary

This chapter defined the four fundamental process activities, contrasted plan-driven and agile families, surveyed six process models with a comparison against this project's needs, and set out the agile method vocabulary — the manifesto, its five principles, Extreme Programming and Scrum's three phases, three roles and four ceremonies. It then recorded the selection of the Agile Incremental Model as a decision with explicit alternatives, consequences and validation criteria, stated the definition of done, and explained the story-point estimation method and the independence of size from MoSCoW priority.

The five iterations were then documented in full — three increments each with sprint goal, backlog, UML artefacts, review, burndown and retrospective, and two maintenance iterations with their findings, fixes and reflections. Every retrospective action was tracked into the iteration that executed it. Finally, the process choice was tested against a counterfactual waterfall execution, event by event.

The next chapter turns from the process itself to its management: how the work was broken down, scheduled, risk-assessed and quality-assured.

---

\newpage
