# Chapter 15 — Software Reuse and Components

---

## 15.1 The Reuse Landscape

In most engineering disciplines, systems are designed by **composing existing components** that have been used in other systems. Software engineering has historically been more focused on original development, but it is now recognised that to achieve better software, more quickly and at lower cost, a design process based on systematic reuse is required. There has been a major switch to reuse-based development.

Reuse-based software engineering operates at three levels of granularity.

**Table 15.1 — The three levels of reuse**

| Level | Description | DEICMS instances |
|---|---|---|
| **Application system reuse** | A whole application system is reused, either incorporated unchanged into another system (COTS reuse) or by developing application families | None — no whole application was incorporated |
| **Component reuse** | Components of an application, from sub-systems down to single objects, are reused | Flask, SQLAlchemy, Flask-Login, Flask-WTF, Flask-Limiter — frameworks and sub-systems that structure the application |
| **Object and function reuse** | Software components implementing a single well-defined object or function are reused | `hashlib`, `cryptography`, Pillow, python-magic, scikit-learn, ReportLab, PyOTP |

**Table 15.2 — Benefits and problems of reuse, assessed for this project**

| Benefits | Realised here? |
|---|---|
| **Increased dependability** — reused software has been tried and tested in working systems, so it is more dependable than new software | **Yes, decisively.** Every cryptographic primitive is a reused, audited implementation. Writing them would have been both slower and less trustworthy |
| **Reduced process risk** — the cost of existing software is already known, which is a major risk factor | **Yes.** The Category B stories carry 2- and 3-point estimates precisely because the cost of calling a known library is predictable, unlike the 13-point verifier |
| **Effective use of specialists** — specialists' knowledge is encapsulated rather than re-derived by each team | **Yes.** No cryptographer, no imaging expert and no machine-learning researcher was available to this project; all three are present in its dependencies |
| **Standards compliance** — reusing standard implementations means conforming to standards | **Yes.** TOTP, EXIF, MIME, PDF and the OpenAI-compatible API shape are all standard because a standard implementation was used |
| **Accelerated development** — less to write and less to validate | **Yes.** Nine third-party integrations against roughly five thousand lines of original code |

| Problems | Encountered here? |
|---|---|
| **Increased maintenance costs** — if the source of a reused element is unavailable or evolves, change may become difficult | **Yes** — the hosted language model was retired by its provider; the project could neither prevent nor delay it |
| **Lack of tool support** — some tools do not support development with reuse | Not encountered |
| **Not-invented-here syndrome** — engineers prefer to rewrite rather than reuse | Not encountered; the opposite discipline was needed — resisting the temptation to *claim* library work as original (Section 16.6) |
| **Creating and maintaining a component library** | Not applicable — no internal component library was created |
| **Finding, understanding and adapting reusable components** | Real but modest: python-magic requires a native library that is absent from some environments, which is why one content-validation test passes on the development machine and is skipped in a bare container |

Reuse of standard parts is a **measure of the maturity of an engineering field**, and the reuse profile of DEICMS is essentially that of a mature discipline: the project wrote the part that is specific to its problem and bought everything that is not.

## 15.2 Application Frameworks Used

An **application framework** is a sub-system design made up of a collection of abstract and concrete classes and the interfaces between them. The framework is specialised by the developer adding concrete classes and overriding abstract ones. Frameworks are a form of component reuse at the sub-system level, and they differ from libraries in a crucial way: **with a library, your code calls it; with a framework, it calls your code.** This inversion of control is what makes a framework a design decision rather than a convenience.

**Table 15.3 — Frameworks used, and what each inverts**

| Framework | Type | What it controls | What DEICMS supplies |
|---|---|---|---|
| **Flask** | Web application framework | The request lifecycle: it receives the HTTP request, routes it, and invokes the handler | Route handlers, blueprints, the application factory, `before_request` hooks |
| **SQLAlchemy** | Object-relational mapping framework | Query construction, session management, the mapping between objects and rows, and the emission of SQL | Model class declarations, relationships, constraints, and event listeners |
| **Flask-Login** | Authentication framework | Session establishment, the `current_user` proxy, and the `@login_required` gate | The user loader and the credential check |
| **Flask-WTF** | Form and CSRF framework | Token generation and validation on every state-changing request | Form definitions |
| **Flask-Limiter** | Rate-limiting framework | Request counting and refusal | The limit declarations |
| **pytest** | Testing framework | Test discovery, fixture lifecycle, assertion rewriting, reporting | Test functions and fixtures |

Frameworks are conventionally classified into three types, and it is worth placing these.

**Table 15.4 — Framework classification**

| Class | Definition | DEICMS |
|---|---|---|
| **System infrastructure frameworks** | Support the development of system infrastructure such as communications, user interfaces and compilers | Flask, SQLAlchemy |
| **Middleware integration frameworks** | Standards and classes supporting component communication and information exchange | None used directly |
| **Enterprise application frameworks** | Concerned with specific application domains, embedding knowledge of that domain | **None — and this is significant.** No forensic or evidence-management framework was used, because the domain knowledge is precisely what this project contributes |

The empty third row is the most informative in the table. Had an evidence-management framework been adopted, the domain rules — the lifecycle, the custody model, the integrity semantics — would have come from the framework rather than from the project, and the Category C claim would have been substantially weaker. The reuse decisions were therefore made **at the infrastructure level and stopped there**, which is exactly the boundary the coursework's categorisation requirement is designed to test.

## 15.3 COTS and Library Reuse

COTS — commercial-off-the-shelf — product reuse means using large-scale, off-the-shelf systems that provide substantial functionality out of the box. The DEICMS analogue is the set of libraries and the one hosted service it consumes. Table 15.5 records each with what it provides, what remains the project's own work, and what is given up by reusing it.

**Table 15.5 — Reused components: what is bought and what is given up**

| Component | What it provides | What remains the project's work | What is given up |
|---|---|---|---|
| `hashlib` (SHA-256) | The hash function | When to hash (plaintext at intake), what the hash means (immutable ground truth), and how it is compared during verification | Nothing material — the algorithm is standardised |
| `cryptography` (Ed25519) | Key generation, signing, verification | **The canonical payload definition** — which bytes are signed and in what order (Section 10.6.1) | Nothing material |
| `cryptography` (AES-256-GCM, Fernet) | Authenticated encryption | Key derivation policy, what is encrypted, and the ordering of hashing before encryption | Nothing material |
| Pillow | EXIF parsing | Which fields to retain and how to store them | Control over parsing edge cases in exotic image formats |
| python-magic | Magic-byte MIME detection | The MIME-to-extension policy table and the rejection rule | Portability — it depends on a native library absent in some environments |
| SQLAlchemy | ORM, query construction, event system | The six-entity model, relationships, constraints, and the append-only event listeners | Fine control over emitted SQL; database portability is gained in exchange |
| scikit-learn (Isolation Forest) | The anomaly-detection algorithm | The six-dimensional feature vector, the score mapping, and the framing as "suggested for review" | Interpretability — the forest cannot explain itself, which is why it is presented beside the explainable score, not instead of it |
| ReportLab | PDF layout and generation | Document structure, content selection, and running a fresh verification at generation time | Nothing material |
| PyOTP | TOTP generation and validation | Enrolment flow and the login integration | Nothing material |
| NVIDIA NIM (hosted model) | Natural-language generation | **Five of the six pipeline stages**: intent classification, access-scoped retrieval, prompt construction, validation, hallucination detection | **Control and availability** — the provider retired the selected model, and the project could only react |

The final row is the clearest illustration of the central trade of reuse. The project gained a capability it could not otherwise have had at all — no locally trainable model was within reach — and gave up control over whether that capability continues to exist. The mitigation was structural rather than contractual: invoke the model through one method, keep an ordered fallback list, and degrade to a context-aware mock. When the retirement happened, the change was confined to a configuration value and a list.

## 15.4 Component-Based Software Engineering in DEICMS

Component-based software engineering (CBSE) is development by **composing independent components with well-defined interfaces**. A component in the CBSE sense is more than a class: it is an independent executable entity that provides services through a published interface, makes no assumptions about other components beyond those interfaces, and is deployable without recompilation of its clients.

Two CBSE ideas apply usefully here.

**Components provide and require services.** A component's interface has two halves: the **provides** interface, describing the services it offers, and the **requires** interface, describing what it needs from its environment. Making both explicit is what allows a component to be reasoned about, replaced or tested in isolation.

**Table 15.6 — DEICMS logic modules as components**

| Module | Provides | Requires | Independently testable? |
|---|---|---|---|
| `graph_integrity` | `verify(evidence) → IntegrityReport` | Models; `hashlib`; Ed25519 verification; file access | Yes |
| `risk_scoring` | `score(evidence) → RiskReport` | Models; `audit_formulas` | Yes |
| `chain_reconstruction` | `reconstruct(evidence) → Chain` | Models; access-log queries | Yes |
| `state_machine` | `transition_to(evidence, state, user, reason) → Result` | Models; the audit recorder; `risk_scoring` | Yes |
| `ai_assistant` | `process(message, user) → Response` | Models; `accessible_case_ids`; an HTTP model endpoint **or the mock** | Yes — because the requires interface admits a substitute |
| `audit_formulas` | Three check functions | Models | Yes |
| `crypto` | Key generation, signing, verification | `cryptography` | Yes |

The final column is the practical test of whether these are components or merely files, and the `ai_assistant` row explains why the answer is yes. Its requires interface is satisfiable by *either* a live endpoint *or* a deterministic mock, which is precisely what a well-specified requires interface buys: **substitutability**. This is the same property that made the 93 tests of `test_increment3` possible without network access, and the same property that absorbed the model retirement.

**Where DEICMS is not CBSE.** The honest qualification is that these are components in the *design* sense, not the *deployment* sense. They are Python modules within one application, not independently deployable executables with versioned published interfaces. A genuine CBSE approach would have made them separately versioned and independently replaceable at run time, which would be disproportionate for a system of this size. The report claims component-oriented **design** discipline and no more.

## 15.5 Benefits and Costs of the Reuse Decisions

**Table 15.7 — Assessment of the reuse decisions**

| Decision | Benefit | Cost | Verdict |
|---|---|---|---|
| Reuse all cryptographic primitives | Dependability that could not otherwise be achieved; standards compliance | None material | **Clearly correct.** Custom cryptography is a named threat (Table 2.2) |
| Reuse Flask rather than Django | Retained the architectural decisions that demonstrate engineering | More to build: auth wiring, admin routes, forms | **Correct for this purpose.** Django would have supplied so much that little architecture would remain to demonstrate |
| Reuse SQLAlchemy rather than raw SQL | Database portability; a central place to enforce append-only | Less control over emitted SQL | **Correct.** The event-listener hook alone justifies it |
| Reuse scikit-learn's Isolation Forest | A working anomaly detector for a 5-point story | Uninterpretable output | **Correct, with mitigation.** Presented beside the explainable score, never instead of it |
| Consume a hosted language model | A capability otherwise unreachable | Loss of control; the model was retired mid-project | **Correct, and the mitigation was vindicated.** The seam and fallback list absorbed the change |
| Use no domain framework | The domain logic is the project's own | Everything domain-specific had to be built | **Correct and necessary.** This is where the Category C work lives |

The pattern across every row is one judgement applied consistently: **reuse everything that is not specific to this problem; build everything that is.** That is also, precisely, the boundary the A/B/C categorisation asks a project to draw, which is why this chapter and the next are two views of the same decision — Chapter 15 looks at it as a reuse decision, Chapter 16 as a categorisation one.

One further observation connects reuse to the process model. Reuse-oriented software engineering was surveyed and **rejected as a whole-process model** in Section 4.3.7, on the ground that its defining feature — modifying requirements to fit the available components — is incompatible with a coursework requirement for original complex logic. That rejection was of reuse as a *process*, not of reuse as a *practice*, and the distinction is worth making explicit: DEICMS reuses heavily at the component and function levels while declining to let component availability shape its requirements. A system that had bent its requirements to fit an evidence-management framework would have been faster to build and would have demonstrated much less.

## 15.6 Summary

This chapter examined DEICMS from the perspective of what it deliberately did **not** build. The three levels of the reuse landscape were defined, and the project placed at the component and object levels with no whole-application reuse. The five benefits of reuse were each assessed as realised, and the five problems assessed honestly — with one genuinely encountered, the retirement of a reused hosted service, and one modest portability issue arising from a native dependency.

Six application frameworks were catalogued, with the inversion-of-control distinction between a framework and a library made explicit, and the three framework classes applied — the significant finding being that **no enterprise application framework was used**, because the domain knowledge is what the project contributes and adopting a domain framework would have surrendered it.

Ten reused components were tabulated with what each provides, what remains the project's work, and what is given up — the last column being the one most reports omit. The CBSE perspective was applied to the logic modules as provides-and-requires interfaces, with the `ai_assistant` module used to show what a well-specified requires interface buys, and an honest qualification that these are components in the design sense rather than the deployment sense.

Finally, six reuse decisions were assessed with benefit, cost and verdict, and the single judgement underlying all of them stated: reuse everything that is not specific to this problem, build everything that is. The next chapter audits that same boundary from the other direction.

---

\newpage
