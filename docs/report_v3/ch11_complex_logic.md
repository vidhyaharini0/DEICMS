# Chapter 11 - Complex Custom Logic

---

This chapter exists because the project guidelines require the
algorithmically complex features to be identified, justified as such, and
described algorithmically. Each of the five is given its own numbered section
below, and each is described by UML behavioural diagrams rather than by prose
alone. They are gathered here, rather than left scattered through the sprint
chapters, so that the Category C contribution of the project can be read in
one place; Sprints 2 and 3 (Chapters 7 and 8) record *when* each was built and
what it cost.

## 11.1 What Makes a Feature Category C

The three feature categories are easy to assign loosely and hard to assign
honestly. A feature that calls a cryptographic library is not complex because
cryptography is complex. The question is what the project itself contributes.

**Table 11.1 - The test applied to every feature**

| Question | If yes | Category |
|---|---|---|
| Is the behaviour obtained by storing, retrieving or arithmetically combining records? | Then the complexity is in the data model | **A** |
| Is the behaviour obtained by calling a library or service that implements it? | Then the complexity belongs to that library | **B** |
| Does the behaviour require a data structure, a multi-step control flow, or a search that the project designs and implements? | Then the complexity is the project's own | **C** |

A feature may call Category B components from inside Category C logic without
changing category, **provided the library calls play the part of primitive
operations inside a larger algorithm the project designed**. The hash function
inside the integrity verifier is used exactly as an arithmetic operator is
used: it is not the algorithm, it is a step in it.

The converse test is the stricter one, and this report applies it: *if the
library were replaced by an equivalent, would anything the project designed
have to change?* For the verifier, no - the traversal, the failure
accumulation and the completeness score are untouched by which hash function
is used. For the anomaly detector, yes - the whole behaviour would change,
which is why anomaly detection is classified **B** and not C despite feeding
the same dashboard.

**Table 11.2 - The five Category C features**

| # | Algorithm | Structure it builds | Why not A | Why not B |
|---|---|---|---|---|
| 1 | Chain integrity verification | Directed acyclic graph of custody events | No query returns "where and how is this chain unsound" | No library verifies a custody chain |
| 2 | Multi-factor risk assessment | Weighted, normalised, interaction-amplified score | A weighted sum is arithmetic; the normalisation choice, the interaction model and the cap are not | No library models this domain |
| 3 | Custody chain reconstruction | Heuristic best-first search over candidate records | There is no correct answer to query for | No library infers missing custody |
| 4 | Evidence lifecycle state machine | Transition table with guards and preconditions | A status column is data; a role-gated, precondition-constrained automaton is not | No library knows this domain's procedure |
| 5 | Assistant orchestration | Six-stage pipeline around a model call | Retrieval is queries, but the pipeline is not | **The model is B; the pipeline around it is C** |

Feature 5 is the one most at risk of being over-claimed, so it is stated
plainly: **the language model is a third-party service and is categorised B in
Chapter 10.** What is C is the intent classification, the access-scoped
retrieval, the template selection, the fallback path and the reference
validation - none of which the model provides and all of which would still be
needed if the model were replaced.

---

## 11.2 Algorithm 1 - Chain Integrity Verification

*Delivered in Sprint 2 as US-13 (13 points, the largest item in the backlog).
Realises SR-25, SR-26, SR-27.*

### 11.2.1 The problem

Given an evidence item, establish whether its custody history is sound, and
where it is not. A check of the most recent record is insufficient: tampering
anywhere in the chain invalidates everything after it, and a forensic user
needs to know **which** event failed and **how**, not merely that something
did.

### 11.2.2 The structure

Custody events are loaded, ordered by time, and built into a **directed
acyclic graph** rooted at the registration event. Each node carries the event
and the fingerprint recorded at that moment; each edge connects a predecessor
to its successor.

The graph is the design decision that makes the rest possible. A flat list
would support a sequential scan but not the predecessor relation that the
order check needs, nor the branching that concurrent access events produce.

### 11.2.3 The algorithm

Described by **Figure 23** (activity diagram), **Figure 12** (sequence
diagram) and **Figure 10** (composite structure of the engine).

The traversal is depth-first from the root. At each unvisited node three
**independent** checks are applied:

| Check | Question | Failure means |
|---|---|---|
| Content | Does the stored content still produce the fingerprint registered at intake? | The content has been altered |
| Authorship | Does the record's signature verify against the signer's public key? | The record has been altered or forged |
| Order | Is this event strictly later than its predecessor? | The sequence has been manipulated |

After the checks, every child is pushed **regardless of the outcome**.

### 11.2.4 The design decision that defines the algorithm

The first implementation stopped at the first failure. It satisfied a naive
reading of the user story and violated its second acceptance criterion.

**Stopping at the first failure gives a user one defect at a time and
guarantees as many verification runs as there are defects.** Worse, in a
forensic setting it actively misleads: an investigator told "the chain failed
at event 3" may reasonably conclude events 4 onward are sound.

Accumulating instead costs nothing asymptotically - the traversal visits every
node either way - and converts the output from a single error into a complete
picture. This is why **Figure 10** is worth attention: the failure collector
sits between the checks and the scorer, and **no connector routes a failure
back to the walker**. The absence of that connector is the property.

### 11.2.5 Pseudocode

```
VERIFY(item):
    logs <- custody records of item ordered by time
    if logs is empty: return (Broken, 0, [], [])

    root <- the registration event
    graph <- BUILD_DAG(logs)
    stack <- [root]; visited <- {}; failures <- []; verified <- 0

    while stack not empty:
        node <- pop(stack)
        if node in visited: continue
        visited <- visited + {node}

        ok <- TRUE
        if not CHECK_CONTENT(node):    failures += (node, Content);    ok <- FALSE
        if not CHECK_AUTHORSHIP(node): failures += (node, Authorship); ok <- FALSE
        if not CHECK_ORDER(node, predecessor(node)):
                                       failures += (node, Order);      ok <- FALSE
        if ok: verified <- verified + 1

        for child in children(node):          // pushed whether or not ok
            push(stack, child)

    completeness <- 100 * verified / |logs|   // a percentage
    verdict <- Intact            if failures is empty
               Broken            if verified = 0
               Partially Verified otherwise
    return (verdict, completeness, failures, verified timeline)
```

### 11.2.6 Complexity

Let *V* be custody events, *E* the edges between them, and *F* the size of the
stored content. The traversal is **O(V + E)**; each node additionally
recomputes a fingerprint over the content, which is **O(F)**. The honest total
is therefore **O(V·F + E)**, dominated in practice by the content reads, not
by the graph work. Section 11.8 records how this was measured rather than
assumed.

### 11.2.7 Verification

`test_increment2` covers a clean chain, an altered content case, a forged
signature case, an out-of-order case, and the case that matters most: a chain
with **three** separate failures, asserting that all three appear in one run.
`test_nfr::TestPerformanceScaling` measures the growth claim above.

---

## 11.3 Algorithm 2 - Multi-Factor Risk Assessment

*Delivered in Sprint 3 as US-18 (8 points). Realises SR-36, SR-37, SR-38.*

### 11.3.1 The problem

Rank evidence items by how much attention they need, so an investigator with
a caseload need not read every record. A single rule ("more than five
transfers") misses that signals interact: an item with many transfers **and** a
failed integrity check **and** role mismatches is far more alarming than the
sum of those three considered separately.

### 11.3.2 Eight indicators, and why each is normalised differently

**Table 11.3 - Indicators and weights (summing to 1.0)**

| Indicator | Weight | Normalisation | Why that curve |
|---|---|---|---|
| Integrity outcome | **0.25** | Direct mapping | A verified failure is the strongest single signal available |
| Handover frequency | 0.13 | Logarithmic | The step from 1 to 3 transfers means far more than 21 to 23 |
| Content kind | 0.12 | Table lookup | An executable is categorically riskier than a photograph |
| Function mismatches | 0.12 | Linear | Each mismatch is an equally serious procedural breach |
| Distinct handlers | 0.10 | Logarithmic | Same saturation argument as handovers |
| Repeated records | 0.10 | Linear | Each duplicate is equally suspicious |
| Lifecycle state | 0.10 | Ordinal mapping | Flagged 1.0 down to Archived 0.1 |
| Dormancy | 0.08 | Sigmoid | Risk is flat, then rises sharply around a threshold, then flattens |

**The normalisation choice per indicator is a substantive design decision, not
a formality.** Applying one curve to all eight would misrepresent at least
three of them: a linear curve on handover frequency would let a busy item
dominate the ranking purely by being busy, and a logarithmic curve on function
mismatches would make the second breach count for less than the first, which
is the opposite of the truth.

### 11.3.3 Interaction rules and the cap

Five ordered pairs are checked. Each fires when **both** of its indicators
exceed their own thresholds, contributing a multiplier:

| Pair | Thresholds | Multiplier | Reading |
|---|---|---|---|
| Integrity failure + function mismatch | 0.6, 0.6 | 1.30 | Deliberate tampering |
| Handover frequency + integrity failure | 0.7, 0.5 | 1.25 | Custody breach |
| Content kind + repeated records | 0.7, 0.5 | 1.20 | Suspicious duplication |
| Distinct handlers + handover frequency | 0.6, 0.6 | 1.20 | Unstable chain |
| Function mismatch + repeated records | 0.5, 0.5 | 1.15 | Administrative tampering |

The total bonus is capped at **0.30**. The cap is the second decision worth
defending: without it, an item firing four rules saturates at the maximum and
becomes indistinguishable from an item firing all five. **A ranking in which
everything alarming scores the same is not a ranking** - which is exactly the
failure the feature exists to prevent.

### 11.3.4 The algorithm

Described by **Figure 17** (activity diagram) and **Figure 14**
(communication diagram). The communication view is included deliberately: it
shows *which objects collaborate*, which is the aspect a sequence diagram
de-emphasises.

```
SCORE(item):
    logs <- custody records of item
    for each indicator i in the eight:
        raw_i        <- EXTRACT(item, logs, i)
        normalised_i <- NORMALISE(raw_i, curve(i))      // linear | log | sigmoid | lookup
    base <- sum over i of weight(i) * normalised_i

    bonus <- 0
    for (a, b, ta, tb, m, reason) in the five rules:
        if normalised_a >= ta and normalised_b >= tb:
            bonus <- bonus + (m - 1) * base
            record (a, b, reason)
    bonus <- min(bonus, 0.30)

    final <- base + bonus
    level <- LOW if final < 0.25
             MEDIUM if final < 0.50
             HIGH if final < 0.75
             CRITICAL otherwise
    return (final, level, per-indicator contributions, rules fired, recommendations)
```

### 11.3.5 Explainability as a requirement, not a nicety

The algorithm returns every indicator with its raw value, its normalised
value, its weight and its contribution, plus the reason text of every rule
that fired. SR-38 requires this. In a forensic setting a number an
investigator cannot interrogate is a number they cannot defend in court, so
the explanation is part of the output rather than a debugging aid.

### 11.3.6 Complexity and verification

Extraction is **O(n)** in the custody records; the weighted sum is O(8) and
the rules O(5), both constant. The whole assessment is therefore **O(n)**.
`test_increment3` covers each indicator independently, the weight
re-normalisation, each interaction rule, and specifically the cap.
`test_nfr::TestPerformanceScaling` measures the linear claim.

---

## 11.4 Algorithm 3 - Custody Chain Reconstruction

*Delivered in Sprint 2 as US-15 (8 points). Realises SR-31, SR-32, SR-33.*

### 11.4.1 The problem

When custody records are missing, offer the most plausible account of what
happened - **without ever presenting a reconstruction as a fact**. This is a
heuristic search: there is no correct answer to retrieve, only candidates to
evaluate.

### 11.4.2 The algorithm

Described by **Figure 18** (activity diagram) and **Figure 25** (sequence
diagram).

Discontinuities are detected where a holder changes with no handover between.
For each, candidate records are drawn from the access log within the gap's
time window, and each candidate is scored on four criteria:

| Criterion | Question |
|---|---|
| Temporal proximity | How near the middle of the gap does it fall? |
| Function consistency | Was this account entitled to hold this kind of exhibit? |
| Place consistency | Is the location plausible given the surrounding records? |
| Behavioural consistency | Did this account interact with the investigation around that time? |

The criteria are averaged with **equal weight over the criteria that have data**.
A criterion with nothing to judge is omitted from the average rather than
scored at a neutral 0.5, because diluting every candidate toward the middle
would flatten exactly the discrimination the search depends on.

### 11.4.3 The threshold, and declining to answer

If the best candidate scores below **0.40**, the gap is marked **Unresolved**
and no inference is made.

**Declining is a result, not a failure.** DR-02 forbids silently closing a gap,
and DR-07 requires an inference to be visibly distinguishable from an
observation. Every link in the output carries one of three labels -
**Confirmed**, **Inferred**, **Unresolved** - and an inferred link carries its
score and the reasoning that produced it. An algorithm that always produces a
complete chain would be more satisfying and less honest.

### 11.4.4 Complexity and verification

With *g* discontinuities and at most *c* candidates each, scoring is
**O(g·c)**, and candidate generation costs one query per gap. `test_increment2`
covers a complete chain (no gaps), a resolvable gap, a gap with no candidate,
and a gap whose best candidate falls below the threshold - the case that
asserts the algorithm declines rather than guesses. Coverage of this module is
65%, the lowest in the project, because the combinations of partially-present
criteria are numerous; this is recorded as a known limitation rather than
presented as complete.

---

## 11.5 Algorithm 4 - Evidence Lifecycle State Machine

*Delivered in Sprint 2 as US-14 (8 points). Realises SR-28, SR-29, SR-30.*

### 11.5.1 The problem

Evidence must pass only through the transitions its procedure permits, at the
hands of someone entitled to make them, and only when the conditions for that
transition hold.

### 11.5.2 Policy as data

The lifecycle is declared as a **transition table**: six states, fourteen
permitted transitions, each mapping an ordered pair of states to the functions
entitled to make it and the preconditions that must hold.

Expressing the policy as data rather than as branching code has three
consequences that matter: the whole policy is auditable in one place; adding a
transition is a data change rather than a code change; and the policy can be
rendered directly as **Figure 15** (state machine diagram) without a human
transcribing it, so the diagram cannot drift from the behaviour.

### 11.5.3 The validation pipeline

Described by **Figure 24** (activity diagram). Four gates in order: the pair
must exist in the table; the requesting account's function must be among those
permitted; every precondition must hold; a justification must be supplied.

A rejection names **the exact condition unmet** - not a generic refusal - and
is written to the audit trail. SR-29 requires this because a rejected attempt
is forensically interesting: someone tried to archive an item whose integrity
was never verified, and that attempt is part of the record.

### 11.5.4 Flagged, and the asymmetry that matters

`Flagged` is reachable from **every** state and escapable from **one**, by an
administrator alone, and only after re-verification. The asymmetry is
deliberate and realises DR-06: an item whose integrity has failed must not
quietly resume normal handling.

One subtlety is worth stating because it looks like an inconsistency. When
verification finds a broken chain it drives the item to `Flagged` with the
role check bypassed, so that an Analyst who runs a check still gets the item
flagged. That bypass is why running a verification is **not** a read, and why
it is refused to a Read-Only Viewer (Section 11.9).

### 11.5.5 Complexity and verification

Table lookup is **O(1)**; precondition evaluation is **O(p)** with *p* at most
two. `test_increment2` covers every permitted transition, a representative
forbidden pair, a function-denied attempt, a precondition-denied attempt, and
asserts that each rejection is audited.

---

## 11.6 Algorithm 5 - Assistant Orchestration

*Delivered in Sprint 3 as US-20 and US-21 (11 points), extended in Sprint 4 as
US-29. Realises SR-40 to SR-43 and SR-53.*

### 11.6.1 Where the third-party boundary falls

**The language model is a third-party service (Category B).** The six-stage
pipeline around it is this project's work, and the test in Section 11.1
applies cleanly: replacing the model would change none of the six stages.

The accepted project proposal named a particular commercial model API. That
service proved unavailable on terms the project could meet, and a different
hosted model was substituted. **The substitution required no change to the
pipeline, to any requirement, or to any test** - which is the practical
demonstration that the boundary is drawn where this section claims.

### 11.6.2 The six stages

Described by **Figure 26** (activity diagram), **Figure 13** (sequence
diagram) and **Figure 20** (timing diagram).

| Stage | What it does | Whose work |
|---|---|---|
| 1. Intent classification | Matches the question against keyword sets for seven intents, breaking ties by fixed priority; parses any identifier; falls back to UNKNOWN | **C** |
| 2. Access scoping | Determines which investigations this account may see | **C** |
| 3. Context retrieval | Runs the query sequence for the intent, restricted to those investigations; an integrity question triggers a **fresh run of Algorithm 1** | **C** |
| 4. Prompt construction | Selects the template for the intent and assembles role, question and serialised context | **C** |
| 5. Model invocation | Calls the model within a per-call budget, falling through candidates, then to a context-only answer | B inside, **C** around |
| 6. Reference validation | Extracts every identifier and name from the reply and checks each against the retrieved context | **C** |

### 11.6.3 Scoping before retrieval, not after

Stage 2 precedes stage 3, which precedes stage 4. **Data the account may not
see never enters the prompt.** The refusal is therefore structural rather than
conversational: no phrasing of a question can extract what was never placed in
front of the model.

This ordering was not present in the first implementation. The assistant
retrieved globally and relied on the answer not mentioning inaccessible cases
- a defect found by adversarial testing and repaired in Sprint 4 as US-29.
Section 11.9 and Chapter 9 record it.

### 11.6.4 Hallucination detection, and what it does not do

Stage 6 extracts every case number, evidence identifier and personal name from
the reply and checks each against the retrieved context. Anything absent is
attached to the answer as an explicit warning.

**The limitation must be stated as plainly as the capability: this verifies
references, not reasoning.** A reply that cites only real identifiers but draws
a wrong conclusion from them passes the check. The interface presents the
answer accordingly - as a drafted reading of records the investigator can see,
not as a finding.

### 11.6.5 Bounded waiting

**Figure 20** shows the timing. A per-call budget bounds any single attempt; a
total budget bounds the whole stage and sits below the browser's abort, so a
slow service produces a clear message rather than a cancelled request. When the
budget is exhausted the pipeline composes an answer from the retrieved records
alone and says that it has done so - a degraded answer, visibly degraded.

### 11.6.6 Complexity and verification

Classification is **O(k)** in keywords; retrieval **O(r)** in records;
validation **O(m)** in references. `test_intent_classifier` covers all seven
intents plus UNKNOWN and the tie-breaking order; `test_scoping` covers the
access boundary; `test_nfr::TestRobustness` covers both the unavailable and
the slow service.

---

## 11.7 Third-Party Components Used Inside Category C Logic

Stated explicitly so the boundary cannot be read as a claim.

**Table 11.4 - What is borrowed, and what is ours**

| Algorithm | Third-party component used | Role it plays | Would replacing it change our design? |
|---|---|---|---|
| 1. Integrity | Hash function; signature verification | Primitive operations at a node | **No** |
| 2. Risk | None | - | - |
| 3. Reconstruction | None | - | - |
| 4. State machine | None | - | - |
| 5. Assistant | Hosted language model | Produces the natural-language sentence at stage 5 | **No** - and this was demonstrated, not asserted (§11.6.1) |
| (Anomaly detection) | Isolation Forest implementation | **Is the algorithm** | **Yes** - therefore classified **B**, not C |

The last row is the control case. Anomaly detection feeds the same dashboard
as Algorithm 2 and could have been presented as a sixth complex feature. It is
not, because the library implements the behaviour and the project supplies
only the feature vector. **A categorisation that never excludes anything is not
a categorisation.**

## 11.8 Complexity, Measured Rather Than Argued

The complexity claims above were originally supported by analysis alone. An
analytical argument cannot regress, so each is now also measured.

**Table 11.5 - Claims and how they are checked**

| Claim | Measurement | Acceptance criterion | Test |
|---|---|---|---|
| Verification grows linearly in chain size | Time 20-element and 200-element chains, best of three | Tenfold size under thirtyfold time | `TestPerformanceScaling` |
| Risk assessment grows linearly in records | Same method | Tenfold records under thirtyfold time | `TestPerformanceScaling` |
| A 100-element chain verifies within tolerance | Single run, 100 elements | Under 5 seconds | `TestPerformanceScaling` |

A quadratic implementation would need roughly a hundredfold increase and would
fail these tests, which is the point: the thresholds are set to catch a change
in the *shape* of the cost, not to certify a particular machine's speed.

## 11.9 What the Algorithms Got Wrong

Three defects in this chapter's subject matter were found after acceptance.
Each is recorded here with its root cause, because the pattern across them is
more instructive than any one of them.

**Table 11.6 - Defects in the complex logic**

| Found in | Defect | Root cause | Repair |
|---|---|---|---|
| Sprint 4 (M1) | The assistant retrieved globally and relied on the answer not mentioning inaccessible records | Scoping treated as a property of the *answer* rather than of the *retrieval* | Stage 2 inserted before stage 3 (§11.6.3) |
| Sprint 5 (M2) | Verification computed a verdict but never wrote it back, so the risk assessment's highest-weighted indicator stayed at its default | Two algorithms sharing a value with no owner for writing it | Verdict persisted at the end of verification |
| Sprint 6 (M3) | Running a verification was reachable by a Read-Only account, although it writes a verdict and can drive an item to Flagged | An operation classified by its *name* ("verify") rather than by its *effect* | Analysis guard added; refused at the route and hidden in the interface |

The pattern: **each defect came from a correct algorithm placed in a context
whose constraints it did not know about.** None was an error in the
algorithmic logic itself. That is an argument for the architectural separation
Chapter 5 describes - and simultaneously a warning that separation makes each
piece easier to verify in isolation and easier to misplace in combination.

---

\newpage
