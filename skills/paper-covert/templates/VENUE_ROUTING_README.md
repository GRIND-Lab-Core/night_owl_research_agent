# Venue Routing

> How `paper-covert` maps a target venue to LaTeX defaults.
> Profiles are repository data, not publisher-official templates.

---

## How it works

1. `paper-covert` resolves `TARGET_VENUE` (argument → `PAPER_PLAN.md` §0/§2 → `research_contract.md` → default `IJGIS`).
2. It looks for `./profiles/<venue>.yaml` under this skill's folder.
3. If present, the profile's fields configure `main.tex`, `preamble.tex`, `metadata.tex`, `build.sh`, and the DOCX reference doc selection.
4. If absent, `./profiles/generic.yaml` is used and the fallback is recorded in `FORMATTING_ASSUMPTIONS.md`.

## Profile schema

```yaml
venue: IJGIS                      # short code, also used as CLI argument
publisher: Taylor & Francis       # publisher name (informational)
documentclass: article            # LaTeX class; interact/elsarticle/IEEEtran/... when shipped
class_options: [11pt, a4paper]    # documentclass options
bib_style: apacite                # bibliography style
bib_engine: bibtex                # bibtex | biber
main_text_word_limit: 8000        # informational, used by submit-check
abstract_word_limit: 200
keywords_count: [6, 8]            # min, max
figure_count_limit: 10
requires_highlights: false
requires_author_contributions: true
requires_data_availability: true
ethics_statement: true
title_page: inline                # inline | separate
section_headings: numbered        # numbered | unnumbered
math_engine: pdflatex             # pdflatex | xelatex
build: latexmk                    # latexmk | pdflatex
notes: |
  Taylor & Francis 'interact' class is not bundled with this skill.
  Fallback to article + apacite; author should re-wrap with 'interact'
  at final submission time.
```

## Adding a new venue

1. Create `./profiles/<venue>.yaml` following the schema above.
2. If venue prose notes exist, add them under `templates/<domain>/<venue>.md` at the repository root (not here).
3. If the publisher's official `.cls` is available and license-compatible, drop it into `./profiles/classes/` and set `documentclass` accordingly; otherwise keep `article` and document the gap in `notes`.
4. Run `/paper-covert — venue: <venue>` on a sample manuscript and verify the generated `FORMATTING_ASSUMPTIONS.md`.

## Bundled profiles

- `generic.yaml` — fallback `article` + `plainnat`.
- `ijgis.yaml` — IJGIS (Taylor & Francis); article + apacite fallback.
- `isprs_jprs.yaml` — ISPRS JPRS (Elsevier); article + elsarticle-harv style.
- `rse.yaml` — RSE (Elsevier); highlights required; article + elsarticle-harv.
- `tgis.yaml` — Transactions in GIS (Wiley); article + apacite fallback.
- `aag_annals.yaml` — Annals of the AAG (Taylor & Francis); article + apacite.
- `ieee_tgrs.yaml` — IEEE TGRS; IEEEtran when available, else article + IEEEtran bibstyle.

## What profiles do **not** do

- They do not imply the output is an official publisher template.
- They do not encode publisher-private rules (reviewer guidance, copy-editing conventions).
- They do not replace `submit-check`'s venue-compliance run.
