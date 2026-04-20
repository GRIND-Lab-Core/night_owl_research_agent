---
name: paper-figure-generate
description: 'Generates publication-quality figures and diagrams from output/PAPER_PLAN.md for GIScience, GeoAI, and remote sensing journals (IJGIS, ISPRS JPRS, RSE, TGIS). Decides per-figure whether to produce reproducible code-generated plots/maps or structured prompts for external image-generation models (nano banana, ChatGPT image). Produces figure files, source scripts, captions, manifest, and prompt artifacts. Never fabricates results — uses only evidence from project files.'
argument-hint: [figure-number-or-"all"-or-plan-path]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, WebFetch, mcp__codex__codex, mcp__codex__codex-reply
---

# Skill: paper-figure-generate

You turn the figure plan in **`output/PAPER_PLAN.md`** into manuscript-ready figures for **$ARGUMENTS**. For each figure you decide between a **code-generated** artifact (plots, maps, quantitative panels) and a **prompt-generated** artifact (workflow, architecture, conceptual diagrams) and produce the right deliverable with captions and provenance.

This skill is used when the manuscript needs:
- standard plots for spatial data science studies,
- a heterogeneous mix of figure types (maps + architecture + ablations + graphical abstract),
- diagrams better produced by an external image model,
- figure planning artifacts while some experiments are still in flight.

---

## Constants

- **PLAN_PATH = `output/PAPER_PLAN.md`** — source of truth for figure inventory.
- **FIG_DIR = `output/figures/`** — all figure artifacts.
- **SCRIPT_DIR = `output/figures/scripts/`** — reproducible figure source code.
- **PROMPT_DIR = `output/figures/prompts/`** — external-image-model prompts and design notes.
- **MANIFEST = `output/figures/FIGURE_MANIFEST.md`** — master index of all figures.
- **CAPTIONS = `output/figures/FIGURE_CAPTIONS.md`** — manuscript-ready captions.
- **TARGET_VENUE** — read from `output/PAPER_PLAN.md` header, else `research_contract.md`, else default `IJGIS`.
- **EXPORT_FORMATS = `png, pdf`** — default raster + vector. Add `svg` if diagram will be edited by hand.
- **DPI = 300** — for raster exports.
- **FIG_WIDTH_SINGLE = 3.5in / 89mm** — single-column.
- **FIG_WIDTH_DOUBLE = 7.2in / 183mm** — double-column.

Override via argument (e.g., `/paper-figure-generate Fig03 — venue: ISPRS, formats: png,pdf,svg`).

---

## Core Philosophy

1. **Evidence over aesthetics.** Never invent metrics, coordinates, or labels. If the evidence is not in the project files, produce a *specification stub* and stop — do not fill with plausible-looking data.
2. **Two honest pathways.** Every figure is either reproducible (code + data → image) or schematic (prompt → image). Pick one deliberately per figure; justify in the manifest.
3. **Publication discipline.** Restrained typography, consistent palette, legible at print size, grayscale-readable where feasible. No marketing gloss.
4. **Consistency across the paper.** Same fonts, line widths, terminology, dataset names, and notation as the manuscript.
5. **Graceful degradation.** Missing data → stub + TODO; partial system knowledge → draft prompt + assumptions list. Never silent guesses.

---

## Phase 1 — Read and Interpret `PAPER_PLAN.md`

1. Read `output/PAPER_PLAN.md` fully. Locate:
   - the **Figure Plan** table (IDs, types, priorities),
   - the **Hero Figure** description,
   - the **Claims-Evidence Matrix** / `memory/APPROVED_CLAIMS.md`,
   - Methods and Results sections that reference specific figures/tables,
   - any figure draft notes, mockups, or placeholder captions.
2. Resolve the target venue from the plan header (e.g., `Target: IJGIS`). Apply venue norms (column width, grayscale-safe palette, line-figure vs. color policy).
3. Build an **internal figure registry**. For each figure extract:

   | Field | Notes |
   |---|---|
   | `id` | `Fig01`, `Fig02`, … — zero-padded. |
   | `title` | Short, manuscript-ready. |
   | `purpose` | Scientific message, one sentence. |
   | `key_message` | What a skim reader should take away. |
   | `claim_refs` | IDs from `APPROVED_CLAIMS.md` (if any). |
   | `data_source` | Path(s) or `MISSING`. |
   | `figure_type` | From the taxonomy below. |
   | `pathway` | `code` or `prompt` (Phase 3). |
   | `priority` | HIGH / MEDIUM / LOW from plan. |
   | `status` | `ready` / `stub` / `draft-prompt` / `blocked`. |
   | `annotations` | Labels, arrows, callouts required. |
   | `dependencies` | Tables, experiments, scripts it depends on. |

   Persist this registry inline in the manifest (Phase 6). Do **not** write it to a separate JSON unless the user asks.

4. If `PAPER_PLAN.md` is missing or incomplete, attempt in order:
   - read linked result files (`output/results/`, `output/spatial-analysis/`, `output/reports/`),
   - read `memory/APPROVED_CLAIMS.md` + `memory/OUTLINE.md`,
   - infer the smallest defensible figure set, and mark every inferred row with `assumption: inferred from <source>` in the manifest.

---

## Phase 2 — Figure Type Taxonomy

Choose the type that best serves the scientific message, not the one that looks nicest.

| Family | Types |
|---|---|
| **Maps** | study-area map, choropleth, spatial distribution, bivariate map, hot-spot (LISA/Gi\*), error/residual map, change map, inset panels. |
| **Quantitative plots** | bar, grouped bar, line, scatter, scatter-with-fit, box, violin, ECDF, heatmap, confusion matrix, calibration plot. |
| **Ablation / sensitivity** | ablation bars with reference line, sensitivity heatmap, tornado plot. |
| **Remote sensing panels** | multi-band image grid, before/after, multi-temporal stack, ground-truth vs. prediction panel. |
| **Qualitative case studies** | image+label panels, attention/overlay visualizations. |
| **Diagrams (prompt-friendly)** | system architecture, workflow/pipeline, conceptual framework, module interaction, graphical abstract, layered platform schematic, human-in-the-loop diagram, data-engine-model-output pipeline. |

**Map defaults** (any map family): scale bar, north arrow, projection + EPSG in caption, legend with units, inset showing regional context, classification scheme stated (quantile / Jenks / equal-interval), class count justified.

---

## Phase 3 — Decide Production Pathway (code vs. prompt)

Apply this decision rule per figure. Record the reason in the manifest.

**Use `code` when any of these hold:**
- the figure depicts real metrics, distributions, or coordinates,
- results must be reproducible from script + data,
- reviewers may ask to regenerate with new data or parameters,
- the figure shows spatial patterns tied to actual geography,
- the figure is a table rendered as a figure.

**Use `prompt` when all of these hold:**
- the figure is primarily structural, conceptual, or schematic,
- no numeric plotting is required,
- the content is labels + boxes + arrows + grouping + style,
- a clean, journal-styled rendering from an image model will be faster than laboriously drawing it in `matplotlib` / `graphviz` / TikZ, **and** editorially acceptable for the target venue.

**Hybrid exception.** If the diagram needs both schematic structure *and* a small embedded real chart (e.g., architecture + mini accuracy bars), generate the chart in code, export as a transparent PNG, and note in the prompt that the rendered diagram should leave a placeholder region for it.

Venue caveat: some venues require vector, hand-editable figures. If so, default `prompt` outputs to **prompt + hand-traceable**: produce the prompt for ideation, but also emit a skeleton `mermaid` / `graphviz` / TikZ file the author can tidy into vector form.

---

## Phase 4 — Produce Code-Generated Figures

For each `code` figure:

1. **Locate evidence.** Grep the paths in `data_source`. If missing, switch `status = stub` and skip to the stub template (Phase 4c).
2. **Prefer existing tooling.** Before writing new code, check whether `output/figures/scripts/visualize.py` (used by `paper-figure`) already supports the figure type. Reuse it with explicit CLI arguments.
3. **Otherwise write a focused script** at `output/figures/scripts/{id}_{slug}.py`:
   - single purpose, < ~120 lines,
   - reads data by explicit path (no hard-coded magic),
   - exports to `FIG_DIR/{id}_{slug}.png` **and** `.pdf` at `DPI`,
   - sets figure width from `FIG_WIDTH_SINGLE` or `FIG_WIDTH_DOUBLE`,
   - uses the palette/typography defaults below.
4. **Run the script** from repo root: `python output/figures/scripts/{id}_{slug}.py`.
5. **Verify output** exists, has non-trivial size, opens without error.
6. **Record** the script path and command in the manifest row.

### 4a. Style defaults for code figures

- Font: a single sans-serif (e.g., Arial, Helvetica, DejaVu Sans) at 8–10 pt for body, 10–12 pt for title, 7–8 pt for tick labels.
- Line weights: 0.8–1.2 pt for axes, 1.2–1.8 pt for data lines.
- Palette: colorblind-safe, ≤ 6 hues. For maps prefer ColorBrewer sequential / diverging appropriate to the variable. Avoid rainbow.
- Grayscale test: if the figure loses meaning in grayscale, add a second channel (line style, marker shape, hatching).
- Whitespace: no unnecessary frames. Remove top/right spines unless they carry meaning.
- Legends: inside the axes when possible, single column, no redundant titles.
- Units: always in axis labels and colorbar labels.

### 4b. Map-specific checks

- Projection and EPSG stated in caption.
- Scale bar, north arrow, legend, inset — add or log a TODO if any is missing.
- Classification: state method + number of classes. Avoid 7+ classes for categorical color.
- No classification scheme that creates misleading clusters (e.g., equal-interval on highly skewed data).

### 4c. Stub template (data missing)

When `data_source = MISSING`, write a **specification stub** to `SCRIPT_DIR/{id}_{slug}.py` containing:
- a module docstring describing the intended figure,
- a TODO list of required inputs,
- a commented `pandas.read_*` call with the expected schema,
- a `matplotlib` skeleton that raises `NotImplementedError("data required: ...")` when run.

Also emit `FIG_DIR/{id}_{slug}_SPEC.md` with: purpose, required data, expected axes, legend, and a short rationale for why the stub cannot be filled yet.

Set `status = stub` in the manifest and list the blocker in `missing_inputs`.

---

## Phase 5 — Produce Prompt-Generated Figures

For each `prompt` figure, write **three artifacts**:

1. `output/figures/prompts/{id}_prompt.md` — the authoritative design document (see template below).
2. `output/figures/prompts/{id}_prompt.txt` — the final ready-to-paste prompt text (no front matter, no explanation).
3. `output/figures/prompts/{id}_design_notes.md` — assumptions, revision checklist, second-pass prompt guidance.

Save the rendered image (once the user supplies it) at `FIG_DIR/{id}_{slug}.png`. Do not fabricate renders.

### 5a. Required prompt contents

Every prompt must include, in order:

1. **Objective** — one sentence on what the figure communicates.
2. **Figure type** — e.g., "system architecture diagram", "workflow schematic", "conceptual framework".
3. **Target journal style** — e.g., "IJGIS — restrained, two-column compatible, print-legible".
4. **Audience** — e.g., "GIScience / GeoAI researchers".
5. **Layout instructions** — number of layers / columns / rows, grouping panels, reading order, aspect ratio (e.g., `16:9` widescreen or `3:2`).
6. **Element inventory** — every box, node, module, lane, or panel, with exact labels.
7. **Relationships** — every arrow / line, its direction, and what it means.
8. **Text labels to include** — verbatim; the model must render them as shown.
9. **Style constraints** — background, palette, line weights, box shapes, icon policy.
10. **Rendering constraints** — resolution, aspect ratio, margin, language (English).
11. **Negative prompt / avoidance** — bullets of what the render must not do.
12. **Short prompt version** — ≤ 60 words, for quick iteration.
13. **Long prompt version** — detailed, paste-ready.

### 5b. Prompt style defaults (bias the model toward these)

- Clean white or subtle neutral background; no decorative gradient.
- Restrained scientific palette — 3–5 muted hues + one accent color for emphasis.
- Rounded rectangles with thin 1–1.5 pt strokes; no drop shadows, no 3-D bevels.
- Sans-serif labels, medium weight, high contrast.
- Explicit arrow directions; no ambiguous double-headed arrows unless the relationship is symmetric.
- Grouping via light-tinted background panels or subtle dashed borders — not saturated color blocks.
- Widescreen layout for architecture/workflow figures; portrait for graphical abstracts.
- Journal-suitable, not marketing-suitable.

### 5c. Required negative prompt

Always include variants of:
- no 3-D shiny icons, no glossy buttons, no reflective surfaces;
- no cartoon or comic styling;
- no stock-photo people;
- no decorative backgrounds, no world-map wallpaper;
- no invented numbers, metrics, or chart-like decorations inside the diagram;
- no unreadable micro-labels;
- no random geographic symbols unrelated to the paper;
- no text in languages other than the manuscript language;
- no watermark, no vendor logo, no signature.

### 5d. Assumptions and iteration

`{id}_design_notes.md` must contain:
- **Assumptions** — every label, grouping, or relationship inferred from context rather than stated explicitly in `PAPER_PLAN.md`. Tag each with the source file + section.
- **Revision checklist** — boxes to tighten, labels to shorten, arrows to reposition once the first render is seen.
- **Second-pass prompt hook** — a placeholder the user fills in after viewing pass 1 ("after render: check that module X is upstream of Y; if not, …").
- **Confirmation list** — modules, datasets, or relationships the author should verify before the figure ships.

If the system/workflow is only partially documented, produce a **conservative draft prompt** (only structure that is clearly supported) and surface the rest as `needs_confirmation`. Do not invent modules to make the diagram look complete.

---

## Phase 6 — Captions, Manifest, Provenance

### 6a. `FIGURE_CAPTIONS.md`

For each figure (code or prompt), append a manuscript-ready caption:

```markdown
**Figure N.** [What is shown]. [Data source / experiment ID / CRS + EPSG if a map]. [One sentence of key takeaway that states the finding or structural message, aligned with claim IDs if applicable].
```

Captions must:
- be self-contained (readable without the body text),
- state CRS/EPSG for every map,
- cite dataset names consistent with the Methods section,
- state sample size / time period where relevant,
- never contain numbers that are not in `APPROVED_CLAIMS.md` or the source file.

### 6b. `FIGURE_MANIFEST.md`

Maintain a single manifest with one row per figure:

```markdown
| ID | Title | Type | Pathway | Priority | Status | Data Source | Script / Prompt | Claims | Missing Inputs | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Fig01 | NORA system architecture | architecture | prompt | HIGH | draft-prompt | - | prompts/Fig01_prompt.md | C1,C2 | - | widescreen, 4 layers |
| Fig02 | Study area, CONUS counties | choropleth map | code | HIGH | ready | data/processed/counties.geojson | scripts/Fig02_study_area.py | C1 | - | EPSG:5070 |
| Fig03 | Local R² by county | choropleth map | code | HIGH | stub | output/results/mgwr_results.json | scripts/Fig03_local_r2.py | C3 | mgwr_results.json | blocked on experiment |
```

Also include a short prose summary at the top: venue, total figures, counts by pathway, counts by status, outstanding blockers.

### 6c. Filename conventions

- Figures: `FIG_DIR/{id}_{slug}.{png,pdf,svg}` — `id` is `Fig01` etc., `slug` is short kebab-case.
- Scripts: `SCRIPT_DIR/{id}_{slug}.py`.
- Prompts: `PROMPT_DIR/{id}_prompt.md`, `{id}_prompt.txt`, `{id}_design_notes.md`, optional `{id}_assumptions.md` if long.
- Specs (stubs): `FIG_DIR/{id}_{slug}_SPEC.md`.

### 6d. Consistency pass (always run before finishing)

After all figures are produced, do one pass across the set and verify:
- figure numbering is contiguous and matches `PAPER_PLAN.md`,
- typography, line widths, and palette are shared across code figures,
- terminology (model names, dataset names, metric names, region names) matches the manuscript and `APPROVED_CLAIMS.md`,
- diagram labels in prompt figures match code figure axis labels,
- every caption in `FIGURE_CAPTIONS.md` has a manifest row and vice versa,
- no caption contains a number absent from `APPROVED_CLAIMS.md`.

Log any inconsistencies at the top of the manifest under `## Consistency Issues`.

---

## Decision Rules (quick reference)

| Situation | Action |
|---|---|
| Plan lists a figure but no data exists | Emit stub script + `_SPEC.md`, set `status=stub`, list blocker. |
| Plan lists a conceptual/system figure | Use `prompt` pathway. |
| Plan lists a hero figure mixing schematic + real metrics | Hybrid: code chart + prompt diagram with placeholder region. |
| Venue requires vector | Default `prompt` figures to produce a companion `mermaid`/`graphviz` skeleton. |
| Map without CRS/scale info | Add TODO in caption; do not silently omit. |
| Finding needed for caption not in `APPROVED_CLAIMS.md` | Write caption without the number and tag `[NEEDS CLAIM]`. |
| Plan missing entirely | Infer minimum viable figure set from claims + results; mark all as `inferred`. |
| User asks for a single figure ID | Restrict work to that ID; do not regenerate others. |

---

## Guardrails

- **Never fabricate** results, coordinates, metrics, dataset names, or module names.
- **Never classify a map** in a way that visually amplifies a pattern not supported by the data (e.g., custom breaks that manufacture clusters).
- **Never produce flashy, 3-D, or marketing-styled renders.** If the prompt tends that way, strengthen the negative prompt.
- **Never overload** a figure with text — if a panel has more than ~8 labels, split it.
- **Never let diagram labels conflict** with `PAPER_PLAN.md`. If the plan says "Agent A" and the architecture says "Scout", pick one and update the other.
- **Never skip** the consistency pass (Phase 6d).
- **Never delete** an existing `FIGURE_MANIFEST.md` or `FIGURE_CAPTIONS.md` — append / edit in place so provenance is preserved.
- **Never run destructive shell commands** and never modify files outside `FIG_DIR`, `SCRIPT_DIR`, `PROMPT_DIR`, and `output/` generally.

---

## Outputs

- `output/figures/{id}_{slug}.png` and `.pdf` (and `.svg` when justified) — rendered code figures.
- `output/figures/scripts/{id}_{slug}.py` — reproducible figure source.
- `output/figures/{id}_{slug}_SPEC.md` — specification stubs when data are missing.
- `output/figures/prompts/{id}_prompt.md` / `.txt` / `_design_notes.md` — prompt artifacts for external image models.
- `output/figures/FIGURE_MANIFEST.md` — master index + consistency log.
- `output/figures/FIGURE_CAPTIONS.md` — manuscript-ready captions.
- Update `memory/OUTLINE.md` Figures section with paths and `status`.
- Append a one-line entry per generated figure to `output/PROJ_NOTES.md` (e.g., `Fig03 stub — waiting on mgwr_results.json`).

---

## Relationship to Other Skills

- **`paper-plan`** produces `PAPER_PLAN.md` (this skill's input). If the plan is missing, invoke `paper-plan` first rather than fabricating one.
- **`paper-figure`** handles the standard spatial-regression figure pipeline via `visualize.py`. When the paper is a pure spatial-regression study, prefer `paper-figure`. Use `paper-figure-generate` for mixed / systems / GeoAI / benchmark papers and whenever diagram prompts are needed.
- **`result-to-claim`** is the safety gate: do not place a number in a caption unless it is in `memory/APPROVED_CLAIMS.md`.
- **`submit-check`** consumes `FIGURE_MANIFEST.md` and `FIGURE_CAPTIONS.md` — keep them in journal-ready shape.

---

## Invocation

```
/paper-figure-generate                      # generate / refresh all figures in PAPER_PLAN.md
/paper-figure-generate Fig03                # generate a single figure
/paper-figure-generate "all — venue: ISPRS" # override venue
/paper-figure-generate prompts-only         # only regenerate prompt artifacts
/paper-figure-generate code-only            # only regenerate code figures
```

See `templates/prompt_template.md` and `templates/manifest_template.md` in this skill folder for the canonical artifact shapes.
