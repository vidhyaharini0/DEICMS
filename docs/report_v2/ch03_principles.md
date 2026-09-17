# Chapter 3 — Software Engineering Principles

---

## 3.1 Principles, Methods, Techniques, Methodologies and Tools

Software qualities define the properties a software product or process *should* have. Principles are what an engineer applies in order to obtain them. Principles are fundamental, primary or general laws or truths from which others are derived; they apply to both process and product, and they are general enough that they cannot be applied directly. They become practice through methods and techniques, which are in turn packaged into methodologies and supported by tools.

**Table 3.1 — The layers from principle to tool**

| Layer | Definition | DEICMS example |
|---|---|---|
| **Principle** | A fundamental law or truth from which others are derived; applies to process and product | Modularity |
| **Method** | A general guideline governing the execution of an activity; rigorous, systematic and disciplined | Decomposing the system into blueprints, each owning one area of functionality |
| **Technique** | More technical and mechanical than a method, often with more restricted applicability | Flask's application-factory pattern with blueprint registration |
| **Methodology** | A packaging of preselected methods and techniques promoting one approach to a problem | The Agile Incremental process adopted in Chapter 4 |
| **Tool** | Software developed to support the application of techniques, methods and methodologies | Git, pytest, pytest-cov, PlantUML |

The relationship is hierarchical: principles are the broadest and most durable, tools the narrowest and most disposable. A project that adopts tools without understanding the principles beneath them acquires the mechanics of good engineering without its judgement — which is why this chapter precedes the chapters on process, design and implementation rather than following them.

## 3.2 The Seven Principles

Seven principles may be applied in all phases of software development. Modularity is the cornerstone principle supporting software design; the others either enable it or build upon it.

**Table 3.2 — The seven principles at a glance**

| # | Principle | One-line statement | Primary DEICMS manifestation |
|---|---|---|---|
| P1 | **Rigour and formality** | Creativity practised systematically; formality is rigour at its highest degree | Ed25519 signature payload defined as an exact canonical byte sequence |
| P2 | **Separation of concerns** | Divide and conquer: separate issues to concentrate on one at a time | Four-layer architecture; routes never contain business logic |
| P3 | **Modularity** | Decompose a complex system into simpler pieces with well-defined interfaces | Ten blueprints, six model modules, twelve logic modules |
| P4 | **Abstraction** | Identify the important aspects of a phenomenon and ignore its details | The custody history modelled as a directed graph |
| P5 | **Anticipation of change** | Support evolution by anticipating potential future changes | Admin-configurable risk weights; ORM for database portability |
| P6 | **Generality** | Look for the general problem behind the specific one, balancing against cost | The factor–normalise–weight–amplify structure of the risk engine |
| P7 | **Incrementality** | Proceed stepwise, delivering early partial functionality and obtaining feedback | Three increments plus two maintenance iterations |

## 3.3 Rigour and Formality

Software engineering is a creative design activity, but it must be practised **systematically**. Rigour is the necessary complement to creativity: it increases confidence in what has been developed. **Formality** is rigour at its highest degree, in which the process is driven and evaluated by mathematical laws.

The principle applies to both process and product. On the **process** side, rigorous documentation of development steps supports project management and the assessment of timeliness — the burndown chart being the canonical example. On the **product** side it appears as mathematical analysis of program correctness and as systematic, rather than ad-hoc, derivation of test data.

DEICMS applies rigour at several degrees, and it is worth being precise about which is which, since claiming formality where only rigour exists would itself be a failure of rigour.

**Table 3.3 — Degrees of rigour applied in DEICMS**

| Artefact | Degree | What makes it so |
|---|---|---|
| Digital signature payload | **Formal** | The signed byte sequence is defined by an exact, canonical concatenation, reproduced identically in three separate modules; any deviation produces a verification failure, which is a mathematical rather than a conventional guarantee |
| Evidence lifecycle | **Formal** | Expressed as a state machine — a mathematical object with a defined state set, alphabet and transition function — so that reachability and the absence of illegal transitions are decidable |
| Risk-score normalisation | **Rigorous** | Every factor is normalised to the closed interval [0, 1] and the weights are re-normalised to sum to exactly 1.0, so the composite score is provably bounded; the choice of curve per factor is engineering judgement, not proof |
| Test data derivation | **Rigorous** | Test cases are derived systematically from acceptance criteria and from boundary values of each algorithm's input domain, not by choosing convenient examples |
| Burndown tracking | **Rigorous** | Remaining points recorded daily against an ideal line, giving an auditable record of process timeliness |
| User interface behaviour | Neither | Assessed by demonstration and inspection; no formal specification exists, and none was warranted |

## 3.4 Separation of Concerns

To dominate complexity, separate the issues so that one can be concentrated on at a time — *divide et impera*. The principle supports the parallelisation of effort and the separation of responsibilities. A *concern* is a set of information that affects the code of a program; it is not absolute but relative to the problem being considered, and its generalisation is the notion of a *concept*.

The principle applies to process and product alike. Applied to the **process**, going through phases one after another — as in the waterfall model — separates activities with respect to time. Applied to the **product**, it keeps requirements separate from one another: functionality, performance, user interface and usability are treated independently.

In DEICMS, separation of concerns operates along three distinct axes simultaneously.

**Separation by layer.** The system is divided into presentation (Jinja templates), routing and request handling (blueprints), business logic (the `logic/` package) and persistence (the `models/` package). The rule enforced throughout is that a route handler validates input, calls into logic, and renders a result — it never contains an algorithm. This is what made the M2 risk-scoring defect a single-file fix.

**Separation by feature.** Each blueprint owns one area of functionality: authentication, cases, evidence, custody, audit, integrity, risk, assistant, reports, administration. A developer working on custody transfer need not read the risk-scoring code at all.

**Separation by cross-cutting concern.** Some concerns cut across every feature and cannot be localised by layer or by feature — authorisation, audit logging, local-time handling. Each of these is implemented once, in one module, and applied uniformly: authorisation through decorators, auditing through a single recording function, time through a single source of truth. The alternative — repeating the concern at every site — is what produced the M1 defect, where case scoping had been applied at the record level but not in the aggregate queries that fed dashboards.

**Separation in the process.** The single developer consciously separated the roles of product owner, developer and tester rather than blurring them (Section 4.6). The access-scoping defects of M1 were found precisely because the person wearing the tester's hat deliberately attempted to reach another case's data rather than assuming the developer had prevented it.

## 3.5 Modularity, Cohesion and Coupling

A complex system may be divided into simpler pieces called **modules**; a system composed of modules is **modular**. Modularity supports the application of separation of concerns, because when dealing with one module the details of the others can be ignored. Modularity — and hence separation of concerns — is achieved by **encapsulating information inside a section of code that has a well-defined interface**.

Modularity is assessed by two complementary measures.

**Cohesion** (internal, or intra-module coupling) is the degree to which the elements of a module belong together — it measures the strength of the relationship between pieces of functionality within a module. Each module should be **highly cohesive**, so that it is understandable as a meaningful unit. High cohesion is associated with robustness, reliability, reusability, understandability and maintainability.

**Coupling** (external, or inter-module coupling) is the degree of interaction between modules. Modules should exhibit **low coupling**, so that each can be understood separately.

The design goal is therefore *high cohesion, low coupling*. Table 3.4 assesses the principal DEICMS modules against it.

**Table 3.4 — Cohesion and coupling assessment of the principal modules**

| Module | Responsibility | Cohesion | Coupling | Assessment |
|---|---|---|---|---|
| `logic/graph_integrity.py` | Verify a custody chain | High — every function serves one algorithm | Low — depends only on the models and `hashlib` | Exemplary; testable in isolation |
| `logic/risk_scoring.py` | Compute a multi-factor risk score | High — factor extraction, normalisation, weighting, classification | Low — reads models, writes nothing | Exemplary |
| `logic/state_machine.py` | Govern lifecycle transitions | High — the transition table and its guards | Low — no knowledge of routes or templates | Exemplary |
| `logic/ai_assistant.py` | Orchestrate the six-stage pipeline | Medium-high — six stages, cohesive as a pipeline but large | Medium — touches several model classes to build context | Acceptable; the retrieval stage is the natural split point if it grows |
| `models/case_access.py` | Determine accessible cases | High — one question, answered one way | Low | Exemplary; the single point that fixed M1 |
| `utils/audit.py` | Record audit events | High | Low — called from everywhere but depends on nothing | Exemplary cross-cutting module |
| `routes/*.py` | Request handling | High per blueprint | Medium — necessarily depends on logic and models | Appropriate for a routing layer |

The one module flagged as merely acceptable is flagged deliberately. `ai_assistant.py` combines intent classification, context retrieval, prompt construction, model invocation, validation and hallucination detection. These are cohesive *as a pipeline*, but the module is the largest in the system, and the honest assessment is that its retrieval stage — which touches the most model classes and therefore carries the most coupling — would be the first thing to extract if the module grew further. Recording this is more useful than claiming uniform excellence.

## 3.6 Abstraction

**Abstraction** means identifying the important aspects of a phenomenon and ignoring its details. It is a special case of separation of concerns, and the type of abstraction to apply depends on the purpose: the buttons of a watch abstract from its internals for the purpose of setting the time, but a different abstraction is needed to support repair.

Abstraction **yields models**. When requirements are analysed, the product is a model of the proposed application — formal or semi-formal — and it then becomes possible to reason about the system by reasoning about the model instead. This is the justification for the entire modelling activity of Chapter 8, and the reason the report contains eight UML diagrams rather than only source code.

Abstraction also applies to the **process**: cost estimation takes only key factors into account, applying similarity with previous systems and ignoring detailed differences — which is precisely what story-point estimation does (Section 4.8).

**Table 3.5 — Principal abstractions in DEICMS and what each deliberately ignores**

| Abstraction | Retains | Ignores | Purpose served |
|---|---|---|---|
| Custody history as a **directed acyclic graph** | Ordering, custodian continuity, hash continuity at each edge | File content, case metadata, user interface state | Makes integrity verification a traversal problem with known complexity |
| Evidence lifecycle as a **finite state machine** | The six legal states and the permitted transitions between them | Everything about the item except its current state | Makes illegal transitions decidable rather than a matter of vigilance |
| Risk as a **vector of eight normalised factors** | The magnitude of each independent signal on a common scale | The natural units and distributions of the raw measurements | Makes heterogeneous signals combinable by weighted sum |
| Evidence handling as **four roles** | The distinctions in responsibility that matter for authorisation | Every other difference between individual investigators | Makes authorisation a table lookup |
| Persistence as an **object-relational mapping** | Entities, relationships and constraints | The dialect of the underlying database engine | Makes the system database-portable |

## 3.7 Anticipation of Change

The ability to support software evolution requires **anticipating potential future changes**. It is the basis of evolvability, and its canonical practical expression is establishing a configuration management environment for the project.

Anticipation of change is a principle that can be over-applied: anticipating every conceivable change produces speculative generality that costs more than it saves. The discipline is to anticipate the changes that are *likely*. Table 3.6 records the changes DEICMS anticipated, the mechanism provided, and — importantly — whether the anticipation proved correct.

**Table 3.6 — Anticipated changes and outcomes**

| Anticipated change | Mechanism provided | Did it occur? |
|---|---|---|
| Risk weights will need tuning per organisation | Admin-configurable weights and thresholds, re-normalised on save (US-19) | Not yet, but the mechanism cost little |
| The database engine will change for production | SQLAlchemy ORM; no engine-specific SQL in application logic | Not yet; the path is open |
| The language model provider or model will change | Model invoked behind a single method; model name is configuration | **Yes** — the selected model was retired by the provider and returned HTTP 410; an ordered fallback list absorbed the change (Section 5.5) |
| The language model may be unavailable entirely | Context-aware mock fallback when no key is configured or all candidates fail | **Yes** — used throughout testing, and during the outage above |
| New evidence categories will be needed | Category stored as a value rather than encoded in class structure | Not yet |
| The code will need to change after delivery | Git configuration management from the first commit; 172 automated tests as a regression net | **Yes** — twice, in M1 and M2 |

The two rows marked *yes* are the ones that justify the principle. The provider's retirement of the model was not foreseeable in detail, but the *category* of change — an external dependency moving beneath us — was, and designing for that category was sufficient.

## 3.8 Generality

While solving a problem, try to discover whether it is an instance of a more general problem whose solution can be reused in other cases. Generality must be **carefully balanced against performance and cost** — though sometimes a general problem is actually easier to solve than a special case.

DEICMS applied this principle selectively, and the selectivity is the point.

**Where generality was adopted.** The risk-scoring engine is structured as a general pipeline — extract factors, normalise each to [0, 1], apply weights, amplify by interaction rules, classify against thresholds — into which the eight domain-specific factors are plugged. Adding a ninth factor requires adding an extractor, a normaliser and a weight, not rewriting the algorithm. The integrity verifier was generalised in a different direction: it was written to traverse *a* custody graph, so it serves both the stored chain and the reconstructed chain without modification. The authorisation decorators are general over role sets rather than being written once per route.

**Where generality was deliberately declined.** The state machine's transition table is hard-coded to the six evidence states rather than being data-driven. A configurable state machine would be more general, but forensic lifecycle states are fixed by procedure, not by customer preference, and making them configurable would add a class of misconfiguration risk — an organisation could define a lifecycle that permits archiving unverified evidence — in exchange for flexibility no stakeholder asked for. This is the balance against cost that the principle requires: generality is not free, and here its cost is paid in safety.

## 3.9 Incrementality

Incrementality means proceeding in a stepwise fashion, in increments. Its practical content is to identify early subsets of the system, deliver partial functionality early, and obtain feedback on it — so that both the product and the understanding of the requirements grow together rather than the product being constructed against a fixed understanding formed at the start.

This principle is the direct justification of the process model selected in Chapter 4, and the whole of Chapter 5 is its application. Its effect in DEICMS is visible in the dependency structure: Increment 1 delivered the data model and CRUD, which gave Increment 2's algorithms a concrete schema and real records to operate on; Increment 2 delivered verified integrity primitives, which Increment 3's risk scorer and AI assistant consume. Each increment was a working, demonstrable system, so technical risk was retired continuously rather than accumulating until a single late integration.

Incrementality also delivered the feedback the principle promises. The per-increment retrospectives produced concrete process changes — most consequentially the adoption of test-first development for complex algorithms from Increment 3 onward, which arose from the Increment 2 retrospective and measurably reduced defect-fixing time.

## 3.10 Principle-to-Artefact Mapping

Table 3.7 consolidates the chapter by mapping each principle to the specific artefacts in the delivered system that embody it, so that the claims made above can be checked against the code rather than taken on trust.

**Table 3.7 — Principles mapped to delivered artefacts**

| Principle | Artefact | Location |
|---|---|---|
| Rigour and formality | Canonical signature payload construction | `logic/custody.py`, `logic/graph_integrity.py`, `seed.py` |
| Rigour and formality | Lifecycle expressed as a formal state machine | `logic/state_machine.py` |
| Rigour and formality | Burndown charts per increment | `diagrams/increment*_burndown_chart` |
| Separation of concerns | Four-layer architecture | `app/routes/`, `app/logic/`, `app/models/`, `app/templates/` |
| Separation of concerns | Authorisation as decorators | `utils/decorators.py` |
| Separation of concerns | Audit recording in one module | `utils/audit.py` |
| Modularity | Ten blueprints registered by the application factory | `app/__init__.py` |
| Modularity | Business logic free of framework dependencies | `app/logic/` |
| Abstraction | Custody chain as a directed acyclic graph | `logic/graph_integrity.py` |
| Abstraction | Eight heterogeneous signals as a normalised vector | `logic/risk_scoring.py` |
| Abstraction | UML models of the system | Chapter 8 |
| Anticipation of change | Ordered model fallback list and total time budget | `logic/ai_assistant.py`, `config.py` |
| Anticipation of change | Configurable risk weights and thresholds | `logic/risk_scoring.py`, admin settings route |
| Anticipation of change | Git configuration management and 172 regression tests | repository, `tests/` |
| Generality | Pluggable factor pipeline in the risk engine | `logic/risk_scoring.py` |
| Generality | Verifier operating on any custody graph | `logic/graph_integrity.py` |
| Incrementality | Three increments and two maintenance iterations | Chapter 4 |

## 3.11 Summary

This chapter set out the seven principles that underpin software engineering practice and showed where each is realised in DEICMS. Rigour was applied at three distinguishable degrees, with formality reserved for the signature payload and the lifecycle state machine. Separation of concerns operates along three axes — layer, feature and cross-cutting concern — and the failure to apply the third consistently is precisely what produced the defects repaired in maintenance iteration M1. Modularity was assessed quantitatively through cohesion and coupling, including an honest note on the one module that is merely acceptable. Abstraction was catalogued by what each model deliberately ignores. Anticipation of change was assessed against whether the anticipated changes actually occurred — two did. Generality was applied selectively, with one case where it was declined on safety grounds. Incrementality leads directly into the next chapter, which selects and justifies the process model that puts it into practice.

---

\newpage
