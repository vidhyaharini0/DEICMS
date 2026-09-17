# Chapter 1 — Introduction

---

## 1.1 Background and Context

Modern criminal and corporate investigations increasingly turn on *digital* evidence: disk images, memory dumps, log files, photographs, intercepted messages, database extracts, and the metadata that surrounds them. Unlike a physical exhibit sealed in an evidence bag, a digital artefact can be copied perfectly, altered without visible trace, and moved between investigators in seconds. This fluidity is precisely what makes digital evidence powerful and, at the same time, fragile as a matter of legal procedure.

Courts admit an exhibit only when the party presenting it can demonstrate an unbroken *chain of custody*: a complete, tamper-evident record of who collected the item, who has held it at every moment since, what was done to it, and proof that its content has not changed between collection and presentation. A single unexplained gap — an hour during which no one is recorded as the custodian, a transfer with no signature, a file whose hash no longer matches the value recorded at seizure — is often sufficient for the evidence to be ruled inadmissible, regardless of how incriminating its content might be.

In practice, the chain of custody has historically been maintained on paper forms and spreadsheets. That approach scales poorly and fails silently. A spreadsheet cannot cryptographically prove that a file is unchanged, cannot prevent an unauthorised analyst from editing a record, and cannot detect that a custody entry has been deleted after the fact. The people who most need these guarantees — forensic investigators, evidence custodians, and the legal teams that rely on their work — are not usually in a position to build bespoke software, and general-purpose document systems do not encode the domain rules that a forensic workflow requires: who may hold which category of evidence, which lifecycle transitions are legally meaningful, and how integrity is proven.

DEICMS — the **Digital Evidence Integrity & Chain-of-Custody Management System** — is a response to that gap. It is a web application in which every action that touches an evidence item is authenticated, authorised against a role and a case membership, cryptographically signed where a hand-off of responsibility occurs, and written to an append-only audit trail. Around this secure core, the system layers analytical capabilities: it verifies the integrity of an entire custody history as a graph rather than a single latest record, scores each item for risk across multiple interacting signals, reconstructs plausible custody chains where records are incomplete, and offers investigators a natural-language assistant that answers questions strictly from the data they are permitted to see.

## 1.2 Problem Definition

The concrete problem DEICMS addresses can be stated as a set of guarantees that a credible digital-evidence system must provide and that ad-hoc tools do not. These five guarantees recur throughout this report as the criteria against which each increment's work is measured.

**Table 1.1 — The five guarantees DEICMS was built to provide**

| # | Guarantee | Why ad-hoc tools fail | How DEICMS delivers it |
|---|---|---|---|
| G1 | Integrity must be **provable, not asserted** | A spreadsheet can store a hash but cannot prove the whole history is untampered | SHA-256 at intake, Ed25519 signatures on custody events, and a graph traversal that verifies *every* link, not just the latest |
| G2 | Access must follow **least privilege at case granularity** | "Logged-in users see everything" leaks across investigations | Four roles plus a case-membership table; every query, dashboard, export and AI answer is scoped |
| G3 | The record must be **tamper-evident and complete** | Rows in a spreadsheet can be edited or deleted silently | Append-only audit trail enforced at the ORM layer; soft deletion preserves history |
| G4 | Procedural rules must be **enforced, not trusted** | Procedure depends on training and vigilance | A formal state machine with role-gated, precondition-constrained transitions |
| G5 | Investigators need **analytical prioritisation** | A human cannot read every audit record across hundreds of items | A multi-factor risk score with interaction rules, plus unsupervised anomaly detection |

Each guarantee is deliberately stated as an engineering obligation rather than a feature, because each one constrains the design in ways that a feature list would not. G1, for example, rules out storing only a current hash; G2 rules out any aggregate query that is not filtered by case membership; G3 rules out physical deletion anywhere in the system.

## 1.3 Motivation

The project was undertaken as coursework for the Software Engineering module, and the domain was chosen deliberately rather than opportunistically. Three considerations drove the choice.

First, the domain **maps honestly onto the three feature categories the coursework requires**. A chain-of-custody system genuinely needs a rich relational model (Category A), genuinely needs established cryptographic and machine-learning libraries that it would be irresponsible to reimplement (Category B), and genuinely needs original algorithmic work that no library provides (Category C). Many project domains require the categories to be manufactured; this one supplies them.

Second, the domain **has real, non-negotiable non-functional requirements**. Security, auditability and integrity are not decorative here — a forensic system that leaks case data or permits history to be rewritten has failed at its purpose, not merely fallen short of best practice. This makes the non-functional requirements examinable and testable rather than aspirational.

Third, the domain **rewards genuine algorithmic thinking**. Verifying that a custody chain is intact is not a database query: it requires modelling the chain as a directed graph, traversing it, and validating multiple independent conditions at every node and edge. That is the kind of problem the complex-functionality requirement exists to elicit.

## 1.4 Project Scope

**Table 1.2 — Scope boundaries**

| In scope | Out of scope |
|---|---|
| Six-entity relational model with full CRUD | Production database deployment or clustering |
| Authentication, optional 2FA, session management, lockout | Certificate from a public certificate authority |
| Role-based and case-based authorisation | Email or push notifications |
| Upload with hashing, metadata extraction, content validation, encryption at rest | Full-text search over evidence *content* |
| Custody transfer workflow with digital signatures | Multi-language interface |
| Evidence lifecycle state machine | Mobile client |
| Five complex algorithms and the anomaly-detection pipeline | Fine-tuning of the language model |
| AI investigation assistant with hallucination detection | Multi-tenant hosting for several organisations |
| Role-scoped dashboards, signed export package, PDF custody report | Automated migration tooling beyond schema creation |
| Append-only audit trail with formula-based checks | Formal accreditation against a forensic standard |

The out-of-scope items are recorded explicitly in the product backlog's *won't-have-this-time* list (Section 7.11) so that the boundary of the release is transparent rather than implied.

Two **limitations** are worth stating at the outset because they are design constraints rather than defects, and the way the system communicates them to the user is itself part of the design. The language model is consumed as a third-party service and, like all such models, can produce plausible but incorrect text; DEICMS mitigates this with a hallucination-detection stage that cross-checks the model's output against retrieved data, but it does not eliminate the underlying risk, and the assistant is positioned as a convenience rather than an authority. The anomaly-detection model is an unsupervised Isolation Forest trained on a small dataset; its output is therefore presented as "suggested for review" alongside the deterministic risk score rather than as a confirmed judgement.

## 1.5 Objectives

**Table 1.3 — Project objectives and how each was met**

| # | Objective | Type | Met by |
|---|---|---|---|
| O1 | Deliver a working web application managing the full evidence lifecycle within cases | Functional | Chapters 10 and 18 |
| O2 | Enforce role-based and case-based access control on every route and aggregate | Functional | Sections 10.3 and 13.3 |
| O3 | Maintain a cryptographically verifiable chain of custody with an append-only audit trail | Functional | Sections 10.5, 10.6 and 11.2 |
| O4 | Design and implement at least three non-trivial algorithms without delegating the interesting work to a library | Algorithmic | Chapter 11 (five delivered) |
| O5 | Consume established third-party services correctly and state the boundary between library and application logic | Integration | Chapters 15 and 16 |
| O6 | Conduct the work as a genuine agile incremental project with per-increment planning and reflection artefacts | Process | Chapter 4 |
| O7 | Validate the system with an automated test suite of meaningful coverage | Quality | Chapter 12 |
| O8 | Harden the system against common web-application vulnerabilities | Quality | Chapter 13 |

## 1.6 Key Contributions

The project's contributions, stated without inflation, are as follows.

- A **graph-based integrity verification algorithm** that models a custody history as a directed acyclic graph and validates hash continuity, signature validity, temporal ordering and custodian continuity across every edge, returning a verdict with a completeness score and a list of specific broken links rather than a single boolean.
- A **multi-factor risk-scoring algorithm** combining eight normalised factors through a weighted sum, amplified by five interaction rules that capture the compounding effect of co-occurring signals, and producing per-factor explanations rather than an opaque number.
- A **heuristic custody-chain reconstruction algorithm** that performs best-first search over candidate links when the recorded chain is incomplete, labelling each inferred link with a confidence level.
- A **formal evidence lifecycle state machine** with six states, role-gated transitions and precondition guards, which converts procedural discipline into enforced logic.
- A **six-stage AI orchestration workflow** with access-scoped retrieval and a hallucination-detection stage that cross-checks every entity reference in the model's reply against the retrieved context.
- A **demonstration of the full software development process** — requirements engineering, modelling, architecture, implementation, testing, and two maintenance iterations — conducted and documented as an agile incremental project.

## 1.7 Structure of this Report

This report is organised to follow the discipline of software engineering rather than the chronology of the project alone. Each chapter first presents the relevant engineering theory and then applies it concretely to DEICMS, so that the report documents both what was built and why it was built that way.

**Table 1.4 — Report structure**

| Chapter | Subject | Corresponding course topic |
|---|---|---|
| 1 | Introduction | Introduction to Software Engineering |
| 2 | Software and Its Qualities | Software Nature and Qualities |
| 3 | Software Engineering Principles | SE Principles |
| 4 | Software Development Process | Software Processes; Agile Development |
| 5 | The Development Iterations | Agile Development (incremental delivery) |
| 6 | Project Management | Software Processes; project planning |
| 7 | Requirements Engineering | Requirements Engineering |
| 8 | System Modelling (UML) | Software Modeling |
| 9 | Software Architecture | Architectural Design |
| 10 | Implementation | Software Processes (development activity) |
| 11 | Complex Algorithms and Workflows | Coursework Category C requirement |
| 12 | Software Testing and Quality Assurance | Software Testing |
| 13 | Security Engineering | Software Qualities (security) |
| 14 | Software Evolution and Maintenance | Software Evolution and Maintenance |
| 15 | Software Reuse and Components | Software Reuse and Components |
| 16 | Feature Categorisation Self-Assessment | Coursework categorisation requirement |
| 17 | Deployment and Operation | DevOps |
| 18 | System Output and Screenshots | — |
| 19 | Conclusion | — |
| 20 | References | — |
| 21 | Appendices | — |

The three development increments and the two maintenance iterations are documented in Chapter 5, each with its own sprint goal, sprint backlog, burndown chart, review and retrospective, so that the per-increment reporting the coursework requires for an agile process is preserved while the syllabus structure of the report is maintained.

## 1.8 Summary

This chapter established the problem domain: digital evidence is legally fragile, its chain of custody must be provable rather than asserted, and the tools traditionally used to maintain it cannot provide that proof. It stated the five guarantees that define the problem, bounded the scope of the work, set out eight objectives against which the project is assessed, and described how the remainder of the report is organised. The next chapter turns from the specific problem to the general one: what kind of artefact software is, and what qualities a software product must exhibit in order to be considered good.

---

\newpage
