# Chapter 11 - Complex Algorithms and Workflows

---

## 11.1 What Makes a Functionality Complex

The coursework requires that a system's functionality be categorised, and that the complex category contain application logic the developer designed rather than invoked. This chapter is the evidence for that claim. It gives an algorithmic account of the five Category C features - data structures, pseudocode, design decisions and complexity - at a level that makes their difficulty **demonstrable rather than asserted**.

The test applied throughout is a single question: *if every third-party call were removed, would a substantial algorithm remain?* Table 11.1 applies it.

**Table 11.1 - The five complex functionalities and the test applied**

| # | Functionality | Third-party calls it makes | What remains if those are removed | Points |
|---|---|---|---|---|
| C1 | Chain-of-custody graph integrity verification | `hashlib.sha256`, Ed25519 `verify` | Graph construction, depth-first traversal, three-condition validation per node, single-pass failure accumulation, completeness scoring, verdict assignment | 13 |
| C2 | Multi-factor evidence risk scoring | None | Eight-factor extraction, four normalisation curve families, weighted combination, five interaction rules with a capped bonus, four-band classification, explanation generation | 8 |
| C3 | Custody chain reconstruction | None | Two-mode gap detection, candidate generation, four-criterion plausibility scoring, best-first selection against a threshold, three-way confidence labelling | 8 |
| C4 | Evidence lifecycle state machine | None | A transition relation over six states with role guards and precondition predicates, plus a three-stage validation pipeline with atomic side effects | 8 |
| C5 | AI assistant orchestration with hallucination detection | One HTTP call to a hosted model | Intent classification, access-scoped context retrieval, prompt construction with history trimming, response validation, reasoning-trace stripping, entity-level hallucination detection | 8 + 3 |

C2, C3 and C4 make **no third-party calls at all**. C1 uses two library primitives as operations inside its traversal, in the same way that arithmetic operators are primitives inside a formula. C5 is the one requiring the most care, and Section 11.6 addresses it directly: the model call is a single message in the middle of a six-stage pipeline, five stages of which are the project's own.

---

## 11.2 Chain-of-Custody Graph Integrity Verification

### 11.2.1 The Primitive: Digital Signing of Custody Events

The verifier depends on custody events being signed, so the signing design is stated first. The Ed25519 algorithm is a library call; the **canonical payload** is the project's design and is specified in Section 10.6.1: a JSON serialisation with sorted keys of exactly six fields - evidence identifier, event type, ISO timestamp, outgoing investigator, incoming investigator, and file hash at the event.

The signature column is `NOT NULL`, which encodes a policy: a custody record must always carry a signature slot. The error behaviour around that policy is deliberately **fail-visible** rather than fail-silent or fail-closed. If signing is unavailable - an account without a key, or a cryptographic error - the system records an explicit unsigned sentinel and warns the user, and the verifier then reports that link as unverified.

This was chosen over two worse alternatives. It is better than the original behaviour, which left the non-nullable column unset and raised a database error that aborted the transfer entirely. And it is better than silently storing a placeholder that would *look* signed. An unsigned event is instead made conspicuous twice over: in the interface through the warning, and in the integrity report through a verification failure at that node. The report describes this as implemented rather than claiming a stronger fail-closed guarantee than the code provides.

### 11.2.2 Purpose and Why It Is Complex

The verifier proves, or disproves, the integrity of an evidence item's **entire** custody history rather than merely its most recent record. This distinction is the whole point: a system that checks only the latest entry can be defeated by tampering with any earlier one, and legal admissibility depends on the whole chain, not its tail.

Verifying the whole chain cannot be expressed as a database query or a library call. It requires modelling the history as a connected structure, walking it, and applying several independent cryptographic and temporal checks at every step while accumulating a complete picture of where - if anywhere - it fails. This reasoning is behind its thirteen-point estimate, the largest in the project.

### 11.2.3 Data Structure

The algorithm loads all custody-log records for the item ordered by timestamp and constructs a **directed acyclic graph** in memory. Each node wraps one custody record and holds a list of outgoing edges to its successors. The root is the `Upload` event - the one custody record with no predecessor, guaranteed to exist by the atomic-creation invariant of Section 10.4.2.

In the common case the chain is linear, each event having a single successor. The structure is nevertheless a general graph so that a future branching scenario - an item split into derived exhibits - could be represented without redesign. This is the *generality* principle applied where it costs almost nothing (Section 3.8).

### 11.2.4 Traversal and Per-Node Validation

**Table 11.2 - The three checks applied at every node**

| Check | What it verifies | What it detects |
|---|---|---|
| **Hash** | On the root: the stored file is decrypted, re-hashed with SHA-256, and compared with the item's immutable `original_hash`. On every node: the recorded `file_hash_at_event` is compared against that ground truth | The physical file was altered since intake, or a custody record was edited after signing |
| **Signature** | The canonical payload is reconstructed from the node's fields and its stored Ed25519 signature verified against the signing investigator's public key | A record was altered after signing, or was never genuinely signed |
| **Timestamp** | The node's timestamp is strictly greater than its predecessor's | A duplicate or backdated record was inserted |

A point of honesty about the hash check: because the system stores a single evidence blob rather than a distinct historical snapshot per event, the per-node check is a **consistency check of recorded hashes against a ground truth**, not a re-hash of per-event file snapshots that the system does not keep. The report states this rather than claiming a stronger guarantee than the data model supports.

### 11.2.5 Pseudocode

```
ALGORITHM VerifyChainIntegrity(evidence)
  logs  <- load custody logs for evidence, ordered by timestamp
  IF logs is empty THEN
      RETURN Report(verdict = BROKEN, completeness = 0, failures = [])

  graph <- BuildGraph(logs)          // nodes = events, edges = successor links
  root  <- the node whose event_type = 'Upload'

  truth <- SHA256(Decrypt(evidence.file))      // ground-truth re-hash
  failures <- []
  verified <- 0
  visited  <- empty set

  STACK <- [root]
  WHILE STACK not empty DO
      node <- STACK.pop()
      IF node in visited THEN CONTINUE
      visited.add(node)

      ok <- TRUE

      // Check 1 - hash continuity
      IF node is root AND truth != evidence.original_hash THEN
          failures.append(Failure(node, HASH, "stored file altered since intake"))
          ok <- FALSE
      IF node.file_hash_at_event != evidence.original_hash THEN
          failures.append(Failure(node, HASH, "recorded hash diverges from ground truth"))
          ok <- FALSE

      // Check 2 - signature validity
      payload <- CanonicalPayload(node)        // sorted-key JSON of six fields
      IF NOT Ed25519Verify(payload, node.signature, signer_public_key(node)) THEN
          failures.append(Failure(node, SIGNATURE, "signature does not verify"))
          ok <- FALSE

      // Check 3 - temporal monotonicity
      IF node.predecessor exists AND node.timestamp <= node.predecessor.timestamp THEN
          failures.append(Failure(node, TEMPORAL, "timestamp not strictly increasing"))
          ok <- FALSE

      IF ok THEN verified <- verified + 1

      FOR EACH successor IN node.edges DO
          STACK.push(successor)                // CONTINUE - do not stop on failure
  END WHILE

  completeness <- verified / |logs|
  verdict <- INTACT             IF failures is empty
           <- BROKEN            IF verified = 0
           <- PARTIALLY_VERIFIED otherwise

  WriteBack(evidence.integrity_status, verdict)
  RETURN Report(verdict, completeness, failures, verified_timeline)
END
```

### 11.2.6 Single-Pass Failure Collection

The design property that mattered most - and the one that cost three days of Increment 2 - is that **the traversal does not stop at the first failure**. When a check fails the algorithm records a structured failure (node identifier, event type, timestamp, failure category, human-readable explanation) and continues, so that all failures across the entire chain are discovered in one pass.

The first implementation short-circuited, which contradicted the acceptance criterion that all failures be found. Reworking the traversal to accumulate while continuing is what the plateau on the Increment 2 burndown (Figure 5.2) represents, and the rework additionally surfaced a payload-format bug: a timestamp-formatting mismatch that the canonical-format decision had been meant to prevent but that had crept back in.

The forensic justification is straightforward. A verifier that reports only the first problem tells an investigator that the chain is broken; a verifier that reports all of them tells the investigator *where* and *how many times* - which is the difference between a verdict and evidence.

### 11.2.7 Output and Complexity

The algorithm returns a structured report carrying the verdict (Intact, Partially Verified, Broken), the completeness score as the proportion of nodes passing all three checks, the counts of total and verified nodes, the ordered failure list and a verified timeline. It is serialisable, so it can be stored as an audit record and consumed by the risk scorer.

**Complexity.** The traversal visits each of the *n* custody nodes once and performs a constant number of checks at each, giving *O(V + E)*, which for a linear chain is *O(n)*. The constant is dominated by cryptographic work - one signature verification per node, plus one file decryption and hash at the root - rather than by the graph walk. This is acceptable for an operation invoked on demand rather than on every request.

---

## 11.3 Multi-Factor Evidence Risk Scoring

### 11.3.1 Purpose and Why It Is Complex

The scorer reduces the many signals bearing on how much an evidence item should worry an investigator into a single comparable number, so that hundreds of items can be ranked and the most concerning surfaced first.

A naive rule such as *flag items with more than five transfers* is inadequate because it ignores the **interaction** between signals: an item with many transfers, a failed integrity check and several handlers is far more concerning than an item with many transfers alone. Capturing those interactions in a defensible, tunable, explainable score is what makes this Category C work rather than a formula.

### 11.3.2 The Eight Factors

**Table 11.3 - The eight risk factors**

| Factor | Signal | Source | Default weight |
|---|---|---|---|
| `integrity_status` | Whether verification passed, failed or has not run | Written back by the graph verifier (Section 11.2) | **0.25** |
| `custody_transfer_frequency` | How often the item has changed hands | Custody log count over time | 0.13 |
| `file_type_risk` | Inherent risk of the file's category | Category-to-risk mapping | 0.12 |
| `role_mismatch_count` | Accesses by roles not permitted for this category | **Category A formula check**, computed live | 0.12 |
| `distinct_investigators` | How many different people have handled it | Distinct custody participants | 0.10 |
| `duplicate_entry_count` | Duplicate custody records | **Category A formula check**, computed live | 0.10 |
| `lifecycle_state` | Current state as an ordinal risk value | Evidence item state | 0.10 |
| `time_since_last_activity` | How long the item has sat untouched | Latest custody timestamp | 0.08 |

Two factors deserve particular note. `role_mismatch_count` and `duplicate_entry_count` are computed **live by the Category A audit-formula checks** built in Increment 1, so the simple formula computations feed directly into the complex algorithm rather than sitting in isolation. `integrity_status` reads the column the graph verifier writes, so the highest-weighted signal reflects a genuine verification result.

Both of these connections were broken when originally written and were repaired in M2 (findings D5 and D2). Before that repair, the two formula factors counted the *wrong* audit events - integrity-check and warning-level records - with the perverse consequence that **running a verification raised an item's risk**, and the integrity factor read a column that did not exist, so a quarter of the algorithm's output was a constant. The repairs are what make Table 11.3 an accurate description rather than an intention.

### 11.3.3 Normalisation

Raw signals are not comparable in their natural units, so each is normalised to [0, 1] using a curve matched to its distribution. Choosing a curve per factor, rather than normalising everything linearly, is a small piece of modelling that materially improves the score's behaviour.

**Table 11.4 - Normalisation curve families**

| Curve | Applied to | Why this curve |
|---|---|---|
| **Categorical mapping** | `integrity_status` (verified → 0.0, not-checked → 0.5, failed → 1.0); `lifecycle_state`; `file_type_risk` | The signal has no natural magnitude, only ordered categories |
| **Logarithmic** | `custody_transfer_frequency`, `distinct_investigators` | Heavy-tailed counts: the difference between one and three handlers matters far more than between eleven and thirteen |
| **Sigmoid centred at 30 days** | `time_since_last_activity` | Risk should rise sharply as the item passes the point where prolonged inactivity becomes suspicious, not linearly from day one |
| **Bounded linear** | `role_mismatch_count`, `duplicate_entry_count` | Small integer counts where each additional occurrence carries similar weight |

Every curve clamps to [0, 1], so the composite score is **provably bounded** - the property that makes it "rigorous" in Table 3.3.

### 11.3.4 Weighting and Interaction Detection

The normalised factors are combined by a weighted sum whose weights sum to 1.0, with integrity failure weighted highest because it is the most direct evidence of a problem. Administrator overrides are re-normalised on save, so the sum-to-one property cannot be broken by configuration.

On top of the base score, **five interaction rules** are evaluated. Each names a pair of factors and a threshold for each; when both exceed their thresholds, a multiplicative bonus is applied.

**Table 11.5 - The five interaction rules**

| Factor A | Factor B | Thresholds | Multiplier | Forensic interpretation |
|---|---|---|---|---|
| `integrity_status` | `role_mismatch_count` | 0.6 / 0.6 | 1.30 | Integrity failure with role mismatches strongly indicates deliberate tampering |
| `custody_transfer_frequency` | `integrity_status` | 0.7 / 0.5 | 1.25 | Rapid transfers alongside integrity issues indicate a chain-of-custody breach |
| `file_type_risk` | `duplicate_entry_count` | 0.7 / 0.5 | 1.20 | A high-risk file type with duplicate entries suggests suspicious duplication |
| `distinct_investigators` | `custody_transfer_frequency` | 0.6 / 0.6 | 1.20 | Many handlers with rapid transfers indicates an unstable custody chain |
| `role_mismatch_count` | `duplicate_entry_count` | 0.5 / 0.5 | 1.15 | Role mismatches with duplicate entries suggest administrative tampering |

The **total** interaction bonus is capped at 0.30. This cap is not incidental: several rules can fire simultaneously, and without it the bonuses stack and trivially push any moderately risky item to a saturated 1.0, which destroys the ranking the score exists to produce. A ranking in which everything is Critical conveys no information.

### 11.3.5 Classification, Explanation and Pseudocode

The final score, clamped to 1.0, is classified into four bands using thresholds that default to 0.25, 0.50 and 0.75 and are administrator-configurable with a validation that they be **strictly increasing**, so the bands cannot overlap or invert.

```
ALGORITHM ScoreEvidenceRisk(evidence)
  // Stage 1 - extract (order-independent)
  raw <- { f : ExtractFactor(f, evidence) FOR EACH f IN EIGHT_FACTORS }

  // Stage 2 - normalise
  norm <- { f : Clamp(Curve[f](raw[f]), 0, 1) FOR EACH f }

  // Stage 3 - weighted sum
  w <- Normalise(GetWeights())              // always sums to 1.0
  base <- SUM over f OF w[f] * norm[f]

  // Stage 4 - interaction detection
  bonus <- 0
  fired <- []
  FOR EACH (a, b, ta, tb, mult, reason) IN INTERACTION_RULES DO
      IF norm[a] >= ta AND norm[b] >= tb THEN
          bonus <- bonus + base * (mult - 1)
          fired.append(reason)
  bonus <- Min(bonus, MAX_INTERACTION_BONUS)   // cap = 0.30
  score <- Min(base + bonus, 1.0)

  // Stage 5 - classify and explain
  level <- CRITICAL IF score >= 0.75
        <- HIGH     IF score >= 0.50
        <- MEDIUM   IF score >= 0.25
        <- LOW      otherwise

  contributions <- sort factors by (w[f] * norm[f]) descending
  RETURN Report(score, level, norm, contributions, fired,
                Recommendations(norm))
END
```

The output is not an opaque number: it carries each factor's normalised value and weighted contribution, the interaction reasons that fired, and recommendations keyed to which factors are elevated. This matters for the same reason DR-07 matters - an investigator must be able to see *why* an item is ranked where it is.

**Complexity.** *O(n)* in the number of custody and audit records for the item, dominated by factor extraction; the normalisation, weighting, five-rule interaction check and classification are all constant-time. Scoring a dashboard of *m* items is therefore *O(m · n)*.

The score is recomputed whenever an item's state changes, because both the lifecycle-state factor and the integrity factor are inputs - which is why the state machine triggers a recalculation on every transition.

---

## 11.4 Custody Chain Reconstruction

### 11.4.1 Purpose and Why It Is Complex

Reconstruction addresses the case where the custody record is incomplete - a transfer was never recorded, an entry was deleted, or timestamps are inconsistent - and the investigator nonetheless needs the most plausible account of what happened, **clearly separated into what is certain, what is inferred, and what cannot be resolved**.

This is fundamentally a heuristic search rather than a lookup: there is no single correct answer when records are missing, so the algorithm must generate possible filling records, evaluate their plausibility against several criteria, and return the best-supported reconstruction together with an honest measure of confidence.

### 11.4.2 Gap Detection

The algorithm loads the confirmed records in timestamp order and walks each consecutive pair, detecting gaps in two modes.

**Table 11.6 - The two gap detection modes**

| Mode | Condition | Example |
|---|---|---|
| **Structural** | The holder implied by one record does not match the holder named by the next | Investigator B is recorded as *receiving* an item, but there is no record of A, its previous holder, transferring it |
| **Temporal** | More than a configured number of hours - 72 by default - separates two consecutive records with no intervening transfer | An item sat unaccounted-for for four days even though the holder fields happen to align |

The temporal mode was added during development because structural matching alone missed the common real-world case of an item that is simply unattended for an extended period. This is worth recording as a design history: the first version of the algorithm was structurally correct and forensically incomplete.

### 11.4.3 Candidate Generation and Four-Criterion Scoring

For each gap the algorithm generates candidate filling records by querying the access log for events falling within the gap's time window that involve investigators who could plausibly have handled the item. Each candidate is scored by a plausibility function combining four independent criteria.

**Table 11.7 - The four plausibility criteria**

| Criterion | Question | Evidence used |
|---|---|---|
| **Temporal proximity** | How close is the candidate's timestamp to the expected transfer window? | Candidate timestamp against the gap boundaries |
| **Role consistency** | Is this investigator's role permitted to hold evidence of this category? | An explicit role-to-category permission matrix |
| **Location consistency** | Is the candidate's recorded location plausible given the surrounding confirmed records? | Locations of the bracketing records |
| **Behavioural consistency** | Did this investigator have other interactions with the same case around that time? | Audit records for the case in the window |

The combined score lies in [0, 1], and the **breakdown across the four criteria is retained**, so that an inferred link can explain itself rather than merely assert a confidence figure.

### 11.4.4 Best-First Selection, Labelling and Pseudocode

```
ALGORITHM ReconstructCustodyChain(evidence)
  confirmed <- load custody logs for evidence, ordered by timestamp
  IF confirmed is empty THEN RETURN Chain(links = [], confidence = 0.0)

  links <- [ Link(r, CONFIRMED, 1.0) FOR EACH r IN confirmed ]
  gaps  <- []
  FOR EACH consecutive pair (r1, r2) IN confirmed DO
      IF HolderMismatch(r1, r2) OR HoursBetween(r1, r2) > GAP_HOURS THEN
          gaps.append(Gap(r1, r2))

  IF gaps is empty THEN RETURN Chain(links, confidence = 1.0)

  FOR EACH gap IN gaps DO
      candidates <- AccessLogEventsWithin(gap.window, evidence.case)
      IF candidates is empty THEN
          links.insert_at(gap, Link(NONE, UNRESOLVED, 0.0, gap.window))
          CONTINUE

      FOR EACH c IN candidates DO
          c.score <- ( TemporalProximity(c, gap)
                     + RoleConsistency(c, evidence.category)
                     + LocationConsistency(c, gap)
                     + BehaviouralConsistency(c, evidence.case) ) / 4

      best <- argmax over candidates OF c.score        // best-first selection

      IF best.score >= PLAUSIBILITY_THRESHOLD THEN     // threshold = 0.40
          links.insert_at(gap, Link(best, INFERRED, best.score,
                                    Explain(best.subscores)))
      ELSE
          links.insert_at(gap, Link(NONE, UNRESOLVED, 0.0, gap.window))
  END FOR

  confidence <- (#CONFIRMED + #INFERRED) / |links|
  RETURN Chain(links, confidence)
END
```

**Three-way labelling is the algorithm's central honesty guarantee.** Every link is *Confirmed*, *Inferred* or *Unresolved*; an inferred record is visibly distinguished from a confirmed one and is never presented as fact. This directly addresses the risk, identified in the project proposal, that a reconstruction might mislead an investigator into treating an estimate as certainty, and it is domain requirement DR-07 in executable form.

The plausibility threshold of 0.40 is what makes the guarantee real. An algorithm optimised to look impressive would lower the threshold and always produce a complete chain; this one refuses to infer a link it cannot justify, which is why three separate paths through Figure 8.7 end in an admission of failure.

**Complexity.** Linear in the number of confirmed records for gap detection, plus, for each gap, a scan of the access-log events within that gap's window: *O(n + Σ|C_g|)* where *C_g* is the candidate set for gap *g*. The four criteria are constant-time per candidate.

---

## 11.5 The Evidence Lifecycle State Machine

### 11.5.1 Purpose

The state machine turns the evidence lifecycle from a convention that investigators are trained to follow into a rule that the system enforces. It guarantees that no item can be moved into an invalid state, that only authorised roles can trigger particular transitions, and that some transitions cannot occur until their preconditions are met - above all, that an item cannot be archived until its integrity has been verified as intact.

### 11.5.2 The Automaton

Formally the lifecycle is a tuple *(S, R, P, δ)* where *S* is the six-element state set {Collected, Submitted, Under Analysis, Transferred, Archived, Flagged}, *R* is the four-element role set, *P* is a set of precondition predicates over an evidence item, and *δ* is a partial function mapping an ordered state pair to the set of permitted roles and the list of preconditions that must hold. The complete transition table is given in Table 8.11, its per-role availability in Table 8.7, and its visual form in Figure 8.8.

Representing the lifecycle as a **table rather than as branching code** was a deliberate choice with three consequences: the whole policy is visible and auditable in one place; adding or changing a transition is a data change rather than a control-flow change; and the table is directly comparable with the state diagram, so drift between model and code is detectable by inspection.

Because *δ* is a **partial function**, illegal transitions are decidable: a state pair either appears in the table or does not, and one that does not is refused. There is no ambiguous case and no default branch.

### 11.5.3 The Validation Pipeline and Pseudocode

```
ALGORITHM TransitionTo(evidence, target_state, investigator, justification)
  key <- (evidence.lifecycle_state, target_state)

  // Stage 1 - does the transition exist?
  IF key NOT IN TRANSITION_TABLE THEN
      Audit(REJECTED, "no such transition")
      RETURN Rejected("Transition from {from} to {to} is not permitted")

  rule <- TRANSITION_TABLE[key]

  // Stage 2 - is the role permitted?
  IF investigator.role NOT IN rule.required_roles THEN
      Audit(REJECTED, "insufficient role")
      RETURN Rejected("Role {role} may not perform this transition")

  // Stage 3 - are all preconditions satisfied?
  FOR EACH (predicate, message) IN rule.preconditions DO
      IF NOT predicate(evidence, investigator) THEN
          Audit(REJECTED, message)
          RETURN Rejected(message)          // exact unmet condition returned

  // All stages passed - execute atomically
  BEGIN TRANSACTION
      evidence.lifecycle_state <- target_state
      Audit(TRANSITION, investigator, timestamp, justification)
      Recompute(evidence.risk_score)        // state is a scoring factor
  COMMIT

  RETURN Accepted(target_state)
END
```

Two properties of this pipeline are worth emphasising.

**Rejections are audited as fully as successes.** A failed attempt to move an item into a state the actor may not reach is itself forensically interesting - it may be the first sign of a procedural problem - so it is written to the trail with the exact condition that was not met, rather than merely refused in the interface.

**The side effects are atomic with the state change.** The state update, the audit write and the risk recalculation occur in one transaction. If they did not, the system could reach a state where an item is Archived but no audit record says who archived it, which would defeat the purpose of the audit trail.

### 11.5.4 Why It Is Complex

The state machine is more than a field update guarded by an `if`. It is a formal automaton whose transition relation, role guards and precondition predicates together encode a body of procedural law, and whose execution has side effects that must occur atomically with the state change.

Its correctness is what allows the rest of the system to trust a claim it could not otherwise make: that an **Archived item really did pass integrity verification**. The archiving precondition enforces this by checking for an integrity-check audit record with an Intact verdict before permitting the transition. That single guard is guarantee G4 in its purest form - a rule of forensic procedure converted into a condition the system will not let anyone bypass.

---

## 11.6 AI Assistant Orchestration and Hallucination Detection

### 11.6.1 Purpose and Why It Is Complex

The assistant lets an investigator ask questions in natural language - *"what is the risk score for evidence seven?"*, *"who has held this item?"*, *"what are my cases?"* - and receive answers grounded in the actual database rather than in the model's imagination.

The language model itself is a Category B service. What the project contributes, and what makes this Category C, is the **orchestration workflow around it**: the logic that decides what the question is about, retrieves exactly the right data while respecting access boundaries, constructs a prompt, and - critically - validates and fact-checks the answer before showing it. Figure 8.5 makes the proportion visible: the model call is one message in the middle; five of the six stages are the project's own.

### 11.6.2 The Six Stages

**Table 11.8 - The six orchestration stages**

| Stage | Name | What it does | Whose work |
|---|---|---|---|
| 1 | **Intent classification** | Assigns the question to one of seven intents plus unknown, using a keyword-frequency classifier, and extracts any entity identifier mentioned. The *identity* intent is checked **with priority**, so that "what are the cases assigned to me?" is recognised as self-referential despite containing case-query keywords | Project |
| 2 | **Context retrieval** | Runs a targeted query determined by the intent, **scoped to `accessible_case_ids`**, and serialises the records into a compact context block | Project |
| 3 | **Prompt construction** | Assembles a system prompt embedding the context and the authenticated user's identity, then appends trimmed conversation history | Project |
| 4 | **Model invocation** | Sends the prompt to the hosted model, with a per-model timeout, an ordered fallback list and a total time budget; falls back to a context-aware mock when no key is configured or all candidates fail | **Third party**, with project-designed fallback |
| 5 | **Response validation** | Checks for minimum length, refusal patterns and off-topic drift; strips any chain-of-thought trace the model emits before the answer | Project |
| 6 | **Hallucination detection** | Cross-checks every entity reference in the reply against the retrieved context | Project |

### 11.6.3 Two Decisions That Shape the Pipeline

**Access scoping in stage 2 is not an afterthought - it is what makes the assistant safe.** Because retrieval is filtered to the user's accessible cases, every downstream stage operates only on permitted data, so the assistant inherits the same case-level authorisation as the rest of the system rather than becoming a hole in it. Before M1 the retrieval was global, and a lead investigator could ask the assistant to list all cases and receive every case in the system - a defect that no amount of prompt engineering would have fixed, because the data was already in the prompt.

**The mock fallback in stage 4 is what made the pipeline testable.** The model is invoked through a single method that tests can exercise without a network call, so stages 1, 2, 3, 5 and 6 are all covered by fast deterministic tests. This is the *dependency behind a seam* practice carried in as action A2-2 from the Increment 2 retrospective, and it paid off twice: once in test coverage, and again when the hosted model was retired mid-project and the change was confined to one method.

### 11.6.4 Hallucination Detection

```
ALGORITHM CheckHallucinations(reply, context, user, question)
  known <- ExtractEntities(context)          // entities actually retrieved
       ∪ { user.full_name, user.role }       // the asker's own identity
       ∪ ExtractEntities(question)           // terms the user themselves used

  flags <- []
  FOR EACH reference IN ExtractEntities(reply) DO
      IF reference NOT IN known THEN
          flags.append("'" + reference + "' was not found in the retrieved data")

  RETURN flags
END
```

The check extracts every case number, evidence identifier and investigator name from the reply and cross-checks each against the context that was actually retrieved and injected into the prompt. A reference not present is flagged as a potential fabrication and surfaced to the user as an explicit warning attached to the answer.

Because retrieval is access-scoped, the check does **double duty**: it catches both invented entities and any attempt by the model to mention a real entity the user was not permitted to see, since neither will be present in the scoped context.

The `known` set deliberately includes two sources beyond the retrieved context. The **user's own identity** is included because it appears in the system prompt rather than the context block, and without it the assistant flagged an administrator's own role as a hallucination when answering "who am I". The **user's own question** is included because a user who names an entity is not being told something fabricated. Both additions came from observed false positives; a hallucination detector that cries wolf is worse than none, because its warnings stop being read.

**The limits are stated plainly.** The check verifies *references, not reasoning*: it cannot establish that the model's prose is correct, only that the entities it names exist and were permitted. The assistant is therefore positioned as a convenience whose output is to be verified, not as an authority. But it addresses the most dangerous failure mode directly - an answer that confidently names an evidence item or investigator that does not exist or that the user cannot access.

### 11.6.5 A Note on the Isolation Forest

The anomaly-detection pipeline is deliberately **not** listed as a Category C feature. The Isolation Forest is scikit-learn's algorithm, not the project's, and the honest claim is limited to the feature engineering around it: a six-dimensional vector per item comprising transfer count, transfer rate, unique handlers, maximum gap in days, an integrity flag and file-type risk, with the resulting anomaly score mapped into [0, 1].

Classifying this as Category B rather than Category C is a deliberate act of the categorisation discipline discussed in Section 16.6. It would have been easy to claim it as complex work; the feature engineering is genuinely the project's own. But the algorithm that does the interesting part is not, and the categorisation is more credible for excluding it.

---

## 11.7 Complexity Summary

**Table 11.9 - Asymptotic complexity of the five algorithms**

| Algorithm | Time complexity | Dominant cost | Space | Invocation |
|---|---|---|---|---|
| Graph integrity verification | *O(V + E)*, linear in custody records | Cryptographic: one signature verification per node; one file decrypt + hash at the root | *O(V)* for the graph and visited set | On demand |
| Multi-factor risk scoring | *O(n)* per item; *O(m · n)* for a dashboard of *m* items | Factor extraction queries | *O(1)* - eight factors | On state change and on dashboard load |
| Custody chain reconstruction | *O(n + Σ&#124;C_g&#124;)* | Candidate scoring per gap | *O(n)* for the link list | On demand |
| Lifecycle state machine | *O(p)* where *p* is the number of preconditions on the transition - in practice at most one | Precondition evaluation (one audit-record query) | *O(1)* | Per transition request |
| AI orchestration | *O(k)* in retrieved context size, plus one bounded network call | The network call, bounded at 20 s per model and 60 s total | *O(k)* for context and history | Per question |

None of these is worse than linear in the data it examines. This is a deliberate property rather than a happy accident: every algorithm was designed around a single pass over its input, which is why the verifier accumulates failures rather than restarting, why the risk scorer extracts all eight factors before combining any, and why reconstruction resolves each gap independently rather than searching over whole-chain hypotheses.

## 11.8 Summary

This chapter gave an algorithmic account of the five Category C functionalities, applying throughout the test of what would remain if every third-party call were removed - and showing that for three of the five, nothing would be removed at all.

The graph integrity verifier was presented with its directed-acyclic-graph representation, its three per-node checks, its single-pass failure accumulation and the three-day rework that produced it, together with an explicit statement of what its hash check does and does not prove. The risk scorer was given with its eight factors, four normalisation curve families, five interaction rules and capped bonus, including the account of how two of its inputs were silently broken until M2 repaired them. Chain reconstruction was presented as a heuristic best-first search whose central property is the number of paths that end in an honest *Unresolved*. The state machine was formalised as a partial transition function with role guards and precondition predicates, executing atomically, and identified as the mechanism by which forensic procedure becomes enforced logic. The AI orchestration was decomposed into six stages, five of them the project's own, with the hallucination detector's `known` set and its stated limits.

Pseudocode was given for all five, and asymptotic complexity established for each. The next chapter turns to how all of this was tested.

---

\newpage
