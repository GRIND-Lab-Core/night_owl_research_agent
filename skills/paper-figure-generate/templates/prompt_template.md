# Prompt Template — External Image-Generation Model

Use this template verbatim when producing `output/figures/prompts/{id}_prompt.md`. Fill every section. If a section does not apply, write `n/a — <reason>`; do not delete it.

---

## Figure Metadata

- **ID:** Fig0N
- **Title:** <manuscript-ready short title>
- **Pathway:** prompt
- **Target journal:** <IJGIS | ISPRS JPRS | RSE | TGIS | …>
- **Why prompt-based:** <one sentence — e.g., "schematic system architecture, no numeric content">
- **Aspect ratio:** <16:9 widescreen | 3:2 | 1:1 graphical abstract>
- **Intended print size:** <single-column 89 mm | double-column 183 mm | full page>

---

## 1. Objective

<one sentence on what the figure must communicate to a skim reader>

## 2. Figure Type

<system architecture | workflow schematic | conceptual framework | graphical abstract | layered platform | module interaction map | human-in-the-loop diagram | data-to-paper pipeline>

## 3. Scientific Message

<2–3 sentences: what the figure proves, which claim(s) it supports (cite claim IDs), what a reviewer should notice first>

## 4. Layout

- Orientation: <landscape | portrait>
- Grid / structure: <e.g., "4 horizontal layers, top-to-bottom">
- Reading order: <e.g., "top-left → bottom-right, left-to-right within each layer">
- Whitespace policy: generous, balanced, no edge-crowding.

## 5. Element Inventory

For every box/module/panel, list: label (verbatim), role, grouping layer.

| Label | Role | Layer / Group |
|---|---|---|
| <exact text> | <what this module does> | <Layer 1 / Data> |
| … | … | … |

## 6. Relationships / Arrows

For every edge: source → target, direction, meaning, line style.

| From | To | Direction | Meaning | Style |
|---|---|---|---|---|
| <A> | <B> | → | "sends parsed docs to" | solid 1.2 pt |
| <B> | <C> | ⇄ | "bidirectional feedback" | dashed 1 pt |

## 7. Labels & Text to Render Verbatim

Bulleted list of every text string that must appear in the rendered figure, exactly as written. Use quotes.

- "NORA Orchestrator"
- "Literature Scout"
- …

## 8. Style Constraints

- Background: clean white (or very light neutral `#F7F8FA`).
- Palette: 3–5 muted hues + 1 accent color for the critical path.
- Shapes: rounded rectangles, thin stroke 1–1.5 pt, no shadow, no bevel.
- Typography: sans-serif, medium weight, high contrast. Label size legible at target print size.
- Icons: flat, line-based, minimal. No 3-D, no gloss, no stock photography.
- Grouping: light tinted panels or dashed borders, not saturated color fills.

## 9. Journal Suitability

<sentence stating why this rendering will read as academic, not marketing; e.g., "restrained palette, consistent thin strokes, labels legible at 89 mm print width">

## 10. Rendering Constraints

- Resolution: ≥ 300 DPI at target print size (or vector).
- Margins: ≥ 3% on every side.
- Language: English only.
- No watermark, no vendor logo, no signature.

## 11. Negative Prompt — Must Avoid

- no 3-D shiny icons, no glossy buttons, no reflective surfaces
- no cartoon, comic, or infographic styling
- no stock-photo people
- no decorative world-map or satellite-photo backgrounds
- no fabricated numbers, charts, or metric-like decorations inside the diagram
- no unreadable micro-labels
- no geographic symbols unrelated to the paper's study area
- no text in non-English languages
- no watermark, no vendor logo

## 12. Short Prompt (≤ 60 words)

<paste-ready one-paragraph prompt for quick iteration>

## 13. Long Prompt (detailed, paste-ready)

<full paragraph(s) consolidating sections 1–11 into a single prompt that can be pasted into nano banana / ChatGPT image generation / comparable tool>

## 14. Assumptions

- <every inferred module, grouping, or relationship, with the source file + section that justified it>
- …

## 15. Revision Checklist (after first render)

- [ ] All module labels render exactly as written
- [ ] Arrow directions correct (no reversed edges)
- [ ] Grouping panels match Section 5
- [ ] No fabricated charts inside diagram boxes
- [ ] Labels legible at target print size
- [ ] Palette restrained; no marketing feel
- [ ] Grayscale-readable (line styles / shape differences preserved)

## 16. Second-Pass Prompt Hook

<template text the author fills in after viewing pass 1 — e.g., "after render: if module X appears downstream of Y, swap their vertical positions and regenerate with the same palette">

## 17. Needs Confirmation

- <modules, edges, or labels the author must verify before submission>
