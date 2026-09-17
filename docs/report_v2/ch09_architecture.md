# Chapter 9 — Software Architecture

---

## 9.1 Architectural Design Decisions

Architectural design is the design process for identifying the sub-systems that make up a system, together with the framework for sub-system control and communication. It is an early stage of system design, it represents the **link between the specification and the design processes**, and it is often carried out in parallel with some specification activities. Its output is a description of the software architecture.

The software architecture of a program or computing system is the *structure*, or structures, of the system. Those structures comprise the software components, the externally visible properties of those components, and the relationships between them. The emphasis on *externally visible* properties is what distinguishes architecture from detailed design: architecture concerns what a component promises to others, not how it keeps that promise.

Architectural design is a creative process, but the decisions it involves are the same set in every project.

**Table 9.1 — The architectural design decisions, answered for DEICMS**

| Decision | Answer for DEICMS | Rationale |
|---|---|---|
| Is there a generic application architecture that can act as a template? | Yes — the **information system** architecture | DEICMS is a transaction-based system over a shared database with role-differentiated users; this is the canonical information-system shape |
| How will the system be distributed? | **Not distributed** — a single application host with one external service dependency | A single-developer academic project; distribution would add operational complexity without demonstrating additional engineering |
| What architectural patterns are appropriate? | **Layered**, **MVC** and **Repository**, combined | Analysed in Section 9.3 |
| What approach will be used to structure the system? | Decomposition into **layers**, then into **feature modules** within each layer | Serves separation of concerns along both axes (Section 3.4) |
| How will the structural units be decomposed into modules? | Ten routing blueprints, thirteen logic modules, six model modules, three utility modules | Each module owns one concern; assessed for cohesion and coupling in Table 3.4 |
| What control strategy should be used? | **Event-driven** at the outer edge (HTTP request dispatch), **call-return** within | The web framework dispatches; everything beneath it is ordinary procedural invocation |
| How will the design be evaluated? | Against the quality priorities of Table 2.3, and by the four-level QA strategy of Table 6.6 | Security, correctness and verifiability are the criteria that dominate |
| How should the architecture be documented? | Component and deployment diagrams (Figures 8.9, 8.10) plus this chapter | Two structural views plus the decisions behind them |

A note on **Conway's law** is appropriate here, since it governs the relationship between organisation and architecture: a system's structure tends to mirror the communication structure of the organisation that produced it. A single-developer project is the degenerate case — there are no inter-team communication boundaries for the architecture to mirror — and the consequence is worth stating honestly. The architecture of DEICMS is layered because layering was chosen deliberately, not because organisational pressure produced it; but equally, no organisational pressure existed to *prevent* modules from becoming entangled, so the discipline that kept them separate was entirely self-imposed. The M1 defect is a small illustration: with no second developer to ask *"where does the case-scoping rule live?"*, the rule was duplicated inline rather than extracted, and the omission went unnoticed until adversarial testing found it.

### 9.1.1 Architecture and System Characteristics

Architectural decisions have direct consequences for the non-functional characteristics of a system, and those consequences frequently conflict — which is why the architecture cannot be derived mechanically from the requirements.

**Table 9.2 — How the architecture serves each characteristic, and the conflicts**

| Characteristic | Architectural response | Conflict |
|---|---|---|
| **Performance** | Localise critical operations within few components; minimise inter-component communication | Conflicts with maintainability: larger, coarser components perform better but are harder to change. DEICMS chose maintainability, because the workload is small |
| **Security** | Use a **layered** structure with the most critical assets in the innermost layers, and validate at each boundary | Conflicts with performance: each layer boundary costs a check. DEICMS accepted the cost, in line with the priority ordering of Table 2.3 |
| **Safety** | Localise safety-critical operations in a small number of components | DEICMS's analogue is integrity: all integrity logic lives in `graph_integrity` and `crypto`, nowhere else |
| **Availability** | Include redundant components and mechanisms for fault tolerance | Largely out of scope — no redundancy. The one concession is the model-fallback chain, which is availability of a *feature*, not of the system |
| **Maintainability** | Use fine-grained, self-contained components that may readily be changed | Chosen over performance throughout, and vindicated by both maintenance iterations being localised fixes |

The security row is the one that shaped DEICMS most. Placing the most critical assets in the innermost layers is exactly why evidence files are reached only through the logic layer, never directly from a route, and why authorisation is checked at the route boundary *and* the data scoping applied again in the query — the same rule enforced at two layers rather than one.

## 9.2 Architectural Views

No single view conveys everything about a system's architecture. The standard answer is the **4 + 1 view model**, in which four views describe the system from different angles and a fifth — use cases or scenarios — ties them together by illustrating how the others cooperate to deliver a piece of behaviour.

**Table 9.3 — The 4 + 1 architectural views**

| View | Shows | Concerned reader | DEICMS artefact |
|---|---|---|---|
| **Logical** | The key abstractions of the system as objects or object classes | Designers, analysts | Class diagram (Figure 8.2); Section 9.4 |
| **Process** | How the system is composed of interacting processes at run time | Integrators, performance engineers | Single-process; discussed in Section 9.1 (no distribution) |
| **Development / implementation** | How the software is decomposed for development — modules, packages, layers | Programmers, configuration managers | Component diagram (Figure 8.9); Sections 9.4 and 9.5 |
| **Physical / deployment** | How the software's components are distributed across hardware | System engineers, operators | Deployment diagram (Figure 8.10); Chapter 17 |
| **+1 Scenarios (use cases)** | How the other four views work together for a given piece of behaviour | Everyone — it validates the rest | Use-case model and descriptions (Sections 8.2, 8.3); sequence diagrams (Figures 8.4, 8.5) |

The **+1 view is not decoration**: it is the view that exposes whether the other four are consistent. The integrity-verification sequence diagram (Figure 8.4) is the clearest instance — it shows the route (development view), the engine object (logical view), the database and file store (physical view) cooperating on one use case, and it is where a contradiction between those views would become visible.

## 9.3 Architectural Patterns Applied

An architectural pattern is a stylised, abstract description of good practice that has been tried and tested in different systems and environments. The principal patterns are surveyed below and assessed for use in DEICMS.

**Table 9.4 — Architectural patterns surveyed**

| Pattern | Description | Advantages | Disadvantages | Used in DEICMS? |
|---|---|---|---|---|
| **Model-View-Controller (MVC)** | Separates presentation and interaction from the system data; three components — model manages the data, view defines and manages presentation, controller manages user interaction and passes it to the other two | Data can change independently of its representation and vice versa; supports several presentations of the same data | Can involve additional code and complexity when the data model and interaction are simple | **Yes** — models, Jinja templates and blueprint route handlers |
| **Layered architecture** | Organises the system into layers, each providing a set of services to the layer above | Supports incremental development; a layer can be replaced by an equivalent one; localises dependencies | Clean separation is often difficult, and a high-level layer may need to bypass intermediate layers; performance can suffer from multiple levels of interpretation | **Yes** — four layers, described in Section 9.4 |
| **Repository** | All data is managed in a central repository accessible to all components; components interact only through that repository | Components are independent and need not know of each other's existence; changes made by one are propagated to all | The repository is a single point of failure and a possible performance bottleneck; distributing it is difficult | **Yes** — the database is the single shared repository; no logic module calls another to obtain data |
| **Client-server** | Functionality is organised into services, each delivered from a separate server; clients access those services | Servers can be distributed across a network; general functionality is available to all clients | Each service is a single point of failure; performance is unpredictable because it depends on the network | **Partially** — browser-to-application is client-server; the application-to-inference-API relationship is a second client-server pairing |
| **Pipe and filter** | Data flows through a sequence of processing components, each transforming it | Easy to understand; supports transformation reuse; straightforward to add new transformations | The format for data transfer must be agreed between communicating transformations | **Within one component** — the six-stage assistant pipeline is a pipe-and-filter arrangement inside the wider architecture |

Three observations about this table matter more than the entries themselves.

**Patterns compose; they are not alternatives.** DEICMS is simultaneously layered, MVC and repository-based, and these do not conflict because they answer different questions. Layering answers *what depends on what*; MVC answers *how is presentation separated from data*; repository answers *how do components share state*. A design that treated them as a menu to choose from would be answering only one of the three questions.

**The repository pattern is doing quiet but essential work.** No logic module in DEICMS calls another logic module to obtain data. The risk scorer does not ask the integrity verifier for a verdict; it reads the `integrity_status` column that the verifier wrote. This keeps the two modules independent — the coupling assessment of Table 3.4 depends on it — and it is also why defect D2 was possible: when the column the verifier was supposed to write did not exist, the scorer had no way to notice, because it was never talking to the verifier in the first place. That is the honest cost of the pattern's decoupling, and it is the reason the M2 review pass was needed.

**Pipe-and-filter is used at the right scale.** It structures the inside of the AI assistant, where a fixed sequence of transformations genuinely applies, and nowhere else. Applying it system-wide would have been a poor fit, because most of DEICMS is request-response rather than data-flow.

## 9.4 The Layered Architecture of DEICMS

The system is organised into four layers plus a cross-cutting utility set, each providing services to the layer above.

**Table 9.5 — The layers**

| Layer | Contents | Responsibility | May depend on |
|---|---|---|---|
| **Presentation** | Jinja2 templates, static assets | Render data for a specific role; contain no logic beyond formatting | Nothing — receives prepared data |
| **Routing / control** | Ten Flask blueprints | Validate input, enforce authorisation, call into logic, select a template | Logic, models, utilities |
| **Business logic** | Thirteen modules in `app/logic/` | All algorithms and domain rules; contains no framework or HTTP concepts | Models, utilities |
| **Data access** | Six model classes over the SQLAlchemy ORM | Entities, relationships, constraints, ORM-level enforcement | The database |
| **Cross-cutting utilities** | Authorisation decorators, audit recorder, local-time helper | Concerns that cannot be localised to one layer or feature | Models |

Two rules are enforced throughout, and both are checkable rather than aspirational.

**Rule 1 — routes contain no algorithms.** A route handler validates its input, performs its authorisation check, calls a single logic function, and renders. The consequence is that every algorithm in the system can be tested by constructing an object and calling a method, with no HTTP machinery involved — which is the direct reason the test suite runs in seconds and contains 172 tests rather than a handful of slow end-to-end ones.

**Rule 2 — logic modules import no framework.** The `logic/` package knows nothing of requests, sessions or templates. This is what makes the algorithms portable, testable and readable, and it is the property that the component diagram (Figure 8.9) exists to make visible.

The layering is not perfectly clean, and the standard criticism of the pattern applies here too: a high-level layer sometimes needs to bypass an intermediate one. In DEICMS the exception is that route handlers query models directly for simple lookups — fetching a case by its identifier, for example — rather than routing every read through a logic function. This is a deliberate concession: inserting a pass-through logic function for every trivial read would add a layer of indirection that conveys no information. It is recorded here rather than hidden, because an architecture chapter that claims perfect layer discipline is usually describing an intention rather than a system.

## 9.5 The Application Factory and Blueprint Structure

The system is constructed using Flask's **application factory** pattern: rather than creating the application object at import time, a function `create_app(config)` builds and returns a configured instance, registering extensions and blueprints as it goes.

**Table 9.6 — What the application factory enables**

| Property | Consequence |
|---|---|
| The application is built by a function, not at import | A test can construct an application with a test configuration and an in-memory database, independently for every test |
| Configuration is a parameter | Development and production profiles differ by a value, not by edited code |
| Extensions are initialised inside the factory | No import-time global state; no circular imports between models and the application |
| Blueprints are registered in one place | The system's complete route surface is visible in a single function |

The decision to use this pattern was taken on the first day of Increment 1, and the Increment 1 retrospective (Table 5.2) records it as the increment's best decision: *"it made the system testable from the first week and repaid its small up-front cost many times over."* That is an unusually clean example of an architectural decision whose benefit is measurable — without it, the 172-test suite could not exist in its current form.

**Blueprints** are Flask's modularity mechanism: each is a self-contained collection of routes, registered with the application under a URL prefix. DEICMS has ten, one per feature area — `auth`, `cases`, `evidence`, `custody`, `audit`, `risk`, `assistant`, `export`, `dashboard`, `admin` — which realises the *separation by feature* axis of Section 3.4 and gives the system a route surface that can be reasoned about one area at a time.

## 9.6 Technology Stack and Justification

**Table 9.7 — Technology choices, with the alternatives rejected**

| Concern | Choice | Why | Alternative rejected, and why |
|---|---|---|---|
| Language | Python 3 | Mature cryptography, imaging and machine-learning ecosystems in one language; readable enough that the algorithms are the point rather than the syntax | Java — heavier for a project of this size; JavaScript — weaker cryptographic and scientific libraries |
| Web framework | Flask | Minimal and explicit; the application factory and blueprints give exactly the modularity needed without imposing structure | Django — its batteries-included ORM, admin and auth would have supplied so much that little architecture would remain to demonstrate |
| Persistence | SQLAlchemy ORM | Database portability (NFR-09); relationships expressed declaratively; event hooks made the append-only audit trail enforceable at the data layer | Raw SQL — would have tied the system to one engine and given no place to enforce append-only centrally |
| Database (development) | SQLite in WAL mode | Zero-configuration, file-based, sufficient for single-user development | PostgreSQL in development — operational overhead with no engineering benefit at this scale; it remains the production target |
| Cryptography | `cryptography` library (Ed25519, AES-256-GCM, Fernet) and `hashlib` (SHA-256) | Established, audited implementations | Custom cryptography — professionally indefensible; explicitly listed as a threat in Table 2.2 |
| Signature scheme | Ed25519 | Small keys and signatures, fast verification, no parameter choices to get wrong | RSA — larger keys, more configuration surface, more ways to misuse |
| Metadata | Pillow (EXIF) and python-magic (magic bytes) | Content-type validation must inspect actual bytes, not the declared extension | Trusting the file extension — precisely the attack the requirement exists to block |
| Anomaly detection | scikit-learn Isolation Forest | Unsupervised, suited to a small unlabelled dataset, no training data required | A supervised classifier — no labelled corpus of "mishandled evidence" exists |
| Language model | Hosted model via the NVIDIA NIM API | OpenAI-compatible interface, so the provider is replaceable behind one method | A locally hosted model — hardware cost and no demonstrable benefit for the orchestration work, which is what the project contributes |
| PDF generation | ReportLab | Programmatic layout, no external binary dependency | An HTML-to-PDF converter — an extra system dependency for a simpler result |
| Two-factor | PyOTP (TOTP) | Standard algorithm, works with any authenticator application | SMS codes — weaker, and requires a paid gateway |
| Testing | pytest with pytest-cov | Concise fixtures, in-memory database per test, coverage measurement in the same tool | unittest — more ceremony for the same result |
| Diagrams | PlantUML | Text source, so diagrams are version-controlled and diff-visible; single-colour rendering | A graphical editor — binary files that drift silently out of step with the code |

The pattern running through this table is that **the interesting work was kept and the uninteresting work was delegated**. Every rejected alternative was rejected either because it would have done too much (Django, raw SQL's absence of a central enforcement point) or because doing it ourselves would have been irresponsible (custom cryptography). This is the reuse judgement developed at length in Chapter 15.

## 9.7 Design Patterns Used

Architectural patterns organise the system; design patterns organise the code within it. Table 9.8 records the design patterns used, where, and what each buys.

**Table 9.8 — Design patterns applied**

| Pattern | Where used | What it buys |
|---|---|---|
| **Factory** | `create_app()` builds and configures the application | Deferred, parameterised construction; independent instances for testing |
| **Decorator** | `@login_required`, `@role_required`, `@admin_required` on route handlers | Authorisation applied declaratively at the point of use; the rule lives in one module (Section 3.4) |
| **Strategy** | Per-factor normalisation curves in the risk scorer — linear, logarithmic, sigmoid, categorical | Each factor's curve is chosen independently; adding a factor does not modify existing ones |
| **Template Method** | The fixed validation pipeline in the state machine: transition exists → role permitted → preconditions met | The sequence is fixed; the preconditions vary per transition |
| **Facade** | Each algorithm engine exposes a single public method — `verify()`, `transition_to()`, `reconstruct()`, `score()` | Callers depend on one method, not on the algorithm's internal structure; this is what makes the engines unit-testable |
| **Observer** | SQLAlchemy event listeners intercepting UPDATE and DELETE on audit records | The append-only guarantee is enforced at the data layer rather than by every route remembering to respect it |
| **Pipeline (Pipe and Filter)** | The six stages of the AI assistant | Each stage is independently testable; a stage can be added without restructuring |
| **Null Object / graceful degradation** | The context-aware mock returned when the language model is unavailable | Callers need no special case for "no model"; the pipeline always returns a usable answer |

Two of these deserve a sentence more. The **Observer** use is the strongest single design decision in the data layer: an append-only rule enforced by convention would fail the first time a developer forgot it, whereas an ORM event listener fails *closed* — any code path that attempts to rewrite history raises, including code paths not yet written. The **Facade** use is what connects the architecture to the test strategy: because each algorithm hides behind one method returning a structured result, Chapter 12's coverage figures were achievable at all.

## 9.8 Summary

This chapter documented the architecture of DEICMS and the decisions that produced it. The eight standard architectural design decisions were answered explicitly, including the choice not to distribute the system, and the consequences of the architecture for performance, security, safety, availability and maintainability were set out along with the conflicts between them — with the security-over-performance and maintainability-over-performance trade-offs recorded as deliberate.

The system was presented through the 4 + 1 view model, with each view tied to the diagram that documents it. Five architectural patterns were surveyed and three adopted in combination — layered, MVC and repository — with a note that the repository pattern's decoupling is what made defect D2 invisible to the module that suffered from it. The four-layer structure was described with its two enforced rules and one honest exception. The application factory and blueprint structure were explained, including the retrospective's judgement that the factory was Increment 1's best decision. Thirteen technology choices were justified against the alternatives rejected, and eight design patterns were catalogued with what each buys.

The next chapter turns from structure to construction.

---

\newpage
