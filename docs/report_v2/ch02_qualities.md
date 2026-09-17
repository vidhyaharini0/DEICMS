# Chapter 2 — Software and Its Qualities

---

## 2.1 The Nature of the Software Product

Software is unlike the products of any other engineering discipline, and almost every difficulty in software engineering can be traced back to that difference. A bridge, an engine or a circuit board is tangible, is constrained by physical law, and is expensive to manufacture but comparatively cheap to inspect. Software is the opposite on every count.

**Table 2.1 — Properties of software as a product, and their consequences**

| Property | Meaning | Consequence for DEICMS |
|---|---|---|
| **Intangible** | There is nothing to look at; progress cannot be observed directly | Progress had to be made visible artificially, through burndown charts and a passing test suite, rather than by inspection |
| **Difficult to describe and evaluate** | Two people can agree on a requirement and mean different things | Requirements were written as user stories with explicit, testable acceptance criteria (Chapter 7) |
| **Malleable** | It can be changed at any time, which is a strength and a trap | An append-only audit trail and a non-nullable signature column were used to make certain things *deliberately* not malleable |
| **Human-intensive** | Cost is almost entirely design and construction effort by people | Estimation was in story points calibrated to one developer's velocity (Section 4.8) |
| **Trivial manufacturing** | Copying costs nothing; all cost is in development | Quality must be built in during development, because there is no "inspection before shipping" stage that could catch it |

The last point is the important one for a forensic system. A manufacturer can test a sample of finished units and reject the batch; a software team cannot, because every copy is identical and the defect, if present, is present in all of them. Quality in software is therefore a property of the *process* as much as of the product, which is why Section 2.6 treats process qualities as first-class.

## 2.2 Functional and Structural Quality

Quality in software divides along two axes that are often conflated.

**Functional quality** reflects how well the software complies with its functional requirements — whether the correct software was produced. It is the fitness for purpose of the artefact: does it do what it was specified to do?

**Structural quality** refers to how well the software meets the non-functional requirements that support the delivery of the functional ones — robustness, maintainability, security, performance. It has much more to do with the degree to which the software works *as needed*, in the conditions it will actually face.

The distinction matters in DEICMS because the two can diverge sharply. An implementation of the custody transfer feature that records the transfer correctly has functional quality. If that same implementation permits an investigator to transfer an item in a case they are not a member of, it has poor structural quality — and in a forensic system that is the more serious failure, because it violates a guarantee (G2) that the entire system exists to provide. Both of the maintenance iterations documented in Sections 5.4 and 5.5 addressed structural rather than functional quality: the features worked, but they worked in ways the system's obligations did not permit.

## 2.3 Internal and External Qualities

A second, orthogonal classification distinguishes who perceives the quality.

- **External qualities** are visible to users — correctness, reliability, robustness, performance, usability, security.
- **Internal qualities** concern developers — verifiability, maintainability, understandability, reusability, portability.

The two are not independent: **internal qualities affect external qualities**. Code that no one can understand cannot be corrected reliably, so poor understandability eventually degrades correctness. This relationship is the reason a project is justified in spending effort on qualities the user will never see. In DEICMS, the decision to place all business logic in a dedicated `app/logic/` package rather than inside route handlers is an internal-quality decision with a direct external consequence: when the risk-scoring defect described in Section 5.5 was found, the fix was confined to a single module and could not disturb the routing layer.

A third classification, **product versus process**, is developed in Section 2.6: the goal is to develop software products, the process is how we do it, and process quality affects product quality.

## 2.4 The Quality Attributes

The quality attributes — often called the *"ilities"* — are the vocabulary in which non-functional requirements are expressed. Each is defined below and assessed for DEICMS.

### 2.4.1 Correctness

Software is **correct** if it satisfies its functional requirements specification — assuming such a specification exists. Because programs are formal objects, if specifications are formal then correctness can in principle be proven as a theorem, or disproved by counterexample through testing.

Correctness has three important limits. It is an **absolute, yes/no quality**: there is no degree of correctness and no notion of severity of deviation — a program that is wrong in one obscure case is, formally, simply incorrect. And it says nothing about the case where **the specification itself is wrong**, which is common when requirements derive from incomplete domain knowledge.

In DEICMS, correctness is established relative to the acceptance criteria of each user story, and verified by 172 automated tests. The limits are visible in the project's own history: the soft-delete defect found in maintenance iteration M2 was a genuine correctness failure against the specification, whereas the access-scoping defects found in M1 were failures against a requirement that had been stated but not carried through into every aggregate view — a specification that was right but incompletely applied.

Correctness is closely tied to the distinction between **verification** and **validation**. Verification asks whether the product complies with its specification — *are we building the product right?* Validation asks whether the product meets the needs of the customer and stakeholders — *are we building the right product?* The automated test suite performs verification; the per-increment sprint reviews, in which each story was demonstrated against its acceptance criteria, perform validation.

### 2.4.2 Reliability

**Reliability** means, informally, that the user can rely on the software; formally, it is the probability of the absence of failures over a given time period. If specifications are correct, all correct software is reliable — but not the converse, because unreliable software may still be correct against a wrong specification, and in practice specifications frequently are wrong. Reliability is therefore the *statistical, degree-bearing* counterpart to the absolute quality of correctness.

DEICMS addresses reliability primarily through determinism: the risk scorer, the integrity verifier and the state machine produce identical outputs for identical inputs, with no reliance on external services. The one non-deterministic component, the language model, is explicitly bounded — the assistant degrades to a context-aware mock when the service is unavailable, so a failure of the external dependency does not become a failure of the system.

### 2.4.3 Robustness

**Robustness** means the software behaves reasonably even in unforeseen circumstances — incorrect input, hardware failure, a dependency that has vanished. Where correctness concerns behaviour inside the specification, robustness concerns behaviour outside it.

Robustness was a recurring theme in the maintenance iterations. The AI assistant's model-invocation path is the clearest example: the hosted model originally selected was retired by the provider mid-project, and the endpoint began returning HTTP 410. A brittle implementation would simply have failed. The implemented design tries an ordered list of candidate models within a bounded total time budget, then falls back to the mock — behaviour that is reasonable in a circumstance the original design had not foreseen.

### 2.4.4 Performance

**Performance** covers time behaviour and the efficient use of resources — memory, processing time, communication. It can be verified analytically through complexity analysis, or empirically through performance evaluation and simulation. Performance affects **scalability**: a solution that works on a small local dataset may not work on a large one.

DEICMS's performance argument is made analytically, because the system is not deployed at scale. Chapter 11 gives the asymptotic complexity of each complex algorithm — the integrity verifier is *O(V + E)* in the size of the custody graph, the risk scorer *O(n)* in the number of custody records for an item — and Section 11.7 collects these. The one place where scalability was consciously traded away is the rate-limiting store, which is in-memory and therefore not shared across worker processes; this is recorded as a known limitation in Section 13.5 rather than hidden.

### 2.4.5 Security

**Security** encompasses data confidentiality and resource integrity, and the measures taken to improve software behaviour in the face of malicious activity: finding, fixing and preventing vulnerabilities across design, development, testing, deployment, operation and maintenance. An evolving but largely consistent set of common flaws recurs across applications — input validation failures, tampering, authentication and authorisation weaknesses, configuration exposure, session management flaws, weak cryptography, parameter manipulation, exception-handling information disclosure, and inadequate auditing.

For DEICMS security is not one quality among many but the dominant one, and Chapter 13 is devoted to it. Table 2.2 maps the standard threat categories onto the specific controls implemented.

**Table 2.2 — Threat categories and DEICMS countermeasures**

| Threat category | Representative attack | DEICMS countermeasure |
|---|---|---|
| Input validation | SQL injection, cross-site scripting | ORM-parameterised queries throughout; HTML escaping before any rendering of user or model text |
| Software tampering | Modifying stored evidence | SHA-256 at intake plus full-chain verification; AES-256-GCM encryption at rest |
| Authentication | Brute force, credential theft | Salted password hashing, account lockout after five failures, optional TOTP second factor |
| Authorisation | Elevation of privilege, disclosure of confidential data | Four-role model plus case-membership scoping enforced on every route and aggregate |
| Configuration management | Retrieval of clear-text configuration | Secrets loaded from environment; production profile refuses to boot on default values |
| Sensitive information | Access to data in storage | Evidence files encrypted at rest; private keys Fernet-encrypted under a derived key |
| Session management | Session hijacking, replay | HttpOnly, Secure, SameSite cookies; sliding idle timeout |
| Cryptography | Weak or custom encryption | Established primitives only — no custom cryptography anywhere in the system |
| Parameter manipulation | Form field or query string manipulation | CSRF tokens on all state-changing requests; server-side authorisation independent of submitted identifiers |
| Exception management | Information disclosure through errors | Generic failure messages; the login path does not reveal whether the email or the password was wrong |
| Auditing and logging | An attacker covers their tracks | Append-only audit trail with updates and deletes blocked at the ORM layer |

### 2.4.6 Usability

**Usability** means the expected users find the system easy to use. It is rather subjective and difficult to evaluate, and is affected mostly by the user interface. The qualification *expected users* matters: a system for trained forensic investigators may legitimately assume domain vocabulary that would confuse a general audience.

DEICMS approaches usability through role-matched interfaces. Rather than presenting one dashboard and hiding controls, each of the four roles is given a view built around its own work — the analyst sees the items they currently hold, the lead investigator sees their cases ranked by risk, the administrator sees system-wide oversight, the read-only auditor sees history without action controls. This decision was reinforced by maintenance iteration M1, which found that a single shared dashboard was not only a usability compromise but a confidentiality defect.

### 2.4.7 Verifiability

**Verifiability** is how easily the properties of the software can be verified. It is mostly an internal quality, but becomes external in security-critical applications — where the ability to demonstrate a property to an auditor is part of what the customer is buying.

DEICMS is an unusual case in which verifiability is simultaneously an internal quality of the codebase and an external, *user-facing feature of the product*. The integrity verifier exists precisely so that a user can verify a property of the data, and the tamper-evident signed export exists so that a third party can verify it afterwards. Internally, verifiability was served by keeping business logic free of framework dependencies, so that algorithms can be tested directly without constructing an HTTP request.

### 2.4.8 Maintainability

**Maintainability** is the ease of maintenance, where maintenance means changes after release. It is economically the dominant quality: maintenance costs exceed 60% of the total cost of software. It decomposes into **repairability** — the ability to correct defects in reasonable time — and **evolvability** — the ability to adapt the software to environmental changes and improve it in reasonable time.

Chapter 14 treats maintenance in full, including the three categories (corrective, adaptive, perfective) and their relative costs. The relevant observation here is that DEICMS provides direct evidence of its own maintainability: the two maintenance iterations made substantive changes — re-scoping every aggregate query, replacing the model-invocation strategy — without structural disruption, because the affected logic was localised.

### 2.4.9 Reusability

**Reusability** is the property that an existing product or component can be used, with minor modification, to build another product. It is similar to evolvability, applies to processes as well as products, and the reuse of standard parts is a measure of the maturity of an engineering field.

DEICMS both consumes and exhibits reuse. It consumes it heavily — every Category B feature is a reuse decision, analysed in Chapter 15. It exhibits it modestly: the `access_control` and `audit` modules are written against no DEICMS-specific assumption beyond the role model and could be lifted into another case-scoped application, and the risk-scoring engine's factor-normalisation-weighting structure is deliberately generic in shape even though its eight factors are domain-specific.

### 2.4.10 Portability

**Portability** is the ability of software to run on different hardware platforms or software environments. It remains relevant as new platforms are introduced and matters particularly when software is distributed across heterogeneous environments.

DEICMS is portable in two respects that were designed rather than accidental. It is **database-portable**: all persistence goes through SQLAlchemy's ORM with no engine-specific SQL in application logic, so the system runs on SQLite in development and is ready for PostgreSQL in production by changing one configuration value. It is **platform-portable**: the application is pure Python with no operating-system-specific calls, and was developed on Windows while its test suite runs unchanged on Linux.

### 2.4.11 Understandability

**Understandability** is the ease of understanding the software. It matters because program modification requires program understanding — you cannot safely change what you do not comprehend, so understandability is a precondition for maintainability rather than a separate luxury.

The measures taken in DEICMS are conventional and applied consistently: descriptive naming, one module per concern, docstrings on every public function stating purpose and contract rather than restating the code, and comments reserved for explaining *why* rather than *what*. The clearest evidence that this succeeded is that the M2 review pass was able to identify a defect in the risk scorer — a factor reading a column that no longer existed — by reading the code, not by observing a failure.

### 2.4.12 Interoperability

**Interoperability** is the ability of a system to coexist and cooperate with other systems.

DEICMS interoperates in three directions: it consumes an external language model over a standard OpenAI-compatible HTTP interface, so the provider can be changed without altering the calling code; it emits a signed ZIP export and a PDF custody report in formats any other system or court process can consume; and it stores evidence metadata in standard EXIF and MIME terms rather than a private vocabulary.

### 2.4.13 Application-Specific Qualities

Beyond the general list, particular application classes have their own dominant qualities. For information systems these are typically **data integrity, security, data availability and transaction performance**. DEICMS is an information system of exactly this kind, and this is why the report devotes an entire chapter to security (Chapter 13) and an entire algorithm to integrity verification (Section 11.2), which in another domain would be minor concerns.

## 2.5 Quality Priorities for DEICMS

Not all qualities can be maximised simultaneously; some conflict. Table 2.3 records the priority assigned to each quality for this system, the justification, and where the report demonstrates it.

**Table 2.3 — Quality priorities**

| Quality | Type | Priority | Justification | Demonstrated in |
|---|---|---|---|---|
| Security | External | **Critical** | A forensic system that leaks or admits tampering has failed at its purpose | Ch. 12 |
| Correctness | External | **Critical** | Evidence handling has legal consequences; a wrong custody record is not a cosmetic defect | Ch. 11 |
| Verifiability | Internal + External | **Critical** | The product's core value proposition is that properties can be *proven*, not asserted | §10.2, §9.7 |
| Maintainability | Internal | High | Two maintenance iterations were anticipated and occurred | Ch. 13 |
| Reliability | External | High | Investigators must be able to depend on the record | §2.4.2 |
| Robustness | External | High | External model retirement proved unforeseen circumstances arise | §5.5 |
| Understandability | Internal | High | Precondition for the maintainability above | §2.4.11 |
| Usability | External | Medium | Important, but a trained-user system may assume domain vocabulary | §9.7 |
| Portability | Internal | Medium | Development-to-production database change anticipated | §8.6 |
| Performance | External | Medium | Forensic caseloads are large but not web-scale; argued analytically | §10.7 |
| Reusability | Internal | Low | Not a project objective; achieved incidentally in two modules | Ch. 14 |
| Interoperability | External | Low | Export formats matter; live integration with other systems does not | §2.4.12 |

Two **trade-offs** were made consciously and are recorded here rather than rationalised later. Security was repeatedly preferred over usability: mandatory admin-only account creation, a twelve-character password minimum and a thirty-minute idle timeout all make the system slightly harder to use, and all were kept. Verifiability was preferred over performance in the integrity verifier, which re-reads and re-hashes file content rather than trusting a cached value — a deliberately more expensive operation, because a cached integrity result is not an integrity proof.

## 2.6 Process Qualities

Because process quality affects product quality, the process itself is assessed against its own three qualities.

**Productivity** denotes the efficiency and performance of the process. For DEICMS this was measured as velocity: forty story points delivered in the first fourteen-day increment, establishing the capacity against which subsequent increments were planned (Section 4.8). The velocity analysis in Section 19.2 examines whether that measure held.

**Timeliness** is the ability to deliver a product on time. The characteristic failure mode is that the development process does not follow the evolution of user requirements, so that a mismatch opens between what users need and what the product can do — the gap widening over time as needs move and the system does not. Incremental delivery is the structural answer: by delivering a working subset every fourteen days and re-examining the backlog at each boundary, the gap is closed repeatedly rather than allowed to accumulate until a single late delivery. The two maintenance iterations are evidence of the same mechanism operating after the increments finished.

**Visibility** requires that all steps of the process and its current status are documented clearly. This was served by four practices: the Git history as an auditable record of how the system evolved; the sprint backlogs and burndown charts making progress observable at any point; the retrospectives recording what was learned; and this report itself, which exists so that the process is legible to someone who did not participate in it.

## 2.7 Summary

This chapter established the vocabulary in which the rest of the report discusses non-functional requirements. Software's intangibility, malleability and trivial manufacturing make quality a property of the process as much as of the product. Qualities divide into functional and structural, and into internal and external, with internal qualities affecting external ones. Thirteen quality attributes were defined and assessed for DEICMS, with security, correctness and verifiability identified as critical, and the trade-offs against usability and performance recorded explicitly. The process itself was assessed against productivity, timeliness and visibility. The next chapter turns from the qualities a product should have to the principles by which engineers achieve them.

---

\newpage
