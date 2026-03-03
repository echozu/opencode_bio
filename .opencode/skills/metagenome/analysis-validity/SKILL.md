---
name: analysis-validity
description: "Use at every gate checkpoint and periodically during pipeline execution to verify that analysis progress matches the target study standards in terms of statistical rigor, biological plausibility, and methodological completeness"
---

# Analysis Validity (Meta-Control Layer — Metagenome)

## Overview

An analysis that claims clinical relevance with n=5 per group will be rejected. A study-grade analysis presented as exploratory wastes its own rigor. This skill keeps analysis ambition and execution aligned with the **target study standard** at every stage.

**Core principle:** Match ambition to evidence. Match evidence to standards.

> **[IRON-LAW]** Check analysis validity at every gate and periodically during Phase 4 execution.

## Study Standard Tiers

| Tier | Description | Typical Context |
|------|-------------|-----------------|
| **Tier 1 — Publication-Grade** | Full statistical rigor, complete methodology, reproducible | Journal submission, thesis |
| **Tier 2 — Report-Grade** | Solid analysis, documented methods, adequate statistics | Internal report, collaboration deliverable |
| **Tier 3 — Exploratory** | Preliminary analysis, hypothesis-generating, limited statistics | Pilot study, feasibility check |

The target tier is declared in `project-anchor.yaml` under `study_standard`.

## Gate-Specific Validity Checks

### G1 — Data Assessment Complete

*"Is the data quality sufficient for [target tier] analysis?"*

| Requirement | Tier 1 | Tier 2 | Tier 3 |
|-------------|--------|--------|--------|
| **Min samples per group** | ≥15 (power analysis recommended) | ≥8 | ≥3 |
| **Sequencing depth** | Verified adequate via rarefaction curves | Checked | Noted |
| **Negative controls** | Mandatory, analyzed | Recommended | Optional |
| **Batch information** | Recorded, plan to account for | Recorded | Noted |
| **Metadata completeness** | All confounders documented | Key variables documented | Basic metadata |

If data falls short of tier requirements → WARN user, suggest tier adjustment.

### G2 — Pipeline Design Frozen

*"Does the analysis design have sufficient rigor for [target tier]?"*

| Requirement | Tier 1 | Tier 2 | Tier 3 |
|-------------|--------|--------|--------|
| **Statistical framework** | Pre-specified primary tests + correction method | Named tests + FDR correction | Descriptive + basic tests |
| **Multiple testing correction** | Mandatory (BH, Bonferroni, or permutation) | Mandatory (BH minimum) | Recommended |
| **Effect size reporting** | Required for all primary comparisons | Required for key findings | Optional |
| **Confounders addressed** | Modeled or stratified | Acknowledged and discussed | Noted |
| **Power analysis** | Required pre-hoc or sensitivity analysis | Recommended | Not required |
| **Pipeline validation** | Mock community or spike-in validation | Tool benchmarks cited | Tool choice justified |

If design lacks rigor for the target tier → WARN user before freezing.

### G3 — Execution Complete

*"Is the executed analysis scale sufficient for [target tier]?"*

| Requirement | Tier 1 | Tier 2 | Tier 3 |
|-------------|--------|--------|--------|
| **Diversity analyses** | Alpha (≥3 metrics) + Beta (≥2 distances) + stats | Alpha + Beta + basic stats | Alpha or Beta |
| **Differential abundance** | ≥2 methods compared (e.g., DESeq2 + ANCOM-BC) | 1 established method | Any method |
| **Taxonomy resolution** | Species/ASV level with genus-level summary | Genus level | Phylum/Class |
| **Functional analysis** | Pathway + module + gene family | Pathway level | Optional |
| **Visualization** | Publication-quality, consistent style | Clear and labeled | Basic plots |
| **Reproducibility** | Complete scripts, seed-locked, environment logged | Scripts provided | Commands noted |

If execution falls short → WARN user, suggest scaling up or adjusting tier.

### G4 — Results Integration Complete

*"Does the evidence package meet [target tier] standards for reporting?"*

| Requirement | Tier 1 | Tier 2 | Tier 3 |
|-------------|--------|--------|--------|
| **Main figures** | ≥4, publication-quality | ≥3, clear | ≥2 |
| **Supplementary data** | Complete tables, additional analyses | Key tables | Optional |
| **Statistical reporting** | p-values, FDR q-values, effect sizes, CIs | p-values + FDR q-values | p-values |
| **Methods documentation** | Full reproducible protocol (STORMS compliant) | Detailed methods section | Methods summary |
| **Claim-evidence mapping** | Every claim ↔ specific figure/table/test | Key claims ↔ evidence | Observations noted |
| **Limitations discussed** | Comprehensive limitations section | Key limitations noted | Brief caveats |

## Misalignment Response

> **[HARD-GATE]** If current progress falls short of tier requirements at any gate, execute ALL steps:

1. **State the gap clearly:**
   *"Current analysis has alpha diversity with 1 metric (Shannon); Tier 1 expects ≥3 metrics (e.g., Shannon, Simpson, Chao1)."*

2. **Quantify the gap:**
   *"3 of 8 Tier 1 requirements are not met at G3."*

3. **Present two options:**
   - □ **Scale up:** Add the missing analyses/statistics to meet the target tier
   - □ **Adjust tier:** Downgrade to a tier where current analysis is sufficient

4. **Record the decision** in `project-anchor.yaml` under `study_standard`

```
⏸️ VALIDITY CHECK — [N] requirements not met for [Tier].
Please choose: (a) Scale up to meet Tier requirements, or (b) Adjust tier.
Agent cannot proceed without your decision.
```

## Metagenomics Validity Red Flags

| Red Flag | Why It Matters |
|----------|---------------|
| Claiming clinical relevance with n<15/group | Underpowered, unreliable effect estimates |
| Reporting p-values without FDR correction for >10 comparisons | Inflated false positive rate |
| Single diversity metric presented as "comprehensive" | Different metrics capture different aspects; one is never enough for Tier 1 |
| Differential abundance with only one method | Methods disagree frequently; consensus findings are more robust |
| No rarefaction curve but claiming "sufficient depth" | Cannot validate depth adequacy without evidence |
| Species-level claims from short amplicon reads | V3-V4 16S cannot reliably resolve to species |
| Functional claims from 16S data alone (PICRUSt only) | Predicted function ≠ measured function; must caveat heavily |
| Ignoring compositionality | Standard statistics on relative abundances can be misleading |

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "The results are significant so the methods must be adequate" | Significance without rigor is noise. Methods determine validity, not p-values. |
| "Other papers in the field use the same approach" | The field is improving. Aim for current best practices, not legacy methods. |
| "Adding more metrics won't change the conclusion" | Then it's cheap to add them and it strengthens the paper. Do it. |
| "Power analysis isn't standard in microbiome studies" | It's becoming standard. Being ahead of the curve is a strength. |
| "FDR correction makes everything non-significant" | That's the data telling you the effect may not be real. Listen. |
| "The reviewer probably won't notice" | Reviewers are increasingly rigorous about microbiome methods. They will notice. |

## Hot Heart Platform Integration

When checking analysis validity, cross-reference with:
- **R·base** for published standards in comparable gut microbiome studies
- **iMeta** guidelines for metagenomics reporting standards
- **Daily Report** for emerging best practices and methodological updates

## The Bottom Line

```
Match ambition to evidence. Match evidence to standards.
Misalignment in either direction wastes effort:
  - Over-ambitious claims + weak methods = rejection
  - Strong methods + timid claims = missed opportunity
```

Check at every gate. Quantify gaps. Present options. Let the user decide.
