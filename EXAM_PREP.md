# Oral exam preparation - DEICMS

---

# PART 0 - If you go blank

Three sentences that always work, in this order:

1. **"Let me start from the problem."** - Every topic has a problem it solves.
   Stating the problem buys you ten seconds and usually unlocks the answer.
2. **"In my project, this appears as..."** - You know your project. Routing a
   theory question through DEICMS turns recall into description.
3. **"May I draw it?"** - Drawing is slower than speaking, which calms you, and
   he *wants* drawings. Ask, then draw while you think.

**Never say "I don't know" alone.** Say: *"I'm not certain of the formal
definition, but in my project it worked like this..."* Partial credit is real.

---

# PART 1 - The opening: explain your project (aim for 90 seconds)

Say it in this order. Do not rush to features.

> **The problem.** Digital evidence can be altered without leaving a visible
> trace. What makes it admissible in court is not the evidence itself but the
> record of who held it and what was done to it - the chain of custody. Break
> that chain and the evidence is worthless, however genuine it is.
>
> **The system.** DEICMS manages digital forensic evidence so that tampering
> is either impossible or evident, every action is attributable to a person,
> and the system's own history cannot be rewritten.
>
> **The shape of it.** Six entities, four roles plus case-level membership,
> about 4,700 lines of code, 216 automated tests.
>
> **The three categories.** Thirty data and repository functionalities;
> eleven third-party integrations; and five algorithms I designed and
> implemented myself - chain integrity verification, multi-factor risk
> assessment, custody chain reconstruction, an evidence lifecycle state
> machine, and the orchestration pipeline around the language model.
>
> **The process.** Scrum, six sprints. Three delivered the planned system.
> Three more came from defects found after acceptance.

**If he says "tell me more", go to the five guarantees:**

| | Guarantee |
|---|---|
| G1 | Content can be shown unchanged since intake, or shown precisely where it changed |
| G2 | A person sees only the investigations they are assigned to, in every view |
| G3 | The record of what happened is complete and cannot be amended |
| G4 | An exhibit moves only as its procedure permits |
| G5 | Exhibits can be ranked by attention needed, with the reasoning exposed |

---

# PART 2 - UML: how to remember all of them

## 2.1 The frame that holds everything

**UML 2.5 defines 14 diagram types: 7 structural and 7 behavioral.
I used 13 of the 14.**

Say that sentence and you have already answered half the question.

**Structural - "what the system is made of"** (7)

> **C**lass, **O**bject, **P**ackage, **C**omponent, **C**omposite structure,
> **D**eployment, **P**rofile
>
> *"**C**an **O**ur **P**roject **C**reate **C**lean **D**eployable
> **P**roducts"*

**Behavioral - "what the system does"** (7)

> **U**se case, **A**ctivity, **S**tate machine, **S**equence,
> **C**ommunication, **T**iming, **I**nteraction overview
>
> *"**U**sers **A**ct, **S**ystems **S**end **C**ommunication **T**hrough
> **I**nteractions"*

The only one I did not use is **Interaction Overview**. If asked why: *it
combines several interaction diagrams into one control flow, and with five
algorithms each already having its own activity and sequence diagram, it would
have added a level of indirection without adding information.*

## 2.2 The four interaction diagrams are one family

This is worth knowing because he may ask the difference:

| Diagram | Emphasis | Answers |
|---|---|---|
| **Sequence** | **Time** - vertical lifelines | In what order do the messages go? |
| **Communication** | **Structure** - objects linked, messages numbered | Which objects collaborate? |
| **Timing** | **Duration** - state against a time axis | How long is each state held? |
| **Interaction overview** | **Control flow** between interactions | Which interaction runs when? |

**Same information, different emphasis.** Sequence and communication are
formally interchangeable.

## 2.3 Drawing each one under pressure

For each: the question it answers, the skeleton to draw, and the mistake he
checks for.

---

### 1. Use Case Diagram

**Question:** Who can do what with the system?

**Draw in this order:**
1. A big rectangle = the system boundary. Write the system name on top.
2. Stick figures **outside** the box = actors.
3. Ovals **inside** = use cases.
4. Plain lines from actor to oval = associations.
5. Only then add «include» / «extend» / generalization.

**The three relationships - get these right:**

| | Arrow | Direction | Meaning |
|---|---|---|---|
| **«include»** | dashed, open arrow | **base → included** | Always happens. Mandatory sub-behavior |
| **«extend»** | dashed, open arrow | **extending → base** | Sometimes happens. Optional |
| **Generalization** | solid line, **hollow triangle** | **child → parent** (triangle touches parent) | Child is a kind of parent |

**The mistake he caught in my report:** generalization inverted. Remember:

> **The parent generalizes. The child specializes. The triangle points at the
> parent.**

In my project: **Read-Only Viewer is the most general actor.** Analyst
specializes it, Lead specializes Analyst, Administrator specializes Lead. So
the triangles all point *up* toward Read-Only Viewer.

**My numbers:** 41 use cases, one per route. Read-Only Viewer 20, Analyst 25,
Lead 32, Administrator 41. Each role inherits the one below.

**Second mistake to avoid:** do **not** make "Log in" an «include» of other
use cases. Authentication is a **precondition of the whole system**, not a
step repeated inside each use case.

---

### 2. Class Diagram

**Question:** What are the types, what do they know, what can they do, how do
they relate?

**Draw in this order:**
1. Boxes with **three compartments**: name / attributes / operations.
2. Visibility: `+` public, `-` private, `#` protected.
3. Lines between them.
4. **Multiplicity at both ends** - `1`, `0..*`, `1..*`.
5. Role names or a labelled arrow if it helps.

**The relationship symbols:**

| Symbol | Name | Meaning |
|---|---|---|
| plain line | Association | They know each other |
| **hollow** diamond | Aggregation | "has-a", parts survive the whole |
| **filled** diamond | Composition | "owns-a", parts die with the whole |
| **hollow triangle** | Generalization | Inheritance |
| dashed arrow | Dependency | Uses it, does not hold it |

**Diamond sits at the WHOLE end**, not the part.

**My project:** `Case ◆— EvidenceItem` is composition - delete the case and
its evidence has no meaning. `EvidenceItem ◆— CustodyLog` likewise.
`Investigator —— CaseAccess —— Case` is an association resolved through an
associative class.

**My three «engine» classes** - GraphIntegrityEngine, EvidenceRiskScorer,
EvidenceStateMachine - plus **«service» CryptoService** hold behavior and
store nothing.

---

### 3. Class diagram vs ER diagram - he WILL ask this

**Answer in one sentence first:**

> *A class diagram models the software; an ER diagram models the data.*

**Then give three differences:**

| | Class diagram | ER diagram |
|---|---|---|
| **Operations** | Yes - behavior belongs with data | None - data only |
| **Inheritance** | First-class relationship | Cannot be expressed; must be simulated |
| **Visibility / encapsulation** | Public, private, protected | Meaningless |

**Then the killer line, which is specific to my project:**

> *In my design model there are four classes - three engines and a crypto
> service - that hold all the behavior and persist nothing. They are completely
> absent from the data model. That absence is the clearest single difference
> between the two.*

**Why I used a class diagram with «table» stereotypes instead of an ER
diagram:** the requirement was UML only, and UML's own extension mechanism is
the stereotype, so the schema can be modelled without importing a second
notation.

---

### 4. Object Diagram

**Question:** What does one concrete instant look like?

**Draw:** boxes labelled `name : Class`, **underlined**, with attribute
*values* (not types). Links between them, no multiplicity.

**One line to say:** *A class diagram states a constraint; an object diagram
shows one case of it.* Mine shows evidence EV-2026-007 where the stored hash
differs from the registered hash **and** a timestamp is out of order - the two
violations that flagged it.

---

### 5. Package Diagram

**Question:** How is the code organized, and what may depend on what?

**Draw:** folder-shaped rectangles, dashed arrows labelled «use».

**My five layers, dependencies downward only:**

```
Presentation (templates)
      ↓
Interface (routes)
      ↓
Application logic (the five algorithms)
      ↓
Domain and persistence (models)
      ↓
Framework and libraries
```

**The point to make:** logic must **not** depend on routes. In my project this
is not a convention - a static test asserts that no logic module imports
`request`, `session`, `render_template` and so on.

---

### 6. Component Diagram

**Question:** What are the replaceable units, and what interfaces do they
offer and need?

**Draw:** rectangles with the component icon. Then:
- **Lollipop** (circle on a stick) = **provided** interface
- **Socket** (half-cup) = **required** interface
- Ball fits into socket = assembly connector

**My point:** every component that reads case-scoped data requires the same
`IAccess` interface, provided by one component. That abstraction is what was
missing when the scoping defect occurred.

---

### 7. Composite Structure Diagram

**Question:** What is *inside* one component?

**Draw:** a big box = the classifier. Inside it, smaller boxes = parts.
Small squares on the boundary = ports. Lines between parts = connectors.

**Mine:** opens the GraphIntegrityEngine - DAG builder, walker, three checks,
failure collector, completeness scorer. **The argument is about an absent
connector:** nothing routes a failure back to the walker, which is structurally
why one failure does not stop the traversal.

---

### 8. Deployment Diagram

**Question:** What runs where?

**Draw:** **3-D boxes** = nodes (hardware or execution environment).
Rectangles inside = artifacts (the actual files deployed).
Lines = communication paths, labelled with the protocol.

**Mine:** workstation (browser) → application host (Python runtime: run.py,
the app, logic modules; file system: deicms.db, encrypted uploads) → cloud
(hosted language model). The model is the **only** thing outside the trust
boundary.

---

### 9. Sequence Diagram

**Question:** In what order do objects exchange messages?

**Draw in this order:**
1. Boxes across the top = participants.
2. **Dashed vertical lines** down = lifelines.
3. **Thin rectangles** on the lifelines = activation bars.
4. Messages left to right, **time flows downward**.

**Arrow types:**

| Arrow | Meaning |
|---|---|
| solid line, **filled** head | synchronous call (caller waits) |
| solid line, open head | asynchronous |
| **dashed** line, open head | return |

**Combined fragments** - a box with a keyword in the corner:
`loop`, `alt` (alternative), `opt` (optional), `par` (parallel), `ref`.

**Mine:** the integrity verification sequence has a `loop` over every node and
an `alt` inside it for the failure case. The assistant sequence has an `alt`
for "model answers" versus "model unavailable".

---

### 10. Communication Diagram

**Question:** Which objects collaborate? (Same content, structural emphasis.)

**Draw:** object boxes anywhere, lines between them, messages written along
the lines **with sequence numbers** - `1:`, `2:`, `3:`.

**The numbers carry the ordering**, because there is no time axis.

**One line:** *Sequence and communication diagrams are formally equivalent. I
used communication for the risk scorer because the point there is which
objects participate, not when.*

---

### 11. Activity Diagram

**Question:** What is the flow of work, including decisions and parallelism?

**Draw in this order:**
1. **Filled circle** = start.
2. Rounded rectangles = actions.
3. **Diamond** = decision. **Every outgoing edge needs a guard in
   `[square brackets]`.**
4. **Thick bar** = fork (split into parallel) and join (wait for all).
5. **Filled circle with a ring** = end.
6. Vertical or horizontal lanes = **partitions** (swimlanes) = who does it.

**Mistake he checks:** a decision diamond with unlabelled branches.

**Mine:** the risk scoring activity forks into eight parallel indicator
extractions, joins, then normalizes, sums, applies interaction rules, caps the
bonus, classifies. The registration activity uses **partitions** across
Investigator / Interface / Validation / Logic / Persistence / Audit.

---

### 12. State Machine Diagram

**Question:** What states can one object be in, and what moves it between
them?

**Draw:**
1. **Filled circle** = initial.
2. Rounded rectangles = states.
3. Arrows = transitions, labelled **`event [guard] / action`**.
4. **Circle with a ring** = final.

**My evidence lifecycle - memorize this, it is the most likely drawing
request:**

**Six states:** Collected → Submitted → Under Analysis → Transferred →
Archived, plus **Flagged**.

**Fourteen transitions.** The ones to remember:
- Collected → Submitted, Collected → Transferred
- Submitted → Under Analysis, Submitted → Transferred, Submitted → Archived
- Under Analysis → Transferred, Under Analysis → Archived
- Transferred → Under Analysis
- **Any of the five → Flagged** (that is 5 transitions)
- **Flagged → Under Analysis** (administrator only, after re-verification)

5 + 1 + 2 + 3 + 2 + 1 = 14.

**The line that shows you understand it:**

> *Flagged is reachable from every state but escapable from only one, by an
> administrator alone, and only after re-verification. An exhibit whose
> integrity has failed cannot quietly resume normal handling.*

**And:** the lifecycle is declared as a **table in data**, not as branching
code - so the policy is auditable in one place and adding a transition is a
data change.

---

### 13. Timing Diagram

**Question:** How long does each state last?

**Draw:** participants stacked down the left, their states on the vertical
axis, **time along the horizontal axis**, a stepped line showing state over
time.

**Mine:** the assistant's bounded waiting - 20 seconds per model call, 60
seconds total budget, kept below the browser's abort so a slow service gives a
clear message instead of a cancelled request.

---

### 14. Profile Diagram

**Question:** How is UML itself extended?

**Draw:** the metaclass (e.g. `Class`) and your «stereotype» boxes with
`«extend»` arrows to it.

**One line:** *Stereotypes are UML's own extension mechanism. I declared
«table», «PK», «FK», «engine», «service» and «external» so that the relational
schema could be modelled in UML rather than in a second notation.*

---

# PART 3 - Software Engineering concepts

## 3.1 SDLC vs SDP - do not confuse these

| | |
|---|---|
| **SDLC** (Software Development **Life Cycle**) | The **phases** every project passes through: requirements → design → implementation → testing → deployment → maintenance. *What* must happen. |
| **SDP** (Software Development **Process**) | The **model** that organizes those phases: waterfall, V-model, incremental, spiral, Scrum. *How* and *in what order*. |

**One line:** *The life cycle is the set of activities; the process is the
strategy for arranging them.*

## 3.2 Waterfall

**Sequential. Each phase completes and is signed off before the next begins.**

Requirements → Design → Implementation → Testing → Deployment → Maintenance.

| Strength | Weakness |
|---|---|
| Simple, highly visible, strong documentation | Requirements must be frozen early |
| Good when requirements are genuinely stable | Change is expensive; working software arrives late |
| Suits safety-critical and contractual work | Errors in early phases surface last |

**Why I rejected it:** my technical risk sat in five algorithms whose design
could not be settled on paper. And it was proved right - the integrity
verifier's traversal semantics changed under implementation, from stopping at
the first failure to accumulating all of them. Waterfall would have frozen the
wrong design in the specification phase.

## 3.3 V-model ("2V")

**Waterfall bent into a V. The left arm descends through specification; the
right arm ascends through testing. Each level on the left pairs with its test
level on the right.**

```
Requirements  ─────────────────────  Acceptance testing
  Architecture  ─────────────────  System testing
    Module design  ───────────  Integration testing
      Implementation (bottom of the V)   Unit testing
```

**The key idea: each test level is planned when its matching specification is
written, not afterwards.**

| Strength | Weakness |
|---|---|
| Testing is planned early | Still sequential - inherits waterfall's rigidity |
| Every deliverable has a matching verification | Poor fit for volatile requirements |

**My position - this is a strong answer:**

> *I rejected the V-model as a **life cycle** but adopted it as a **test
> strategy**. In my report each construction phase is paired with a test
> level: system requirements with acceptance tests, architecture with
> architectural boundary tests, module design with unit tests, implementation
> with integration tests, and quality requirements with measurement tests.*

## 3.4 Plan-driven vs Agile

| | Plan-driven | Agile |
|---|---|---|
| Planning | All up front | Incremental, each iteration |
| Requirements | Frozen early | Expected to change |
| Documentation | Heavy, formal | Working software preferred |
| Customer | At start and end | Continuous |
| Change | Controlled, costly | Welcomed |
| Delivery | One release at the end | Working increment each iteration |
| Suits | Stable, safety-critical, contractual | Volatile, exploratory |

**They are not opposites - most real projects are hybrid.** Mine is:
requirements and the data model were specified up front in plan-driven style;
the algorithms were left to the sprint that built them.

**The line to use:** *Scrum does not forbid up-front analysis. It forbids
committing the whole design up front.*

## 3.5 Agile - the four values

From the Agile Manifesto (2001). **Items on the left are valued more, but
those on the right still have value.**

1. **Individuals and interactions** over processes and tools
2. **Working software** over comprehensive documentation
3. **Customer collaboration** over contract negotiation
4. **Responding to change** over following a plan

There are also 12 principles; the ones most likely asked: deliver working
software frequently, welcome changing requirements, simplicity, and the team
reflects regularly and adjusts.

**Honest caveat about my project:** value 3 is the weakest. I had no customer.
Requirements came from domain sources and reasoning, and were never contested
by a stakeholder. I state that as a limitation of validation.

## 3.6 Scrum

**Scrum is a framework, not a methodology. It is agile and incremental.**

**3 roles** (the 2020 Guide calls them accountabilities):

| Role | Owns |
|---|---|
| **Product Owner** | The product backlog, its ordering, and value |
| **Scrum Master** | The process; removes impediments |
| **Developers** | Building the increment |

**3 artifacts**, each with a commitment:

| Artifact | Commitment |
|---|---|
| **Product Backlog** | Product Goal |
| **Sprint Backlog** | Sprint Goal |
| **Increment** | Definition of Done |

**5 events:**

1. **The Sprint** itself - a container for the other four
2. **Sprint Planning** - what and how
3. **Daily Scrum** - 15 minutes, re-plan the day
4. **Sprint Review** - inspect the increment with stakeholders
5. **Sprint Retrospective** - inspect the *process*, decide improvements

**Careful:** **Backlog Refinement is an ongoing activity, NOT an event.** If
he asks how many events, say **five**.

**Also careful:** "Sprint 0" and "Definition of Ready" are **common industry
practice, not in the Scrum Guide.** Only Definition of **Done** is official. I
used both; if challenged, say they are team conventions this project adopted.

**How I adapted Scrum as one developer:**

| | |
|---|---|
| Product Owner | Me, ordering by stakeholder concerns and domain requirements rather than preference |
| Scrum Master | Me, treating retrospective actions as binding |
| Developers | Me |
| **Daily Scrum** | **Abandoned honestly** - a stand-up with yourself coordinates nothing. Replaced by a daily written note feeding the burndown, which serves tracking but not coordination |

**Say that abandonment out loud.** It shows you know what the event is *for*.

## 3.7 Sprint

**A fixed-length iteration, one month or less, producing a working increment.**

Properties worth stating:
- **Fixed length** - a sprint is never extended; scope flexes instead
- **Sprint Goal** - the single objective, which gives coherence
- **No scope changes** that endanger the goal
- A new sprint starts immediately after the previous one ends

**My six sprints:**

| Sprint | Name | Points | Why it existed |
|---|---|---|---|
| 1 | Foundation | 40 | Cases, evidence, custody, audit |
| 2 | Integrity | 38 | Three complex algorithms |
| 3 | Assessment | 42 | Risk scoring, assistant, reporting |
| 4 (M1) | Access scoping | 10 | **Adversarial testing** found aggregates unscoped |
| 5 (M2) | Defect repair | 11 findings | **Structured code reading** found 11 issues |
| 6 (M3) | Quality enforcement | 23 | **An audit** found NFRs untested |

**The sentence that lands well:**

> *Sprints 4, 5 and 6 each exist because a defect was found after acceptance,
> each by a different means. In no case did a sprint find its own defects -
> which is exactly the condition that makes successive increments worth their
> cost.*

**Burndown chart:** story points remaining against days, with an ideal
straight line. **The shape matters more than the total** - a plateau means
rework. My Sprint 2 has a plateau at days 5-7, which is the traversal rework.

**Velocity:** points delivered per sprint. **Observed, not a target.** My
caveat: with one person, estimator and implementer are the same, so estimates
unconsciously track the implementer's pace. I rated that as an accepted risk.

## 3.8 Functional vs Non-Functional Requirements

| | Functional | Non-functional |
|---|---|---|
| Describes | **What** the system does | **How well** it does it |
| Form | A service, behavior, or reaction | A constraint or quality property |
| Example (mine) | "Record every handover with parties, moment, place and reason" | "No listing shall render in time proportional to the whole collection" |
| Failure | A missing capability | A capability that is unusable, unsafe or too slow |

**Types of NFR:** performance, security, usability, reliability,
maintainability, portability, availability.

**The second distinction - user vs system requirements:**

| | User requirement | System requirement |
|---|---|---|
| Reader | The customer | The developer and tester |
| Language | The customer's vocabulary | Precise, bounded, countable |
| Testable directly? | No - too abstract | **Yes** |

**My numbers:** 22 user requirements, 61 system functional requirements,
9 user quality requirements, 21 system quality requirements, 7 domain
requirements.

**The strongest thing I can say about NFRs:**

> *Every one of my 21 system quality requirements carries three things: how it
> is measured, what value counts as a pass, and the name of the automated test
> that applies it. Before this revision, nine of eighteen were verified only by
> "code review" or "manual check" - and a verification method that does not
> re-run cannot fail, so the requirement could not fail either.*

**Requirements must state problems, not solutions.** "Compute a SHA-256
fingerprint" is a design decision. The requirement is: *"the system shall be
able to determine, at any later time, whether the stored content differs from
the content registered at intake."* The mechanism belongs in the design
chapter.

## 3.9 Testing

**The levels - bottom to top:**

| Level | Scope | Who |
|---|---|---|
| **Unit** | One module in isolation | Developer |
| **Integration** | Modules working together | Developer |
| **System** | The whole system against its requirements | Test team |
| **Acceptance** | Against user needs | Customer |

**Regression testing** cuts across all of them: re-running tests after a
change to confirm nothing previously working has broken.

**Verification vs Validation - he may ask:**

| | |
|---|---|
| **Verification** | *Are we building the product **right**?* Against the specification. |
| **Validation** | *Are we building the **right** product?* Against the user's actual need. |

**My honest position:** verification is strong - 216 tests, every requirement
traced to one. **Validation is weak**, because there was no customer. The
system can be shown to satisfy its requirements; the requirements cannot be
shown to be the right ones.

**Black box vs white box:**
- **Black box** - from the specification, without seeing the code
- **White box** - from the code structure, aiming at paths and branches

**My testing facts:**
- 216 tests, 78% statement coverage overall, **80% across the five algorithms**
- Weakest module: chain reconstruction at **65%** - the plausibility function
  has four criteria each present or absent, giving sixteen combinations
- The suite runs **with no network access**, which is why the language model
  pipeline is testable at all
- **Adversarial testing** - asking what an *unentitled* user receives, not
  just whether an entitled one succeeds. This found the scoping defect

**The best single line about testing:**

> *A green test suite can coexist with critical defects. Ninety-three tests
> passed in Sprint 3 and not one asked what an unentitled user receives - so
> the system had a scoping defect in every aggregate it had just built.*

---

# PART 4 - The five algorithms (he will ask why they are complex)

**The test I applied:** not *"does it call a library?"* but *"if the library
were replaced by an equivalent, would anything I designed have to change?"*

| # | Algorithm | What makes it complex | One memorable fact |
|---|---|---|---|
| 1 | **Chain integrity verification** | Builds a DAG of custody events, depth-first traversal, three checks per node, **accumulates all failures in one pass** | Children are pushed whether or not the node passed |
| 2 | **Multi-factor risk assessment** | Eight indicators, each normalized by a curve suited to its own distribution, weighted sum, five interaction rules, **bonus capped at 0.30** | Without the cap, everything alarming scores the same and the ranking collapses |
| 3 | **Custody chain reconstruction** | Heuristic best-first search; four plausibility criteria; **declines below 0.40** | Declining to guess is a result, not a failure |
| 4 | **Lifecycle state machine** | Six states, fourteen transitions, declared **as data**, four validation gates | A refusal names the exact unmet condition and is itself audited |
| 5 | **Assistant orchestration** | Six stages around the model: intent, **scoping**, retrieval, prompt, call with fallback, reference validation | Scoping happens *before* retrieval, so inaccessible data never enters the prompt |

**The control case - say this, it proves the categorization is honest:**

> *Anomaly detection with an Isolation Forest feeds the same dashboard as my
> risk scorer, and I could have claimed it as a sixth complex feature. I
> classified it as third-party, because there the library **is** the algorithm
> and I supply only the feature vector.*

**On the language model:** *the model is a third-party service. The six-stage
pipeline around it is mine. I can prove the boundary is real: the model I
originally planned became unavailable, I substituted a different one, and no
stage, no requirement and no test changed.*

---

# PART 5 - Likely questions, short answers

**"Why Scrum and not waterfall?"**
> Technical risk sat in five algorithms whose design could not be settled on
> paper. Scrum commits one sprint at a time. It was proved right: the integrity
> verifier's traversal semantics changed under implementation on day five of
> Sprint 2. Waterfall would have frozen the wrong design and found the mismatch
> during acceptance testing.

**"Your proposal said incremental, your report says Scrum."**
> Scrum **is** an agile incremental framework. The proposal named the family;
> the report names the member and implements its artifacts - a prioritized
> product backlog, refinement between sprints, sprint backlogs decomposed into
> tasks.

**"How is this an increment and not a version?"**
> An increment is working, usable software that adds to what exists. Each of my
> sprints ended with the system running, not with a document.

**"What is the difference between a class diagram and an ER diagram?"**
> A class diagram models the software, an ER diagram models the data. Three
> differences: operations, inheritance, and visibility. And in my project, four
> classes hold all the behavior and persist nothing - they are completely
> absent from the data model.

**"Draw the use case diagram."**
> Box, actors outside, ovals inside, plain associations first. Then say: *the
> Read-Only Viewer is the most general actor; each other role specializes it,
> so the triangles point toward Read-Only Viewer.*

**"What is a burndown chart for?"**
> Remaining work against time, with an ideal line. Its value is the **shape** -
> a plateau shows where rework happened. My Sprint 2 plateaus at days five to
> seven, which is exactly the traversal rework.

**"How many Scrum events are there?"**
> Five: the Sprint, Sprint Planning, Daily Scrum, Sprint Review, Sprint
> Retrospective. Backlog refinement is an ongoing activity, not an event.

**"What would you do differently?"**
> Adversarial authorization testing from Sprint 1 instead of Sprint 4. Every
> test I wrote in the first three sprints asked whether an entitled user
> succeeds; none asked what an unentitled user receives. That single omission
> caused two of my six sprints.

**"Is your project balanced across the three categories?"**
> By count, Category A dominates - thirty functionalities - as it will in any
> system with a real data model. By effort it is balanced differently: the five
> complex algorithms are 43% of estimated story points and 42% of the source.
> The whole third-party category is 439 lines, less than any two algorithm
> modules combined.

---

# PART 6 - The morning of

**Read only this page.**

- **14 UML diagrams: 7 structural, 7 behavioral. I used 13.**
- **Triangle points at the parent.** Read-Only Viewer is the most general.
- **«include» = always, base→included. «extend» = sometimes,
  extending→base.**
- **Filled diamond = composition, dies with the whole. Hollow = aggregation.**
- **Six states, fourteen transitions. Flagged: in from everywhere, out from
  one.**
- **SDLC = phases. SDP = the model that arranges them.**
- **Scrum: 3 roles, 3 artifacts, 5 events.** Refinement is not an event.
- **V-model: rejected as a life cycle, adopted as a test strategy.**
- **FR = what it does. NFR = how well. User req = customer's words. System
  req = testable.**
- **Verification = built it right. Validation = built the right thing.**
- **216 tests, 78% overall, 80% on the algorithms, 65% weakest.**
- **Five algorithms. Isolation Forest is NOT one of them - that is the point.**

**If you freeze:** *"Let me start from the problem."* Then: *"In my project,
this appears as..."* Then: *"May I draw it?"*
