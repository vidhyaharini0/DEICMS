# Chapter 14 - Software Evolution and Maintenance

---

## 14.1 Why Software Must Evolve

**Software change is inevitable.** New requirements emerge and old ones change; the business environment changes; errors must be repaired; new computers and equipment are added to the system; performance or reliability may have to be improved. A key problem for every organisation is implementing and managing change to its existing software systems.

The economic importance of this is easy to underestimate from inside a development project. Organisations have huge investments in their software systems - they are critical business assets - and to maintain the value of those assets they must be changed and updated. The consequence is that **the majority of the software budget in large companies is devoted to changing and evolving existing software rather than developing new software**, and that maintenance costs exceed 60% of the total cost of a software product over its life (Section 2.4.8).

This chapter therefore does not describe an afterthought. It describes the activity that, measured in money and effort, *is* software engineering for most of a system's life. DEICMS provides direct evidence of this in miniature: two maintenance iterations followed its three development increments, and they are documented as first-class iterations in Chapter 5 rather than as a postscript.

A distinction is worth making at the outset. **Evolution** refers to the continuing development of a system that is still actively being extended, where the original developers are usually still involved. **Maintenance** refers to changes made to a system that is in operational use and is no longer under active development. In practice the boundary blurs, and DEICMS sits on it: M1 and M2 occurred after the planned scope was complete but while the developer was still fully engaged, which is closer to evolution than to classical maintenance. The report uses "maintenance" for both because that is the term the iterations were planned under, but the distinction matters for interpreting the cost figures in Section 14.5.

## 14.2 Lehman's Laws Applied to DEICMS

After several major empirical studies, Lehman and Belady proposed a number of "laws" applying to all systems as they evolve. They are more accurately described as **sensible observations rather than laws**, and they were confirmed in later work on the FEAST project. They apply most clearly to large, tailored systems developed by an organisation for its own use - which DEICMS is not - so the honest application below asks, for each law, whether it is *visible*, *not yet applicable*, or *not observable at this scale*.

**Table 14.1 - Lehman's laws applied to DEICMS**

| # | Law | Statement | Observed in DEICMS? |
|---|---|---|---|
| 1 | **Continuing change** | A program used in a real-world environment must necessarily change or become progressively less useful | **Visible.** The external language model was retired by its provider mid-project; the system had to change simply to keep working. This is the law in its purest form - the environment changed, not the requirements |
| 2 | **Increasing complexity** | As a program evolves, its structure becomes more complex unless effort is made to maintain or reduce it | **Visible, and actively resisted.** M1's fix *reduced* complexity by replacing an inline rule duplicated-by-omission with a single helper. M2's fixes added two columns and a fallback list, increasing it. The net is roughly neutral, which is only true because refactoring was treated as part of the fix |
| 3 | **Large program evolution** | Program evolution is a self-regulating process; system attributes such as size, time between releases and number of reported errors are approximately invariant for each release | **Not observable.** Three increments is far too short a series to establish invariance. The velocity clustering between 38 and 42 points (Section 4.8) is suggestive of self-regulation but is better explained by deliberate capacity planning |
| 4 | **Organisational stability** | Over a program's lifetime, its rate of development is approximately constant and independent of the resources devoted to it | **Not applicable.** A single developer with no resource variation to observe |
| 5 | **Conservation of familiarity** | Over the lifetime of a system, the incremental change in each release is approximately constant | **Weakly visible.** The three increments carried 40, 38 and 42 points - approximately constant. But see the caveat in Section 4.8: the estimator and implementer were the same person |
| 6 | **Continuing growth** | The functionality offered by a system has to continually increase to maintain user satisfaction | **Not observable.** The project has no user population and a fixed scope |
| 7 | **Declining quality** | The quality of a system will decline unless it is modified to reflect changes in its operational environment | **Visible in the small.** The risk scorer's `integrity_status` factor and its two formula factors decayed into meaninglessness not because they changed, but because the environment around them changed while they did not (findings D2 and D5). The code was untouched; its *correctness* declined anyway |
| 8 | **Feedback system** | Evolution processes incorporate multi-agent, multi-loop feedback systems, and these must be treated as such to achieve significant product improvement | **Visible.** Every retrospective action was fed into the next iteration and its effect observed - A1-2 into Increment 2's payload design, A2-1 and A2-2 into Increment 3's burndown steadiness, A3-1 into M1's existence |

**Law 7 is the one this project illustrates best, and in an unexpected way.** The conventional reading of declining quality concerns an operational environment that moves on. Here the movement was *internal*: the risk scorer read a column that a schema change was supposed to have provided and never did, so a quarter of the flagship algorithm silently produced a constant while every test stayed green. Nothing in that module changed; its quality declined because the world around it did. That is precisely the law's mechanism operating over three increments instead of ten years.

**Law 2 is the one the project most consciously acted on.** Increasing complexity is resisted only by spending effort on structure during maintenance rather than after it, and both iterations did so: M1 introduced an abstraction rather than patching five call sites, and M2's fixes were accompanied by tests and a schema migration rather than left as local repairs. The counterfactual - five inline scoping checks and two ad-hoc column workarounds - would have made the third maintenance iteration materially harder, which is the compounding effect the law describes.

## 14.3 Types of Maintenance

Maintenance does not normally involve major changes to the system's architecture. Changes are implemented by modifying existing components and adding new ones. Maintenance divides into three categories, whose relative shares of effort are well established.

**Table 14.2 - The types of maintenance and their typical effort distribution**

| Type | Definition | Typical share of maintenance effort |
|---|---|---|
| **Corrective** | Maintenance to repair software faults - removing residual errors | ~20% |
| **Adaptive** | Maintenance to adapt the software to a different operating environment: changes to hardware, platform, operating system or supporting software | ~20% |
| **Perfective** | Maintenance to add to or modify the system's functionality, or to improve quality attributes - usually in response to changing requirements | **>50%** |

A fourth category, **preventive** maintenance, is sometimes distinguished: work done to reduce the likelihood of future faults or to make future change cheaper, of which refactoring is the canonical example. It is not always separated out because it tends to be folded into whichever of the three occasions it.

The striking figure is that **more than half of maintenance effort goes into perfective work** - changing what the system does, not repairing what it does wrongly. This contradicts the intuitive picture of maintenance as bug-fixing, and it is the reason maintainability is treated as an *evolvability* property (Section 2.4.8) rather than merely a repairability one.

Maintainability decomposes accordingly into **repairability**, the ability to correct defects in reasonable time, and **evolvability**, the ability to adapt the software to environmental changes and improve it in reasonable time.

## 14.4 Classification of the Maintenance Work Performed

The seventeen maintenance items delivered in M1 and M2 are classified below against the taxonomy. This is the chapter's central evidence, and its distribution is instructive precisely because it *departs* from the typical figures.

**Table 14.3 - Classification of the DEICMS maintenance work**

| Iteration | Item | Type | Repairability or evolvability | Justification |
|---|---|---|---|---|
| M1 | CR-01 - scope every aggregate to accessible cases | **Corrective** | Repairability | A stated requirement was not met on five surfaces |
| M1 | CR-01 - role-tailored dashboard panels | **Perfective** | Evolvability | Not required to fix the leak; added because scoping raised a design question the global view never had to answer |
| M1 | CR-02 - scope assistant retrieval | **Corrective** | Repairability | Same requirement, different surface |
| M1 | CR-02 - identity intent and user injection | **Perfective** | Evolvability | New capability: the assistant could not previously answer "who am I" |
| M1 | CR-02 - chat history isolation | **Corrective** | Repairability | A session-management fault |
| M1 | CR-02 - smaller model and request timeout | **Adaptive** | Evolvability | A response to the operating environment - the hosted model's latency |
| M2 | D1 - soft delete persisted properly | **Corrective** | Repairability | The feature silently did nothing |
| M2 | D2 - `integrity_status` column written back | **Corrective** | Repairability | The highest-weighted factor read a non-existent field |
| M2 | D3 - cross-case evidence access closed | **Corrective** | Repairability | An authorisation fault |
| M2 | D4 - fail-visible signing behaviour | **Corrective** | Repairability | A crash and an unverifiable-record risk |
| M2 | D5 - risk factors pointed at the real formula checks | **Corrective** | Repairability | Two factors computed the opposite of their intended meaning |
| M2 | D6 - timestamp consistency | **Corrective** | Repairability | A latent comparison hazard |
| M2 | H1 - escape untrusted model output | **Corrective** | Repairability | A stored XSS vector |
| M2 | H2 - Content-Security-Policy and hardening headers | **Preventive** | Evolvability | No defect existed; defence in depth added against future injection |
| M2 | H3 - insecure-default-secret warnings | **Preventive** | Evolvability | No defect; a guard against a future misdeployment |
| M2 | R1 - paginate listings | **Perfective** | Evolvability | A quality improvement anticipating data growth |
| M2 | R2 - intent classifier priority rule | **Corrective** | Repairability | Self-referential questions were mis-ranked |

**Table 14.4 - Distribution, against the typical figures**

| Type | DEICMS | Typical | Difference |
|---|---|---|---|
| Corrective | 11 of 17 (65%) | ~20% | **Far higher** |
| Adaptive | 1 of 17 (6%) | ~20% | Lower |
| Perfective | 3 of 17 (18%) | >50% | **Far lower** |
| Preventive | 2 of 17 (12%) | folded in | - |

The departure is large and it has a straightforward explanation that is worth stating rather than glossing.

**Corrective work dominates here because this is maintenance of a system that has never been operated.** The typical distribution describes a system in production, where users generate a continuous stream of new requirements - which is what makes perfective work the majority. DEICMS has no users and a fixed scope, so there is almost no source of perfective demand. What it does have is a backlog of latent defects accumulated during rapid development and never exposed by operation, and M1 and M2 are the first occasions on which anyone looked for them systematically.

**The single adaptive item is the most realistic of the seventeen**, because it is the only one caused by something genuinely outside the project: the hosted model's latency, and later its retirement. That is what adaptive maintenance actually feels like - an external party changes something and the system must accommodate it, with no defect on anyone's part.

The honest conclusion is that the DEICMS maintenance distribution should **not** be read as evidence about maintenance in general. It is evidence about what happens when a system built quickly is reviewed carefully for the first time, which is a different and narrower phenomenon.

## 14.5 Maintenance Prediction and Cost Factors

Maintenance prediction is concerned with assessing which parts of the system are likely to cause problems and have high maintenance costs. Maintenance costs depend fundamentally on the **number of changes**, and change requests are related to the system components that must be modified.

**Table 14.5 - Maintenance cost factors, assessed for DEICMS**

| Factor | Effect on cost | Position in DEICMS |
|---|---|---|
| **Team stability** | Costs are reduced if the same staff are involved in maintenance, because they already understand the system | **Favourable and unrepeatable.** The maintainer was the author, which is the best possible case - and a case no real project sustains |
| **Contractual responsibility** | If the maintainer is not the developer, there is no incentive during development to design for future change | Not applicable; but the general point is why the anticipation-of-change measures in Table 3.6 were worth taking |
| **Staff skills and domain understanding** | Maintenance staff are often inexperienced and have limited domain understanding, making the system harder to understand and change | Not applicable here, but it is the reason the understandability measures of Section 2.4.11 matter - they are insurance against a maintainer who is not the author |
| **Program age and structure** | As programs age their structure degrades and they become harder to understand and change | Too young to observe. The relevant precaution taken was resisting structural degradation during maintenance itself (law 2, Section 14.2) |
| **Maintenance corrupts structure** | Each round of maintenance makes the next harder, unless structure is actively maintained | Actively resisted in both iterations; see Section 14.2 |

Applying prediction to this system, the components most likely to generate future change are identifiable, and the reasons differ.

**Table 14.6 - Maintenance prediction for DEICMS**

| Component | Predicted change frequency | Why |
|---|---|---|
| `ai_assistant` | **High** | Depends on an external hosted model whose availability and identity are outside the project's control; this has already changed once |
| Risk weights and thresholds | **Medium** | Tuning is expected per deploying organisation - which is why they were made configurable rather than requiring code change (Table 3.6) |
| `chain_reconstruction` | **Medium** | Its four plausibility criteria and 0.40 threshold are heuristics, and heuristics are refined in the light of use |
| Routes and templates | **Medium** | Presentation changes with user feedback, which this project has not yet had |
| `graph_integrity`, `state_machine`, `crypto` | **Low** | They encode legal and procedural rules and use standard primitives; these change on the timescale of legislation, not software |

The prediction has a design consequence that was acted on in advance: the component predicted to change most often is the one deliberately placed behind the narrowest interface - a single method with a fallback (Section 11.6.3). That is anticipation of change applied where prediction says it will be needed.

## 14.6 Evolution Strategy and Maintainability Measures

Table 14.7 records the measures taken during development specifically to make later change cheaper, together with whether each has yet been exercised.

**Table 14.7 - Maintainability measures, and whether they were tested by events**

| Measure | Intended benefit | Exercised? |
|---|---|---|
| Business logic free of framework imports | An algorithm can be changed without touching the web layer | **Yes** - D2 and D5 were single-module fixes |
| Each algorithm behind a single method returning a structured result | Callers are insulated from internal change | **Yes** - the assistant's model-invocation strategy was replaced entirely with no caller change |
| 172 automated tests as a regression net | Change can be attempted safely | **Yes** - the full suite was re-run after every maintenance fix |
| Configurable risk weights and thresholds | Tuning without code change | Not yet |
| ORM with no engine-specific SQL | Database portability | Not yet |
| Lightweight startup schema migration | Columns can be added without rebuilding the database | **Yes** - M2 added two columns to an existing database |
| Git with artefacts versioned alongside code | Diagrams and documentation cannot drift silently from the implementation | **Yes** - throughout |
| Single source of truth for cross-cutting rules | A rule is changed in one place | **Yes** - introduced by M1, and it is the reason a sixth aggregate view would now be scoped correctly by default |

Six of the eight measures have been exercised by real events within the project's own short life. That is a higher proportion than most projects can claim, and it is a direct consequence of having had two genuine maintenance iterations rather than none.

The **forward evolution strategy**, were the system to continue, follows from the prediction in Table 14.6 and from the limitations recorded elsewhere: replace the self-signed certificate and move to PostgreSQL and a production WSGI server (Chapter 17); tighten the Content-Security-Policy to a nonce-based policy (Section 13.5); move rate-limit storage to a shared backend; and revisit the reconstruction heuristics once real usage data exists to calibrate them against. Each of these is a known next step rather than a discovered defect, which is the distinction between planned evolution and unplanned maintenance.

## 14.7 Summary

This chapter treated software evolution and maintenance as the activity that dominates a system's life rather than as a postscript to development. It established why change is inevitable and why maintenance exceeds 60% of lifetime cost, and distinguished evolution from maintenance while noting that DEICMS sits on the boundary between them.

Lehman's eight laws were applied individually and honestly, with four marked as not observable at this scale rather than stretched to fit. Two were argued to be genuinely illustrated: declining quality, in the unexpected internal form of a risk factor whose correctness decayed while its code stood still; and increasing complexity, which both iterations actively resisted by refactoring during the fix rather than patching around it.

The three maintenance types were defined with their typical effort distribution, and all seventeen items delivered in M1 and M2 were classified against them. The resulting distribution departs sharply from the typical figures - 65% corrective against a typical 20% - and the chapter explains why rather than presenting the departure as a finding: this is maintenance of a system that has never been operated, so it has a backlog of latent defects and almost no source of perfective demand.

Maintenance cost factors were assessed, with the note that the most favourable one here - the maintainer being the author - is precisely the condition no real project sustains. Maintenance prediction identified the assistant as the component most likely to change, and recorded that it was already the component placed behind the narrowest interface. Finally, eight maintainability measures were listed with an assessment of which have been exercised by real events; six of the eight have.

The next chapter examines the other side of the same coin: not what the project built and must maintain, but what it deliberately did not build at all.

---

\newpage
