---
name: data-quality-alert
description: "Use when data quality signals indicate the input data may be insufficient, contaminated, or unsuitable for the planned analysis — forces honest quality classification and escalates to user before proceeding"
---

# Data Quality Alert (Meta-Control Layer — Metagenome)

## Overview

Proceeding with poor-quality data produces unreliable results that waste time and erode trust. This skill forces honest classification of data quality and checks whether the data can support the planned analyses. It triggers **automatically** during Phase 1 (data-assessment) and Phase 4 (pipeline-execution), and **on-demand** whenever quality signals are detected.

**Core principle:** Classify data quality honestly. Do not proceed on hope.

> **[IRON-LAW]** Violating the letter of this rule is violating the spirit of this rule.

## The Iron Law

```
CLASSIFY DATA QUALITY HONESTLY. DO NOT OVERSTATE. PROBLEMS CAUGHT HERE SAVE WEEKS OF WASTED ANALYSIS.
```

## When This Runs

1. **Phase 1 (data-assessment):** Initial quality profiling — can this data support the planned analyses?
2. **Phase 4 (pipeline-execution):** Runtime quality checks — are intermediate results within expected ranges?
3. **Any phase:** When quality anomalies are detected in any output

If classification **downgrades** between Phase 1 and Phase 4, **WARN the user immediately**.

## Trigger Conditions

Any **ONE** of these activates this skill:

| Signal | Threshold | Implication |
|--------|-----------|-------------|
| Per-sample read count too low | <10,000 reads (amplicon) or <1Gbp (shotgun) | Insufficient depth for planned analysis |
| Excessive quality filtering loss | >40% reads removed by QC | Sample preparation or sequencing issues |
| High host contamination | >50% host reads (after host removal) | Low microbial biomass or extraction issue |
| Adapter contamination persists | >5% reads with adapters after trimming | Trimming parameters incorrect or library prep issue |
| Extreme batch effects | PCoA shows clustering by batch, not biology | Confounded experiment, results may be artifacts |
| Negative control contamination | Negative controls have >1000 reads or share abundant taxa with samples | Kit contamination or cross-contamination |
| Uneven sequencing depth | >10x variation across samples in same group | Normalization may mask or create false signals |
| Low complexity | >30% duplicate reads (shotgun) | Library complexity issue; effective coverage much lower than raw |

## Quality Classification Flow

> **[HARD-GATE]** The agent MUST execute all steps in order when triggered.

### Step 1 — Quantify the Problem

For each triggered signal, provide:
- **Metric name** and **observed value**
- **Expected range** for this data type
- **Number of samples affected** (all, subset, single outlier)

Be specific. "Some samples have low read counts" is not acceptable. "12 of 30 samples have <5,000 reads after QC (expected: >10,000)" is required.

### Step 2 — Classify Overall Data Quality

| Grade | Definition | Can Proceed? |
|-------|------------|-------------|
| **A — High Quality** | All metrics within expected ranges | ✅ Proceed as planned |
| **B — Acceptable with Caveats** | Minor issues; analyses possible with adjustments | ✅ Proceed with documented caveats and parameter adjustments |
| **C — Marginal** | Significant issues; only a subset of planned analyses are reliable | ⚠️ Reduce scope, warn user, get approval to proceed |
| **D — Insufficient** | Fundamental quality problems; most analyses will be unreliable | 🛑 STOP. Present options to user. |
| **F — Unusable** | Data cannot support any meaningful metagenomics analysis | 🛑 STOP. Recommend re-sequencing or project termination. |

### Step 3 — Impact Assessment

For grades B–F, map each quality issue to its downstream impact:

```
Quality Issue → Affected Analysis Steps → Impact on Research Questions

Example:
"Low sequencing depth (12 samples <5k reads)"
  → Alpha diversity: underestimated richness
  → Beta diversity: increased noise, reduced power
  → Differential abundance: cannot detect low-abundance taxa
  → Research Q2 ("Rare taxa differences"): CANNOT BE ANSWERED with current data
```

### Step 4 — Present Options to User

For Grade **A**: Proceed normally (no user action needed).

For Grade **B**: Present caveats, get acknowledgment, document in `project-log.md`.

For Grade **C**:
```
⚠️ DATA QUALITY ALERT — Grade C (Marginal)
The following analyses are UNRELIABLE with current data quality:
- [list affected analyses]

Options:
a) PROCEED with reduced scope (remove unreliable analyses)
b) REPROCESS with stricter/looser QC parameters (specify)
c) EXCLUDE problematic samples (list them) and proceed
d) STOP and request additional data / re-sequencing

Please choose. Agent cannot proceed without your decision.
```

For Grade **D** or **F**:
```
🛑 DATA QUALITY ALERT — Grade D/F (Insufficient/Unusable)
Current data quality cannot support reliable metagenomics analysis.

Root cause assessment: [specific issues]

Options:
a) ATTEMPT analysis with severe caveats (results will be exploratory only)
b) REQUEST re-sequencing / additional samples
c) TERMINATE this analysis branch

Please choose. Agent cannot proceed without your decision.
```

## Metagenomics-Specific Quality Traps

| Trap | Why It's Dangerous |
|------|-------------------|
| Low-biomass samples analyzed like high-biomass | Contamination dominates; real signal is buried |
| Ignoring negative controls | Cannot distinguish real taxa from kit contaminants |
| Assuming uniform depth across samples | Rarefaction or normalization artifacts |
| Trusting raw read counts without QC | Garbage in → garbage out |
| Batch effects dismissed as "biology" | Confounded results published and later retracted |
| Merged runs without checking compatibility | Different error profiles corrupt denoising |

## Red Flags — STOP

- Proceeding with Grade D data without user approval
- Ignoring negative control signals
- Classifying Grade C data as Grade B to avoid user interruption
- Skipping quality checks to "save time"
- Claiming "the analysis will correct for it" without specifying how
- Hiding the number of affected samples in vague language

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Most samples are fine, we can exclude the bad ones" | Excluding samples reduces power. Quantify the impact before deciding. |
| "Rarefaction will normalize everything" | Rarefaction discards data and cannot fix fundamental quality issues. |
| "The downstream tools handle low-quality input" | Tools produce output regardless; they don't validate biological meaning. |
| "We can add a caveat in the discussion" | Caveats don't rescue unreliable analyses. Fix the input or reduce scope. |
| "Other studies used similar quality data" | Other studies may have been wrong. Don't replicate their mistakes. |
| "Re-sequencing is too expensive" | Publishing wrong results is more expensive — in reputation and wasted effort. |

## The Bottom Line

```
Honest quality assessment now → appropriate analysis scope → trustworthy results
Ignored quality warnings now → months of work → unreliable conclusions → retraction risk
```

Classify honestly. Quantify impact. Present options. Let the user decide.
