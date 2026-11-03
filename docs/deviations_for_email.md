## 1.6 Relationship to the Accepted Proposal

The project proposal approved before implementation specified the Agile
Incremental Model, three increments, five entities, three core algorithms plus
a state machine and an orchestration workflow, and a report structured with
one section per increment.

**Table 1.4 - Deviations from the accepted proposal**

| Proposed | Delivered | Why |
|---|---|---|
| Agile Incremental Model | **Scrum**, an agile incremental framework, with its artefacts implemented | The proposal named the family; §4.1.3 names the member and commits to its artefacts |
| Three increments | **Six sprints** - three planned, three arising from findings | Sprints 4, 5 and 6 each exist because something was found wrong (Ch. 9, 10) |
| Five entities | **Six** - `CaseAccess` added | Case-level membership proved to need its own associative entity (Sprint 4) |
| Six risk signals, three risk levels | **Eight signals, four levels** | Two further signals proved discriminating; a fourth band separated the genuinely critical |
| A named commercial language-model API | **A different hosted model** | The named service was unavailable on terms the project could meet. The requirement never named a vendor, so this changed the design and not the requirements (§3.1.1, §11.6.1) |
| Test coverage above 70% | **78%**, 216 tests | - |

**Every deviation is an addition or a substitution forced by circumstance;
none removes something promised.** They are collected here rather than
scattered, so that a reader holding the proposal can check the delivery
against it in one place.

## 1.7 How to Read This Report

The report is organised according to the development process it used, as the
guidelines require of an incremental model: **one chapter per sprint**, each
containing that sprint's own backlog, tasks, models, tests, burndown, review
and retrospective.

**Table 1.5 - Structure**

| Chapters | Content |
|---|---|
| 1-2 | The problem, and the feature categorisation with its balance self-assessment |
| 3-5 | Requirements at two levels, the process and its justification, the architecture |
| **6-10** | **The six sprints, one chapter each** |
| 11 | The five Category C algorithms, each with pseudocode and UML |
| 12-13 | Verification and validation; conclusions |

Three things are deliberately *not* in this report. There is no restatement of
software-engineering theory: the process is described where it was used, not
in a chapter of its own. There is no diagram that is not UML, and every one is
generated from versioned source so it cannot drift from the code. And there is
no claim of a flawless result - the three maintenance sprints are described at
the same length as the three that went to plan, because a process is
demonstrated by what it catches, not by what it avoids.

