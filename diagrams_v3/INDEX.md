# UML Diagram Set (v3)

Twenty-two diagrams, every one of them UML. The previous set contained an
entity-relationship diagram and block-style architecture figures, neither of
which is UML notation; both have been replaced by UML equivalents.

Each diagram is a `.puml` text file in this folder, versioned alongside the
application code. Definition of Done condition 7 requires a diagram and the
code it illustrates to change in the same commit. Rendering:

```
java -jar plantuml.jar -tpng -o . *.puml
```

## The set, by UML diagram kind

| # | File | UML kind | Subject |
|---|---|---|---|
| 01 | `01_usecase_overview` | Use case | Four actors, 41 use cases grouped, actor specialisation |
| 02 | `02_usecase_case_evidence` | Use case | Cases and evidence, with `«include»` |
| 03 | `03_usecase_reading` | Use case | The 20 use cases of the Read-Only Viewer, the base actor |
| 04 | `04_usecase_analysis` | Use case | What each role ADDS: Analyst +5, Lead +7, Administrator +9 |
| 05 | `05_class_domain` | Class | Domain model: attributes, operations, visibility, `«engine»` classes |
| 06 | `06_class_persistent` | Class | The relational schema as stereotyped classes - **replaces the ER diagram** |
| 07 | `07_object_snapshot` | Object | One flagged evidence item at an instant, with the two violations visible |
| 08 | `08_package_layers` | Package | Five layers and their permitted dependencies - **replaces a block figure** |
| 09 | `09_component` | Component | Components, provided and required interfaces |
| 10 | `10_composite_verifier` | Composite structure | Internals of the integrity engine |
| 11 | `11_deployment` | Deployment | Nodes, execution environments, artifacts, trust boundary |
| 12 | `12_sequence_integrity` | Sequence | Chain integrity verification |
| 13 | `13_sequence_assistant` | Sequence | Assistant orchestration, with the `alt` fallback |
| 14 | `14_communication_risk` | Communication | Risk assessment, organised by structure |
| 15 | `15_state_evidence` | State machine | Evidence lifecycle: 6 states, 14 transitions |
| 16 | `16_state_account` | State machine | Account access, with a composite state |
| 17 | `17_activity_risk` | Activity | Multi-factor risk assessment, with `fork`/`join` |
| 18 | `18_activity_reconstruction` | Activity | Chain reconstruction, with the plausibility loop |
| 19 | `19_activity_upload` | Activity | Evidence registration, with partitions (swimlanes) |
| 20 | `20_timing_assistant` | Timing | Bounded waiting on the model service |
| 21 | `21_profile_stereotypes` | Profile | Every stereotype this report uses, declared |
| 22 | `22_class_traceability` | Class | The traceability metamodel itself |
| 23 | `23_activity_integrity` | Activity | Chain integrity verification (Algorithm 1) |
| 24 | `24_activity_state_machine` | Activity | The lifecycle transition validation pipeline (Algorithm 4) |
| 25 | `25_sequence_reconstruction` | Sequence | Custody chain reconstruction (Algorithm 3) |
| 26 | `26_activity_assistant` | Activity | Assistant orchestration, six stages (Algorithm 5) |

## UML coverage of the five Category C algorithms

The guidelines require the complex custom logic to be described
algorithmically by proper UML diagrams. Each algorithm has at least two
independent behavioural views:

| Algorithm | Diagrams |
|---|---|
| 1. Chain integrity verification | 23 activity, 12 sequence, 10 composite structure |
| 2. Multi-factor risk assessment | 17 activity, 14 communication |
| 3. Custody chain reconstruction | 18 activity, 25 sequence |
| 4. Evidence lifecycle state machine | 15 state machine, 24 activity |
| 5. Assistant orchestration | 26 activity, 13 sequence, 20 timing |

**Eleven distinct UML diagram kinds**: use case, class, object, package,
component, composite structure, deployment, sequence, communication, state
machine, activity, timing, profile.

## Corrections made in this revision

| Issue | Was | Now |
|---|---|---|
| **Generalisation / specialisation inverted** | The text read "the Analyst *generalises* the Read-Only Viewer". Backwards: the parent generalises, the child specialises | The Read-Only Viewer is the most general actor; the Analyst **specialises** it, the Lead specialises the Analyst, the Administrator specialises the Lead. Stated that way in both the diagrams and the text |
| **`«extend»` drawn backwards** | An arrow from the base use case to the extending one | `«extend»` now points **from the extending use case to the base**: "Present second factor" extends "Sign in", "Reconstruct" extends "Verify" |
| **Login as an included use case** | `Register evidence ..> Log in : «include»` | Removed. Authentication is a **precondition of the subject**, not a step repeated inside each use case. Noted on the diagram so the omission reads as a decision |
| **Only 12 of 41 use cases shown** | One diagram, 12 use cases | An overview plus three detail diagrams covering all 41, one per system operation |
| **Role named wrongly throughout** | "Read-Only Auditor" - a name that exists nowhere in the system | **Read-Only Viewer**, the name the seeded account actually carries; the role value is `Read-Only` |
| **Global audit trail attributed to the wrong role** | Drawn on the Read-Only actor | It is `is_admin()` only, in the route and in the sidebar. Moved to the Administrator |
| **Verification drawn as a read** | Drawn on the Read-Only actor | Running a verification writes `integrity_status` and can drive an item to Flagged. It is an Analyst operation; a role guard now enforces it (SR-06) |
| **ER diagram is not UML** | `entity` notation | A class diagram with `«table»`, `«PK»`, `«FK»`, `«UQ»` stereotypes, declared in the profile diagram |
| **Architecture figures are not UML** | Block diagrams | A package diagram for the layering and a component diagram for the interfaces |
| **Stereotypes used but never defined** | `«engine»`, `«value»`, `«external»` used without declaration | Declared in diagram 21 |

## Why the data model is a class diagram rather than an ER diagram

The guidance is to use UML throughout, including for data structure. UML has
its own extension mechanism - stereotypes - so a relational schema can be
expressed as stereotyped classes without importing a second notation. Diagram
06 does exactly that, and diagram 21 declares the stereotypes it uses.

Placing diagrams 05 and 06 side by side also makes the distinction between the
two models visible rather than asserted: the three `«engine»` classes in 05
hold behaviour and persist nothing, so they are **absent** from 06 altogether.
That absence is the clearest single statement of what separates a design model
from a data model.
