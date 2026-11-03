# Chapter 1 - Introduction

---

## 1.1 The Problem

Digital evidence is trivially copyable and silently alterable. A photograph
from a seized device, a server log, a transaction export - each can be changed
without visible trace, and a court has no way to inspect bytes and tell.

What makes digital evidence admissible is therefore not the evidence but the
**record of its handling**: an unbroken, documented account of who held it,
when, and what was done to it. Break that chain and the evidence is worthless
however genuine it is. The requirement is procedural, and it is exactly the
kind of requirement software is good at enforcing and humans are bad at
remembering.

DEICMS - the Digital Evidence Integrity and Chain-of-Custody Management
System - manages digital forensic evidence so that tampering is either
impossible or evident, every action is attributable, and the system's own
history cannot be rewritten.

## 1.2 Why This Project

The project had to satisfy two conditions simultaneously: be a credible
software system, and provide honest material for all three feature categories
the guidelines require.

Forensic evidence management does both without strain. It has a genuine
relational model with real constraints (Category A). It needs cryptographic,
metadata and machine-learning components that would be irresponsible to
reimplement (Category B). And it poses problems that no library solves -
verifying a chain of custody, ranking exhibits by the attention they need,
reconstructing a history with gaps in it (Category C).

**The domain was chosen because its hardest problems are algorithmic rather
than merely procedural.** Chapter 2 gives the full categorisation and assesses
whether the balance was actually achieved.

## 1.3 The Five Guarantees

Everything the system does serves one of five guarantees. They are stated
here because the chapters that follow refer to them, and because a system's
claims are easier to judge when they are enumerated.

**Table 1.1 - The guarantees, and what would falsify each**

| | Guarantee | Falsified by |
|---|---|---|
| **G1** | An exhibit's content can be shown to be unchanged since intake, or shown precisely where and how it changed | A change that verification does not detect, or a verdict that names no location |
| **G2** | A person sees only the investigations they are assigned to, in every view without exception | Any surface - detail, aggregate, export, generated answer - returning data from an unassigned investigation |
| **G3** | The system's record of its own history is complete and cannot be amended | An action that leaves no record, or a record that can be altered |
| **G4** | An exhibit moves only as its procedure permits, at the hands of someone entitled | A transition that succeeds when the procedure forbids it |
| **G5** | Exhibits can be prioritised by the attention they need, with the reasoning exposed | A ranking its user cannot interrogate |

G2 is the guarantee this project failed twice and repaired twice, in Sprints 4
and 6. That history is in Chapters 9 and 10, told as what it is rather than
minimised.

## 1.4 Objectives

**Table 1.2 - Objectives and where each is assessed**

| | Objective | Assessed in |
|---|---|---|
| O1 | A working system managing the full evidence lifecycle | Ch. 6-10 |
| O2 | Access controlled by both function and case membership, on every route and aggregate | Ch. 9 |
| O3 | A cryptographically verifiable chain of custody with an append-only history | §11.2 |
| O4 | At least three non-trivial algorithms designed and implemented in this project | **Ch. 11 - five delivered** |
| O5 | Third-party services consumed correctly, with the boundary stated honestly | Ch. 2, §11.7 |
| O6 | A genuine agile incremental project with per-iteration artefacts | Ch. 4, 6-10 |
| O7 | An automated test suite of meaningful coverage | Ch. 12 |
| O8 | Quality attributes implemented **and demonstrably enforced** | Ch. 10, §3.7 |

O8 is stated in the form it reached after Sprint 6. Its original wording asked
only that the system be hardened; the word *demonstrably* was added when an
external review observed that enforcement without verification is a claim
rather than a property.

## 1.5 Scope

**Table 1.3 - In and out of scope**

| In scope | Out of scope, and why |
|---|---|
| Investigation and exhibit management, custody recording, integrity verification, lifecycle enforcement, risk assessment, natural-language querying, audit, export | Production deployment behind a multi-process server - an operational concern, not an engineering demonstration |
| Four roles plus case-level membership | Notifications - no engineering content |
| A single-host deployment with an external model service | Full-text search over exhibit *content* rather than metadata |
| An automated suite running without network access | A mobile client; a multi-language interface |
| | Fine-tuning of the language model - would move Category B work into the project without adding design |

The exclusions are recorded in the product backlog's *won't have* list
(Section 4.4), so the boundary is a decision rather than an omission.

## 1.6 Relationship to the Accepted Proposal

The project proposal approved before implementation specified the Agile
Incremental Model, three increments, five entities, three core algorithms plus
a state machine and an orchestration workflow, and a report structured with
one section per increment.

**Table 1.4 - Deviations from the accepted proposal**

| Proposed | Delivered | Why |
|---|---|---|
| Agile Incremental Model | **Scrum**, an agile incremental framework, with its artefacts implemented | The proposal named the family; §4.1.3 names the member and commits to its artefacts |
| Three increments | **Six sprints** - three planned, three arising from findings | Sprints 4, 5 and 6 each exist because something was found wrong (Ch. 9, 10) |
| Five entities | **Six** - `CaseAccess` added | Case-level membership proved to need its own associative entity (Sprint 4) |
| Six risk signals, three risk levels | **Eight signals, four levels** | Two further signals proved discriminating; a fourth band separated the genuinely critical |
| A named commercial language-model API | **A different hosted model** | The named service was unavailable on terms the project could meet. The requirement never named a vendor, so this changed the design and not the requirements (§3.1.1, §11.6.1) |
| Test coverage above 70% | **78%**, 216 tests | - |

**Every deviation is an addition or a substitution forced by circumstance;
none removes something promised.** They are collected here rather than
scattered, so that a reader holding the proposal can check the delivery
against it in one place.

## 1.7 How to Read This Report

The report is organised according to the development process it used, as the
guidelines require of an incremental model: **one chapter per sprint**, each
containing that sprint's own backlog, tasks, models, tests, burndown, review
and retrospective.

**Table 1.5 - Structure**

| Chapters | Content |
|---|---|
| 1-2 | The problem, and the feature categorisation with its balance self-assessment |
| 3-5 | Requirements at two levels, the process and its justification, the architecture |
| **6-10** | **The six sprints, one chapter each** |
| 11 | The five Category C algorithms, each with pseudocode and UML |
| 12-13 | Verification and validation; conclusions |

Three things are deliberately *not* in this report. There is no restatement of
software-engineering theory: the process is described where it was used, not
in a chapter of its own. There is no diagram that is not UML, and every one is
generated from versioned source so it cannot drift from the code. And there is
no claim of a flawless result - the three maintenance sprints are described at
the same length as the three that went to plan, because a process is
demonstrated by what it catches, not by what it avoids.

---

\newpage
