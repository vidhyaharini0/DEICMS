# Digital Evidence Integrity & Chain-of-Custody Management System (DEICMS)

## Software Engineering Project Report

---

**Student:** Vidhya Harini Vijayarajan Sangeetha
**Student ID:** 533994
**Course:** Software Engineering
**Degree Programme:** Bachelor's Degree in Data Analysis
**Software Development Process:** Agile / Incremental Model (three increments)
**Repository:** local Git repository (`deicms/`)

---

## Abstract

Digital forensic evidence is admissible in a court of law only when its *chain of custody* — the documented sequence of every person who has handled an item and every action taken upon it — is unbroken and provably free of tampering. Maintaining that guarantee manually is error-prone, and the consequences of a single undocumented gap can invalidate an entire investigation. This report presents the **Digital Evidence Integrity & Chain-of-Custody Management System (DEICMS)**, a secure web application that manages digital forensic evidence from intake to court-ready export while enforcing an unbroken, tamper-evident chain of custody through cryptography and role-based access control.

The system was designed and built to satisfy the three feature categories required by the course: *data / repository* functionality (a relational model of six entities with full CRUD operations, case-level access control, an append-only audit trail, and formula-based audit checks); *third-party services* (SHA-256 hashing, Ed25519 digital signatures and AES-256-GCM encryption from the `cryptography` library, EXIF and magic-byte metadata extraction, a pre-trained large language model consumed through the NVIDIA NIM API, a scikit-learn Isolation Forest, ReportLab PDF generation, and TOTP two-factor authentication); and *complex application logic* implemented from scratch (a graph-based chain-of-custody integrity verification algorithm, a multi-factor evidence risk-scoring algorithm, a heuristic custody-chain reconstruction algorithm, a formal evidence-lifecycle state machine, and a multi-stage orchestration workflow for an AI investigation assistant with hallucination detection).

Development followed the **Agile Incremental Model** across three increments — core case and evidence management, integrity algorithms and the lifecycle state machine, and risk scoring with the AI assistant and security hardening — followed by two maintenance iterations that resolved access-scoping defects found through review testing and a set of correctness and security defects found through a structured code review. Each increment produced a working, tested version of the system together with its own user stories, sprint backlog, UML artefacts, burndown chart, and retrospective. The final system comprises approximately five thousand lines of application code, is validated by a suite of 172 automated tests, and is documented by thirteen UML diagrams. This report describes the full software development process, presents the analysis and design of every increment, gives an algorithmic account of the complex functionalities, and reflects on the process through per-increment retrospectives and a project-level evaluation.

---

## Table of Contents

**Part I — Project Foundations**
1. Introduction
   1.1 Project Background
   1.2 Problem Statement
   1.3 Objectives
   1.4 Scope and Limitations
   1.5 Structure of this Report
2. Software Development Process
   2.1 Choice of Process Model
   2.2 The Incremental Plan
   2.3 Roles, Ceremonies and Definition of Done
   2.4 Tooling and Engineering Practices
3. Requirements Engineering
   3.1 Stakeholders and Personas
   3.2 Functional Requirements
   3.3 Non-Functional Requirements
   3.4 Feature Categorisation (A / B / C) and Balance Rationale
   3.5 Prioritisation and the Product Backlog
4. System-Wide Architecture
   4.1 Technology Stack and Justification
   4.2 Application Architecture (Factory and Blueprints)
   4.3 Component and Deployment Views
   4.4 Data Model and Entity-Relationship Design
   4.5 Security Architecture Overview

**Part II — Increment 1: Core Case & Evidence Management**
5. Increment 1 Planning
6. Analysis and Design
7. Implementation
8. Testing
9. Sprint Review, Burndown and Retrospective

**Part III — Increment 2: Integrity Algorithms & State Machine**
10. Increment 2 Planning
11. Complex Algorithm Design (Graph Integrity, State Machine, Chain Reconstruction)
12. Implementation and User Interface
13. Testing
14. Sprint Review, Burndown and Retrospective

**Part IV — Increment 3: Risk Scoring, AI Assistant & Hardening**
15. Increment 3 Planning
16. Complex Algorithm and Workflow Design (Risk Scoring, AI Orchestration, Anomaly Detection)
17. Implementation
18. Testing
19. Sprint Review, Burndown and Retrospective

**Part V — Maintenance Iterations: Access-Scoping (M1) and Correctness & Hardening (M2)**
20. Maintenance Iteration M1 — Access-Scoping Change Requests
21. Maintenance Iteration M2 — Correctness and Security Hardening

**Part VI — Cross-Cutting Quality**
22. Testing Strategy and Coverage Analysis
23. Security Engineering
24. Feature Categorisation Self-Assessment

**Part VII — Conclusions and Appendices**
25. Project Retrospective, Velocity Analysis and Future Work
26. References
27. Appendices
