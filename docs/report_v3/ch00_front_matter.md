::: {custom-style="TitlePage"}
University of Messina

Department of Mathematics, Computer Sciences,
Physical Sciences and Earth Sciences (MIFT)

Bachelor's Degree in Data Analysis

**DEICMS**

Digital Evidence Integrity & Chain-of-Custody Management System

Agile Incremental Model - Scrum

Software Engineering Project Report

Submitted to: Prof. Salvatore Distefano

Prepared by: Vidhya Harini Vijayarajan Sangeetha

Student ID: 533994

Academic Year: 2025 / 2026

Revised Submission - November 2026
:::

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Abstract

DEICMS is a web application for managing digital forensic evidence, built so
that tampering with an exhibit is either impossible or evident, every action
is attributable to the person who performed it, and the system's own history
cannot be rewritten.

The system is organised around **five guarantees**: an exhibit's content can
be shown unchanged since intake or shown precisely where it changed; a person
sees only the investigations they are assigned to, in every view without
exception; the record of what happened is complete and unalterable; an exhibit
moves only as its procedure permits; and exhibits can be prioritised by the
attention they need, with the reasoning exposed.

Its functionality is categorised across the three required categories and
**self-assessed for balance on four independent measures**. Thirty
data-oriented functionalities realise the entity model and its formulae.
Eleven third-party integrations are consumed as they are, with the boundary
stated in each case. **Five algorithms are designed and implemented in this
project**: chain integrity verification over a directed acyclic graph of
custody events, multi-factor risk assessment with per-indicator normalisation
and bounded interaction effects, heuristic custody-chain reconstruction that
declines to infer below a plausibility threshold, a role-gated
precondition-constrained lifecycle automaton, and a six-stage orchestration
pipeline around a language model. By estimated effort these account for 43% of
the project and by source size 42%; the whole of the third-party category is
439 lines, less than any two of the five algorithm modules combined.

The project followed **Scrum**, an agile incremental framework, across six
sprints. Three delivered the planned system. The remaining three exist because
something was found wrong - by adversarial testing, by structured code
reading, and by external review respectively - and each is described here at
the same length as the sprints that went to plan. This report is organised
with **one chapter per sprint**, each carrying that sprint's backlog, tasks,
UML models, tests, burndown, review and retrospective, and with a dedicated
chapter describing each complex algorithm through UML behavioural diagrams.

The delivered system comprises approximately 4,700 source lines across ten
blueprints and six entities, verified by **216 automated tests** reaching 78%
statement coverage overall and 80% across the five algorithms, with every one
of the twenty-one system quality requirements carrying a measurement, an
acceptance value and a named test. Twenty-six UML diagrams are generated from
versioned source, so no figure in this report can contradict the code it
describes.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Table of Contents

```{=openxml}
<w:sdt><w:sdtPr><w:docPartObj><w:docPartGallery w:val="Table of Contents"/><w:docPartUnique/></w:docPartObj></w:sdtPr><w:sdtContent><w:p><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/><w:instrText xml:space="preserve">TOC \o "1-2" \h \z \u</w:instrText><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>Right-click and choose "Update Field" to build the table of contents.</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:sdtContent></w:sdt>
```

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```
