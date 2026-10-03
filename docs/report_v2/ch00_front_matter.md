# University of Messina

### Department of Mathematics, Computer Sciences, Physical Sciences and Earth Sciences (MIFT)

### Bachelor's Degree in Data Analysis

&nbsp;

# DEICMS

## Digital Evidence Integrity & Chain-of-Custody Management System

### Agile Incremental Model

### Software Engineering Project Report

&nbsp;

**Submitted to:** Prof. Salvatore Distefano

**Prepared by:** Vidhya Harini Vijayarajan Sangeetha

**Student ID:** 533994

**Academic Year:** 2025 / 2026

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Abstract

Digital forensic evidence is admissible in a court of law only when its *chain of custody* - the documented sequence of every person who has handled an item and every action taken upon it - is unbroken and provably free of tampering. Maintaining that guarantee manually is error-prone, and the consequences of a single undocumented gap can invalidate an entire investigation. This report presents the **Digital Evidence Integrity & Chain-of-Custody Management System (DEICMS)**, a secure web application that manages digital forensic evidence from intake to court-ready export while enforcing an unbroken, tamper-evident chain of custody through cryptography and role-based access control.

The system was designed and built to satisfy the three feature categories required by the course. *Category A - data and repository functionality* comprises a relational model of six entities with full CRUD operations, case-level access control, an append-only audit trail, and formula-based audit checks. *Category B - third-party services* comprises SHA-256 hashing, Ed25519 digital signatures and AES-256-GCM encryption drawn from the `cryptography` library, EXIF and magic-byte metadata extraction, a pre-trained large language model consumed through the NVIDIA NIM API, a scikit-learn Isolation Forest, ReportLab PDF generation, and TOTP two-factor authentication. *Category C - complex application logic implemented from first principles* comprises a graph-based chain-of-custody integrity verification algorithm, a multi-factor evidence risk-scoring algorithm, a heuristic custody-chain reconstruction algorithm, a formal evidence-lifecycle state machine, and a multi-stage orchestration workflow for an AI investigation assistant with hallucination detection.

Development followed the **Agile Incremental Model** across three increments - core case and evidence management, integrity algorithms and the lifecycle state machine, and risk scoring with the AI assistant and security hardening - followed by two maintenance iterations that resolved access-scoping defects found through review testing and a set of correctness and security defects found during a final review pass. Each increment produced a working, tested version of the system together with its own user stories, sprint backlog, UML artefacts, burndown chart, and retrospective.

The report is organised to follow the discipline of software engineering itself rather than the chronology of the project alone: the nature and qualities of software, the seven engineering principles, process models and their selection, project management, requirements engineering, system modelling in UML, architectural design, implementation, testing and quality assurance, security engineering, software evolution and maintenance, and software reuse. Each topic is first presented as engineering theory and then applied concretely to DEICMS, so that the report documents both *what was built* and *why it was built that way*.

The final system comprises approximately five thousand lines of application code, is validated by a suite of 172 automated tests, and is documented by a complete set of UML models spanning use-case, class, entity-relationship, sequence, activity, state-machine, component and deployment views.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Table of Contents

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```
