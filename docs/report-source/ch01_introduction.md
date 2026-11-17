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

The project had to satisfy two conditions simultaneously: to be a credible
software system, and to provide substantial material in each of the three
feature categories.

Forensic evidence management does both without strain. It has a genuine
relational model with real constraints (Category A). It needs cryptographic,
metadata and machine-learning components that would be irresponsible to
reimplement (Category B). And it poses problems that no library solves -
verifying a chain of custody, ranking exhibits by the attention they need,
reconstructing a history with gaps in it (Category C).

The domain was chosen because its hardest problems are algorithmic rather
than merely procedural. Chapter 2 gives the categorization across the three
feature categories and assesses its balance.

## 1.3 The Five Guarantees

Everything the system does serves one of five guarantees. The chapters that follow refer to them by number.

**Table 1.1 - The guarantees, and what would falsify each**

| | Guarantee | Falsified by |
|---|---|---|
| **G1** | An exhibit's content can be shown to be unchanged since intake, or shown precisely where and how it changed | A change that verification does not detect, or a verdict that names no location |
| **G2** | A person sees only the investigations they are assigned to, in every view without exception | Any surface - detail, aggregate, export, generated answer - returning data from an unassigned investigation |
| **G3** | The system's record of its own history is complete and cannot be amended | An action that leaves no record, or a record that can be altered |
| **G4** | An exhibit moves only as its procedure permits, at the hands of someone entitled | A transition that succeeds when the procedure forbids it |
| **G5** | Exhibits can be prioritized by the attention they need, with the reasoning exposed | A ranking its user cannot interrogate |

G2 was breached twice during development and repaired in Sprints 4 and 6;
Chapters 9 and 10 give both cases.

## 1.4 Objectives

**Table 1.2 - Objectives and where each is assessed**

| | Objective | Assessed in |
|---|---|---|
| O1 | A working system managing the full evidence lifecycle | Ch. 6-10 |
| O2 | Access controlled by both function and case membership, on every route and aggregate | Ch. 9 |
| O3 | A cryptographically verifiable chain of custody with an append-only history | §11.2 |
| O4 | At least three non-trivial algorithms designed and implemented in this project | **Ch. 11 - five delivered** |
| O5 | Third-party services consumed correctly, with the boundary stated | Ch. 2, §11.7 |
| O6 | A genuine agile incremental project with per-iteration artifacts | Ch. 4, 6-10 |
| O7 | An automated test suite of meaningful coverage | Ch. 12 |
| O8 | Quality attributes implemented **and demonstrably enforced** | Ch. 10, §3.7 |

O8 reached this wording in Sprint 6. It originally asked only that the system
be hardened; *demonstrably* was added once it became clear that enforcement
without verification is a claim rather than a property.

## 1.5 Scope

**Table 1.3 - In and out of scope**

| In scope | Out of scope, and why |
|---|---|
| Investigation and exhibit management, custody recording, integrity verification, lifecycle enforcement, risk assessment, natural-language querying, audit, export | Production deployment behind a multi-process server - an operational concern, not an engineering demonstration |
| Four roles plus case-level membership | Notifications - no engineering content |
| A single-host deployment with an external model service | Full-text search over exhibit *content* rather than metadata |
| An automated suite running without network access | A mobile client; a multi-language interface |
| | Fine-tuning of the language model - would move Category B work into the project without adding design |

The exclusions are held in the product backlog's *won't have* list
(Section 4.4).

---

\newpage
