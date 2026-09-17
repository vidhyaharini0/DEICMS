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
- 4.9 Summary

**Chapter 5 — The Development Iterations**

- 5.0 Overview
- 5.1 Increment 1 — Core Case and Evidence Management
- 5.2 Increment 2 — Integrity Algorithms and Lifecycle
- 5.3 Increment 3 — Risk Scoring, AI Assistant and Hardening
- 5.4 Maintenance Iteration M1 — Access-Scoping Change Requests
- 5.5 Maintenance Iteration M2 — Correctness and Security Hardening
- 5.6 Comparison with a Plan-Driven Execution
- 5.7 Summary

**Chapter 6 — Project Management**

- 6.1 Planning Approach
- 6.2 Work Breakdown Structure
- 6.3 Project Timeline and Milestones
- 6.4 Risk Management
- 6.5 Configuration Management and Version Control
- 6.6 Quality Assurance Strategy
- 6.7 Summary

**Chapter 7 — Requirements Engineering**

- 7.1 The Requirements Engineering Process
- 7.2 Stakeholders and Personas
- 7.3 Requirements Elicitation
- 7.4 User Requirements
- 7.5 Functional Requirements
- 7.6 Non-Functional Requirements
- 7.7 Domain Requirements
- 7.8 System Requirements
- 7.9 Constraints
- 7.10 Feature Categorisation (A / B / C)
- 7.11 Prioritisation and the Product Backlog
- 7.12 Requirements Validation and Traceability
- 7.13 Summary

**Chapter 8 — System Modelling (UML)**

- 8.1 Why Model a System
- 8.2 Context and Use-Case Models
- 8.3 Use-Case Descriptions
- 8.4 Structural Model: the Class Diagram
- 8.5 Data Model: the Entity-Relationship Diagram
- 8.6 Interaction Models: Sequence Diagrams
- 8.7 Behavioural Models: Activity Diagrams
- 8.8 State Machine Model: the Evidence Lifecycle
- 8.9 Implementation and Deployment Models
- 8.10 Diagram Index
- 8.11 Summary

**Chapter 9 — Software Architecture**

- 9.1 Architectural Design Decisions
- 9.2 Architectural Views
- 9.3 Architectural Patterns Applied
- 9.4 The Layered Architecture of DEICMS
- 9.5 The Application Factory and Blueprint Structure
- 9.6 Technology Stack and Justification
- 9.7 Design Patterns Used
- 9.8 Summary

**Chapter 10 — Implementation**

- 10.1 Development Environment and Coding Standards
- 10.2 The Data Layer
- 10.3 Authentication, Authorisation and Session Management
- 10.4 Case and Evidence Management
- 10.5 The Custody Log and the Audit Trail
- 10.6 Cryptographic Services
- 10.7 Dashboards, Reporting and Export
- 10.8 The AI Assistant Interface
- 10.9 Summary

**Chapter 11 — Complex Algorithms and Workflows**

- 11.1 What Makes a Functionality Complex
- 11.2 Chain-of-Custody Graph Integrity Verification
- 11.3 Multi-Factor Evidence Risk Scoring
- 11.4 Custody Chain Reconstruction
- 11.5 The Evidence Lifecycle State Machine
- 11.6 AI Assistant Orchestration and Hallucination Detection
- 11.7 Complexity Summary
- 11.8 Summary

**Chapter 12 — Software Testing and Quality Assurance**

- 12.1 Testing Objectives and Philosophy
- 12.2 Development Testing
- 12.3 Test-Driven Development
- 12.4 Release Testing
- 12.5 User Testing
- 12.6 Testing and the V-Model
- 12.7 Test Case Catalogue
- 12.8 Coverage Analysis
- 12.9 What the Coverage Does and Does Not Establish
- 12.10 Summary

**Chapter 13 — Security Engineering**

- 13.1 The Threat Model
- 13.2 Defence in Depth
- 13.3 Controls by Layer
- 13.4 Cryptographic Design
- 13.5 Acknowledged Limitations
- 13.6 The Security Contribution of the Maintenance Iterations
- 13.7 Summary

**Chapter 14 — Software Evolution and Maintenance**

- 14.1 Why Software Must Evolve
- 14.2 Lehman's Laws Applied to DEICMS
- 14.3 Types of Maintenance
- 14.4 Classification of the Maintenance Work Performed
- 14.5 Maintenance Prediction and Cost Factors
- 14.6 Evolution Strategy and Maintainability Measures
- 14.7 Summary

**Chapter 15 — Software Reuse and Components**

- 15.1 The Reuse Landscape
- 15.2 Application Frameworks Used
- 15.3 COTS and Library Reuse
- 15.4 Component-Based Software Engineering in DEICMS
- 15.5 Benefits and Costs of the Reuse Decisions
- 15.6 Summary

**Chapter 16 — Feature Categorisation Self-Assessment**

- 16.1 The Requirement and the Method
- 16.2 Category A — Data and Repository Functionality
- 16.3 Category B — Third-Party Services
- 16.4 Category C — Complex Application Logic
- 16.5 Balance Assessment
- 16.6 Where the Categories Were Kept Honest
- 16.7 Summary

**Chapter 17 — Deployment and Operation**

- 17.1 Development Environment
- 17.2 Configuration Management
- 17.3 Database Setup and Seeding
- 17.4 Running the System
- 17.5 Path to Production
- 17.6 A Note on DevOps
- 17.7 Summary

**Chapter 18 — System Output and Screenshots**

- 18.1 Purpose of this Chapter
- 18.2 Authentication and Access Control
- 18.3 Role-Tailored Dashboards
- 18.4 Case and Evidence Management
- 18.5 Chain of Custody and Integrity
- 18.6 Lifecycle State Machine
- 18.7 Risk Scoring and Anomaly Detection
- 18.8 AI Investigation Assistant
- 18.9 Audit Trail and Reporting
- 18.10 Test Execution
- 18.11 Code Listings
- 18.12 Summary

**Chapter 19 — Conclusion**

- 19.1 Project Retrospective
- 19.2 Velocity Analysis
- 19.3 Was the Process Choice Right?
- 19.4 Achievements
- 19.5 Limitations
- 19.6 Future Work
- 19.7 Concluding Remarks

**Chapter 20 — References**

**Chapter 21 — Appendices**

- Appendix A — User-Story Catalogue
- Appendix B — HTTP Interface Reference
- Appendix C — Database Schema Reference
- Appendix D — Requirements Traceability Matrix
- Appendix E — Glossary and Acronyms

---

\newpage
