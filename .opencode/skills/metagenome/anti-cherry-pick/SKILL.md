---
name: anti-cherry-pick
description: Use when reporting any analysis results — enforces that all samples are reported, all analyses are included, failures are documented, and no selective reporting occurs
---

# Anti-Cherry-Pick (Discipline Layer)

## Overview

Cherry-picking results — reporting only favorable findings while hiding unfavorable ones — is scientific misconduct. This skill enforces complete, honest reporting of all analysis outputs.

**Core principle:** All samples. All results. All failures recorded.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

<IRON-LAW>
ALL SAMPLES MUST BE REPORTED. ALL ANALYSES MUST BE INCLUDED. ALL FAILURES MUST BE DOCUMENTED.

You may NOT:
- Silently exclude samples that don't fit the narrative
- Report only the differential abundance method that gives more significant results
- Hide diversity results that contradict the main story
- Omit failed analyses from the report
- Select favorable rarefaction depths after seeing results
- Report only certain taxonomic levels because they look better
</IRON-LAW>

## What Must Be Reported

### Samples
- ALL samples that passed QC must be included in analysis
- If samples are excluded, document EXACTLY why (with QC evidence)
- Sample exclusion must happen BEFORE analysis, not after seeing results
- Report total samples, samples excluded, and reasons

### Analyses
- ALL planned analyses from analysis-protocol.yaml must be reported
- If multiple differential abundance methods were run, report ALL
- If results differ between methods, discuss the discrepancy honestly
- Null results (no significant differences) are RESULTS, not failures

### Failures
- Document in `docs/04_execution/negative-results.md`:
  - Analyses that failed to run (with error messages)
  - Analyses that produced null results
  - Unexpected findings that contradict expectations
  - Pipeline steps that needed to be rerun

## Specific Cherry-Pick Patterns to Watch

| Pattern | Why It's Wrong | What To Do |
|---------|---------------|------------|
| Excluding outlier samples after analysis | Post-hoc exclusion biases results | Exclude only with pre-defined QC criteria |
| Reporting DESeq2 but not ANCOM-BC | Methods may disagree; hiding disagreement is dishonest | Report both, discuss discrepancy |
| Showing genus-level but not species-level | Species-level may not support claims | Report multiple levels |
| Reporting only significant comparisons | Non-significant comparisons are informative | Report all planned comparisons |
| Adjusting significance threshold post-hoc | Threshold was locked in G2 | Use locked threshold only |

## Red Flags — STOP

- "Let me just remove this outlier sample"
- "The other method didn't give significant results, so I'll use this one"
- "This comparison isn't interesting, I'll skip it"
- "The species-level results are noisy, let me show genus only"
- "These negative results aren't relevant"
- Reporting different numbers of samples in different analyses

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "The outlier is clearly contaminated" | If it passed QC, include it. If contaminated, document the evidence. |
| "Both methods show the same trend" | If true, report both — it strengthens the finding. If not, report the discrepancy. |
| "Null results don't add anything" | Null results prevent others from wasting time. Report them. |
| "The sample was a technical failure" | Document the failure. Don't silently remove. |
| "This analysis wasn't in the original plan" | If you ran it, report it. Ad-hoc analyses that work aren't bonus findings — they're potential cherry-picks. |
| "I'll include it in supplementary" | Supplementary is fine, but don't hide it there to avoid discussion. |

## The Bottom Line

```
If you ran it, report it.
If it failed, document it.
If it's inconvenient, that's not a reason to hide it.
```

Complete reporting is the foundation of scientific integrity. No exceptions.
