---
name: auto-review-loop
description: Adversarial iterative review loop with generator-evaluator separation. Up to 4 rounds of independent review, improvement, and re-evaluation. Persists state to REVIEW_STATE.json for recovery. Stop: score ≥ 7.5/10 on all dimensions, or 4 rounds. Writes full history to AUTO_REVIEW.md.
tools: all
flags:
  HUMAN_CHECKPOINT: true    # If true, pause after each round for user approval of fixes
  COMPACT_MODE: false       # If true, use findings.md instead of full experiment logs
  EXTERNAL_REVIEW: false    # If true, use MCP claude-review or gemini-review server
---

# Skill: auto-review-loop

You run adversarial review cycles to iteratively improve research work. The architecture enforces **generator-evaluator separation**: the entity that wrote a section does NOT score it. Each round: independent review → parse → implement fixes → re-evaluate → decide.

---

## Core Principle: Generator-Evaluator Separation

**Never let the same agent that wrote a section score it.**

- Generator: `paper-writer` agent writes content
- Evaluator: `peer-reviewer` agent scores it — invoked independently with **no shared context** with the writer
- This is enforced in Step 2 below: always route evaluation to `peer-reviewer`, never ask `paper-writer` to self-assess

If you are currently acting as a writer and are asked to evaluate, refuse and re-invoke the skill as evaluator mode.

---

## Startup: Initialize or Resume

1. Check if `handoff.json` exists — read it first for pipeline state (fast context recovery)
2. Check if `REVIEW_STATE.json` exists:
   - If yes: read current round number, score, per-criterion scores, and pending_fixes. Resume from next phase.
   - If no: initialize `REVIEW_STATE.json` with round=0, per_criterion={}, status="in_progress"
3. Check if `AUTO_REVIEW.md` exists; if not, create it with header
4. Identify what to review: read `outputs/papers/` for sections, or `EXPERIMENT_LOG.md` for experiment results

---

## Hard Per-Criterion Thresholds

**Accept only if ALL dimensions meet their floor.** A 9.5 in novelty does not compensate for a 4.0 in rigor.

| Dimension | Weight | Floor (hard threshold) | What "floor" means |
|---|---|---|---|
| Novelty | 30% | ≥ 6.5 | Contribution clearly distinguished from prior work |
| Rigor | 25% | ≥ 7.0 | OLS+GWR+MGWR compared; Moran's I reported; reproducible |
| Literature coverage | 20% | ≥ 6.5 | ≥ 15 citations, majority ≥ 2020, key GeoAI/soundscape papers cited |
| Clarity | 15% | ≥ 6.0 | Active voice; specific numbers; no "may", "could", "might" claims |
| Impact | 10% | ≥ 6.0 | Practical application or scientific significance stated |

**Weighted average threshold:** ≥ 7.5 overall AND all floors met.

If any single floor is missed, the verdict is **not acceptable** regardless of weighted average.

---

## Few-Shot Score Calibration

Use these anchors to calibrate scores consistently. Read them before scoring.

### Score 6.0 / 10 (Needs Work)
> Methodology section describes GWR but does not report MGWR or compare the two. Moran's I of residuals is mentioned but the value is not given. Seven of 12 citations are older than 2019. The problem statement uses passive voice throughout and does not specify which cities are studied. Generation fidelity metrics (FID, SSIM) are mentioned but their values are not reported numerically.
- Rigor floor MISSED (no MGWR, no Moran's I value)
- Literature floor MISSED (too many old citations)
- Would score: Novelty 7.0, Rigor 4.5, Literature 5.5, Clarity 5.0, Impact 6.5 → average ~5.7

### Score 7.5 / 10 (Acceptable — Minimum Bar)
> Methodology section runs OLS, GWR, and MGWR on NYC, London, Singapore data. Reports R² (OLS 0.43, GWR 0.61, MGWR 0.67) and Moran's I of MGWR residuals (0.08, p=0.12, not significant — spatial autocorrelation removed). Cites 16 papers, 13 from 2020–2025 including ControlNet (Zhang 2023), ImageBind (Girdhar 2023), CLAP (LAION 2022). Uses active voice. FID = 42.3 reported. One limitation: GWI (Green View Index) is described but its contribution to FID is not ablated.
- All floors met (barely)
- Weighted average ≈ 7.5

### Score 9.0 / 10 (Strong — Target Quality)
> Methodology clearly positions contribution against three prior systems (sound2sight, UrbanCLIP, GeoGen) with head-to-head FID/SSIM/LPIPS table. OLS R²=0.43, GWR R²=0.61, MGWR R²=0.67 across all three cities; Moran's I = 0.08 (p=0.12). MGWR local coefficient maps reveal that sky-view factor matters more in Singapore (β̄=0.41) than London (β̄=0.19). All 22 citations ≥ 2019; 7 from ISPRS/IEEE-TGRS/CEUS venues. Ablation: removing soundscape conditioning drops FID by 18.3 points. Each figure has scale bar, north arrow, CRS label, inset locator.
- All floors exceeded
- Novelty 9.5, Rigor 9.0, Literature 9.0, Clarity 8.5, Impact 8.5 → average ~9.0

---

## Loop: Up to 4 Rounds

For each round (while round < 4 AND NOT all_floors_met AND weighted_avg < 7.5):

### Round Step 1: Prepare Review Context

Build the review context (**evaluator does NOT read generator's working notes**):
- Current work: the specific section file(s) being reviewed
- Previous round scores: last entry from `AUTO_REVIEW.md` (scores only, not writer's reasoning)
- Research contract: `research_contract.md` (ground truth for what was promised)
- Approved claims: `memory/approved_claims.md` (to check if claims are grounded)

COMPACT_MODE: use `findings.md` + latest section files only (not full EXPERIMENT_LOG).
Full context: read section files + `memory/approved_claims.md`.

**Do NOT include**: writer's draft notes, prior writer context, or any information that blurs generator/evaluator separation.

### Round Step 2: Evaluate (Independent Evaluator)

**Always use peer-reviewer agent as evaluator — never self-review.**

Invoke `.claude/agents/peer-reviewer.md` with this exact instruction:
```
Score each dimension independently using the calibration anchors in auto-review-loop/SKILL.md.
For each dimension, state: score (0–10), floor (from skill), pass/fail, and one specific improvement required.
Report: weighted average, whether all floors are met, and verdict (accept/revise/reject).
```

The peer-reviewer MUST return a structured response:
```
Novelty:             X.X / 10 (floor 6.5) — PASS/FAIL — [specific improvement]
Rigor:               X.X / 10 (floor 7.0) — PASS/FAIL — [specific improvement]
Literature coverage: X.X / 10 (floor 6.5) — PASS/FAIL — [specific improvement]
Clarity:             X.X / 10 (floor 6.0) — PASS/FAIL — [specific improvement]
Impact:              X.X / 10 (floor 6.0) — PASS/FAIL — [specific improvement]
Weighted average:    X.X / 10
All floors met:      YES / NO
Verdict:             ACCEPT / NEEDS REVISION / REJECT
Top 3 must-fix items:
1. [specific, actionable fix with target dimension]
2. [specific, actionable fix with target dimension]
3. [specific, actionable fix with target dimension]
```

If EXTERNAL_REVIEW is true and MCP server is available: call `claude-review` or `gemini-review` with the same instruction; parse the structured response.

### Round Step 3: Evaluate Stop Condition

Parse the reviewer response to extract per-criterion scores and floors.

**ACCEPT if:**
- Weighted average ≥ 7.5 AND
- All five dimension floors are met

**CONTINUE if:**
- Any floor is missed OR weighted average < 7.5
- AND round < 4

**FORCE STOP if:**
- round == 4 (max rounds reached, even if not accepted)

On ACCEPT: write to `AUTO_REVIEW.md`: `STOP — accepted at round N, score X.X/10, all floors met`
Update `REVIEW_STATE.json`: `{"status": "complete", "final_score": X.X, "all_floors_met": true}`

On FORCE STOP: write to `AUTO_REVIEW.md`: `STOP — max rounds reached, score X.X/10 — human review required`
Update `REVIEW_STATE.json`: `{"status": "max_rounds", "final_score": X.X}`

### Round Step 4: Implement Fixes (Generator)

Focus only on dimensions that failed their floor or are below 7.5.

For each must-fix item, route to the appropriate generator:
- **Write more content / restructure**: call `.claude/agents/paper-writer.md` with section + specific reviewer feedback + calibration target
- **Run new experiment or ablation**: add to `EXPERIMENT_PLAN.md` and run skill `geo-experiment` EXECUTE mode
- **Fix spatial analysis**: run skill `spatial-analysis` for re-interpretation and Moran's I
- **Add or fix citations**: call `.claude/agents/citation-manager.md` with APA 7th edition format
- **Fix figures**: run skill `paper-figure` with corrected cartographic conventions

If HUMAN_CHECKPOINT is true: show action plan (what will be fixed, by which agent) and await user confirmation before executing.

After implementing fixes, re-evaluate only the fixed dimensions (not all five) to verify improvement.

### Round Step 5: Persist State

Write to `REVIEW_STATE.json`:
```json
{
  "round": <N>,
  "score": <weighted_average>,
  "per_criterion": {
    "novelty": {"score": X.X, "floor": 6.5, "pass": true|false},
    "rigor": {"score": X.X, "floor": 7.0, "pass": true|false},
    "literature": {"score": X.X, "floor": 6.5, "pass": true|false},
    "clarity": {"score": X.X, "floor": 6.0, "pass": true|false},
    "impact": {"score": X.X, "floor": 6.0, "pass": true|false}
  },
  "all_floors_met": true|false,
  "verdict": "<verdict>",
  "completed_fixes": ["<fix1>", "<fix2>"],
  "pending_fixes": [],
  "timestamp": "<ISO datetime>",
  "status": "in_progress"
}
```

Append to `AUTO_REVIEW.md`:
```markdown
## Round N — Weighted avg: X.X/10 — <timestamp>

### Per-Criterion Scores
| Dimension | Score | Floor | Status |
|---|---|---|---|
| Novelty | X.X | 6.5 | PASS/FAIL |
| Rigor | X.X | 7.0 | PASS/FAIL |
| Literature | X.X | 6.5 | PASS/FAIL |
| Clarity | X.X | 6.0 | PASS/FAIL |
| Impact | X.X | 6.0 | PASS/FAIL |

### Must-Fix Items
1. [fix 1]
2. [fix 2]

### Fixes Implemented
1. [what was done]
2. [what was done]

### Post-fix Re-score (dimensions that changed)
- Rigor: 5.5 → 7.2 (PASS)
```

Increment round counter. Continue to next round.

---

## Exit Report

When loop exits, output:
```
Auto-review loop complete.
Rounds run: N/4
Weighted average: X.X/10
Floors met: [list which passed/failed]
All floors met: YES/NO
Verdict: ACCEPTED / NOT ACCEPTED — human review required

Key improvements made:
- [improvement 1]
- [improvement 2]

Full history: AUTO_REVIEW.md
State file: REVIEW_STATE.json

[If not accepted]: The following dimensions are below floor — do not proceed to final submission:
  - [Dimension]: X.X (floor Y.Y) — [specific remaining issue]

[If accepted]: Ready for references compilation. Run /write-section references.
```
