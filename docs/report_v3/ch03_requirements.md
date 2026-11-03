# Chapter 3 - Requirements Engineering

---

## 3.1 How Requirements Are Expressed in This Project

Requirements in DEICMS are recorded at two levels of abstraction, following the
distinction Sommerville draws between user requirements and system
requirements. The two levels serve different readers and answer different
questions, and conflating them is the commonest way a requirements document
becomes unusable.

**Table 3.1 - The two levels of requirement**

| | User requirements (UR, UNF) | System requirements (SR, SNF) |
|---|---|---|
| Reader | The investigating authority commissioning the system | The developer building it, and the tester verifying it |
| Question answered | What must we be able to do, and what must be true of the system? | What exactly must the software do, and how will we know it does? |
| Language | The reader's own vocabulary - exhibit, custody, investigation | Precise, bounded, countable |
| Abstraction | One statement covers a whole capability | One statement covers one checkable behaviour |
| Count | 22 functional + 9 quality | 61 functional + 21 quality |
| Testable directly? | No - too coarse | **Yes - each carries an acceptance criterion and a named test** |

Every system requirement derives from exactly one user requirement, and every
user requirement is realised by at least one system requirement. The
traceability runs forward from there: requirement to user story, user story to
sprint, sprint to module, module to test. The full chain is given in
Section 3.9 and carried in the right-hand columns of Tables 3.3 and 3.7.

### 3.1.1 Requirements state problems, not solutions

A requirement that names a technology has stopped being a requirement and
become a design decision wearing a requirement's clothes. It forecloses
alternatives before they have been weighed, and it cannot survive the
technology being replaced.

The first version of this requirements set made this mistake repeatedly. The
correction is recorded here rather than hidden, because the difference between
the two columns is the whole point.

**Table 3.2 - Requirements restated as problems**

| Originally written as (a solution) | Restated as (a problem) | Where the technology now lives |
|---|---|---|
| "compute a SHA-256 fingerprint at upload" | **UR-06 / SR-13:** the system shall be able to determine, at any later time, whether the stored content of an exhibit differs in any way from the content registered at intake | §5.3 - cryptographic hash function selection |
| "sign every transfer with the outgoing investigator's Ed25519 private key" | **UR-09 / SR-23:** the system shall enable any holder of a custody record to establish which investigator created it and whether it has been altered since | §5.4 - signature scheme selection |
| "flag outliers with an Isolation Forest" | **UR-13 / SR-44:** the system shall identify exhibits whose handling pattern differs markedly from the rest of the population | §7.6 - anomaly detection approach |
| "encrypt stored files with AES-256-GCM" | **UR-18 / SR-48:** the system shall ensure that evidence content is unintelligible to anyone obtaining the storage medium without authorisation | §5.5 - encryption scheme selection |
| "support TOTP two-factor authentication" | **UR-01 / SR-47:** the system shall allow an account to require a second, independently held factor before granting access | §5.6 - second-factor mechanism |
| "fit the model via the NVIDIA NIM endpoint" | **UR-15 / SR-40:** the system shall answer questions posed in ordinary language using only the records the questioner is entitled to see | §7.5 - language model procurement |

The last row matters for an additional reason. The accepted project proposal
named a particular commercial language-model API. That service proved
unavailable on the terms the project could meet, and a different hosted model
was used instead. **Because the requirement asks for an answer in ordinary
language rather than for a named vendor, the substitution changed the design
and not the requirements.** Had the requirement named the vendor, a commercial
fact outside the project's control would have invalidated a requirement.
Section 5.8 records the substitution as a design decision with its rationale.

## 3.2 Stakeholders

**Table 3.3 - Stakeholders and their primary concern**

| Stakeholder | Role in the system | Primary concern |
|---|---|---|
| Administrator | Operates the system | Nothing is lost; everything is attributable |
| Lead Investigator | Owns investigations | Her team's exhibits are sound and court-admissible |
| Forensic Analyst | Examines exhibits | Analysis is not invalidated by a procedural gap |
| Read-Only Auditor | Reviews after the fact | The record can be inspected but not disturbed |
| The court (indirect) | Consumes the output | The chain of custody is unbroken and demonstrably so |
| Opposing counsel (adversarial) | Attacks the output | Any weakness in the chain is found and exploited |

The last stakeholder is the reason several requirements are phrased
negatively. A system of this kind is specified as much by what it must make
impossible as by what it must allow, and the adversarial reader is the one who
determines whether a negative requirement was written broadly enough. This
proved to be exactly where the project's own defects lay (Section 3.10).

## 3.3 User Requirements - Functional

Stated in the language of the investigating authority. No statement here names
a mechanism.

**Table 3.4 - User requirements**

| ID | Requirement | Realised by |
|---|---|---|
| UR-01 | Investigators must identify themselves before using the system, and the system must not help an outsider discover which accounts exist | SR-01 to SR-03, SR-47 |
| UR-02 | A person's access must be confined to what their function requires | SR-04 to SR-06 |
| UR-03 | A person must see only the investigations they have been assigned to, in every part of the system without exception | SR-07, SR-09, SR-51, SR-52 |
| UR-04 | Investigators must be able to open, find, amend and close investigations, and no act of closure may destroy information | SR-07, SR-08 |
| UR-05 | Investigators must be able to register a digital exhibit, describe it, and classify it | SR-10 to SR-12, SR-15 |
| UR-06 | The system must be able to establish, at any time, whether an exhibit still holds exactly the content it held when collected | SR-13, SR-25 to SR-27, SR-56 |
| UR-07 | Every passage of an exhibit from one person to another must be recorded with who, when, where and why | SR-16, SR-17 |
| UR-08 | The record of what has happened must not be alterable by anyone, including the administrator | SR-18, SR-19 |
| UR-09 | Anyone holding a custody record must be able to establish who created it and whether it has since been altered | SR-23, SR-24 |
| UR-10 | Where a custody history is unsound, the system must say where and in what way, not merely that it is | SR-25 to SR-27, SR-34 |
| UR-11 | Where parts of a custody history are missing, the system must offer the most plausible reconstruction, and must never present a reconstruction as a fact | SR-31 to SR-33, SR-35 |
| UR-12 | An exhibit must pass only through the states its procedure permits, and only at the hands of someone entitled to move it | SR-28 to SR-30 |
| UR-13 | Investigators must be able to tell which exhibits most need attention without reading every record | SR-36 to SR-38, SR-44 to SR-46 |
| UR-14 | The authority must be able to change what it considers risky without the software being rebuilt | SR-39 |
| UR-15 | Investigators must be able to ask about a case in ordinary language and receive answers drawn from the actual records | SR-40 to SR-42, SR-53 |
| UR-16 | An answer must never assert anything not present in the records it was drawn from | SR-43 |
| UR-17 | Accounts must be created only by a person authorised to create them | SR-21, SR-22 |
| UR-18 | Evidence content must remain unintelligible to anyone who obtains the storage medium without authorisation | SR-48 |
| UR-19 | An investigator must be able to hand a complete case to an outside party who can verify it without access to this system | SR-49, SR-50 |
| UR-20 | The system must remain useful, in reduced form, when an external service it depends on is unavailable | SR-42 |
| UR-21 | The system must remain usable as the number of cases and exhibits grows | SR-57, SR-58 |
| UR-22 | Each role must be shown the information its work requires, and never a blank or unexplained screen | SR-52, SR-59 |

## 3.4 User Requirements - Quality

**Table 3.5 - User quality requirements**

| ID | Requirement | Quality attribute |
|---|---|---|
| UNF-01 | Confidentiality between investigations must hold absolutely | Security |
| UNF-02 | Tampering with evidence must be detectable | Integrity |
| UNF-03 | Actions must be attributable to the person who performed them | Non-repudiation |
| UNF-04 | The history of the system must be complete and permanent | Auditability |
| UNF-05 | The system must respond quickly enough not to interrupt an investigator's work | Performance |
| UNF-06 | A failure in one part must not make the whole system unusable | Robustness |
| UNF-07 | The system must be maintainable by a developer who did not write it | Maintainability |
| UNF-08 | The system must not be tied to one database product | Portability |
| UNF-09 | Claims the system makes about itself must be independently checkable | Verifiability |

These are deliberately unmeasurable. That is what distinguishes a user quality
requirement from a system one: "quickly enough not to interrupt an
investigator's work" is the right thing to say to a customer and the wrong
thing to hand a tester. Section 3.7 converts each into statements that can
pass or fail.

## 3.5 System Requirements - Functional

Each row is a single checkable behaviour, traced back to its user requirement
and forward to the sprint that delivered it, the user story that carried it,
and the test that verifies it. Category is the feature categorisation of
Chapter 2: **A** data/repository, **B** third-party, **C** complex custom logic.

**Table 3.6 - System functional requirements**

| ID | Requirement | From | Cat | Pri | Sprint | Story | Verified by |
|---|---|---|---|---|---|---|---|
| SR-01 | The system shall grant access only on presentation of an identifier and a secret known to the account holder, and shall return an identical failure message whether the identifier is unknown or the secret wrong | UR-01 | A | Must | 1 | US-01 | `test_increment1` |
| SR-02 | The system shall store authentication secrets only in a form from which the original cannot be recovered | UR-01 | A | Must | 1 | US-01 | `test_increment1` |
| SR-03 | The system shall end a session after a bounded period without activity | UR-01 | A | Must | 1, 3 | US-01, US-24 | `test_nfr`, `test_increment3` |
| SR-04 | The system shall assign each account exactly one of four functions: administration, investigation leadership, analysis, or review | UR-02 | A | Must | 1 | US-02 | `test_increment1` |
| SR-05 | The system shall verify the required function on every operation, refusing with an explanation rather than failing silently | UR-02 | A | Must | 1 | US-02 | `test_increment1`, `test_scoping` |
| SR-06 | The system shall prevent an account limited to review from causing any change of state | UR-02 | A | Must | 1 | US-02 | `test_scoping` |
| SR-07 | The system shall allow an authorised account to create, search, amend and close an investigation | UR-04 | A | Must | 1 | US-03 | `test_increment1` |
| SR-08 | The system shall treat closure as a reversible marking that destroys no data | UR-04 | A | Must | 1 | US-03 | `test_increment1` |
| SR-09 | The system shall confine each account's view of investigations to those it is assigned to | UR-03 | A | Must | 1, M1 | US-02, US-28 | `test_scoping` |
| SR-10 | The system shall accept for registration only content of permitted kinds, and refuse all others | UR-05 | A | Must | 1 | US-04 | `test_increment1` |
| SR-11 | The system shall allocate each exhibit an identifier unique across the system and record its registrar as first custodian | UR-05 | A | Must | 1 | US-04 | `test_increment1` |
| SR-12 | The system shall create the first custody record in the same indivisible operation as the exhibit, so that no exhibit can exist without a custody history | UR-05 | A | Must | 1 | US-04 | `test_increment1` |
| SR-13 | The system shall derive from the content at registration a value that changes if the content changes, store it, and never alter it thereafter | UR-06 | B | Must | 1 | US-05 | `test_increment1` |
| SR-14 | The system shall determine the actual kind of registered content from the content itself, and refuse it where this contradicts its declared kind | UR-05 | B | Must | 1, 3 | US-06, US-25 | `test_increment1`, `test_increment3` |
| SR-15 | The system shall allow an authorised account to amend an exhibit's description and classification while leaving its content and derived values untouched | UR-05 | A | Must | 1 | US-07 | `test_increment1` |
| SR-16 | The system shall record each passage of an exhibit with the parties, the moment, the place and the reason | UR-07 | A | Must | 1 | US-08 | `test_increment1` |
| SR-17 | The system shall permit only the present custodian or an administrator to pass an exhibit on | UR-07 | A | Must | 1 | US-08 | `test_increment2` |
| SR-18 | The system shall record every access, attempt, amendment and administrative act with actor, origin, moment and outcome | UR-08 | A | Must | 1 | US-09 | `test_increment1` |
| SR-19 | The system shall make amendment and removal of its own history impossible at the point of data access, not merely absent from the interface | UR-08 | A | Must | 1 | US-09 | `test_increment1` |
| SR-20 | The system shall identify custody intervals exceeding a configured duration, repeated records, and acts inconsistent with the actor's function | UR-10 | A | Should | 1 | US-10 | `test_increment1` |
| SR-21 | The system shall offer no route by which an account may be created other than by an administrator | UR-17 | A | Must | 1 | US-11 | `test_increment1` |
| SR-22 | The system shall furnish each new account with a secret meeting a stated strength policy and with the means to establish authorship of its future acts | UR-17 | B | Must | 1 | US-11 | `test_increment1` |
| SR-23 | The system shall attach to every custody record a value, derived from the record's content and the creator's private means, by which both authorship and subsequent alteration can be established | UR-09 | B | Must | 2 | US-12 | `test_increment2` |
| SR-24 | The system shall make a custody record without that value impossible to store | UR-09 | B | Must | 2 | US-12 | `test_increment2` |
| SR-25 | The system shall assemble an exhibit's custody records into a connected structure and examine it from the registration event onward | UR-06, UR-10 | **C** | Must | 2 | US-13 | `test_increment2` |
| SR-26 | The system shall apply to every element three independent examinations - content consistency, authorship validity, and chronological order - and shall continue after a failure so that all failures are found in one pass | UR-10 | **C** | Must | 2 | US-13 | `test_increment2` |
| SR-27 | The system shall report an overall finding, a proportion of the history examined successfully, an ordered list of failures with their nature, and the sequence of events that did verify | UR-06, UR-10 | **C** | Must | 2 | US-13 | `test_increment2` |
| SR-28 | The system shall express the permitted progression of an exhibit as data, each permitted step naming the function entitled to take it and the conditions that must hold | UR-12 | **C** | Must | 2 | US-14 | `test_increment2` |
| SR-29 | The system shall refuse an impermissible step, naming the precise condition unmet, and shall record the refusal in its history | UR-12 | **C** | Must | 2 | US-14 | `test_increment2` |
| SR-30 | The system shall require a stated reason for every permitted step and shall reassess the exhibit's attention level immediately afterwards | UR-12 | **C** | Must | 2, 3 | US-14, US-18 | `test_increment2` |
| SR-31 | The system shall identify discontinuities between confirmed custody records and assemble candidate records capable of filling them | UR-11 | **C** | Must | 2 | US-15 | `test_increment2` |
| SR-32 | The system shall choose among candidates by ranked search against stated criteria, and shall leave a discontinuity unresolved where no candidate reaches a stated minimum | UR-11 | **C** | Must | 2 | US-15 | `test_increment2` |
| SR-33 | The system shall mark every link confirmed, inferred or unresolved, and shall never present an inferred link in the manner of a confirmed one | UR-11 | **C** | Must | 2 | US-15 | `test_increment2` |
| SR-34 | The system shall present a verification finding in a form a reader can act on, and in a form another program can consume | UR-10 | A | Should | 2 | US-16 | `test_increment2` |
| SR-35 | The system shall present a reconstruction as a sequence distinguishing link kinds and exposing the reasoning behind each inference | UR-11 | A | Should | 2 | US-17 | `test_increment2` |
| SR-36 | The system shall derive for each exhibit a fixed set of independent indicators and bring each to a common scale by a transformation suited to its distribution | UR-13 | **C** | Must | 3 | US-18 | `test_increment3` |
| SR-37 | The system shall combine the indicators by weighted summation, amplified where stated combinations co-occur, with the amplification bounded | UR-13 | **C** | Must | 3 | US-18 | `test_increment3` |
| SR-38 | The system shall place the combined value in a band and accompany it with the contribution of each indicator and the actions it suggests | UR-13 | **C** | Must | 3 | US-18 | `test_increment3` |
| SR-39 | The system shall allow an administrator to alter the indicator weights and the band boundaries, restoring the weights to a unit total and requiring the boundaries to increase strictly | UR-14 | **C**/A | Should | 3 | US-19 | `test_increment3` |
| SR-40 | The system shall determine the purpose of a question posed in ordinary language among a closed set of purposes, and shall recognise when it cannot | UR-15 | **C** | Must | 3 | US-20 | `test_intent_classifier` |
| SR-41 | The system shall gather the records relevant to the determined purpose, confined to the investigations the questioner is assigned to, before any answer is composed | UR-15, UR-03 | **C** | Must | 3, M1 | US-20, US-29 | `test_scoping` |
| SR-42 | The system shall answer from the gathered records alone when no external service is available, stating that it has done so | UR-20 | **C** | Must | 3 | US-20 | `test_nfr`, `test_increment3` |
| SR-43 | The system shall check every identifier and name appearing in an answer against the records gathered, and shall mark any that does not appear | UR-16 | **C** | Must | 3 | US-21 | `test_increment3` |
| SR-44 | The system shall characterise each exhibit by a fixed set of measurements and identify those whose pattern departs markedly from the population | UR-13 | B | Could | 3 | US-22 | `test_increment3` |
| SR-45 | The system shall present such identifications as warranting review and never as findings | UR-13 | B | Could | 3 | US-22 | `test_increment3` |
| SR-46 | The system shall present exhibits ordered by attention level, a view of departures from the norm, and a detailed account for any single exhibit | UR-13 | A | Should | 3 | US-23 | `test_increment3` |
| SR-47 | The system shall allow an account to require a second, independently held factor; shall suspend an account after a stated number of consecutive failures for a stated period | UR-01 | B | Should | 3 | US-24 | `test_increment3`, `test_nfr` |
| SR-48 | The system shall store evidence content, and the private means of establishing authorship, in a form unintelligible without a key held separately from the data | UR-18 | B | Should | 3 | US-25 | `test_increment3` |
| SR-49 | The system shall assemble a complete investigation into a single transferable package carrying the means for a recipient to establish that it is unaltered without access to this system | UR-19 | B | Should | 3 | US-26 | `test_increment3` |
| SR-50 | The system shall render an exhibit's custody history in a form suitable for printing and filing | UR-19 | B | Could | 3 | US-27 | `test_increment3` |
| SR-51 | The system shall compute every total, ranking, chart and export over only the investigations the viewer is assigned to | UR-03 | A | Must | M1 | US-28 | `test_scoping` |
| SR-52 | The system shall compose each role's overview from the elements its work requires, and shall explain the situation rather than show an empty screen when the viewer is assigned to nothing | UR-22, UR-03 | A | Must | M1 | US-28 | `test_scoping`, `test_nfr` |
| SR-53 | The system shall answer questions about the questioner's own identity and assignments from the authenticated session | UR-15 | **C** | Must | M1 | US-29 | `test_intent_classifier` |
| SR-54 | The system shall attribute retained conversation to its owner and discard it both on entry and on departure | UR-03 | A | Must | M1 | US-29 | `test_scoping` |
| SR-55 | The system shall treat removal of an exhibit as a marking that preserves its custody and audit history, and shall omit such exhibits from every listing and total | UR-04 | A | Must | M2 | D1 | `test_integration` |
| SR-56 | The system shall record the outcome of a verification against the exhibit, so that a failed verification raises its attention level | UR-06 | **C** | Must | M2 | D2 | `test_integration` |
| SR-57 | The system shall divide every listing into pages of bounded size | UR-21 | A | Must | M3 | CR-03 | `test_nfr` |
| SR-58 | The system shall examine a custody history in time proportional to its size | UR-21 | **C** | Must | M3 | CR-04 | `test_nfr` |
| SR-59 | The system shall compose four distinguishable overviews, one per function, none of them without content | UR-22 | A | Must | M1, M3 | US-28, CR-05 | `test_nfr` |
| SR-60 | The system shall transmit with every response the directives that constrain where a browser may load content from and how it may frame or interpret the response | UNF-01 | A | Must | M2, M3 | D5, CR-06 | `test_nfr` |
| SR-61 | The system shall refuse to begin serving in a production configuration whose secrets are absent or known-weak, and shall warn when they are weak in development | UNF-01 | A | Must | M2, M3 | D6, CR-07 | `test_nfr` |

## 3.6 Why Some System Requirements Are Negative

Seven system requirements say what the system must make impossible: SR-01
(identical failure messages), SR-06, SR-08, SR-12, SR-19, SR-21, SR-24, SR-33,
SR-45. These are harder to satisfy than positive requirements, because a
positive requirement is met by one correct path while a negative one is met
only when **every** path is correct.

This is not a theoretical observation. Both maintenance iterations of this
project were caused by negative requirements applied to fewer surfaces than
they governed - SR-09 was enforced on record access but not on aggregates, and
SR-55 was enforced in the interface but not in the listing queries. Section
3.10 records the lesson.

## 3.7 System Requirements - Quality

This is the table the first version of the report lacked. Every row carries
the three things a quality requirement needs to be real: **how it is
measured**, **what value constitutes a pass**, and **the test that applies
the measurement**. A quality requirement without all three is an aspiration.

**Table 3.7 - System quality requirements**

| ID | From | Requirement | Measurement | Acceptance criterion | Verified by |
|---|---|---|---|---|---|
| SNF-01 | UNF-01 | No account shall obtain data from an investigation it is not assigned to, by any route | Adversarial request against every aggregate and detail route as each of four roles | Zero records from unassigned investigations in any response | `test_scoping` (14) |
| SNF-02 | UNF-02 | Any difference between stored content and registered content shall be detected | Alter one byte of a stored exhibit, then verify | Verification reports a failure naming the affected element | `test_increment2` |
| SNF-03 | UNF-03 | A custody record's author shall be establishable, and alteration detectable | Verify each record against the author's public means; then alter one field and repeat | Unaltered records verify; altered records fail | `test_increment2` |
| SNF-04 | UNF-04 | The system's history shall admit insertion only | Attempt amendment and removal of an audit record through the data-access layer | Both raise; the record is unchanged | `test_increment1` |
| SNF-05 | UNF-06 | An unavailable external service shall not prevent an answer | Pose a question with no service configured | An answer is returned, drawn from records, and says so | `test_nfr`, `test_increment3` |
| SNF-06 | UNF-06 | A slow external service shall not hold a request open indefinitely | Substitute a service that exceeds its budget | Request completes under 30 s; per-call budget at most the total, total at most 90 s | `test_nfr` |
| SNF-07 | UNF-05 | Examination of a custody history shall grow linearly with its size | Time examination at 20 and 200 elements, best of three | Tenfold size costs under thirtyfold time | `test_nfr` |
| SNF-08 | UNF-05 | Assessment of attention level shall grow linearly with the records considered | Time assessment at 20 and 200 records, best of three | Tenfold records cost under thirtyfold time | `test_nfr` |
| SNF-09 | UNF-05 | Examination of a hundred-element history shall complete within an investigator's tolerance | Time a single examination of 100 elements | Under 5 seconds | `test_nfr` |
| SNF-10 | UNF-05 | No listing shall render in time proportional to the whole collection | Create 45 investigations and 45 exhibits; request each listing | At most 20 rendered per page; navigation present | `test_nfr` |
| SNF-11 | UNF-07 | Business logic shall not depend on the request cycle | Static examination of every logic module's imports | No module imports request, session, redirect, url_for, render_template, flash or abort | `test_nfr` |
| SNF-12 | UNF-07 | Business logic shall not depend on the interface layer | Static examination for route imports | No logic module imports from the routes package | `test_nfr` |
| SNF-13 | UNF-08 | No database-product-specific construct shall appear in logic, models or routes | Static examination for dialect keywords | No occurrence of PRAGMA, AUTOINCREMENT, sqlite_master or SERIAL | `test_nfr` |
| SNF-14 | UNF-08 | Values written to constrained columns shall lie within the declared domain | Assess an exhibit, persist, compare against the column's declared values | Persisted value is within the declared set | `test_nfr` |
| SNF-15 | UNF-01 | The session token shall be unreadable by page scripts, sent only over a protected transport, and resistant to cross-origin submission | Inspect effective configuration | Script-inaccessible, transport-restricted, and same-site constrained | `test_nfr` |
| SNF-16 | UNF-01 | Every response shall carry directives restricting content origin, framing, interpretation and referrer disclosure | Request an unauthenticated and an authenticated page; inspect response directives | All four present on both; content origin defaults to the application's own | `test_nfr` |
| SNF-17 | UNF-01 | Text originating outside the system shall never be interpreted as markup | Store markup in an investigation title and in a conversation; render both | Markup appears escaped; no element boundary can be closed by stored text | `test_nfr` |
| SNF-18 | UNF-01 | A production configuration with an absent or known-weak secret shall not start | Apply validation to absent, weak and sound configurations | Absent raises; weak raises; sound passes | `test_nfr` |
| SNF-19 | UNF-01 | Authentication secrets shall meet a stated minimum strength, and repeated failure shall suspend the account | Inspect effective policy | Minimum length at least 12; suspension at no more than 5 failures for at least 15 minutes | `test_nfr` |
| SNF-20 | UNF-09 | The whole verification suite shall run without reaching any external service | Execute the suite with no network configuration | All tests pass; no external call attempted | Suite execution |
| SNF-21 | UNF-09 | Each role's overview shall be distinguishable from every other | Render the overview as each of four roles and compare | Four distinct renderings; administrative panels absent from the other three | `test_nfr` |

**Coverage.** Every one of the twenty-one system quality requirements names a
test. Section 3.11 records what this table looked like before the revision and
why the difference matters.

## 3.8 Domain Requirements

Constraints arising from the forensic domain rather than from any stakeholder's
wish. They are separated because they are not negotiable and not traded off.

**Table 3.8 - Domain requirements**

| ID | Constraint | Consequence if violated |
|---|---|---|
| DR-01 | An exhibit's custody history must begin at the moment of collection | The chain has no established origin and the exhibit is inadmissible |
| DR-02 | No gap in custody may be silently closed | A reconstruction presented as fact misleads the court |
| DR-03 | The record of handling must outlive the exhibit's deletion | Deleting an exhibit would erase the evidence of its own mishandling |
| DR-04 | Closure of an investigation must not destroy its contents | Later challenge cannot be answered |
| DR-05 | A person must not both perform an act and be the sole attestor to it | Attribution becomes unverifiable |
| DR-06 | An exhibit whose integrity has failed must not re-enter normal handling unnoticed | Compromised material is treated as sound |
| DR-07 | An inference must be visibly distinguishable from an observation | The distinction between evidence and supposition collapses |

## 3.9 Traceability

The chain is complete in both directions and is carried inline rather than in
an appendix, so that a reader checking any single requirement need not turn
pages. Its six links are: a **user requirement** is derived into one or more
**system requirements**; each system requirement is carried by a **user
story**; each user story is scheduled into a **sprint**; each sprint
implements it in a **module**; and each module is verified by a named
**test**. The relationships between these artefacts are modelled formally as a
UML class diagram in Figure 3.1, so that the traceability structure is itself
expressed in the notation the rest of the report uses.

**Table 3.9 - Coverage**

| Check | Result |
|---|---|
| User requirements realised by at least one system requirement | 22 of 22 |
| System functional requirements traced to a user requirement | 61 of 61 |
| System functional requirements carried by a user story | 61 of 61 |
| System quality requirements with a measurement and acceptance criterion | 21 of 21 |
| System quality requirements with a named automated test | 21 of 21 |
| Requirements naming a technology rather than a problem | 0 |

## 3.10 What the Requirements Process Got Wrong

Two failures are recorded here because the report's account of its own process
is worth more than a claim of having had none.

**Negative requirements were scoped to the surfaces their author had in mind.**
UR-03 and SNF-01 were stated correctly from the start, but the system
requirements realising them addressed record access alone. Aggregates -
counts, charts, rankings, exports, generated answers - were not enumerated, and
so were not protected. The requirement was right; its scope of application was
incomplete. SR-51 exists because of this, and the maintenance iteration M1 is
its consequence. **A negative requirement must enumerate the surfaces it
governs, or it will be applied only to those its author pictured.**

**Quality requirements were stated without the means to check them.** The first
version of Table 3.7 gave each quality requirement a property and a sentence
of justification, but nine of eighteen named only "code review", "configuration
inspection", "manual check" or an analytical argument as their verification. A
verification method that does not re-run cannot fail, and a requirement that
cannot fail is not a requirement. The most pointed instance: the requirement
that untrusted text never be rendered as markup (now SNF-17) arose from a
defect found and fixed in maintenance iteration M2 - and was given no test, so
the fix could have been removed without a single failure anywhere in the suite.
**A fixed defect without a regression test is an unfixed defect with a delay
built in.**

Both failures share a shape: the requirement was correct and the verification
was not. This is why Section 3.7 now treats the measurement and the acceptance
criterion as part of the requirement rather than as commentary on it.

---

\newpage
