# Chapter 18 — System Output and Screenshots

---

## 18.1 Purpose of this Chapter

The preceding chapters describe DEICMS as a design and as an argument. This chapter shows it running. Each screenshot is accompanied by a statement of which requirement or algorithm it demonstrates, so that the evidence can be checked against the claims made earlier rather than merely admired.

The screenshots are grouped by the five guarantees of Table 1.1, because those are the criteria the system was built against and the criteria by which it should be judged.

---

## 18.2 Authentication and Access Control

*Demonstrates: FR-01 to FR-06, FR-21, FR-47, NFR-01, NFR-12, NFR-13 — guarantee G2.*

**[SCREENSHOT 18.1 — Login page]**
*Caption: The login form. There is no registration link, because account creation is Admin-only (FR-21). A failed attempt returns the same message whether the email is unknown or the password wrong, preventing account enumeration.*

**[SCREENSHOT 18.2 — Two-factor authentication prompt]**
*Caption: The TOTP second-factor step, reached only after the password has been accepted (FR-47).*

**[SCREENSHOT 18.3 — Account locked message]**
*Caption: Lockout after five consecutive failed attempts (FR-47). An administrator can unlock the account.*

**[SCREENSHOT 18.4 — Admin account creation form]**
*Caption: The Admin-only account-creation route, showing the role selector and the twelve-character password policy (FR-21, FR-22, NFR-12). A fresh Ed25519 key pair is generated for each new account.*

**[SCREENSHOT 18.5 — Unauthorised access redirect]**
*Caption: A Read-Only investigator attempting a state-changing action is redirected with an explanatory message rather than failing silently (FR-05, FR-06).*

---

## 18.3 Role-Tailored Dashboards

*Demonstrates: FR-51, FR-52, NFR-01, NFR-07 — the M1 change request CR-01.*

These four screenshots should be taken from the **same seeded database** so that the differences between them are attributable to role and case membership rather than to different data.

**[SCREENSHOT 18.6 — Administrator dashboard]**
*Caption: System-wide totals and the security-alerts panel showing locked accounts and recent failed logins. The Administrator is the only role with global scope.*

**[SCREENSHOT 18.7 — Lead Investigator dashboard]**
*Caption: Pending actions — flagged items and items awaiting a lifecycle step — **within this investigator's cases only**. Compare the totals with Screenshot 18.6: the difference is the access scoping introduced in M1.*

**[SCREENSHOT 18.8 — Analyst dashboard]**
*Caption: The workbench of items this analyst currently holds, with shortcuts to verify, transfer and change state.*

**[SCREENSHOT 18.9 — Read-Only auditor dashboard, and the empty state]**
*Caption: The review queue for an auditor with shared cases; and, for a user belonging to no case, the explanatory message rather than a blank page or a global view (FR-52).*

---

## 18.4 Case and Evidence Management

*Demonstrates: FR-07 to FR-15, FR-55 — guarantees G2 and G3.*

**[SCREENSHOT 18.10 — Case list]**
*Caption: Paginated and scoped to the viewing investigator's memberships (FR-09).*

**[SCREENSHOT 18.11 — Case detail view]**
*Caption: A case with its evidence items, membership list and status. Soft-deleted items are excluded (FR-55).*

**[SCREENSHOT 18.12 — Evidence upload form]**
*Caption: Upload with category selection. Only allow-listed extensions are accepted (FR-10).*

**[SCREENSHOT 18.13 — Upload rejected on magic-byte mismatch]**
*Caption: An executable renamed with an image extension is rejected because its actual content type does not match its declared one (FR-14). This is the control that a file-extension check alone would miss.*

**[SCREENSHOT 18.14 — Evidence detail view]**
*Caption: The registered item showing its evidence number, SHA-256 original hash, extracted EXIF metadata, current holder, lifecycle state and risk level (FR-11 to FR-15).*

---

## 18.5 Chain of Custody and Integrity

*Demonstrates: FR-16, FR-17, FR-23 to FR-27, FR-56 — guarantee G1.*

**[SCREENSHOT 18.15 — Custody transfer form]**
*Caption: Recording a transfer with recipient, location and reason. Only the current holder or an Admin may transfer (FR-17).*

**[SCREENSHOT 18.16 — Custody log for an item]**
*Caption: The full chronological chain from the initial Upload entry onward, each event carrying its Ed25519 signature (FR-16, FR-23).*

**[SCREENSHOT 18.17 — Integrity verification: Intact verdict]**
*Caption: A clean chain. Verdict `Intact`, completeness 100%, no failure rows. Compare with the next screenshot.*

**[SCREENSHOT 18.18 — Integrity verification: failure located]**
*Caption: A tampered chain. The verdict is downgraded and the failure table locates **every** failing node with its category and explanation — not just the first, which is the design decision described in Section 11.2.6.*

**[SCREENSHOT 18.19 — Custody chain reconstruction]**
*Caption: The reconstructed timeline with Confirmed, Inferred and Unresolved links visually distinguished, each inferred link showing its confidence and reasoning. An inferred link is never presented as confirmed (DR-07, FR-33).*

---

## 18.6 Lifecycle State Machine

*Demonstrates: FR-28 to FR-30 — guarantee G4.*

**[SCREENSHOT 18.20 — Lifecycle transition form]**
*Caption: The available transitions for the current state and the acting investigator's role. A Read-Only investigator sees none at all.*

**[SCREENSHOT 18.21 — Transition rejected on an unmet precondition]**
*Caption: An attempt to archive an item whose integrity has not been verified as Intact. The exact unmet condition is returned, and the rejection is itself written to the audit trail (FR-29).*

**[SCREENSHOT 18.22 — Flagged item]**
*Caption: An item moved to `Flagged` following an integrity failure. Only an Administrator can move it out again.*

---

## 18.7 Risk Scoring and Anomaly Detection

*Demonstrates: FR-36 to FR-39, FR-44 to FR-46 — guarantee G5.*

**[SCREENSHOT 18.23 — Risk dashboard]**
*Caption: Evidence ranked highest-risk first, scoped to accessible cases. The unified score weights the deterministic risk at 0.6 and the anomaly score at 0.4.*

**[SCREENSHOT 18.24 — Per-item risk detail]**
*Caption: The full breakdown — each of the eight factors with its normalised value and weighted contribution, any interaction rules that fired with their reasons, and the generated recommendations. The score is an account, not an opaque number.*

**[SCREENSHOT 18.25 — Anomaly view]**
*Caption: Isolation Forest results with each item's six-dimensional feature vector, framed as "suggested for review" and presented **alongside** the explainable score rather than instead of it (DR-07).*

**[SCREENSHOT 18.26 — Admin risk settings]**
*Caption: The eight weights and three thresholds, editable by an Administrator. Weights are re-normalised to sum to 1.0 on save and thresholds must be strictly increasing (FR-39).*

---

## 18.8 AI Investigation Assistant

*Demonstrates: FR-40 to FR-43, FR-53, FR-54, NFR-05, NFR-15 — Category C complex logic.*

**[SCREENSHOT 18.27 — Assistant answering a data question]**
*Caption: A question answered from retrieved database context, with the metadata bar showing the classified intent, that context was used, and that validation passed.*

**[SCREENSHOT 18.28 — Assistant answering an identity question]**
*Caption: "What are my cases?" answered from the authenticated user, demonstrating the identity intent added in M1 (FR-53).*

**[SCREENSHOT 18.29 — Assistant refusing an inaccessible case]**
*Caption: A request for a case outside the user's memberships returns an access-denied response. Retrieval is scoped, so the data is never in the prompt to begin with (FR-41).*

**[SCREENSHOT 18.30 — Hallucination warning]**
*Caption: An entity reference not present in the retrieved context is flagged as a potential fabrication and shown as an explicit warning attached to the answer (FR-43).*

---

## 18.9 Audit Trail and Reporting

*Demonstrates: FR-18 to FR-20, FR-34, FR-35, FR-49, FR-50 — guarantee G3.*

**[SCREENSHOT 18.31 — Audit trail for an evidence item]**
*Caption: Every event touching the item, with actor, IP address, outcome and timestamp (FR-18).*

**[SCREENSHOT 18.32 — Global audit trail]**
*Caption: The system-wide trail, visible to Administrators only.*

**[SCREENSHOT 18.33 — Formula check results]**
*Caption: The three Category A checks — custody time-gaps above the 72-hour threshold, duplicate entries, and role-permission mismatches (FR-20). Two of these feed the risk scorer.*

**[SCREENSHOT 18.34 — Signed export package]**
*Caption: The downloaded ZIP with its manifest, audit trail, Ed25519 signature and verification instructions. A recipient can confirm the package is unaltered **without access to the system that produced it** (FR-49).*

**[SCREENSHOT 18.35 — PDF chain-of-custody report]**
*Caption: The printable per-item document, containing a **fresh** integrity verdict computed at generation time rather than a cached status (FR-50).*

---

## 18.10 Test Execution

*Demonstrates: Chapter 12.*

**[SCREENSHOT 18.36 — Full test suite passing]**
*Caption: `pytest` output showing 172 tests passing. The suite requires no network access.*

**[SCREENSHOT 18.37 — Coverage report]**
*Caption: `pytest --cov=app` output, corresponding to the figures in Table 12.12. Coverage is highest in the complex-algorithm and cryptographic modules.*

---

## 18.11 Code Listings

The following listings should accompany the algorithmic accounts in Chapter 11. Each is referenced from the section it illustrates.

**[CODE LISTING 18.1 — `graph_integrity.py`: the traversal loop and the three per-node checks]**
*Illustrates Section 11.2.5. Show the depth-first loop, the three checks, and the failure-accumulation step that does not break the loop.*

**[CODE LISTING 18.2 — `risk_scoring.py`: the weight table, the five interaction rules and the bonus cap]**
*Illustrates Sections 11.3.2 to 11.3.4.*

**[CODE LISTING 18.3 — `state_machine.py`: the transition table]**
*Illustrates Section 11.5.2. The declarative table is the point — show enough rows to make the role guards and preconditions visible.*

**[CODE LISTING 18.4 — `chain_reconstruction.py`: the plausibility scoring function]**
*Illustrates Section 11.4.3 — the four criteria combined into one score.*

**[CODE LISTING 18.5 — `ai_assistant.py`: the six-stage pipeline and the hallucination check]**
*Illustrates Sections 11.6.2 and 11.6.4.*

**[CODE LISTING 18.6 — The canonical signature payload construction]**
*Illustrates Section 10.6.1. Show the sorted-key serialisation of the six fields.*

**[CODE LISTING 18.7 — `case_access.py`: `accessible_case_ids`]**
*Illustrates Sections 10.3.3 and 13.3.1 — the single point of truth introduced by M1.*

**[CODE LISTING 18.8 — The ORM event listeners enforcing the append-only audit trail]**
*Illustrates Section 10.2 — the guarantee that binds code not yet written.*

**[CODE LISTING 18.9 — `test_scoping.py`: two adversarial authorisation tests]**
*Illustrates Section 12.5 — tests whose success consists of the system refusing.*

---

## 18.12 Summary

This chapter presented the running system, organised by the five guarantees it was built to provide, with each screenshot tied to the requirements it demonstrates. Where two screenshots are more informative as a pair than individually — the Administrator and Lead Investigator dashboards over the same data, the Intact and failed verification verdicts — they are presented that way and the comparison is stated in the caption.

Nine code listings accompany the algorithmic accounts of Chapters 10 and 11, chosen so that each shows the specific construct the text argues about rather than a module in full.

---

\newpage
