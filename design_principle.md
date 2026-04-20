# Skill Design Principles — Night Owl Research Agent

> A structural discipline for authoring, reviewing, and evolving Claude Code skills within a multi-stage research orchestration system.

---

## Part I: Required Sections of a Skill

Every SKILL.md file in this project must contain the sections below. Each section exists for a specific reason rooted in the operational demands of long-running, multi-agent research pipelines.

---

### 1. YAML Frontmatter

```yaml
---
name: <skill-name>
description: <one-liner with primary use cases>
argument-hint: [expected arguments]
tools: [allowed tool list]
flags: [optional configuration flags]
---
```

**Why required.** The frontmatter is the machine-readable contract between the skill and the Claude Code harness. It controls:
- **Tool allowlisting** — limits the blast radius of any single skill invocation. A literature-review skill has no business calling `Write` on experiment logs.
- **Argument parsing** — tells the orchestrator (and the user) what inputs the skill expects before it runs.
- **Discovery** — pipeline orchestrators (`idea-discovery-pipeline`, `paper-writing-pipeline`, `full-pipeline`) use `name` and `description` to route work to the correct skill.
- **Flags** — enable opt-in behaviors (e.g., `hard_mode`, `nightmare_mode` in `auto-review-loop`) without forking the skill into variants.

**Design failure without it.** A skill without explicit tool allowlisting can read, write, and execute anything — violating the principle of least privilege. A skill without `argument-hint` forces users to read the full body to understand how to invoke it.

---

### 2. Overview / Purpose Statement

A 2–5 sentence block explaining *what* the skill does, *when* to use it, and *where* it fits in the pipeline.

**Why required.** Skills are composed into pipelines by both humans and orchestrator skills. The overview is the only section that gets read at routing time. It must answer three questions in under 30 seconds:
1. What does this skill produce?
2. What does it consume (upstream dependencies)?
3. When should I reach for this skill instead of a neighboring one?

**Design failure without it.** Without a clear purpose boundary, skills drift into overlapping scope. The distinction between `generate-idea` (brainstorm divergently) and `refine-research` (converge on one proposal) would collapse, causing redundant work and contradictory outputs.

---

### 3. Constants / Configurable Thresholds

A named block of tuneable parameters with default values.

```
MAX_ROUNDS = 5
SCORE_THRESHOLD = 9
MAX_PRIMARY_CLAIMS = 2
MAX_NEW_TRAINABLE_COMPONENTS = 2
```

**Why required.** Constants serve three purposes:
1. **Parsimony enforcement** — caps like `MAX_PRIMARY_CLAIMS = 2` prevent scope creep within a single skill run.
2. **Termination guarantees** — `MAX_ROUNDS` ensures refinement loops halt even when the score threshold is never met, preventing infinite token burn.
3. **Reproducibility** — when a colleague runs the same skill, the constants document the operating envelope. Changing `SCORE_THRESHOLD` from 9 to 7 is a conscious, visible decision rather than a buried prompt tweak.

**Design failure without it.** Magic numbers scattered through prose are invisible to reviewers. A refinement loop without `MAX_ROUNDS` can run indefinitely. A generation step without output caps produces sprawling, unfocused artifacts.

---

### 4. Workflow / Phases

A numbered sequence of phases, each with:
- **Entry conditions** (what files/state must exist)
- **Actions** (what the skill does)
- **Exit conditions** (what is produced, what state is written)

**Why required.** Research workflows are long-running (hours to days) and frequently interrupted. Phase structure provides:
1. **Resumability** — checkpoint state files (e.g., `REFINE_STATE.json`, `REVIEW_STATE.json`) record the last completed phase. On resume, the skill skips completed phases.
2. **Debuggability** — when output quality is poor, the phase structure localizes the failure. "The problem is in Phase 3 (scoring)" is actionable; "the skill produced bad output" is not.
3. **Composability** — pipeline orchestrators can skip phases that another skill already completed (e.g., `paper-writing-pipeline` skips the planning phase if `PAPER_PLAN.md` already exists).

**Design failure without it.** A monolithic skill that "does everything in one pass" cannot be resumed, cannot be partially reused, and cannot be debugged without re-running the entire sequence.

---

### 5. Checkpoint / State Persistence

Explicit specification of:
- State file path and schema (JSON with phase, round, threadId, scores, status, timestamp)
- Recovery logic (how to detect and resume from a prior checkpoint)
- Expiry rules (e.g., checkpoints older than 24 hours are stale)

**Why required.** Claude Code sessions are stateless across invocations. Without explicit state persistence:
- A 5-round refinement loop that crashes at round 3 must restart from round 1.
- An adversarial review loop loses the reviewer's accumulated memory.
- Pipeline orchestrators cannot determine which skill last completed successfully.

The `handoff.json` pattern (used by pipeline orchestrators) is the inter-skill equivalent: it records `pipeline.stage` and `recovery.resume_skill` so the full pipeline can resume from the correct point.

**Design failure without it.** Every interruption (timeout, token limit, user break) forces a full restart, wasting compute and producing inconsistent artifacts.

---

### 6. Canonical Output Paths

A list of every file the skill writes, with fixed paths relative to the project root.

**Why required.** Skills are chained: `refine-research` writes `output/refine-logs/FINAL_PROPOSAL.md`, which `experiment-design` reads. If output paths are ad-hoc or user-chosen:
- Downstream skills cannot find upstream artifacts.
- The `generate-report` skill (which consolidates all outputs into `NARRATIVE_REPORT.md`) cannot locate its sources.
- `PROJ_NOTES.md` entries become meaningless without stable path references.

The canonical path convention also enables the memory/audit system: `APPROVED_CLAIMS.md`, `DATA_MANIFEST.md`, and `PROJ_NOTES.md` are always in known locations.

**Design failure without it.** Every pipeline run requires manual path wiring, breaking automation and introducing silent failures when a downstream skill reads a stale file from a previous run.

---

### 7. Decision Rules / Branching Logic

Explicit if/then rules for choosing between alternatives within the skill.

**Why required.** Research skills frequently face forks:
- `deploy-experiment`: Track A (ML/DL) vs. Track B (spatial/GIScience) vs. local vs. SSH vs. Modal GPU.
- `spatial-analysis`: ESDA → regression ladder → GWR/MGWR → clustering (method selection tree).
- `paper-figure-generate`: code-generated (plots, maps) vs. prompt-generated (architecture diagrams).

Without explicit decision rules, the LLM must infer the correct branch from context, which is unreliable across sessions. Decision rules make the skill deterministic at branch points.

**Design failure without it.** The skill makes inconsistent choices across runs. One invocation uses GWR; the next uses OLS for the same data, because the prompt context differed slightly.

---

### 8. Guardrails / "Do NOT" Rules

An explicit list of prohibited behaviors.

**Why required.** LLMs have systematic failure modes that must be explicitly suppressed:
- **Fabrication**: "Do NOT invent statistics, p-values, or citation details."
- **Self-scoring**: "The entity that writes NEVER scores its own output."
- **Scope creep**: "Do NOT add features beyond the experiment plan."
- **Silent failure**: "Do NOT skip a failed step; log the failure and halt."

Guardrails are not aspirational — they are countermeasures against observed failure patterns. Each rule exists because the skill (or a similar skill) produced that exact failure in testing.

**Design failure without it.** The skill produces plausible but fabricated results, self-validates its own output, or silently degrades in ways that are only caught downstream (or never caught).

---

### 9. Evidence Discipline

Rules governing how claims are sourced, verified, and traced.

**Why required.** This is the load-bearing section for research integrity:
- Every quantitative claim must trace to `APPROVED_CLAIMS.md` or experiment logs.
- Missing evidence must be marked with `[PLACEHOLDER — ...]`, never fabricated.
- Claim-to-evidence matrices (tables mapping each claim to its source) are mandatory in paper drafts.
- Gap reports document unsupported claims and unresolved citations.

This discipline is enforced across the entire pipeline: `refine-research` establishes claims, `experiment-design` plans their validation, `deploy-experiment` produces the evidence, `auto-review-loop` audits the chain, and `paper-draft` renders the final mapping.

**Design failure without it.** The system produces convincing but unverifiable research artifacts — the worst possible outcome for an academic research agent.

---

### 10. Generator-Evaluator Separation

Explicit rules ensuring that the entity producing content never evaluates its own quality.

**Why required.** Self-evaluation is the most dangerous failure mode in iterative refinement:
- In `auto-review-loop`: Codex MCP (gpt-5.4) reviews; Claude Code revises. Never the reverse.
- In `paper-review-loop`: Codex MCP performs cold-read evaluation; Claude Code implements revisions.
- In `refine-research`: Codex MCP scores each round; Claude Code refines based on feedback.

ThreadId persistence ensures the reviewer maintains context across rounds without contamination from the author's perspective.

**Design failure without it.** The skill converges on outputs that score well by its own criteria but fail under external scrutiny — a form of mode collapse in the refinement loop.

---

### 11. Composability / Pipeline Integration

A section describing:
- What upstream skills feed into this one (and which artifacts they must produce)
- What downstream skills consume this skill's output
- How to invoke this skill standalone vs. as part of a pipeline

**Why required.** No skill in this system operates in true isolation. The five workflows form a directed acyclic graph of dependencies. Without explicit composability documentation:
- Users invoke skills out of order, producing errors or empty outputs.
- Pipeline orchestrators cannot validate preconditions.
- Refactoring one skill's output format silently breaks downstream consumers.

**Design failure without it.** Skills become black boxes that only work when invoked in the exact sequence the original author intended, with no documentation of that sequence.

---

### 12. Key Rules Summary

A bullet-point summary of the most critical rules, always including the large-file handling guardrail:

> "If Write fails due to size, retry with Bash heredoc (`cat << 'EOF' > file`). Do NOT ask the user."

**Why required.** The full SKILL.md can be thousands of tokens. The key rules summary serves as a compressed instruction set that fits in the LLM's working attention during execution. It prioritizes the rules most likely to be violated under token pressure.

**Design failure without it.** Under long-context scenarios, the LLM forgets critical rules from earlier in the document. The summary acts as a recency-biased reinforcement of the most important constraints.

---

### 13. Audit Trail (PROJ_NOTES.md Logging)

Every skill must append a one-line entry to `output/PROJ_NOTES.md`:

```
[YYYY-MM-DD] <skill-name>: <summary of what was produced>
```

**Why required.** The audit trail provides:
- **Provenance**: which skill produced which artifact, and when.
- **Pipeline debugging**: if the final paper has a weak section, trace it back through the FINDINGS log to the skill that generated the source material.
- **Progress tracking**: for multi-day research campaigns, PROJ_NOTES.md is the changelog.

**Design failure without it.** Artifacts accumulate in `output/` with no record of which skill produced them, when, or in what order. Debugging becomes archaeological.

---

## Part II: Advanced Design Disciplines for Skill Optimization

The current skill architecture is robust but can be further strengthened with the following sophisticated design patterns. Each pattern addresses a specific class of failure or inefficiency observed in multi-agent research systems.

---

### A. Formal Pre/Post-Condition Contracts

**Current state.** Phase entry/exit conditions are described in prose, checked informally.

**Optimization.** Add a machine-checkable contract block to each phase:

```yaml
phase_3_scoring:
  preconditions:
    - file_exists: output/refine-logs/round_${N}_proposal.md
    - file_exists: memory/APPROVED_CLAIMS.md
    - state.round <= MAX_ROUNDS
  postconditions:
    - file_exists: output/refine-logs/round_${N}_score.json
    - state.last_score is numeric
    - PROJ_NOTES.md has new entry
  on_failure: halt_with_diagnostic
```

**Why.** Prose conditions are subject to interpretation drift across sessions. A formalized contract enables automated validation, both by the skill itself (self-check before proceeding) and by pipeline orchestrators (pre-flight validation before invoking a downstream skill). This eliminates the class of bugs where a skill proceeds with missing or malformed inputs.

---

### B. Artifact Versioning and Immutability

**Current state.** Skills overwrite artifacts in place (e.g., `FINAL_PROPOSAL.md` is rewritten each refinement round).

**Optimization.** Adopt an append-only versioning scheme:

```
output/refine-logs/FINAL_PROPOSAL_v1.md
output/refine-logs/FINAL_PROPOSAL_v2.md
output/refine-logs/FINAL_PROPOSAL_v3.md  ← current
output/refine-logs/FINAL_PROPOSAL.md     ← symlink to v3
```

**Why.** Overwriting destroys the refinement history. When a reviewer asks "why did you drop the spatial heterogeneity analysis?", the answer is in v2 vs. v3 — but only if both versions exist. Immutable versioning also enables rollback without re-running the skill.

---

### C. Confidence-Gated Progression

**Current state.** Progression between phases is binary: pass/fail based on score thresholds.

**Optimization.** Introduce a three-tier confidence gate:

| Confidence | Score Range | Action |
|---|---|---|
| High | ≥ threshold | Proceed to next phase |
| Medium | threshold − 1.5 to threshold | Proceed with mandatory human review flag |
| Low | < threshold − 1.5 | Halt and request user intervention |

**Why.** Binary gating forces a choice between permissive thresholds (low quality passes through) and strict thresholds (good-enough work gets blocked). The medium tier allows the pipeline to continue while flagging uncertain decisions for asynchronous human review, reducing both false positives and unnecessary halts.

---

### D. Semantic Dependency Graph

**Current state.** Pipeline dependencies are documented in prose within each skill's composability section.

**Optimization.** Create a machine-readable dependency manifest:

```yaml
# skills/DEPENDENCY_GRAPH.yaml
refine-research:
  reads:
    - output/IDEA_REPORT.md
    - output/LIT_REVIEW_REPORT.md
  writes:
    - output/refine-logs/FINAL_PROPOSAL.md
    - output/refine-logs/REFINE_STATE.json
  requires_before: [generate-idea, lit-review]
  enables_after: [experiment-design, deploy-experiment]
```

**Why.** A formal dependency graph enables:
1. **Automated precondition checks** — the pipeline orchestrator can verify all upstream artifacts exist before invoking a skill.
2. **Parallel execution** — independent branches of the graph can run concurrently (e.g., `data-download` and `spatial-analysis` planning).
3. **Impact analysis** — changing one skill's output format immediately reveals which downstream skills are affected.
4. **Visualization** — the graph can be rendered as a DAG for onboarding and debugging.

---

### E. Structured Error Taxonomy

**Current state.** Errors are handled ad-hoc: some skills halt, some retry, some log and continue.

**Optimization.** Define a standard error taxonomy with prescribed responses:

| Error Class | Example | Prescribed Response |
|---|---|---|
| `MISSING_INPUT` | Upstream artifact not found | Halt with diagnostic; suggest which skill to run first |
| `TOOL_UNAVAILABLE` | MCP server unreachable | Fall back to local alternative; log degradation |
| `QUALITY_BELOW_THRESHOLD` | Score < minimum after MAX_ROUNDS | Halt; write partial output with gap report |
| `STATE_CORRUPTION` | Checkpoint schema mismatch | Delete checkpoint; restart from Phase 0 |
| `RESOURCE_LIMIT` | Token limit / file size limit | Chunk output; use Bash heredoc fallback |
| `EXTERNAL_TIMEOUT` | Codex MCP / API timeout | Retry once with backoff; halt on second failure |

**Why.** Consistent error handling across 19 skills eliminates an entire class of debugging: "did the skill fail, or did it silently produce bad output?" Every failure mode has a known response, reducing the cognitive load on both users and pipeline orchestrators.

---

### F. Skill Telemetry and Cost Accounting

**Current state.** PROJ_NOTES.md logs what was produced but not the cost of producing it.

**Optimization.** Add a telemetry block to each skill's output:

```json
{
  "skill": "refine-research",
  "rounds_used": 4,
  "rounds_max": 5,
  "external_llm_calls": 4,
  "total_input_tokens": 128000,
  "total_output_tokens": 24000,
  "wall_clock_minutes": 22,
  "final_score": 9.2,
  "artifacts_produced": ["FINAL_PROPOSAL.md", "REFINE_STATE.json"]
}
```

**Why.** Without cost accounting, users cannot distinguish between skills that converge efficiently (3 rounds, 10 minutes) and skills that burn budget (5 rounds, 45 minutes, still below threshold). Telemetry enables data-driven decisions about which skills to optimize, which thresholds to adjust, and when to switch from expensive external reviewers to cheaper local alternatives.

---

### G. Degradation-Aware Fallback Chains

**Current state.** Skills note that MCP tools are optional and fall back to local alternatives, but the fallback logic is ad-hoc.

**Optimization.** Define explicit fallback chains with quality annotations:

```
Review source priority:
1. Codex MCP (gpt-5.4, xhigh reasoning) → quality: HIGH
2. Claude subagent (fresh context)       → quality: MEDIUM
3. Self-review with structured rubric    → quality: LOW (flag output)
```

**Why.** The current "graceful degradation" pattern does not communicate quality loss. A pipeline that falls back from Codex MCP to self-review produces lower-quality output, but nothing downstream knows this. Explicit quality annotations let downstream skills adjust their trust level (e.g., `paper-review-loop` might require an extra round if the upstream review was `MEDIUM` quality).

---

### H. Prompt Modularization and Slot Filling

**Current state.** Prompts to external LLMs (Codex MCP) are constructed inline within the skill body, mixing structure with content.

**Optimization.** Extract prompts into reusable templates with named slots:

```markdown
<!-- templates/prompts/review_prompt.md -->
You are reviewing a {{ARTIFACT_TYPE}} for submission to {{VENUE}}.

## Evaluation Criteria
{{CRITERIA_BLOCK}}

## Artifact Under Review
{{ARTIFACT_CONTENT}}

## Prior Round Context
{{PRIOR_FEEDBACK}}
```

**Why.** Inline prompts are:
1. Hard to A/B test (changing the prompt requires editing the skill).
2. Hard to reuse (three skills use similar review prompts but with slight variations).
3. Hard to version (prompt changes are buried in skill diffs).

Modularized prompts can be versioned, tested, and shared across skills independently of the skill logic.

---

### I. Multi-Perspective Review Ensembles

**Current state.** `auto-review-loop` uses a single reviewer persona per round (domain-specific: ML, GIScience, Remote Sensing, or Spatial Data Science).

**Optimization.** Run multiple reviewer personas in parallel per round and aggregate:

```
Round N:
  Reviewer A (ML expert)       → scores + critique
  Reviewer B (GIScience)       → scores + critique
  Reviewer C (Methods skeptic) → scores + critique
  ──────────────────────────────
  Aggregation: weighted average scores + union of unique critiques
  Conflict resolution: flag contradictory feedback for human arbitration
```

**Why.** Single-perspective reviews have blind spots. An ML reviewer may approve a method that a GIScience reviewer would flag for ignoring spatial autocorrelation. Ensemble reviews surface cross-disciplinary issues earlier, reducing late-stage revisions. The cost is 3x the review tokens per round, but the reduction in wasted revision rounds typically offsets this.

---

### J. Skill Self-Test Suites

**Current state.** Skills are tested by running them on real research tasks. There are no unit tests for skill behavior.

**Optimization.** Add a `tests/` directory to each skill with synthetic test cases:

```
skills/refine-research/tests/
  ├── test_resume_from_checkpoint.md    # synthetic REFINE_STATE.json → verify skip logic
  ├── test_max_rounds_halt.md           # score never reaches threshold → verify halting
  ├── test_missing_input.md             # no IDEA_REPORT.md → verify error message
  └── test_large_file_fallback.md       # simulate Write failure → verify heredoc fallback
```

**Why.** Skills are complex programs written in natural language. Like any program, they have edge cases that are only discovered in production. A test suite — even one composed of markdown scenarios — enables regression testing when skills are modified. The test cases also serve as documentation of expected behavior at boundary conditions.

---

## Part III: Concise Reference Table

The table below summarizes both the required sections (Part I) and the advanced optimizations (Part II) in a single view.

### Required Sections

| # | Section | Purpose | Failure Mode If Missing |
|---|---------|---------|------------------------|
| 1 | YAML Frontmatter | Machine-readable contract: tools, args, flags | Unbounded tool access; opaque invocation |
| 2 | Overview | Routing and scope boundary | Skill overlap and redundant work |
| 3 | Constants | Parsimony, termination, reproducibility | Magic numbers; infinite loops; irreproducible runs |
| 4 | Workflow / Phases | Resumability, debuggability, composability | Monolithic execution; no resume; no debugging |
| 5 | Checkpoint Persistence | Session recovery across interruptions | Full restart on every interruption |
| 6 | Canonical Output Paths | Inter-skill artifact handoff | Broken pipelines; stale file reads |
| 7 | Decision Rules | Deterministic branching at forks | Inconsistent method/tool choices across runs |
| 8 | Guardrails | Suppress known LLM failure modes | Fabrication, self-scoring, scope creep |
| 9 | Evidence Discipline | Research integrity and claim traceability | Unverifiable claims; placeholder-free fabrication |
| 10 | Generator-Evaluator Separation | Prevent self-validation mode collapse | Refinement loops that converge on self-pleasing output |
| 11 | Composability | Pipeline integration documentation | Skills that only work in one exact invocation sequence |
| 12 | Key Rules Summary | Compressed instruction set for execution | Critical rules forgotten under long-context pressure |
| 13 | Audit Trail | Provenance and pipeline debugging | Untraceable artifacts; archaeological debugging |

### Advanced Optimizations

| ID | Optimization | What It Adds | Key Benefit |
|----|-------------|--------------|-------------|
| A | Pre/Post-Condition Contracts | Machine-checkable phase contracts | Eliminates malformed-input bugs |
| B | Artifact Versioning | Append-only versioned outputs | Rollback capability; refinement history |
| C | Confidence-Gated Progression | Three-tier pass/flag/halt gates | Reduces both false positives and unnecessary halts |
| D | Semantic Dependency Graph | Machine-readable DAG of skill dependencies | Automated precondition checks; parallel execution |
| E | Structured Error Taxonomy | Standard error classes with prescribed responses | Consistent failure handling across all 19 skills |
| F | Skill Telemetry | Token/time/round cost accounting per run | Data-driven optimization of skill parameters |
| G | Degradation-Aware Fallbacks | Quality-annotated fallback chains | Downstream skills adjust trust based on review quality |
| H | Prompt Modularization | Externalized, slotted prompt templates | A/B testable; reusable; independently versioned prompts |
| I | Multi-Perspective Ensembles | Parallel multi-persona review per round | Cross-disciplinary blind spot detection |
| J | Skill Self-Test Suites | Synthetic test cases for edge behaviors | Regression testing; boundary documentation |

---

*This document codifies the design discipline observed across all 19 skills of the Night Owl Research Agent. It should be treated as a living standard — updated as new skills are added and as advanced optimizations are adopted.*
