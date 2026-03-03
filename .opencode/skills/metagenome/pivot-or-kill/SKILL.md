---
name: pivot-or-kill
description: "Use when 3 consecutive pipeline steps or analysis attempts fail to meet quality thresholds — forces honest status assessment and escalates the pivot/downgrade/kill decision to the user"
---

# Pivot or Kill (Meta-Control Layer — Metagenome)

## Overview

Repeated failure in metagenomics pipelines is signal, not noise. When 3 consecutive core analysis steps fail quality thresholds, **stop iterating and escalate**. The agent does not get to decide whether to continue — the user does.

**Core principle:** Honesty over optimism. Escalate over iterate.

> **[IRON-LAW]** Violating the letter of this rule is violating the spirit of this rule.

## The Iron Law

```
AFTER 3 CONSECUTIVE FAILURES, STOP RUNNING PIPELINES. ESCALATE TO USER.
```

No fourth attempt. No "quick parameter tweak." Escalate.

## Definition of "Failure" in Metagenomics Context

| Domain | Failure Criteria |
|--------|-----------------|
| **QC / Preprocessing** | >50% reads lost after filtering; adapter contamination persists after trimming; host removal eliminates >90% reads |
| **Amplicon (DADA2)** | Chimera rate >30%; ASV count <50 after denoising; merge rate <20% |
| **Assembly** | N50 <1kb after 2 assembly parameter sets; <50% reads mapping to contigs |
| **Binning** | <5 medium-quality MAGs from >10Gbp data; CheckM completeness <50% on all bins |
| **Taxonomy** | >60% reads unclassified at phylum level; database mismatch suspected |
| **Functional** | HUMAnN pathway coverage <10%; >80% unmapped after translated search |
| **Downstream stats** | No significant results after FDR correction across all primary comparisons |

A "failure" is defined as: the pipeline step was executed correctly (no code bugs) but the output does not meet the minimum quality threshold defined in `qc-standards`.

## Trigger and Escalation Flow

```
Failure #1 → Log it, diagnose, adjust parameters, retry
Failure #2 → Log it, diagnose deeper, try alternative tool/approach, retry
Failure #3 → STOP. Execute escalation protocol below.
```

> **[HARD-GATE]** After failure #3, the agent MUST NOT attempt a 4th fix without user approval.

## Escalation Protocol (4 Mandatory Steps)

### Step 1 — Summarize Status Honestly

State plainly:
- **What was tried** (each of the 3 attempts, with exact parameters)
- **What failed** (specific metrics vs. thresholds)
- **Trend direction** (improving, flat, or worsening)

> **[IRON-LAW]** Do NOT soften language. "All three denoising attempts produced <50 ASVs" is correct. "Results showed some variability in ASV yield" is evasion.

### Step 2 — Analyze Failure Root Cause

Classify the failure into one of these categories:

| Category | Description | Signal |
|----------|-------------|--------|
| **Data quality issue** | Input data fundamentally insufficient | All parameter variants produce similar poor results |
| **Protocol mismatch** | Wrong pipeline for this data type | E.g., using V3-V4 primers reference for ITS data |
| **Tool limitation** | Tool cannot handle this specific scenario | Known limitation documented in tool literature |
| **Database incompatibility** | Reference database not suitable | High unclassified rate despite adequate sequencing depth |
| **Biological reality** | The expected signal may not exist | Low-biomass samples, degraded DNA, genuine low diversity |
| **Implementation bug** | Code-level error | Should be caught by debugging, not this skill |

Be specific. "Something is off with the data" is not a root cause.

### Step 3 — Present Exactly Three Options

Present all three. No filtering, no pre-selecting.

**a) Pivot** — Change analysis approach.
- Specify: what changes (e.g., switch from assembly-based to read-based), what stays
- Estimated additional time
- Risk level (high/medium/low)
- Example: "Switch from MEGAHIT assembly to HUMAnN3 read-based profiling"

**b) Downgrade** — Lower analysis ambition.
- Specify: what analyses are simplified or removed
- What research questions can still be answered
- Example: "Drop strain-level analysis, focus on genus-level composition only"

**c) Kill** — Terminate this analysis branch.
- Archive all logs and intermediate results
- Document lessons learned in `project-log.md`
- Redirect effort to other research questions or data types
- Example: "Functional annotation is not feasible with this sequencing depth; focus on taxonomy only"

### Step 4 — User Decides

```
⏸️ PIVOT-OR-KILL DECISION REQUIRED
THE AGENT CANNOT MAKE THIS DECISION. PRESENT OPTIONS AND WAIT FOR USER.
```

Present the options. Stop. Do not nudge. Do not recommend. The user decides.

## Post-Decision Actions

| Decision | Required Actions |
|----------|-----------------|
| **Pivot** | Update `analysis-protocol.yaml` with new approach; re-run Phase 2 validation for changed branch; reset failure counter |
| **Downgrade** | Update `project-anchor.yaml` research questions; update `analysis-protocol.yaml`; document removed analyses in `future-work.md` |
| **Kill** | Archive branch in `results/archived/`; document failure analysis in `project-log.md`; remove from active pipeline |

## Red Flags — STOP

- Attempting a 4th fix without user consultation
- Downplaying failure severity ("close to working", "almost there", "just needs tuning")
- Blaming compute resources instead of examining the approach
- Framing continued iteration as "one last parameter sweep"
- Silently lowering quality thresholds instead of escalating
- Redefining "failure" to avoid triggering this skill

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "One more parameter set might work" | You said that twice already. Escalate. |
| "I think the database just needs updating" | You thought that before too. Three failures means the problem is deeper. Escalate. |
| "Killing this branch is too drastic" | Killing saves compute and user time for analyses that will work. It's responsible, not drastic. |
| "Let me just try a different k-mer size" | Parameter sweeping is not problem-solving. If 3 approaches failed, the issue is fundamental. |
| "The sample quality is borderline" | That's useful information. Maybe this sample set cannot support this analysis type. Present that honestly. |
| "Other studies got it to work" | Other studies had different data, different samples, different sequencing depth. Your data is your data. |

## The Bottom Line

```
3 failures → STOP → summarize honestly → analyze root cause → present options → user decides
```

Honesty is not pessimism. Escalation is not failure. Continuing blindly is.
