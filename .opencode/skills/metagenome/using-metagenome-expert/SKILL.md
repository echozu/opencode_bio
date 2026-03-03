---
name: using-metagenome-expert
description: Use when starting any gut metagenome analysis conversation — establishes how to find and use metagenome analysis skills, requiring Skill tool invocation before ANY response including clarifying questions
---

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a metagenome analysis skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. This is not optional. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

# ABSOLUTE RULE #1: ONE PHASE PER TURN

<IRON-LAW>
YOU MUST COMPLETE ONLY **ONE PHASE** PER RESPONSE. After completing a phase or reaching a gate, you MUST:

1. Present the phase deliverables and/or gate checklist to the user
2. **END YOUR RESPONSE AND WAIT FOR THE USER TO REPLY**
3. Only proceed to the next phase AFTER the user explicitly approves

**THIS IS THE SINGLE MOST IMPORTANT RULE IN THE ENTIRE SYSTEM.**

Violating this rule — even once — collapses the entire analysis workflow into a shallow one-shot demo. The phases exist because each one requires human judgment before the next can begin.

### What "end your response" means

- After Phase 0: present `project-anchor.yaml` summary → **STOP. Wait for user.**
- After Phase 1 + G1: present G1 checklist → **STOP. Wait for user.**
- After Phase 2: present validated analysis design → **STOP. Wait for user.**
- After Phase 3 + G2: present frozen analysis-protocol.yaml → **STOP. Wait for user.**
- After G3: present execution readiness check → **STOP. Wait for user.**
- After Phase 4 exploratory: present QC/pipeline report + options (proceed / adjust / return) → **STOP. Wait for user decision.**
- After Phase 4 full: present results summary → **STOP. Ask: "Are results sufficient? Shall I proceed to results integration?"**
- After Phase 5 + G4: present argument blueprint → **STOP. Ask: "Shall I proceed to report generation?"**
- During Phase 6: present EACH SECTION individually → **STOP. Wait for user feedback on that section.**

### What counts as user approval

- Explicit: "approved", "yes", "proceed", "looks good, go ahead", "继续", "可以"
- NOT approval: silence, no response, "ok" (ambiguous), or your own judgment that "it looks fine"

### Fast Mode

If the user says **"fast mode"**, **"快速模式"**, or **"combine phases"** at the start:
- Combine Phase 0 + Phase 1 into a single turn (but still present both deliverables)
- After each gate, still STOP and wait for approval (gates are never combined)
- Multi-agent deliberation rounds are reduced to max 3 (instead of 5)
- Per-section polishing rounds are reduced to max 2 (instead of 5)

**Fast Mode does NOT skip any phase or gate.** It only reduces stops and deliberation rounds. If the user wants to skip phases entirely, they must explicitly say which phases to skip.

### Rationalization Prevention — One Phase Per Turn

| Your thought | Why it's wrong |
|-------------|---------------|
| "Let me also run QC since the data is ready" | ONE PHASE PER TURN. Stop and wait. |
| "This is simple 16S data, I can do all phases" | No project is simple enough to skip human checkpoints. |
| "The user will get impatient if I stop" | The user will get bad results if you don't stop. |
| "I already know what the user will say" | You don't. That's why you ask. |
| "Let me just quickly check diversity too" | "Quickly" = cutting corners. Stop. |
| "Phase 2 isn't needed for standard analysis" | Phase 2 is ALWAYS required. Adversarial review catches blind spots. |
</IRON-LAW>

# ABSOLUTE RULE #2: NO PHASE IS OPTIONAL

<IRON-LAW>
ALL SEVEN PHASES (0 through 6) ARE MANDATORY FOR ALL ANALYSIS TYPES.

Specifically:
- **Phase 2 (Analysis Design Validation) is REQUIRED for all data types.** "It's just standard 16S analysis" is the #1 rationalization for skipping validation. Standard analysis without adversarial review produces shallow, undefendable findings.
- **Phase 3 (Pipeline Design) is REQUIRED** even if the analysis seems straightforward. Locking parameters and databases prevents goalpost-moving later.
- **Phase 5 (Results Integration) requires the full multi-agent discussion.** Skipping the discussion panel and jumping to report produces thin, report-like outputs.

The ONLY exception: the user explicitly says "skip Phase X" — and even then, warn them of consequences.
</IRON-LAW>

# ABSOLUTE RULE #3: MULTI-AGENT DELIBERATION MUST EXECUTE

<IRON-LAW>
Multi-agent deliberation is MANDATORY at the following phases:
- Phase 1 (data-assessment): 3 agents × max 5 rounds — data type selection and QC strategy
- Phase 2 (analysis-design-validation): 3 agents × max 5 rounds — adversarial review of analysis plan
- Phase 3 (pipeline-design): 3 agents × max 5 rounds — parameter and tool selection review
- Phase 5 (results-integration): 3 agents × max 5 rounds — story design and claim validation
- Phase 6 (report-generation): per-section 3 agents + full-report 3 agents

This is NOT optional. Single-agent evaluation has blind spots. Dispatch ALL agents every round.
Follow the `multi-round-deliberation` skill protocol for loop, convergence, and non-convergence handling.
</IRON-LAW>

## How to Access Skills

Skills are loaded by name using the Skill tool. Each skill has a unique name defined in its SKILL.md frontmatter.

**To load a skill:** Use the skill tool with the skill name, e.g., `project-anchoring`, `parameter-lock`, etc.

## Tool Mapping for OpenCode

When skills reference tools, use these OpenCode equivalents:

- `Skill` tool → Use the Skill tool by name (e.g., `project-anchoring`)
- `TodoWrite` → `todowrite` tool
- `Task` with subagents → `task` tool
- `Read`, `Write`, `Edit` → `read`, `edit`, `write` tools
- `Bash` → `bash` tool
- `WebSearch` → `websearch` tool

# System Architecture

The Gut Metagenome Expert operates on three layers:

**Workflow Layer** — Phase-by-phase analysis flow (project-anchoring → data-assessment → analysis-design-validation → pipeline-design → pipeline-execution → results-integration → report-generation). These tell you WHAT to do next.

**Discipline Layer** — Cross-phase scientific rigor (parameter-lock, anti-cherry-pick, claim-evidence-alignment, qc-standards, contamination-check, reproducibility-enforcement, results-verification). These tell you WHAT RULES to follow at all times.

**Meta-Control Layer** — Project governance (scope-control, pivot-or-kill, data-quality-alert, analysis-validity-check). These tell you WHEN to stop, pivot, or escalate.

## Four Gates

Progress between phases requires passing gates:

- **G1 (Data & Path Confirmed)** — Between data assessment and analysis design
- **G2 (Pipeline Freeze)** — Between pipeline design and execution
- **G3 (Execution Readiness)** — Before full-scale pipeline execution
- **G4 (Report-Ready)** — Before report generation

No gate may be skipped. Each gate has a checklist that must be fully satisfied.

## Analysis Workflow Priority

When a user describes analysis intent, skills apply in this order:

1. Project anchored? → If no, invoke `project-anchoring` → **STOP and wait for user**
2. Data assessed? → If no, invoke `data-assessment` → present G1 → **STOP and wait**
3. Analysis design validated? → If no, invoke `analysis-design-validation` → **STOP and wait**
4. Pipeline designed? → If no, invoke `pipeline-design` → present G2 → **STOP and wait**
5. Executing pipeline? → If yes, invoke `pipeline-execution` → present results → **STOP and wait**
6. Results ready? → If yes, invoke `results-integration` → present G4 → **STOP and wait**
7. Generating report? → **ONLY** when user explicitly says "ready for report", invoke `report-generation`

## Available Skills (26)

### Workflow Skills — Phase-by-phase analysis flow

| Skill | Phase | When to use |
|-------|-------|-------------|
| `using-metagenome-expert` | Bootstrap | Core rules (already loaded). |
| `project-anchoring` | 0 | User describes analysis intent — anchor data type, goals, persona |
| `data-assessment` | 1 | QC profiling, tool selection, data type confirmation, G1 gate |
| `analysis-design-validation` | 2 | 3-agent adversarial review of analysis plan |
| `pipeline-design` | 3 | Parameter lock, database selection, G2 gate |
| `amplicon-analysis` | 4 | Type A: DADA2 → taxonomy → PICRUSt2 |
| `metagenome-assembly` | 4 | Type M: assembly → gene prediction → annotation |
| `metagenome-readbased` | 4 | Type R: MetaPhlAn3 → HUMAnN2/3 |
| `downstream-analysis` | 4 | Shared: diversity, differential, network analysis |
| `functional-annotation` | 4 | Functional gene mining (SBA, SCFAs, etc.) |
| `pipeline-execution` | 4 | Orchestrates execution, G3 gate |
| `results-integration` | 5 | Story design, claim-evidence check, G4 gate |
| `report-generation` | 6 | Per-section + full review writing |
| `multi-round-deliberation` | 1,2,3,5,6 | Multi-agent discussions iterate until convergence |
| `tool-recommendation` | Any | Context-aware metagenome tool selection |

### Discipline Skills — Scientific rigor (always active once triggered)

| Skill | Active from | What it enforces |
|-------|------------|------------------|
| `parameter-lock` | G2 → end | Analysis parameters cannot change without user permission |
| `anti-cherry-pick` | Phase 4 → end | All samples reported, failures recorded, no selective reporting |
| `claim-evidence-alignment` | Phase 5–6 | Every claim maps to specific evidence |
| `qc-standards` | Phase 1 → end | Minimum quality thresholds for reads, assemblies, annotations |
| `contamination-check` | Phase 1 → end | Host DNA, kit contamination, cross-contamination screening |
| `reproducibility-enforcement` | Phase 4 → end | Tool versions, database versions, commands logged |
| `results-verification` | Always | Domain sanity check before any status claim |

### Meta-Control Skills — Project governance

| Skill | Triggered by | What it does |
|-------|-------------|-------------|
| `scope-control` | Scope expansion | Forces scope reduction discussion with user |
| `pivot-or-kill` | 3 consecutive failures | Presents pivot/downgrade/kill options |
| `data-quality-alert` | Data quality degradation | Alerts user when data quality drops below thresholds |
| `analysis-validity-check` | Results anomaly | Checks whether results make biological sense |

## Analysis Type Awareness

Every decision must account for the data type (from project-anchor.yaml):

- **Type A (Amplicon)**: 16S/18S/ITS rRNA sequencing. DADA2 → ASV → taxonomy → diversity. Focus: community structure.
- **Type M (Metagenome-Assembly)**: Shotgun WGS, assembly-based. MEGAHIT/metaSPAdes → gene prediction → MEGAN/eggNOG. Focus: gene catalog, MAGs.
- **Type R (Metagenome-ReadBased)**: Shotgun WGS, read-based. MetaPhlAn3 → HUMAnN2/3. Focus: taxonomic + functional profiling.
- **Type C (Combined)**: Both amplicon + shotgun data. Requires cross-validation and complementary analysis.

## User Progress Declaration (Jump-In)

If the user says any of:
- "I've already done QC" / "我已经做完质控了"
- "I'm at the diversity analysis stage" / "我在多样性分析阶段"
- "Skip to Phase 4" / "跳到第4阶段"
- "I have MetaPhlAn results" / "我有MetaPhlAn结果了"

Then:
1. ASK the user to confirm exactly what has been completed
2. VERIFY by checking for expected output files/artifacts
3. CREATE a partial project-anchor.yaml with completed phases marked
4. ENTER at the appropriate phase with a VALIDATION STEP first

<IRON-LAW>
Jump-in does NOT skip gates. When entering mid-flow:
- The GATE IMMEDIATELY BEFORE the target phase MUST be validated
- If artifacts from prior phases are missing, request them or return to earlier phase
- Document what was declared vs what was verified in project-anchor.yaml
</IRON-LAW>

### Jump-In Validation Checklist

| Target Phase | Required Artifacts | Validation |
|-------------|-------------------|------------|
| Phase 2 | QC report, clean reads, data type confirmed | Verify QC stats meet thresholds |
| Phase 3 | Validated analysis plan, tool chain confirmed | Verify tool versions available |
| Phase 4 | Locked analysis-protocol.yaml, databases ready | Verify parameter completeness |
| Phase 5 | Complete pipeline outputs, experiment log | Verify all samples processed |
| Phase 6 | Argument blueprint, claim-evidence map | Verify story coherence |

## Hot Heart Platform Integration

For interpretation and evidence backing, leverage these resources when available:
- **R·base (热心肠数据库)**: Reference gut microbiome composition data for comparison
- **Daily Report (每日科研速递)**: Latest gut microbiome research findings for contextualization
- **iMeta**: Methodological references for metagenome analysis best practices

## Red Flags — STOP

These thoughts mean you're rationalizing:

| Thought | Reality |
|---------|---------|
| "Let me do the next phase too" | ONE PHASE PER TURN. Stop and wait for user. |
| "Phase 2 isn't needed for this data" | Phase 2 is ALWAYS needed. Standard analysis still has blind spots. |
| "The results are done, let me write the report" | User must say "ready for report." Ask and wait. |
| "Let me just start running the pipeline" | Pipeline design and parameter lock come first. |
| "This is a simple 16S analysis" | Simple analyses still need QC validation and parameter locking. |
| "I know what tool to use" | Tool selection must be discussed, locked, and documented. |
| "Let me run diversity analysis first" | No execution before G2 (pipeline freeze). |
| "The results look biologically reasonable" | Run domain sanity check. Show numbers. Evidence before claims. |
| "Standard parameters are fine" | Standard for WHOSE data? Lock parameters for THIS dataset. |
| "I'll check contamination later" | Contamination invalidates everything downstream. Check NOW. |

## Skill Types

**Rigid** (parameter-lock, anti-cherry-pick, results-verification): Follow exactly. No adaptation.

**Flexible** (data-assessment, pipeline-design): Adapt principles to context and data type.

The skill itself tells you which.

## User Instructions

User instructions say WHAT, not HOW. "Analyze this 16S data" or "Run metagenome pipeline" doesn't mean skip the analysis workflow. The workflow tells you HOW.
