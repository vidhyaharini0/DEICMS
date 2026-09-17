# PlantUML diagram sources

All UML diagrams for the DEICMS report, written as PlantUML text.

## How to render

**Option 1 — online (no install):**
Go to <https://www.planttext.com> or <https://www.plantuml.com/plantuml>,
paste the contents of a `.puml` file, and export as PNG or SVG.

**Option 2 — VS Code:**
Install the "PlantUML" extension by jebbs, open a `.puml` file,
press `Alt+D` to preview, right-click to export.

**Option 3 — command line:**
`java -jar plantuml.jar -tpng *.puml`

## Style

Every file begins with the same four style lines:

```
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 12
```

`monochrome true` is what removes all colour — everything renders as
black line art on white, with no green/blue differentiation.

## Files

| File | Figure | Diagram type |
|---|---|---|
| `01_use_case.puml` | 7.1 | Use case |
| `02_class.puml` | 7.4 | Class |
| `03_er.puml` | 7.5 | Entity-relationship |
| `04_state_lifecycle.puml` | 7.9 | State machine |
| `05_sequence_integrity.puml` | 7.6 | Sequence |
| `06_sequence_ai.puml` | 7.10 | Sequence |
| `07_activity_risk.puml` | 7.7 | Activity |
| `08_activity_reconstruction.puml` | 7.8 | Activity |
| `09_component.puml` | 7.11 | Component |
| `10_deployment.puml` | 7.12 | Deployment |

The three burndown charts are not UML and remain as the existing SVG files
in `diagrams/`.
