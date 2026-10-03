# Chapter 13 - Security Engineering

---

## 13.1 The Threat Model

Security encompasses **data confidentiality** and **resource integrity**, together with the measures taken to improve software behaviour in the face of malicious activity: finding, fixing and preventing vulnerabilities across design, development, testing, deployment, operation and maintenance (Section 2.4.5).

For most systems security is one quality among several. For DEICMS it is the dominant one, because the system's entire purpose is to be trustworthy: a chain-of-custody system that leaks case data, or that permits history to be rewritten, has not merely fallen short of best practice - it has failed at the thing it exists to do.

Before describing controls it is necessary to say what they defend against. Table 13.1 states the threat model: who the adversaries are, what each wants, and what the system assumes about them.

**Table 13.1 - Threat model**

| Adversary | Capability assumed | Objective | Primary defence |
|---|---|---|---|
| **External attacker, unauthenticated** | Network access to the application; no credentials | Gain access; enumerate accounts; inject content | TLS; account-creation restricted to Admin; identical login error messages; rate limiting; CSRF tokens |
| **External attacker with stolen credentials** | One valid password | Act as that investigator | Two-factor authentication; account lockout; idle timeout; every action audited under the stolen identity |
| **Insider - investigator outside the case** | Valid credentials for a *different* case | See or alter evidence in a case they are not a member of | Case-membership scoping applied to every route **and** every aggregate; `accessible_case_ids` |
| **Insider - malicious custodian** | Legitimate access to the item | Alter evidence content, or alter the record of their own handling | SHA-256 at intake; Ed25519 signatures; append-only audit trail; full-chain verification |
| **Attacker with database access** | Read access to the stored database | Extract evidence content or usable signing keys | AES-256-GCM encryption of files at rest; private keys Fernet-encrypted under a derived key |
| **Prompt injection via stored content** | Ability to write a case title or description | Steer the language model into emitting markup or leaking data | Output HTML-escaped before formatting; retrieval access-scoped, so the model never holds data the user may not see |

The fourth row is the one that distinguishes this system from an ordinary web application. Most threat models treat the authenticated user as trusted; a forensic system cannot, because **the person who mishandles evidence is usually someone entitled to handle it**. This is why integrity is enforced cryptographically rather than by permission, and why the audit trail is append-only rather than merely restricted.

## 13.2 Defence in Depth

Security in DEICMS is engineered as a property **distributed across every layer of the architecture** rather than concentrated in any single control. The design goal is defence in depth: the compromise or failure of any one control should not by itself defeat the system.

This is the reason for the architectural choice recorded in Table 9.2 - a layered structure with the most critical assets in the innermost layers, validating at each boundary. Authorisation is checked at the route boundary *and* the scoping applied again inside the query. Evidence content is protected by a hash *and* a signature *and* encryption at rest. Each duplication costs something, and each was kept.

**Table 13.2 - The six defensive layers**

| Layer | Defends against | If this layer fails alone |
|---|---|---|
| Transport | Interception, downgrade | Session and request layers still require valid credentials and tokens |
| Session | Credential theft, session hijacking | Authorisation layer still restricts what the session may reach |
| Request | CSRF, injection, clickjacking, brute force | Authorisation layer still restricts what a forged request may reach |
| Authorisation | Cross-case access, privilege escalation | Data layer still yields only encrypted content |
| Data | Database or disk compromise | Integrity layer still detects any alteration |
| Integrity | Tampering, forgery, repudiation | - the last line; failure here is detectable but not preventable |

## 13.3 Controls by Layer

**Table 13.3 - Security controls**

| Layer | Control | Requirement | Introduced |
|---|---|---|---|
| **Transport** | HTTPS only, certificate generated on first run | NFR-13 | Inc. 1 |
| **Transport** | HTTP Strict-Transport-Security header - a browser that has once connected securely refuses plaintext fallback | NFR-13 | Inc. 3 |
| **Session** | Flask-Login session management | FR-01 | Inc. 1 |
| **Session** | Salted password hashing; never plaintext | FR-02 | Inc. 1 |
| **Session** | Password strength policy - minimum 12 characters | NFR-12 | Inc. 1 |
| **Session** | Identical error for unknown email and wrong password, preventing account enumeration | FR-01 | Inc. 1 |
| **Session** | Sliding idle-session timeout | FR-03 | Inc. 1 |
| **Session** | Account lockout after five consecutive failures | FR-47 | Inc. 3 |
| **Session** | Optional TOTP two-factor authentication | FR-47 | Inc. 3 |
| **Session** | Cookies `HttpOnly`, `Secure`, `SameSite=Lax` | NFR-13 | Inc. 3 |
| **Request** | CSRF tokens on every state-changing form | NFR-14 | Inc. 1 |
| **Request** | Rate limiting on the login route | FR-47 | Inc. 3 |
| **Request** | Content-Security-Policy | NFR-14 | **M2** |
| **Request** | `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` | NFR-14 | **M2** |
| **Request** | Untrusted output HTML-escaped *before* formatting is re-applied | NFR-15 | **M2** |
| **Authorisation** | Four-role model; minimum role enforced on every route | FR-04, FR-05 | Inc. 1 |
| **Authorisation** | No public registration; account creation Admin-only | FR-21 | Inc. 1 |
| **Authorisation** | Case-membership scoping on record access | FR-09 | Inc. 1 |
| **Authorisation** | `accessible_case_ids` applied to **every aggregate** - dashboards, rankings, exports, assistant retrieval | FR-51, NFR-01 | **M1** |
| **Authorisation** | Loaded evidence item's case verified against the access that was checked | FR-05 | **M2** |
| **Data** | Evidence files encrypted at rest with AES-256-GCM | FR-48 | Inc. 3 |
| **Data** | Private keys Fernet-encrypted under a key derived from the application secret | FR-48 | Inc. 3 |
| **Data** | Magic-byte validation; executables rejected outright | FR-14, FR-48 | Inc. 1 / 3 |
| **Data** | Soft deletion only - history never destroyed | FR-55, DR-04 | **M2** |
| **Data** | Startup warning when running on insecure default secrets; production profile refuses to boot | NFR-16 | **M2** |
| **Integrity** | SHA-256 at intake; `original_hash` immutable | FR-13 | Inc. 1 |
| **Integrity** | Ed25519 signature on every custody event; signature column `NOT NULL` | FR-23, FR-24 | Inc. 2 |
| **Integrity** | Append-only audit trail enforced at the ORM layer | FR-19 | Inc. 1 |
| **Integrity** | Full-chain graph verification | FR-25 to FR-27 | Inc. 2 |
| **Integrity** | Integrity status written back, so a failed verification raises risk | FR-56 | **M2** |
| **Integrity** | Tamper-evident signed export verifiable without the system | FR-49 | Inc. 3 |

Eleven of the thirty-one controls - more than a third - were introduced in the two maintenance iterations. Section 13.5 addresses what that implies.

### 13.3.1 Two Controls Worth Singling Out

**The append-only audit trail is enforced at the ORM layer, not by convention.** SQLAlchemy event listeners intercept any attempt to update or delete an audit record and raise. The significance is that the guarantee holds for **code that has not been written yet**: a future route that attempts to rewrite history fails, whether or not its author knew the rule. A convention would have failed the first time someone forgot.

**`accessible_case_ids` is a single point of truth, not a shared utility.** The distinction matters. A utility is available to whoever remembers to call it; a single point of truth is the *only* route by which the answer can be obtained, so omitting it is conspicuous rather than silent. Before M1 the scoping rule was computed inline in one place and nowhere else, which is exactly why five other surfaces omitted it without anyone noticing.

## 13.4 Cryptographic Design

The cryptographic choices are conventional, and deliberately so: **a forensic system is not the place to innovate in cryptography.** Weak or custom encryption is itself a named threat category (Table 2.2), and the project implements no cryptographic primitive of its own.

**Table 13.4 - Cryptographic primitives and their role**

| Purpose | Primitive | Property relied upon | Where applied |
|---|---|---|---|
| Content integrity | **SHA-256** | Collision resistance - an altered file cannot produce the same digest | Computed on plaintext at intake; recomputed against the decrypted file during verification |
| Non-repudiation | **Ed25519** | Unforgeability without the private key; strong security margin; small keys and signatures | Signatures over a canonical, sorted-key serialisation of each custody event |
| Confidentiality at rest | **AES-256-GCM** | Authenticated encryption - provides both secrecy **and** tamper-detection of the ciphertext | Evidence files on disk |
| Key protection | **Fernet** | Authenticated symmetric encryption under a derived key | Investigators' private keys, so that database compromise alone yields no usable signing keys |
| Second factor | **TOTP** | Time-bound one-time codes independent of the password | Optional per-account second factor |

Three design points deserve emphasis.

**AES-GCM was chosen over an unauthenticated mode deliberately.** GCM detects tampering with the ciphertext itself, so an attacker who modifies an encrypted evidence file cannot produce plaintext that merely decrypts to something different - decryption fails. An unauthenticated mode such as CBC would have provided confidentiality without that property.

**Hashing precedes encryption.** The intake hash is computed on the **plaintext**, so verification compares like with like after decrypting. Hashing the ciphertext would have made the stored hash depend on the encryption key, breaking verification the moment the key changed.

**The operational caveat is surfaced by the code, not buried in documentation.** The key-encryption secret **must not be rotated after data exists**, because doing so renders every encrypted file and private key unrecoverable. The system emits a startup warning whenever it is running under the insecure development default for this secret, precisely so that the condition cannot pass unnoticed into a real deployment.

## 13.5 Acknowledged Limitations

Consistent with the report's commitment to honesty, the limits of the security engineering are stated rather than concealed.

**Table 13.5 - Known limitations**

| Limitation | Consequence | Status |
|---|---|---|
| The TLS certificate is self-signed | Suitable for local demonstration; a browser will warn, and it provides no identity assurance | Accepted for an academic project; a CA-issued certificate is required before any real use |
| The Content-Security-Policy still permits inline scripts and styles | Weakens the policy's protection against injected script, because the templates embed both | Recorded as a known next step - tightening to a nonce-based policy - rather than claimed as done |
| The application ships with insecure default secrets | A deployment that forgot to set them would run with a known key | Startup warnings make it conspicuous; the production profile refuses to boot; but development mode does not prevent it |
| Rate-limit storage is in-memory | Limits reset on restart and are not shared across worker processes, so they are not enforced consistently under a multi-worker production server | Documented in configuration; production requires a shared backend |
| No load or penetration testing | Behaviour under attack volume and against a skilled adversary is unknown | Out of scope; stated rather than implied |
| Sequential case and evidence numbering | Collision-free in single-user operation because deletion is soft; behaviour under concurrency unverified | Recorded as a known limitation rather than papered over |
| No key rotation procedure | The key-encryption secret cannot be changed after data exists | Inherent to the design; surfaced by a startup warning |

These are the appropriate limitations for an academic project that **demonstrates** security engineering rather than **operating** a production evidence store, and naming them is part of demonstrating that engineering maturely.

## 13.6 The Security Contribution of the Maintenance Iterations

It should be recorded plainly that the security posture described in this chapter was **not fully present at the end of Increment 3**, and that the two maintenance iterations materially improved it.

**Table 13.6 - Security defects found after the planned scope was complete**

| Iteration | Defect | Class | Severity |
|---|---|---|---|
| M1 | Every aggregate view and the AI assistant exposed data across case boundaries | Authorisation | Critical |
| M1 | Conversation history survived logout on a shared browser | Session | High |
| M2 | Cross-case evidence access via a mismatched URL identifier (insecure direct object reference) | Authorisation | Critical |
| M2 | Untrusted model output rendered as HTML - stored cross-site scripting | Injection | High |
| M2 | No Content-Security-Policy or complementary hardening headers | Defence in depth | Medium |
| M2 | No warning when running with insecure default secrets | Configuration | Low |

Two observations follow, and they point in opposite directions.

**The uncomfortable one:** a system whose dominant quality is security shipped its planned scope with two critical authorisation defects. Neither was exotic. The aggregate-scoping leak is the direct consequence of expressing a rule inline rather than once; the insecure direct object reference is one of the most common web vulnerabilities there is. The suite was green throughout.

**The one that matters more:** **both were found, understood at the level of root cause, and fixed before delivery** - by deliberate adversarial testing and structured code review, the two quality-assurance levels that were added precisely because the first two had not been enough (Table 6.6). A security posture arrived at through review and adversarial testing, with the gaps documented and their causes analysed, is more trustworthy than one merely asserted to have been correct from the start. The alternative account - a report claiming the system was secure from Increment 3 onward - would have been both less true and less useful.

## 13.7 Summary

This chapter documented the security engineering of DEICMS, beginning with an explicit threat model that names six adversaries and what each is assumed capable of - including the malicious insider, whom most threat models omit and whom a forensic system cannot afford to. It described the defence-in-depth posture as a property distributed across six layers, with a statement of what still holds if each layer fails alone, and catalogued thirty-one controls by layer, requirement and the iteration that introduced them.

Two controls were singled out for the structural reason they work: the append-only trail is enforced at the ORM layer, so it binds code not yet written; and `accessible_case_ids` is a single point of truth rather than a shared utility, so omitting it is conspicuous rather than silent. The cryptographic design was presented with the property relied upon in each case, and three design points explained - authenticated encryption over an unauthenticated mode, hashing before encryption, and an operational caveat surfaced by the running code rather than by documentation.

Seven limitations were stated with their consequences and status. Finally, the chapter recorded that more than a third of the controls were added in maintenance, that two critical authorisation defects survived a green test suite, and that both were found and fixed by the review practices added in response - which is the honest account and, the report argues, the more trustworthy one.

---

\newpage
