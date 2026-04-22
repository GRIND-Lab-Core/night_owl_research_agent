# Agent Design Principles — Night Owl Research Agent

> A structural discipline for authoring, reviewing, and evolving Claude Code specialist sub-agents within a multi-stage research orchestration system.

Agents in NORA are defined as Markdown files under `.claude/agents/`. Unlike skills — which describe workflow logic that runs inside the parent conversation context — an agent is a **specialist persona invoked via the Agent tool in its own context window**. That isolation is the entire point: agents let the pipeline parallelise independent subtasks, protect the parent context from tool-call noise, and enforce the generator–evaluator separation that NORA relies on for research integrity.

The nine agents shipped in this project (`orchestrator`, `literature-scout`, `synthesis-analyst`, `gap-finder`, `hypothesis-generator`, `geo-specialist`, `paper-writer`, `peer-reviewer`, `citation-manager`) were designed against the principles below.

---

## Part I: Required Sections of an Agent

Every agent file in `.claude/agents/` must contain the sections below. Each section exists for a specific reason rooted in the operational demands of multi-agent research pipelines.

---

### 1. YAML Frontmatter

```yaml
---
name: <agent-name>
description: |
  <One-paragraph statement of when to use this agent.>
  Use this agent to:
  - <capability 1>
  - <capability 2>
tools: <explicit tool list — never "all" unless orchestrator>
---
```

**Why required.** The frontmatter is the machine-readable contract that the Claude Code harness and parent skills rely on for routing and permissioning:

- **Name and description** — parent skills select the correct agent by matching the description against the subtask; vague descriptions cause mis-routing.
- **Explicit tool allowlist** — agents receive the tightest allowlists in the system (e.g., `peer-reviewer` has `Read, Write` only; `literature-scout` has `WebFetch, WebSearch, Read, Write, Bash`). This is stricter than skills because agents run unattended in a separate context and cannot be interrupted by a user gate during execution.
- **"Use this agent to" bullet list** — a structured capability menu the orchestrator uses to decide whether the agent matches the task.

**Design failure without it.** A missing or vague description causes the parent skill to invoke the wrong agent; a missing tool allowlist gives the sub-context unbounded authority to write files, run shell commands, or call external APIs the caller never intended.

---

### 2. Persona and Role Statement

A 2–4 sentence block declaring *who* the agent is and what scope it owns.

> "You are the domain expert for all spatial analysis decisions in NORA. You are consulted before methodology and results sections are written, and whenever spatial analysis code is generated." — `geo-specialist.md`

**Why required.** Agents run in a fresh context with none of the parent's conversational history. The persona statement is the first thing the sub-context reads; it seeds role-consistent behaviour for the entire invocation. It also disambiguates overlap — the orchestrator can reason about the boundary between `synthesis-analyst` (reads papers, writes synthesis) and `gap-finder` (reads synthesis, writes gaps) because each persona explicitly names its scope.

**Design failure without it.** Without a clear persona, the sub-context behaves as a generic assistant and produces output that looks plausible but fails the role's discipline (a reviewer that drafts instead of critiques, a writer that self-approves, a scout that synthesises).

---

### 3. Context Isolation Contract

An explicit statement of what the agent reads from disk on startup and what it does **not** assume from the caller.

**Why required.** The parent skill's context is invisible to the agent. Two corollaries:

1. **Everything the agent needs must be fetchable from files** (e.g., `program.md`, `memory/paper-cache/`, `output/LIT_REVIEW_REPORT.md`) or passed explicitly as the `$ARGUMENTS` payload at invocation time.
2. **Anything the agent produces must land in a canonical output path** because the parent has no way to "read back" the sub-context — only the final tool-return payload is visible.

This is the architectural reason NORA is file-driven: agents are stateless and context-isolated by design, so persistent state must live on disk.

**Design failure without it.** The agent silently assumes the caller passed context that was never actually in its window, hallucinates missing details, and produces confidently wrong output.

---

### 4. Single-Responsibility Scope

A declaration that the agent performs one discrete subtask — not a pipeline.

**Why required.** Agents are cheap to compose but expensive to mis-scope. An agent that "does literature search and synthesis and gap analysis" collapses three specialists into one, loses the parallelism advantage (search and synthesis can overlap), and defeats generator–evaluator separation (the same context that summarises cannot objectively critique its own summary).

NORA's nine agents each own exactly one pipeline stage:

| Agent | Single responsibility |
|---|---|
| `literature-scout` | Retrieve and cache papers |
| `synthesis-analyst` | Read cache, write synthesis |
| `gap-finder` | Read synthesis, write ranked gaps |
| `hypothesis-generator` | Read gaps, write scored hypotheses |
| `geo-specialist` | Review spatial choices, recommend methods |
| `paper-writer` | Draft one section, self-score |
| `peer-reviewer` | Cold-read critique, no drafting |
| `citation-manager` | Format and validate references |
| `orchestrator` | Sequence the above, never do their work |

**Design failure without it.** Composite agents are harder to test, harder to debug, and harder to run in parallel. Scope creep inside one agent produces output whose quality is dominated by the weakest sub-task.

---

### 5. Narrow Tool Allowlist (Least Privilege)

An explicit `tools:` field listing only the tools the agent actually needs.

**Why required.** Because agents run unattended, the blast radius of any single agent call is bounded only by the allowlist. A reviewer that can `Write` anywhere can corrupt the manuscript it is reviewing; a scout that can `Bash` freely can run arbitrary shell commands outside the retrieval workflow.

Observed allowlist discipline in NORA:

- `peer-reviewer` and `gap-finder` — `Read, Write` only (no network, no shell).
- `literature-scout` — `WebFetch, WebSearch, Read, Write, Bash` (network + cache management).
- `paper-writer` — `Read, Write` (deliberately no WebSearch — writer must not improvise citations).
- `orchestrator` — `all` (the sole exception, because it must invoke every downstream tool).

**Design failure without it.** Tool-allowlist creep turns specialist agents into generalist assistants, erasing both the safety and the composability that made the agent pattern worth adopting.

---

### 6. Deterministic I/O Contract

A specification of the structured input the agent expects and the structured output it returns.

**Why required.** Agents are called programmatically by skills and by the orchestrator. The caller must be able to predict the shape of the return payload well enough to parse it and feed it downstream. NORA agents define their output schema inline (e.g., `literature-scout` returns a JSON object per paper with `id, title, authors, year, venue, abstract, citation_count, doi, url, domain_tags, priority_venue`).

Three contracts must be explicit:

1. **Inputs** — what `$ARGUMENTS` must contain (keywords, section name, scoring rubric).
2. **Files read** — which disk paths are consulted (handoff.json, APPROVED_CLAIMS, paper-cache).
3. **Outputs** — canonical file writes *plus* the structured return payload the caller parses.

**Design failure without it.** The caller receives freeform prose it cannot reliably parse, forcing an LLM re-read of the agent's output to extract structure — wasting tokens and reintroducing the context pollution the agent was supposed to prevent.

---

### 7. Evaluator-vs-Producer Role Lock

A rule declaring whether the agent **produces** content or **evaluates** content — never both.

**Why required.** This is the agent-side enforcement of the generator–evaluator separation principle. NORA splits this role explicitly:

- **Producers** — `paper-writer`, `synthesis-analyst`, `gap-finder`, `hypothesis-generator`, `literature-scout`, `citation-manager`.
- **Evaluators** — `peer-reviewer`, `geo-specialist` (as reviewer), plus Codex MCP (`gpt-5.4`) when invoked from a skill.

A producer agent that self-scores is allowed **only** for internal gating (e.g., `paper-writer`'s 5-dimension rubric is a triage signal, not an acceptance decision). Any score that actually opens a gate must come from an evaluator agent or external reviewer invoked in a separate context.

**Design failure without it.** Refinement loops converge on outputs that score well against the producer's own priors but fail external scrutiny — a mode collapse the pipeline is specifically engineered to prevent.

---

### 8. Persona-Grounded Expertise

An embedded block of domain knowledge the agent references on every invocation.

**Why required.** Agents start cold. If they had to re-derive domain conventions every run, output quality would be inconsistent and token spend would explode. NORA bakes domain priors directly into the agent body:

- `geo-specialist` lists CRS rules, dataset recommendations per domain, and spatial-method decision rules.
- `paper-writer` lists section-specific guidelines and geo conventions ("state spatial resolution for all raster data", "CRS specified in methods").
- `citation-manager` lists venue-specific formatting deltas (APA vs. IEEE vs. ACM).
- `hypothesis-generator` lists geo-specific hypothesis templates.

These blocks are the agent's "always-on" memory, compensating for the absence of conversational history.

**Design failure without it.** The agent falls back on generic best-practice, missing the discipline-specific checks (Moran's I on residuals, spatial CV vs. random CV, EPSG codes for analysis vs. storage vs. display) that distinguish publishable research from plausible-sounding output.

---

### 9. Structured Output Format (Return Schema)

A concrete Markdown/JSON template for the final return payload, with named fields and example values.

**Why required.** The parent skill needs to locate specific values (a score, a top-ranked gap, a decision verdict) without re-parsing prose. NORA agents declare these templates literally — the reviewer's `Editor Summary` block, the synthesis analyst's matrix columns, the hypothesis generator's `Overall: X.X/10` line, the writer's `Score: X.X (N:X, R:X, L:X, C:X, I:X)` signature.

The template serves three consumers:

1. **The agent itself** — a checklist of what must appear in its return.
2. **The parent skill** — a parsing anchor.
3. **Future humans** — a documented expectation when outputs need audit.

**Design failure without it.** Output formats drift between invocations; parser regex and downstream skills break every time the agent's phrasing shifts.

---

### 10. Cold-Read Discipline (Evaluator Agents Only)

For reviewer agents, an explicit instruction to evaluate the artifact without the author's framing.

**Why required.** The `peer-reviewer` agent simulates three external reviewers (methods expert, domain specialist, applications reviewer). Its value is precisely that the sub-context has no memory of how the draft was produced. Cold-read discipline means the agent reads the artifact on disk and produces a verdict as if encountering the work for the first time.

**Design failure without it.** The reviewer inherits the author's justifications from the parent context, converging on an agreeable review that misses the blind spots a real reviewer would surface.

---

### 11. Cost and Parallelism Awareness

A note on whether the agent can be invoked in parallel with others and an estimate of its typical token footprint.

**Why required.** Each agent invocation spawns a sub-context billed independently. Orchestrator skills must know:

- **Independent agents** — `literature-scout` and `geo-specialist` (for dataset suggestions) can run concurrently; the orchestrator should dispatch them in a single message with multiple Agent tool calls.
- **Sequential-only agents** — `synthesis-analyst` must finish before `gap-finder` starts; `paper-writer` must finish before `peer-reviewer`.
- **Heavy agents** — `synthesis-analyst` reads the entire paper-cache and can consume 50k+ input tokens; the orchestrator should batch its calls.

**Design failure without it.** The orchestrator serialises work that could run in parallel (wasting wall-clock time) or parallelises work with data dependencies (producing inconsistent artifacts).

---

### 12. Error and Degradation Handling

An explicit list of failure modes and the agent's prescribed response.

**Why required.** Agents cannot ask the user for help mid-run. Every foreseeable failure must have a deterministic response documented in the agent body:

- `literature-scout` — "If < 20 papers found: broaden keywords (add synonyms, relax year filter to 2015+) and retry."
- `orchestrator` — "API failure in literature-scout: log, retry once, fall back to cached papers."
- `paper-writer` — escalation rubric mapping self-score ranges to revision directives (Major / Moderate / Minor).

**Design failure without it.** The agent halts silently on the first unfamiliar failure, leaving the caller with an empty return and no diagnostic trail.

---

### 13. Audit Contribution

Every agent must either append to `output/PROJ_NOTES.md` itself or return enough metadata for the parent skill to log on its behalf.

**Why required.** The audit trail established at the skill level must extend into agent calls; otherwise the provenance chain breaks. When a reviewer later asks "which agent generated this section?", the log must answer unambiguously.

**Design failure without it.** Artifacts arrive in `output/` with no record of which agent in which invocation produced them, making regression impossible when an agent's prompt is later tuned.

---

## Part II: Advanced Design Disciplines for Agent Optimisation

The required sections above make agents safe and composable. The patterns below make them fast, robust, and evolvable.

---

### A. Agent Contract Tests

**Current state.** Agent I/O contracts are described in prose and verified by running the full pipeline.

**Optimisation.** Add a `.claude/agents/tests/<agent>/` directory with synthetic input fixtures and expected-output schemas:

```
.claude/agents/tests/peer-reviewer/
  ├── fixture_draft_strong.md      → expect Accept / Minor Revision
  ├── fixture_draft_weak_methods.md → expect Major Revision, flag methods
  └── fixture_no_results.md        → expect Major Revision, flag results
```

**Why.** Contract tests catch prompt regressions (an edit that silently changes the return schema) before they reach the pipeline. They also document expected behaviour at boundary conditions, which prose alone cannot.

---

### B. Parallel Invocation Manifest

**Current state.** Parallelism is implicit — the orchestrator decides per-stage whether to dispatch agents concurrently.

**Optimisation.** Each agent declares its parallelism class in frontmatter:

```yaml
parallelism:
  class: independent   # independent | depends_on: [<agent>] | global_singleton
  max_concurrent: 3
```

**Why.** The orchestrator can validate a parallel dispatch plan against declared classes before invoking, catching dependency violations statically instead of after a failed run.

---

### C. Return-Payload JSON Schema

**Current state.** Return formats are documented as Markdown templates with example values.

**Optimisation.** Ship a JSON Schema alongside each agent:

```
.claude/agents/schemas/peer-reviewer.schema.json
```

**Why.** Parent skills can validate agent output programmatically, rejecting malformed returns with a clear diagnostic instead of silently consuming a partial payload. Schemas also enable stricter downstream parsing without LLM fallback.

---

### D. Persona Composition over Inheritance

**Current state.** Each agent's persona and expertise are embedded verbatim in its body.

**Optimisation.** Extract shared domain knowledge into reusable blocks under `.claude/agents/_shared/`:

```
.claude/agents/_shared/geo_conventions.md   → included by geo-specialist, paper-writer, synthesis-analyst
.claude/agents/_shared/apa7_rules.md        → included by citation-manager, paper-writer
```

**Why.** Domain rules that live in three agents drift apart over time. Shared blocks keep the rules synchronised and make a single edit propagate to every consumer.

---

### E. Cold-Read Assertion

**Current state.** Reviewer agents rely on instructions to ignore author context.

**Optimisation.** The orchestrator strips any author-supplied rationale from the payload before invoking a reviewer, and the reviewer asserts `author_context_present == false` before proceeding. If the assertion fails, the review halts with a diagnostic instead of producing a tainted review.

**Why.** The cold-read property must be structurally enforced, not just prompted. A prompt rule can be overridden by a chatty caller; a payload check cannot.

---

### F. Token-Budget Declaration

**Current state.** Token footprint is implicit; cost surprises surface only in post-run accounting.

**Optimisation.** Each agent declares an expected input/output token range in frontmatter, and the orchestrator refuses to invoke it when the assembled payload exceeds the upper bound.

```yaml
token_budget:
  input_max: 80000
  output_max: 4000
```

**Why.** Prevents runaway dispatches that would time out or blow the context window. Makes per-agent cost legible in the orchestrator's pre-flight planning.

---

### G. Reviewer Ensemble for High-Stakes Gates

**Current state.** `peer-reviewer` simulates three reviewers inside one sub-context.

**Optimisation.** For high-stakes gates (final paper acceptance, contract-violation calls), dispatch three independent `peer-reviewer` invocations in parallel sub-contexts and aggregate. Mid-stakes gates keep the single-invocation triple-reviewer persona.

**Why.** Three independent sub-contexts cannot influence each other; a single sub-context simulating three reviewers risks internal consensus bias. The cost is 3x review tokens, paid only where the gate is worth it.

---

### H. Reviewer Memory (Adversarial Continuity)

**Current state.** Agent invocations are stateless; reviewer memory lives only in files (`memory/REVIEWER_MEMORY.md`) when the calling skill persists it.

**Optimisation.** Reviewer agents explicitly read and append to a persistent reviewer memory file, so suspicions raised in round N survive into round N+1 even across sessions.

**Why.** The `auto-review-loop` skill already supports this at the skill level for Codex MCP. Pushing it into the agent body extends the same adversarial continuity to local Claude-subagent reviewers, closing a quality gap in the fallback path.

---

### I. Capability Probe Instead of Static Allowlists

**Current state.** Agents declare tool allowlists statically.

**Optimisation.** Agents additionally declare capability tags (`retrieves_papers`, `formats_citations`, `reviews_spatial_methods`). Orchestrators select agents by capability, not by name, allowing drop-in replacement when a better agent exists.

**Why.** Decouples orchestrators from agent names, so swapping `literature-scout` for a future `semantic-scout-v2` requires changing zero caller code.

---

### J. Agent Versioning and Deprecation

**Current state.** Agents are edited in place; prior versions are reachable only through git history.

**Optimisation.** Agents carry a `version` field and support side-by-side coexistence (`peer-reviewer@1`, `peer-reviewer@2`). The orchestrator pins a version per pipeline run.

**Why.** Prompt edits to a reviewer agent silently change every downstream score. Versioning makes prompt evolution auditable and lets experimental prompts ship without disturbing the production pipeline.

---

## Part III: Concise Reference Table

### Required Sections

| # | Section | Purpose | Failure Mode If Missing |
|---|---------|---------|------------------------|
| 1 | YAML Frontmatter | Name, description, tool allowlist — the machine-readable contract | Mis-routing; unbounded tool access in an unattended sub-context |
| 2 | Persona and Role Statement | Seeds role-consistent behaviour in a fresh context | Generic assistant behaviour; role overlap |
| 3 | Context Isolation Contract | Declares what the agent reads from disk vs. expects from args | Hallucinated context; confidently wrong output |
| 4 | Single-Responsibility Scope | One discrete subtask per agent | Composite agents that cannot be parallelised or audited |
| 5 | Narrow Tool Allowlist | Least-privilege enforcement per agent | Allowlist creep; reviewer that overwrites what it reviews |
| 6 | Deterministic I/O Contract | Structured input and output shape | Freeform prose that downstream skills cannot parse |
| 7 | Evaluator-vs-Producer Role Lock | Enforces generator–evaluator separation at the agent layer | Self-validating loops; mode collapse |
| 8 | Persona-Grounded Expertise | Embedded domain priors (CRS, APA, spatial methods) | Generic output that misses discipline-specific checks |
| 9 | Structured Output Format | Named fields, parser anchors, audit template | Format drift between runs; broken downstream parsers |
| 10 | Cold-Read Discipline (evaluators) | Reviewer sees artifact without author rationale | Agreeable reviews that inherit author blind spots |
| 11 | Cost and Parallelism Awareness | Declares whether agent can run concurrently and its typical budget | Wasted wall-clock or data-race artifacts |
| 12 | Error and Degradation Handling | Deterministic responses to foreseeable failures | Silent halts with no diagnostic trail |
| 13 | Audit Contribution | PROJ_NOTES.md entry or metadata for caller to log | Broken provenance chain across the skill–agent boundary |

### Advanced Optimisations

| ID | Optimisation | What It Adds | Key Benefit |
|----|--------------|--------------|-------------|
| A | Agent Contract Tests | Synthetic fixtures + expected output schemas per agent | Catches prompt regressions before they reach the pipeline |
| B | Parallel Invocation Manifest | Declared parallelism class and max_concurrent | Static validation of dispatch plans |
| C | Return-Payload JSON Schema | Machine-checkable output schema per agent | Programmatic parser validation; cleaner downstream code |
| D | Persona Composition | Shared domain blocks under `_shared/` | Rules stay synchronised across agents |
| E | Cold-Read Assertion | Orchestrator strips author rationale; reviewer asserts absence | Structural (not just prompted) enforcement of cold-read |
| F | Token-Budget Declaration | Declared input/output token bounds per agent | Pre-flight cost control; no runaway dispatches |
| G | Reviewer Ensemble | Three independent parallel reviewer sub-contexts | Eliminates intra-context consensus bias at high-stakes gates |
| H | Reviewer Memory | Persistent reviewer suspicions across rounds | Adversarial continuity for local-fallback reviewers |
| I | Capability Probes | Select agents by capability tags, not by name | Drop-in agent replacement without caller changes |
| J | Agent Versioning | Side-by-side versioned agents with pipeline pinning | Auditable prompt evolution; safe experimentation |

---

## Part IV: How Agent Principles Relate to Skill Principles

Skills and agents are complementary, not redundant. The relationship is:

| Concern | Skill layer | Agent layer |
|---|---|---|
| Context | Runs in parent context | Runs in isolated sub-context |
| Composition | Chains other skills and agents | Is a leaf — does not call other agents |
| State | Reads and writes canonical files; resumable via checkpoints | Stateless per invocation; disk is the only memory |
| Scope | A stage of the pipeline (many subtasks) | One discrete subtask inside a stage |
| Tool allowlist | Broad (workflow-level) | Narrow (task-level) |
| Parallelism | One skill at a time in the parent context | Multiple agents in parallel sub-contexts |
| Evaluator role | Orchestrates evaluator invocation | Can *be* the evaluator |
| Audit | Appends to PROJ_NOTES.md | Contributes metadata for the skill to log |

Skills encode **workflow intent**. Agents encode **specialist execution**. The harness (hooks, handoff.json, memory files) encodes **guarantees** that span both. Together they form the three-layer discipline that makes NORA's long-horizon autonomous research pipeline tractable.

---

*This document codifies the design discipline observed across all nine specialist agents of the Night Owl Research Agent. It should be treated as a living standard — updated as new agents are added and as advanced optimisations are adopted.*
