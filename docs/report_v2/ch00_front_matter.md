# University of Messina

## Department of Mathematics, Computer Sciences, Physical Sciences and Earth Sciences (MIFT)

### Bachelor's Degree in Data Analysis

---

# DEICMS

## Digital Evidence Integrity & Chain-of-Custody Management System

### Software Engineering Project Report

---

**Submitted to:**
Prof. Salvatore Distefano

**Prepared by:**
Vidhya Harini Vijayarajan Sangeetha
Student ID: 533994

**Academic Year:** 2025 / 2026

**Software Development Process:** Agile Incremental Model

---

\newpage

## Abstract

Digital forensic evidence is admissible in a court of law only when its *chain of custody* — the documented sequence of every person who has handled an item and every action taken upon it — is unbroken and provably free of tampering. Maintaining that guarantee manually is error-prone, and the consequences of a single undocumented gap can invalidate an entire investigation. This report presents the **Digital Evidence Integrity & Chain-of-Custody Management System (DEICMS)**, a secure web application that manages digital forensic evidence from intake to court-ready export while enforcing an unbroken, tamper-evident chain of custody through cryptography and role-based access control.

The system was designed and built to satisfy the three feature categories required by the course. *Category A — data and repository functionality* comprises a relational model of six entities with full CRUD operations, case-level access control, an append-only audit trail, and formula-based audit checks. *Category B — third-party services* comprises SHA-256 hashing, Ed25519 digital signatures and AES-256-GCM encryption drawn from the `cryptography` library, EXIF and magic-byte metadata extraction, a pre-trained large language model consumed through the NVIDIA NIM API, a scikit-learn Isolation Forest, ReportLab PDF generation, and TOTP two-factor authentication. *Category C — complex application logic implemented from first principles* comprises a graph-based chain-of-custody integrity verification algorithm, a multi-factor evidence risk-scoring algorithm, a heuristic custody-chain reconstruction algorithm, a formal evidence-lifecycle state machine, and a multi-stage orchestration workflow for an AI investigation assistant with hallucination detection.

Development followed the **Agile Incremental Model** across three increments — core case and evidence management, integrity algorithms and the lifecycle state machine, and risk scoring with the AI assistant and security hardening — followed by two maintenance iterations that resolved access-scoping defects found through review testing and a set of correctness and security defects found during a final review pass. Each increment produced a working, tested version of the system together with its own user stories, sprint backlog, UML artefacts, burndown chart, and retrospective.

The report is organised to follow the discipline of software engineering itself rather than the chronology of the project alone: the nature and qualities of software, the seven engineering principles, process models and their selection, project management, requirements engineering, system modelling in UML, architectural design, implementation, testing and quality assurance, security engineering, software evolution and maintenance, and software reuse. Each topic is first presented as engineering theory and then applied concretely to DEICMS, so that the report documents both *what was built* and *why it was built that way*.

The final system comprises approximately five thousand lines of application code, is validated by a suite of 172 automated tests, and is documented by a complete set of UML models spanning use-case, class, entity-relationship, sequence, activity, state-machine, component and deployment views.

---

\newpage

## Table of Contents

**Chapter 1 — Introduction**

- 1.1 Background and Context
- 1.2 Problem Definition
- 1.3 Motivation
- 1.4 Project Scope
- 1.5 Objectives
- 1.6 Key Contributions
- 1.7 Structure of this Report
- 1.8 Summary

**Chapter 2 — Software and Its Qualities**

- 2.1 The Nature of the Software Product
- 2.2 Functional and Structural Quality
- 2.3 Internal and External Qualities
- 2.4 The Quality Attributes
- 2.5 Quality Priorities for DEICMS
- 2.6 Process Qualities
- 2.7 Summary

**Chapter 3 — Software Engineering Principles**

- 3.1 Principles, Methods, Techniques, Methodologies and Tools
- 3.2 The Seven Principles
- 3.3 Rigour and Formality
- 3.4 Separation of Concerns
- 3.5 Modularity, Cohesion and Coupling
- 3.6 Abstraction
- 3.7 Anticipation of Change
- 3.8 Generality
- 3.9 Incrementality
- 3.10 Principle-to-Artefact Mapping
- 3.11 Summary

**Chapter 4 — Software Development Process**

- 4.1 The Four Fundamental Process Activities
- 4.2 Plan-Driven and Agile Processes
- 4.3 A Survey of Process Models
- 4.4 Agile Methods: the Manifesto, Extreme Programming and Scrum
- 4.5 Process Model Selection for DEICMS
- 4.6 Roles, Ceremonies and the Definition of Done
- 4.7 The Increment Plan
- 4.8 Estimation Method
- 4.9 Increment 1 — Core Case and Evidence Management
- 4.10 Increment 2 — Integrity Algorithms and Lifecycle
- 4.11 Increment 3 — Risk Scoring, AI Assistant and Hardening
- 4.12 Maintenance Iteration M1 — Access-Scoping Change Requests
- 4.13 Maintenance Iteration M2 — Correctness and Security Hardening
- 4.14 Comparison with a Plan-Driven Execution
- 4.15 Summary

**Chapter 5 — Project Management**

- 5.1 Planning Approach
- 5.2 Work Breakdown Structure
- 5.3 Project Timeline and Milestones
- 5.4 Risk Management
- 5.5 Configuration Management and Version Control
- 5.6 Quality Assurance Strategy
- 5.7 Summary

**Chapter 6 — Requirements Engineering**

- 6.1 The Requirements Engineering Process
- 6.2 Stakeholders and Personas
- 6.3 Requirements Elicitation
- 6.4 User Requirements
- 6.5 Functional Requirements
- 6.6 Non-Functional Requirements
- 6.7 Domain Requirements
- 6.8 System Requirements
- 6.9 Constraints
- 6.10 Feature Categorisation (A / B / C)
- 6.11 Prioritisation and the Product Backlog
- 6.12 Requirements Validation and Traceability
- 6.13 Summary

**Chapter 7 — System Modelling (UML)**

- 7.1 Why Model a System
- 7.2 Context and Use-Case Models
- 7.3 Use-Case Descriptions
- 7.4 Structural Model: the Class Diagram
- 7.5 Data Model: the Entity-Relationship Diagram
- 7.6 Interaction Models: Sequence Diagrams
- 7.7 Behavioural Models: Activity Diagrams
- 7.8 State Machine Model: the Evidence Lifecycle
- 7.9 Implementation and Deployment Models
- 7.10 Diagram Index
- 7.11 Summary

**Chapter 8 — Software Architecture**

- 8.1 Architectural Design Decisions
- 8.2 Architectural Views
- 8.3 Architectural Patterns Applied
- 8.4 The Layered Architecture of DEICMS
- 8.5 The Application Factory and Blueprint Structure
- 8.6 Technology Stack and Justification
- 8.7 Design Patterns Used
- 8.8 Summary

**Chapter 9 — Implementation**

- 9.1 Development Environment and Coding Standards
- 9.2 The Data Layer
- 9.3 Authentication, Authorisation and Session Management
- 9.4 Case and Evidence Management
- 9.5 The Custody Log and the Audit Trail
- 9.6 Cryptographic Services
- 9.7 Dashboards, Reporting and Export
- 9.8 The AI Assistant Interface
- 9.9 Summary

**Chapter 10 — Complex Algorithms and Workflows**

- 10.1 What Makes a Functionality Complex
- 10.2 Chain-of-Custody Graph Integrity Verification
- 10.3 Multi-Factor Evidence Risk Scoring
- 10.4 Custody Chain Reconstruction
- 10.5 The Evidence Lifecycle State Machine
- 10.6 AI Assistant Orchestration and Hallucination Detection
- 10.7 Complexity Summary
- 10.8 Summary

**Chapter 11 — Software Testing and Quality Assurance**

- 11.1 Testing Objectives and Philosophy
- 11.2 Development Testing
- 11.3 Test-Driven Development
- 11.4 Release Testing
- 11.5 User Testing
- 11.6 Testing and the V-Model
- 11.7 Test Case Catalogue
- 11.8 Coverage Analysis
- 11.9 What the Coverage Does and Does Not Establish
- 11.10 Summary

**Chapter 12 — Security Engineering**

- 12.1 The Threat Model
- 12.2 Defence in Depth
- 12.3 Controls by Layer
- 12.4 Cryptographic Design
- 12.5 Acknowledged Limitations
- 12.6 Summary

**Chapter 13 — Software Evolution and Maintenance**

- 13.1 Why Software Must Evolve
- 13.2 Lehman's Laws Applied to DEICMS
- 13.3 The Four Types of Maintenance
- 13.4 Classification of the Maintenance Work Performed
- 13.5 Maintenance Prediction and Cost Factors
- 13.6 Evolution Strategy and Maintainability Measures
- 13.7 Summary

**Chapter 14 — Software Reuse and Components**

- 14.1 The Reuse Landscape
- 14.2 Application Frameworks Used
- 14.3 COTS and Library Reuse
- 14.4 Component-Based Software Engineering in DEICMS
- 14.5 Benefits and Costs of the Reuse Decisions
- 14.6 Summary

**Chapter 15 — Feature Categorisation Self-Assessment**

- 15.1 The Requirement and the Method
- 15.2 Category A — Data and Repository Functionality
- 15.3 Category B — Third-Party Services
- 15.4 Category C — Complex Application Logic
- 15.5 Balance Assessment
- 15.6 Where the Categories Were Kept Honest
- 15.7 Summary

**Chapter 16 — Deployment and Operation**

- 16.1 Development Environment
- 16.2 Configuration Management
- 16.3 Database Setup and Seeding
- 16.4 Running the System
- 16.5 Path to Production
- 16.6 Summary

**Chapter 17 — System Output and Screenshots**

**Chapter 18 — Conclusion**

- 18.1 Project Retrospective
- 18.2 Velocity Analysis
- 18.3 Was the Process Choice Right?
- 18.4 Achievements
- 18.5 Limitations
- 18.6 Future Work
- 18.7 Concluding Remarks

**Chapter 19 — References**

**Chapter 20 — Appendices**

- Appendix A — User-Story Catalogue
- Appendix B — HTTP Interface Reference
- Appendix C — Database Schema Reference
- Appendix D — Requirements Traceability Matrix
- Appendix E — Glossary and Acronyms

---

\newpage
