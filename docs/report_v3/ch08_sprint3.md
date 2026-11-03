# Chapter 8 - Sprint 3: Assessment

*15 working days · 42 points committed · 42 delivered*

---

## 8.1 Sprint Goal

**An investigator with a caseload can tell which exhibits need attention
without reading every record, and can ask about a case in ordinary language
and be answered from the records themselves.**

## 8.2 Backlog Refinement Before Planning

Refinement produced backlog **v1.2**, with two priority changes and no
re-estimates:

| Change | Cause |
|---|---|
| US-22 (statistical outliers) lowered Should → **Could** | Sprint 2's review showed the deterministic assessment would carry the ranking; an uninterpretable second signal was a nice-to-have |
| US-24 (second factor, lockout) raised Could → **Should** | The same review noted that every guarantee in the system rests on the account being who it claims to be |

**The second change is a priority decision made on evidence rather than on
taste.** Nothing in Sprint 2 failed; the reasoning was that the integrity
guarantees built there are worth exactly as much as the authentication
protecting them.

**Table 8.1 - Sprint 3 backlog**

| ID | Story | Pts | Realises | Category |
|---|---|---|---|---|
| US-18 | Exhibits ranked by attention needed | 8 | SR-36 to SR-38 | **C** |
| US-20 | Ask questions in ordinary language | 8 | SR-40 to SR-42 | **C** |
| US-21 | Unsupported statements flagged | 3 | SR-43 | **C** |
| US-24 | Second factor and lockout | 5 | SR-47 | B |
| US-19 | Tune what counts as risky | 3 | SR-39 | **C**/A |
| US-25 | Evidence unreadable without authorisation | 3 | SR-48 | B |
| US-23 | Ranked and anomalous views | 3 | SR-46 | A |
| US-22 | Statistical outliers surfaced | 5 | SR-44, SR-45 | B |
| US-26 | Verifiable export | 2 | SR-49 | B |
| US-27 | Printable custody report | 2 | SR-50 | B |
| | **Total** | **42** | | |

## 8.3 Action B1 Applied: Criteria as Tests, Written First

Sprint 2's retrospective required acceptance criteria for Category C stories
to exist as failing tests before implementation. US-18's criteria were
therefore written as six tests on day one, before any scoring code:

**Table 8.2 - US-18 acceptance criteria, written as tests before the code**

| Criterion | Test written first | Why it would have been missed |
|---|---|---|
| The eight weights sum to exactly 1.0 | Assert the sum | A later weight edit silently breaks the scale |
| Administrator overrides are re-normalised | Set weights summing to 1.4, assert 1.0 | The interface would accept an unusable configuration |
| Each indicator contributes independently | One test per indicator | A copy-paste error between indicators is invisible in the total |
| Each interaction rule fires on its own pair | One test per rule | Five rules, five chances for a wrong pair |
| **The total bonus is capped at 0.30** | Construct an item firing four rules | Without the cap the ranking collapses, and the total still looks plausible |
| The output explains itself | Assert per-indicator contributions present | An unexplained score is unusable in court |

The cap test is the one that justifies the practice. An item firing four rules
produces a high score either way; **only a test that knows what the cap is for
can tell a correct high score from a saturated one.**

## 8.4 Sprint Backlog: Tasks

**Table 8.3 - US-18 (risk assessment) decomposed**

| Task | Description | Est. (h) | Realises |
|---|---|---|---|
| T-18.1 | Write the six acceptance tests (Table 8.2) | 6 | B1 |
| T-18.2 | Extract the eight indicators | 8 | SR-36 |
| T-18.3 | Choose and implement a normalisation curve per indicator | 6 | SR-36 |
| T-18.4 | Weighted combination | 2 | SR-37 |
| T-18.5 | The five interaction rules | 5 | SR-37 |
| T-18.6 | The bonus cap | 1 | SR-37 |
| T-18.7 | Classification into bands | 2 | SR-38 |
| T-18.8 | Per-indicator explanation and recommendations | 5 | SR-38 |
| T-18.9 | Activity and communication diagrams | 2 | DoD 7 |
| | **Total** | **37 h** | |

**Table 8.4 - US-20 and US-21 (assistant) decomposed**

| Task | Description | Est. (h) | Realises |
|---|---|---|---|
| T-20.1 | Intent classification over seven intents, with tie-breaking | 6 | SR-40 |
| T-20.2 | Retrieval sequence per intent | 8 | SR-41 |
| T-20.3 | **Put the model behind a seam that tests can substitute** | 3 | B2 |
| T-20.4 | Prompt templates per intent | 4 | SR-42 |
| T-20.5 | Budgeted invocation with candidate fallback | 5 | SR-42 |
| T-20.6 | Context-only answer when the service is unavailable | 4 | SR-42 |
| T-21.1 | Extract identifiers and names from a reply | 4 | SR-43 |
| T-21.2 | Check each against the retrieved context; warn on absences | 4 | SR-43 |
| | **Total** | **38 h** | |

T-20.3 is retrospective action B2. Because the model sits behind a seam, the
whole pipeline is testable without network access - which is why SNF-20 ("the
suite runs without reaching any external service") is satisfiable at all.

## 8.5 Design and Models

**Table 8.5 - Models produced in this sprint**

| Figure | Kind | Subject |
|---|---|---|
| 17 | Activity | Risk assessment |
| 14 | Communication | Risk assessment collaboration |
| 26 | Activity | Assistant orchestration, six stages |
| 13 | Sequence | Assistant orchestration |
| 20 | Timing | Bounded waiting on the model service |
| 16 | State machine | Account access, with lockout |
| 9 | Component | Components and their interfaces |
| 11 | Deployment | Nodes, artifacts and the trust boundary |

The algorithms are described in **Chapter 11**, sections 11.3 and 11.6.

Figure 11 is drawn in this sprint rather than earlier because this is the
sprint that puts something **outside** the trust boundary. Until the model
service existed, every component ran on one host.

## 8.6 Implementation

Two decisions are worth recording.

**The assessment reads the integrity verdict as its highest-weighted
indicator.** This couples Sprint 3's algorithm to Sprint 2's, and the coupling
later proved to be the site of a defect: the verdict was computed but never
persisted, so the indicator sat at its default. Chapter 9, finding D2.

**The anomaly detector was kept visibly separate from the assessment.** Its
output is labelled "suggested for review" and never merged into the
deterministic score. SR-45 requires this, and it is also the honest treatment
of an uninterpretable signal sitting beside an explainable one.

## 8.7 Verification

**Table 8.6 - Tests written in Sprint 3**

| Area | Cases |
|---|---|
| Risk: the six criteria of Table 8.2 | 6 |
| Risk: indicators individually | 8 |
| Risk: interaction rules individually | 5 |
| Risk: classification bands | 4 |
| Intent classification | 10 |
| Retrieval per intent | 7 |
| Degraded answer with no service | 3 |
| Reference validation | 4 |
| Second factor, lockout, idle timeout | 9 |
| Encryption at rest | 4 |
| Export and printable report | 6 |

Ninety-three tests in `test_increment3`, the largest single module in the
suite.

## 8.8 Burndown

**[FIGURE 8.1 - Sprint 3 burndown]**

The steadiest of the three, tracking the ideal within about two points
throughout. **This is the measurable result of two sprints of retrospective
actions** - and it is also the sprint with the most third-party integration,
which would normally be the least predictable.

## 8.9 Sprint Review

**Table 8.7 - Acceptance against the stories' criteria**

| Story | Criterion | Outcome |
|---|---|---|
| US-18 | Eight indicators, each normalised appropriately | Met |
| US-18 | Interaction bonus bounded | Met |
| US-18 | Output explains its own score | Met |
| US-19 | Weights re-normalised; bands strictly increasing | Met |
| US-20 | Seven intents classified, UNKNOWN recognised | Met |
| US-20 | Answers drawn from retrieved records | Met |
| US-20 | A usable answer with the service unavailable | Met |
| US-21 | References absent from context are flagged | Met |
| US-22 | Outliers presented as suggestions, never findings | Met |
| US-23 | Ranked view, anomaly view, per-item detail | Met |
| US-24 | Second factor; lockout after five failures | Met |
| US-25 | Content unintelligible without the key | Met |
| US-26 | A recipient can verify without this system | Met |
| US-27 | Printable report produced | Met |

All forty-two points accepted. **At this point the project appeared complete.**

## 8.10 Retrospective

**What worked.** Action B1 - criteria as failing tests first - produced the
steadiest burndown in the project. Action B2 made the external dependency
testable.

**What did not, and was not visible yet.** Every test written in this sprint
was a *positive* test: it asserted that an entitled user gets the right
answer. Not one asked what an *unentitled* user gets. The suite was green and
the system had a scoping defect in every aggregate it had just built.

**Table 8.8 - Actions carried forward**

| # | Action | Where it shows |
|---|---|---|
| C1 | Add the per-item risk detail to the evidence view | Delivered |
| C2 | Document the model-unavailable path in the interface | Delivered |
| C3 | **Adversarially test the authorisation boundary** | Raised in Sprint 4 - *after* the defect was found, not before |

**C3 is recorded honestly as an action that came too late.** It was written
during this retrospective as a general improvement and not acted on until
Sprint 4 forced it. Chapter 9 records what that cost.

---

\newpage
