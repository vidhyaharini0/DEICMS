# Chapter 13 - Conclusion

---

## 13.1 Was the Process Choice Right?

Section 4.1.3 recorded four reasons for choosing Scrum, and promised this
section would judge them against what happened rather than against what was
hoped.

**Table 13.1 - The four reasons, assessed**

| Reason claimed at selection | What actually happened | Verdict |
|---|---|---|
| R1 - technical risk sits in work that cannot be specified in advance, and Scrum commits only one sprint at a time | The integrity verifier's traversal semantics **did** change under implementation, from stop-at-first to accumulate-all, on day five of Sprint 2 | **Borne out precisely.** A plan-driven process would have frozen the wrong design in a specification phase and discovered the mismatch during acceptance |
| R2 - the capability tiers have a dependency order that rewards slices | Sprint 2's algorithms needed Sprint 1's records; Sprint 3's assessment needed Sprint 2's verdicts | **Borne out** |
| R3 - feedback between sprints should change the next sprint's plan | Every retrospective action was executed and its effect observed; Sprint 3's burndown is the measurable result of B1 | **Borne out more strongly than expected** |
| R4 - the process must leave behind backlogs, burndowns, reviews and retrospectives | Six of each, in Chapters 6 to 10 | **Borne out** |

**The strongest evidence is one the selection did not anticipate.** Sprints 4,
5 and 6 - the clearest demonstrations of the model's value - were possible
only because working software existed early enough to be probed adversarially,
read critically, and reviewed externally while the project was still running.
A plan-driven project would have found the scoping leak, the dead soft-delete
and the unverified quality requirements after delivery, if at all.

## 13.2 Velocity, Read Honestly

**Table 13.2 - Delivery across the six sprints**

| Sprint | Committed | Delivered | Burndown shape |
|---|---|---|---|
| 1 - Foundation | 40 | 40 | Flat through day two; scaffolding the estimate omitted |
| 2 - Integrity | 38 | 38 | Plateau days five to seven; the traversal rework |
| 3 - Assessment | 42 | 42 | Steadiest; tracked the ideal within two points |
| 4 (M1) - Scoping | 10 | 10 | Short and linear; scope fixed by two change requests |
| 5 (M2) - Defects | - | 11 findings | Measured in findings, not points |
| 6 (M3) - Quality | 23 | 23 | Day four flat; a requirement had to be met before it could be tested |
| **Total** | **153** | **153 + 11** | Mean velocity across the three full sprints: 40.0 |

**Every committed point was delivered, and that should be read sceptically
rather than as success.** It is partly realiztic estimation and stable scope,
and partly an artifact of a single developer in whom estimator and implementer
are the same person - so estimates could be, and unconsciously were, adjusted
to the implementer's known pace. This is risk R-10, rated high-probability and
**accepted rather than mitigated**, because no mitigation exists for one
person.

**The informative signal is the shape of each burndown, not the total.** The
flat start in Sprint 1, the plateau in Sprint 2, the steady tracking in Sprint
3, the stall on day four of Sprint 6 - those say where the work was actually
hard. And it is not a coincidence that the steadiest burndown belongs to the
sprint that had two sprints of retrospective actions behind it.

## 13.3 Achievements and Limitations

**Table 13.3 - Objectives, assessed**

| Objective | Outcome |
|---|---|
| O1 - a working system | ~4,700 source lines; ten blueprints; six entities |
| O2 - access by function **and** membership, on every route and aggregate | Delivered; and failed twice before it was (Ch. 9, 10) |
| O3 - verifiable custody with append-only history | Signed custody events; append-only enforced at the data layer |
| O4 - at least three non-trivial algorithms | **Five**, each with pseudocode and UML (Ch. 11) |
| O5 - third-party services with the boundary stated | Eleven integrations; boundary demonstrated, not asserted (§11.6.1) |
| O6 - a genuine incremental project with artifacts | Six sprints, six backlogs, six burndowns, six retrospectives |
| O7 - a test suite of meaningful coverage | 216 tests; 78% overall, 80% across the Category C algorithms |
| O8 - quality attributes **demonstrably** enforced | 21 of 21 system quality requirements measured and tested |

**Table 13.4 - Consolidated limitations**

| Area | Limitation | Where discussed |
|---|---|---|
| Validation | No customer; requirements never contested by a stakeholder | §12.8 |
| Testing | No concurrency, load, penetration or browser testing; live model behavior untested | §12.7 |
| Coverage | Chain reconstruction at 65%; route paths at 71% | §12.3.1, §12.3.2 |
| Process | Estimator and implementer are the same person | §13.2 |
| Algorithms | Hallucination detection verifies references, not reasoning; the anomaly detector is uninterpretable | §11.6.4 |
| Security | No key-rotation procedure; content-security policy permits inline scripts | §5.5 |
| Deployment | Development server, single process, self-signed certificate | §5.7 |
| Implementation | Sequential identifier allocation unverified under concurrency | §12.7 |

Naming a limitation precisely turns it into a specification for the work that
would remove it, which is what the next section is.

## 13.4 Future Work

**In order of what the report's own evidence says matters most:**

1. **Cover the reconstruction algorithm properly.** 65% is the weakest number
   in the project, and the uncovered branches are combinations of
   partially-present plausibility criteria - exactly where a heuristic is most
   likely to behave unexpectedly.
2. **Calibrate the reconstruction heuristics against real data.** The four
   criteria are equally weighted and the threshold is 0.40 because no usage
   data existed to suggest otherwise.
3. **A key-rotation procedure**, which requires re-encrypting the store under
   a new key while retaining the old.
4. **Concurrency hardening** of sequential identifier allocation, with a test
   harness that can actually exercise it.
5. **Continuous integration.** The suite is fast, deterministic and needs no
   network - the three properties that usually block adoption. The project is
   CI-ready and not CI-practicing, and closing that gap is a small step.

Deferred scope recorded in the backlog's *won't have* list - production
deployment, notifications, full-text search over content, a mobile client, a
multi-language interface, model fine-tuning - is unchanged.

## 13.5 What the Project Demonstrates

**A system.** Six entities, five algorithms implemented from first principles,
eleven third-party integrations with the boundary stated, four roles with
case-level membership, and a history that cannot be rewritten.

**A process.** A development model chosen for stated reasons and judged
against outcomes; a product backlog prioritized, refined and decomposed into
tasks; requirements at two levels, each traced to a test; and twenty-six UML
diagrams written as text descriptions held in the repository beside the code,
which the Definition of Done requires to be updated in the same commit.

**A record of defect detection.** Three of the six sprints arose from defects
found after acceptance: the scoping leak across every aggregate, the integrity
verdict computed and never stored, the repair that went five sprints without a
regression test, the requirement claiming a pagination the code did not
implement, and the role whose guard contradicted its name.

Each was found by a different means - adversarial testing, structured code
reading, and audit against the specification - and in no case did a sprint
detect its own defects. That is the condition under which successive
increments earn their cost, and it is the strongest evidence the project
offers for the process it chose.

---

\newpage
