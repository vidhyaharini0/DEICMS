# Chapter 18 - System Output and Screenshots

---

## 18.1 Purpose of this Chapter

The preceding chapters describe DEICMS as a design and as an argument; this chapter shows it running. Each screenshot is captioned with the requirements it demonstrates, so the evidence can be checked against the claims rather than merely admired. The set is deliberately **selective**: twenty-one screenshots chosen to evidence the five guarantees of Table 1.1, rather than a tour of every page.

Where two screenshots are more informative as a pair than individually - the same data seen by two roles, the intact and the failed verdict - they are presented that way and the comparison is stated in the caption.

---

## 18.2 Access Control and Role Scoping

*Guarantee G2 - FR-01 to FR-06, FR-21, FR-47, FR-51, FR-52, NFR-01.*

**[SCREENSHOT 18.1 - Login page]**
*The login form. There is no registration link: account creation is Admin-only (FR-21). A failed attempt returns the same message whether the email is unknown or the password wrong, preventing account enumeration.*

**[SCREENSHOT 18.2 - Admin account creation form]**
*The Admin-only route, showing the role selector and the twelve-character password policy (FR-21, FR-22, NFR-12). A fresh Ed25519 key pair is generated for each account.*

**[SCREENSHOT 18.3 - Administrator dashboard]**
*System-wide totals and the security-alerts panel. The Administrator is the only role with global scope.*

**[SCREENSHOT 18.4 - Lead Investigator dashboard, same database]**
*Pending actions within this investigator's cases only. **Compare the totals with 18.3** - the difference is the access scoping introduced in M1 (FR-51).*

**[SCREENSHOT 18.5 - Analyst dashboard, same database]**
*Narrower again: fewer case memberships than the Lead, and a different panel set - the workbench of items this analyst holds in place of pending actions, with the monitoring charts absent. **18.3 to 18.5** are one database seen three ways.*

**[SCREENSHOT 18.6 - Read-Only auditor with no case memberships]**
*The explanatory empty state rather than a blank page or a global view (FR-52). A security constraint producing a better interface, not a worse one.*

---

## 18.3 Evidence Registration and Validation

*Guarantee G3 - FR-10 to FR-15, FR-48.*

**[SCREENSHOT 18.7 - Evidence upload form]**

**[SCREENSHOT 18.8 - Upload rejected on a magic-byte mismatch]**
*An executable renamed with an image extension is rejected because its actual content type does not match its declared one (FR-14). This is the control a file-extension check alone would miss.*

**[SCREENSHOT 18.9 - Evidence detail view]**
*Evidence number, SHA-256 original hash, extracted EXIF metadata, current holder, lifecycle state and risk level.*

---

## 18.4 Chain of Custody and Integrity

*Guarantee G1 - FR-16, FR-17, FR-23 to FR-27, FR-33, FR-56.*

**[SCREENSHOT 18.10 - Custody log for an item]**
*The full chronological chain from the initial Upload entry onward, each event carrying its Ed25519 signature.*

**[SCREENSHOT 18.11 - Integrity verification: Intact verdict]**
*A clean chain. Verdict `Intact`, completeness 100%, no failure rows.*

**[SCREENSHOT 18.12 - Integrity verification: failures located]**
*A tampered chain. **Compare with 18.11.** The failure table locates **every** failing node with its category and explanation - not just the first, which is the design decision of Section 11.2.6.*

**[SCREENSHOT 18.13 - Custody chain reconstruction]**
*Confirmed, Inferred and Unresolved links visually distinguished, each inferred link showing its confidence and reasoning. An inferred link is never presented as confirmed (DR-07).*

---

## 18.5 Lifecycle Enforcement

*Guarantee G4 - FR-28 to FR-30.*

**[SCREENSHOT 18.14 - Transition rejected on an unmet precondition]**
*An attempt to archive an item whose integrity has not been verified as Intact. The exact unmet condition is returned, and the rejection is itself written to the audit trail (FR-29).*

**[SCREENSHOT 18.15 - Flagged item]**
*An item moved to `Flagged` following an integrity failure. Only an Administrator can move it out again.*

---

## 18.6 Risk Scoring and the AI Assistant

*Guarantee G5 - FR-36 to FR-46; and the Category C assistant, FR-40 to FR-43.*

**[SCREENSHOT 18.16 - Per-item risk detail]**
*The full breakdown: each of the eight factors with its normalised value and weighted contribution, any interaction rules that fired with their reasons, and the generated recommendations. The score is an account, not an opaque number.*

**[SCREENSHOT 18.17 - Admin risk settings]**
*The eight weights and three thresholds. Weights are re-normalised to sum to 1.0 on save; thresholds must be strictly increasing (FR-39).*

**[SCREENSHOT 18.18 - Assistant refusing an inaccessible case]**
*A request for a case outside the user's memberships returns an access-denied response. Retrieval is scoped, so the data is never in the prompt to begin with (FR-41).*

**[SCREENSHOT 18.19 - Hallucination warning]**
*An entity reference not present in the retrieved context is flagged and shown as an explicit warning attached to the answer (FR-43).*

---

## 18.7 Audit Trail, Export and Test Execution

*Guarantee G3 - FR-18 to FR-20, FR-49; and Chapter 12.*

**[SCREENSHOT 18.20 - Signed export package and audit trail]**
*The downloaded ZIP with its manifest, audit trail, Ed25519 signature and verification instructions. A recipient can confirm the package is unaltered **without access to the system that produced it** (FR-49).*

**[SCREENSHOT 18.21 - Full test suite and coverage]**
*`pytest` output showing 172 tests passing with no network access, and the `--cov` summary corresponding to Table 12.12.*

---

## 18.8 Code Listings

Six listings accompany the algorithmic accounts of Chapters 10 and 11. Each shows the specific construct the text argues about, not the module in full.

**[CODE LISTING 18.1 - `graph_integrity.py`: the traversal loop and the three per-node checks]**
*Section 11.2.5. Show the depth-first loop, the three checks, and the failure-accumulation step that does **not** break the loop.*

**[CODE LISTING 18.2 - `risk_scoring.py`: the weight table, the five interaction rules and the bonus cap]**
*Sections 11.3.2 to 11.3.4.*

**[CODE LISTING 18.3 - `state_machine.py`: the transition table]**
*Section 11.5.2. The declarative table is the point - show enough rows to make the role guards and preconditions visible.*

**[CODE LISTING 18.4 - The canonical signature payload construction]**
*Section 10.6.1. The sorted-key serialisation of the six fields.*

**[CODE LISTING 18.5 - `case_access.py`: `accessible_case_ids`]**
*Sections 10.3.3 and 13.3.1 - the single point of truth introduced by M1.*

**[CODE LISTING 18.6 - The ORM event listeners enforcing the append-only audit trail]**
*Section 10.2 - the guarantee that binds code not yet written.*

---

\newpage
