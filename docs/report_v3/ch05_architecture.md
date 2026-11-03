# Chapter 5 - Architecture and Design

---

## 5.1 The Decision Made Before Sprint 1

One architectural decision was taken in Sprint 0 and never revisited:
**business logic is separated from the web interface, and depends on nothing
in it.**

The reason is specific to this project rather than general good practice. Five
Category C algorithms had to be designed, and an algorithm entangled with a
request cycle cannot be tested without one. The separation is what makes the
suite of Chapter 12 runnable without a browser or a network, and what made the
assistant pipeline testable without calling a model.

By Sprint 6 the convention had become a tested requirement - SNF-11 and
SNF-12 - rather than a habit.

## 5.2 Layers

**Figure 8** (package diagram) gives the structure: five layers, dependencies
downward only, no cycle.

**Table 5.1 - The layers**

| Layer | Contents | Depends on | May not depend on |
|---|---|---|---|
| Presentation | Templates | - | anything |
| Interface | Routes, guards, form handling | Logic, Models, Presentation | - |
| Application logic | The five algorithms, formulae, validators | Models, Libraries | **Interface** |
| Domain and persistence | Six entities, constraints, ORM listeners | Libraries | Interface, Logic |
| Libraries | Framework, ORM, cryptography, model client | - | - |

The one prohibition that is enforced rather than merely stated is the third
row's: a static test asserts that no logic module imports `request`,
`session`, `redirect`, `url_for`, `render_template`, `flash` or `abort`.

### 5.2.1 An honest correction to this rule

The first version of this requirement claimed business logic contained **no**
framework imports. That was never true: four logic modules import the
application-context object to read configuration.

The requirement was corrected in Sprint 6 to the boundary that is both true
and meaningful - logic never touches the **request cycle** - rather than
leaving a stricter claim that the code contradicted. **A requirement the code
violates is worse than a weaker requirement the code honours**, because the
first teaches a reader to distrust the document.

## 5.3 Cryptographic Hash Function

*Design decision realising SR-13 and UR-06.*

The requirement asks that a later difference in content be detectable. It
names no mechanism.

| Option | Assessment |
|---|---|
| Checksum (CRC32) | Fast, but collisions are constructible; useless against deliberate alteration |
| MD5 / SHA-1 | Collision attacks are practical; unacceptable in a forensic context |
| **SHA-256** | **Chosen.** Standardised, no practical collision attack, available in the standard library |

The fingerprint taken at intake is stored once and **never updated**; the
current fingerprint is a separate column. Verification is the comparison of
the two, so collapsing them into one column would destroy the capability
rather than optimise it.

## 5.4 Signature Scheme

*Design decision realising SR-23, SR-24 and UR-09.*

The requirement asks that a custody record's author be establishable and
alteration detectable.

| Option | Assessment |
|---|---|
| Shared secret (HMAC) | Anyone able to verify can also forge; defeats non-repudiation |
| RSA | Works; larger keys and signatures |
| **Ed25519** | **Chosen.** Small keys and signatures, strong margin, misuse-resistant |

The design decision that mattered more than the scheme is the **canonical
payload**: six fields serialised with deterministic ordering, fixed before any
signing code was written (retrospective action A2, task T-12.1). The bytes
signed at creation must be byte-identical to those reconstructed at
verification. Settling this first eliminated an entire defect class.

The signature column is **non-nullable**, so an unsigned custody record cannot
be represented - a constraint rather than a convention.

## 5.5 Encryption at Rest

*Design decision realising SR-48 and UR-18.*

Evidence content is encrypted with an authenticated scheme (AES-256-GCM), so
that modification of the stored ciphertext is detected on decryption rather
than producing plausible garbage. Private keys are encrypted separately under
a key derived from a master secret held outside the data.

**The limitation is recorded rather than glossed:** there is no key-rotation
procedure. Rotating the master secret would require re-encrypting the whole
store, and doing so after data exists without that procedure would make
content unrecoverable. This is in Section 13.3 and in the deployment notes.

## 5.6 Second Factor

*Design decision realising SR-47 and UR-01.*

Time-based one-time codes were chosen over the alternatives: SMS is
interceptable and requires a telephone number; hardware tokens cannot be
assumed; email as a second factor usually shares a compromise with the first.
The secret is stored encrypted under the same derived key as private keys.

Account lockout is **time-bounded as well as administratively releasable**
(Figure 16), so an attacker cannot make a denial of service permanent by
deliberately failing an account's logins.

## 5.7 Components and Interfaces

**Figure 9** (component diagram) shows nine components and the interfaces
between them. One is worth drawing attention to.

**Every component that reads case-scoped data depends on a single provider of
`IAccess`.** This is the abstraction whose absence caused the Sprint 4 defect:
the rule "which investigations may this account see" was expressed inline in
each route, and so was omitted by six of them. One provider, one rule, one
place to change it.

**Figure 10** (composite structure) opens the integrity engine, and **Figure
11** (deployment) places the components on hosts, with the model service as
the only element outside the trust boundary.

## 5.8 Design Patterns Used

**Table 5.2 - Patterns, and the problem each solved here**

| Pattern | Where | Problem solved |
|---|---|---|
| Application factory | Application setup | Lets a test build an isolated application with its own database |
| Repository (via ORM) | Models | Keeps queries out of the algorithms |
| **State machine** | Lifecycle | Policy as data rather than branching code (§11.5) |
| **Strategy** | Risk normalisation | Each indicator's curve chosen independently (§11.3) |
| Template method | Prompt construction | A common shape with per-intent variation |
| Observer | Audit listeners | History recorded without each route remembering to |
| Facade | Logic modules | One entry point per algorithm |
| Guard clause | Routes | Authorisation refused early and uniformly |

The Observer row is the one that carries a guarantee. Audit records are
written by listeners at the data-access layer, so **the append-only history
binds code that has not been written yet**: a route added later cannot omit
auditing by forgetting to.

## 5.9 Data Model

**Figure 6** gives the persistent model as a UML class diagram with `«table»`
stereotypes; **Figure 5** gives the design model with behaviour; **Figure 7**
gives one instance snapshot.

**Table 5.3 - Constraints that carry domain meaning**

| Table | Constraint | Why it matters |
|---|---|---|
| `evidence_items` | `original_hash` NOT NULL, never updated | The ground truth all verification compares against (G1) |
| `evidence_items` | `current_hash` separate from `original_hash` | Verification is the comparison; one column would destroy it |
| `evidence_items` | `is_deleted` with no DELETE path | Removal preserves custody and audit history (DR-03) |
| `custody_logs` | `digital_signature` NOT NULL | An unsigned custody record cannot exist (SR-24) |
| `custody_logs` | At least one row per exhibit | Enforced by atomic creation at registration (DR-01) |
| `audit_records` | Insert-only, enforced by listeners | Not expressible in DDL; history cannot be rewritten (G3) |
| `case_access` | UNIQUE (case, investigator) | The associative entity resolving the many-to-many |
| `cases` | `is_archived` with no DELETE path | Closure destroys nothing (DR-04) |

### 5.9.1 A portability caveat found by testing

The risk assessment classifies into four bands including CRITICAL, while the
`risk_level` column is a three-value enumeration. A deliberate mapping
collapses CRITICAL onto High before persistence, so the stored value is always
within the column's domain.

This was invisible under the development database, which does not enforce
enumerations, and would have failed under the production database the
portability requirement anticipates. A test now asserts that the persisted
value lies within the declared domain (SNF-14). **The mapping was correct; the
absence of a test for it was not.**

---

\newpage
