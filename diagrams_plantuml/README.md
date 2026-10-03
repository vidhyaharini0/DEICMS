# PlantUML diagram sources

All UML diagrams for the DEICMS report, written as PlantUML text.

## How to render

**Option 1 - online (no install):**
Go to <https://www.planttext.com> or <https://www.plantuml.com/plantuml>,
paste the contents of a `.puml` file, and export as PNG or SVG.

**Option 2 - VS Code:**
Install the "PlantUML" extension by jebbs, open a `.puml` file,
press `Alt+D` to preview, right-click to export.

**Option 3 - command line:**
`java -jar plantuml.jar -tpng *.puml`

## Style

Every file begins with the same four style lines:

```
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 12
```

`monochrome true` is what removes all colour - everything renders as
black line art on white, with no green/blue differentiation.

## Files

| File | Figure | Diagram type |
|---|---|---|
| `01_use_case.puml` | 8.1 | Use case |
| `02_class.puml` | 8.2 | Class |
| `03_er.puml` | 8.3 | Entity-relationship |
| `04_sequence_integrity.puml` | 8.4 | Sequence |
| `05_sequence_ai.puml` | 8.5 | Sequence |
| `06_activity_risk.puml` | 8.6 | Activity |
| `07_activity_reconstruction.puml` | 8.7 | Activity |
| `08_state_lifecycle.puml` | 8.8 | State machine |
| `09_component.puml` | 8.9 | Component |
| `10_deployment.puml` | 8.10 | Deployment |

All ten are deliberately kept small enough to redraw by hand in a few minutes.


Rendered PNGs of all eleven are in `../diagrams_png/`, produced with
`java -jar plantuml.jar -tpng -o ../diagrams_png *.puml`.

The three burndown charts are not UML and remain as the existing SVG files
in `diagrams/`.
