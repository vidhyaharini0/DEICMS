# Chapter 4 - Software Development Process

---

## 4.1 The Four Fundamental Process Activities

A software process is a set of related activities that leads to the production of a software product. There are many different software processes, but all of them involve four fundamental activities.

**Table 4.1 - The four fundamental process activities in DEICMS**

| Activity | Definition | How DEICMS performed it |
|---|---|---|
| **Specification** | Defining what the system should do | Personas, five guarantees, 29 user stories with acceptance criteria, FR/NFR tables (Chapter 7) |
| **Development** | Designing and implementing the system | UML modelling (Chapter 8), architecture (Chapter 9), implementation (Chapters 10 and 11) |
| **Validation** | Checking that it does what the customer wants | 172 automated tests plus per-increment sprint reviews against acceptance criteria (Chapter 12) |
| **Evolution** | Changing the system in response to changing needs | Two maintenance iterations, M1 and M2 (Sections 5.4 and 5.5; Chapter 14) |

A **software process description** identifies these activities and the ordering between them. It may also include the *products* that are the outcomes of each activity, the *roles* that reflect the responsibilities of the people involved, and the *pre- and post-conditions* that must hold before and after an activity is enacted.

The critical observation - and the one that separates process models from each other - is that these activities are **interleaved, not sequential**. In a plan-driven process they are separated in time; in an agile process they are interleaved within every cycle. Neither arrangement changes what the activities *are*, only when each is performed and how often.

## 4.2 Plan-Driven and Agile Processes

Processes divide broadly into two families.

In a **plan-driven** process, all of the activities are planned in advance and progress is measured against that plan. The plan is the instrument of control: deviation from it is visible, and management consists largely of keeping the work aligned with it.

In an **agile** process, planning is incremental, and it is easier to change the process to reflect changing customer requirements. Control comes from short feedback cycles rather than from a long-range plan.

**There are no right or wrong software processes.** In practice most real processes include elements of both, and the engineering question is not which family is superior but which mixture fits the risk profile of the work at hand.

**Table 4.2 - Plan-driven versus agile characteristics**

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

The V-model is a refinement of the waterfall that makes the relationship between construction and verification explicit. The descending arm holds the specification and design phases; the ascending arm holds the corresponding test phases; and each construction phase is paired with the test level that validates it - requirements with acceptance testing, system design with system testing, detailed design with integration testing, implementation with unit testing.

Its contribution is the insight that **test planning belongs to the phase whose output it validates**, not to the end of the project. This idea survives the model: DEICMS is not developed with a V-model, but the pairing of each requirement with the test level that verifies it is applied in Section 12.6 and in the traceability matrix of Appendix D.

### 4.3.3 Incremental Development

Incremental development interleaves specification, development and validation, and delivers the system as a series of versions, each adding functionality to its predecessor. It is the basis of agile approaches, though it does not require them: incremental delivery can be managed in a plan-driven way.

Its advantages follow from delivering early and often: the cost of accommodating changing requirements is reduced, because less analysis and documentation has to be redone; customer feedback is obtained on something that actually runs; and more rapid delivery of useful functionality is possible. Its disadvantages are that the process is less visible, because there are fewer document deliverables against which to measure progress, and that system structure tends to degrade as increments are added unless time is spent on refactoring.

### 4.3.4 The Spiral Model

Boehm's spiral model represents the process as a spiral rather than a sequence, with each loop passing through four sectors: objective setting, risk assessment and reduction, development and validation, and planning of the next loop. Its distinguishing feature is that **risk is explicitly assessed and resolved throughout**, and the model is fundamentally risk-driven: each loop chooses its development approach according to the risks that dominate it.

### 4.3.5 Reuse-Oriented Software Engineering

In reuse-oriented development the process is organised around integrating existing components rather than writing new ones. Its stages are requirements specification, component analysis, requirements modification, system design with reuse, development and integration, and system validation. The significant feature is that requirements may be **modified to fit the available components**, trading a degree of requirement fidelity for a large reduction in development effort and risk.

### 4.3.6 The Rational Unified Process

The Rational Unified Process is a modern hybrid that derives from the UML and associated process work. It is described from three perspectives - a dynamic perspective giving the phases over time, a static perspective giving the activities undertaken, and a practice perspective giving good practices to follow. Its four phases are **inception**, **elaboration**, **construction** and **transition**, and unlike waterfall phases these are iterative: several iterations occur within each phase. RUP's essential contribution is the separation of *phases*, which are business milestones, from *workflows*, which are technical activities that recur across all phases.

### 4.3.7 Comparison

**Table 4.3 - Comparison of process models against this project's needs**

| Model | Change handling | Risk retired | Documentation | Fit for DEICMS | Verdict |
|---|---|---|---|---|---|
| **Waterfall** | Poor - change invalidates signed-off documents | Late, at integration | Heavy, phase-gated | Algorithm designs would be fixed on paper before feasibility was known | **Rejected** |
| **V-model** | Poor - inherits waterfall rigidity | Late, though testing is planned early | Heavy | Same rigidity; its test-pairing idea was adopted without the model | **Rejected, idea retained** |
| **Incremental** | Good - each increment re-plans | Continuously | Moderate | Matches the natural dependency order of the three feature tiers | **Selected** |
| **Spiral** | Good - risk-driven loops | Continuously and explicitly | Moderate to heavy | Its ceremony exceeds what a single-developer, single-semester project can sustain | **Rejected, risk focus retained** |
| **Reuse-oriented** | Moderate | Early, by avoiding construction | Light | Category C requires original algorithms, so requirements cannot be bent to fit components | **Rejected as a whole process; applied within Category B** |
| **RUP** | Good | Continuously | Heavy - many prescribed artefacts | Artefact overhead disproportionate for one developer | **Rejected** |

## 4.4 Agile Methods: the Manifesto, Extreme Programming and Scrum

### 4.4.1 Why Agile Methods Arose

Rapid development and delivery is now often the most important requirement for software systems. Businesses operate in fast-changing conditions, and it is practically impossible to produce a set of stable software requirements; software has to evolve quickly to reflect changing business needs. Dissatisfaction with the overheads of the design-heavy methods of the 1980s and 1990s led to the creation of agile methods, which focus on the code rather than the design, are based on an iterative approach, and are intended to deliver working software quickly and evolve it quickly to meet changing requirements. The aim is to reduce process overhead - for example by limiting documentation - and to respond quickly to change without excessive rework. The main agile methods are Extreme Programming, Scrum, Lean Software Development and Crystal.

### 4.4.2 The Agile Manifesto and Its Principles

The Agile Manifesto expresses four value preferences: **individuals and interactions** over processes and tools; **working software** over comprehensive documentation; **customer collaboration** over contract negotiation; and **responding to change** over following a plan. The formulation is deliberately comparative - there is value in the items on the right, but more in those on the left.

**Table 4.4 - The five agile principles and their application in DEICMS**

| Principle | Statement | Application in DEICMS |
|---|---|---|
| **Customer involvement** | Customers should be closely involved throughout, providing and prioritising requirements and evaluating iterations | Adapted: the product-owner role was held consciously and separately by the developer, who wrote and prioritised the backlog and accepted stories at each review (Section 4.6) |
| **Incremental delivery** | The software is developed in increments, with the customer specifying the requirements for each | Three increments of 40, 38 and 42 points, each delivering a working, demonstrable system |
| **People not process** | The skills of the team should be recognised and exploited; members develop their own ways of working | Ceremonies were adapted to a single developer rather than imitated (Section 4.6) |
| **Embrace change** | Expect the system requirements to change, and design the system to accommodate it | Two maintenance iterations absorbed post-delivery change as planned work, not as failure |
| **Maintain simplicity** | Focus on simplicity in both the software and the process; eliminate complexity where possible | Generality was declined where it added risk without demand (Section 3.8) |

### 4.4.3 Extreme Programming

Extreme Programming takes recognised good practice to "extreme" levels: if testing is good, test all the time; if code review is good, review continuously. Its characteristic practices include incremental planning through story cards, small releases, simple design, **test-first development**, refactoring, pair programming, collective ownership, continuous integration, sustainable pace and an on-site customer.

Two XP practices were adopted in DEICMS and one was not. **Test-first development** was adopted from Increment 3 onward, as a direct action from the Increment 2 retrospective, and is credited in Section 5.3 with the steadiness of that increment's burndown. **Refactoring** was adopted continuously, most visibly in the introduction of the `accessible_case_ids` helper in M1. **Pair programming** was impossible with one developer; the partial substitute was the deliberate role separation described in Section 4.6, and the structured review pass that produced M2.

### 4.4.4 Scrum

Scrum is the most widely used agile framework. It differs from XP in focusing on **managing iterative development** rather than prescribing specific technical practices, which is why the two are frequently combined.

Scrum has three phases: an **initial phase** establishing the general objectives and the software architecture; a series of **sprint cycles**, each developing an increment of the system; and a **project closure phase**, which completes the documentation and assesses the lessons learned.

**Table 4.5 - Scrum roles and their adaptation to a single-developer project**

| Role | Responsibility | DEICMS adaptation |
|---|---|---|
| **Product Owner** | Maximises the value of the product; manages the product backlog; business-oriented; keeps the team *building the right thing* | Held by the developer when writing and prioritising user stories, setting MoSCoW priorities, and accepting stories at review |
| **Scrum Master** | Ensures Scrum is understood and enacted; servant-leader, coach and facilitator; keeps the team *building it fast* | Held by the developer when running planning, keeping the burndown, and conducting retrospectives |
| **Development Team** | Delivers a potentially releasable increment of "done" product each sprint; self-organising; keeps the team *building things right* | Held by the developer when designing, implementing and testing |

**Table 4.6 - Scrum ceremonies and their DEICMS equivalents**

| Ceremony | Purpose | DEICMS equivalent |
|---|---|---|
| Sprint planning | Select from the top of the product backlog what the team commits to deliver; scope and end date do not then change | A planning session opening each increment, selecting stories into the sprint backlog and breaking them into estimated tasks |
| Daily scrum | A short meeting reporting three things - done since yesterday, to be done by tomorrow, and blocks; the burndown chart supports self-management | A short daily written note of yesterday, today and blockers |
| Sprint review | A demonstration to the product owner and stakeholders; feedback gathered on what was built | A review at which each story was demonstrated against its acceptance criteria and accepted or rejected |
| Sprint retrospective | The team reviews its way of working: what went well, what could improve, what to commit to improving | A retrospective producing named actions carried into the next increment - every one of which is tracked in Chapter 5 |

Taking on all three Scrum roles simultaneously is not recommended, because Scrum exists to address problems of interpersonal cooperation that do not arise for a single developer. This report states the adaptation openly rather than describing ceremonies that did not occur, on the principle that an honest account of an adapted process is worth more than a fictional account of a textbook one. The adaptation had one genuine benefit: consciously switching roles is what caused the tester persona to probe adversarially in M1 rather than assume the developer persona had got it right.

## 4.5 Process Model Selection for DEICMS

The project adopted the **Agile Incremental Model**, organised into three increments plus two maintenance iterations, with Scrum-derived ceremonies adapted to a single developer. Four factors were decisive, and each is a property of this project rather than a general preference for agility.

**Factor 1 - Technical risk concentrated in the complex algorithms.** The graph integrity verifier, the risk scorer and the chain reconstructor were the parts of the system whose feasibility and shape were least certain at the outset. A plan-driven model would have committed their full design on paper before any of them had been built, and the near-certainty of discovering during implementation that the design needed to change would have invalidated large amounts of up-front documentation. This was not hypothetical: the verifier's design *did* change substantially during construction, when the traversal had to be reworked from stop-at-first-failure to accumulate-all-failures (Section 5.2).

**Factor 2 - A natural dependency order that rewards increments.** The three feature tiers depend on one another in exactly one sensible order. The algorithms of Increment 2 needed a concrete schema and real records to operate on, which Increment 1 supplied. The risk scorer and AI assistant of Increment 3 needed verified integrity primitives, which Increment 2 supplied. Incremental delivery is not an imposition on this structure; it *is* this structure.

**Factor 3 - The value of feedback between increments.** Each retrospective produced concrete process adjustments that measurably improved the next increment - most consequentially the adoption of test-first development for algorithms, which arose from Increment 2's retrospective and is visible in Increment 3's burndown. A plan-driven model has no natural place for that mid-project learning.

**Factor 4 - Reporting fit.** The coursework requires the report to be organised according to the chosen process, with a section per increment for an agile model. The incremental structure produces exactly the planning-and-reflection artefacts - user stories, sprint backlogs, burndown charts, retrospectives - that make an agile report substantial and verifiable.

**Table 4.7 - The selection decision recorded as an architectural decision record**

| Field | Content |
|---|---|
| **Decision** | Adopt the Agile Incremental Model with Scrum-derived ceremonies, three increments of fourteen working days, plus maintenance iterations as required |
| **Status** | Accepted; retained through project completion |
| **Context** | Single developer; one semester; high technical risk concentrated in five original algorithms; a coursework requirement for per-increment documentation |
| **Alternatives rejected** | Waterfall (change handling), V-model (same rigidity), Spiral (ceremony cost), RUP (artefact overhead), Reuse-oriented (Category C forbids bending requirements to components) |
| **Consequences, positive** | Risk retired continuously; working software from week two; two post-delivery defect classes found and fixed inside the process; retrospective learning compounded across increments |
| **Consequences, negative** | Less up-front documentation than a plan-driven process would have produced; process visibility depends on the burndowns and this report rather than on phase deliverables; the single-developer adaptation weakens the customer-collaboration principle |
| **Validated by** | Section 19.3, which revisits the decision against what actually happened |

## 4.6 Roles, Ceremonies and the Definition of Done

The role and ceremony adaptations are given in Tables 4.5 and 4.6. What remains to be stated is the **definition of done**, which was applied uniformly to every story in every iteration.

**Table 4.8 - Definition of done**

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

**Table 4.9 - The five iterations**

| Iteration | Title | Duration | Stories | Points | Principal deliverable |
|---|---|---|---|---|---|
| Increment 1 | Core Case & Evidence Management | 14 working days | 11 | 40 | A working repository with authentication, RBAC, CRUD, hashing and an append-only audit trail |
| Increment 2 | Integrity Algorithms & State Machine | 14 working days | 6 | 38 | Signed custody events, graph integrity verification, the lifecycle state machine, chain reconstruction |
| Increment 3 | Risk Scoring, AI Assistant & Hardening | 14 working days | 10 | 42 | Risk scoring, the AI assistant, anomaly detection, dashboards, security hardening, export and reporting |
| M1 | Access-Scoping Change Requests | Maintenance | 2 | 10 | Uniform case scoping across every aggregate; role-tailored dashboards; access-scoped assistant |
| M2 | Correctness & Security Hardening | Maintenance | 11 findings | - | Eleven correctness, security and robustness fixes found by structured review |

The sequencing placed the **riskiest work in the middle**: after the foundation had stabilised but before schedule pressure peaked. This is a deliberate application of the spiral model's risk-driven insight inside an incremental frame.

## 4.8 Estimation Method

Because the sprint backlogs and burndown charts are expressed in story points, it is worth setting out precisely how those numbers were arrived at, so that the figures quoted throughout the report are understood as the product of a method rather than as arbitrary values.

Estimation used **story points on a Fibonacci scale** - 1, 2, 3, 5, 8, 13 - rather than hours. The distinction matters. An hour estimate claims to predict how long something will take, which is a prediction developers are famously poor at making; a story point claims only that one piece of work is about twice the size of another, which is a judgement people make far more reliably. The Fibonacci sequence is used because its gaps widen as the numbers grow: it is possible to distinguish a 3 from a 5 with some confidence, but nobody can honestly distinguish a 7 from an 8, and the absence of those intermediate values prevents false precision. The widening gaps also encode a real property of estimation - that uncertainty grows with size, so large items deserve coarser buckets.

**Table 4.10 - Story-point scale and its application**

| Points | Meaning | Representative stories |
|---|---|---|
| 1 | Trivial; a single small piece that reuses existing patterns | US-11 admin-only account creation |
| 2 | Simple; essentially a library call plus its wiring | US-05 SHA-256 fingerprint, US-26 signed ZIP export, US-27 PDF report, US-16 and US-17 report interfaces |
| 3 | Small; a few parts, but no new design work | US-01 login, US-06 metadata extraction, US-10 formula checks, US-19 configurable weights, US-21 hallucination detection, US-23 dashboards |
| 5 | Moderate; multi-part and substantial, but well understood | US-02 role-based access control, US-03 case CRUD, US-04 evidence upload, US-08 custody logging, US-09 audit trail, US-12 digital signing, US-22 anomaly detection, US-24 two-factor authentication |
| 8 | Large; genuine design work, typically a new algorithm | US-14 state machine, US-15 chain reconstruction, US-18 risk scoring, US-20 AI orchestration |
| 13 | Very large; significant unknowns at the time of estimation | US-13 graph integrity verification |

Estimates were assigned **relatively**, anchored on a reference story rather than judged in isolation. US-05, the SHA-256 fingerprint - call a hashing function, store the result in a column, display it - served as the natural 2, and every other story was sized by asking whether it was about the same, roughly twice as large, or several times larger. This anchoring is what keeps a scale internally consistent when one person applies it across several months.

The resulting distribution is itself evidence that the method was applied honestly rather than retrofitted. Every story estimated at 8 is one of the five complex Category C algorithms; every story estimated at 2 is a thin wrapper over a third-party library; and the single 13 in the entire project went to the graph integrity verifier, the one item whose difficulty genuinely could not be predicted in advance. That last judgement proved correct in a way the estimate could not have anticipated: US-13 is precisely where Increment 2's three-day mid-sprint plateau occurred.

It is important to note that **story points and MoSCoW priority are independent dimensions**, even though they appear side by side in the same backlog tables. A point value answers *how large is this?*; a MoSCoW priority answers *what happens if time runs out?*. The two do not correlate, and deliberately so. US-11, admin-only account creation, is the smallest story in the project at 1 point yet is a Must, because a forensic system that permits self-registration is unacceptable regardless of how little code the restriction requires. Conversely US-22, the Isolation Forest anomaly detection, is a 5-point story but only a Could, because it represents real work whose absence would leave the system coherent. Keeping size and importance separate is what allows scope to be cut sensibly under pressure: one drops the least important work, not the largest.

The increment totals quoted throughout this report are **derived quantities rather than planning targets**: each is the arithmetic sum of the estimates of the stories allocated to that increment. Increment 1 totals forty points across eleven stories (3+5+5+5+2+3+3+5+5+3+1), Increment 2 thirty-eight points across six (5+13+8+8+2+2), and Increment 3 forty-two points across ten (8+3+8+3+5+3+5+3+2+2); maintenance iteration M1 contributes a further ten points (5+5), giving a project total of one hundred and thirty points. That the three increment totals fall within the narrow band of thirty-eight to forty-two is a consequence of **capacity rather than coincidence**. Each increment occupied a fixed cycle of fourteen working days undertaken by a single developer, so the volume of work admitted to an increment was bounded by the throughput observed in the preceding one. Increment 1 established that bound empirically by completing forty points within its cycle; forty points per increment therefore became the project's measured velocity, and the two subsequent increments were loaded against that measurement rather than against an assumed rate. This ordering - estimate the work, measure the capacity, then fit the plan to the measurement - is the relationship between estimation and planning prescribed by agile practice, in which velocity is treated as an observed property of the team rather than a target imposed upon it.

A methodological limitation must be acknowledged, noted in Section 4.5 and revisited in the velocity analysis of Section 19.2: a single-developer project places the estimator and the implementer in the same person, so estimates can be adjusted with perfect knowledge of the implementer's pace. The report therefore treats the *shape* of each burndown chart - where progress stalled and where it recovered - as more informative than the fact that each increment's total was met.

## 4.9 Summary

This chapter defined the four fundamental process activities - specification, development, validation and evolution - and showed that what distinguishes process models is not which activities they contain but when each is performed and how often. It contrasted the plan-driven and agile families, surveyed six process models with an explicit comparison against this project's needs, and set out the agile method vocabulary: the manifesto and its five principles, the practices of Extreme Programming, and Scrum's three phases, three roles and four ceremonies, each with the adaptation a single-developer project requires.

The selection of the Agile Incremental Model was then recorded as an architectural decision with four named factors, six rejected alternatives, and both positive and negative consequences. The definition of done was stated as six conditions applied uniformly to every story. Finally, the estimation method was explained in full: Fibonacci story points anchored on a reference story, the independence of size from MoSCoW priority, and the derivation of each increment's total from measured velocity rather than from a chosen target.

The next chapter applies all of this: it documents the three development increments and the two maintenance iterations that the process produced.

---

\newpage
