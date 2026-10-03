# Chapter 16 - Feature Categorisation Self-Assessment

---

## 16.1 The Requirement and the Method

The coursework requires that the system's functionality be categorised into three kinds - data/repository, third-party services, and complex application logic - that the proposal be **balanced** across them, and that the reasoning be made explicit. This chapter audits the delivered system against that requirement.

The method, applied from the proposal onward, was to assign each feature to exactly one category **on the basis of where its essential difficulty lies**. Three tests were applied, restated here from Section 7.10 because the audit that follows depends on them.

**Table 16.1 - The categorisation tests**

| Category | Test applied |
|---|---|
| **A - data / repository** | Could this be expressed as a query plus a simple arithmetic or set operation? |
| **B - third-party services** | Is the interesting work done by someone else's code? |
| **C - complex application logic** | Would removing the third-party calls still leave a substantial algorithm? |

This chapter is written as a **self-critical audit** rather than a summary. The useful question is not *"did the project produce features in all three categories?"* - that is trivially satisfiable by labelling - but *"does the categorisation describe where the difficulty actually lies, and would it survive someone reading the code?"*

## 16.2 Category A - Data and Repository Functionality

**Table 16.2 - Category A features**

| Feature | What makes it Category A | Where documented |
|---|---|---|
| Six-entity relational model with full CRUD | Structured records, relationships, constraints; no application-level algorithm | §10.2, Fig. 8.3 |
| Case search, filtering and soft archive | Query plus a boolean flag | §10.4.1 |
| Case-level access membership | An associative table plus a set lookup | §10.3.3 |
| Append-only audit trail | Insert-only persistence with ORM-level enforcement | §10.5.2 |
| Custody time-gap check | Arithmetic over consecutive timestamps against a threshold | §10.5.3 |
| Duplicate-entry check | A grouping query over three fields | §10.5.3 |
| Role-permission mismatch check | A set-membership test against a permission matrix | §10.5.3 |
| Role-scoped aggregates and role-tailored dashboards | Filtered queries and per-role panel composition | §10.7.1 |
| Integrity and reconstruction report pages | Rendering a structured result produced elsewhere | §5.2.2 |
| Soft deletion | A boolean flag plus listing filters | §5.5.2 |

This is a **substantial data layer rather than a token one**. The six entities and their relationships encode real domain rules - the `1..*` custody multiplicity, the non-nullable signature, the associative access table - and the append-only enforcement and the three formula checks are genuine data-oriented engineering rather than bare CRUD.

The three formula checks are worth a note, because they are the clearest examples of the category's "formulae" clause: each is a direct computation over database fields, and none involves a data structure or a branching algorithm. Calling them Category A rather than C is straightforwardly correct, and it matters that the report does so, because they are the features it would be most tempting to inflate.

## 16.3 Category B - Third-Party Services

**Table 16.3 - Category B features, with the boundary stated**

| Service | Library / provider | What the third party does | What DEICMS does around it |
|---|---|---|---|
| SHA-256 hashing | `hashlib` | The hash function | When to hash, what the hash means, how it is compared |
| Ed25519 signatures | `cryptography` | Key generation, signing, verification | **The canonical payload definition** (§10.6.1) |
| AES-256-GCM encryption | `cryptography` | Authenticated encryption | Key derivation policy; hashing before encryption |
| Fernet key protection | `cryptography` | Authenticated symmetric encryption | Deriving the key from the application secret |
| EXIF extraction | Pillow | Parsing image metadata | Which fields to retain and how to store them |
| Magic-byte MIME detection | python-magic | Identifying true content type | The MIME-to-extension policy and the rejection rule |
| Object-relational mapping | SQLAlchemy | Query construction, session management, event system | The six-entity model and the append-only listeners |
| Large language model | NVIDIA NIM (hosted) | Natural-language generation | **Five of six pipeline stages** (§11.6) |
| Isolation Forest | scikit-learn | The anomaly-detection algorithm | The six-dimensional feature vector and the output framing |
| PDF generation | ReportLab | Document layout and rendering | Content selection; running a fresh verification at generation time |
| TOTP two-factor | PyOTP | Code generation and validation | Enrolment flow and login integration |

Eleven integrations, spanning cryptography, imaging, content inspection, persistence, machine learning, natural language, document generation and authentication. This is **numerous and varied rather than a single decorative API call**, and the third column of the table is what keeps the claim honest: in each case the report states what the library provides so that the fourth column can be read as the project's contribution rather than as the whole story.

## 16.4 Category C - Complex Application Logic

**Table 16.4 - Category C features against the test**

| Feature | Third-party calls made | Would a substantial algorithm remain without them? | Points |
|---|---|---|---|
| Graph integrity verification | `hashlib`, Ed25519 verify | **Yes** - graph construction, DFS traversal, three-condition validation, single-pass failure accumulation, completeness scoring | 13 |
| Multi-factor risk scoring | **None** | Nothing to remove | 8 |
| Custody chain reconstruction | **None** | Nothing to remove | 8 |
| Evidence lifecycle state machine | **None** | Nothing to remove | 8 |
| AI orchestration + hallucination detection | One HTTP call | **Yes** - five of six stages remain | 8 + 3 |

Each involves a custom data structure, a multi-step algorithm with branching logic, or a heuristic search that cannot be reduced to a query, a formula or a library call. Each was given an algorithmic account in Chapter 11 - data structure, pseudocode, design decisions and complexity - sufficient to **demonstrate** that complexity rather than merely assert it.

A useful additional test of whether a complex-logic claim is real is to ask whether the feature **could have been bought**. For all five the answer is no: there is no library that verifies a bespoke custody graph against this schema, scores risk against these eight factors and five interaction rules, reconstructs gaps with this four-criterion plausibility model, enforces this particular lifecycle with these role guards and preconditions, or orchestrates a language model against this access-scoped context with this entity-level hallucination check.

## 16.5 Balance Assessment

**Table 16.5 - Distribution of delivered work across the categories**

| Measure | Category A | Category B | Category C |
|---|---|---|---|
| Distinct features / integrations | 10 feature groups | 11 integrations | 5 algorithms |
| User stories primarily in this category | 13 | 8 | 6 (plus 2 hybrid) |
| Story points | 43 | 24 | 51 |
| Share of total points (of 130, excluding M1's 10) | 36% | 20% | **44%** |
| Report chapters principally devoted to it | 10 (§10.2-10.5, 10.7) | 15 | 11 |

The point distribution is the most informative row. Category C carries the largest share at 44%, which is appropriate - the complex logic is where the engineering demonstration lies - but it does not dominate: Category A carries 36% and Category B 20%. **No single category carries the system.** The data layer is not a thin veneer over the algorithms; the third-party integrations are not a single API call; and the complex-logic layer is not one algorithm padded out with claims.

### 16.5.1 Integration Between Categories

The most persuasive evidence that the categorisation was approached with rigour rather than as a labelling exercise is the deliberate **integration across categories**.

**Table 16.6 - Cross-category integrations**

| Integration | Direction | Effect |
|---|---|---|
| Duplicate-entry and role-mismatch formula checks feed the risk scorer | **A → C** | Two simple Category A computations become inputs to the complex Category C algorithm, weighted 0.10 and 0.12 |
| The graph verifier writes `integrity_status`, which the risk scorer reads | **C → A → C** | A failed verification genuinely raises an item's risk, through a persisted Category A column |
| The state machine triggers a risk recalculation | **C → C** | Lifecycle state is itself a scoring factor, so the two algorithms are coupled by data |
| The PDF report runs a fresh verification at generation time | **B ← C** | A Category B document carries a live Category C result rather than a cached one |
| The signed export's manifest is verifiable without the system | **C → B** | Category C integrity work gives the Category B serialisation its meaning |

The first two of these were not necessary to make either category "count" - each stood on its own - but they produce a system in which **the categories reinforce rather than merely coexist**, which is a stronger design than three isolated silos and is exactly the relationship the categorisation exercise is meant to encourage.

It is worth recording that both of the first two integrations were **broken when originally written** and were repaired in M2 as findings D5 and D2 (Table 5.9). Before that repair, the two formula factors counted the wrong audit events - so running a verification perversely *raised* an item's risk - and the integrity factor read a column that did not exist. The integration described above is therefore a claim about the delivered system, not about the system as first written, and Chapter 14 treats the distinction.

## 16.6 Where the Categories Were Kept Honest

A categorisation that never declines to claim complexity is not a categorisation at all. This section records the places where the temptation to inflate was consciously resisted, because that restraint is what makes the Category C claims credible.

**Table 16.7 - Claims deliberately not made**

| Feature | Could have been claimed as | Actually classified as | Why the restraint is correct |
|---|---|---|---|
| Isolation Forest anomaly detection | C - "a machine-learning risk pipeline" | **B** | The feature engineering is the project's; the algorithm that does the interesting part is scikit-learn's |
| Ed25519 signing | C - "a cryptographic non-repudiation system" | **B**, with the canonical payload noted as the project's design | The project implements no cryptography; only the payload definition is its own |
| The language model | C - "an AI system" | **B**, with the orchestration claimed as C | The model is not the project's. The pipeline around it is |
| Sequential case and evidence numbering | C - "a collision-resistant identifier scheme" | **A** | It is a count plus a format string, and it is described as such |
| The role predicates | C - "an authorisation engine" | **A** | Three boolean methods over a nested role hierarchy |
| The dashboards | C - "an analytics layer" | **A** | Filtered queries rendered into panels |

Two further points of restraint deserve statement.

**Where a Category C feature calls a Category B library, the report says so.** The graph verifier calls `hashlib` and Ed25519 verification; the assistant calls a hosted model. These libraries play the role of **primitive operations inside an algorithm the project designed**, in the same way that arithmetic operators sit inside a formula. The report does not claim to have implemented SHA-256 or Ed25519, and Table 16.4's second column exists precisely so that a reader can check the claim rather than take it.

**Where behaviour turned out to be simpler than a complex-logic claim would require, it was described as what it is.** The clearest case is the numbering scheme, which is a count plus a format string with an acknowledged weakness under concurrency - and is described that way in Section 10.4.1 rather than dressed up.

### 16.6.1 One Honest Qualification About the Method

Section 7.3 recorded that the categorisation was used as a **completeness check during elicitation**: the requirement set was reviewed against the three categories and gaps were visible as under-populated ones. This is an unusual elicitation route and it raises a fair question - did the categorisation requirement distort the system?

The assessment is that it shaped **emphasis** but not **substance**, and the evidence is the counterfactual. Every Category C feature answers a genuine need stated in the five guarantees of Table 1.1: G1 requires full-chain verification, G4 requires an enforced lifecycle, G5 requires analytical prioritisation. None was invented to fill a category. The features most exposed to the charge of being category-driven are the two *Could-have* stories - the Isolation Forest and the PDF report - and both were classified as Category B, where the pressure to invent was lowest.

Where the requirement did have an effect is in **depth rather than existence**: the risk scorer has eight factors and five interaction rules rather than three factors and none, and the reconstruction algorithm scores four criteria rather than one. A project without a complex-logic requirement would plausibly have built simpler versions of the same features. That is a real influence and it is stated rather than denied - but it is influence on how thoroughly a genuine need was met, not on whether the need existed.

## 16.7 Summary

This chapter audited the delivered system against the coursework's categorisation requirement. Ten Category A feature groups were catalogued, with the three formula checks identified as the clearest instances of the category's "formulae" clause and deliberately not inflated. Eleven Category B integrations were listed with an explicit statement, for each, of what the third party provides and what the project supplies around it. Five Category C algorithms were tested against the question of what would remain if their third-party calls were removed - with three of the five making no third-party calls at all - and against the further test of whether the feature could have been bought, which none could.

The balance was assessed quantitatively: 36% of story points in Category A, 20% in B and 44% in C, with no category carrying the system. Five cross-category integrations were documented, two of which were broken when first written and repaired in M2 - a fact recorded rather than elided.

Finally, six claims the project could have made and deliberately did not were listed, together with an honest qualification about the elicitation method: the categorisation requirement shaped how thoroughly genuine needs were met, not whether those needs existed. A categorisation is only worth as much as its willingness to decline, and the value of this one is that it draws the line where the code actually draws it.

---

\newpage
